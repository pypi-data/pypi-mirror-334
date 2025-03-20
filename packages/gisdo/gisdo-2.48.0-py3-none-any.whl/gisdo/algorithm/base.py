from abc import (
    ABCMeta,
    abstractmethod,
)
from datetime import (
    datetime,
)

from future.builtins import (
    object,
)
from future.utils import (
    with_metaclass,
)
from sqlalchemy import (
    and_,
)
from sqlalchemy.orm import (
    load_only,
)

from kinder.core.declaration_status.models import (
    DSS,
)
from kinder.core.dict.models import (
    UnitKind,
)
from kinder.core.group.models import (
    GroupStatusEnum,
)

from gisdo.alchemy_models import (
    AlchemyChildren,
    AlchemyDeclaration,
    AlchemyDeclarationUnit,
    AlchemyGroup,
    AlchemyPupil,
    AlchemyUnit,
)
from gisdo.constants import (
    ALL,
)
from gisdo.utils import (
    AgeDeltas,
    DateMixin,
)


class BaseAlgorithm(with_metaclass(ABCMeta, object)):
    def __init__(self, session, unit):
        self.unit = unit
        self.unit_mo_id = unit.unit_mo_id
        self.session = session

    def _kids(self, **kwargs):
        """
        Дети с датой рождения из age_range
        """

        age_range = kwargs.get('age_range', ALL)
        age_on_date = kwargs.get('on_date', AgeDeltas.calculate_date)
        down, up = AgeDeltas.get_category_deltas(age_range, age_on_date)
        kids = (
            self.session.query(AlchemyChildren)
            .filter(AlchemyChildren.date_of_birth > down, AlchemyChildren.date_of_birth <= up)
            .options(load_only('id'))
            .subquery()
        )
        return kids

    @abstractmethod
    def get_result_set(self):
        pass


class BaseApplicationAlgorithm(with_metaclass(ABCMeta, type('NewBase', (BaseAlgorithm, DateMixin), {}))):
    def _kids(self, **kwargs):
        """
        Дети с датой рождения из age_range
        """

        age_range = kwargs.get('age_range', ALL)
        age_on_date = kwargs.get('on_date', AgeDeltas.calculate_date)
        down, up = AgeDeltas.get_category_deltas(age_range, age_on_date)
        kids = (
            self.session.query(AlchemyChildren)
            .filter(AlchemyChildren.date_of_birth > down, AlchemyChildren.date_of_birth <= up)
            .options(load_only('id', 'date_of_birth'))
            .subquery()
        )
        return kids

    def _dou_units(self):
        """
        Достаём для каждой желаемой организации
        привязаннкю к ней организации
        """
        # Организация с типом ДОО
        dou_units = (
            self.session.query(AlchemyUnit)
            .filter(AlchemyUnit.kind_id == UnitKind.DOU)
            .options(load_only('id'))
            .subquery()
        )
        # JOIN с желаемыми организациями.
        return (
            self.session.query(AlchemyDeclarationUnit, 'unit_id')
            .join(dou_units)
            .options(load_only('id', 'ord', 'declaration_id'))
            .subquery()
        )

    def _get_base_query(self, **kwargs):
        """
        Базовый запрос для группы показателей
        "Общее количество поданных заявлений..."
        """

        # Фильтрация по отчетному периоду.
        begin_report_period, end_report_period = self.get_report_period()

        _base_query = (
            self.session.query(AlchemyDeclaration, 'ord', 'unit_id')
            .filter(
                AlchemyDeclaration.date >= begin_report_period,
                AlchemyDeclaration.date <= datetime.combine(end_report_period, datetime.max.time()),
            )
            .join(self._dou_units())
            .join(self._kids(**kwargs))
            .options(load_only('portal', 'status_id', 'work_type_id', 'id', 'children_id'))
            .subquery()
        )
        return _base_query

    @abstractmethod
    def get_result_set(self, **kwargs):
        pass


