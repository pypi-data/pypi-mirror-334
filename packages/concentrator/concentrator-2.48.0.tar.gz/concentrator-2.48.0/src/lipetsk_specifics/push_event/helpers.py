from kinder.webservice.push_event.helpers import (
    SimplePushEvent,
)

from .loaders import (
    QueueDirectionDecisionLoader,
)
from .provider import (
    ChangeDeclarationDataProvider,
    QueueDirectionDecisionDataProvider,
)


class ChangeInDeclarationPushEvent(SimplePushEvent):
    """Заменен provider"""

    provider = ChangeDeclarationDataProvider


class QueueDirectionDecision(SimplePushEvent):
    """Заменен provider и loader"""

    method_name = 'Синхронизация статуса с ЕПГУ (Липецк)'

    provider = QueueDirectionDecisionDataProvider
    loader = QueueDirectionDecisionLoader
