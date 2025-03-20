import datetime

from django.db.models import (
    Q,
)

from m3.plugins import (
    ExtensionManager,
)

from kinder.core.direct.models import (
    DRS,
    Direct,
)
from kinder.core.group.enum import (
    GroupStatusEnum,
)
from kinder.core.group.models import (
    Pupil,
)
from kinder.core.unit.models import (
    Unit,
)

from gisdo.utils import (
    get_report_date_or_today,
)


def get_children_last_direct_ids(mo_id, report_start_date, directs_filter=Q(), include_pupil=False):
    """
    Возвращает отфильтрованные последние направления детей.

    Используется для расчета показателей 32, 32.1, 32.2.

    Последнее выданное направление, если у ребенка их несколько в периоде:
        - направления в статусе "Направлен в ДОУ", "Заключение договора",
        "Желает изменить ДОУ", "Не явился", "Отказано", "Зачислен".

        С включенным плагином "Архивные направления"
        добавляются направления в статусе "Архив".

        - дата создания направления: [01.01.2019 - текущая дата],
        т.е текущий календарный год.

    Если параметр include_pupil == True, то выполняет выборку зачислений:
        - В плавновые группы;
        - Дата зачисления по приказу больше контрольной даты;
        - Организация зачисления переданное МО и ниже по иерархии;
        - Дата зачисления [01.01.2019 - контрольная дата]

    :param: mo_id: ID МО для заявлений которого выбираются направления.
    :param: directs_filter: Фильтр статусов заявлений среди последних.
    :param include_pupil: Признак включения зачислений

    :return: Tuple[QuerySet, QuerySet]
    """

    direction_status_codes = {
        DRS.DOGOVOR,
        DRS.REGISTER,
        DRS.NEED_CHANGE,
        DRS.REJECT,
        DRS.REFUSED,
        DRS.ACCEPT,
    }

    archive_status_code = ExtensionManager().execute(
        'kinder.plugins.archival_directions.extensions.get_archive_status_code'
    )

    if archive_status_code:
        direction_status_codes.add(archive_status_code)

    today_ = datetime.date.today()
    date_in_order = get_report_date_or_today(report_start_date)

    # фильтр для выбора последних заявлений детей
    directs_ids = (
        Direct.objects.filter(
            declaration__mo__id=mo_id,
            status__code__in=direction_status_codes,
            date__range=(datetime.date(today_.year, 1, 1), today_),
        )
        .order_by('declaration__children', '-date', '-id')
        .distinct('declaration__children')
        .values_list('id', flat=True)
    )

    # Так же считается направлениями
    if include_pupil:
        pupils = Pupil.objects.filter(
            Q(grup__status=GroupStatusEnum.PLAN, date_in_order__gt=date_in_order),
            grup__unit_id__in=Unit.objects.get(pk=mo_id).get_descendants(),
            date__range=(datetime.date(today_.year, 1, 1), date_in_order),
        )
    else:
        pupils = Pupil.objects.none()

    # фильтруются уже среди последних заявлений детей
    return Direct.objects.filter(
        directs_filter,
        id__in=directs_ids,
    ).values_list('id', flat=True), pupils


def get_32_filter():
    """Фильтр для показателя 32.

    Направления в статусе "Зачислен".

    С включенным плагином "Архивные направления"
    добавляются направления в статусе "Архив".

    :return: Q объект
    :rtype: Q
    """

    direction_status_codes = {
        DRS.ACCEPT,
    }

    archive_status_code = ExtensionManager().execute(
        'kinder.plugins.archival_directions.extensions.get_archive_status_code'
    )

    if archive_status_code:
        direction_status_codes.add(archive_status_code)

    return Q(status__code__in=direction_status_codes)


def get_321_filter():
    """
    Фильтр для показателя 32.1.

    Направления в статусе "Направлен в ДОУ", "Заключение договора",
    "Желает изменить ДОУ", "Не явился", "Отказано", "Зачислен".

    С включенным плагином "Архивные направления"
    добавляются направления в статусе "Архив".

    :return: Q объект
    :rtype: Q
    """

    direction_status_codes = {
        DRS.DOGOVOR,
        DRS.REGISTER,
        DRS.NEED_CHANGE,
        DRS.REJECT,
        DRS.REFUSED,
        DRS.ACCEPT,
    }

    archive_status_code = ExtensionManager().execute(
        'kinder.plugins.archival_directions.extensions.get_archive_status_code'
    )

    if archive_status_code:
        direction_status_codes.add(archive_status_code)

    return Q(status__code__in=direction_status_codes)


def get_322_filter():
    """
    Фильтр для показателя 32.2.

    Направления в статусе "Не явился", "Желает изменить ДОО", "Отказано"

    :return: Q объект
    :rtype: Q
    """

    return Q(status__code__in=(DRS.REJECT, DRS.NEED_CHANGE, DRS.REFUSED))
