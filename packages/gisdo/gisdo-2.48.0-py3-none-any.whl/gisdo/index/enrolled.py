import datetime
import pickle
from datetime import (
    date,
)
from itertools import (
    chain,
)

from dateutil.relativedelta import (
    relativedelta,
)
from django.core.cache import (
    cache,
)
from django.db.models import (
    Q,
)
from django.utils.functional import (
    cached_property,
)
from future import (
    standard_library,
)
from future.builtins import (
    object,
)

from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.dict.models import (
    HNE,
    GroupTypeEnumerate,
    WorkType,
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
from kinder.core.unit.models import (
    FilialData,
    FilialTypeStatus,
)

from gisdo import (
    settings as gs_settings,
)
from gisdo.algorithm.enrolled import (
    EnrolledCountByAge,
    EnrolledCountByCare,
    EnrolledCountByCorrect,
    EnrolledCountByDisabled,
    EnrolledCountByFamily,
    EnrolledCountByHealth,
    EnrolledCountFullDayStay,
    EnrolledCountShortStay,
    EnrolledCountWantChangeDou,
    EnrolledCountWantChangeDouWithHN,
    PredictableDecreaseContingent,
)
from gisdo.algorithm.utils import (
    get_has_health_need_codes,
)
from gisdo.constants import (
    ALL_UNIT_TYPES,
    DOU_TYPE_MAP,
    GOVERNMENT,
)
from gisdo.index.base import (
    BaseIndex,
)
from gisdo.queue_index.config_filters import (
    SICK_CODES,
    exclude_ovz_codes,
)
from gisdo.utils import (
    AgeDeltas,
    get_report_date_or_today,
)
from gisdo.xml_helpers import (
    NOT_CALCULATED_STATUSES,
    get_dou_status,
)

from .constants import (
    get_short_day_types,
)


standard_library.install_aliases()


class EnrolledIndex(BaseIndex):
    """
    Запросы группы "Количество детей зачисленных ... "
    """

    COUNT_BY_AGE = 1
    COUNT_DISABLED = 2
    COUNT_FAMILY = 3
    COUNT_CORRECT = 4
    COUNT_HEALTH = 5
    COUNT_SHORT_STAY = 6
    COUNT_FULL_DAY_STAY = 11
    COUNT_WANT_CHANGE_DOU = 7
    COUNT_WANT_CHANGE_DOU_WITH_HN = 8
    COUNT_BY_CARE = 9
    COUNT_DECREASE_CONTINGENT = 10
    COUNT_INVALID_WITHOUT_HEALTH_NEED = 14
    COUNT_INVALID_WITH_HEALTH_NEED = 12
    COUNT_NO_INVALID_WITHOUT_HEALTH_NEED = 13

    ALGORITHM_MAP = {
        COUNT_BY_AGE: EnrolledCountByAge,
        COUNT_DISABLED: EnrolledCountByDisabled,
        COUNT_FAMILY: EnrolledCountByFamily,
        COUNT_CORRECT: EnrolledCountByCorrect,
        COUNT_HEALTH: EnrolledCountByHealth,
        COUNT_SHORT_STAY: EnrolledCountShortStay,
        COUNT_FULL_DAY_STAY: EnrolledCountFullDayStay,
        COUNT_WANT_CHANGE_DOU: EnrolledCountWantChangeDou,
        COUNT_WANT_CHANGE_DOU_WITH_HN: EnrolledCountWantChangeDouWithHN,
        COUNT_BY_CARE: EnrolledCountByCare,
        COUNT_DECREASE_CONTINGENT: PredictableDecreaseContingent,
    }

    def get_count(self, dou_type=ALL_UNIT_TYPES, index_type=COUNT_BY_AGE, **kwargs):
        if dou_type != ALL_UNIT_TYPES:
            if (not self.dou_type and dou_type != GOVERNMENT) or (
                self.dou_type and self.dou_type.code not in DOU_TYPE_MAP[dou_type]
            ):
                return 0

        result_set = EnrolledIndex.get_algorithm(index_type)(unit=self.unit, session=self.session).get_result_set(
            **kwargs
        )

        return self.session.query(result_set)


def get_count(collection, age_filter):
    """Определение количества записей в коллекции подходящих под фильтр.

    Функция применяет фильтр age_filter к коллекции collection и возвращает
    количество отфильтрованных записей.
    """

    return sum(1 for data in collection if age_filter(*data))


def get_age_filter(age, on_date):
    """Функция строит фильтр возраста."""

    down, up = AgeDeltas.get_category_deltas(age, on_date)

    def filter_(child_id, date_of_birth, *args):
        return date_of_birth > down

    if up:
        if age == 'от 2 месяцев до 6 месяцев':

            def filter_(child_id, date_of_birth, *args):
                return down < date_of_birth
        else:

            def filter_(child_id, date_of_birth, *args):
                return down < date_of_birth <= up

    return filter_


def get_age_for_date_filter(age):
    """Фильтр возраста на третью дату переданную из индекса."""
    age_border_cache = {}

    def filter_(child_id, date_of_birth, on_date, *args):
        if on_date not in age_border_cache:
            age_border_cache[age, on_date] = AgeDeltas.get_category_deltas(age, on_date)

        down, up = age_border_cache[age, on_date]

        result = date_of_birth > down

        if up:
            if age == 'от 2 месяцев до 6 месяцев':
                result = down < date_of_birth
            else:
                result = down < date_of_birth <= up

        return result

    return filter_


class Index(object):
    """Класс для вычисления показателей по группам."""

    def __init__(self, dou, report_start_date=None):
        self.dou = dou
        self._report_start_date = report_start_date

    @cached_property
    def groups(self):
        """Группы данной организации.

        Включает группы подтвержденных филиалов.
        """
        branches = FilialData.objects.filter(
            head=self.dou,
            filial__closed=False,
            status=FilialTypeStatus.APPROVE,
            filial__gisdo__not_on_federal_report=False,
        ).values_list('filial_id', flat=True)

        return (
            Group.extended_objects.with_count_norm()
            .filter(status=GroupStatusEnum.FACT)
            .filter(Q(unit=self.dou) | Q(unit__in=branches))
            .order_by('id')
        )

    @property
    def is_calculated(self):
        """Возвращает нужно ли считать free_space в группе."""
        return get_dou_status(self.dou) not in NOT_CALCULATED_STATUSES

    def enrolled_in_group_fact(self, group):
        children_in_fact = Pupil.objects.filter(grup=group, temporary_deduct=False, grup__status=GroupStatusEnum.FACT)

        return children_in_fact

    def enrolled_in_group_plan(self, group):
        """Возвращает выборку зачислений.

        Выбираются зачисления:
            - Связанные комнатой с полученной группой;
            - Дата зачисления <= контрольной даты;
            - Планованая группа;
            - Нет временного отчисления.

        :param group: Объект группы
        :type group: Group

        :return: Выборка зачислений
        :rtype: QuerySet
        """
        date_in_order = get_report_date_or_today(self._report_start_date)

        children_in_plan = (
            Pupil.objects.filter(
                grup__room_id__isnull=False,
                grup__room_id=group.room_id,
                grup__unit=group.unit,
            )
            .filter(
                Q(date_in_order__lte=date_in_order) | Q(date_in_order__isnull=True),
                temporary_deduct=False,
                grup__status=GroupStatusEnum.PLAN,
            )
            .exclude(
                children_id__in=Pupil.objects.filter(
                    grup__unit=group.unit, temporary_deduct=False, grup__status=GroupStatusEnum.FACT
                ).values_list('children_id', flat=True)
            )
        )

        return children_in_plan

    def get_enrolled_in_group_queries(self, group, query_filter, child_filter=None, pupil_filter=Q()):
        """
        Количество зачисленных в группе.
        :param group: Объект группы.
        :param child_filter: Фильтр для детей.
        :param query_filter: Название фильтра для выборки
        :param pupil_filter: Фильтр для зачислений
        """

        kid_filter = kid_filters.get(child_filter, Q())
        filter_ = filters.get(query_filter, filters['default'])()

        return (
            self.enrolled_in_group_fact(group).filter(pupil_filter).filter(filter_).filter(kid_filter),
            self.enrolled_in_group_plan(group).filter(pupil_filter).filter(filter_).filter(kid_filter),
        )

    def enrolled_in_group(self, group, query_filter, child_filter=None, pupil_filter=Q(), prep_enrolled_func=None):
        """Количество зачисленных в группе.
        :param group: Объект группы.
        :param child_filter: Фильтр для детей.
        :param query_filter: Название фильтра для выборки
        :param pupil_filter: Фильтр для зачислений
        :param prep_enrolled_func: Дополнительная функция меняющая результат
        выполнения текущего метода
        """

        enrolled_in_group_fact, enrolled_in_group_plan = self.get_enrolled_in_group_queries(
            group, query_filter, child_filter, pupil_filter
        )

        if prep_enrolled_func:
            return prep_enrolled_func(enrolled_in_group_fact, enrolled_in_group_plan)

        return list(
            chain(
                enrolled_in_group_fact.values_list('children_id', 'children__date_of_birth'),
                enrolled_in_group_plan.values_list('children_id', 'children__date_of_birth'),
            )
        )

    def directs_in_group(
        self, group, query_filter=None, children_filter=None, ovz_filter=None, pupil_filter=None, prep_direct_func=None
    ):
        """Направления в группу, влияющих на места.

        Учитывает зачисления в плановые группы,
        связанные с фактическими группами по кабинетам,
        с датой зачисления > контрольной даты.

        :param group: Объект группы
        :param query_filter: фильтр для направлений
        :param children_filter: фильтр для детей
        :param ovz_filter: фильтр ОВЗ
        :param pupil_filter: фильтр для зачислений

        :return: список направлений в группу
        """

        ovz_filter = ovz_filter or Q()
        pupil_filter = pupils_filter.get(pupil_filter, Q())
        query_filter = directs_filter.get(query_filter, Q())
        children_filter = kid_filters.get(children_filter, None)
        if children_filter is not None:
            children_filter = Q(declaration__in=Declaration.objects.filter(children_filter))
        else:
            children_filter = Q()

        direct_in_group = Direct.objects.filter(
            query_filter,
            children_filter,
            Q(group=group) & Q(status__code__in=[DRS.REGISTER, DRS.DOGOVOR]),
        )

        bounded_plan_groups = Group.objects.filter(
            Q(room_id__isnull=False, room_id=group.room_id, status=GroupStatusEnum.PLAN)
        )

        bounded_fact_groups = Group.objects.filter(
            Q(room_id__isnull=False, room_id=group.room_id, status=GroupStatusEnum.FACT)
        )

        direct_count_in_bounded_group = Direct.objects.filter(
            query_filter,
            children_filter,
            Q(group__in=bounded_plan_groups) & Q(status__code__in=[DRS.REGISTER, DRS.DOGOVOR]),
        ).exclude(
            declaration__children_id__in=Direct.objects.filter(
                Q(group__unit=group.unit)
                & Q(group__status=GroupStatusEnum.FACT)
                & Q(status__code__in=[DRS.REGISTER, DRS.DOGOVOR])
            ).values_list('declaration__children_id', flat=True)
        )

        date_in_order = get_report_date_or_today(self._report_start_date)

        pupil_direct_in_bounded_group = (
            Pupil.objects.filter(
                pupil_filter,
                grup__in=bounded_plan_groups,
                date_in_order__gt=date_in_order,
                temporary_deduct=False,
            )
            .exclude(
                Q(children_id__in=direct_count_in_bounded_group.values_list('declaration__children_id', flat=True))
                | Q(
                    children_id__in=Pupil.objects.filter(grup__in=bounded_fact_groups).values_list(
                        'children_id', flat=True
                    )
                )
            )
            .exclude(ovz_filter)
            .distinct('children_id')
        )

        if prep_direct_func:
            return prep_direct_func(direct_in_group, direct_count_in_bounded_group, pupil_direct_in_bounded_group)

        return list(
            chain(
                direct_in_group.values_list('declaration__children_id', 'declaration__children__date_of_birth'),
                direct_count_in_bounded_group.values_list(
                    'declaration__children_id', 'declaration__children__date_of_birth'
                ),
                pupil_direct_in_bounded_group.values_list('children_id', 'children__date_of_birth'),
            )
        )

    def get_capacity_in_group(self, group):
        """Наполняемость в группе."""
        # определяем тип наполняемости
        if gs_settings.USE_MAX_OCCUPANCY is None:
            is_max_occupancy = group.unit.get_use_fact_norm_cnt()
        else:
            is_max_occupancy = gs_settings.USE_MAX_OCCUPANCY

        if is_max_occupancy:
            return group.max_count or 0
        else:
            try:
                return int(group.get_count_norm())
            except (TypeError, ValueError):
                return 0

    def free_space_in_group(self, group, query_filter=None, prep_function=None):
        """Свободные места в группе.

        :param group: Группа
        :type group: Group
        :param query_filter: Фильтр запроса
        :param prep_function: Функция для преобразования данных запроса
        для отчёта
        :type prep_function: Optional[Callable]

        :return: Свободные места в группе, если prep_function равно None,
            иначе возвращаются списки с данными детей, которые учитываются
            при подсчёте свободных мест в группе
        :rtype: Union[int, list]
        """

        if not self.is_calculated:
            return 0 if not prep_function else []

        occupancy = self.get_capacity_in_group(group)

        query_filter = query_filter or 'default'
        enrolled = self.enrolled_in_group(
            group=group,
            query_filter=query_filter,
            pupil_filter=self.pupil_filter_allowing_few_fact_pupils,
        )
        directs = self.directs_in_group(group)

        enrolled_count = len(list(enrolled))
        directs_count = len(directs)
        vacant_places = group.vacant_places

        free_space = occupancy - enrolled_count - directs_count - vacant_places

        free_space = free_space if free_space > 0 else 0

        if prep_function:
            return prep_function(occupancy, enrolled_count, directs_count, vacant_places, free_space)

        return free_space

    @cached_property
    def pupil_filter(self):
        """Фильтрует зачисления при котороых дети не будут дублироваться

        Подразумевается, что у ребенка может быть не больше одной фактической
        и не больше одной плановой групп
        """
        pupil_ids = set()
        children_ids = set()

        # в приоритете фактические группы детей
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_fact(group).values_list('id', 'children_id'):
                if child_id not in children_ids:
                    children_ids.add(child_id)
                    pupil_ids.add(pupil_id)

        # у ребенка нет фактической только тогда добавляется плановая
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_plan(group).values_list('id', 'children_id'):
                if child_id not in children_ids:
                    children_ids.add(child_id)
                    pupil_ids.add(pupil_id)

        return Q(id__in=pupil_ids)

    @cached_property
    def pupil_filter_allowing_few_fact_pupils(self):
        """Фильтрует зачисления при которых дети не будут дублироваться

        Отличие от pupil_filter в том, что разрешает более одного фактического
        зачисления (например, постоянное и временное). При этом при наличии
        зачисления в фактическую группу, плановое уже не учитывается.
        """
        pupil_ids = set()
        children_ids = set()

        # в приоритете фактические группы детей
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_fact(group).values_list('id', 'children_id'):
                children_ids.add(child_id)
                pupil_ids.add(pupil_id)

        # у ребенка нет фактической только тогда добавляется плановая
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_plan(group).values_list('id', 'children_id'):
                if child_id not in children_ids:
                    children_ids.add(child_id)
                    pupil_ids.add(pupil_id)

        return Q(id__in=pupil_ids)

    @cached_property
    def plan_only_pupil_filter(self):
        """Фильтрует зачисления при котороых дети не будут дублироваться

        Подразумевается, что у ребенка может быть не больше одной фактической
        и не больше одной плановой групп.

        Возвращает только детей попавших из ПЛАНОВЫХ групп.
        """
        pupil_ids = set()
        children_ids = set()
        plan_only_pupil_ids = set()

        # в приоритете фактические группы детей
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_fact(group).values_list('id', 'children_id'):
                if child_id not in children_ids:
                    children_ids.add(child_id)
                    pupil_ids.add(pupil_id)

        # у ребенка нет фактической только тогда добавляется плановая
        for group in self.groups:
            for pupil_id, child_id in self.enrolled_in_group_plan(group).values_list('id', 'children_id'):
                if child_id not in children_ids:
                    children_ids.add(child_id)
                    pupil_ids.add(pupil_id)
                    plan_only_pupil_ids.add(pupil_id)

        return Q(id__in=plan_only_pupil_ids)

    def __call__(
        self, group_filter=None, child_filter=None, query_filter='default', plan_only=False, prep_enrolled_func=None
    ):
        if group_filter is None:

            def group_filter(_):
                return True

        pupil_filter = self.plan_only_pupil_filter if plan_only else self.pupil_filter

        summary = chain()
        for group in self.groups:
            if group_filter(group):
                summary = chain(
                    summary,
                    self.enrolled_in_group(
                        group=group,
                        child_filter=child_filter,
                        query_filter=query_filter,
                        pupil_filter=pupil_filter,
                        prep_enrolled_func=prep_enrolled_func,
                    ),
                )

        return summary

    def free_space_in_unit(self, group_filter='default', prep_function=None):
        group_filter = free_space_filters.get(group_filter, lambda _: True)

        free_space = {}
        for group in self.groups:
            if not group_filter(group):
                continue
            free_space[group] = self.free_space_in_group(group, prep_function=prep_function)

        return free_space


def predictable_decrease_contingent_filter():
    return Q(school=True)


def by_disabled():
    return Q(
        Q(grup__type__code=GroupTypeEnumerate.COMP)
        | Q(grup__type__code=GroupTypeEnumerate.COMBI, children__health_need___code__in=get_has_health_need_codes())
    )


filters = {
    'default': lambda: Q(),
    'by_disabled_1': lambda: by_disabled(),
    'by_disabled_2': lambda: by_disabled(),
    'by_disabled_3': lambda: by_disabled(),
    'by_disabled_4': lambda: by_disabled(),
    'by_disabled_5': lambda: by_disabled(),
    'by_disabled_6': lambda: by_disabled(),
    'by_disabled_7': lambda: by_disabled(),
    'by_disabled_8': lambda: by_disabled(),
    'predictable_decrease_contingent': predictable_decrease_contingent_filter,
    'combined_with_hn': lambda: (
        Q(grup__type__code=GroupTypeEnumerate.COMBI)
        & (Q(children__health_need_id__isnull=False) & ~Q(children__health_need__code=HNE.NOT))
    ),
    'compensative': lambda: (Q(grup__type__code=GroupTypeEnumerate.COMP)),
    'health': lambda: (Q(grup__type__code=GroupTypeEnumerate.HEALTH)),
    # Группы для которых все дети считаются с ОВЗ
    'hn_groups': lambda: (Q(grup__type__code__in=(GroupTypeEnumerate.COMP, GroupTypeEnumerate.HEALTH))),
    # Противоположно hn_groups
    'not_hn_groups': lambda: (~Q(grup__type__code__in=(GroupTypeEnumerate.COMP, GroupTypeEnumerate.HEALTH))),
    'without_hn_in_all_group': lambda: (
        Q(Q(children__health_need_id__isnull=True) | Q(children__health_need__code=HNE.NOT))
    ),
    'with_hn': lambda: (
        Q(
            Q(grup__type__code__in=(GroupTypeEnumerate.COMP, GroupTypeEnumerate.HEALTH))
            | Q(
                Q(
                    grup__type__code__in=(GroupTypeEnumerate.COMBI, GroupTypeEnumerate.DEV),
                    children__health_need__code__in=get_has_health_need_codes(),
                )
            )
        )
    ),
    # отличный от режима группы режим пребывания (не кратковременного)
    'not_short_actual_wt': lambda: (
        Q(
            actual_work_type__isnull=False,
        )
        & ~Q(
            actual_work_type__code__in=get_short_day_types(),
        )
    ),
    # отличный от режима группы режим пребывания (кратковременного)
    'short_actual_wt': lambda: (
        Q(
            actual_work_type__isnull=False,
            actual_work_type__code__in=get_short_day_types(),
        )
    ),
    # плановая группа кратковременного режима пребывания
    'short_wt_plan': lambda: (
        Q(
            grup__status=GroupStatusEnum.PLAN,
            temporary_deduct=False,
            grup__work_type__code__in=get_short_day_types(),
        )
    ),
}


INVALID = Q(children__is_invalid=True)
HEALTHY = Q(children__is_invalid=False)
WITH_HN = Q(children__health_need__code__in=get_has_health_need_codes())
WITHOUT_HN = Q(children__health_need_id__isnull=True) | Q(children__health_need__code=HNE.NOT)
# Наличие любого овз (включая часто болеющих, с туберкулезом и иных)
HAVE_OVZ = ~Q(Q(children__health_need_id__isnull=True) | Q(children__health_need__code=HNE.NOT))
# Проверка на наличие подтверждающего документа
HAVE_OVZ_DOC = ~Q(children__health_need_confirmation__isnull=True)
# фильтр по специфике ребенка для индекса 22.8.1
CHILDREN_FILTER_22_8_1 = Q(children__health_need__code=HNE.ADHD)
# фильтр по специфике ребенка для индекса 22.8.2
CHILDREN_FILTER_22_8_2 = Q(children__health_need__code__in=(HNE.COCHLEAR_IMPL, HNE.PHTHISIS, HNE.SICK))

FEDERAL_REPORT_EXCLUDE = HAVE_OVZ & exclude_ovz_codes(SICK_CODES)
# Зачисления где режим работы группы кратковременное пребывание
# (может быть указан в зачислении и отличаться от группы)
SHORT_TIME_ONLY = lambda: (
    Q(actual_work_type__code__in=get_short_day_types()) | Q(grup__work_type__code__in=get_short_day_types())
)

kid_filters = {
    'invalid': INVALID,
    'healthy': HEALTHY,
    'with_hn': WITH_HN,
    'without_hn': WITHOUT_HN,
    'invalid_with_hn': INVALID & WITH_HN,
    'healthy_with_hn': HEALTHY & WITH_HN,
    'invalid_without_hn': INVALID & (WITHOUT_HN | ~exclude_ovz_codes(SICK_CODES)),
    'healthy_without_hn': HEALTHY & WITHOUT_HN,
    # Исключаются дети с типами ОВЗ:
    # - "Другие"
    # - "Часто болеющие"
    # - "С туберкулезной интоксикацией"
    # - "нет"
    # - с незаполненным ОВЗ
    'fed_report_exclude': FEDERAL_REPORT_EXCLUDE,
    # Исключаются вышеуказанные типы ОВЗ + по инвалидности разделение
    'fed_report_invalid': FEDERAL_REPORT_EXCLUDE & INVALID,
    'fed_report_invalid_with_hn': FEDERAL_REPORT_EXCLUDE & INVALID,
    'fed_report_healthy': FEDERAL_REPORT_EXCLUDE & HEALTHY,
    'fed_report_healthy_with_hn': FEDERAL_REPORT_EXCLUDE & HEALTHY,
    'fed_report_exclude_for_22_8_1': FEDERAL_REPORT_EXCLUDE & CHILDREN_FILTER_22_8_1,
    'fed_report_exclude_for_22_8_2': FEDERAL_REPORT_EXCLUDE & CHILDREN_FILTER_22_8_2,
    # Проверка на наличие документа если есть валидный овз
    'with_ovz_doc': HAVE_OVZ & HAVE_OVZ_DOC,
    'invalid_with_ovz_doc': INVALID & HAVE_OVZ & HAVE_OVZ_DOC,
    'healthy_with_ovz_doc': HEALTHY & HAVE_OVZ & HAVE_OVZ_DOC,
    'short_time_only': SHORT_TIME_ONLY,
}


free_space_filters = {
    'short_stay': lambda group: True if group.work_type and group.work_type.code in get_short_day_types() else False,
    'with_health_need': lambda group: True
    if group.type and group.type.code in (GroupTypeEnumerate.COMBI, GroupTypeEnumerate.COMP)
    else False,
    'compensating': lambda group: True if group.type and group.type.code == GroupTypeEnumerate.COMP else False,
    'health_group': lambda group: True if group.type and group.type.code == GroupTypeEnumerate.HEALTH else False,
}

# Направления где режим работы группы кратковременное пребывание
# (может быть указан в направлении и отличаться от группы)
SHORT_TIME_DIRECTS = Q(work_type__code=WorkType.SHORT) | Q(group__work_type__code=WorkType.SHORT)

SHORT_TIME_PUPILS = Q(actual_work_type__code=WorkType.SHORT) | Q(grup__work_type__code=WorkType.SHORT)

directs_filter = {'short_time_directs': SHORT_TIME_DIRECTS}

pupils_filter = {'short_time_pupils': SHORT_TIME_PUPILS}

ovz_filter = Q(
    Q(~HAVE_OVZ_DOC, grup__type__code=GroupTypeEnumerate.HEALTH)
    | Q(
        WITHOUT_HN
        | Q(
            ~HAVE_OVZ_DOC,
            children__health_need__code__in=[
                HNE.OTHER,
                HNE.SICK,
                HNE.PHTHISIS,
                HNE.CELIAC,
                HNE.NEPHRO_UROL,
                HNE.CARDIOVASCULAR,
                HNE.RESPIRATORY,
                HNE.DIABETES,
                HNE.ALLERGOPATHOLOGY,
            ],
        ),
        grup__type__code__in=[
            GroupTypeEnumerate.DEV,
            GroupTypeEnumerate.COMBI,
            GroupTypeEnumerate.YOUNG,
            GroupTypeEnumerate.CARE,
            GroupTypeEnumerate.FAMILY,
        ],
    )
)
