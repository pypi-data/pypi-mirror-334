from __future__ import (
    unicode_literals,
)

import re
from datetime import (
    datetime,
)
from operator import (
    attrgetter,
)

from django.db.models import (
    Q,
    Subquery,
)

from kinder.core.dict.models import (
    DouType,
    UnitKind,
)
from kinder.core.emie_unit.models import (
    EmieUnitModel,
    UnitDocFiles,
)
from kinder.core.employer.models import (
    EmployerPost,
)
from kinder.core.group.models import (
    Group,
    GroupStatusEnum,
    Pupil,
)
from kinder.core.unit.models import (
    FilialData,
    FilialType,
    StructureTypes,
    Unit,
    UnitStatus,
)

from .utils import (
    UnitHelper,
    get_file_url,
    try_date_in_string,
)


website_pattern = re.compile('((https?)\:\/\/)?(\S+)')
phone_pattern = re.compile('([0-9]{10}(,[0-9]{10})*)')
email_pattern = re.compile('(\S+@\S+\.\S+)')


ORGANIZATION_TYPES = {
    DouType.MUNICIPAL: 1,
    DouType.GOVERNMENT: 2,
    DouType.NOT_GOVERNMENT_WITH_LICENSE: 3,
    DouType.NOT_GOVERNMENT_WITHOUT_LICENSE: 4,
    DouType.IP_WITH_LICENSE: 5,
    DouType.IP_WITHOUT_LICENSE: 6,
    DouType.DEPARTMENTAL: 7,
}


def get_dou_type(dou):
    dou_type = dou.dou_type
    if dou_type is None or dou_type.code == DouType.OTHER:
        code = DouType.GOVERNMENT
    else:
        code = dou_type.code
    return ORGANIZATION_TYPES[code]


# Коды статусов в Информике (отличаются от наших)
WORK = 1
RECONSTRUCTION = 3
IN_CAPITAL_REPAIR = 2
SUSPENDED = 4
NO_CONTINGENT = 5
PENDING_OPEN = 6

# Маппинг этих статусов на наши
STATUSES = (
    (UnitStatus.NONE, WORK),
    (UnitStatus.RECONSTRUCTION, RECONSTRUCTION),
    (UnitStatus.IN_CAPITAL_REPAIR, IN_CAPITAL_REPAIR),
    (UnitStatus.SUSPENDED, SUSPENDED),
    (UnitStatus.MISSING_CONTINGENT, NO_CONTINGENT),
    (UnitStatus.PENDING_OPEN, PENDING_OPEN),
)


def _get_gisdo_unit_status_code(original_code, default=None):
    """Маппинг кодов статусов учреждения для фед. отчётности."""
    return dict(STATUSES).get(original_code, None or default)


# статусы для атрибута `status_building`
FUNCTIONING = 1
NOT_FUNCTIONING = 0

FUNCTIONING_MAPPING = {
    WORK: FUNCTIONING,
    RECONSTRUCTION: NOT_FUNCTIONING,
    IN_CAPITAL_REPAIR: NOT_FUNCTIONING,
    SUSPENDED: NOT_FUNCTIONING,
    NO_CONTINGENT: FUNCTIONING,
    PENDING_OPEN: NOT_FUNCTIONING,
}


def get_dou_status_building(dou, default=None):
    """Код для атрибута `status_building` по "нашему" статусу учреждения."""
    return FUNCTIONING_MAPPING.get(get_dou_status(dou), None or default)


# статусы при которых в случае отсутствия детей в ДОУ
# устанавливаются нулевые свободные места
NOT_CALCULATED_STATUSES = [k for k, v in list(FUNCTIONING_MAPPING.items()) if v == NOT_FUNCTIONING]


