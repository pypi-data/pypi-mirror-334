import datetime
from collections import (
    OrderedDict,
)
from json import (
    JSONEncoder,
)
from typing import (
    Any,
    List,
    Optional,
    Union,
)
from urllib.parse import (
    urljoin,
)

from dateutil.relativedelta import (
    relativedelta,
)
from django.conf import (
    settings,
)
from django.db.models import (
    Q,
    Sum,
)
from future import (
    standard_library,
)
from future.builtins import (
    object,
    str,
)

from m3.actions import (
    ApplicationLogicException,
    ControllerCache,
)

from kinder.core.dict.models import (
    UnitKind,
)
from kinder.core.group.enum import (
    GroupStatusEnum,
)
from kinder.core.group.models import (
    Group,
)
from kinder.core.unit.models import (
    FilialData,
    FilialTypeStatus,
    Unit,
)

from gisdo import (
    settings as gisdo_settings,
)
from gisdo.constants import (
    AGE_CATEGORIES_CUT,
    AGE_CATEGORIES_EIGHT,
    AGE_CATEGORIES_FULL,
    ALL,
    STATUSES_UNIT_EXCLUDE,
)


standard_library.install_aliases()


class ViewList(object):
    def __init__(self):
        self._data = []
        self._index = 0

    def append(self, tpl):
        description, value = tpl

        data_value = (self._index, description, value)

        self._data.append(data_value)
        self._index += 1

    def get_data(self):
        return self._data


class DataDictionary(object):
    """Словарь, который содержит в себе индекс"""

    def __init__(self):
        self._data_dictionary = {}
        self.index = 0

    def __setitem__(self, key, value):
        # Пока simple_report не видит параметр,
        # который внутри себя содержит символы "-", "."
        key = key.replace('-', '_')
        key = key.replace('.', '_')
        self._data_dictionary[key] = value
        self.index += 1

    def get_data(self):
        return self._data_dictionary


class DateMixin(object):
    """
    Класс-примесь добавляет к классу ряд методов для вычисления различных дат.

    """

    LAST_ACADEMIC_DAY = 1
    LAST_ACADEMIC_MONTH = 9

    SEPTEMBER = 9
    AUGUST = 8

    @classmethod
    def get_desired_date(cls):
        """
        Последний день текущего учебного года
        LAST_ACADEMIC_DAY.LAST_ACADEMIC_MONTH.год

        """

        return cls.get_current_calendar_year_start()

    @classmethod
    def get_next_calendar_year_start(cls):
        """Возвращает след учебный год"""

        today = datetime.date.today()
        today_month = today.month

        if today_month < 9:
            last_day = datetime.date(today.year, cls.LAST_ACADEMIC_MONTH, cls.LAST_ACADEMIC_DAY)
        else:
            last_day = datetime.date(today.year + 1, cls.LAST_ACADEMIC_MONTH, cls.LAST_ACADEMIC_DAY)

        return last_day

    @classmethod
    def get_current_calendar_year_start(cls):
        """Возвращает текущий учебный год"""

        today = datetime.date.today()
        today_month = today.month

        if today_month < 9:
            last_day = datetime.date(today.year - 1, cls.LAST_ACADEMIC_MONTH, cls.LAST_ACADEMIC_DAY)
        else:
            last_day = datetime.date(today.year, cls.LAST_ACADEMIC_MONTH, cls.LAST_ACADEMIC_DAY)

        return last_day

    @classmethod
    def get_current_calendar_year_range(cls):
        """Период с 1.09.x - 31.08.x+1 для текущего учебного года."""

        today = datetime.date.today()
        today_month = today.month

        if today_month < 9:
            begin = datetime.date(today.year - 1, cls.SEPTEMBER, 1)
            end = datetime.date(today.year, cls.AUGUST, 31)
        else:
            begin = datetime.date(today.year, cls.SEPTEMBER, 1)
            end = datetime.date(today.year + 1, cls.AUGUST, 31)

        return begin, end

    @staticmethod
    def get_report_period():
        today = datetime.date.today()

        beg = datetime.date(today.year, 1, 1)
        end = datetime.date(today.year, today.month, today.day)

        return beg, end

    @classmethod
    def get_desired_period(cls):
        pass

    @classmethod
    def get_current_learn_year(cls):
        """
        Возвращает текущий учебный год [2.09.Y-31.08.(Y+1)]

        :return: текущий учебный год
        :rtype: date
        """
        today = datetime.date.today()
        today_month = today.month

        begin_period_year = today.year
        # Если ещё не сентябрь, то
        # 2.9.(Y-1) - 31.08.Y
        if today_month < cls.SEPTEMBER:
            begin_period_year = today.year - 1

        return (
            datetime.date(begin_period_year, cls.SEPTEMBER, 2),
            datetime.date(begin_period_year + 1, cls.AUGUST, 31),
        )

    @classmethod
    def get_current_calendar_year(cls):
        return datetime.date(datetime.date.today().year, 9, 1)

    @classmethod
    def get_next_calendar_year(cls):
        """Возвращает 1 января следующего календарного года"""

        cur_year = datetime.date.today().year
        return datetime.date(cur_year + 1, 1, 1)


