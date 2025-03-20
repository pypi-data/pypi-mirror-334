from django.db.models import (
    Count,
    Q,
)
from future.builtins import (
    object,
)

from kinder.core.alloc.helpers import (
    GroupHelper,
)
from kinder.core.dict.models import (
    GroupState,
    HealthNeed,
    UnitKind,
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
    UnitStatus,
)

from gisdo import (
    xml_helpers,
)
from gisdo.algorithm.capacities import (
    CommonCountAlgorithm,
    CompensatingAlgorithm,
    HealthGroupAlgorithm,
    HealthNeedAlgorithm as CapacitiesHealthNeedAlgorithm,
    ShortStayAlgorithm,
)
from gisdo.constants import (
    AGE_CATEGORIES_CUT,
    AGE_CUT_CATEGORY_MAP,
    AGE_CUT_DEFAULT_CATEGORY,
    AGE_CUT_SUBCATEGORY_MAP,
    AGE_EIGHT_CATEGORY_MAP,
    AGE_EIGHT_DEFAULT_CATEGORY,
    AGE_EIGHT_SUBCATEGORY_MAP,
    ALL_UNIT_TYPES,
    DOU_TYPE_MAP,
    GOVERNMENT,
)
from gisdo.index.base import (
    BaseIndex,
)


def _get_age_map(age_category):
    cut_values = list(AGE_CATEGORIES_CUT.values())

    if age_category in cut_values:
        subcategory_map, category_map, default_category = (
            AGE_CUT_SUBCATEGORY_MAP,
            AGE_CUT_CATEGORY_MAP,
            AGE_CUT_DEFAULT_CATEGORY,
        )
    else:
        subcategory_map, category_map, default_category = (
            AGE_EIGHT_SUBCATEGORY_MAP,
            AGE_EIGHT_CATEGORY_MAP,
            AGE_EIGHT_DEFAULT_CATEGORY,
        )

    return subcategory_map, category_map, default_category


def free_space_in_age_category(free_space_by_group, age_category):
    subcategory_map, category_map, default_category = _get_age_map(age_category)

    total = 0
    for group in free_space_by_group:
        free_space_count = free_space_by_group[group]

        # Если у группы есть возрастная подкатегория,
        # то соотношение проводится по ней.
        if group.sub_age_cat:
            # Возраст до в годах (В БД хранится целое число месяцев).
            # Минимальное значение 0, максимальное 8.
            to_years, _ = divmod(group.sub_age_cat.to_age, 12)
            if to_years in subcategory_map[age_category]:
                total += free_space_count
        # В противном случае по возрастной категории, если она есть.
        elif group.age_cat:
            if group.age_cat.code in category_map[age_category]:
                total += free_space_count
        else:
            if age_category and age_category == default_category:
                total += free_space_count
    return total


def childrens_in_age_category(data_by_group, age_category):
    """
    Аналог функции free_space_in_age_category за исключением того,
    что считаются не свободные места, а информация о детях, которые участвуют
    при расчёте свободных мест
    """

    subcategory_map, category_map, default_category = _get_age_map(age_category)

    data = []
    for group, group_info in data_by_group.items():
        group_data = (
            '',
            '',
            group_info,
            'group',
            group.id,
        )

        # Если у группы есть возрастная подкатегория,
        # то соотношение проводится по ней.
        if group.sub_age_cat:
            # Возраст до в годах (В БД хранится целое число месяцев).
            # Минимальное значение 0, максимальное 8.
            to_years, _ = divmod(group.sub_age_cat.to_age, 12)
            if to_years in subcategory_map[age_category]:
                data.append(group_data)
        # В противном случае по возрастной категории, если она есть.
        elif group.age_cat:
            if group.age_cat.code in category_map[age_category]:
                data.append(group_data)
        else:
            if age_category and age_category == default_category:
                data.append(group_data)
    return data