def _has_working_filials(dou):
    """Проверяет имеет ли ДОУ функционирующие филилалы/корпуса.

    Функционирующими считаются ДОУ у которых есть дети
    в плановых / фактических группах.

    """

    result = False

    filials = (
        FilialData.objects.filter(head=dou).filter(UnitHelper.ALLOWED_FILIAL_FILTER).values_list('filial_id', flat=True)
    )

    # Если у ДОО нет филиалов/корпусов, то проверять зачисления не нужно
    if not filials.exists():
        return result

    filials = filials.iterator()

    dou_groups = Group.objects.filter(status=GroupStatusEnum.FACT).filter(Q(unit=dou) | Q(unit__in=filials))

    for group in dou_groups:
        children_in_fact = Pupil.objects.filter(grup=group, temporary_deduct=False, grup__status=GroupStatusEnum.FACT)

        children_in_plan = (
            Pupil.objects.filter(Q(grup__room_id__isnull=False, grup__room_id=group.room_id))
            .filter(temporary_deduct=False, grup__status=GroupStatusEnum.PLAN)
            .exclude(
                children_id__in=Pupil.objects.filter(
                    grup__unit=group.unit, temporary_deduct=False, grup__status=GroupStatusEnum.FACT
                ).values_list('children_id', flat=True)
            )
        )

        if children_in_fact.exists() or children_in_plan.exists():
            result = True
            break

    return result


def get_dou_status(dou):
    """Код статуса учреждения в gisdo."""

    if _has_working_filials(dou) and dou.status != UnitStatus.NONE:
        status = WORK
    else:
        status = _get_gisdo_unit_status_code(dou.status, default=NO_CONTINGENT)

    return status


def get_dou_status_comment(status, unit):
    """Комментарий к полю статус.

    для status = 1 атрибут не передается,
    для status = 2 и 3 указывается планируемая дата окончания работ,
    для status = 4 и 5 указывается причина и планируемая дата открытия
        (Если статус 5 и при этом наш статус NONE (0) то передаем "нет"),
    для status = 6 указывается планируемая дата открытия.

    :param status: статус учреждения в кодах фед отчетности, см список
    который возвращает get_dou_status_comment
    :param unit: Unit инстанс модели учреждений
    :return: текстовое представление комментария к статусу
    или None если атрибут не надо передавать

    """

    comment = None
    if status in (RECONSTRUCTION, IN_CAPITAL_REPAIR):
        comment = try_date_in_string(unit.end_repair_date)
    elif status == SUSPENDED:
        comment = unit.suspend_missing_cont_reason or ''
        comment += try_date_in_string(unit.commissioning_date)
    elif status == NO_CONTINGENT:
        if unit.status == UnitStatus.NONE:
            comment = 'нет'
        else:
            comment = unit.suspend_missing_cont_reason or ''
            comment += try_date_in_string(unit.commissioning_date)
    elif status == PENDING_OPEN:
        comment = try_date_in_string(unit.build_date)

    return comment


def get_passport(ext_unit):
    """Возвращает ссылку на паспорт доступности
    :param ext_unit:
    :return:

    """

    default = ''
    if not ext_unit:
        return default
    if ext_unit.availability_passport_url:
        return ext_unit.availability_passport_url
    elif ext_unit.availability_passport_doc:
        return get_file_url(ext_unit, 'availability_passport_doc')
    elif ext_unit.no_availability_passport:
        return 'нет'
    return default


def get_detailed_passport(ext_unit):
    """Возвращает ссылку на паспорт доступности и тип паспорта

    :param ext_unit: Экземляр BaseEmieModel для организации или None

    :return: Строка со ссылкой на паспорт доступности и типом, если есть
    """
    if ext_unit:
        if ext_unit.availability_passport_url:
            return f'{ext_unit.availability_passport_url} (ссылка)'
        elif ext_unit.availability_passport_doc:
            file_url = get_file_url(ext_unit, 'availability_passport_doc')
            return f'{file_url} (файл)'
    return 'нет'