class AgeDeltas(object):
    ACADEMIC_YEAR = 1
    CALENDAR_YEAR = 0

    _map = {
        # код: (количество лет, месяцев)
        '2_months': (0, 0),
        '6_months': (0, 6),
        '1_year': (1, 0),
        '1.5_year': (1, 6),
        '2_year': (2, 0),
        '2.5_year': (2, 6),
        '3_year': (3, 0),
        '3.5_year': (3, 6),
        '4_year': (4, 0),
        '4.5_year': (4, 6),
        '5_year': (5, 0),
        '5.5_year': (5, 6),
        '6_year': (6, 0),
        '6.5_year': (6, 6),
        '7_year': (7, 0),
        '7.5_year': (7, 6),
        '99_year': (99, 0),
    }

    _plane_category_map = {
        ALL: ('7.5_year', '2_months'),
        AGE_CATEGORIES_FULL['2-6-MONTHS']: ('6_months', '2_months'),
        AGE_CATEGORIES_FULL['0.5-1-YEARS']: ('1_year', '6_months'),
        AGE_CATEGORIES_FULL['1-1.5-YEARS']: ('1.5_year', '1_year'),
        AGE_CATEGORIES_FULL['1.5-2-YEARS']: ('2_year', '1.5_year'),
        AGE_CATEGORIES_FULL['2-2.5-YEARS']: ('2.5_year', '2_year'),
        AGE_CATEGORIES_FULL['2.5-3-YEARS']: ('3_year', '2.5_year'),
        AGE_CATEGORIES_FULL['3-3.5-YEARS']: ('3.5_year', '3_year'),
        AGE_CATEGORIES_FULL['3.5-4-YEARS']: ('4_year', '3.5_year'),
        AGE_CATEGORIES_FULL['4-4.5-YEARS']: ('4.5_year', '4_year'),
        AGE_CATEGORIES_FULL['4.5-5-YEARS']: ('5_year', '4.5_year'),
        AGE_CATEGORIES_FULL['5-5.5-YEARS']: ('5.5_year', '5_year'),
        AGE_CATEGORIES_FULL['5.5-6-YEARS']: ('6_year', '5.5_year'),
        AGE_CATEGORIES_FULL['6-6.5-YEARS']: ('6.5_year', '6_year'),
        AGE_CATEGORIES_FULL['6.5-7-YEARS']: ('7_year', '6.5_year'),
        AGE_CATEGORIES_FULL['7-7.5-YEARS']: ('7.5_year', '7_year'),
        AGE_CATEGORIES_FULL['7.5-99-YEARS']: ('99_year', '7.5_year'),
    }

    _plane_eight_category_map = {
        ALL: ('7.5_year', '2_months'),
        AGE_CATEGORIES_EIGHT['2-1-YEARS']: ('1_year', '2_months'),
        AGE_CATEGORIES_EIGHT['1-2-YEARS']: ('2_year', '1_year'),
        AGE_CATEGORIES_EIGHT['2-3-YEARS']: ('3_year', '2_year'),
        AGE_CATEGORIES_EIGHT['3-4-YEARS']: ('4_year', '3_year'),
        AGE_CATEGORIES_EIGHT['4-5-YEARS']: ('5_year', '4_year'),
        AGE_CATEGORIES_EIGHT['5-6-YEARS']: ('6_year', '5_year'),
        AGE_CATEGORIES_EIGHT['6-7-YEARS']: ('7_year', '6_year'),
        AGE_CATEGORIES_EIGHT['7-7.5-YEARS']: ('7.5_year', '7_year'),
    }

    _plane_cut_category_map = {
        AGE_CATEGORIES_CUT['2M-3YEARS']: ('3_year', '2_months'),
        AGE_CATEGORIES_CUT['3-5-YEARS']: ('5_year', '3_year'),
        AGE_CATEGORIES_CUT['5-7.5-YEARS']: ('7.5_year', '5_year'),
    }

    @classmethod
    def _get_age_deltas(cls, date, age_code):
        if callable(date):
            d = date()
        else:
            d = date

        years, months = cls._map[age_code]
        return d - relativedelta(years=years, months=months)

    @staticmethod
    def calculate_date():
        today = datetime.date.today()

        def calculate_academic_date():
            """
            Способ расчета возраста на текущий учебный год

            """

            return (
                datetime.date(today.year, 9, 1)
                if today >= datetime.date(today.year, 9, 1)
                else datetime.date(today.year - 1, 9, 1)
            )

        def calculate_calendar_date():
            """
            Способ расчета возраста на текущий календарный год

            """

            return datetime.date(today.year, 9, 1)

        if gisdo_settings.AGE_CALCULATION_DATE == AgeDeltas.CALENDAR_YEAR:
            date = calculate_calendar_date()
        elif gisdo_settings.AGE_CALCULATION_DATE == AgeDeltas.ACADEMIC_YEAR:
            date = calculate_academic_date()
        else:
            raise ApplicationLogicException('В конфигурациях неверно задан способ расчета возраста ребенка')

        return date

    @classmethod
    def get_category_deltas(cls, category_code, date_func):
        if category_code in cls._plane_category_map:
            down_border, up_border = cls._plane_category_map[category_code]
        elif category_code in cls._plane_cut_category_map:
            down_border, up_border = cls._plane_cut_category_map[category_code]
        else:
            down_border, up_border = cls._plane_eight_category_map[category_code]

        return (cls._get_age_deltas(date_func, down_border), cls._get_age_deltas(date_func, up_border))

    @classmethod
    def get_categories_borders(cls, category_code):
        """
        Метод возвращает границы возрастных категорий по коду категории.

        Возвращает кортеж их двух элементов.
        (нижняя граница=(количество лет, количество месяцев),
        верхняя граница=(количество лет, количество мясяцев))

        """

        if category_code in cls._plane_category_map:
            down_border, up_border = cls._plane_category_map[category_code]
        elif category_code in cls._plane_cut_category_map:
            down_border, up_border = cls._plane_cut_category_map[category_code]
        else:
            down_border, up_border = cls._plane_eight_category_map[category_code]

        return (cls._map[down_border], cls._map[up_border])


