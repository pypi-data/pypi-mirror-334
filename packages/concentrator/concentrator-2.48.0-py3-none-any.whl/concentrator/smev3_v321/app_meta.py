from m3.plugins import (
    ExtensionHandler,
    ExtensionManager,
    ExtensionPoint,
)

from kinder.urls import (
    dict_controller,
)

from concentrator.smev3_v321.esnsi.actions import (
    ClassifierListPack,
    ClassifierUpdatePack,
)

from . import (
    listeners,
)
from .application_request.extensions import (
    get_storage_helper,
)
from .extensions import (
    add_applicant_answer_column,
    add_applicant_answer_column_filter,
    add_applicant_answer_data,
    additional_declarations_search_fields,
    applicant_answer_update_filter_list,
    apply_applicant_answer_filter,
    apply_applicant_answer_sort,
    apply_need_confirmation_only_filter,
    change_fields_allow_blank,
    exists_declarationportalid,
    get_create_changes,
    get_delete_changes,
    get_snapshot,
    get_update_changes,
    send_changes_info,
)
from .order import (
    listeners,
)
from .order.extensions import (
    apply_epgu_subscribed_only_filter,
    send_update_order_request,
    set_epgu_subscribed_checkbox,
)


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.add_applicant_answer_column',
            default_listener=ExtensionHandler(handler=add_applicant_answer_column),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.add_applicant_answer_data',
            default_listener=ExtensionHandler(handler=add_applicant_answer_data),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.add_applicant_answer_column_filter',
            default_listener=ExtensionHandler(handler=add_applicant_answer_column_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.apply_applicant_answer_filter',
            default_listener=ExtensionHandler(handler=apply_applicant_answer_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.apply_applicant_answer_sort',
            default_listener=ExtensionHandler(handler=apply_applicant_answer_sort),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.applicant_answer_update_filter_list',
            default_listener=ExtensionHandler(handler=applicant_answer_update_filter_list),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.apply_need_confirmation_only_filter',
            default_listener=ExtensionHandler(handler=apply_need_confirmation_only_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.send_update_order_request',
            default_listener=ExtensionHandler(handler=send_update_order_request),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.additional_declarations_search_fields',
            default_listener=ExtensionHandler(handler=additional_declarations_search_fields),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.application_request.extensions.get_storage_helper',
            default_listener=ExtensionHandler(handler=get_storage_helper),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.application_request.extensions.exists_declarationportalid',
            default_listener=ExtensionHandler(handler=exists_declarationportalid),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.order.extensions.set_epgu_subscribed_checkbox',
            default_listener=ExtensionHandler(handler=set_epgu_subscribed_checkbox),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.order.extensions.apply_epgu_subscribed_only_filter',
            default_listener=ExtensionHandler(handler=apply_epgu_subscribed_only_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.get_snapshot',
            default_listener=ExtensionHandler(handler=get_snapshot),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.get_create_changes',
            default_listener=ExtensionHandler(handler=get_create_changes),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.get_delete_changes',
            default_listener=ExtensionHandler(handler=get_delete_changes),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.get_update_changes',
            default_listener=ExtensionHandler(handler=get_update_changes),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.send_changes_info',
            default_listener=ExtensionHandler(handler=send_changes_info),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3_v321.extensions.change_fields_allow_blank',
            default_listener=ExtensionHandler(handler=change_fields_allow_blank),
        )
    )


def register_actions():
    dict_controller.packs.extend([ClassifierListPack(), ClassifierUpdatePack()])
