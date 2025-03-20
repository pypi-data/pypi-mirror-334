import datetime

from django.conf import (
    settings,
)
from django.db.models import (
    F,
    Q,
)
from future.builtins import (
    range,
)

from m3.plugins import (
    ExtensionManager,
)

from kinder.core.children.models import (
    Children,
)
from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.declaration_status.models import (
    DSS,
)
from kinder.core.dict.models import (
    HNE,
    GroupTypeEnumerate,
    HealthNeed,
    PrivilegeType,
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

from gisdo.algorithm.constants import (
    get_all_day_work_types,
    get_short_day_types,
)
from gisdo.constants import (
    GOVERNMENT_TYPES,
)
from gisdo.utils import (
    DateMixin,
    get_report_date_or_today,
)


SICK_CODES = (
    HealthNeed.NO,
    HNE.SICK,
    HNE.PHTHISIS,
    HNE.OTHER,
    HNE.ALLERGOPATHOLOGY,
    HNE.DIABETES,
    HNE.RESPIRATORY,
    HNE.RESPIRATORY,
    HNE.CARDIOVASCULAR,
    HNE.NEPHRO_UROL,
    HNE.CELIAC,
)

# Фактический и плановый статусы групп.
FACT_PLAN_GS = (GroupStatusEnum.FACT, GroupStatusEnum.PLAN)

# Статусы направлений "До зачисления":
# Подтверждено, Заключение договора, Направлен в ДОУ, Предложено системой.
BEFORE_ENROLL_DRS = (DRS.CONFIRM, DRS.DOGOVOR, DRS.REGISTER, DRS.NEW)


def get_1_filter(context):
    """Фильтр для показателя 1

    - Все заявления, кроме заявлений в статусах:
        "Учет детей, не посещающих ДОО".
    - Дата подачи >= 01.01 текущего года.

    - В заявления учитываем только первый приоритетный ДОУ.
    - Не разбивать по возрастам.
    - Показатель считается по всем видам ДОУ.

    :return: Q
    """

    date_border = datetime.date.today()

    base_1_filter = ~Q(status__code=DSS.NOT_ATTENDED) & Q(date__gte=datetime.date(date_border.year, 1, 1))

    # Для Тюмени не выполняет фильтрацию по чек-боксу "Отложенный запрос".
    if settings.PARTNER_QUIRKS != 'TUMEN':
        base_1_filter &= Q(defer_demand=False)

    return base_1_filter


def get_4_filter(context):
    """Фильтр показателя 4

    - Все заявления в статусах:
        "Зарегистрировано", "Подтверждение льгот", "Желает изменить ДОУ"
    - Заявления в других статусах, у которых есть привязанные направления в
        факт/план группы в статусах:
            "Заключение договора", "Подтверждено", "Направлен в ДОУ",
            "Предложено системой".
    - Дата подачи заявления = [01.09.2014; 31.08.2015] или текущий учебный год.
    - Желаемая дата зачисления <= 31.08.2015 или текущий учебный год.

    - В заявках учитываем только первый приоритетный ДОУ.
    - Дата расчета возраста = текущая дата.
    - Показатель считается по всем видам ДОУ.
    - Разбивка по возрастам - 16 категорий.
    - Исключаем заявки, у ребенка которого имеется зачисление
        в фактическую группу (не учитываем временно отчисленных)

    :return: Q
    """

    d = DateMixin.get_next_calendar_year_start()
    date_begin, date_end = DateMixin.get_current_learn_year()

    return (
        queue_with_want_change_dou(context)
        & Q(
            date__gte=datetime.date(date_begin.year, 9, 1),
            date__lte=date_end,
        )
        & Q(desired_date__lte=datetime.date(d.year, 8, 31))
        & Q(defer_demand=False)
        & ~with_fact_pupil()
    )


def get_41_filter(context):
    """Фильтр для показателя 4.1

    - Все заявления в статусах:
        "Зарегистрировано", "Подтверждение льгот", "Желает изменить ДОУ"
    - Заявления в других статусах, у которых есть привязанные направления
    в факт/план группы статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой".
    - Тип группы "ОВЗ" у ребенка = "Компенсирующий".
    - "ОВЗ" у ребенка не пусто и не равно "Нет".
    - Дата подачи заявления = [01.09.2014; 31.08.2015] или текущий учебный год.
    - Желаемая дата зачисления <= 31.08.2015 или текущий учебный год.

    - Учитывать первый приоритетный ДОУ.
    - Показатель считается по всем видам ДОУ.
    - Дата расчета возраста = текущая дата.
    - Разбивка по возрастам - 16 категорий.
    - Исключаем заявки, у ребенка которого имеется зачисление
        в фактическую группу (не учитываем временно отчисленных)

    :return: Q
    """

    d = DateMixin.get_next_calendar_year_start()
    date_begin, date_end = DateMixin.get_current_learn_year()

    return (
        queue_with_want_change_dou(context)
        & Q(children__health_need__group_type__code=GroupTypeEnumerate.COMP)
        & with_health_need_filter()
        & Q(
            date__gte=datetime.date(date_begin.year, 9, 1),
            date__lte=date_end,
        )
        & Q(desired_date__lte=datetime.date(d.year, 8, 31))
        & Q(defer_demand=False)
        & ~with_fact_pupil()
    )


def get_42_filter(context):
    """Фильтр для показателя 4.2

    - Все заявления в статусах:
        "Зарегистрировано", "Подтверждение льгот", "Желает изменить ДОУ"
    - Заявления в других статусах, у которых есть привязанные направления
    в в факт/план группы статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой".
    - Желаемая дата зачисления <= 31.08.2015 или текущий учебный год.
    - Тип группы "ОВЗ" у ребенка = "Оздоровительный".
    - Дата подачи заявления = [01.09.2014; 31.08.2015] или текущий учебный год.

    - Показатель считается по всем видам ДОУ.
    - Дата расчета возраста = текущая дата.
    - Разбивка по возрастам с периодичностью в полгода - 16 категорий.
    - Исключаем заявки, у ребенка которого имеется зачисление
        в фактическую группу (не учитываем временно отчисленных)

    :return: Q
    """

    date_border = DateMixin.get_next_calendar_year_start()
    date_begin, date_end = DateMixin.get_current_learn_year()

    return (
        queue_with_want_change_dou(context)
        & Q(desired_date__lte=datetime.date(date_border.year, 8, 31))
        & Q(children__health_need__group_type__code=GroupTypeEnumerate.HEALTH)
        & Q(
            date__gte=datetime.date(date_begin.year, 9, 1),
            date__lte=date_end,
        )
        & Q(defer_demand=False)
        & ~with_fact_pupil()
    )


def get_5_filter(context):
    """ "Фильтр для показателя 5

    - Все заявления в статусе "Желает изменить ДОУ"
    - Заявления в статусе "Подтверждение льгот" или заявления в других статусах
    у которых есть привязанные направления в факт/план группы в статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой"
    у детей которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата подачи заявления = [01.09.2014; 31.08.2015] или текущий учебный год.
    - Желаемая дата зачисления <= 31.08.2015 или текущий учебный год.

    - Показатель считается по всем видам ДОУ.
    - Расчет возраста на текущую дату.
    - По первому приоритетному ДОУ.
    - Разбивка по возрастной категории - 16.

    :return: Q
    """

    d = DateMixin.get_next_calendar_year_start()
    date_begin, date_end = DateMixin.get_current_learn_year()

    return Q(
        Q(
            Q(status__code=DSS.WANT_CHANGE_DOU)
            | Q(
                with_pupil(context)
                & Q(
                    Q(status__code=DSS.PRIV_CONFIRMATING)
                    | Q(
                        direct__status__code__in=BEFORE_ENROLL_DRS,
                        direct__group__status__in=FACT_PLAN_GS,
                    )
                )
            )
        )
        & Q(
            date__gte=datetime.date(date_begin.year, 9, 1),
            date__lte=datetime.date(date_end.year, 8, 31),
        )
        & Q(desired_date__lte=datetime.date(d.year, 8, 31))
        & Q(defer_demand=False)
    )


def get_7_filter(context):
    """Фильтр для показателя 7

    - Заявления в статусах "Зарегистрировано" и "Подтверждение льгот".
    - Заявления в других статусах, у которых есть привязанные
        направления в статусах в факт/план группы в статусах:
            "Заключение договора", "Подтверждено",
            "Направлен в ДОУ", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления текущий учебный год - >= 02.09.2015
      (т.е. все заявки позже этой даты (включительно)).
    - Дата расчета возраста: на 01.09.2015 (текущего календарного года).

    - Возрастная категория 16.
    - По первому приоритетному ДОУ.
    - Тип ДОУ = любой ДОУ.

    :return: Q
    """

    return (
        queue_with_direct(context)
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(
            Q(after_desired_date_in_current_learn_year())
            | Q(
                Q(desired_date__isnull=True)
                & Q(children__date_of_birth__gte=(DateMixin.get_current_calendar_year_start()))
            )
            | Q(defer_demand=True)
        )
    )


def get_71_filter(context):
    """Фильтр для показателя 7.1

    - Заявления в статусах "Зарегистрировано" и "Подтверждение льгот".
    - Заявления в других статусах, у которых есть привязанные
        направления в факт/план группы встатусах:
            "Заключение договора", "Подтверждено",
            "Направлен в ДОУ", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления текущий учебный год >= с 02.09.2015
      (т.е. все заявки позже этой даты (включительно)).
    - Дата расчета возраста ребенка: на текущую дату.

    - возрастная категория 16.
    - Тип ДОУ = любой ДОУ.
    - по первому приоритетному ДОУ

    :return: Q
    """

    return (
        queue_with_direct(context)
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(
            Q(after_desired_date_in_current_learn_year())
            | Q(
                Q(desired_date__isnull=True)
                & Q(children__date_of_birth__gte=(DateMixin.get_current_calendar_year_start()))
            )
            | Q(defer_demand=True)
        )
    )


def get_72_filter(context):
    """Фильтр для показателя 7.2

    - Заявления в статусе "Зарегистрировано", "Подтверждение льгот".
    - Заявления в других статусах, у которых есть привязанные
        направления в факт/план группы в статусах:
            "Заключение договора", "Подтверждено",
            "Направлен в ДОУ", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - дата дата желаемого зачисления интервал [2.09.2015; 31.08.2016]
        период - после текущего учебного года.

    - тип ДОУ в заявке = любой.
    - дата расчета возраста = текущая дата.
    - возрастная категория 16.
    - по первому приоритетному ДОУ.

    :return: Q
    """

    return (
        queue_with_direct(context)
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(desired_date_interval_current_learn_year())
        & Q(defer_demand=False)
    )


def get_73_filter(context):
    """Фильтр для показателя 7.3
    - Заявления в статусе "Зарегистрировано" или "Подтверждение льгот"
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Заключение договора", "Подтверждено", "Направлен в ДОУ",
            "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - дата дата желаемого зачисления - следующий учебный год.

    - возрастная категория 16.
    - по первому приоритетному ДОУ.

    :return: Q
    """

    next_calendar_year = DateMixin.get_next_calendar_year_start()

    return (
        queue_with_direct(context)
        & ~with_pupil(context, check_plan=False)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(Q(desired_date__gt=next_calendar_year) | Q(defer_demand=True))
    )


def get_74_filter(context):
    """Фильтр для показателя 7.4

    - Заявления во всех статусах с направлениями в факт/план группы
        в статусах:
            "Заключение договора", "Подтверждено", "Направлен в ДОУ",
            "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления - текущий учебный год.

    - Возрастная категория 16.
    - по первому приоритетному ДОУ.

    :return: Q
    """

    return Q(
        ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(
            direct__status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            direct__group__status__in=FACT_PLAN_GS,
        ),
        desired_date_interval_current_learn_year(),
        Q(defer_demand=False),
    )


def get_75_filter(context):
    """Фильтр для показателей 7.5 и 7.6.

    7.5 - на текущую дату.
    7.6 - на первый день следующего учебного года.

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот".
    - Заявления в других статусах, у которых есть привязанные
        направления в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Следующий учебный год или не указана.

    - По первому приоритетному ДОУ.
    - Возрастная категория 16.

    :return: Q
    """

    return Q(
        Q(
            status_registration_or_privilege_confirmation()
            | Q(
                direct__status__code__in=(DRS.NEW, DRS.CONFIRM),
                direct__group__status__in=FACT_PLAN_GS,
            )
        )
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(declarationunit__ord=1, declarationunit__unit__id=context.unit.id)
        & Q(before_desired_date_in_next_learn_year() | Q(desired_date__isnull=True) | Q(defer_demand=True))
    )


def get_77_filter(context):
    """Фильтр для показателя 7.7.

    7.7 - на первый день следующего учебного года.

    - Статус заявления не важен, важно наличие направления в статусах:
            Направлен в ДОО, Заключение договора.
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Следующий учебный год или не указана.

    - По первому приоритетному ДОУ.
    - Возрастная категория 16.

    :return: Q
    """

    return Q(
        Q(
            direct__status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            direct__group__status__in=FACT_PLAN_GS,
        )
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(declarationunit__ord=1, declarationunit__unit__id=context.unit.id)
        & Q(before_desired_date_in_next_learn_year() | Q(desired_date__isnull=True) | Q(defer_demand=True))
    )


def get_8_filter(context):
    """
    Возвращает фильтр для расчета показателя 8.

    :param context: контекст
    :return: фильтр
    :rtype: Q

    """

    from_date = datetime.datetime.now()

    if from_date.day == 29 and from_date.month == 2:
        from_date = from_date.replace(month=from_date.month + 1, day=1)

    from_date = from_date.replace(year=from_date.year - 2)

    direction_status_codes = {
        DRS.ACCEPT,
        DRS.REGISTER,
        DRS.DOGOVOR,
        DRS.REJECT,
        DRS.NEED_CHANGE,
        DRS.REFUSED,
    }

    archive_status_code = ExtensionManager().execute(
        'kinder.plugins.archival_directions.extensions.get_archive_status_code'
    )

    if archive_status_code:
        direction_status_codes.add(archive_status_code)

    return Q(
        Q(direct__isnull=False)
        & Q(direct__status__code__in=direction_status_codes)
        & Q(direct__date__isnull=False)
        & Q(direct__date__gte=from_date)
        & Q(desired_date__isnull=False)
    )


def get_81_filter(context):
    """
    Возвращает фильтр для расчета показателя 8.1.

    :param context: контекст
    :return: фильтр
    :rtype: Q

    """

    return Q(get_8_filter(context) & Q(best_privilege__isnull=False))


def get_82_filter(context):
    """
    Возвращает фильтр для расчета показателя 8.2.

    :param context:
    :return: фильтр
    :rtype: Q

    """

    return Q(get_8_filter(context) & Q(best_privilege__isnull=True))


def get_83_filter(context):
    """
    Фильтр показателя 8.3.

    Направление в заявке не пустое и
    1. Имеет статус:
       - зачислен
       - направлен в доо
       - заключение договора
       - не явился
       - желает изменить доу
       - отказано
       - архив
    2. Дата выдачи направления больше чем два года назад
    3. Дата желаемого зачисления в заявке не пустая
    4. Исключаются заявки с кодами ОВЗ
       - Пусто
       - "Нет"
       - "Другое"
       - "Часто болеющие"
       - "С туберкулезной интоксикацией"
    5. Если ребенок в заявлении возрастом от 2-х месяцев до 7.5 лет
       то фильтруется еще по среднему времени ожидания
       очереди в детский сад
    """
    return Q(get_8_filter(context) & exclude_ovz_codes(SICK_CODES))


# TODO Фильтр показателя 9 не используется.
# TODO На всякий случай оставил.

# TODO Сейчас показатель 9 считается как сумма по фильтрам
# TODO 10 и 11 с фильтрацией по возрасту на 01.09

# TODO Сейчас показатель 9.1 считается как сумма по фильтрам
# TODO 10 и 11 с фильтрацией по возрасту на текущую дату

# def get_9_filter(context):
#     """Фильтр для показателя 9
#     :param context:
#     :return: Q
#     """
#
#     return (
#         Q(
#             queue_register_with_direct(context) &
#             ~Q(status__code=DSS.WANT_CHANGE_DOU)
#         ) &
#         Q(best_privilege__isnull=False) &
#         Q(
#             before_desired_date_in_current_learn_year() |
#             Q(desired_date__isnull=True)
#         ) &
#         Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
#     )


def get_10_filter(context):
    """Фильтр для показателя 10

    - Заявления в статусе "Зарегистрировано".
    - Заявления в других статусах с направлениями в факт/план группы в
        статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Тип лучшей привелегии заявления - FED (1).
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_register_with_direct(context)
        & ~with_pupil(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(best_privilege__type_id=PrivilegeType.FED)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_101_filter(context):
    """Фильтра для показателя 10.1

    То же что и 10 и
    - У ребёнка должна быть проставлена галочка наличия инвалидности

    :return: Q
    """
    return get_10_filter(context) & Q(children__is_invalid=True) & Q(defer_demand=False)


def get_11_filter(context):
    """Фильтр для показателя 11

    - Заявления в статусе "Зарегистрировано"
    - Заявления в других статусах с направлениями в факт/план группы в
        статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Тип лучшей привелегии заявления - MUN (2) или REG (3).
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_register_with_direct(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(best_privilege__type_id__in=(PrivilegeType.MUN, PrivilegeType.REG))
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_12_filter(context):
    """
    Фильтр для показателя 12.

    - Заявка в статусах "Зарегистрировано", "Подтверждение льгот",
       "Желает изменить ДОУ" или заявки в других статусах с направлениями
       в статусах "Подтверждено", "Предложено системой"
    - Исключаются заявки с кодами ОВЗ пусто,
       "Нет", "Другие", "Часто болеющие", "С туберкулезной интоксикацией"
    - Дата желаемого зачисления меньше 01.09 текущего учебного года
        или не указана вовсе.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_with_want_change_dou(context, direct_status=(DRS.CONFIRM, DRS.NEW))
        & exclude_ovz_codes(SICK_CODES)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
        & Q(children__health_need__isnull=False)
    )


def get_121_filter(context):
    """
    Фильтр для показателя 12.1.

    - Статус направления "Заключение договора" или "Направлен в ДОО"
        и группа в направлении Фактическая или Плановая.
    - Исключаются заявки с кодами ОВЗ пусто,
        "Нет", "Другие", "Часто болеющие", "С туберкулезной интоксикацией".
    - Дата желаемого зачисления меньше 01.09 текущего учебного года
        или дата желаемого зачисления не указана вовсе.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            direct__status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            direct__group__status__in=FACT_PLAN_GS,
        )
        & exclude_ovz_codes(SICK_CODES)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_13_filter(context):
    """Фильтр для показателя 13

    - Заявления в статусе "Зарегистрировано".
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Потребности по здоровью - ОВЗ компенсирующие (коды 1-13).
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Заявление с согласием на общеразвивающую группу.
        вне зависимости от наличия ОВЗ
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            Q(status__code=DSS.REGISTERED)
            | Q(
                direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                direct__group__status__in=FACT_PLAN_GS,
            )
        )
        & ~with_pupil(context, check_plan=False)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & health_need_filter(list(range(1, 14)))
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(consent_dev_group=True)
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_131_filter(context):
    """Фильтр для показателя 13.1

    - Заявления в направлениями в статусах "Направлен в ДОО" и
        "Заключение договора" в факт/план группы.
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - У ребенка в заявление нет зачисления в фактическую группу.
    - Потребности по здоровью - ОВЗ компенсирующие (коды 1-13).
    - Заявление с согласием на общеразвивающую группу
        вне зависимости от наличия ОВЗ.
    - Тип группы направления "Общеразвивающий".
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            direct__status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            direct__group__status__in=FACT_PLAN_GS,
        )
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & ~with_pupil(context, check_plan=False)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & health_need_filter(list(range(1, 14)))
        & Q(consent_dev_group=True)
        & Q(direct__group__type__code=GroupTypeEnumerate.DEV)
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_14_filter(context):
    """Фильтр для показателя 14

    - Заявления в направлениями в статусах "Зарегистрировано",
        "Подтверждение льгот", "Желает изменить ДОО".
    - Заявления в любых других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено" и "Предложено системой".
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Потребности по здоровью - ОВЗ оздоровительные (коды 14, 15, 16).
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            Q(status__code__in=(DSS.REGISTERED, DSS.PRIV_CONFIRMATING, DSS.WANT_CHANGE_DOU))
            | Q(
                direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                direct__group__status__in=FACT_PLAN_GS,
            )
        )
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & health_need_filter_by_codes(
            [
                HNE.OTHER,
                HNE.SICK,
                HNE.PHTHISIS,
                HNE.CELIAC,
                HNE.NEPHRO_UROL,
                HNE.CARDIOVASCULAR,
                HNE.RESPIRATORY,
                HNE.DIABETES,
                HNE.ALLERGOPATHOLOGY,
            ]
        )
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_15_filter(context):
    """Фильтр для показателя 15

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот"
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Заявление с согласием на на группу по присмотру и уходу.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_with_direct_status_confirm_new(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(consent_care_group=True)
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_16_filter(context):
    """Фильтр для показателя 16

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот"
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Режим работы групп в заявлении - круглосуточное пребывание.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_with_direct_status_confirm_new(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(work_type__code__in=get_all_day_work_types())
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_17_filter(context):
    """Фильтр для показателя 17

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот".
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Режим работы групп в заявлении - кратковременное пребывание.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_with_direct_status_confirm_new(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(work_type__code__in=get_short_day_types())
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_171_filter(context):
    """Фильтр для показателя 17.1

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот".
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Подтверждено", "Предложено системой".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Заявления с согласием на группу кратковременного пребывания.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        queue_with_direct_status_confirm_new(context)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context)
        & Q(consent_short_time_group=True)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_18_filter(context):
    """Фильтр для показателей 18

    - Заявления в статусах "Зарегистрировано" или "Подтверждение льгот"
    - Заявления в других статусах с направлениями в факт/план группы
        в статусах:
            "Предложено системой", "Подтверждено".
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Ребенку еще нет одного года.

    Возраст на 01.09

    :return: Q
    """

    return (
        Q(
            status_registration_or_privilege_confirmation()
            | Q(
                direct__status__code__in=(DRS.NEW, DRS.CONFIRM),
                direct__group__status__in=FACT_PLAN_GS,
            )
        )
        & ~with_pupil(context, check_plan=False)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_181_filter(context):
    """Фильтр для показателей 18.1

    То же что и в показателе 18, возраст на текущую дату.

    :return: Q
    """

    return get_18_filter(context)


def get_182_filter(context):
    """Фильтр для показателей 18.2

    То же что и в показателе 18, возраст на 01.01.следующего года.

    :return: Q
    """

    return get_18_filter(context)


def get_183_filter(context):
    """Фильтр для показателей 18.3

    - Заявления во всех других статусах с направлениями в статусах
        "Направлен в ДОО", "Заключение договора" в факт/план группы.
    - Исключены заявления в статусе "Желает изменить ДОО".
    - Исключены заявления детей у которых "есть зачисление":
        у ребенка есть хотя бы одно зачисление в статус группы которой
        "Фактическая" либо "Плановая",
        не учитываются временные зачисления и отчисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            direct__status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            direct__group__status__in=FACT_PLAN_GS,
        )
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~with_pupil(context, check_plan=False)
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_184_filter(context):
    """Фильтр для показателей 18.4

    То же что и в показателе 18, возраст на текущую дату.
    - Дата желаемого зачисления <= текущей даты или не указана.
    - Временные направления не учитываются
    - Не учитывать заявления, у которых есть направление в статусе
        "Направлен в ДОУ" либо "Заключение договора".
    :return: Q
    """

    return (
        Q(
            status_registration_or_privilege_confirmation()
            | Q(
                direct__status__code__in=(DRS.NEW, DRS.CONFIRM),
                direct__group__status__in=FACT_PLAN_GS,
            )
        )
        & ~with_pupil(context, check_plan=False)
        & ~Q(status__code=DSS.WANT_CHANGE_DOU)
        & ~Q(direct__temporary=True)
        & ~direct_status_registered_or_dogovor(context)
        & Q(before_desired_date_in_current_date() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_185_filter(context):
    """Фильтр для показателей 18.5

    То же что и в показателе 12, возраст на текущую дату.
    - Дата желаемого зачисления <= текущей даты или не указана.
    - нет проверки на ОВЗ
    :return: Q
    """

    return (
        queue_with_want_change_dou(context, direct_status=(DRS.CONFIRM, DRS.NEW))
        & Q(before_desired_date_in_current_date() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_20_filter(context):
    """Фильтр для показателя 20

    - Заявление в статусе "Желает изменить ДОУ".
    - Заявления в статусе "Подтверждение льгот" или в других статусах с
        направлениями в факт/план группы в статусах:
            "Подтверждено", "Предложено системой"
        при наличии у ребенка зачисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            Q(status__code=DSS.WANT_CHANGE_DOU)
            | Q(
                with_pupil(context)
                & Q(
                    Q(
                        direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                        direct__group__status__in=FACT_PLAN_GS,
                    )
                    | Q(status__code__in=(DSS.PRIV_CONFIRMATING, DSS.REGISTERED))
                )
            )
        )
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_201_filter(context):
    """Фильтр для показателя 20.1

    - Заявления со связанными направлениями в статусах "Направлен в ДОО" и
        "Заключение договора" во все факт/план группы организации при наличии
        у ребенка зачисления в другой детский сад в фактическую группу
        (зачисления с признаком Временно отчислен не учитываются).
        Направления в плановую группу учитываются только если есть связь с
        фактической группой через поле "Кабинет".
    - Заявления детей с зачислениями в плановую группу  с
        Датой зачисления по приказу > текущей (если нет зачислений
        в фактические группы данной организации). И при этом есть другое
        зачисление в фактическую или плановую группу,
        с датой зачисления по приказу <= текущей дате

    :return: Q
    """

    date_in_order = get_report_date_or_today()

    # Запрос для поиска зачислений не в текущую организацию
    pupils_in_other_dou = Pupil.objects.filter(temporary_deduct=False).exclude(grup__unit_id=context.unit.id)

    # Дети с зачислениями в фактические группы не в текущую организацию
    children_ids_in_fact_groups = (
        pupils_in_other_dou.filter(grup__status=GroupStatusEnum.FACT).values_list('children', flat=True).distinct()
    )

    # Дети с зачислениями в фактич. или плановые группы не в текущую организацию
    # с датой зачисления по приказу <= текущей дате
    children_ids = (
        pupils_in_other_dou.filter(
            grup__status__in=(GroupStatusEnum.FACT, GroupStatusEnum.PLAN),
            date_in_order__lte=date_in_order,
        )
        .values_list('children', flat=True)
        .distinct()
    )

    allowed_direct_statuses = (DRS.REGISTER, DRS.DOGOVOR)
    direct_filter = Q(direct__in=[])
    pupil_direct_filter = Q(children_id__in=[])

    # Фактические группы указанной организации
    fact_groups_of_unit = Group.objects.filter(unit=context.unit, status=GroupStatusEnum.FACT)

    for group in fact_groups_of_unit:
        # направления в факт группы в разрешенных статусах
        direct_in_group = Direct.objects.filter(
            Q(group=group) & Q(status__code__in=allowed_direct_statuses)
        ).values_list('id', flat=True)

        # связанные плановые группы
        bounded_plan_groups = Group.objects.filter(
            Q(room_id__isnull=False, room_id=group.room_id), status=GroupStatusEnum.PLAN
        )

        # направления в связанные план. группы в разрешенных статусах
        direct_count_in_bounded_group = (
            Direct.objects.filter(Q(group__in=bounded_plan_groups) & Q(status__code__in=allowed_direct_statuses))
            .exclude(
                declaration__children_id__in=Direct.objects.filter(
                    Q(group__unit=group.unit)
                    & Q(group__status=GroupStatusEnum.FACT)
                    & Q(status__code__in=allowed_direct_statuses)
                ).values_list('declaration__children_id', flat=True)
            )
            .values_list('id', flat=True)
        )

        pupil_direct_in_bounded_group = (
            Pupil.objects.filter(grup__in=bounded_plan_groups, date_in_order__gt=date_in_order)
            .exclude(
                Q(children_id__in=direct_count_in_bounded_group.values_list('declaration__children_id', flat=True))
                | Q(
                    children_id__in=Pupil.objects.filter(
                        temporary_deduct=False, grup__in=fact_groups_of_unit
                    ).values_list('children_id', flat=True)
                )
            )
            .distinct('children_id')
            .values_list('children_id', flat=True)
        )

        direct_filter |= Q(direct__in=direct_in_group) | Q(direct__in=direct_count_in_bounded_group)

        pupil_direct_filter |= Q(children_id__in=pupil_direct_in_bounded_group)

    return (
        direct_filter & Q(children_id__in=children_ids_in_fact_groups)
        | pupil_direct_filter & Q(children_id__in=children_ids)
    ) & Q(direct__group__unit_id=context.unit.id)


def get_202_filter(context):
    """Фильтр для показателя 20.2

    - Заявление в статусе "Желает изменить ДОУ".
    - Заявления в статусе "Подтверждение льгот" или в других статусах с
        направлениями в факт/план группы в статусах:
            "Подтверждено", "Предложено системой"
        при наличии у ребенка зачисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год или не указана.
    зачисления с признаком Временно отчислен
    - В заявлении в поле "Ограниченные возможности здоровья"
     значение не пусто и не равно "нет".
    - Ребенку еще нет одного года.

    :return: Q
    """

    return (
        Q(
            Q(status__code=DSS.WANT_CHANGE_DOU)
            | Q(
                with_pupil(context)
                & Q(
                    Q(
                        direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                        direct__group__status__in=FACT_PLAN_GS,
                    )
                    | Q(status__code__in=(DSS.PRIV_CONFIRMATING, DSS.REGISTERED))
                )
            )
        )
        & Q(before_desired_date_in_current_learn_year() | Q(desired_date__isnull=True))
        & with_health_need_filter()
        & Q(children__date_of_birth__lt=DateMixin.get_current_calendar_year_start())
        & Q(defer_demand=False)
    )


def get_203_filter(context):
    """Фильтр для показателя 20.3

    - Заявление в статусе "Желает изменить ДОУ".
    - Заявления в статусе "Подтверждение льгот" или в других статусах с
        направлениями в факт/план группы в статусах:
            "Подтверждено", "Предложено системой"
        при наличии у ребенка зачисления.
    - Дата желаемого зачисления <= 1/09/Текущий учебный год.

    :return: Q
    """

    return (
        Q(
            Q(status__code__in=DSS.WANT_CHANGE_DOU)
            | Q(
                with_pupil(context)
                & Q(
                    Q(
                        direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                        direct__group__status__in=FACT_PLAN_GS,
                    )
                    | Q(status__code__in=(DSS.PRIV_CONFIRMATING, DSS.REGISTERED))
                )
            )
        )
        & desired_date_interval_current_learn_year()
        & Q(defer_demand=False)
    )


def get_204_filter(context):
    """Фильтр для показателя 20.4

    - Заявление в статусе "Желает изменить ДОУ".
    - Заявления в статусе "Подтверждение льгот" или других статусах с
        направлениями в факт/план группы в статусах:
            "Подтверждено", "Предложено системой"
        при наличииу ребенка зачисления.
    - Дата желаемого зачисления > 1/09/Следующего учебного года.

    :return: Q
    """

    return Q(
        Q(status__code=DSS.WANT_CHANGE_DOU)
        | Q(
            with_pupil(context)
            & Q(
                Q(
                    direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                    direct__group__status__in=FACT_PLAN_GS,
                )
                | Q(status__code__in=(DSS.PRIV_CONFIRMATING, DSS.REGISTERED))
            )
        )
    ) & Q(after_desired_date_in_next_learn_year() | Q(defer_demand=True))


def get_205_filter(context):
    """Фильтр для показателя 20.5

    То же что и 20-й, но
    - Желаемая дата зачисления <= текущей дате или отсутствует
    - Отображается по учреждениям в которые ребёнок зачислен на данный момент

    :return: Q
    """
    pupil_filter = Q(
        children_id__in=Children.objects.filter(
            pupil__grup__unit_id=context.unit.id, pupil__grup__status__in=FACT_PLAN_GS
        )
    )

    return no_unit_specified_want_change_dou_filter() & pupil_filter & Q(defer_demand=False)


def get_206_filter(context):
    """Фильтр для показателя 20.6

    То же что и 20.5, но
    - Выбираются только заявки смена ДОО в которых связанна с изменением
      режима пребывания ребёнка
    - Исключаются те что попали в 20.8

    :return: Q
    """
    pupil_filter = Q(
        ~Q(work_type_id=F('children__pupil__grup__work_type_id')),
        children__pupil__grup__unit_id=context.unit.id,
        children__pupil__grup__status__in=FACT_PLAN_GS,
        work_type_id__isnull=False,
    )

    return no_unit_specified_want_change_dou_filter() & pupil_filter & ~get_208_filter(context) & Q(defer_demand=False)


def get_207_filter(context):
    """Фильтр для показателя 20.7

    То же что и 20.5, но
    - Выбираются только заявки смена ДОО в которых связанна с изменением
      направленности группы
    - Исключаются те что попали в 20.6 и 20.8

    :return: Q
    """
    pupil_filter = Q(
        ~Q(desired_group_type_id=F('children__pupil__grup__type_id')),
        children__pupil__grup__unit_id=context.unit.id,
        children__pupil__grup__status__in=FACT_PLAN_GS,
        desired_group_type_id__isnull=False,
    )

    return (
        no_unit_specified_want_change_dou_filter()
        & pupil_filter
        & ~get_208_filter(context)
        & ~Q(id__in=Declaration.objects.filter(get_206_filter(context)).values_list('id', flat=True))
        & Q(defer_demand=False)
    )


def get_208_filter(context):
    """Фильтр для показателя 20.8

    То же что и 20.5-й, но остаются только те заявления
    дети в которых зачислены в ДОО с типом:
        НЕ муниципальная/федеральная/государственная,
    и планируют перейти в ДОО с типом:
        муниципальная/федеральная/государственная.

    :return: Q
    """
    pupil_filter = Q(
        children_id__in=Children.objects.filter(
            pupil__grup__unit_id=context.unit.id,
            pupil__grup__status__in=FACT_PLAN_GS,
        ).exclude(pupil__grup__unit__dou_type__code__in=GOVERNMENT_TYPES)
    )

    target_unit_filter = Q(declarationunit__unit__dou_type__code__in=GOVERNMENT_TYPES)

    return no_unit_specified_want_change_dou_filter() & pupil_filter & target_unit_filter & Q(defer_demand=False)


def get_33_filter(context):
    """
    Фильтр для показателя 33

    Передается численность детей, снятых с учета в течение
    **текущего календарного года** по таким причинам:

    - Не явился (код didnt_come)
    - Отказано в услуге (код refused)
        в случае изменения заявления со статуса
        Зарегистрировано, Желает изменить ДОУ на статус
        Отказано в услуге
    - Архивное (код archive)
        в случае изменения заявления со статуса
        Зарегистрировано на статус Архивное
    - Архивное (код archive)
        в случае изменения заявления со статуса
        Желает изменить ДОУ на Архивное

    При расчета показателя 33 необходимо учитывать все заявления,
    у которых дата изменения статуса заявления входит в период с 01.01.хххх,
    где хххх - текущий год.

    :returns: Q
    """
    # Рассчетная дата начинается с 1 января,
    # год текущий или формирования отчета
    current_year = datetime.date(datetime.date.today().year, 1, 1)
    on_date = getattr(context, 'on_date', None)
    if callable(on_date):
        on_date = on_date()
    # Сработает для date и datetime
    if isinstance(on_date, datetime.date):
        current_year = datetime.date(on_date.year, 1, 1)

    didnt_come = (
        Q(status__code=DSS.DIDNT_COME)
        & Q(declarationstatuslog__status__code=DSS.DIDNT_COME)
        & Q(declarationstatuslog__datetime__gte=current_year)
    )
    refused = (
        Q(status__code=DSS.REFUSED)
        & Q(declarationstatuslog__old_status__code__in=[DSS.REGISTERED, DSS.WANT_CHANGE_DOU])
        & Q(declarationstatuslog__status__code=DSS.REFUSED)
        & Q(declarationstatuslog__datetime__gte=current_year)
    )
    archive = (
        Q(status__code=DSS.ARCHIVE)
        & Q(declarationstatuslog__old_status__code__in=[DSS.REGISTERED, DSS.WANT_CHANGE_DOU])
        & Q(declarationstatuslog__status__code=DSS.ARCHIVE)
        & Q(declarationstatuslog__datetime__gte=current_year)
    )
    return didnt_come | refused | archive


def queue_register_with_direct(context):
    """Фильтр.
    Заявления в статусе "Зарегистрировано".
    Заявления в других статусах со связанными направлениями в факт/план группы
    в статусах:
        "Подтверждено", "Предложено системой".

    :return: Q
    """

    return Q(status__code=DSS.REGISTERED) | Q(
        direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
        direct__group__status__in=FACT_PLAN_GS,
    )


def queue_with_direct(context):
    """Фильтр.
    Заявления в статусах "Зарегистрировано" или "Подтверждение льгот".
    Заявления в других статусах со связанными направлениями в факт/план группы
    в статусах:
        "Подтверждено", "Заключение договора", "Направлен в ДОУ",
        "Предложено системой".

    :return: Q
    """

    return Q(status__code__in=(DSS.REGISTERED, DSS.PRIV_CONFIRMATING)) | Q(
        direct__status__code__in=BEFORE_ENROLL_DRS,
        direct__group__status__in=FACT_PLAN_GS,
    )


def queue_with_direct_status_confirm_new(context):
    """Фильтр.
    Заявление в статусах "Зарегистрировано" или "Подтверждение льгот"
    Заявления в других статусах со связанными направлениями в статусах:
        "Подтверждено", "Предложено системой"

    :return: Q
    """

    return Q(status__code__in=(DSS.REGISTERED, DSS.PRIV_CONFIRMATING)) | Q(
        direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
        direct__group__status__in=FACT_PLAN_GS,
    )


def status_registration_or_privilege_confirmation():
    """Фильтр.
     Заявления в статусе "Зарегистрировано" или "Подтверждение льгот"

    :return: Q
    """

    return Q(status__code__in=(DSS.REGISTERED, DSS.PRIV_CONFIRMATING))


def queue_with_want_change_dou(context, direct_status=None):
    """Фильтр.
    Заявление в статусах:
        "Зарегистрировано", "Подтверждение льгот", "Желает изменить ДОУ"
    Заявления в других статусах со связанными направлениями в факт/план группы
    в статусах:
        "Заключение договора", "Подтверждено", "Направлен в ДОУ",
        "Предложено системой"

    :return: Q
    """
    if direct_status is None:
        direct_status = BEFORE_ENROLL_DRS

    q = Q(status__code__in=(DSS.REGISTERED, DSS.PRIV_CONFIRMATING, DSS.WANT_CHANGE_DOU)) | Q(
        direct__status__code__in=direct_status,
        direct__group__status__in=FACT_PLAN_GS,
    )

    if DRS.DOGOVOR in direct_status:
        q |= plan_pupil_directions()

    return q


def status_directed():
    """Фильтр Направлен в ДОУ
    :return: Q
    """

    return Q(status__code=DSS.DIRECTED)


def direct_status_registered_or_dogovor(context):
    """Направление в статусе Направлен в ДОУ или Заключение договора

    :return: Q
    """
    declarations_id_with_needed_directs = (
        Direct.objects.filter(
            group__unit__in=(context.unit.get_mo().get_descendants(include_self=True)),
            status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
        )
        .values_list('declaration_id', flat=True)
        .distinct()
    )

    return Q(id__in=declarations_id_with_needed_directs)


def direct_in_common_group(context):
    """Фильтр Направления выданные в общеразвивающие группы в статусе
    Направлен в ДОУ или Заключение договора.
    Повторяет функциональность direct_status_registered_or_dogovor
    для того, чтобы не выполнять два запроса

    :return: Q
    """
    declarations_id_with_needed_directs = (
        Direct.objects.filter(
            group__unit_id=context.unit.id,
            status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
            group__type__code=GroupTypeEnumerate.DEV,
        )
        .values_list('declaration_id', flat=True)
        .distinct()
    )

    return Q(id__in=declarations_id_with_needed_directs)


def desired_date_in_next_learn_year():
    """Фильтр дата желаемого зачисления >= 2/09/Следующего учебного года
    :return: Q
    """

    next_learn_year_begin, _ = DateMixin.get_current_learn_year()
    return Q(desired_date__gte=next_learn_year_begin)


def desired_date_interval_current_learn_year():
    """Фильтр дата желаемого зачисления > 1/09/Текущий учебный год и
     < 1/09/Следующего учебного года
    :return: Q
    """

    date_start = DateMixin.get_current_calendar_year_start()
    date_end = DateMixin.get_next_calendar_year_start()

    return Q(desired_date__gt=date_start, desired_date__lt=date_end)


def before_desired_date_in_current_date():
    """Фильтр дата желаемого зачисления <= Текущей даты
    :return: Q
    """
    date_border = datetime.date.today()

    return Q(desired_date__lte=date_border)


def before_desired_date_in_current_learn_year():
    """Фильтр дата желаемого зачисления <= 1/09/Текущий учебный год
    :return: Q
    """

    date_border = DateMixin.get_current_calendar_year_start()

    return Q(desired_date__lte=date_border)


def after_desired_date_in_current_learn_year():
    """Фильтр дата желаемого зачисления > 1/09/Текущий учебный год
    :return: Q
    """

    date_border = DateMixin.get_current_calendar_year_start()

    return Q(desired_date__gt=date_border)


def after_desired_date_in_next_learn_year():
    """Фильтр дата желаемого зачисления > 1/09/Следующего учебного года
    :return: Q
    """

    date_border = DateMixin.get_next_calendar_year_start()

    return Q(desired_date__gte=date_border)


def before_desired_date_in_next_learn_year():
    """Фильтр дата желаемого зачисления <= 1/09/Следующего учебного года."""
    date_border = DateMixin.get_next_calendar_year_start()

    return Q(desired_date__lte=date_border)


def health_need_filter(health_need):
    """Фильтр потребностей по здоровью

    :return: Q
    """
    return Q(children__health_need_id__in=health_need)


def health_need_filter_by_codes(codes):
    """Фильтр потребностей по здоровью (по кодам)

    :type codes: List[str]
    :rtype: Q
    """
    return Q(children__health_need__code__in=codes)


def with_health_need_filter():
    """В заявлении в поле "Ограниченные возможности здоровья"
     значение не пусто и не равно "Нет".
     Если фильтровать по коду,
     то формируется неверный запрос, пришлось зашить Id.

    :return: Q
    """
    hn_ids = HealthNeed.objects.exclude(code=HealthNeed.NO).values_list('id', flat=True).distinct()

    return Q(children__health_need__id__in=hn_ids)


def exclude_ovz_codes(codes=None):
    """
    Возвращает фильтр по ОВЗ исключая переданные коды если
    не заполнен документ подтверждающий ОВЗ.

    :return: Q
    """
    if not codes:
        return Q()
    hn_ids = HealthNeed.objects.exclude(code__in=codes).values_list('id', flat=True).distinct()

    return Q(children__health_need__id__in=hn_ids) | ~Q(children__health_need_confirmation__isnull=True)


def no_unit_specified_want_change_dou_filter():
    """Заявления в статусе "Подтверждение льгот" или в других статусах с
    направлениями в факт/план группы в статусах: "Подтверждено",
    "Предложено системой"

    !!! Без проверки наличия у ребенка зачисления в учреждение
    """
    return Q(
        Q(status__code=DSS.WANT_CHANGE_DOU)
        | Q(
            Q(
                direct__status__code__in=(DRS.CONFIRM, DRS.NEW),
                direct__group__status__in=FACT_PLAN_GS,
            )
            | Q(status__code=DSS.PRIV_CONFIRMATING)
        )
    ) & (Q(desired_date__lte=datetime.date.today()) | Q(desired_date__isnull=True))


def with_pupil(context, check_plan=True):
    """Фильтр по детям.

    Заявления детей, у которых есть зачисления в факт/план группы.
    Не исключаются дети с временными отчислениями.

    :param context: Контекст
    :param check_plan: Признак доп. фильтрации плановых зачислений
    :type check_plan: bool

    :return: Q объект
    :rtype: Q
    """

    if check_plan:
        date_in_order = get_report_date_or_today()

        q = Q(grup__status__in=GroupStatusEnum.FACT) | Q(
            Q(date_in_order__lte=date_in_order) | Q(date_in_order__isnull=True), grup__status=GroupStatusEnum.PLAN
        )
    else:
        q = Q(grup__status__in=FACT_PLAN_GS)

    children_ids = Pupil.objects.filter(q).values_list('children', flat=True).distinct()

    return Q(children__in=children_ids)


def plan_pupil_directions():
    """Фильтр по детям.

    Зачисления в плановые группы с датой зачисления по приказу
    большей контрольной даты, которые считаются как направления
    в статусе "Заключение договора".

    :return: Q объект
    :rtype: Q
    """

    date_in_order = get_report_date_or_today()

    children_ids = (
        Pupil.objects.filter(
            date_in_order__gt=date_in_order,
            grup__status=GroupStatusEnum.PLAN,
        )
        .values_list('children', flat=True)
        .distinct()
    )

    return Q(children__in=children_ids)


def with_fact_pupil() -> Q:
    """Фильтр по детям.

    Идентификаторы детей, у которых есть зачисления в факт группы.
    Не учитываем временно отчисленных.
    """

    q = Q(grup__status=GroupStatusEnum.FACT, temporary_deduct=False)

    children_ids = Pupil.objects.filter(q).values_list('children', flat=True).distinct()

    return Q(children__in=children_ids)