class UnitHelper(object):
    """
    Класс-помощник для работы с организациями при формировании ФО.

    """

    # Фильтр филиалов, которые учитываются в головной МО
    # (применим для модели FilialData):
    # статус должен быть "Подтвержден",
    # настройка у организации
    # "Не отправлять фед.отчетность" установлена в False (Нет),
    # организация не закрыта и имеет статус отличный от
    # ("Ликвидировано", "Закрыто", "Присоединена к другой организации")
    ALLOWED_FILIAL_FILTER = Q(status=FilialTypeStatus.APPROVE, filial__gisdo__not_on_federal_report=False) & Q(
        Q(filial__closed=False) & ~Q(filial__status__in=STATUSES_UNIT_EXCLUDE)
    )

    def __init__(self, report_main_unit):
        self._unit = report_main_unit

        # Признак того, является ли организация,
        # для которой формируется ФО, регионом.
        self.is_region = self._unit.kind.id == UnitKind.REGION

        # Муниципальные организации, по которым собирается отчет ФО.
        self._mo_iterable = self._get_high_level_units()

        # Словарь вида:
        # {mo_id: [dou]},
        # где mo_id - идентификатор МО,
        # [dou] - список организаций типа ДОУ для переданной МО.
        self._dou_units = dict([(mo.id, [r for r in self._get_list_dou(mo)]) for mo in self._mo_iterable])

        # Общее количество организаций, по которым собирается отчет ФО.
        # Смотрит организации-потомки типа (Регион, ДОУ, МО),
        # не включает себя в расчет количества.
        self._unit_count = (
            self._unit.get_descendants().filter(kind__id__in=(UnitKind.DOU, UnitKind.MO, UnitKind.REGION)).count()
        )

    def _get_high_level_units(self):
        """
        Возвращает список организаций типа МО,
        у которых есть вложенные организации типа ДОУ.

        Если после UnitHelper(unit) были изменения в дереве,
        их нужно подтянуть.

        :return: список организаций
        :rtype: QuerySet

        """

        self._unit = Unit.objects.get(id=self._unit.id)

        unit_data = Unit.objects.raw(
            'select * '
            'from unit '
            'join (select unit.id, count(t1.id) as count_1'
            '      from unit'
            '      join (select id, lft, rght, tree_id'
            '            from unit'
            '            where kind_id=%s) as t1'
            '      on t1.lft >= unit.lft and'
            '               t1.rght <= unit.rght and'
            '               t1.tree_id = unit.tree_id'
            '      where unit.kind_id = %s'
            '      group by unit.id) as t2 '
            'on t2.id = unit.id '
            'where t2.count_1 > 0 and unit.lft >= %s and'
            '                         unit.rght <= %s and'
            '                         unit.tree_id = %s'
            % (UnitKind.DOU, UnitKind.MO, self._unit.lft, self._unit.rght, self._unit.tree_id)
        )

        return unit_data

    @staticmethod
    def _get_list_dou(unit):
        """
        Возвращает список ДОУ переданной организации.

        Если переданная организация имеет тип МО,
        то для нее выполняется формирование списка ДОУ + сама МО
        (тоже включается в список).

        Если тип отличается от МО, то формируется список из одной организации,
        которая была передана.

        :param unit: инстанс организации
        :type unit: Unit


        :return: список организаций
        :rtype: List[Unit]

        """

        if unit.kind.id == UnitKind.MO:
            # Фильтр для отбора допустимых организаций
            # для последующей фильтрации:
            # Тип организации ДОУ,
            # настройка у организации
            # "Не отправлять фед.отчетность" установлена в False (Нет),
            # организация не закрыта и имеет статус отличный от
            # ("Ликвидировано", "Закрыто", "Присоединена к другой организации")
            allowed_dou_filter = (
                Q(kind__id=UnitKind.DOU)
                & Q(gisdo__not_on_federal_report=False)
                & Q(closed=False)
                & ~Q(status__in=STATUSES_UNIT_EXCLUDE)
            )

            # ДОУ с заполненным полем "Относится к МО"
            # должны попадать в ФО в рамках него,
            # а не в родительский по дереву.
            dou_related_to_mo = Unit.objects.filter(Q(allowed_dou_filter) & Q(gisdo__related_to_mo=unit))

            result = (
                unit.get_descendants(include_self=True)
                .filter(allowed_dou_filter)
                .filter(
                    # Исключает организации,
                    # которые имеет запоненное поле "Относится к МО".
                    # Для предотвращения появления дублей и
                    # сторонних ДОУ, которые относятся к другой организации,
                    # а не к текущей.
                    Q(gisdo__related_to_mo__isnull=True)
                )
                .filter(
                    # Обычная организация и головная организация.
                    Q(filial__isnull=True)
                    # Не закрытые филиалы, с не закрытой головной организацией
                    | Q(filial__isnull=False, filial__status=FilialTypeStatus.UNKNOWN)
                )
                | dou_related_to_mo
            ).order_by('kind__id')

        else:
            result = [unit]

        return result

    @staticmethod
    def get_filial(unit):
        """
        Функция возвращает филиалы организации пригодные для отправки.

        Для текущей организации выполняет поиск филиалов
        статус должен быть "Подтвержден",
        настройка у организации "Не отправлять фед.отчетность" установлена
        в False (Нет), организация не закрыта и имеет статус отличный от
        ("Ликвидировано", "Закрыто", "Присоединена к другой организации"),
        должны быть фактические группы.

        :param unit: инстанс организации
        :type unit: Unit

        :return: список организаций (филиалов)
        :rtype: QuerySet

        """

        filial_data = FilialData.objects.filter(Q(head=unit) & Q(UnitHelper.ALLOWED_FILIAL_FILTER)).values_list(
            'filial_id', flat=True
        )

        units_with_groups = (
            Group.objects.values('unit')
            .annotate(cnt=Sum('id'))
            .filter(status=GroupStatusEnum.FACT, unit_id__in=filial_data, cnt__gt=0)
            .values_list('unit_id', flat=True)
        )

        return Unit.objects.filter(id__in=units_with_groups)

    def get_main_unit(self):
        """
        Возвращает организацию, по которой формируется ФО.

        :return: возвращает инстанс организации
        :rtype: Unit

        """

        return self._unit

    def get_report_units(self):
        """
        Возвращает Муниципальные организации (МО), по которым собирается ФО.

        :return: список организаций
        :rtype: QuerySet

        """

        return self._mo_iterable

    def get_mo_units(self, mo):
        """
        Возвращает организации типа ДОУ для заданного МО.
        Если МО не найдено в словаре, возвращает пустой список.

        :param mo: организация типа МО
        :type mo: Unit

        :return: список организаций
        :rtype: QuerySet

        """

        return self._dou_units[mo] if mo in self._dou_units else []


