from spyne.model.complex import (
    ComplexModel,
    XmlAttribute,
    XmlData,
)
from spyne.model.primitive import (
    Boolean,
    Date,
    DateTime,
    Integer,
    Long,
    Unicode,
)

from concentrator import (
    settings,
)


# класс для обязательных текстовых полей
class NotBlankUnicode(Unicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 0


# класс для обязательных полей c датой
class NotBlankDate(Date):
    class Attributes(Date.Attributes):
        nillable = False
        min_occurs = 0


class NotBlankDateTime(DateTime):
    class Attributes(DateTime.Attributes):
        nillable = False
        min_occurs = 0


class ComplexModelWithNamespace(ComplexModel):
    """
    Для перегрузки пространства имен
    """

    __namespace__ = settings.TNS


# -----------------------------------------------------------------------------
# Типы заявления
# -----------------------------------------------------------------------------
class ExternalId(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Идентификатор заявления в подсистеме "Концентратор Услуг"'


class Status(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Статус запроса'


class RegionalId(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Идентификатор заявления в региональной системе'


class SubmitDate(NotBlankDateTime):
    class Attributes(DateTime.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(DateTime.Annotations):
        doc = 'Дата создания заявление'


class EntryDate(NotBlankDate):
    class Attributes(NotBlankDate.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(DateTime.Annotations):
        doc = 'Дата желаемого зачисления'


class StateName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Статус заявления'


class StateDetails(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Детализация статуса'


class StateCode(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Код статуса'


# -----------------------------------------------------------------------------
# Типы фил лица
# -----------------------------------------------------------------------------
class FIO(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Первые буквы фамилии, имени и отчества'


class FirstName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Имя'


class LastName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Фамилия'


class MiddleName(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Отчество ребенка'


# TODO: Регулярочка не помешала бы
class Snils(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'СНИЛС'


class FourDocNumber(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = '4 цифры номера документа'


class DocNumber(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Серия и номер документа удостоверяющего личность'


class DocSeria(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Серия документа удостоверяющего личность'


class DocType(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Идентификатор типа документа удостоверяющего личность'


class DocIssueDate(NotBlankDate):
    class Annotations(Date.Annotations):
        doc = 'Дата выдачи документа удостоверяющего личность'


class DocIssuerName(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Место выдачи документа удостоверяющего личность'


class DocIssuerDepartmentCode(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Код подзразделения выдавший документ удостоверяющей личность'


class DateOfBirth(NotBlankDate):
    class Annotations(Date.Annotations):
        doc = 'День рождения'


# -----------------------------------------------------------------------------
# Типы групп
# -----------------------------------------------------------------------------
class AgeGroupType(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Возрастная группа в ДОО. Справочника'


# -----------------------------------------------------------------------------
# Типы ребенка
# -----------------------------------------------------------------------------
# Потребность по здоровью
class AdaptationProgramType(NotBlankUnicode):
    class Annotations(NotBlankUnicode.Annotations):
        doc = 'Адаптационная программа'


class AdaptationProgramDocInfo(NotBlankUnicode):
    class Annotations(NotBlankUnicode.Annotations):
        doc = 'Реквизиты документа, подтверждающего ограничение в здоровье'


class Sex(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = 'Пол заявлемого'


class AddressRegistration(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = 'Адрес регистрации'


class AddressResidence(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(NotBlankUnicode.Annotations):
        doc = 'Адрес проживания'


class BenefitItem(ComplexModelWithNamespace):
    """
    Информация о льготе
    """

    name = XmlData(Unicode)
    Type = XmlAttribute(Integer)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Информация о льготе'


class Benefits(ComplexModelWithNamespace):
    Benefit = BenefitItem.customize(min_occurs=0, max_occurs='unbounded', nillable=False)
    BenefitsDocInfo = NotBlankUnicode
    Other = NotBlankUnicode


class DeclaredPersonSearchResult(ComplexModelWithNamespace):
    FIO = FIO
    DocNumber = DocNumber(min_occurs=1)
    DateOfBirth = DateOfBirth(min_occurs=1)
    Sex = Sex
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence
    AgeGroupType = AgeGroupType
    Benefits = Benefits.customize(min_occurs=0, nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Данные о ребенке'


# -----------------------------------------------------------------------------
# Типы организации
# -----------------------------------------------------------------------------
class EduOrganizationCode(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Код ОО в регионе'


class EducationProgramType(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Образовательная программа'


class Other(NotBlankUnicode):
    class Annotations(Unicode.Annotations):
        doc = 'Другие льготы'


class EduOrganization(ComplexModelWithNamespace):
    """
    Информация об организации
    """

    Code = Unicode
    Priority = Integer

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию об ОО'


class EduOrganizationsData(ComplexModelWithNamespace):
    """
    Информация о ОО
    """

    _type_info = [('EduOrganization', EduOrganization.customize(max_occurs='unbounded')), ('AllowOfferOther', Boolean)]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Информация об ОО'


class ScheduleData(ComplexModelWithNamespace):
    """Информация о режимах пребывания"""

    _type_info = [('ScheduleType', Integer.customize(min_occurs=0, max_occurs='unbounded'))]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о режимах пребывания'


# -----------------------------------------------------------------------------
# Типы представителя
# -----------------------------------------------------------------------------
class ApplicantType(NotBlankUnicode):
    class Attributes(Unicode.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Категоря заявителя'


class ApplicantSearchResult(ComplexModelWithNamespace):
    FIO = FIO
    ApplicantType = ApplicantType
    DocNumber = DocNumber(min_occurs=1)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Данные о заявителе'


class ApplicationSearchResult(ComplexModelWithNamespace):
    ExternalId = ExternalId
    RegionalId = RegionalId
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    State = StateName
    StateDetails = StateDetails
    Applicant = ApplicantSearchResult
    DeclaredPerson = DeclaredPersonSearchResult


# -----------------------------------------------------------------------------
# Типы очереди
# -----------------------------------------------------------------------------
class Order(Long):
    class Attributes(Long.Attributes):
        nillable = False
        min_occurs = 1

    class Annotations(Unicode.Annotations):
        doc = 'Порядок заявления в очереди'


class Application(ComplexModelWithNamespace):
    Order = Order
    ExternalId = ExternalId
    RegionalId = RegionalId
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    AdaptationProgramDocInfo = AdaptationProgramDocInfo
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    State = StateCode(min_occurs=1)
    StateDetails = StateDetails
    Applicant = ApplicantSearchResult.customize(nillable=False, min_occurs=1)
    DeclaredPerson = DeclaredPersonSearchResult.customize(nillable=False, min_occurs=1)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Данные о заявке'


class Queue(ComplexModelWithNamespace):
    EduOrganizationCode = EduOrganizationCode
    ApplicationsCount = Long(nillable=False, min_occurs=1)
    Application = Application.customize(min_occurs=1, max_occurs='unbounded', nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию об Очереди'


# -----------------------------------------------------------------------------
# Типы очереди
# -----------------------------------------------------------------------------


class ApplicantData(ComplexModelWithNamespace):
    """
    Информация о заявителе
    """

    FirstName = FirstName(min_occurs=1)
    LastName = LastName(min_occurs=1)
    MiddleName = MiddleName
    DocType = DocType(min_occurs=1)
    DocSeria = DocSeria(min_occurs=1)
    DocNumber = DocNumber(min_occurs=1)
    DocIssueDate = DocIssueDate(min_occurs=1)
    DocIssuerName = DocIssuerName
    DocIssuerDepartmentCode = DocIssuerDepartmentCode
    Snils = Snils(min_occurs=1)
    ApplicantType = ApplicantType
    ApplicantTypeOtherName = NotBlankUnicode
    ApplicantTypeOtherDocNumber = NotBlankUnicode
    Email = NotBlankUnicode(min_occurs=1)
    PhoneNumber = NotBlankUnicode

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о заявителе'


class DeclaredPersonData(ComplexModelWithNamespace):
    """
    Информация о ребенке
    """

    FirstName = FirstName(min_occurs=1)
    LastName = LastName(min_occurs=1)
    MiddleName = MiddleName
    Snils = Snils(min_occurs=1)
    BirthPlace = Unicode
    BirthDocSeria = DocSeria
    BirthDocNumber = DocNumber
    BirthDocActNumber = Unicode.customize(min_occurs=0)
    BirthDocIssueDate = DocIssueDate
    BirthDocIssuer = Unicode.customize(min_occurs=0)
    BirthDocForeign = Unicode.customize(min_occurs=0)
    BirthDocForeignNumber = Unicode.customize(min_occurs=0)
    AgeGroupType = AgeGroupType
    DateOfBirth = Date
    # В большом городе
    Sex = Sex
    AddressRegistration = AddressRegistration
    AddressResidence = AddressResidence
    Benefits = Benefits.customize(min_occurs=0, nillable=False)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о ребенке'


# -----------------------------------------------------------------------------
# Типы сервиса "Запрос текущей очереди заявления"
# -----------------------------------------------------------------------------
class GetApplicationQueueRequest(ComplexModelWithNamespace):
    ExternalId = ExternalId(min_occurs=1)
    AllApplications = Boolean(min_occurs=0, nillable=False)
    EduOrganizationCode = EduOrganizationCode(min_occurs=0)

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Идентификатор заявления в подсистеме “Концентратор Услуг”.'


class GetApplicationQueueResponse(ComplexModelWithNamespace):
    Queue = Queue.customize(max_occurs='unbounded', nillable=False)
    SupportAllApplications = Boolean(min_occurs=0, nillable=False)


# -----------------------------------------------------------------------------
# Типы сервиса “Запрос текущего статуса заявления”
# -----------------------------------------------------------------------------
class GetApplicationStateResponse(ComplexModelWithNamespace):
    Code = StateCode(min_occurs=1)
    Name = StateName(min_occurs=1)
    Details = StateDetails


class GetApplicationStateRequest(ComplexModelWithNamespace):
    _type_info = [('ExternalId', ExternalId(min_occurs=1))]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Идентификатор заявления в подсистеме “Концентратор Услуг”.'


# -----------------------------------------------------------------------------
# типы сервиса Поиск Заявлений по совпадению персональных данных ребенка и
# представителя
# -----------------------------------------------------------------------------
class FindApplicationsByDeclaredPersonRequest(ComplexModelWithNamespace):
    FirstName = FirstName
    LastName = LastName
    MiddleName = MiddleName
    Snils = Snils
    DateOfBirth = DateOfBirth
    DocType = DocType
    DocNumber = DocNumber
    DocIssueDate = Date

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о персональных данных'


class FindApplicationsByApplicantRequest(ComplexModelWithNamespace):
    FirstName = FirstName
    LastName = LastName
    MiddleName = MiddleName
    Snils = Snils
    DateOfBirth = DateOfBirth
    DocType = DocType
    DocSeria = DocSeria
    DocNumber = DocNumber
    DocIssueDate = Date


class FindApplicationsByDeclaredPersonResponse(ComplexModelWithNamespace):
    Application = ApplicationSearchResult.customize(max_occurs='unbounded', nillable=False)


class FindApplicationsByApplicantResponse(ComplexModelWithNamespace):
    Application = ApplicationSearchResult.customize(max_occurs='unbounded', nillable=False)


# -----------------------------------------------------------------------------
# типы сервиса Создания заявления
# -----------------------------------------------------------------------------
class DocumentReference(ComplexModelWithNamespace):
    Code = Unicode.customize(nillable=False, min_occurs=1, max_occurs=1)
    Name = NotBlankUnicode
    Description = NotBlankUnicode

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о документах'


class DocumentReferencesData(ComplexModelWithNamespace):
    _type_info = [('DocumentReference', DocumentReference.customize(max_occurs='unbounded', min_occurs=0))]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о документах'


class NewApplicationRequest(ComplexModelWithNamespace):
    _type_info = [
        ('ExternalId', ExternalId),
        ('SubmitDate', SubmitDate),
        ('EntryDate', EntryDate),
        ('EducationProgramType', EducationProgramType),
        ('AdaptationProgramType', AdaptationProgramType),
        ('AdaptationProgramDocInfo', AdaptationProgramDocInfo),
        ('Schedule', ScheduleData),
        ('Applicant', ApplicantData),
        ('DeclaredPerson', DeclaredPersonData),
        ('EduOrganizations', EduOrganizationsData),
        ('DocumentReferences', DocumentReferencesData.customize(min_occurs=0)),
    ]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о заявлении'


class NewApplicationResponse(ComplexModelWithNamespace):
    _type_info = [('RegionalId', RegionalId)]

    class Annotations(ComplexModelWithNamespace.Annotations):
        doc = 'Контейнер, содержит информацию о результатах работы метода'


# -----------------------------------------------------------------------------
# типы сервиса Получение данных Заявления для изменения
# -----------------------------------------------------------------------------
class ReadOnlyFields(ComplexModelWithNamespace):
    Field = Unicode.customize(max_occurs='unbounded', min_occurs=0, nillable=False)


class ApplicationRulesData(ComplexModelWithNamespace):
    ReadOnlyFields = ReadOnlyFields.customize(min_occurs=0, nillable=False)


class GetApplicationRequest(ComplexModelWithNamespace):
    ExternalId = ExternalId
    ApplicantFirstName = FirstName(min_occurs=1)
    ApplicantLastName = LastName(min_occurs=1)
    ApplicantMiddleName = MiddleName


class GetApplicationResponse(ComplexModelWithNamespace):
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    AdaptationProgramDocInfo = AdaptationProgramDocInfo
    Applicant = ApplicantData.customize(nillable=False, min_occurs=1)
    DeclaredPerson = DeclaredPersonData.customize(nillable=False, min_occurs=1)
    Schedule = ScheduleData.customize(min_occurs=0, max_occurs=1)
    EduOrganizationsData = EduOrganizationsData.customize(nillable=False, min_occurs=1)
    ApplicationRules = ApplicationRulesData.customize(nillable=False, min_occurs=1)
    DocumentReferences = DocumentReferencesData.customize(min_occurs=0)


class UpdateApplicationRequest(ComplexModelWithNamespace):
    ExternalId = ExternalId
    State = StateCode
    SubmitDate = SubmitDate
    EntryDate = EntryDate
    EducationProgramType = EducationProgramType
    AdaptationProgramType = AdaptationProgramType
    AdaptationProgramDocInfo = AdaptationProgramDocInfo
    Schedule = ScheduleData
    Applicant = ApplicantData.customize(nillable=False, min_occurs=1)
    DeclaredPerson = DeclaredPersonData.customize(nillable=False, min_occurs=1)
    EduOrganizationsData = EduOrganizationsData.customize(nillable=False, min_occurs=1)
    DocumentReferences = DocumentReferencesData.customize(min_occurs=0)


class UpdateApplicationResponse(ComplexModelWithNamespace):
    Status = Status
