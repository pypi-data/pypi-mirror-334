from __future__ import (
    annotations,
)

import abc
import datetime
from dataclasses import (
    dataclass,
)
from typing import (
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
)

from django.utils.functional import (
    cached_property,
)

from kinder.core.children.models import (
    Children,
)
from kinder.core.declaration.enum import (
    DeclPortalEnum,
)
from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.declaration_status.models import (
    DSS,
)
from kinder.core.direct.models import (
    DRS,
)
from kinder.core.group.models import (
    GroupStatusEnum,
)

from gisdo.counter.age import (
    get_age_full_label,
    get_age_half_label,
)
from gisdo.counter.constants import (
    DRS_NEW_CONFIRM,
)
from gisdo.utils import (
    DateMixin,
)


class DirectData(NamedTuple):
    """
    Данные направления
    """

    status: str  # Статус направления
    group_status: str  # Статус группы направления


@dataclass
class ChildExtra:
    """
    Дополнительные данные для ребёнка
    """

    # Есть зачисления в план/факт, если в план то дата
    # зачисления либо отсутствует либо меньше или равна даты отчёта
    # учитываются временно отчисленные
    with_pupil_check_plan: bool
    # Есть зачисления в план/факт
    # учитываются временно отчисленные
    with_pupil: bool
    # Есть зачисления в факт
    # не учитываются временно отчисленные
    with_fact_pupil: bool
    # Зачисления в плановые группы с датой зачисления по приказу
    # большей контрольной даты, которые считаются как направления
    # в статусе "Заключение договора".
    plan_pupil_directions: bool


@dataclass
class DeclExtra:
    """
    Дополнительные данные для заявки
    """

    directs: list[DirectData]  # Данные по связанным с заявкой направлениям


