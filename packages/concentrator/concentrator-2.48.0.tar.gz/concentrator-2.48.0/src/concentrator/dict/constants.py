from m3.db import (
    BaseEnumerate,
)


class OperationEnumerate(BaseEnumerate):
    """Тип операции."""

    ADD = 'Add'
    UPDATE = 'Update'
    DELETE = 'Delete'
    values = {ADD: 'Добавление', UPDATE: 'Изменение', DELETE: 'Удаление'}


class ModelForSend(BaseEnumerate):
    """
    Модель для отправки
    """

    GROUP = 'GroupAgeSubCathegoryProxy'
    HEALTH = 'HealthNeedProxy'
    PRIVILEGE = 'PrivilegeProxy'
    UNIT = 'UnitProxy'
    STAT = 'GroupStatisticProxy'
    values = {
        GROUP: 'ДОО.ВозрастнаяГруппа',
        HEALTH: 'ДОО.СпецификаГрупп',
        PRIVILEGE: 'Льготы.ДОО.Региональные',
        UNIT: 'Организации.ДОО.Региональные',
        STAT: 'Статистика.ВозрастнаяГруппа',
    }
