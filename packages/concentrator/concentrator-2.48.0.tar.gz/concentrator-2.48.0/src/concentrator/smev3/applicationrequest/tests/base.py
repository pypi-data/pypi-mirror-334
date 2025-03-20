import os

from kinder.core.unit.tests import (
    factory_unit,
)

from concentrator.smev3.base.tests.base import (
    Smev3TC,
)
from concentrator.smev3.base.tests.utils import (
    examples,
)
from concentrator.smev3.service_types import (
    kinder_conc,
)


class ApplicationTC(Smev3TC):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.application = kinder_conc.parseString(
            next(examples(os.path.dirname(__file__))), silence=True
        ).ApplicationRequest
        cls.attachments = None
        cls.mo = factory_unit.UnitMoFactory()
        cls.unit = factory_unit.UnitDouFactory(parent=cls.mo)
