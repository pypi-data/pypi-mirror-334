import datetime
from collections import (
    OrderedDict,
    defaultdict,
)
from functools import (
    partial,
)
from itertools import (
    chain,
)

from kinder.core.children.models import (
    Children,
)
from kinder.core.dict.models import (
    GroupTypeEnumerate,
    UnitKind,
)
from kinder.core.group.models import (
    Group,
    GroupStatusEnum,
)
from kinder.core.helpers import (
    get_instance,
)
from kinder.core.unit.models import (
    Unit,
)

from gisdo import (
    constants as const,
    xml_helpers,
)
from gisdo.alchemy_session import (
    session_scope,
)
from gisdo.algorithm.direct import (
    get_32_filter,
    get_321_filter,
    get_322_filter,
    get_children_last_direct_ids,
)
from gisdo.algorithm.enrolled import (
    get_22_8_x_index,
    get_22_index,
    get_22_x_index,
    get_26_index,
    get_27_index,
    get_28_index,
    get_30_1_index,
    get_30_2_index,
    get_30_index,
)
from gisdo.exceptions import (
    NoDataInMo,
)
from gisdo.index import (
    ApplicationIndex,
    get_enrolled_age_filter,
    get_queue_index_collection,
)
from gisdo.index.capacities import (
    childrens_in_age_category,
)
from gisdo.index.direct import (
    DirectIndex,
    ind_19_3,
    ind_29_1,
    ind_29_2,
    ind_29_3,
)
from gisdo.index.enrolled import (
    Index,
    get_age_for_date_filter,
)
from gisdo.models import (
    ScheduleSettings,
)
from gisdo.service import (
    FilialGroupData,
    GroupData,
    ParentGroupData,
    TemplateView,
)
from gisdo.utils import (
    DateMixin,
    get_ordered_dict_of_dicts,
    set_empty_list_values,
)
from gisdo.xml_helpers import (
    get_detailed_passport,
)

from ..algorithm.utils import (
    HealthNeedIdsProvider,
)
from ..collector import (
    DataCollector,
)
from ..constants import (
    AGE_CATEGORIES_EIGHT,
)
from ..index import (
    get_queue_index,
)
from ..index.queue import (
    get_age_filter,
    get_average_waiting_time,
    get_count,
)
from .constants import *
from .helpers import (
    ReportQuery,
    get_count_data,
    prep_directs_in_group_queries,
    prep_in_29_2_data,
    prep_ind_19_3_queries,
    prep_ind_29_1_queries,
    prep_ind_29_2_query,
    prep_ind_29_3_query,
    prep_ind_enrolled_data,
    prepare_31_x_index,
    prepare_direct_index_queries,
    prepare_enrolled_index_queries,
)


