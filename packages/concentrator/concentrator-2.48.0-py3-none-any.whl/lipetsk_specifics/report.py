# coding: utf-8

import os

from excel_reporting import (
    report_gen,
)

from lipetsk_specifics.utils import (
    date2str,
)
from lipetsk_specifics.webservice.helpers import (
    get_priv_data,
)

from kinder.core.children.models import (
    Children,
    Delegate,
    DelegateTypeEnumerate,
)
from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.dict.models import (
    HNE,
    WorkType,
)
from kinder.core.helpers import (
    get_report_filepath,
    make_initials,
)
from kinder.plugins.lipetsk_specifics_noconc.helpers import (
    get_zags_act_place_value,
)
from kinder.plugins.privilege_attributes.models import (
    PrivilegeOwnerEnum,
)


class GenericPrintReport(report_gen.BaseReport):
    """Печать чего-угодно."""

    def __init__(self, template_path, vars=None, name=None):
        (self.base_name, self.result_name, self.result_url) = get_report_filepath('xls', name)

        if isinstance(template_path, list):
            template_name = os.path.join(*template_path)
        else:
            template_name = template_path

        self.template_name = os.path.join(os.path.dirname(__file__), template_name)
        self.vars = vars

    def collect(self, *args, **kwargs):
        return self.vars if self.vars else {}

    def get_result_url(self):
        return self.result_url