def get_dou_structure_type(dou):
    conformity = {
        StructureTypes.KINDER: 1,
        StructureTypes.SCHOOL: 2,
        StructureTypes.PRESOTHER: 3,
        StructureTypes.UNIVERSITY: 4,
    }

    if dou.structure_type == StructureTypes.OTHER:
        return 1
    else:
        return conformity[dou.structure_type]


def get_groups_num(dou):
    filials = (
        FilialData.objects.filter(head=dou)
        .filter(UnitHelper.ALLOWED_FILIAL_FILTER)
        .values_list('filial_id', flat=True)
        .iterator()
    )

    dou_groups = (
        Group.extended_objects.with_count_norm()
        .select_related('type', 'health_need')
        .filter(status=GroupStatusEnum.FACT)
        .filter(Q(unit=dou) | Q(unit__in=filials))
    )

    return dou_groups.count()


def has_fact_groups(dou):
    """Проверяет есть ли в ДОУ фактические группы"""

    return Group.objects.filter(unit=dou, status=GroupStatusEnum.FACT).exists()


def get_dou_filials(dou):
    """Возвращает филиалы ДОУ"""

    return FilialData.objects.filter(head=dou).filter(UnitHelper.ALLOWED_FILIAL_FILTER)


def get_units_report(mo, units):
    """
    Возвращает организации для отчета ФО (xml).

    Данные организации записываются в теге:
     <organizations>
        <organization>
            ...
        </organization>
     <.organizations>

    :param mo: организация типа МО, для которой отбираются ДОО в отчет
    :type mo: Unit
    :param units: список ранее выбранных организаций для МО,
    по которым были подсчитаны показатели
    :type units: List[Unit]

    :return: список организаций
    :rtype: QuerySet

    """

    # Идентификаторы организаций найденных для расчета показателей ФО.
    units_id = tuple(map(attrgetter('id'), units))

    # По найденным организациям для отчета применяет доп. проверку,
    # исключает организации, которые относятся к МО
    # и являются филиалами организаций, находящихся в данном МО.
    subquery_banned_units = Subquery(
        FilialData.objects.filter(
            Q(head__in=units_id) & UnitHelper.ALLOWED_FILIAL_FILTER & Q(filial__gisdo__related_to_mo=mo)
        ).values_list('id', flat=True)
    )

    result_units = Unit.objects.filter(id__in=units_id).exclude(filial__in=subquery_banned_units)

    return result_units


def get_dou_filials_and_building_ids(dou):
    """Возвращает id филиалов и корпусов ДОУ"""

    filials = get_dou_filials(dou).values('filial_id')

    valid_filials = Unit.objects.filter(id__in=filials, is_filial__in=[FilialType.FILIAL, FilialType.CORPUS])
    return valid_filials.values('id')


def get_filial_num(dou):
    """Количество подтвержденных филиалов."""

    filials = get_dou_filials(dou).select_related('filial')

    filials_count = 0
    for filial_data in filials:
        if has_fact_groups(filial_data.filial):
            filials_count += 1

    return filials_count


def get_unit_fias_house_guid(dou):
    """Возвращаем фиас код адреса организации."""

    if dou.address_house_guid:
        return dou.address_house_guid
    elif dou.address_street:
        return dou.address_street
    elif dou.address_place:
        return dou.address_place
    else:
        return '00000000-0000-0000-0000-000000000000'


def get_additional_info_by_dou(dou, model=UnitDocFiles):
    """Дополнительная информация по организации."""

    filials = UnitHelper.get_filial(dou)
    extensions = model.objects.filter(Q(unit=dou) | Q(unit__in=filials)).values_list('name', flat=True)

    if not extensions.exists():
        return 'нет'
    else:
        filled_extensions = [extension for extension in extensions if extension]
        info = ','.join(filled_extensions)
        if info:
            return info
        else:
            return 'нет'