class ReportDataCollector(DataCollector):
    """Сборщик данных отчета "Выгрузка детей по показателю/тегу"."""

    # Название в словаре self._cache для данных о выгружаемых в xml тегах
    XML_TAGS = 'xml_tags'
    XML_TAGS_BY_GROUP = 'xml_tags_by_group'
    QUEUE_8 = 'queue_8'
    XML_TAGS_BY_GROUP_ONLY_VALUES = 'xml_tags_by_group_only_values'
    REPORT_APPLICATIONS = 'report_applications'

    def __init__(self, mo, unit_helper, report_start_date, indexes=None):
        super().__init__(mo, unit_helper, report_start_date)

        self.indexes = indexes or []
        self._cache[self.XML_TAGS] = {}
        self._cache[self.XML_TAGS_BY_GROUP] = {}
        self._cache[self.QUEUE_8] = {}
        self._cache[self.XML_TAGS_BY_GROUP_ONLY_VALUES] = {}
        self._cache[self.REPORT_APPLICATIONS] = {}

    def collect(self, report_form=None):
        # Признак наличия садов по которым можно собрать данные
        dou_list = self._unit_helper.get_mo_units(self._mo.id)
        have_data = len(dou_list)

        if not have_data:
            raise NoDataInMo(f'Нет садов в МО {self._mo} пригодных для отправки')

        # Для расчета показателя 32 и 32.1, 32.2, необходим список
        # идентификаторов последних направлений у ребенка в рамках МО
        if INDEX_32 in self.indexes:
            self.list_last_id_directs_32 = get_children_last_direct_ids(
                self._mo.id, self._report_start_date, get_32_filter()
            )
        if INDEX_32_1 in self.indexes:
            self.list_last_id_directs_321 = get_children_last_direct_ids(
                self._mo.id, self._report_start_date, get_321_filter()
            )
        if INDEX_32_2 in self.indexes:
            self.list_last_id_directs_322 = get_children_last_direct_ids(
                self._mo.id, self._report_start_date, get_322_filter()
            )

        group_data = dict()

        # Собираем по ДОУ
        for dou in dou_list:
            self._collect_applications_data(dou)
            self._collect_enrolled_data(dou)
            self._collect_capacities(dou)
            self._collect_8_queue(dou)

            filials = xml_helpers.get_dou_filials(dou.get_mo()).select_related('filial')

            parent_group_data = ParentGroupData(
                dou.get_mo(), self._report_start_date, filials, prep_enrollments_func=prep_ind_enrolled_data
            )

            filial_group_data = FilialGroupData(
                dou, parent_group_data, self._report_start_date, prep_enrollments_func=prep_ind_enrolled_data
            )

            group_data[dou.id] = list(filial_group_data.groups)

        self._update_cache(group_data, self.CAPACITIES)
        if self.has_selected_index(XML_TAGS):
            (xml_tags_data, xml_tags_data_by_group, xml_tags_data_by_group_only_values) = self._calculate_xml_tags(
                report_form
            )

            self._cache[self.XML_TAGS] = xml_tags_data
            self._cache[self.XML_TAGS_BY_GROUP] = xml_tags_data_by_group
            self._cache[self.XML_TAGS_BY_GROUP_ONLY_VALUES] = xml_tags_data_by_group_only_values

        return self._cache

    @staticmethod
    def _merge_dicts(first_dict, second_dict):
        if not first_dict or not second_dict:
            return

        first_dou_id = list(first_dict.keys())[0]
        second_dou_id = list(second_dict.keys())[0]

        for index, first_index_dict in first_dict[first_dou_id].items():
            second_index_dict = second_dict[second_dou_id][index]
            age_categories = set(first_index_dict.keys()) | set(second_index_dict.keys())

            for age_cat in age_categories:
                if age_cat not in second_index_dict:
                    continue

                data = second_index_dict[age_cat]
                if age_cat in first_index_dict:
                    if isinstance(first_index_dict[age_cat], dict) and isinstance(data, dict):
                        first_index_dict[age_cat].extend(data)
                    else:
                        first_index_dict[age_cat] += data
                else:
                    if isinstance(data, dict):
                        first_index_dict[age_cat] = data.copy()
                    else:
                        first_index_dict[age_cat] = data

    def get_enrolled_data(self, collection, age_filter):
        """Фильтрация данных по тегу"""

        data = [data for data in collection if age_filter(*data)]

        return data

    def get_enrolled_index_data(self, _unit, report_start_date):
        """Получение данных для тега enrolled"""

        full_enrolled_data = defaultdict(list)

        filials = xml_helpers.get_dou_filials(_unit).select_related('filial')

        parent_group_data = ParentGroupData(
            _unit, report_start_date, filials, prep_enrollments_func=prep_ind_enrolled_data
        )

        # головная организация передается только если у нее есть группы
        if xml_helpers.has_fact_groups(_unit):
            for parent_group in Group.objects.filter(status=GroupStatusEnum.FACT, unit=_unit).order_by('id'):
                age_from, age_to = GroupData.get_age_range(parent_group)
                age_cat = f'от {int(age_from)} до {int(age_to)} лет'

                enrolled = parent_group_data.get_enrollments_count(
                    parent_group, prep_enrollments_func=prep_ind_enrolled_data
                )

                full_enrolled_data[age_cat].extend(enrolled)

        for filial in (fd.filial for fd in filials.iterator()):
            # филиал передается только если у него есть группы
            if xml_helpers.has_fact_groups(filial):
                filial_group_data = FilialGroupData(
                    filial, parent_group_data, report_start_date, prep_enrollments_func=prep_ind_enrolled_data
                )

                for filial_group in Group.objects.filter(status=GroupStatusEnum.FACT, unit=_unit).order_by('id'):
                    age_from, age_to = GroupData.get_age_range(filial_group)
                    age_cat = f'от {int(age_from)} до {int(age_to)} лет'

                    enrolled = filial_group_data.get_enrollments_count(
                        filial_group, prep_enrollments_func=prep_ind_enrolled_data
                    )

                    full_enrolled_data[age_cat].extend(enrolled)

        return full_enrolled_data

    def has_selected_index(self, indexes):
        """Проверяет, был ли выбран хотя бы один из указанных индексов

        :param indexes: Названия индексов для проверки
        :type indexes: Iterable

        :return: Был ли выбран хотя бы один из указанных индексов для отчёта
        :rtype: bool
        """
        return any(index in self.indexes for index in indexes)

    def _collect_enrolled_data(self, dou):
        def _inner(_dou, report_start_date, calc_filial=False):
            enrolled_indexes = (
                INDEX_ENROLLED,
                INDEX_7,
                INDEX_7_1,
                INDEX_7_2,
                INDEX_7_3,
                INDEX_7_4,
                INDEX_7_5,
                INDEX_7_6,
                INDEX_7_7,
                INDEX_8,
                INDEX_8_1,
                INDEX_8_2,
                INDEX_8_3,
                INDEX_9,
                INDEX_9_1,
                INDEX_10,
                INDEX_10_1,
                INDEX_11,
                INDEX_12,
                INDEX_12_1,
                INDEX_13,
                INDEX_13_1,
                INDEX_14,
                INDEX_15,
                INDEX_16,
                INDEX_17,
                INDEX_17_1,
                INDEX_18,
                INDEX_18_1,
                INDEX_18_2,
                INDEX_18_3,
                INDEX_18_4,
                INDEX_18_5,
                INDEX_19,
                INDEX_19_1,
                INDEX_19_2,
                INDEX_19_3,
                INDEX_20,
                INDEX_20_1,
                INDEX_20_2,
                INDEX_20_3,
                INDEX_20_4,
                INDEX_20_5,
                INDEX_20_6,
                INDEX_20_7,
                INDEX_20_8,
                INDEX_21,
                INDEX_22,
                INDEX_22_1,
                INDEX_22_1_1,
                INDEX_22_1_2,
                INDEX_22_2,
                INDEX_22_3,
                INDEX_22_3_1,
                INDEX_22_3_2,
                INDEX_22_4,
                INDEX_22_5,
                INDEX_22_5_1,
                INDEX_22_5_2,
                INDEX_22_6,
                INDEX_22_7,
                INDEX_22_8,
                INDEX_22_8_1,
                INDEX_22_8_2,
                INDEX_23,
                INDEX_24,
                INDEX_25,
                INDEX_26,
                INDEX_27,
                INDEX_28,
                INDEX_29,
                INDEX_29_1,
                INDEX_29_2,
                INDEX_29_3,
                INDEX_30,
                INDEX_30_1,
                INDEX_30_2,
                INDEX_31,
                INDEX_32,
                INDEX_32_1,
            )
            enrolled = {_dou.id: get_ordered_dict_of_dicts(enrolled_indexes)}
            dou_enrolled = enrolled[_dou.id]

            def chain_dou_enrolled(_indexes_22, _on_date_enrolled_filter, *indexes):
                """Объединение различных показателей для dou_enrolled."""
                return list(
                    chain.from_iterable(
                        self.get_enrolled_data(_indexes_22[_ind], _on_date_enrolled_filter) for _ind in indexes
                    )
                )

            if INDEX_ENROLLED in self.indexes:
                ind_enrolled_data = self.get_enrolled_index_data(_dou, report_start_date)
                if ind_enrolled_data:
                    dou_enrolled[INDEX_ENROLLED] = ind_enrolled_data

            enrolled_index = Index(_dou, report_start_date)
            prepared_enrolled_index = partial(
                enrolled_index,
                prep_enrolled_func=prepare_enrolled_index_queries,
            )

            if INDEX_29_1 in self.indexes:
                index_29_1 = ind_29_1(_dou, self._report_start_date, prep_func=prep_ind_29_1_queries)

            queue_indexes = {}

            for index in QUEUE_INDEXES:
                if index in self.indexes:
                    params = QUEUE_INDEXES_PARAMS.get(index, {})

                    index_param = index
                    if index == INDEX_7_6:
                        index_param = INDEX_7_5

                    queue_indexes[index] = get_queue_index_collection(index_param, _dou, report=True, **params)

            if INDEX_10 in self.indexes or INDEX_9 in self.indexes or (INDEX_9_1 in self.indexes):
                dou_enrolled[INDEX_10][const.ALL] = 0
                index_10 = get_queue_index_collection(INDEX_10, _dou)
            if INDEX_10_1 in self.indexes:
                index_10_1 = get_queue_index_collection(INDEX_10_1, _dou)
            if INDEX_11 in self.indexes or INDEX_9 in self.indexes or (INDEX_9_1 in self.indexes):
                dou_enrolled[INDEX_11][const.ALL] = 0
                index_11 = get_queue_index_collection(INDEX_11, _dou)

            if INDEX_29_2 in self.indexes:
                index_29_2 = ind_29_2(_dou, prep_func=prep_ind_29_2_query)

            if INDEX_29_3 in self.indexes:
                index_29_3 = ind_29_3(_dou, prep_func=prep_ind_29_3_query)

            if not calc_filial:
                if self.has_selected_index([INDEX_19, INDEX_19_1, INDEX_19_2]):
                    index_19 = list(prepared_enrolled_index())

                if INDEX_21 in self.indexes:
                    index_21 = list(
                        prepared_enrolled_index(
                            group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.FAMILY)
                        )
                    )

                # Формирование множества с показателям для расчёта (22.х).
                # Связано с тем, что могут быть выбраны не все показатели
                calc_indexes_22 = {i for i in const.SIMPLE_INDEXES_22 if i in self.indexes}
                # Добавление показателей для расчёта показателей с суммой
                for main_index, sum_indexes in const.SUM_INDEXES_22.items():
                    if main_index in self.indexes:
                        for dop_index in sum_indexes:
                            calc_indexes_22.add(dop_index)

                # Индексы для расчёта показателей 22.х
                indexes_22 = {}
                for ind in calc_indexes_22:
                    if ind == INDEX_22:
                        indexes_22[ind] = get_22_index(prepared_enrolled_index)
                        continue

                    hn = HealthNeedIdsProvider.get_health_need(ind)
                    if ind == INDEX_22_8_1:
                        indexes_22[ind] = get_22_8_x_index(
                            enrolled_index=prepared_enrolled_index,
                            health_need_list=hn,
                            children_filter='fed_report_exclude_for_22_8_1',
                        )
                    elif ind == INDEX_22_8_2:
                        indexes_22[ind] = get_22_8_x_index(
                            enrolled_index=prepared_enrolled_index,
                            health_need_list=hn,
                            children_filter='fed_report_exclude_for_22_8_2',
                        )
                    else:
                        indexes_22[ind] = get_22_x_index(prepared_enrolled_index, hn)

                if INDEX_23 in self.indexes:
                    index_23 = list(
                        prepared_enrolled_index(
                            group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.COMP)
                        )
                    )

                if INDEX_24 in self.indexes:
                    index_24 = list(
                        prepared_enrolled_index(
                            group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.HEALTH)
                        )
                    )

                if INDEX_25 in self.indexes:
                    index_25 = list(
                        prepared_enrolled_index(
                            group_filter=lambda group: (
                                group.type
                                and (
                                    group.type.code == GroupTypeEnumerate.CARE
                                    or group.type.code == GroupTypeEnumerate.YOUNG
                                )
                            )
                        )
                    )

                if INDEX_26 in self.indexes:
                    index_26 = get_26_index(prepared_enrolled_index)

                if INDEX_27 in self.indexes:
                    index_27 = get_27_index(prepared_enrolled_index)

                if INDEX_28 in self.indexes:
                    index_28 = get_28_index(prepared_enrolled_index)

                if INDEX_30 in self.indexes:
                    index_30 = get_30_index(prepared_enrolled_index)

                if INDEX_30_1 in self.indexes:
                    index_30_1 = get_30_1_index(prepared_enrolled_index)

                if INDEX_30_2 in self.indexes:
                    index_30_2 = get_30_2_index(prepared_enrolled_index)

            for age_cat in list(const.AGE_CATEGORIES_FULL.values()):
                current_year_first_september = get_age_filter(
                    age_cat,
                    DateMixin.get_current_calendar_year(),
                )
                current_year_enrolled_filter = get_enrolled_age_filter(age_cat, DateMixin.get_current_calendar_year())
                on_date_enrolled_filter = get_enrolled_age_filter(age_cat, datetime.date.today)
                next_calendar_year_enrolled = get_enrolled_age_filter(age_cat, DateMixin.get_next_calendar_year)
                on_other_date_age_filter = get_age_for_date_filter(age_cat)

                next_year_first_day = get_age_filter(
                    age_cat,
                    datetime.date(datetime.date.today().year + 1, 1, 1),
                )
                next_learn_year_first_day = get_age_filter(age_cat, DateMixin.get_next_calendar_year_start())
                on_date_filter = get_age_filter(age_cat, datetime.date.today)
                # Общая численность детей зачисленных в ДОО
                if not calc_filial:
                    if INDEX_19 in self.indexes:
                        ind_19_data = self.get_enrolled_data(index_19, current_year_enrolled_filter)
                        if ind_19_data:
                            dou_enrolled[INDEX_19][age_cat] = ind_19_data

                    if INDEX_19_1 in self.indexes:
                        ind_19_1_data = self.get_enrolled_data(index_19, on_date_enrolled_filter)
                        if ind_19_1_data:
                            dou_enrolled[INDEX_19_1][age_cat] = ind_19_1_data

                    if INDEX_19_2 in self.indexes:
                        ind_19_2_data = self.get_enrolled_data(index_19, next_calendar_year_enrolled)
                        if ind_19_2_data:
                            dou_enrolled[INDEX_19_2][age_cat] = ind_19_2_data

                if INDEX_19_3 in self.indexes:
                    ind_19_3_children_ids = ind_19_3(
                        _dou, report_start_date, age_range=age_cat, prep_direct_func=prep_ind_19_3_queries
                    )
                    ind_19_3_data = ReportQuery.get_child_query(Children.objects.filter(id__in=ind_19_3_children_ids))
                    if ind_19_3_data:
                        dou_enrolled[INDEX_19_3][age_cat] = list(ind_19_3_data)

                # Общая численность детей, зачисленных в группы для
                # детей с ограниченными возможностями здоровью
                if not calc_filial:
                    if INDEX_21 in self.indexes:
                        dou_enrolled[INDEX_21][age_cat] = self.get_enrolled_data(index_21, on_date_enrolled_filter)

                    # Подсчёт показателей 22.х
                    for ind in const.SIMPLE_INDEXES_22:
                        if ind not in self.indexes:
                            continue
                        dou_enrolled[ind][age_cat] = self.get_enrolled_data(indexes_22[ind], on_date_enrolled_filter)

                    for main_index, dop_indexes in const.SUM_INDEXES_22.items():
                        if main_index not in self.indexes:
                            continue
                        # Может быть выбран только составной индекс, тогда
                        # нужно подсчитать его суммирующие нидексы
                        dou_enrolled[main_index][age_cat] = chain_dou_enrolled(
                            indexes_22, on_date_enrolled_filter, *dop_indexes
                        )
                else:
                    set_empty_list_values(
                        dou_enrolled,
                        (INDEX_21, *const.SIMPLE_INDEXES_22, *list(const.SUM_INDEXES_22.keys())),
                        age_cat,
                    )

                # Общее количество детей зачисленных в
                # оздоровительные и компенсирующие группы
                if not calc_filial:
                    if INDEX_23 in self.indexes:
                        dou_enrolled[INDEX_23][age_cat] = self.get_enrolled_data(index_23, on_date_enrolled_filter)
                    if INDEX_24 in self.indexes:
                        dou_enrolled[INDEX_24][age_cat] = self.get_enrolled_data(index_24, on_date_enrolled_filter)
                    if INDEX_25 in self.indexes:
                        dou_enrolled[INDEX_25][age_cat] = self.get_enrolled_data(index_25, on_date_enrolled_filter)

                    if INDEX_26 in self.indexes:
                        # Общая численность детей, зачисленных в
                        # группы круглосуточного пребывания детей
                        dou_enrolled[INDEX_26][age_cat] = self.get_enrolled_data(index_26, on_date_enrolled_filter)

                    if INDEX_27 in self.indexes:
                        # Общая численность детей, зачисленных в группы
                        # кратковременного пребывания детей
                        dou_enrolled[INDEX_27][age_cat] = self.get_enrolled_data(index_27, on_date_enrolled_filter)

                    # Общая численность детей, посещающих ДОО в режиме
                    # кратковременного пребывания
                    if INDEX_28 in self.indexes:
                        dou_enrolled[INDEX_28][age_cat] = self.get_enrolled_data(index_28, on_date_enrolled_filter)
                else:
                    set_empty_list_values(
                        dou_enrolled, (INDEX_23, INDEX_24, INDEX_25, INDEX_26, INDEX_27, INDEX_28), age_cat
                    )

                if not calc_filial:
                    if INDEX_30 in self.indexes:
                        dou_enrolled[INDEX_30][age_cat] = self.get_enrolled_data(index_30, on_date_enrolled_filter)

                    if INDEX_30_1 in self.indexes:
                        dou_enrolled[INDEX_30_1][age_cat] = self.get_enrolled_data(index_30_1, on_date_enrolled_filter)

                    if INDEX_30_2 in self.indexes:
                        dou_enrolled[INDEX_30_2][age_cat] = self.get_enrolled_data(index_30_2, on_date_enrolled_filter)
                else:
                    set_empty_list_values(dou_enrolled, (INDEX_30, INDEX_30_1, INDEX_30_2), age_cat)

                if INDEX_29_1 in self.indexes:
                    ind_29_1_data = self.get_enrolled_data(index_29_1, on_date_enrolled_filter)
                    if ind_29_1_data:
                        dou_enrolled[INDEX_29_1][age_cat] = ind_29_1_data

                if INDEX_29_2 in self.indexes:
                    index_29_2_data = self.get_enrolled_data(index_29_2, on_other_date_age_filter)
                    if index_29_2_data:
                        dou_enrolled[INDEX_29_2][age_cat] = prep_in_29_2_data(index_29_2_data)

                if INDEX_29_3 in self.indexes:
                    index_29_3_data = self.get_enrolled_data(index_29_3, next_calendar_year_enrolled)
                    if index_29_3_data:
                        dou_enrolled[INDEX_29_3][age_cat] = index_29_3_data

                for index in QUEUE_INDEXES:
                    if index in self.indexes:
                        if index in (INDEX_18, INDEX_7):
                            dou_enrolled[index][age_cat] = get_count_data(
                                queue_indexes[index], current_year_first_september
                            )
                        elif index in (INDEX_7_6, INDEX_7_7):
                            dou_enrolled[index][age_cat] = get_count_data(
                                queue_indexes[index], next_learn_year_first_day
                            )
                        elif index == INDEX_18_2:
                            dou_enrolled[INDEX_18_2][age_cat] = get_count_data(
                                queue_indexes[index], next_year_first_day
                            )
                        else:
                            dou_enrolled[index][age_cat] = get_count_data(queue_indexes[index], on_date_filter)

                if INDEX_9 in self.indexes:
                    dou_enrolled[INDEX_9][age_cat] = get_count_data(
                        index_10, current_year_first_september
                    ) + get_count_data(index_11, current_year_first_september)
                if INDEX_10_1 in self.indexes:
                    dou_enrolled[INDEX_10_1][age_cat] = get_count_data(index_10_1, on_date_filter)

                # Количество детей в очереди имеющих право зачисления
                # на основе федеральных и региональных льгот.
                if INDEX_10 in self.indexes or INDEX_9_1 in self.indexes:
                    current_10_value = get_count(index_10, on_date_filter)
                    dou_enrolled[INDEX_10][const.ALL] += current_10_value

                if INDEX_11 in self.indexes or INDEX_9_1 in self.indexes:
                    current_11_value = get_count(index_11, on_date_filter)
                    dou_enrolled[INDEX_11][const.ALL] += current_11_value

                if INDEX_9_1 in self.indexes:
                    index_9_1_value = current_10_value + current_11_value

                    if index_9_1_value:
                        dou_enrolled[INDEX_9_1][age_cat] = [('', '', index_9_1_value, '', '')]

            for index in [INDEX_10, INDEX_11]:
                if index in self.indexes or INDEX_9_1 in self.indexes:
                    index_value = dou_enrolled[index][const.ALL]

                    if not index_value:
                        del dou_enrolled[index][const.ALL]
                    else:
                        dou_enrolled[index][const.ALL] = [('', '', index_value, '', '')]

            # Общее количество детей зачисленных в семейные,
            # оздоровительные и компенсирующие группы
            if not calc_filial and INDEX_29 in self.indexes:
                ind_29_data = list(prepared_enrolled_index(query_filter='predictable_decrease_contingent'))

                if ind_29_data:
                    dou_enrolled[INDEX_29][const.ALL] = ind_29_data

            return enrolled

        enrolled_data = _inner(dou, self._report_start_date)

        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_enrolled = _inner(filial, self._report_start_date, calc_filial=True)

            self._merge_dicts(enrolled_data, filial_enrolled)

        self._update_cache(enrolled_data, self.ENROLLED)

        return enrolled_data

    def _collect_8_queue(self, dou):
        queue_8 = {INDEX_8: {}, INDEX_8_1: {}, INDEX_8_2: {}, INDEX_8_3: {}}

        for index in set(QUEUE_INDEXES_ONLY_VALUES) & set(self.indexes):
            queue_data = get_queue_index_collection(index, dou, report=True)
            for age_cat in AGE_CATEGORIES_EIGHT.values():
                queue_8[index][age_cat] = get_average_waiting_time(queue_data, age_cat)
        self._cache[self.QUEUE_8][dou] = queue_8

    def _collect_capacities(self, dou):
        def _inner(_dou, report_start_date, calc_filial=True):
            _capacities = {
                _dou.id: OrderedDict(
                    [
                        (INDEX_31, {}),
                        (INDEX_31_1, {}),
                        (INDEX_31_2, {}),
                        (INDEX_31_3, {}),
                        (INDEX_31_4, {}),
                        (INDEX_32, {}),
                        (INDEX_32_1, {}),
                        (INDEX_32_2, {}),
                        (INDEX_33, {}),
                    ]
                )
            }
            dou_capacities = _capacities[_dou.id]

            if not self.has_selected_index(dou_capacities.keys()):
                return _capacities

            common = []
            short_stay = []
            with_hn = []
            compensating = []
            health_group = []

            # Подситываем свободные места в группах, только если
            # выбран один из показателей 31.x
            if calc_filial and any(set(INDEXES_31_x) & set(self.indexes)):
                common, short_stay, with_hn, compensating, health_group = self.get_free_spaces_by_group(
                    _dou, report_start_date, prep_function=(prepare_31_x_index)
                )

            if INDEX_31 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_EIGHT.values()):
                    if calc_filial:
                        dou_capacities[INDEX_31][age_cat] = childrens_in_age_category(common, age_cat)
                    else:
                        dou_capacities[INDEX_31][age_cat] = []

            if INDEX_31_1 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_EIGHT.values()):
                    if calc_filial:
                        dou_capacities[INDEX_31_1][age_cat] = childrens_in_age_category(with_hn, age_cat)
                    else:
                        dou_capacities[INDEX_31_1][age_cat] = []

            if INDEX_31_2 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_EIGHT.values()):
                    if calc_filial:
                        dou_capacities[INDEX_31_2][age_cat] = childrens_in_age_category(compensating, age_cat)
                    else:
                        dou_capacities[INDEX_31_2][age_cat] = []

            if INDEX_31_3 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_EIGHT.values()):
                    if calc_filial:
                        dou_capacities[INDEX_31_3][age_cat] = childrens_in_age_category(health_group, age_cat)
                    else:
                        dou_capacities[INDEX_31_3][age_cat] = []

            if INDEX_31_4 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_EIGHT.values()):
                    if calc_filial:
                        dou_capacities[INDEX_31_4][age_cat] = childrens_in_age_category(short_stay, age_cat)
                    else:
                        dou_capacities[INDEX_31_4][age_cat] = []

            direct_index = DirectIndex(_dou)

            if INDEX_32 in self.indexes:
                index_32_data = prepare_direct_index_queries(*direct_index.get_queries(*self.list_last_id_directs_32))
                if index_32_data:
                    dou_capacities[INDEX_32][const.ALL] = index_32_data

            if INDEX_32_1 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_FULL.values()):
                    index_32_1_data = prepare_direct_index_queries(
                        *direct_index.get_queries(
                            *self.list_last_id_directs_321, age_range=age_cat, on_date=datetime.date.today
                        )
                    )
                    if index_32_1_data:
                        dou_capacities[INDEX_32_1][age_cat] = index_32_1_data

            if INDEX_32_2 in self.indexes:
                for age_cat in list(const.AGE_CATEGORIES_FULL.values()):
                    index_32_2_data = prepare_direct_index_queries(
                        *direct_index.get_queries(
                            *self.list_last_id_directs_322, age_range=age_cat, on_date=datetime.date.today
                        )
                    )
                    if index_32_2_data:
                        dou_capacities[INDEX_32_2][age_cat] = index_32_2_data

            if INDEX_33 in self.indexes:
                dou_capacities[INDEX_33][const.ALL] = get_count_data(
                    get_queue_index_collection(INDEX_33, _dou, report=True)
                )

            return _capacities

        capacities = _inner(dou, self._report_start_date)
        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_capacities = _inner(filial, self._report_start_date, calc_filial=False)

            self._merge_dicts(capacities, filial_capacities)

        self._update_cache(capacities, self.CAPACITIES)

        return capacities

    def _calculate_xml_tags(self, report_form=None):
        """Расчёт тегов в выходном файле xml."""

        unit = self._mo
        region_data = unit.kind.id == UnitKind.REGION

        data_dict = defaultdict(dict)
        data_dict_by_group = defaultdict(dict)
        data_dict_by_group_only_values = defaultdict(dict)
        for mo in unit.get_descendants(include_self=True).filter(kind__id=UnitKind.MO):
            document = TemplateView(
                mo,
                datetime.datetime.now(),
                ScheduleSettings.get_settings(),
                self._unit_helper,
                report_form,
                region_data=region_data,
            )
            # Данные для региона передаются только в одном МО
            region_data = False

            (mo_data, mo_data_by_groups, mo_data_by_groups_only_values) = self._get_unit_data_from_template_view(
                document
            )

            for tag, tag_data_dict in mo_data.items():
                data_dict[tag][mo.id] = tag_data_dict

            for tag, tag_data_dict in mo_data_by_groups.items():
                data_dict_by_group[tag][mo.id] = tag_data_dict

            for tag, tag_data_dict in mo_data_by_groups_only_values.items():
                data_dict_by_group_only_values[tag][mo.id] = tag_data_dict

        return data_dict, data_dict_by_group, data_dict_by_group_only_values

    def _get_unit_data_from_template_view(self, document):
        """Получение данных организации из объекта TemplateView."""

        result_dict = defaultdict(dict)
        result_dict_by_groups = defaultdict(dict)
        result_dict_by_groups_only_values = defaultdict(dict)

        for dou_data in document.units:
            unit_id = dou_data.unit_id
            unit = get_instance(unit_id, Unit)
            ext_unit = getattr(unit, 'ext_unit', None)

            # Словари с данными
            organization = dou_data.organization
            data_advisory_centr = organization['data_advisory_centr']
            early_assistant_data = organization['early_assistant_data']
            # Маппинг для сопоставления словарей в маппинге XML_TAGS_MAPPING
            data_mapping = {
                'organization': organization,
                'data_advisory_centr': data_advisory_centr,
                'early_assistant_data': early_assistant_data,
            }

            for data_type, tag_info in XML_TAGS_MAPPING.items():
                data = data_mapping[data_type]
                for tag, param_name in tag_info:
                    if tag in self.indexes and param_name in data:
                        result_dict[tag][unit_id] = data[param_name]

            if INDEX_PASSPORT in self.indexes:
                result_dict[INDEX_PASSPORT][unit_id] = get_detailed_passport(ext_unit)

            for building in dou_data.buildings:
                for group_data in building['groups']:
                    for tag, param_name in XML_GROUP_TAGS_MAP:
                        if tag in self.indexes and param_name in group_data:
                            if unit_id not in result_dict_by_groups[tag]:
                                result_dict_by_groups[tag][unit_id] = defaultdict(list)
                            age_cat = ''
                            if tag not in EXCLUDE_AGE_CATEGORY:
                                age_cat = f'от {int(group_data["ageFrom"])} до {int(group_data["ageTo"])} лет'

                            result_dict_by_groups[tag][unit_id][age_cat].extend(group_data[param_name])

            for building in dou_data.buildings:
                for group_data in building['groups']:
                    for tag, param_name in XML_GROUP_TAGS_ONLY_VALUES_MAP:
                        if tag in self.indexes and param_name in group_data:
                            if unit_id not in result_dict_by_groups_only_values[tag]:
                                result_dict_by_groups_only_values[tag][unit_id] = {}
                            result_dict_by_groups_only_values[tag][unit_id][group_data['id']] = {
                                'doo_name': group_data['doo_name'],
                                'group_name': group_data['name'],
                                'value': group_data[param_name],
                            }

        return (result_dict, result_dict_by_groups, result_dict_by_groups_only_values)

    def _collect_applications_data(self, dou):
        def _inner(_dou):
            applications = OrderedDict(
                [
                    ('1', OrderedDict()),
                    ('1.1', OrderedDict()),
                    ('2', OrderedDict()),
                    ('3', OrderedDict()),
                    ('4', OrderedDict()),
                    ('4.1', OrderedDict()),
                    ('4.2', OrderedDict()),
                    ('5', OrderedDict()),
                    ('6', OrderedDict()),
                ]
            )

            if INDEX_4 in self.indexes:
                index_4 = get_queue_index_collection(INDEX_4, _dou)
            if INDEX_4_1 in self.indexes:
                index_4_1 = get_queue_index_collection(INDEX_4_1, _dou)
            if INDEX_4_2 in self.indexes:
                index_4_2 = get_queue_index_collection(INDEX_4_2, _dou)

            if INDEX_5 in self.indexes:
                index_5 = get_queue_index_collection(INDEX_5, _dou)

            with session_scope() as session:
                index = ApplicationIndex(_dou, session)

                for age_category in list(const.AGE_CATEGORIES_FULL.values()):
                    on_date_filter = get_age_filter(age_category, datetime.date.today)

                    index_2_value = 0
                    index_3_value = 0

                    if INDEX_2 in self.indexes or INDEX_1_1 in self.indexes:
                        index_2_value = index.get_count(
                            index_type=ApplicationIndex.COUNT_BY_DELIVERY,
                            portal=1,
                            age_range=age_category,
                            on_date=datetime.date.today,
                        )
                    if INDEX_3 in self.indexes or INDEX_1_1 in self.indexes:
                        index_3_value = index.get_count(
                            index_type=ApplicationIndex.COUNT_BY_DELIVERY,
                            age_range=age_category,
                            on_date=datetime.date.today,
                        )

                    if INDEX_2 in self.indexes:
                        applications[INDEX_2][age_category] = index_2_value

                    if INDEX_3 in self.indexes:
                        applications[INDEX_3][age_category] = index_3_value
                    if INDEX_1_1 in self.indexes:
                        applications[INDEX_1_1][age_category] = index_2_value + index_3_value
                    if INDEX_4 in self.indexes:
                        applications[INDEX_4][age_category] = get_count(index_4, on_date_filter)
                    if INDEX_4_1 in self.indexes:
                        applications[INDEX_4_1][age_category] = get_count(index_4_1, on_date_filter)
                    if INDEX_4_2 in self.indexes:
                        applications[INDEX_4_2][age_category] = get_count(index_4_2, on_date_filter)

                    if INDEX_5 in self.indexes:
                        applications[INDEX_5][age_category] = get_count(index_5, on_date_filter)

                    # Общее количество заявлений на постановку в очередь
                    # в группы кратковременного пребывания
                    if INDEX_6 in self.indexes:
                        applications[INDEX_6][age_category] = index.get_count(
                            index_type=ApplicationIndex.COUNT_BY_GROUP_TYPE,
                            age_range=age_category,
                            on_date=datetime.date.today,
                        )

                if INDEX_1 in self.indexes:
                    applications[INDEX_1][const.ALL] = get_queue_index(INDEX_1, _dou, distinct_children=True)

            return {_dou.id: applications}

        app = _inner(dou)

        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_app = _inner(filial)
            self._merge_dicts(app, filial_app)

        self._update_cache(app, self.REPORT_APPLICATIONS)

        return app
