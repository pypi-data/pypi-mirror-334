import datetime
from typing import (
    Callable,
)

from dateutil.relativedelta import (
    relativedelta,
)
from sqlalchemy import (
    and_,
    or_,
)
from sqlalchemy.orm import (
    load_only,
)
from sqlalchemy.sql.expression import (
    false,
    true,
)

from kinder.core.declaration_status.models import (
    DSS,
)
from kinder.core.dict.models import (
    HNE,
    GroupTypeEnumerate,
)

from gisdo.alchemy_models import (
    AlchemyChildren,
    AlchemyDeclaration,
    AlchemyDeclarationStatus,
    AlchemyGroupType,
    AlchemyGroupWorkType,
)
from gisdo.algorithm.base import (
    BaseEnrolledAlgorithm,
)
from gisdo.algorithm.constants import (
    get_all_day_work_types,
    get_short_day_types,
)
from gisdo.algorithm.utils import (
    HealthNeedIdsProvider,
)
from gisdo.constants import (
    ALL,
)
from gisdo.utils import (
    AgeDeltas,
    merge_unical_data_in_lists,
)


def get_22_index(enrolled_index):
    return list(
        enrolled_index(
            group_filter=lambda group: (
                group.type
                and (group.type.code == GroupTypeEnumerate.COMP or group.type.code == GroupTypeEnumerate.COMBI)
            )
        )
    )


def get_22_x_index(enrolled_index, health_need_list):
    index_22_x_comp = list(
        enrolled_index(
            group_filter=lambda group: (
                group.type
                and (group.type.code == GroupTypeEnumerate.COMP)
                and (group.health_need and group.health_need.code in health_need_list)
            )
        )
    )

    index_22_x_combi = list(
        enrolled_index(
            group_filter=lambda group: (
                group.type
                and (group.type.code == GroupTypeEnumerate.COMBI)
                and (group.health_need and group.health_need.code in health_need_list)
            ),
            child_filter='fed_report_exclude',
        )
    )

    index_22_x_total = merge_unical_data_in_lists(
        index_22_x_comp,
        index_22_x_combi,
    )

    return index_22_x_total


def get_22_8_x_index(
    enrolled_index: Callable,
    health_need_list: tuple[str],
    children_filter: str = 'fed_report_exclude',
) -> list[tuple]:
    """Индекс показателя 22.8.

    Args:
           enrolled_index: Вызываемый объект класса functools.partial
           health_need_list: Кортеж с кодами специфики групп
           children_filter: Строка с наименованием фильтра для детей

    Returns: Итоговый список с данными детей, подходящих под условия индекса
    """

    index_22_8_comp = list(
        enrolled_index(
            group_filter=lambda group: (
                group.type
                and (group.type.code == GroupTypeEnumerate.COMP)
                and (
                    group.health_need is None
                    or (
                        group.health_need.code == HNE.NOT
                        or (group.health_need.id and group.health_need.code in health_need_list)
                    )
                )
            )
        )
    )

    index_22_8_combi = list(
        enrolled_index(
            group_filter=lambda group: (
                group.type
                and (group.type.code == GroupTypeEnumerate.COMBI)
                and (
                    group.health_need is None
                    or (
                        group.health_need.code == HNE.NOT
                        or (group.health_need.id and group.health_need.code in health_need_list)
                    )
                )
            ),
            child_filter=children_filter,
        )
    )

    index_22_8_total = merge_unical_data_in_lists(
        index_22_8_comp,
        index_22_8_combi,
    )

    return index_22_8_total


def get_26_index(enrolled_index):
    """Индекс показателя 26."""
    return list(
        enrolled_index(
            group_filter=lambda group: (group.work_type and group.work_type.code in get_all_day_work_types())
        )
    )


def get_27_index(enrolled_index):
    """Индекс показателя 27."""
    return list(
        enrolled_index(group_filter=lambda group: (group.work_type and group.work_type.code in get_short_day_types()))
    )


def get_28_index(enrolled_index):
    """Индекс показателя 28."""

    index_27 = get_27_index(enrolled_index)

    # дети не из факт. групп кратковременного пребывания, но
    # посещающие ДОО с этим режимом
    not_short_wt_groups_pupils_with_short_status_idx = list(
        enrolled_index(
            group_filter=lambda group: not (group.work_type and group.work_type.code in get_short_day_types()),
            query_filter='short_actual_wt',
        )
    )

    # дети в плановых группах кратковременного пребывания
    # без зачислений в фактические
    short_wt_plan_groups_pupils_idx = list(
        enrolled_index(
            group_filter=lambda group: not (group.work_type and group.work_type.code in get_short_day_types()),
            query_filter='short_wt_plan',
            plan_only=True,
        )
    )

    index_28 = merge_unical_data_in_lists(
        index_27,
        not_short_wt_groups_pupils_with_short_status_idx,
        short_wt_plan_groups_pupils_idx,
    )
    return index_28


