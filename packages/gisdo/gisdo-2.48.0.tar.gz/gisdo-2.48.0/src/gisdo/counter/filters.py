from typing import (
    Optional,
)

from django.conf import (
    settings,
)

from kinder.core.declaration_status.models import (
    DSS,
)
from kinder.core.dict.models import (
    GroupTypeEnumerate,
    PrivilegeType,
    WorkTypeEnumerate,
)
from kinder.core.direct.models import (
    DRS,
)

from gisdo.counter.constants import (
    DRS_REGISTER_DOGOVOR,
    PRIV_TYPE_MUN_REG,
)
from gisdo.counter.declaration import (
    ChildrenRow,
)


def get_decl_count(
    child: ChildrenRow,
    is_portal: Optional[bool] = None,
    work_type: Optional[str] = None,
) -> int:
    """
    Число заявок во всех статусах, кроме "Учет детей, не посещающих ДОО"
    Дата подачи >= 01.01.<текущий год>

    + доп фильтры
    """
    n = 0
    date_border = child.extra.first_day_of_the_year
    for decl in child.declarations:
        use = decl.status != DSS.NOT_ATTENDED and decl.date >= date_border
        if settings.PARTNER_QUIRKS != 'TUMEN':
            use = use and not decl.defer_demand

        if is_portal is not None:
            use = use and (decl.is_portal == is_portal)

        if work_type is not None:
            use = use and (decl.work_type == work_type)

        if use:
            n += 1

    return n


# Фильтры для показателей


def filter_1(child: ChildrenRow) -> int:
    """
    Показатель 1 и 1.1

    Все заявки во всех статусах, кроме "Учет детей, не посещающих ДОО"
    Дата подачи >= 01.01.<текущий год>

    Возвращает число т.к. на 1 ребёнка может быть несколько заявок
    """
    return get_decl_count(child)


def filter_2(child: ChildrenRow) -> int:
    """
    Показатель 2

    Показатель 1 и заявка с портала

    Возвращает число т.к. на 1 ребёнка может быть несколько заявок
    """
    return get_decl_count(child, is_portal=True)


def filter_3(child: ChildrenRow) -> int:
    """
    Показатель 3

    Показатель 1 и заявка не с портала

    Возвращает число т.к. на 1 ребёнка может быть несколько заявок
    """
    return get_decl_count(child, is_portal=False)


def filter_4(child: ChildrenRow) -> bool:
    """
    Показатель 4

    см. queue_with_want_change_dou и
    Дата подачи заявления = текущий учебный год.
    Желаемая дата зачисления <= конца текущего учебного года.
    Исключаем заявки, у ребенка которого имеется зачисление
    в фактическую группу (не учитываем временно отчисленных)
    """
    _, date_end = child.extra.current_learn_year

    if child.child_extra.with_fact_pupil:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_want_change_dou
            and child.extra.pre_current_learn_year <= decl.date <= date_end
            and decl.desired_date
            and decl.desired_date <= (child.extra.pre_last_day_next)
            and not decl.defer_demand
        ):
            return True

    return False


def filter_4_1(child: ChildrenRow) -> bool:
    """
    Показатель 4.1

    Показатель 4 и
    Тип группы "ОВЗ" у ребенка = "Компенсирующий"
    "ОВЗ" у ребенка не пусто и не равно "Нет".
    """
    if child.health_need_group_type != GroupTypeEnumerate.COMP:
        return False

    return filter_4(child)


def filter_4_2(child: ChildrenRow) -> bool:
    """
    Показатель 4.2

    Показатель 4 и
    Тип группы "ОВЗ" у ребенка = "Оздоровительный"
    """
    if child.health_need_group_type != GroupTypeEnumerate.HEALTH:
        return False

    return filter_4(child)


def filter_5(child: ChildrenRow) -> bool:
    """
    Показатель 5

    Заявления в статусе "Желает изменить ДОУ"
    Заявления в статусе "Подтверждение льгот" или заявления в других статусах
    у которых есть привязанные направления в факт/план группы в статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой"
    у детей которых есть зачисление
    Дата подачи заявления = [01.09.2014; 31.08.2015] или текущий учебный год.
    Желаемая дата зачисления <= 31.08.2015 или текущий учебный год.
    """
    _, date_end = child.extra.current_learn_year

    for decl in child.declarations:
        status = decl.status == DSS.WANT_CHANGE_DOU
        if not status and child.child_extra.with_pupil_check_plan:
            status = (decl.status == DSS.PRIV_CONFIRMATING) or (decl.direct_statuses & set(DRS.directs_total()))

        if (
            status
            and child.extra.pre_current_learn_year <= decl.date <= date_end
            and decl.desired_date
            and decl.desired_date <= (child.extra.pre_last_day_next)
            and not decl.defer_demand
        ):
            return True

    return False