def get_report_date_or_today(report_start_date=None):
    """
    Возвращает дату сборки отчета гисдо, либо если эта дата не переданна,
    то текущий день. Т.к. некоторые теги расчитываются в момент отправки
    (например enrolled, add_cont, reduction_other и т.д.), то для них берется
    дата сборки, для других показателей будет использованна
    текущая дата (т.е. фактическая дата сборки).

    :param report_start_date: дата сборки отчета
    :type report_start_date: datetime.date
    :return: дата
    :rtype: datetime.date

    """

    return report_start_date or datetime.date.today()


def get_file_url(model_record, field_name):
    """
    Формирование URL для получения файла.

    :param model_record: Экземпляр записи модели.
    :param field_name: Имя поля модели в котором храниться файл

    """

    file_ = getattr(model_record, field_name, None)

    if file_ is None or not file_:
        return 'нет'

    return urljoin(settings.SYSTEM_SITE_ADDRESS, file_.url)


class GisdoJsonEncoder(JSONEncoder):
    """Дампит дополнительные классы для отчета."""

    def default(self, obj):
        from gisdo.index.queue import (
            AverageWaitingTimeWrapper,
        )

        if isinstance(obj, AverageWaitingTimeWrapper):
            return str(obj)

        return super(GisdoJsonEncoder, self).default(obj)