def _get_ext_unit_value(dou, name_param):
    """Проверяем что значение поля name_param равно True в
    самом доу или его филилале
    :param dou:
    :param name_param: имя парамера
    :return:

    """

    try:
        ext_unit = dou.ext_unit
        value = getattr(ext_unit, name_param)
        if value:
            return value
        param = dict()
        param['filial__ext_unit__%s' % name_param] = True
        return get_dou_filials(dou).filter(**param).exists()
    except EmieUnitModel.DoesNotExist:
        pass
    return False


def get_num_advisory_centr(dou_list):
    """Считаем ДОО, у которых выставлен чек бокс "Наличие КЦ в
    ДОО или его филиале

    """

    result = 0
    for dou in dou_list:
        if _get_ext_unit_value(dou, 'counseling_center'):
            result += 1
    return result


def get_num_early_assistance(dou_list):
    """читаем ДОО, у которых выставлен чек бокс "Наличие КЦ в
    ДОО или его филиале

    """

    result = 0
    for dou in dou_list:
        if _get_ext_unit_value(dou, 'early_help_service'):
            result += 1
    return result


def get_filial_info(dou):
    return 1 if UnitHelper.get_filial(dou).exists() else 0


def get_max_doo(mo):
    """Возвращает максимальное количество желаемых ДОО для МО."""

    # максимальное количество ДОО указанное для МО
    if mo.max_desired_dou != -1:
        return mo.max_desired_dou

    # если для МО не указано - максимальное количество для РЕГИОНА
    region = mo.get_ancestors().filter(kind=UnitKind.REGION).first()
    if region is not None and region.max_desired_dou != -1:
        return region.max_desired_dou

    # если у РЕГИОНА не указано - общее количество ДОО в данном муниципалитете
    # (не учитываются Статус учреждения = "Закрытые", "ликвидированные",
    # "присоединненные к другой организации", а так же филиалы и корпуса)
    return (
        mo.get_descendants()
        .filter(kind=UnitKind.DOU)
        .exclude(
            status__in=UnitStatus.ALL_CLOSED_STATUS,
        )
        .exclude(is_filial__in=(FilialType.FILIAL, FilialType.CORPUS))
        .count()
    )


def get_value(value, default=None):
    if not value:
        return default or ''
    return value


def get_employers_in_dou_by_category(dou_ids: list[int], category: list[str], part_time: bool = False) -> int:
    """Возвращает количество не уволенных и находящиеся в должности на текущую дату сотрудников в указанных ДОО
    по категории должности и типу совместительства.

    Args:
        dou_ids: Список id организаций
        category: Список категорий должностей
        part_time: Признак работы по совместительству

    Returns: Количество сотрудников, подходящих под условия
    """

    today = datetime.today()

    query = EmployerPost.objects.filter(
        post__post_category__code__in=category, employer__unit_id__in=dou_ids, employer__discharged=False
    ).exclude(Q(date_of_resignation__lt=today) | Q(date_of_inauguration__gt=today))

    if not part_time:
        return query.filter(Q(part_time=part_time) | Q(contingentemployeepost__is_internal_part_time=True)).count()

    return query.filter(contingentemployeepost__is_external_part_time=True).count()


# Наличие лицензии на ведение образовательной деятельности

HAVE_LICENSE = 1  # Имеется лицензия на образовательную деятельность
NO_LICENSE = 2  # Лицензия на образовательную деятельность отсутствует

# Наличие договора на оказание образовательных услуг с другой ДОО

# Указывается в случае отсутствия у ДОО лицензии на ведение образовательной
# деятельности и заключения договора об оказании образовательных услуг
# с другой ДОО
NO_PARTNER_DOO = 2
# Указывается в случае наличия у ДОО лицензии на ведение
# образовательной деятельности
HAVE_PARTNER_DOO = 1


def get_unit_license_partner_values(unit):
    """
    Возвращает значения тегов `license` и `partner_doo`
    """
    license_value = HAVE_LICENSE if unit.have_lic else NO_LICENSE
    partner_value = HAVE_PARTNER_DOO if unit.have_contract else NO_PARTNER_DOO

    return license_value, partner_value
