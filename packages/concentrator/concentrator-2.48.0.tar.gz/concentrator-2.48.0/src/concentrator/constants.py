from __future__ import (
    annotations,
)

from typing import (
    TYPE_CHECKING,
)

from m3.db import (
    BaseEnumerate,
)

from kinder.core.declaration_status.models import (
    DSS,
)


if TYPE_CHECKING:
    try:
        from typing import (
            TypedDict,
        )
    except ImportError:
        from typing_extensions import (
            TypedDict,
        )

    class DeclarationChanges(TypedDict):
        """Словарь данных изменения поля заявления."""

        field: str
        old_value: str
        new_value: str


MESSAGE_PLUGIN_SMEV3_REQUIRED = 'Для работы с данным функционалом необходимо подключить плагин'

# Разделить для идентификатора льготы и льготы в МО
DELIMITER_PRIV = '000'
# Муниципальные льготы приходят портала с типом 3
MUNICIPAL_TYPE = 3
# Поле комментария к привилегии, пришедшей с концентратора
PRIVILEGE_COMMENT = 'ConcentratorPrivilegeComment'


class ConcentratorDelegateDocType(BaseEnumerate):
    """
    Типы документов представителя в концентраторе
    """

    USSR_PASSPORT = 1
    ABROAD_USSR_PASSPORT = 2
    IDENTITY_CARD = 4
    CERTIFICATE_OF_RELEASE = 5
    MINMORFLOT_PASSPORT = 6
    MILITARY_ID = 7
    DIPLOMATIC_RF_PASSPORT = 9
    ABROAD_PASSPORT = 10
    CERTIFICATE_OF_REGISTRATION = 11
    RESIDENCE_PERMIT = 12
    REFUGEE_CERTIFICATE = 13
    TEMPORARY_IDENTITY_CARD = 14
    RF_PASSPORT = 21
    ABROAD_RF_PASSPORT = 22
    MARINE_PASSPORT = 26
    MILITARY_ID_RESERVE_OFFICER = 27

    values = {
        USSR_PASSPORT: 'Паспорт гражданина СССР',
        ABROAD_USSR_PASSPORT: 'Загранпаспорт гражданина СССР',
        IDENTITY_CARD: 'Удостоверение личности',
        CERTIFICATE_OF_RELEASE: 'Справка об освобождение',
        MINMORFLOT_PASSPORT: 'Паспорт Минморфлота',
        MILITARY_ID: 'Военный билет',
        DIPLOMATIC_RF_PASSPORT: 'Дипломатический паспорт гражданина РФ',
        ABROAD_PASSPORT: 'Иностранный паспорт',
        CERTIFICATE_OF_REGISTRATION: 'Свидетельство о регистрации ходатайства иммигранта о признании его беженцом',
        RESIDENCE_PERMIT: 'Вид на жительство',
        REFUGEE_CERTIFICATE: 'Удостоверение беженца',
        TEMPORARY_IDENTITY_CARD: 'Временное удостоверение личности гражданина РФ',
        RF_PASSPORT: 'Паспорт гражданина РФ',
        ABROAD_RF_PASSPORT: 'Загранпаспорт гражданина РФ',
        MARINE_PASSPORT: 'Паспорт моряка',
        MILITARY_ID_RESERVE_OFFICER: 'Военный билет офицера запаса',
    }


class ConcentratorChildrenDocType(BaseEnumerate):
    """
    Типы документов ребенка в концентраторе
    """

    BIRTH_CERTIFICATE = 3
    ABROAD_BIRTH_CERTIFICATE = 23

    values = {
        BIRTH_CERTIFICATE: 'Свидетельство о рождении',
        ABROAD_BIRTH_CERTIFICATE: 'Свидетельство о рождении выданное уполномоченным органом иностранного государства',
    }


class ResetDeclarationResponse:
    SUCCESS = 'Успех'
    ALREADY_ENROLLED = 'Ребенок уже зачислен'
    ALREADY_DIRECTED = 'Ребенок уже направлен в ДОО'
    SERVICE_IS_NOT_AVAILABLE = 'Сервис недоступен'

    RESET_AVAILABLE_STATUSES = [DSS.PRIV_CONFIRMATING, DSS.REGISTERED, DSS.WANT_CHANGE_DOU]

    RESPONSES = {
        DSS.ACCEPTED: ALREADY_ENROLLED,
        DSS.ARCHIVE: SUCCESS,
        DSS.DIDNT_COME: SUCCESS,
        DSS.DIRECTED: ALREADY_DIRECTED,
        DSS.DUL_CONFIRMATING: SUCCESS,
        DSS.MED_CONFIRMATING: SUCCESS,
        DSS.PRIV_CONFIRMATING: SUCCESS,
        DSS.REFUSED: SUCCESS,
        DSS.REGISTERED: SUCCESS,
        DSS.TUTOR_CONFIRMATING: SUCCESS,
        DSS.WANT_CHANGE_DOU: SUCCESS,
        DSS.ZAGS_CHECKING: SERVICE_IS_NOT_AVAILABLE,
        DSS.ACCEPTED_FOR_CONSIDERING: SUCCESS,
        DSS.RECEIVED: SUCCESS,
    }