def reset_metric_values(metric, reset_value=None):
    """
    Сброс значений показателя.

    :param reset_value: новое значение
    :type reset_value: object

    :param metric: словарь, значения которого необходимо обновить
    :type metric: dict

    :return: None

    """

    for k, v in metric.items():
        metric[k] = reset_value


def try_date_in_string(date_or_none):
    """
    Проверяет, если входящее значение дата, то
    возвращает текстовое представление в формате %d.%m.%Y, иначе пустую строку.

    :param date_or_none: дата
    :type date_or_none: Optional[datetime]

    :return: текстовое представление даты или пустая строка
    :rtype: str

    """

    return date_or_none.strftime('%d.%m.%Y') if isinstance(date_or_none, datetime.date) else ''


def merge_unical_data_in_lists(
    *data_lists: List[Union[list, tuple]],
    unical_data_index: int = 0,
) -> List[Union[list, tuple]]:
    """Собирает данные из всех списков в один список, оставляя только
    уникальные данные

    :param data_lists: Списки с данных - списки со списками/кортежами
    :param unical_data_index: Индекс во внутренних списках/кортежах, в которых
        содержится элемент, по которому сравнивают уникальность
        (например, id ребенка)

    :return: Список с уникальными данными из всех списков
    """

    final_data = []
    unical_ids = set()

    for data_list in data_lists:
        for row_data in data_list:
            row_id = row_data[unical_data_index]
            if row_id not in unical_ids:
                final_data.append(row_data)
                unical_ids.add(row_id)

    return final_data


def get_ordered_dict_of_ordered_dicts(keys):
    """
    Создание OrderedDict с указанными ключами, в которых будут находиться
    пустые OrderedDict

    :param keys: Ключи для словаря
    :type keys: Iterable[str]

    :return: OrderedDict с указанными ключами, где значения - пустые OrderedDict
    :rtype: Dict[str, dict]
    """
    return OrderedDict([(key, OrderedDict()) for key in keys])


def get_ordered_dict_of_dicts(keys):
    """
    Создание OrderedDict с указанными ключами, в которых будут находиться
    пустые словари

    :param keys: Ключи для словаря

    :return: Dict[str, dict]
    """
    return OrderedDict([(key, {}) for key in keys])


def set_zero_values(data, indexes, age_cat):
    """Установка нулей для индексов в словаре для возрастной категории.

    :param data: Словарь с данными
    :type data: dict
    :param indexes: Индексы для установки нулей
    :type indexes: Iterable[str]
    :param age_cat: Возрастная категория
    :type data: str
    """
    for index_name in indexes:
        data[index_name][age_cat] = 0


def set_empty_list_values(data, indexes, age_cat):
    """
    Установка пустых списков для индексов в словаре для возрастной категории.

    :param data: Словарь с данными
    :type data: dict
    :param indexes: Индексы для установки пустых список
    :type indexes: Iterable[str]
    :param age_cat: Возрастная категория
    :type data: str
    """
    for index_name in indexes:
        data[index_name][age_cat] = []


def has_federal_report_permission(request: Any, permission_code: str) -> bool:
    """Проверяет права для работы Фед. отчетностью

    :param request: Request
    :param permission_code: Тип права, который надо проверить
    :return: Право есть
    """
    gisdo_pack = ControllerCache.find_pack('gisdo.actions.ReportFormActionPack')
    permission_to_check = getattr(gisdo_pack, permission_code)

    return gisdo_pack and gisdo_pack.has_perm(request, permission_to_check)
