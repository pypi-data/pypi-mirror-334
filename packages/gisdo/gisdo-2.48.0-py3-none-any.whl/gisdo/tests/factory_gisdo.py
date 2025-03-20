import factory
from future.builtins import (
    object,
)

from kinder.core.unit.tests import (
    factory_unit,
)

from gisdo.models import (
    GisdoUnit,
)


class GisdoUnitFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = GisdoUnit

    unit = factory.SubFactory(factory_unit.UnitDouFactory)