class ExtraDataBase(metaclass=abc.ABCMeta):
    """
    Дополнительные данные из других связанных таблиц
    """

    @cached_property
    def report_day(self) -> datetime.date:
        """
        Дата отчёта (сегодня)
        """
        return datetime.date.today()

    @cached_property
    def last_day_next(self) -> datetime.date:
        """
        Следующее 1.09
        """
        return DateMixin.get_next_calendar_year_start()

    @cached_property
    def pre_last_day_next(self) -> datetime.date:
        """
        День перед следующим 1.09
        """
        return datetime.date(self.last_day_next.year, 8, 31)

    @cached_property
    def last_day_current(self) -> datetime.date:
        """
        Последнее 1.09
        """
        return DateMixin.get_current_calendar_year_start()

    @cached_property
    def current_learn_year(self) -> Tuple[datetime.date, datetime.date]:
        """
        Текущий учебный год

        2.09.Y-31.08.(Y+1)
        где Y - год начала учебного года
        """
        return DateMixin.get_current_learn_year()

    @cached_property
    def pre_current_learn_year(self) -> datetime.date:
        """
        День перед началом текущего учебного года
        """
        date_begin, _ = self.current_learn_year
        return datetime.date(date_begin.year, 9, 1)

    @cached_property
    def current_september(self) -> datetime.date:
        """
        1.09 текущего года
        """
        return DateMixin.get_current_calendar_year()

    @cached_property
    def first_day_of_the_year(self) -> datetime.date:
        """
        1.01.Y
        где Y текущий год
        """
        return datetime.date(datetime.date.today().year, 1, 1)

    @abc.abstractmethod
    def get_decl_extra(self, decl_id: int) -> DeclExtra:
        """
        Получить дополнительные данные для заявки
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_child_extra(self, child_id: int) -> ChildExtra:
        """
        Получить дополнительные данные для ребёнка
        """
        raise NotImplementedError


class DeclarationRow(NamedTuple):
    """
    Строка итератора по заявкам
    """

    id: int  # ID
    date: datetime.datetime  # Дата создания заявки
    desired_date: datetime.date  # Дата желаемого зачисления
    status: str  # Статус заявки
    work_type: Optional[str]  # Время пребывания
    defer_demand: bool  # Отложенное зачисление
    is_portal: bool  # Подано с портала
    best_privilege_type: Optional[int]  # Лучшая льгота
    direct_statuses: Set[str]  # Статусы направлений связанных с заявкой

    # Результаты выполнения некоторых часто используемых функций

    # queue_with_want_change_dou с direct_statuses=DRS.directs_total()
    queue_with_want_change_dou: bool
    # queue_with_direct c direct_statuses=DRS.directs_total()
    queue_with_direct: bool
    # queue_with_direct c direct_statuses={}
    queue_with_direct_any: bool
    # queue_with_direct c direct_statuses={DRS.NEW, DRS.CONFIRM}
    queue_with_direct_new: bool
    # queue_register_with_direct
    queue_register_with_direct: bool

    @classmethod
    def from_declaration(
        cls, decl: Declaration, child: Children, child_extra: ChildExtra, extra: ExtraDataBase
    ) -> 'DeclarationRow':
        """
        Получить строку из заявки

        :param decl: Заявка
        :param cache: Кешированные данные
        """
        decl_extra = extra.get_decl_extra(decl.id)

        direct_statuses = set(d.status for d in decl_extra.directs if d.group_status != GroupStatusEnum.ARCHIVE)

        decl_status = decl.status.code

        return cls(
            id=decl.id,
            date=decl.date.date(),
            desired_date=decl.desired_date,
            status=decl_status,
            work_type=decl.work_type and decl.work_type.code,
            defer_demand=decl.defer_demand,
            is_portal=(decl.portal == DeclPortalEnum.PORTAL),
            best_privilege_type=decl.best_privilege and decl.best_privilege.type_id,
            direct_statuses=direct_statuses,
            queue_with_want_change_dou=queue_with_want_change_dou(
                decl_status, direct_statuses, child_extra.plan_pupil_directions, set(DRS.directs_total())
            ),
            queue_with_direct=queue_with_direct(decl_status, direct_statuses, set(DRS.directs_total())),
            queue_with_direct_any=queue_with_direct(decl.status.code, direct_statuses, set()),
            queue_with_direct_new=queue_with_direct(decl_status, direct_statuses, DRS_NEW_CONFIRM),
            queue_register_with_direct=queue_register_with_direct(
                decl_status,
                direct_statuses,
            ),
        )


class ChildrenRow(NamedTuple):
    """
    Строка итератора по детям
    """

    id: int  # ID
    extra: ExtraDataBase  # Дополнительные данные общие
    child_extra: ChildExtra  # Дополнительные данные ребёнка
    date_of_birth: datetime.date  # Дата рождения
    is_invalid: bool  # Является ли инвалидом
    declarations: List[DeclarationRow]  # Список заявок связанных с ребёнком
    health_need: Optional[str]  # ОВЗ
    health_need_group_type: Optional[str]  # Тип группы ОВЗ

    # Возрастные категории в разных разрезах
    age_full: str
    age_full_sep: str
    age_full_next_sep: str
    age_half: str

    @classmethod
    def from_child(cls, child: Children, decls: Iterator[Declaration], extra: ExtraDataBase) -> 'ChildrenRow':
        """
        Получить строку из записи ребёнка

        :param child: Ребёнок
        :param decls: Заявки
        :param cache: Кешированные данные
        """
        child_extra = extra.get_child_extra(child.id)
        declarations: List[DeclarationRow] = []

        for decl in decls:
            declarations.append(DeclarationRow.from_declaration(decl, child, child_extra, extra))

        return cls(
            id=child.id,
            extra=extra,
            child_extra=child_extra,
            date_of_birth=child.date_of_birth,
            is_invalid=child.is_invalid,
            declarations=declarations,
            health_need=(child.health_need and child.health_need.code),
            health_need_group_type=(
                child.health_need and child.health_need.group_type and child.health_need.group_type.code
            ),
            age_full=get_age_full_label(child.date_of_birth, extra.report_day),
            age_full_sep=get_age_full_label(child.date_of_birth, extra.current_september),
            age_full_next_sep=get_age_full_label(child.date_of_birth, extra.last_day_next),
            age_half=get_age_half_label(child.date_of_birth, extra.report_day),
        )


def queue_with_want_change_dou(
    decl_status: str, decl_direct_statuses: Set[str], plan_pupil_directions: bool, direct_statuses: Set[str]
) -> bool:
    """
    Заявление в статусах:
        "Зарегистрировано", "Подтверждение льгот", "Желает изменить ДОУ"
    Заявления в других статусах со связанными направлениями в факт/план группы
    в статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой"
    Зачисления в плановые группы с датой зачисления по приказу
    большей контрольной даты, которые считаются как направления
    в статусе "Заключение договора".
    """
    if DRS.DOGOVOR in direct_statuses and plan_pupil_directions:
        return True

    queue_status = decl_status in DSS.status_queue()
    if queue_status:
        return True

    has_direct = decl_direct_statuses & direct_statuses
    if has_direct:
        return True

    return False


def queue_with_direct(decl_status: str, decl_direct_statuses: Set[str], direct_statuses: Set[str]) -> bool:
    """
    Заявления в статусах "Зарегистрировано" или "Подтверждение льгот".
    или
    Заявления в других статусах со связанными направлениями в факт/план группы
    в указанных статусах (если множество пустое - в любом статусе)
    """
    dcl_status_check = decl_status in {DSS.REGISTERED, DSS.PRIV_CONFIRMATING}
    if not direct_statuses:
        drct_status_check = decl_direct_statuses
    else:
        drct_status_check = decl_direct_statuses & direct_statuses

    return dcl_status_check or drct_status_check


def queue_register_with_direct(
    decl_status: str,
    decl_direct_statuses: Set[str],
) -> bool:
    """
    Заявления в статусе "Зарегистрировано".
    Заявления в других статусах со связанными направлениями в факт/план группы
    в статусах:
        "Подтверждено", "Предложено системой".
    """
    decl_status = decl_status == DSS.REGISTERED
    drct_status = decl_direct_statuses & {DRS.CONFIRM, DRS.NEW}

    return decl_status or drct_status