def get_30_index(enrolled_index):
    """Показатель 30. Численность детей-инвалидов, не имеющих ОВЗ.


    все инвалиды
    исключаем тех кто в комп группах
        далее из HealthNeed.NO, HNE.SICK, HNE.PHTHISIS, HNE.OTHER, allergopathology,
        diabetes, respiratory, cardiovascular, nephro_urol, celiac
        исключаем с документом, подтверждающим овз
    исключаются с другими овз
    """
    return list(
        enrolled_index(
            group_filter=lambda group: (
                (group.type and group.type.code != GroupTypeEnumerate.COMP) or group.type is None
            ),
            child_filter='invalid_without_hn',
        )
    )


def get_30_1_index(enrolled_index):
    """Показатель 30.1

    дети в группах "Компенсирующий" с галкой инвалид
    в остальных группах с галкой инвалид и с
        наличием ОВЗ Комбинированной (вне зависимости от документа) и с ОВЗ=
        HealthNeed.NO, HNE.SICK, HNE.PHTHISIS, HNE.OTHER , allergopathology,
        diabetes, respiratory, cardiovascular, nephro_urol, celiac,
        у которых есть документ ОВЗ и другие овз вне зависимости от документа
    """
    index_30_1_by_group_type = list(
        enrolled_index(
            group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.COMP),
            child_filter='invalid',
        )
    )
    index_30_1_by_attr = list(
        enrolled_index(
            group_filter=lambda group: (
                (group.type and group.type.code != GroupTypeEnumerate.COMP) or group.type is None
            ),
            child_filter='fed_report_invalid_with_hn',
        )
    )

    index_30_1_total = merge_unical_data_in_lists(
        index_30_1_by_group_type,
        index_30_1_by_attr,
    )

    return index_30_1_total


def get_30_2_index(enrolled_index):
    """Показатель 30.2

    аналогичен 30.1 только дети без инвалидности (происходит их исключение)
    дети в группах "Компенсирующий" без галки инвалид
        в остальных группах с галкой инвалид и с наличием ОВЗ Комбинированной
        (вне зависимости от документа) и с ОВЗ= HealthNeed.NO, HNE.SICK,
        HNE.PHTHISIS, HNE.OTHER , allergopathology, diabetes, respiratory,
        cardiovascular, nephro_urol, celiac, у которых есть документ ОВЗ
        и другие овз вне зависимости от документа
    """
    index_30_2_by_group_type = list(
        enrolled_index(
            group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.COMP),
            child_filter='healthy',
        )
    )
    index_30_2_by_attr = list(
        enrolled_index(
            group_filter=lambda group: (
                (group.type and group.type.code != GroupTypeEnumerate.COMP) or group.type is None
            ),
            child_filter='fed_report_healthy_with_hn',
        )
    )

    index_30_2_total = merge_unical_data_in_lists(
        index_30_2_by_group_type,
        index_30_2_by_attr,
    )

    return index_30_2_total


class EnrolledCountByAge(BaseEnrolledAlgorithm):
    """Кол-во зачислений в Ф группы, без временно отчисленных детей"""

    def get_result_set(self, **kwargs):
        not_temporary_deduct_pupils = super(EnrolledCountByAge, self).get_result_set()
        groups_this_unit = self._get_groups()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledInvalidWithoutHealthNeed(BaseEnrolledAlgorithm):
    """Дети-инвалиды без ограниченных возможностей здоровья (30 <= 19.1)."""

    def get_result_set(self, **kwargs):
        not_temporary_deduct_pupils = super(EnrolledInvalidWithoutHealthNeed, self).get_result_set()
        groups_this_unit = self._get_groups()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                kids, and_(kids.c.children_id == not_temporary_deduct_pupils.c.children_id, kids.c.is_invalid == true())
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code != GroupTypeEnumerate.HEALTH,
                        AlchemyGroupType.code != GroupTypeEnumerate.COMP,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code != GroupTypeEnumerate.HEALTH,
                        AlchemyGroupType.code != GroupTypeEnumerate.COMP,
                    ),
                ),
            )
            .filter(kids.c.health_need_id is None)
            .subquery()
        )


