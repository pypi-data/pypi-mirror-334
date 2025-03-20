from django.apps import (
    AppConfig,
)


class DeclarationConfig(AppConfig):
    name = 'concentrator'
    label = 'concentrator'
    verbose_name = 'заявления'

    def ready(self):
        from .change import (
            ChildrenChangeHelper,
            DeclarationChangeHelper,
            DeclarationDocsChangeHelper,
            DeclarationPrivilegeChangeHelper,
            DeclarationUnitChangeHelper,
            DelegateChangeHelper,
            StorageHelper,
        )

        def register_change_handlers():
            """Регистрация хэлперов для обработки изменений модели."""
            StorageHelper.register_change_helper('Declaration', DeclarationChangeHelper)
            StorageHelper.register_change_helper('DeclarationUnit', DeclarationUnitChangeHelper)
            StorageHelper.register_change_helper('DeclarationPrivilege', DeclarationPrivilegeChangeHelper)
            StorageHelper.register_change_helper(DeclarationDocsChangeHelper.NAME_MODEL, DeclarationDocsChangeHelper)
            StorageHelper.register_change_helper('Delegate', DelegateChangeHelper)
            StorageHelper.register_change_helper('Children', ChildrenChangeHelper)

        register_change_handlers()
