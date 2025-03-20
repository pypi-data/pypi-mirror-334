import datetime
from itertools import (
    chain,
)

from django.db.models import (
    Q,
)

from kinder.core.deduct.models import (
    Deduct,
)
from kinder.core.dict.models import (
    DeductReasonEnum as DRE,
)
from kinder.core.direct.models import (
    DRS,
    Direct,
)
from kinder.core.group.models import (
    Group,
    GroupStatusEnum,
    Pupil,
)

from gisdo.constants import (
    ALL,
)
from gisdo.utils import (
    AgeDeltas,
    DateMixin,
    get_report_date_or_today,
)

from .base import (
    BaseIndex,
)
from .enrolled import (
    Index,
)


class DirectIndex(BaseIndex):
    """Запросы расчитывающие количество направлений,
    написанные на django queryset'ах"""

    ALGORITHM_MAP = {}

    def get_queries(self, direct_ids, pupil_ids, **kwargs):
        qs_direct = Direct.objects.filter(
            id__in=direct_ids,
            group__unit=self.unit,
        )
        qs_pupil = Pupil.objects.filter(id__in=pupil_ids).exclude(
            children_id__in=qs_direct.values_list('declaration__children_id', flat=True),
            grup__unit=self.unit,
        )

        age_range = kwargs.get('age_range', ALL)
        if age_range != ALL:
            on_date = kwargs.get('on_date', AgeDeltas.calculate_date)
            down, up = AgeDeltas.get_category_deltas(age_range, on_date)
            qs_direct = qs_direct.filter(
                declaration__children__date_of_birth__gt=down, declaration__children__date_of_birth__lte=up
            )
            qs_pupil = qs_pupil.filter(children__date_of_birth__gt=down, children__date_of_birth__lte=up)
        return qs_direct, qs_pupil

    def get_count(self, direct_ids, pupil_ids, **kwargs):
        qs_direct, qs_pupil = self.get_queries(direct_ids, pupil_ids, **kwargs)
        return qs_direct.count() + qs_pupil.count()


def ind_19_3(dou, report_start_date, age_range=ALL, prep_direct_func=None):
    """Показатель #19.3."""

    result = 0
    data = []
    group_index = Index(dou, report_start_date)

    for group in Group.objects.filter(status=GroupStatusEnum.FACT, unit=dou):
        for extra_data, date_of_birth in group_index.directs_in_group(group, prep_direct_func=prep_direct_func):
            down, up = AgeDeltas.get_category_deltas(age_range, datetime.date.today)

            if down < date_of_birth <= up:
                if not prep_direct_func:
                    result += 1
                else:
                    data.append(extra_data)

    if not prep_direct_func:
        return result
    else:
        return data


def ind_29_1(dou, report_start_date, prep_func=None):
    """Показатель 29.1.

    Прогнозируемое уменьшение контингента воспитанников в текущем учебном году.

    :param dou: Организация
    :type dou: Unit

    :return: Возвращает список кортежей с данными детей
    """

    date_in_order = get_report_date_or_today(report_start_date)
    groups = dou.group_set.filter(status=GroupStatusEnum.FACT)
    children_ids = set()

    for group in groups.iterator():
        qs = Pupil.objects.filter(temporary_deduct=False)
        children_in_fact = qs.filter(grup=group, grup__status=GroupStatusEnum.FACT).values_list(
            'children_id', flat=True
        )

        children_in_plan = (
            qs.filter(Q(grup__room_id__isnull=False, grup__room_id=group.room_id))
            .filter(
                Q(date_in_order__lte=date_in_order) | Q(date_in_order__isnull=True), grup__status=GroupStatusEnum.PLAN
            )
            .exclude(
                children_id__in=qs.filter(grup__unit=group.unit, grup__status=GroupStatusEnum.FACT).values_list(
                    'children_id', flat=True
                )
            )
            .values_list('children_id', flat=True)
        )

        children_ids.update(children_in_fact, children_in_plan)

    direct_query = (
        Direct.objects.filter(
            status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            group__status__in=(GroupStatusEnum.FACT, GroupStatusEnum.PLAN),
        )
        .filter(declaration__children_id__in=children_ids)
        .exclude(
            # направление в другое ДОО
            group__unit=dou
        )
        .distinct('declaration__children')
    )

    pupil_query = (
        Pupil.objects.filter(
            children_id__in=children_ids,
            date_in_order__gt=date_in_order,
            grup__status=GroupStatusEnum.PLAN,
        )
        .exclude(grup__unit=dou)
        .distinct('children')
    )

    if prep_func:
        return prep_func(direct_query, pupil_query)

    return set(
        chain(
            direct_query.values_list('declaration__children_id', 'declaration__children__date_of_birth'),
            # Как направления считаем и зачисления, дата зачисления по приказу
            # которых больше контрольной даты
            pupil_query.values_list('children_id', 'children__date_of_birth'),
        )
    )


def ind_29_2(dou, prep_func=None):
    """Показатель 29.2.

    Фактическое уменьшение контингента воспитанников в текущем учебном году.

    :param dou: Организация
    :type dou: Unit
    :param prep_func: Функция для преобразования данных запроса для отчёта
    :type prep_func: Optional[Callable]

    :return: Возвращает список кортежей с данными детей
    """

    deduct_query = Deduct.objects.filter(
        date__range=DateMixin.get_current_calendar_year_range(),
        group__unit=dou,
        temporary_deduct=False,
    ).exclude(
        reason__code__in=(
            DRE.CODE_DIDNT_COME,
            DRE.CODE_CHANGE_STATUS_DIRECT,
            DRE.CODE_AUTO_DEDUCT,
            DRE.CODE_MOVE_WITHIN_DOU,
        )
    )

    if prep_func:
        return prep_func(deduct_query)

    deduct_final_query = (
        deduct_query.values_list(
            # Возраст считается на дату отчисления, поэтому её тоже берём
            'children_id',
            'children__date_of_birth',
            'date',
        )
        .order_by('children_id', '-date')
        .distinct('children_id')
    )
    return deduct_final_query


def ind_29_3(dou, prep_func=None):
    """Показатель 29.3.

    Фактическое уменьшение контингента воспитанников в связи с уходом
    в школу в текущем учебном году.

    :param dou: Организация
    :type dou: Unit
    :param prep_func: Функция для преобразования данных запроса для отчёта
    :type prep_func: Optional[Callable]

    :return: Возвращает список кортежей с данными детей
    """

    deduct_query = Deduct.objects.filter(
        date__range=DateMixin.get_current_calendar_year_range(),
        group__unit=dou,
        temporary_deduct=False,
    ).filter(reason__code=DRE.CODE_ISSUE_TO_SCHOOL)

    if prep_func:
        return prep_func(deduct_query)

    deduct_final_query = (
        deduct_query.values_list('children_id', 'children__date_of_birth')
        .order_by('children_id', '-date')
        .distinct('children_id')
    )
    return deduct_final_query
