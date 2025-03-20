from django.apps.registry import (
    apps,
)

from m3.plugins import (
    ExtensionHandler,
    ExtensionManager,
    ExtensionPoint,
)

from .extensions import (
    add_applicant_answer_column,
    add_applicant_answer_column_filter,
    add_applicant_answer_data,
    applicant_answer_update_filter_list,
    apply_applicant_answer_filter,
    apply_applicant_answer_sort,
    get_text_message_event_builder,
    handle_text_message_response,
    validate_text_message_response,
)


def register_extensions():
    """Регистрация точек расширения плагина"""

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.add_applicant_answer_column',
            default_listener=ExtensionHandler(handler=add_applicant_answer_column),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.add_applicant_answer_data',
            default_listener=ExtensionHandler(handler=add_applicant_answer_data),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.add_applicant_answer_column_filter',
            default_listener=ExtensionHandler(handler=add_applicant_answer_column_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.apply_applicant_answer_filter',
            default_listener=ExtensionHandler(handler=apply_applicant_answer_filter),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.apply_applicant_answer_sort',
            default_listener=ExtensionHandler(handler=apply_applicant_answer_sort),
        )
    )

    ExtensionManager().register_point(
        ExtensionPoint(
            name='concentrator.smev3.extensions.applicant_answer_update_filter_list',
            default_listener=ExtensionHandler(handler=applicant_answer_update_filter_list),
        )
    )

    if apps.is_installed('kinder.plugins.message_exchange'):
        ExtensionManager().register_point(
            ExtensionPoint(
                name='concentrator.extensions.get_text_message_event_builder',
                default_listener=ExtensionHandler(handler=get_text_message_event_builder),
            )
        )

        ExtensionManager().register_point(
            ExtensionPoint(
                name='concentrator.extensions.handle_text_message_response',
                default_listener=ExtensionHandler(handler=handle_text_message_response),
            )
        )

        ExtensionManager().register_point(
            ExtensionPoint(
                name='concentrator.extensions.validate_text_message_response',
                default_listener=ExtensionHandler(handler=validate_text_message_response),
            )
        )