class BaseEnrolledAlgorithm(with_metaclass(ABCMeta, BaseAlgorithm)):
    def _get_fact_group(self):
        """
        Получаем фактические группы данной организации.
        """

        fact_group_this_unit = (
            self.session.query(AlchemyGroup)
            .filter(AlchemyGroup.status == GroupStatusEnum.FACT, AlchemyGroup.unit_id == self.unit.id)
            .options(load_only('id', 'work_type_id', 'is_family', 'type_id', 'is_care'))
            .subquery()
        )
        return fact_group_this_unit

    def _get_groups(self):
        """
        :return:
        """

        fact_groups_this_unit = (
            self.session.query(AlchemyGroup)
            .filter(AlchemyGroup.status == GroupStatusEnum.FACT, AlchemyGroup.unit_id == self.unit.id)
            .options(
                load_only(
                    'id',
                    'room_id',
                    'work_type_id',
                    'is_family',
                    'type_id',
                    'is_care',
                    'is_young_children',
                    'health_need_id',
                )
            )
            .subquery('fact_groups')
        )

        plan_groups_this_unit = (
            self.session.query(AlchemyGroup)
            .filter(AlchemyGroup.status == GroupStatusEnum.PLAN, AlchemyGroup.unit_id == self.unit.id)
            .options(
                load_only(
                    'id',
                    'room_id',
                    'work_type_id',
                    'is_family',
                    'type_id',
                    'is_care',
                    'is_young_children',
                    'health_need_id',
                )
            )
            .subquery('plan_groups')
        )

        group_this_unit = (
            self.session.query(
                fact_groups_this_unit.c.id.label('fact_group_id'),
                fact_groups_this_unit.c.room_id.label('fact_group_room_id'),
                fact_groups_this_unit.c.work_type_id.label('fact_group_work_type_id'),
                fact_groups_this_unit.c.is_family.label('fact_group_is_family'),
                fact_groups_this_unit.c.type_id.label('fact_group_type_id'),
                fact_groups_this_unit.c.is_care.label('fact_group_is_care'),
                fact_groups_this_unit.c.is_young_children.label('fact_group_is_young_children'),
                fact_groups_this_unit.c.health_need_id.label('fact_group_health_need_id'),
                plan_groups_this_unit.c.id.label('plan_group_id'),
                plan_groups_this_unit.c.room_id.label('plan_group_room_id'),
                plan_groups_this_unit.c.work_type_id.label('plan_group_work_type_id'),
                plan_groups_this_unit.c.is_family.label('plan_group_is_family'),
                plan_groups_this_unit.c.type_id.label('plan_group_type_id'),
                plan_groups_this_unit.c.is_care.label('plan_group_is_care'),
                plan_groups_this_unit.c.is_young_children.label('plan_group_is_young_children'),
                plan_groups_this_unit.c.health_need_id.label('plan_group_health_need_id'),
            ).outerjoin(
                plan_groups_this_unit,
                and_(
                    plan_groups_this_unit.c.room_id == fact_groups_this_unit.c.room_id,
                    plan_groups_this_unit.c.room_id is not None,
                ),
            )
        ).subquery()

        return group_this_unit

    def _kids(self, **kwargs):
        """
        Дети с датой рождения из age_range
        """

        # age_range = ALL
        # age_on_date = kwargs.get('on_date', AgeDeltas.calculate_date)
        # down, up = AgeDeltas.get_category_deltas(age_range, age_on_date)
        kids = (
            self.session.query(
                AlchemyChildren.id.label('children_id'),
                AlchemyChildren.date_of_birth,
                AlchemyChildren.is_invalid,
                AlchemyChildren.health_need_id,
            )
            # ).filter(
            #     AlchemyChildren.date_of_birth > down,
            #     AlchemyChildren.date_of_birth <= up)
            .subquery('kids')
        )
        return kids

    def get_result_set(self):
        """Отбрасываем временно отчисленных детей"""

        return (
            self.session.query(AlchemyPupil)
            .filter(AlchemyPupil.temporary_deduct == False)
            .options(load_only('id', 'children_id', 'grup_id'))
            .subquery()
        )


class BaseQueueAlgorithm(with_metaclass(ABCMeta, BaseAlgorithm)):
    """
    Базовый алгоритм для вычисления показателей по очереди
    """

    def __init__(self, cache, **kwargs):
        super(BaseQueueAlgorithm, self).__init__(session=None, **kwargs)

        self._cache = cache

    def _get_base_queue(self, age_range, on_date):
        result = []
        if self.unit.id in self._cache:
            result = self._cache[self.unit.id][on_date][age_range]

        return result

    def get_result_set(self, **kwargs):
        age_range = kwargs.get('age_range', ALL)
        on_date = kwargs.get('on_date', 'ON_NEW_YEAR')
        return self._get_base_queue(age_range, on_date)


class BaseQueueAlgorithmWithOutWantChangeDou(BaseQueueAlgorithm):
    """
    Базовый алгоритм без учета Желающих сменить ДОУ
    """

    def get_result_set(self, **kwargs):
        result = super(BaseQueueAlgorithmWithOutWantChangeDou, self).get_result_set(**kwargs)

        return [x for x in result if x['status__code'] != DSS.WANT_CHANGE_DOU]


class BaseQueueWithDesiredDateInPeriodAlgorithm(
    with_metaclass(ABCMeta, type('NewBase', (BaseQueueAlgorithm, DateMixin), {}))
):
    def get_result_set(self, **kwargs):
        result_set = super(BaseQueueWithDesiredDateInPeriodAlgorithm, self).get_result_set(**kwargs)

        down, up = self.get_desired_period()
        return [x for x in result_set if x['desired_date'] and (down <= x['desired_date'] <= up)]


class BaseActualCallAlgorithm(
    with_metaclass(ABCMeta, type('NewBase', (BaseQueueAlgorithmWithOutWantChangeDou, DateMixin), {}))
):
    """
    Базовый алгоритм для вычисления актуального спроса
    """

    def get_result_set(self, **kwargs):
        qs = super(BaseActualCallAlgorithm, self).get_result_set(**kwargs)
        return [x for x in qs if not x['desired_date'] or x['desired_date'] <= self.get_desired_date()]


class BaseDeferredQueueAlgorithm(
    with_metaclass(ABCMeta, type('NewBase', (BaseQueueAlgorithmWithOutWantChangeDou, DateMixin), {}))
):
    """
    Базовый алгоритм для вычисления отложенного спроса
    """

    def get_result_set(self, **kwargs):
        qs = super(BaseDeferredQueueAlgorithm, self).get_result_set(**kwargs)
        return [x for x in qs if x['desired_date'] and x['desired_date'] > self.get_desired_date()]


class BaseHealthNeedAlgorithm(with_metaclass(ABCMeta, type('NewBase', (BaseQueueAlgorithm, DateMixin), {}))):
    @abstractmethod
    def _get_heath_needs(self):
        """
        Возвращает ID конкретной потребности по здоровью.
        """

    def get_result_set(self, **kwargs):
        qs = super(BaseHealthNeedAlgorithm, self).get_result_set(**kwargs)

        hn_pks = self._get_heath_needs()

        return [
            rec
            for rec in qs
            if (not rec['desired_date'] or rec['desired_date'] <= self.get_desired_date())
            and rec['children__health_need_id'] in hn_pks
            and rec['status__code'] in [DSS.REGISTERED, DSS.PRIV_CONFIRMATING]
            and rec['children__date_of_birth'] < self.get_current_calendar_year_start()
        ]