class EnrolledInvalidWithHealthNeed(BaseEnrolledAlgorithm):
    """Дети-инвалиды c ограниченными возможностями здоровья (30.1 <= 19.1)."""

    def get_result_set(self, **kwargs):
        not_temporary_deduct_pupils = super(EnrolledInvalidWithHealthNeed, self).get_result_set()
        groups_this_unit = self._get_groups()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                kids, and_(kids.c.children_id == not_temporary_deduct_pupils.c.children_id, kids.c.is_invalid == true())
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                    ),
                ),
            )
            .filter(
                or_(
                    or_(
                        AlchemyGroupType.code == GroupTypeEnumerate.HEALTH,
                        AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                    ),
                    kids.c.health_need_id is not None,
                )
            )
            .subquery()
        )


class EnrolledNoInvalidWithHealthNeed(BaseEnrolledAlgorithm):
    """Дети неинвалиды, имеющие потребность по здоровью.

    30.2 <= 19.1,
    30.1 + 30.2 >= 22.1 + 22.2 + 22.3 + 22.4 + 22.5 + 22.6 + 22.7 + 22.8
    """

    def get_result_set(self, **kwargs):
        not_temporary_deduct_pupils = super(EnrolledNoInvalidWithHealthNeed, self).get_result_set()
        groups_this_unit = self._get_groups()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                kids,
                and_(kids.c.children_id == not_temporary_deduct_pupils.c.children_id, kids.c.is_invalid == false()),
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                    ),
                ),
            )
            .filter(
                or_(
                    or_(
                        AlchemyGroupType.code == GroupTypeEnumerate.HEALTH,
                        AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                    ),
                    kids.c.health_need_id is not None,
                )
            )
            .subquery()
        )


class PredictableDecreaseContingent(EnrolledCountByAge):
    """Прогнозируемое уменьшение контингента

    - количество детей в текущих группах (реестр "Группы")
      возраст которых больше 6,5 лет
    - дата расчета возраста = текущая дата
    """

    def _kids(self, **kwargs):
        today = datetime.date.today()
        # Если ДР раньше этой даты, то ребенку > 6,5 лет.
        date_of_birth_border = today - relativedelta(years=6, months=6)

        kids = (
            self.session.query(AlchemyChildren.id.label('children_id'), AlchemyChildren.date_of_birth)
            .filter(AlchemyChildren.date_of_birth < date_of_birth_border)
            .subquery('kids')
        )

        return kids


class EnrolledCountByCare(BaseEnrolledAlgorithm):
    """Группы по присмотру и уходу"""

    def get_result_set(self, **kwargs):
        not_temporary_deduct_pupils = super(EnrolledCountByCare, self).get_result_set()
        groups_this_unit = self._get_groups()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_is_family == false(),
                        or_(
                            groups_this_unit.c.fact_group_is_care == true(),
                            groups_this_unit.c.fact_group_is_young_children == true(),
                        ),
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_is_family == false(),
                        or_(
                            groups_this_unit.c.plan_group_is_care == true(),
                            groups_this_unit.c.plan_group_is_young_children == true(),
                        ),
                    ),
                ),
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.DEV,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.DEV,
                    ),
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledCountByDisabled(BaseEnrolledAlgorithm):
    def get_result_set(self, health_need=None, **kwargs):
        groups_this_unit = self._get_groups()
        not_temporary_deduct_pupils = super(EnrolledCountByDisabled, self).get_result_set()
        kids = self._kids(**kwargs)

        _filter = ''
        if health_need:
            _filter = and_(
                or_(
                    groups_this_unit.c.fact_group_health_need.code.in_(health_need),
                    groups_this_unit.c.plan_group_health_need.code.in_(health_need),
                ),
                or_(
                    AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                    and_(
                        AlchemyGroupType.code == GroupTypeEnumerate.COMBI,
                        kids.c.health_need_id.isnot(None),
                        kids.c.health_need_.code.notin_(HealthNeedIdsProvider.get_not_health_need()),
                    ),
                ),
            )

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        or_(
                            AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                            AlchemyGroupType.code == GroupTypeEnumerate.COMBI,
                        ),
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        or_(
                            AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                            AlchemyGroupType.code == GroupTypeEnumerate.COMBI,
                        ),
                    ),
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .filter(_filter)
            .subquery()
        )