def filter_6(child: ChildrenRow) -> int:
    """
    Показатель 6

    Показатель 1 и заявка с временем пребывания "Кратковременный"

    Возвращает число т.к. на 1 ребёнка может быть несколько заявок
    """
    return get_decl_count(child, work_type=WorkTypeEnumerate.SHORT)


def filter_7(child: ChildrenRow) -> bool:
    """
    Показатель 7

    см. queue_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления >= 02.09.2015
    или
    Установлен чекбокс "Отложенный спрос"
    """
    d = child.extra.last_day_current
    child_birth_after = child.date_of_birth >= d

    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and (
                (decl.desired_date and decl.desired_date > d)
                or (decl.desired_date is None and child_birth_after)
                or decl.defer_demand
            )
        ):
            return True

    return False


def filter_7_2(child: ChildrenRow) -> bool:
    """
    Показатель 7.2

    см. queue_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления текущий учебный год
    Не отложенный спрос
    """
    date_start, date_end = (child.extra.last_day_current, child.extra.last_day_next)
    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and decl.desired_date
            and date_start < decl.desired_date < date_end
            and not decl.defer_demand
        ):
            return True

    return False


def filter_7_3(child: ChildrenRow) -> bool:
    """
    Показатель 7.3

    см. queue_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление

    Дата желаемого зачисления след учебный год
    """
    d = child.extra.last_day_next
    if child.child_extra.with_pupil:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and ((decl.desired_date and decl.desired_date > d) or decl.defer_demand)
        ):
            return True

    return False


def filter_7_4(child: ChildrenRow) -> bool:
    """
    Показатель 7.4

    см. queue_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления текущий учебный год
    Не отложенный спрос
    """
    date_start, date_end = (child.extra.last_day_current, child.extra.last_day_next)
    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_direct_any
            and decl.status != DSS.WANT_CHANGE_DOU
            and date_start < decl.desired_date < date_end
            and not decl.defer_demand
        ):
            return True

    return False


def filter_7_5(child: ChildrenRow) -> bool:
    """
    Показатель 7.5

    см. queue_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления <= 1/09/Следующий учебный год или не указана
    Не отложенный спрос
    """
    d = child.extra.last_day_next
    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_with_direct_new
            and decl.status != DSS.WANT_CHANGE_DOU
            and (decl.desired_date is None or decl.desired_date <= d or decl.defer_demand)
        ):
            return True

    return False


def filter_7_7(child: ChildrenRow) -> bool:
    """
    Показатель 7.7

    Заявления в других статусах, у которых есть привязанные направления в
    статусах: "Заключение договора", "Направлен в ДОО"
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления <= 1/09/Следующий учебный год или не указана
    Не отложенный спрос
    """
    d = child.extra.last_day_next
    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.direct_statuses & DRS_REGISTER_DOGOVOR
            and decl.status != DSS.WANT_CHANGE_DOU
            and (decl.desired_date is None or decl.desired_date <= d or decl.defer_demand)
        ):
            return True

    return False


def filter_9(child: ChildrenRow) -> bool:
    """
    Показатель 9

    см. queue_register_with_direct
    Исключены заявления в статусе "Желает изменить ДОО"
    Исключены заявления детей у которых есть зачисление
    Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана
    Ребенку еще нет одного года
    """
    d = child.extra.last_day_current

    if child.date_of_birth >= d:
        return False

    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_register_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and (decl.desired_date is None or decl.desired_date <= d)
            and not decl.defer_demand
        ):
            return True

    return False


def filter_10(child: ChildrenRow) -> bool:
    """
    Показатель 10

    Показатель 9
    Тип лучшей привелегии заявления - FED (1)
    """
    d = child.extra.last_day_current

    if child.date_of_birth >= d:
        return False

    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_register_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and decl.best_privilege_type == PrivilegeType.FED
            and (decl.desired_date is None or decl.desired_date <= d)
            and not decl.defer_demand
        ):
            return True

    return False


def filter_10_1(child: ChildrenRow) -> bool:
    """
    Показатель 10.1

    Показатель 10
    У ребёнка должна быть проставлена галочка наличия инвалидности
    """
    d = child.extra.last_day_current

    if not child.is_invalid:
        return False

    if child.date_of_birth >= d:
        return False

    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_register_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and decl.best_privilege_type == PrivilegeType.FED
            and (decl.desired_date is None or decl.desired_date <= d)
            and not decl.defer_demand
        ):
            return True

    return False


def filter_11(child: ChildrenRow) -> bool:
    """
    Показатель 11

    Показатель 9
    Тип лучшей привелегии заявления - MUN (2) или REG (3)
    """
    d = child.extra.last_day_current

    if child.date_of_birth >= d:
        return False

    if child.child_extra.with_pupil_check_plan:
        return False

    for decl in child.declarations:
        if (
            decl.queue_register_with_direct
            and decl.status != DSS.WANT_CHANGE_DOU
            and decl.best_privilege_type in PRIV_TYPE_MUN_REG
            and (decl.desired_date is None or decl.desired_date <= d)
            and not decl.defer_demand
        ):
            return True

    return False
