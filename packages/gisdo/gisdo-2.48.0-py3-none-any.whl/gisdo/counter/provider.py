from __future__ import (
    annotations,
)

import datetime
from collections import (
    defaultdict,
)
from itertools import (
    groupby,
)
from operator import (
    attrgetter,
)
from typing import (
    Iterator,
)

from django.db.models.query import (
    QuerySet,
)
from django.utils.functional import (
    cached_property,
)

from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.dict.models import (
    UnitKind,
)
from kinder.core.direct.models import (
    Direct,
)
from kinder.core.group.models import (
    GroupStatusEnum,
    Pupil,
)
from kinder.core.unit.models import (
    Unit,
)

from gisdo.counter.declaration import (
    ChildExtra,
    ChildrenRow,
    DeclExtra,
    DirectData,
    ExtraDataBase,
)


class ExtraData(ExtraDataBase):
    """
    Дополнительные данные из других связанных таблиц
    """

    def __init__(self) -> None:
        self._decl_extra = defaultdict(lambda: DeclExtra([]))
        self._child_extra = defaultdict(
            lambda: ChildExtra(
                False,
                False,
                False,
                False,
            )
        )

    def add_direct(self, decl_id: int, direct_status: str, direct_group_status: str) -> None:
        """
        Добавить направление связанное с заявкой
        """
        data = self._decl_extra[decl_id]
        data.directs.append(DirectData(direct_status, direct_group_status))

    def update_child_pupil(
        self,
        child_id: int,
        with_pupil_check_plan: bool,
        with_pupil: bool,
        with_fact_pupil: bool,
        plan_pupil_directions: bool,
    ) -> None:
        """
        Обновить флаги для зачисления ребёнка
        """
        data = self._child_extra[child_id]

        # Флаг должен быть true если есть хотя бы одно зачисление подходящее под условие
        data.with_pupil_check_plan = data.with_pupil_check_plan or with_pupil_check_plan
        data.with_pupil = data.with_pupil or with_pupil
        data.with_fact_pupil = data.with_fact_pupil or with_fact_pupil
        data.plan_pupil_directions = data.plan_pupil_directions or plan_pupil_directions

    def get_decl_extra(self, decl_id: int) -> DeclExtra:
        return self._decl_extra[decl_id]

    def get_child_extra(self, child_id: int) -> ChildExtra:
        return self._child_extra[child_id]


class DataProvider:
    """
    Поставщик данных для подсчёта значение показателей
    """

    select_related = [
        'status',
        'work_type',
        'children',
        'best_privilege',
        'children__health_need',
        'children__health_need__group_type',
    ]

    def __init__(self, unit: Unit) -> None:
        self._unit = unit
        self._extra = ExtraData()
        self._collect_extra()

    @property
    def extra(self) -> ExtraData:
        return self._extra

    @cached_property
    def report_datetime(self) -> datetime.datetime:
        """
        Дата-время отчёта, для сравнения с datetime
        """
        return datetime.datetime.combine(datetime.datetime.now(), datetime.datetime.max.time())

    @cached_property
    def report_date(self) -> datetime.date:
        """
        Дата отчёта
        """
        return datetime.date.today()

    def get_decl_query(self) -> QuerySet:
        """
        Получение заявок для отчёта
        """
        return Declaration.objects.filter(
            declarationunit__unit_id=self._unit.id,
            declarationunit__ord=1,
            declarationunit__unit__kind_id=UnitKind.DOU,
            date__lte=self.report_datetime,
        )

    def _collect_pupils(self) -> None:
        """
        Сбор доп. данных из таблицы зачислений
        """
        for pupil in (
            Pupil.objects.filter(children__in=self.get_decl_query().values_list('children', flat=True))
            .select_related(
                'grup',
            )
            .iterator()
        ):
            with_pupil_check_plan = pupil.grup.status == GroupStatusEnum.FACT or (
                pupil.grup.status == GroupStatusEnum.PLAN
                and (pupil.date_in_order is None or pupil.date_in_order <= self.report_date)
            )

            with_pupil = pupil.grup.status == GroupStatusEnum.FACT or pupil.grup.status == GroupStatusEnum.PLAN

            with_fact_pupil = pupil.grup.status == GroupStatusEnum.FACT and not pupil.temporary_deduct

            plan_pupil_directions = (
                pupil.grup.status == GroupStatusEnum.PLAN
                and pupil.date_in_order
                and pupil.date_in_order > self.report_date
            )

            self.extra.update_child_pupil(
                pupil.children_id, with_pupil_check_plan, with_pupil, with_fact_pupil, plan_pupil_directions
            )

    def _collect_directs(self) -> None:
        """
        Сбор доп. данных из таблицы направлений
        """
        for decl_id, status, group_status in (
            Direct.objects.filter(declaration__in=self.get_decl_query())
            .values_list('declaration_id', 'status__code', 'group__status')
            .iterator()
        ):
            self.extra.add_direct(decl_id, status, group_status)

    def _collect_extra(self) -> None:
        """
        Сбор дополнительных данных из других таблиц
        """
        self._collect_pupils()
        self._collect_directs()

    def get_rows(self) -> Iterator[ChildrenRow]:
        """
        Получение строк с данными по детям
        """
        for child, decls in groupby(
            self.get_decl_query().select_related(*self.select_related).order_by('children_id').iterator(),
            key=attrgetter('children'),
        ):
            yield ChildrenRow.from_child(child, decls, self.extra)