class CapacitiesIndex(BaseIndex):
    """ """

    COMMON_COUNT = 1
    SHORT_STAY = 2
    HEALTH_NEED = 3
    COMPENSATING = 4
    HEALTH = 5

    ALGORITHM_MAP = {
        COMMON_COUNT: CommonCountAlgorithm,
        SHORT_STAY: ShortStayAlgorithm,
        HEALTH_NEED: CapacitiesHealthNeedAlgorithm,
        COMPENSATING: CompensatingAlgorithm,
        HEALTH: HealthGroupAlgorithm,
    }

    class Ctx(object):
        kind = 1

        def __init__(self, unit_id):
            self.group_unit = unit_id
            self.group_states = list(GroupState.objects.values_list('code', flat=True))

    WORK = 1
    RECONSTRUCTION = 2
    IN_CAPITAL_REPAIR = 3
    SUSPENDED = 4
    NO_CONTINGENT = 5
    PENDING_OPEN = 6

    STATUSES = {
        UnitStatus.RECONSTRUCTION: RECONSTRUCTION,
        UnitStatus.IN_CAPITAL_REPAIR: IN_CAPITAL_REPAIR,
        UnitStatus.SUSPENDED: SUSPENDED,
        UnitStatus.PENDING_OPEN: PENDING_OPEN,
    }

    @classmethod
    def _get_dou_status(cls, dou):
        filials = (
            FilialData.objects.filter(
                head=dou,
                status=FilialTypeStatus.APPROVE,
                filial__closed=False,
                filial__gisdo__not_on_federal_report=False,
            )
            .values_list('filial_id', flat=True)
            .iterator()
        )

        if (
            Pupil.objects.filter(grup__status=GroupStatusEnum.FACT, temporary_deduct=False)
            .filter(Q(grup__unit=dou) | Q(grup__unit__in=filials))
            .exists()
        ):
            status = cls.WORK
        elif dou.status == UnitStatus.RECONSTRUCTION:
            status = cls.STATUSES[UnitStatus.RECONSTRUCTION]
        elif dou.status == UnitStatus.IN_CAPITAL_REPAIR:
            status = cls.STATUSES[UnitStatus.IN_CAPITAL_REPAIR]
        elif dou.status == UnitStatus.SUSPENDED:
            status = cls.STATUSES[UnitStatus.SUSPENDED]
        elif dou.status == UnitStatus.PENDING_OPEN:
            status = cls.STATUSES[UnitStatus.PENDING_OPEN]
        else:
            status = cls.NO_CONTINGENT

        return status

    def __init__(self, unit):
        super(CapacitiesIndex, self).__init__(unit, session=None)

        _, self._cache = GisdoGroupHelper(CapacitiesIndex.Ctx(self.unit.id)).getList()

        self.need_calculate = self._get_dou_status(unit) not in (
            xml_helpers.RECONSTRUCTION,
            xml_helpers.IN_CAPITAL_REPAIR,
            xml_helpers.SUSPENDED,
            xml_helpers.PENDING_OPEN,
        )

    @staticmethod
    def _get_age_map(age_category):
        cut_values = list(AGE_CATEGORIES_CUT.values())

        if age_category in cut_values:
            subcategory_map, category_map, default_category = (
                AGE_CUT_SUBCATEGORY_MAP,
                AGE_CUT_CATEGORY_MAP,
                AGE_CUT_DEFAULT_CATEGORY,
            )
        else:
            subcategory_map, category_map, default_category = (
                AGE_EIGHT_SUBCATEGORY_MAP,
                AGE_EIGHT_CATEGORY_MAP,
                AGE_EIGHT_DEFAULT_CATEGORY,
            )

        return subcategory_map, category_map, default_category

    def get_count(self, index_type=COMMON_COUNT, dou_type=ALL_UNIT_TYPES, **kwargs):
        if not self.need_calculate:
            return 0

        if dou_type != ALL_UNIT_TYPES:
            if (not self.dou_type and dou_type != GOVERNMENT) or (
                self.dou_type and self.dou_type.code not in DOU_TYPE_MAP[dou_type]
            ):
                return 0

        result_list = CapacitiesIndex.get_algorithm(index_type)().get_result_set(cache=self._cache)

        age_category = kwargs.get('age_category', None)
        subcategory_map, category_map, default_category = self._get_age_map(age_category)

        total = 0
        for group in result_list:
            # Если у группы есть возрастная подкатегория,
            # то соотношение проводится по ней
            if group.sub_age_cat:
                if group.sub_age_cat.code in subcategory_map[age_category]:
                    total += group.cntFree if group.cntFree >= 0 else 0
            # в противном случае по возрастной категории,
            # которая обязательна.
            elif group.age_cat:
                if group.age_cat.code in category_map[age_category]:
                    total += group.cntFree if group.cntFree >= 0 else 0
            else:
                if age_category and age_category == default_category:
                    total += group.cntFree if group.cntFree >= 0 else 0
        return total


