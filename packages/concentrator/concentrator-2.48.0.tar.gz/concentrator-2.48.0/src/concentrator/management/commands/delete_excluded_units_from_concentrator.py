from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from concentrator.dict.constants import (
    OperationEnumerate,
)
from concentrator.dict.proxy import (
    ExcludedUnitProxy,
)


class Command(BaseCommand):
    help = 'Delete excluded units from concentrator'

    def add_arguments(self, parser):
        parser.add_argument(
            '--size',
            action='store',
            dest='size',
            default=200,
            help='Send buffer size in records',
        )

    def handle(self, *args, **options):
        """
        Отсылаем запрос на удаление исключенных ДОО
        """

        try:
            size = int(options['size'])
        except ValueError:
            raise CommandError('option --size must have an integer argument. Example: --size 10')

        ExcludedUnitProxy().send_all(OperationEnumerate.DELETE, size)
