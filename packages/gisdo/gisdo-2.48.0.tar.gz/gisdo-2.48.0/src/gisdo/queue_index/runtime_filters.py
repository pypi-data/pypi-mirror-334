from django.conf import (
    settings,
)
from django.db.models import (
    Q,
)

from kinder.core.queue_api.filters import (
    common_unit_filter,
    tula_unit_filter,
)
from kinder.core.queue_api.filters.runtime_filters import (
    BaseRuntimeQFilter,
)
from kinder.core.unit.models import (
    Unit,
    UnitKind,
)

from gisdo.utils import (
    AgeDeltas,
)


class DateYearFilter(BaseRuntimeQFilter):
    """Дата рождения ребенка с указанный период"""

    verbose_name = 'Дата рождения в указанный период'

    def filter_(self, ctx):
        age_on_date = ctx.on_date
        down, up = AgeDeltas.get_category_deltas(self._value, age_on_date)

        result_filter = Q(children__date_of_birth__gte=down)

        if up:
            result_filter &= Q(children__date_of_birth__lt=up)

        return result_filter


class UnitFilter(BaseRuntimeQFilter):
    """Фильтр по организации"""

    verbose_name = 'Фильтр по организации'

    @classmethod
    def _is_valid(cls, value):
        return isinstance(value, Unit) and value.kind_id == UnitKind.DOU

    def filter_(self, ctx):
        if settings.QUEUE_SORT_UNIT_ADDTIME:
            unit_filter = tula_unit_filter
        else:
            unit_filter = common_unit_filter

        return unit_filter(ctx)
