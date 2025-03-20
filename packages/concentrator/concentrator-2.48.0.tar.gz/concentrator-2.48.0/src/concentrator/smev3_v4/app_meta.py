from m3.plugins import (
    ExtensionHandler,
    ExtensionManager,
    ExtensionPoint,
)

from .extensions import (
    extend_esnsi_classifier_data,
    extend_esnsi_classifier_fields,
    get_agreement_on_other_group,
    get_executors,
    get_order_request_builder,
    get_parsing_module,
    get_unit_params,
    get_update_order_request_builder,
    service_type_smev4,
)
from .listeners import (
    register_listeners,
)


register_listeners()


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_parsing_module',
            default_listener=ExtensionHandler(handler=get_parsing_module),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.service_type_smev4',
            default_listener=ExtensionHandler(handler=service_type_smev4),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_executors',
            default_listener=ExtensionHandler(handler=get_executors),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_unit_params',
            default_listener=ExtensionHandler(handler=get_unit_params),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_agreement_on_other_group',
            default_listener=ExtensionHandler(handler=get_agreement_on_other_group),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_order_request_builder',
            default_listener=ExtensionHandler(handler=get_order_request_builder),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.get_update_order_request_builder',
            default_listener=ExtensionHandler(handler=get_update_order_request_builder),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.extend_esnsi_classifier_fields',
            default_listener=ExtensionHandler(handler=extend_esnsi_classifier_fields),
        )
    )
    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v4.extensions.extend_esnsi_classifier_data',
            default_listener=ExtensionHandler(handler=extend_esnsi_classifier_data),
        )
    )
