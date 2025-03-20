from kinder.core.dict.models import (
    HealthNeedEnumerate as HNE,
    WorkType,
)


def get_all_day_work_types():
    work_types = WorkType.objects.all()
    all_day_types = [WorkType.ALLDAY]
    for work_type in work_types:
        code = work_type.code
        try:
            torn_code = code.split('-')
        except AttributeError:
            # Код может быть не заполнен
            continue

        map_code = torn_code[0]
        map_code = map_code.replace(',', '.')
        try:
            numeric_map_code = float(map_code)
        except ValueError:
            continue

        if numeric_map_code == 24:
            all_day_types.append(work_type.code)

    return all_day_types


def get_short_day_types():
    work_types = WorkType.objects.all()
    short_types = [WorkType.SHORT]
    for work_type in work_types:
        code = work_type.code
        try:
            torn_code = code.split('-')
        except AttributeError:
            # Код может быть не заполнен
            continue

        map_code = torn_code[0]
        map_code = map_code.replace(',', '.')
        try:
            numeric_map_code = float(map_code)
        except ValueError:
            continue

        if 1 <= numeric_map_code < 8:
            short_types.append(work_type.code)

    return short_types


class HealthNeedEnumsCollectorMap(object):
    """Маппинг справочника Ограниченные возможности здоровья в показатель"""

    health_need_22_1 = (HNE.DEAFNESS, HNE.HARDOFHEARTING)
    health_need_22_1_1 = (HNE.DEAFNESS,)
    health_need_22_1_2 = (HNE.HARDOFHEARTING,)
    health_need_22_2 = (HNE.SPEACH, HNE.PHONETICS)
    health_need_22_3 = (HNE.BLINDNESS, HNE.AMAUROSIS)
    health_need_22_3_1 = (HNE.AMAUROSIS,)
    health_need_22_3_2 = (HNE.BLINDNESS,)
    health_need_22_4 = (HNE.BACKLIGHT, HNE.BACKHARD)
    health_need_22_5_1 = (HNE.BACK,)
    health_need_22_5_2 = (HNE.AUTISM,)
    health_need_22_6 = (HNE.DISABLEMENT,)
    health_need_22_7 = (HNE.INVALIDITY,)
    health_need_22_8_2 = (HNE.COCHLEAR_IMPL,)
    not_health_need = (HNE.NOT,)