class PrintDeclarationWithPDReport(report_gen.BaseReport):
    """Печать заявления с обработкой ПД на карточке заявления"""

    template_name = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'templates/xls/print_declaration_with_pd.xls')
    )

    def __init__(self, context):
        super(PrintDeclarationWithPDReport, self).__init__()
        (self.base_name, self.result_name, self.result_url) = get_report_filepath('xls')

        self.context = context

    def collect(self):
        declaration = Declaration.objects.get(id=self.context.declaration_id)
        children = Children.objects.get(id=self.context.children_id)
        delegate = Delegate.objects.get(id=self.context.delegate_id)

        priv_conf_attr = get_priv_data(declaration)
        if priv_conf_attr:
            if priv_conf_attr.privilege_owner == PrivilegeOwnerEnum.CHILDREN:
                privilege_owner = children
            else:
                privilege_owner = priv_conf_attr.delegate
        else:
            privilege_owner = None

        res = {
            'mo_name': declaration.mo.name,
            'boss_fio': declaration.mo.boss_fio,
            'delegate_fio': delegate.fullname,
            'delegate_snils': delegate.snils,
            'delegate_series_number': ', '.join((delegate.dul_series or '', delegate.dul_number or '')),
            'delegate_passport_data': ', '.join((delegate.dul_issued_by or '', date2str(delegate.dul_date))),
            'delegate_birthday': date2str(delegate.date_of_birth),
            'delegate_address': delegate.address_full,
            'delegate_email': delegate.email,
            'delegate_phones': delegate.phones,
            'delegate_phone_for_sms': delegate.phone_for_sms,
            'children_fio': children.fullname,
            'children_types': self.get_children_types(delegate),
            'children_birthday': date2str(children.date_of_birth),
            'children_snils': children.snils,
            'children_birthplace': children.birthplace,
            'children_reg_address': children.reg_address_full,
            'children_address': children.address_full,
            'children_dul_series_number': '{0} {1}'.format(children.dul_series or '', children.dul_number or ''),
            'children_dul_date': date2str(children.dul_date),
            'children_zags_act_number': children.zags_act_number,
            'children_zags_act_date': date2str(children.zags_act_date),
            'children_zags_act_place': get_zags_act_place_value(children.zags_act_place),
            'children_health_need_not': self.get_health_need_not(children),
            'children_health_needs_all': self.get_health_needs_all(children),
            'declaration_units': ', '.join(
                declaration.declarationunit_set.values_list('unit__name', flat=True).order_by('ord')
            ),
            'declaration_desired_date': date2str(declaration.desired_date),
            'declaration_work_types': self.get_work_types(declaration),
            'declaration_has_privilege': self.get_has_privilege(priv_conf_attr),
            'privilege_owners': self.get_privilege_owners(priv_conf_attr),
            'privilege_owner_types': self.get_owner_types(priv_conf_attr),
            'privilege_owner_fio': privilege_owner.fullname if privilege_owner else '',
            'privilege_owner_snils': privilege_owner.snils if privilege_owner else '',
            'privilege_owner_birthday': (date2str(privilege_owner.date_of_birth) if privilege_owner else ''),
            'declaration_date': date2str(declaration.date),
            'delegate_transcript_sign': make_initials(delegate.surname, delegate.firstname, delegate.patronymic),
        }

        # отображение льгот
        res.update(self.get_privileges(declaration))

        return res

    def get_checkbox_value(self, checked=False):
        return '☑' if checked else '☐'

    def get_tuples(self, items, checked_func, args=None):
        """Генератор записей с чекбоксами"""
        for code, name in items:
            checked = self.get_checkbox_value(checked_func(args, code))
            yield dict(checked=checked, name=name)

    def get_children_types(self, delegate):
        items = [
            (DelegateTypeEnumerate.MOTHER, 'мать'),
            (DelegateTypeEnumerate.FATHER, 'отец'),
            (DelegateTypeEnumerate.LEX, 'законный представитель'),
        ]

        def checked_func(delegate, code):
            return delegate and delegate.type == code

        return [item for item in self.get_tuples(items, checked_func, delegate)]

    def get_health_need_not(self, children):
        """Наличие ОВЗ (отсутствует)"""
        items = [
            (HNE.NOT, 'потребность отсутствует;'),
        ]

        def checked_func(children, code):
            return children.health_need_id is None or children.health_need.code == code

        return [item for item in self.get_tuples(items, checked_func, children)]

    def get_health_needs_all(self, children):
        """Наличие ОВЗ (потребность имеется в группе для детей:)"""
        items = [
            (HNE.SPEACH, 'с тяжелыми нарушениями речи'),
            (HNE.PHONETICS, 'с фонетико-фонематическими нарушениями'),
            (HNE.DEAFNESS, 'глухих'),
            (HNE.HARDOFHEARTING, 'слабослышаших'),
            (HNE.AMAUROSIS, 'слепых'),
            (HNE.BLINDNESS, 'слабовидящих, с амблиопией, косоглазием'),
            (HNE.DISABLEMENT, 'с нарушением опорно-двигательного аппарата'),
            (HNE.BACKLIGHT, 'с умственной отсталостью легкой степени'),
            (HNE.BACKHARD, 'с умственной отсталостью умеренной, тяжелой'),
            (HNE.BACK, 'с задержкой психического развития'),
            (
                HNE.INVALIDITY,
                'со сложным дефектом (сочетание 2 или более недостатков в физическом и (или) психическом развитии)',
            ),
            (HNE.RESTRICTION, 'с аллергическими заболеваниями'),
            (HNE.PHTHISIS, 'с туберкулезной интоксикацией'),
            (HNE.SICK, 'часто болеющих и других категорий детей, нуждающихся в длительном лечении'),
            (HNE.OTHER, 'с иными ограниченными возможностями здоровья'),
            (HNE.AUTISM, 'с аутизмом'),
        ]

        def checked_func(children, code):
            return children.health_need and children.health_need.code == code

        return [item for item in self.get_tuples(items, checked_func, children)]

    def get_work_types(self, declaration):
        """Режим пребывания в организации"""
        items = [
            (WorkType.SHORT, 'кратковременное пребывание от 3 до 5 часов'),
            (WorkType.ABREV, 'сокращенный день 8-10 часов'),
            (WorkType.FULL, 'полный день 10,5-12 часов '),
            (WorkType.EXTEND, 'продленный день 13-14 часов'),
            (WorkType.ALLDAY, 'круглосуточное пребывание 24 часа'),
        ]

        def checked_func(declaration, code):
            return declaration.work_type and declaration.work_type.code == code

        return [item for item in self.get_tuples(items, checked_func, declaration)]

    def get_has_privilege(self, priv_conf_attr):
        """Наличие льготы на направление для зачисления ребенка
        в образовательной организации:"""
        items = [
            (True, 'да'),
            (None, 'нет'),
        ]

        def checked_func(priv_conf_attr, code):
            return (code and priv_conf_attr) or priv_conf_attr is code

        return [item for item in self.get_tuples(items, checked_func, priv_conf_attr)]

    def get_privilege_owners(self, priv_conf_attr):
        """Обладатель льготы:"""
        items = [
            (PrivilegeOwnerEnum.CHILDREN, 'ребенок'),
            (PrivilegeOwnerEnum.PARENT, 'родитель'),
            (PrivilegeOwnerEnum.DELEGATE, 'представитель*'),
        ]

        def checked_func(priv_conf_attr, code):
            return priv_conf_attr and priv_conf_attr.privilege_owner == code

        return [item for item in self.get_tuples(items, checked_func, priv_conf_attr)]

    def get_owner_types(self, priv_conf_attr):
        """Степень родства обладателя льготы"""
        if priv_conf_attr and (priv_conf_attr.privilege_owner != PrivilegeOwnerEnum.CHILDREN):
            delegate = priv_conf_attr.delegate
        else:
            delegate = None

        return self.get_children_types(delegate)

    def get_privileges(self, declaration):
        """Сведения о льготе"""

        privileges_set = set(declaration.declarationprivilege_set.values_list('privilege__name', flat=True))

        # условие сопоставления льгот по наименованию
        # в соответствии с приложенным
        # документом. В случае изменения названия льготы придется менять код
        mapping = {
            'priv_1': ['Дети из многодетных семей'],
            'priv_2': ['Дети-инвалиды', 'Дети из семей, в которых хотя бы один родитель инвалид'],
            'priv_3': ['Дети судей'],
            'priv_4': ['Дети прокуроров, помощников прокуроров, прокурорских работников'],
            'priv_5': ['Дети военнослужащих'],
            'priv_6': [
                'Дети сотрудников полиции',
                'Дети сотрудников полиции, погибших или умерших вследствие исполнения служебной деятельности',
            ],
            'priv_7': ['Дети сотрудника полиции, уволенного вследствие увечья или иного повреждения здоровья,'],
            'priv_8': ['Дети сотрудников Следственного комитета'],
            'priv_9': [
                'Дети сотрудников органов ФСИН',
                'Дети сотрудников Федеральной таможенной службы',
                'Дети сотрудников службы Наркоконтроля',
                'Дети сотрудников органов МЧС',
                'Дети сотрудников ФСИН, погибших или получивших увечья в связи с выполнением служебных обязанностей',
                'Дети сотрудников МЧС, погибших или получивших увечья в связи с выполнением служебных обязанностей',
                'Дети сотрудников Наркоконтроля, погибших или получивших увечья в связи с выполнением служебных обязанностей',
            ],
            'priv_10': ['Дети сотрудников органов ФСИН, МЧС, ФСКН и ФТС РФ,'],
            'priv_11': ['Дети участников контртеррористических операций'],
            'priv_12': [
                'Дети получивших лучевую болезнь, другие заболевания, и инвалиды вследствие чернобыльской катастрофы'
            ],
            'priv_13': [
                'Дети участников ликвидации последствий катастрофы на Чернобыльской АЭС',
                'Дети получивших лучевую болезнь, другие заболевания, и инвалиды вследствие чернобыльской катастрофы',
            ],
            'priv_14': ['Дети эвакуированных из зоны отчуждения и переселенных (переселяемых) из зоны отселения'],
            'priv_15': [
                'Дети граждан из подразделений особого риска, а также семей, потерявших кормильца из числа военнослужащих'
            ],
            'priv_16': ['Дети участников контртеррористических операций'],
            'priv_17': ['Дети участников контртеррористических операций'],
            'priv_18': [
                'Дети участников контртеррористических операций',
                'Дети военнослужащих по контракту, погибших или ставших инвалидами',
                'Дети военнослужащих, проходящих военную службу по контракту, '
                'уволенных с военной службы при достижении ими предельного возраста пребывания '
                'на военной службе, по состоянию здоровья или в связи '
                'с организационно-штатными мероприятиями',
                'Дети лиц, проходящих службу в войсках национальной '
                'гвардии Российской Федерации и имеющие специальные '
                'звания полиции, граждан, уволенных со службы в '
                'войсках национальной гвардии Российской Федерации',
            ],
            'priv_19': [
                'Дети военнослужащих, проходящих военную службу по контракту, '
                'уволенных с военной службы при достижении ими предельного возраста '
                'пребывания на военной службе, по состоянию здоровья или в связи с '
                'организационно-штатными мероприятиями'
            ],
            'priv_20': ['Дети сотрудников органов принудительного исполнения Российской Федерации по месту жительства'],
        }

        def checked_func(names):
            """Возвращает пустой/заполненный чекбокс, в зависимости
            от наличия соответствующех льгот в заявке"""
            return self.get_checkbox_value(any(1 for n in names for p in privileges_set if p in n))

        return dict((tag, checked_func(names)) for tag, names in list(mapping.items()))

    def get_result_url(self):
        return self.result_url
