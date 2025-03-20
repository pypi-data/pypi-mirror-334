from django.apps import (
    AppConfig,
)


class Smev3Config(AppConfig):
    """Конфиг приложения Концентратор (СМЭВ 3)."""

    name = __package__
    label = 'smev3_v321'
    verbose_name = 'СМЭВ 3'

    def ready(self) -> None:
        """Выполняет доп. операции, когда приложение готово.

        Выполняет проверку обязательных плагинов:
            Контингент,

        Выполняет регистрацию сигналов, асинк. задач,
        исполнителей сервисов СМЭВ (AIO) и менеджеров изменений.

        """

        from kinder.plugins.helpers import (
            check_required_plugins,
        )

        # Данные из контингента используются в сервисах Концентратора (СМЭВ 3).
        dependencies = [
            'kinder.plugins.contingent',
        ]
        check_required_plugins(self.name, dependencies)

        # Инициализирует асинк. задачи, обсерверы и сигналы.
        from concentrator.smev3_v321.get_application_queue.executors import (
            GetApplicationQueueRequestExecutor,
        )
        from concentrator.smev3_v321.get_application_request.executors import (
            GetApplicationRequestExecutor,
        )

        from . import (
            observer,
            signals,
        )
        from .application_admission_request.executors import (
            ApplicationAdmissionRequestExecutor,
        )
        from .application_order_info_request.executors import (
            ApplicationOrderInfoRequestExecutor,
        )
        from .application_rejection_request.executors import (
            ApplicationRejectionRequestExecutor,
        )
        from .application_request.executors import (
            ApplicationRequestExecutor,
        )
        from .base import (
            tasks,
        )
        from .cancel_request.executors import (
            CancelRequestExecutor,
        )
        from .esnsi import (
            tasks,
        )
        from .executors import (
            RepositoryExecutors,
        )
        from .get_application_admission_request.executors import (
            GetApplicationAdmissionRequestExecutor,
        )
        from .get_application_queue_reason_request.executors import (
            GetApplicationQueueReasonRequestExecutor,
        )

        # Настройка всех исполнителей для сервисов СМЭВ 3.
        executors = (
            ApplicationRequestExecutor,
            GetApplicationAdmissionRequestExecutor,
            ApplicationRejectionRequestExecutor,
            GetApplicationQueueRequestExecutor,
            GetApplicationRequestExecutor,
            CancelRequestExecutor,
            ApplicationOrderInfoRequestExecutor,
            GetApplicationQueueReasonRequestExecutor,
            ApplicationAdmissionRequestExecutor,
        )

        for executor in executors:
            RepositoryExecutors.set_executor(executor)

        from .application_request.changes import (
            Smev3ChildrenChangeHelper,
            Smev3DeclarationChangeHelper,
            Smev3DeclarationDocsChangeHelper,
            Smev3DeclarationPrivilegeChangeHelper,
            Smev3DeclarationUnitChangeHelper,
            Smev3DelegateChangeHelper,
            Smev3StorageHelper,
        )

        # Настройка необходимых обработчиков изменений для сервисов СМЭВ 3
        # (подача заявления).
        change_helpers = (
            Smev3DeclarationPrivilegeChangeHelper,
            Smev3DeclarationUnitChangeHelper,
            Smev3DeclarationDocsChangeHelper,
            Smev3DeclarationChangeHelper,
            Smev3DelegateChangeHelper,
            Smev3ChildrenChangeHelper,
        )

        for change_helper in change_helpers:
            Smev3StorageHelper.register_change_helper(change_helper.NAME_MODEL, change_helper)

        from concentrator.changes.rules import (
            display_changes_map,
        )
        from concentrator.smev3_v321.utils import (
            get_delegate,
        )

        # Замена функции получения объекта представителя из изменений заявки.
        # change_declaration is ChangeDeclaration.
        display_changes_map.set('Delegate', lambda change_declaration: get_delegate(change_declaration.declaration))