class GisdoGroupHelper(GroupHelper):
    @staticmethod
    def _get_group_cnt_info(unit_scope_ids):
        """
        @type   unit_scope_ids: list
        @param  unit_scope_ids: список садов, для групп которых необходимо
        посчитать кол-во зачислений, кол-во новых направлений и кол-во всех
        направлений

        @return: {dict}
        {15360: {'cnt_direct': 0,
                 'cnt_direct_new': 0,
                 'cnt_pupil': 27},
         15361: {'cnt_direct': 2,
                 'cnt_direct_new': 2,
                 'cnt_pupil': 24},
         ...}
         где 15360 - id группы

        """
        # TODO: Переименовать
        group_cnt_info = {}

        fact_groups_in_units = Group.objects.filter(unit_id__in=unit_scope_ids, status=GroupStatusEnum.FACT)

        pupils_fact = Pupil.objects.filter(
            temporary_deduct=False, grup__in=fact_groups_in_units.values_list('id', flat=True)
        )
        for group in pupils_fact.values('grup_id', 'grup__room_id', 'grup__vacant_places').annotate(
            cnt=Count('children')
        ):
            group_id = group['grup_id']
            group_cnt_info[group_id] = dict(
                cnt_pupil=group['cnt'], cnt_direct=0, cnt_direct_new=0, cnt_vacant_places=group['grup__vacant_places']
            )

            room_id = group['grup__room_id']
            if room_id:
                pupils_in_binding_plan_groups_cnt = (
                    Pupil.objects.filter(
                        temporary_deduct=False,
                        grup__status=GroupStatusEnum.PLAN,
                        grup__room_id=room_id,
                    )
                    .exclude(children_id__in=pupils_fact.values_list('children_id', flat=True))
                    .count()
                )

                group_cnt_info[group_id]['cnt_pupil'] += pupils_in_binding_plan_groups_cnt

        # Подсчет новых направлений
        new_directs_in_fact = Direct.objects.filter(
            group_id__in=fact_groups_in_units.values_list('id', flat=True), status__code='new'
        )
        for direct in new_directs_in_fact.values('group_id', 'group__room_id').annotate(cnt=Count('declaration')):
            group_id = direct['group_id']
            if group_id not in group_cnt_info:
                group_cnt_info[group_id] = dict(cnt_pupil=0)
            group_cnt_info[group_id]['cnt_direct_new'] = direct['cnt']
        for group in fact_groups_in_units:
            binding_plan_groups = Group.objects.filter(status=GroupStatusEnum.PLAN).filter(
                Q(room_id__isnull=False, room_id=group.room_id)
            )

            if group.id in group_cnt_info:
                group_cnt_info[group.id]['cnt_direct_new'] += (
                    Direct.objects.filter(
                        status__code=DRS.NEW, group_id__in=binding_plan_groups.values_list('id', flat=True)
                    )
                    .exclude(
                        declaration__children_id__in=new_directs_in_fact.values_list(
                            'declaration__children_id', flat=True
                        )
                    )
                    .count()
                )

        # Подсчет всех направлений в фактические группы.
        directs_in_fact = Direct.objects.filter(group_id__in=fact_groups_in_units.values_list('id', flat=True)).filter(
            status__code__in=[DRS.REGISTER, DRS.DOGOVOR]
        )
        for direct in directs_in_fact.values('group_id', 'group__room_id').annotate(cnt=Count('declaration')):
            group_id = direct['group_id']
            if group_id not in group_cnt_info:
                group_cnt_info[group_id] = dict(
                    cnt_pupil=0,
                    cnt_direct_new=0,
                )
            group_cnt_info[group_id]['cnt_direct'] = direct['cnt']
        for group in fact_groups_in_units:
            binding_plan_groups = Group.objects.filter(status=GroupStatusEnum.PLAN).filter(
                Q(room_id__isnull=False, room_id=group.room_id)
            )

            if group.id in group_cnt_info:
                group_cnt_info[group.id]['cnt_direct'] += (
                    Direct.objects.filter(
                        status__code__in=[DRS.REGISTER, DRS.DOGOVOR],
                        group_id__in=binding_plan_groups.values_list('id', flat=True),
                    )
                    .exclude(
                        declaration__children_id__in=directs_in_fact.values_list('declaration__children_id', flat=True)
                    )
                    .count()
                )

        return group_cnt_info

    def _get_query(self):
        """
        Внутреняя функция получения запроса на выборку групп из ДОУ без
        нераспределенных детей.
        :return list список груп, не Quryset!
        """
        q = Group.extended_objects.with_count_norm().select_related(
            'sub_age_cat', 'age_cat', 'unit', 'type', 'unit__parent', 'unit__parent__parent'
        )
        q = q.filter(Q(state__code__in=self.group_states) | Q(state__code__isnull=True))
        # TODO: убрать проверку на тип организации, когда реализуют ограничение
        # при создание и изменении групп
        q = q.filter(self.getUnitRange()).filter(unit__kind_id=UnitKind.DOU)
        # Текущее доукомплектование
        q = q.filter(status=GroupStatusEnum.FACT)
        # Исключим плановые группы, у которых есть направления
        direct_to_plan = Direct.objects.filter(
            status__code__in=['confirm', 'register', 'new'], group__status=GroupStatusEnum.PLAN
        ).filter(self.getUnitRange(prefix='group'))
        group_list = direct_to_plan.values_list('group__id', flat=True).distinct('group__unit__id')
        q = q.exclude(id__in=group_list)

        health_need = getattr(self.context, 'health_need', None)
        if health_need:
            hn = HealthNeed.objects.get(id=health_need)
            if hn.name != 'Нет':
                q = q.filter(Q(health_need=hn) | Q(type__code='combined'))

        result = []
        unit_scope_ids = q.values_list('unit__id', flat=True)
        unit_scope_ids = list(set(unit_scope_ids))
        group_cnt_info = self._get_group_cnt_info(unit_scope_ids)

        for group in q:
            group_id = group.id
            cnt = group_cnt_info.get(
                group_id,
                {
                    'cnt_pupil': 0,
                    'cnt_direct': 0,
                    'cnt_direct_new': 0,
                    'cnt_vacant_places': 0,
                },
            )
            self._set_cnt(group, cnt)

            if self._check_filter(group):
                result.append(group)

        return result, unit_scope_ids

    def getUnitRange(self, prefix=None):
        if prefix:
            search_key = prefix + '__unit_id'
        else:
            search_key = 'unit_id'
        return Q(**{search_key: self.context.group_unit})

    def _set_cnt(self, group, group_cnt):
        super(GisdoGroupHelper, self)._set_cnt(group, group_cnt)

        if group.cntFree > 0:
            group.cntFree -= group_cnt['cnt_vacant_places'] or 0

        if group.cntFree < 0:
            group.cntFree = 0
