import datetime

from dateutil import (
    relativedelta,
)
from future.builtins import (
    object,
)

from kinder.core.dict.models import (
    UnitKind,
)
from kinder.core.direct.models import (
    Direct,
)

from gisdo.index_report.constants import (
    REPORT_FIELDS,
)
from gisdo.queue_index.context import (
    Context,
)
from gisdo.queue_index.queue_conf import (
    GisdoContainer,
)
from gisdo.queue_index.runtime_filters import (
    DateYearFilter,
)
from gisdo.utils import (
    AgeDeltas,
)


def get_queue_index(
    index_number, unit, age_range=None, on_date=datetime.date.today, check_unit=True, distinct_children=False
):
    """Вычисление новых показателей по очереди."""

    qs = get_queue_index_collection(
        index_number,
        unit,
        age_range=age_range,
        on_date=on_date,
        check_unit=check_unit,
        distinct_children=distinct_children,
    )

    return qs.count()


def get_queue_index_collection(
    index_number,
    unit,
    age_range=None,
    on_date=datetime.date.today,
    check_unit=True,
    distinct_children=False,
    report=False,
):
    """Вычисление новых показателей по очереди.

    :param index_number: Номер индекса фильтра
    :type index_number: str
    :param unit: Организация
    :type unit: Unit
    :param age_range: Возрастной диапазон
    :param on_date: Дата (по умолчанию сегодня)
    :type on_date: datetime.date
    :param check_unit: Признак доп. фильтрации Желаемых ДОО
        + даты заявления (дата меньше либо равна сегодня)
    :param distinct_children: Признак уникальности детей
    :type distinct_children: Optional[bool]
    :param report: Признак того, что показатель вычисляется для отчета
    :type report: bool
    :return: Выборка заявлений
    :rtype: QuerySet
    """

    assert 'p{0}'.format(index_number.replace('.', '_')) in GisdoContainer.index_filters, 'Queue config failed'

    # Формирование контекста на основе показателей.
    ctx = Context(unit, on_date=on_date, first_dou_only=True, select_fields=REPORT_FIELDS if report else None)
    if age_range is not None:
        ctx = ctx.add_filters(DateYearFilter(age_range))

    # Получение билдера
    cont = GisdoContainer()
    builder = cont.get_builder(index_number)

    # Построение QuerySet-а
    qs = builder.build(ctx)
    if check_unit:
        qs = qs.filter(
            declarationunit__unit_id=unit.id,
            declarationunit__ord=1,
            declarationunit__unit__kind_id=UnitKind.DOU,
            date__lte=datetime.datetime.combine(datetime.datetime.now(), datetime.datetime.max.time()),
        )

    if distinct_children:
        qs = qs.distinct('children')

    return qs


def _months_between(left_date, right_date):
    r = relativedelta.relativedelta(left_date, right_date)
    diff = r.months + r.days / 30.4
    return diff if diff >= 0 else 0


class AverageWaitingTimeWrapper(object):
    def __init__(self, child_quantity, total_waiting_time):
        super(AverageWaitingTimeWrapper, self).__init__()
        self._child_quantity = child_quantity
        self._total_waiting_time = total_waiting_time

    @property
    def child_quantity(self):
        return self._child_quantity

    @property
    def total_waiting_time(self):
        return self._total_waiting_time

    def __str__(self):
        return '-' if self._child_quantity <= 0 else '%.1f' % (float(self._total_waiting_time) / self._child_quantity)

    def __add__(self, other):
        if isinstance(other, AverageWaitingTimeWrapper):
            return AverageWaitingTimeWrapper(
                child_quantity=self._child_quantity + other.child_quantity,
                total_waiting_time=self._total_waiting_time + other.total_waiting_time,
            )
        else:
            return self

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, AverageWaitingTimeWrapper):
            self._child_quantity += other.child_quantity
            self._total_waiting_time += other.total_waiting_time

        return self


def get_average_waiting_time(collection, age_value):
    """
    Определение среднего времени ожидания очереди в детский сад
    """

    age_filter = get_age_filter_for_ind_8(age_value)

    directs = Direct.objects.filter(
        declaration_id__in=[declaration['id'] for declaration in collection if age_filter(declaration)]
    ).values('declaration__desired_date', 'date')

    waiting_times = [_months_between(direct['date'], direct['declaration__desired_date']) for direct in directs]
    return AverageWaitingTimeWrapper(child_quantity=len(waiting_times), total_waiting_time=sum(waiting_times))


def get_count(collection, age_filter):
    """Определение количества записей в коллекции подходящих под фильтр.

    Функция применяет фильтр age_filter к коллекции collection и возвращает
    количество отфильтрованных записей.
    """

    return len([declaration for declaration in collection if age_filter(declaration)])


def get_age_filter(age, on_date):
    """Функция строит фильтр возраста."""

    down, up = AgeDeltas.get_category_deltas(age, on_date)

    filter_ = lambda rec: rec['children__date_of_birth'] > down
    if up:
        if age == 'от 2 месяцев до 6 месяцев':
            filter_ = lambda rec: (down < rec['children__date_of_birth'])
        else:
            filter_ = lambda rec: (down < rec['children__date_of_birth'] <= up)

    return filter_


def get_age_filter_for_ind_8(age):
    """Функция строит фильтр возрастов для показателей 8.X"""

    down, up = AgeDeltas.get_categories_borders(age)

    down_years, down_months = down

    filter_ = lambda rec: (
        rec['children__date_of_birth']
        > rec['desired_date'] - relativedelta.relativedelta(years=down_years, months=down_months)
    )
    if up:
        up_years, up_months = up
        if age == 'от 2 месяцев до 6 месяцев':
            filter_ = lambda rec: (
                rec['desired_date'] - relativedelta.relativedelta(years=down_years, months=down_months)
                < rec['children__date_of_birth']
            )
        else:
            filter_ = lambda rec: (
                rec['desired_date'] - relativedelta.relativedelta(years=down_years, months=down_months)
                < rec['children__date_of_birth']
                <= rec['desired_date'] - relativedelta.relativedelta(years=up_years, months=up_months)
            )

    return filter_