class EnrolledCountByFamily(BaseEnrolledAlgorithm):
    def get_result_set(self, **kwargs):
        groups_this_unit = self._get_groups()
        not_temporary_deduct_pupils = super(EnrolledCountByFamily, self).get_result_set()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.DEV,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.DEV,
                    ),
                ),
            )
            .filter(
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_is_family == true(),
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_is_family == true(),
                    ),
                )
            )
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledCountByCorrect(BaseEnrolledAlgorithm):
    def get_result_set(self, **kwargs):
        groups_this_unit = self._get_groups()
        not_temporary_deduct_pupils = super(EnrolledCountByCorrect, self).get_result_set()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.COMP,
                    ),
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledCountByHealth(BaseEnrolledAlgorithm):
    def get_result_set(self, **kwargs):
        groups_this_unit = self._get_groups()
        not_temporary_deduct_pupils = super(EnrolledCountByHealth, self).get_result_set()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                AlchemyGroupType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.HEALTH,
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_type_id == AlchemyGroupType.id,
                        AlchemyGroupType.code == GroupTypeEnumerate.HEALTH,
                    ),
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledCountStay(BaseEnrolledAlgorithm):
    def get_result_set(self, group_work_types=None, **kwargs):
        groups_this_unit = self._get_groups()
        not_temporary_deduct_pupils = super(EnrolledCountStay, self).get_result_set()
        kids = self._kids(**kwargs)

        return (
            self.session.query(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .join(
                groups_this_unit,
                or_(
                    groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                    groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                ),
            )
            .join(
                AlchemyGroupWorkType,
                or_(
                    and_(
                        groups_this_unit.c.fact_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.fact_group_work_type_id == AlchemyGroupWorkType.id,
                        AlchemyGroupWorkType.code.in_(group_work_types),
                    ),
                    and_(
                        groups_this_unit.c.plan_group_id == not_temporary_deduct_pupils.c.grup_id,
                        groups_this_unit.c.plan_group_work_type_id == AlchemyGroupWorkType.id,
                        AlchemyGroupWorkType.code.in_(group_work_types),
                    ),
                ),
            )
            .join(kids, kids.c.children_id == not_temporary_deduct_pupils.c.children_id)
            .group_by(not_temporary_deduct_pupils.c.children_id, kids.c.date_of_birth)
            .subquery()
        )


class EnrolledCountShortStay(EnrolledCountStay):
    def get_result_set(self, **kwargs):
        return super(EnrolledCountShortStay, self).get_result_set(get_short_day_types(), **kwargs)


class EnrolledCountFullDayStay(EnrolledCountStay):
    def get_result_set(self, **kwargs):
        return super(EnrolledCountFullDayStay, self).get_result_set(get_all_day_work_types(), **kwargs)


class EnrolledCountWantChangeDou(BaseEnrolledAlgorithm):
    def get_result_set(self, **kwargs):
        fact_group_this_unit = self._get_fact_group()
        not_temporary_deduct_pupils = super(EnrolledCountWantChangeDou, self).get_result_set()
        kids = self._kids(**kwargs)
        pupils = self.session.query(not_temporary_deduct_pupils).join(fact_group_this_unit).subquery()
        pupils = (
            self.session.query(kids.c.id.label('children_id'))
            .join(pupils, pupils.c.children_id == kids.c.id)
            .subquery()
        )

        want_change_dou_status = (
            self.session.query(AlchemyDeclarationStatus)
            .filter(AlchemyDeclarationStatus.code == DSS.WANT_CHANGE_DOU)
            .subquery()
        )
        declarations_want_change_dou = (
            self.session.query(AlchemyDeclaration)
            .join(want_change_dou_status)
            .join(pupils, AlchemyDeclaration.children_id == pupils.c.children_id)
            .options(load_only('children_id'))
            .distinct()
            .subquery()
        )

        return declarations_want_change_dou


class EnrolledCountWantChangeDouWithHN(EnrolledCountWantChangeDou):
    def _kids(self, **kwargs):
        age_range = kwargs.get('age_range', ALL)
        age_on_date = kwargs.get('on_date', AgeDeltas.calculate_date)
        down, up = AgeDeltas.get_category_deltas(age_range, age_on_date)
        kids = (
            self.session.query(AlchemyChildren.id.label('children_id'), AlchemyChildren.date_of_birth)
            .filter(
                AlchemyChildren.date_of_birth > down,
                AlchemyChildren.date_of_birth <= up,
                AlchemyChildren.health_need_id != None,
            )
            .options(load_only('id'))
            .subquery('kids')
        )
        return kids
