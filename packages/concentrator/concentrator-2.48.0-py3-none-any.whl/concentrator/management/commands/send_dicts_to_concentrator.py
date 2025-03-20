from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from concentrator.dict.constants import (
    ModelForSend,
    OperationEnumerate,
)
from concentrator.dict.proxy import (
    GroupAgeSubCathegoryProxy,
    GroupStatisticProxy,
    HealthNeedProxy,
    PrivilegeProxy,
    UnitProxy,
)


class Command(BaseCommand):
    help = 'Send dictionaries info to concentrator [-U] [--size]'

    def add_arguments(self, parser):
        parser.add_argument(
            '-O',
            action='store',
            dest='mode',
            choices=[OperationEnumerate.UPDATE, OperationEnumerate.ADD, OperationEnumerate.DELETE],
            default=OperationEnumerate.UPDATE,
            help='Send data to update, delete or adding it',
        )

        parser.add_argument(
            '-D',
            action='store',
            dest='dict',
            choices=list(ModelForSend.values.keys()),
            default=ModelForSend.UNIT,
            help='NameDict',
        )

        parser.add_argument(
            '--size', action='store', dest='size', default=200, help='Send data to update instead of adding it'
        )

    def handle(self, *args, **options):
        """
        Если команда вызвана с ключом -U, то данные
        будут отправлены на обновление. В противном случае - на добавление.
        """
        operation = options['mode']
        try:
            size = int(options['size'])
        except ValueError:
            raise CommandError('option --size must have an integer argument. Example: --size 10')

        proxy_classes = (
            GroupAgeSubCathegoryProxy,
            HealthNeedProxy,
            PrivilegeProxy,
            UnitProxy,
            GroupStatisticProxy,
        )
        for proxy_class in proxy_classes:
            if options['dict'] == proxy_class.__name__:
                proxy_class().send_all(operation, size)
