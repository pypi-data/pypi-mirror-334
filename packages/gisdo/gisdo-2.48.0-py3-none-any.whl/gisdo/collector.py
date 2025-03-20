import datetime
import json
from collections import (
    OrderedDict,
)
from functools import (
    partial,
)
from itertools import (
    chain,
)

from future.builtins import (
    object,
)

from kinder.core.dict.models import (
    GroupTypeEnumerate,
)

from gisdo import (
    constants as const,
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
from gisdo.algorithm.utils import (
    HealthNeedIdsProvider,
)
from gisdo.counter.counter import (
    get_main_counter,
)
from gisdo.counter.provider import (
    DataProvider,
)
from gisdo.exceptions import (
    NoDataInMo,
)
from gisdo.index import (
    ApplicationIndex,
    get_enrolled_age_filter,
    get_enrolled_count,
    get_queue_age_filter,
    get_queue_average_waiting_time,
    get_queue_count,
    get_queue_index,
    get_queue_index_collection,
)
from gisdo.index.capacities import (
    free_space_in_age_category,
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
    ReportFormRow,
)
from gisdo.utils import (
    DateMixin,
    GisdoJsonEncoder,
    get_ordered_dict_of_ordered_dicts,
    set_zero_values,
)


class GisdoJsonDumpsMixin(object):
    """Позволяет дампить в сборщиках отчета дополнительные классы."""

    json_dumps = partial(json.dumps, cls=GisdoJsonEncoder)


class ReportCacheMixin(object):
    APPLICATIONS = 'applications'
    QUEUES = 'queues'
    ENROLLED = 'enrolled'
    CAPACITIES = 'capacities'

    DATA_TYPE = [APPLICATIONS, QUEUES, ENROLLED, CAPACITIES]

    def __init__(self):
        self._cache = {self.APPLICATIONS: {}, self.QUEUES: {}, self.ENROLLED: {}, self.CAPACITIES: {}}

    def _update_cache(self, data, data_type):
        """Обновление кэша."""

        for key, value in data.items():
            if key not in self._cache[data_type]:
                self._cache[data_type][key] = value
            elif isinstance(value, dict):
                for age_cat in data[key]:
                    self._cache[data_type][key][age_cat] += data[key][age_cat]


class DataCollector(GisdoJsonDumpsMixin, ReportCacheMixin):
    def __init__(self, mo, unit_helper, report_start_date):
        super(DataCollector, self).__init__()

        self._mo = mo
        self._unit_helper = unit_helper
        self._report_start_date = report_start_date

    def collect(self, report_form):
        # Признак наличия садов по которым можно
        # собрать данные
        dou_list = self._unit_helper.get_mo_units(self._mo.id)
        have_data = len(dou_list)

        if not have_data:
            raise NoDataInMo(f'Нет садов в МО {self._mo} пригодных для отправки')

        # Для расчета показателя 32 и 32.1, 32.2, необходим список
        # идентификаторов последних направлений у ребенка в рамках МО
        self.list_last_id_directs_32 = get_children_last_direct_ids(
            self._mo.id, self._report_start_date, get_32_filter()
        )
        self.list_last_id_directs_321 = get_children_last_direct_ids(
            self._mo.id, self._report_start_date, get_321_filter()
        )
        self.list_last_id_directs_322 = get_children_last_direct_ids(
            self._mo.id, self._report_start_date, get_322_filter()
        )

        # Собираем по ДОУ
        for dou in dou_list:
            counter = get_main_counter()
            decl_data = DataProvider(dou)
            decls = []
            decls.append(decl_data.get_rows())

            for filial in self._unit_helper.get_filial(dou).iterator():
                decl_data = DataProvider(filial)
                decls.append(decl_data.get_rows())

            decls = chain(*decls)
            result = counter.count(decls)
            self._dou_collect(report_form, dou, result)

        # Данные по МО лежат в кэше
        ReportFormRow.objects.update_or_create(
            report=report_form,
            unit=self._mo,
            defaults=dict(
                applications=self.json_dumps(self._cache[self.APPLICATIONS]),
                queues=self.json_dumps(self._cache[self.QUEUES]),
                enrolled=self.json_dumps(self._cache[self.ENROLLED]),
                capacities=self.json_dumps(self._cache[self.CAPACITIES]),
            ),
        )

        return self._cache

    def _dou_collect(self, report_form, dou, counter):
        applications = self._collect_applications_data(counter)
        queues = self._collect_queue_data(dou)
        enrolled = self._collect_enrolled_data(dou)
        capacities = self._collect_capacities(dou)

        ReportFormRow.objects.update_or_create(
            report=report_form,
            unit=dou,
            defaults=dict(
                applications=self.json_dumps(applications),
                queues=self.json_dumps(queues),
                enrolled=self.json_dumps(enrolled),
                capacities=self.json_dumps(capacities),
            ),
        )

    @staticmethod
    def _merge_dicts(first_dict, second_dict):
        for index in first_dict:
            for age_cat in first_dict[index]:
                try:
                    value = second_dict[index][age_cat]
                except KeyError:
                    value = 0
                first_dict[index][age_cat] += value

    def _collect_applications_data(self, counter):
        applications = OrderedDict(
            [
                ('1', OrderedDict()),
                ('1.1', OrderedDict()),
                ('2.1', OrderedDict()),
                ('3.1', OrderedDict()),
                ('4', OrderedDict()),
                ('4.1', OrderedDict()),
                ('4.2', OrderedDict()),
                ('5', OrderedDict()),
                ('6', OrderedDict()),
            ]
        )

        applications['1'][const.ALL] = counter[('1',)]

        indexes = (
            '1.1',
            '2.1',
            '3.1',
            '4',
            '4.1',
            '4.2',
            '5',
            '6',
        )

        for age_cat, age_cat_name in const.AGE_CATEGORIES_FULL.items():
            for index in indexes:
                applications[index][age_cat_name] = counter[(index, age_cat)]

        self._update_cache(applications, self.APPLICATIONS)

        return applications

    def _collect_queue_data(self, dou):
        def _inner(dou):
            queues = get_ordered_dict_of_ordered_dicts(
                (
                    '7',
                    '7.1',
                    '7.2',
                    '7.3',
                    '7.4',
                    '7.5',
                    '7.6',
                    '7.7',
                    '8',
                    '8.1',
                    '8.2',
                    '8.3',
                    '9',
                    '9.1',
                    '10',
                    '10.1',
                    '11',
                    '12',
                    '12.1',
                    '13',
                    '13.1',
                    '14',
                    '15',
                    '16',
                    '17',
                    '17.1',
                    '18',
                    '18.1',
                    '18.2',
                    '18.3',
                    '18.4',
                    '18.5',
                )
            )

            index_7 = get_queue_index_collection('7', dou)
            index_7_1 = get_queue_index_collection('7.1', dou)
            index_7_2 = get_queue_index_collection('7.2', dou)
            index_7_3 = get_queue_index_collection('7.3', dou)
            index_7_4 = get_queue_index_collection('7.4', dou)
            index_7_5 = get_queue_index_collection('7.5', dou)
            index_7_7 = get_queue_index_collection('7.7', dou)

            index_8 = get_queue_index_collection('8', dou)
            index_8_1 = get_queue_index_collection('8.1', dou)
            index_8_2 = get_queue_index_collection('8.2', dou)
            index_8_3 = get_queue_index_collection('8.3', dou)

            index_10 = get_queue_index_collection('10', dou)
            index_10_1 = get_queue_index_collection('10.1', dou)

            index_11 = get_queue_index_collection('11', dou)

            index_12 = get_queue_index_collection('12', dou)
            index_12_1 = get_queue_index_collection('12.1', dou)

            index_13 = get_queue_index_collection('13', dou)
            index_13_1 = get_queue_index_collection('13.1', dou)

            index_14 = get_queue_index_collection('14', dou)

            index_15 = get_queue_index_collection('15', dou)

            index_16 = get_queue_index_collection('16', dou)

            index_17 = get_queue_index_collection('17', dou)
            index_17_1 = get_queue_index_collection('17.1', dou)

            index_18 = get_queue_index_collection('18', dou)
            index_18_1 = get_queue_index_collection('18.1', dou)
            index_18_2 = get_queue_index_collection('18.2', dou)
            index_18_3 = get_queue_index_collection('18.3', dou)
            index_18_4 = get_queue_index_collection('18.4', dou, distinct_children=True)
            index_18_5 = get_queue_index_collection('18.5', dou)

            queues['10'][const.ALL] = 0
            queues['11'][const.ALL] = 0

            for value in list(const.AGE_CATEGORIES_FULL.values()):
                on_date_filter = get_queue_age_filter(value, datetime.date.today)
                current_year_first_september = get_queue_age_filter(
                    value,
                    DateMixin.get_current_calendar_year(),
                )
                next_year_first_day = get_queue_age_filter(
                    value,
                    datetime.date(datetime.date.today().year + 1, 1, 1),
                )
                next_learn_year_first_day = get_queue_age_filter(
                    value,
                    DateMixin.get_next_calendar_year_start(),
                )

                # Отложенный спрос
                queues['7'][value] = get_queue_count(index_7, current_year_first_september)
                queues['7.1'][value] = get_queue_count(index_7_1, on_date_filter)
                queues['7.2'][value] = get_queue_count(index_7_2, on_date_filter)
                queues['7.4'][value] = get_queue_count(index_7_4, on_date_filter)
                queues['7.5'][value] = get_queue_count(index_7_5, on_date_filter)
                queues['7.6'][value] = get_queue_count(index_7_5, next_learn_year_first_day)
                queues['7.7'][value] = get_queue_count(index_7_7, next_learn_year_first_day)

                # Актуальный спрос
                queues['7.3'][value] = get_queue_count(index_7_3, on_date_filter)
                queues['18'][value] = get_queue_count(index_18, current_year_first_september)
                queues['18.1'][value] = get_queue_count(index_18_1, on_date_filter)
                queues['18.2'][value] = get_queue_count(index_18_2, next_year_first_day)
                queues['18.3'][value] = get_queue_count(index_18_3, on_date_filter)
                queues['18.4'][value] = get_queue_count(index_18_4, on_date_filter)
                queues['18.5'][value] = get_queue_count(index_18_5, on_date_filter)

                # Количество детей в очереди с ограниченными
                # возможностями по здоровью
                queues['12'][value] = get_queue_count(index_12, on_date_filter)
                queues['12.1'][value] = get_queue_count(index_12_1, on_date_filter)

                queues['13'][value] = get_queue_count(index_13, on_date_filter)
                queues['13.1'][value] = get_queue_count(index_13_1, on_date_filter)

                queues['14'][value] = get_queue_count(index_14, on_date_filter)

                queues['15'][value] = get_queue_count(index_15, on_date_filter)

                queues['16'][value] = get_queue_count(index_16, on_date_filter)

                queues['17'][value] = get_queue_count(index_17, on_date_filter)
                queues['17.1'][value] = get_queue_count(index_17_1, on_date_filter)

                queues['9'][value] = get_queue_count(index_10, current_year_first_september) + get_queue_count(
                    index_11, current_year_first_september
                )

                queues['10.1'][value] = get_queue_count(index_10_1, on_date_filter)

                # Количество детей в очереди имеющих право зачисления
                # на основе федеральных и региональных льгот.
                current_10_value = get_queue_count(index_10, on_date_filter)
                queues['10'][const.ALL] += current_10_value

                current_11_value = get_queue_count(index_11, on_date_filter)
                queues['11'][const.ALL] += current_11_value

                queues['9.1'][value] = current_10_value + current_11_value

            for value in list(const.AGE_CATEGORIES_EIGHT.values()):
                queues['8'][value] = get_queue_average_waiting_time(index_8, value)
                queues['8.1'][value] = get_queue_average_waiting_time(index_8_1, value)
                queues['8.2'][value] = get_queue_average_waiting_time(index_8_2, value)
                queues['8.3'][value] = get_queue_average_waiting_time(index_8_3, value)

            return queues

        queues = _inner(dou)
        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_queues = _inner(filial)
            self._merge_dicts(queues, filial_queues)

        self._update_cache(queues, self.QUEUES)

        return queues

    def _collect_enrolled_data(self, dou):
        def _inner(dou, report_start_date, calc_filial=False):
            enrolled = get_ordered_dict_of_ordered_dicts(
                (
                    '19',
                    '19.1',
                    '19.2',
                    '19.3',
                    '20',
                    '20.1',
                    '20.2',
                    '20.3',
                    '20.4',
                    '20.5',
                    '20.6',
                    '20.7',
                    '20.8',
                    '21',
                    '22',
                    '22.1',
                    '22.1.1',
                    '22.1.2',
                    '22.2',
                    '22.3',
                    '22.3.1',
                    '22.3.2',
                    '22.4',
                    '22.5',
                    '22.5.1',
                    '22.5.2',
                    '22.6',
                    '22.7',
                    '22.8',
                    '22.8.1',
                    '22.8.2',
                    '23',
                    '24',
                    '25',
                    '26',
                    '27',
                    '28',
                    '29',
                    '29.1',
                    '29.2',
                    '29.3',
                    '30',
                    '30.1',
                    '30.2',
                )
            )

            def sum_enrolled(age_cat, *indexes):
                return sum(enrolled[i][age_cat] for i in indexes)

            enrolled_index = Index(dou, report_start_date)

            index_20 = get_queue_index_collection('20', dou)
            index_20_1 = get_queue_index_collection('20.1', dou, check_unit=False, distinct_children=True)
            index_20_2 = get_queue_index_collection('20.2', dou)
            index_20_3 = get_queue_index_collection('20.3', dou)
            index_20_5 = get_queue_index_collection('20.5', dou, check_unit=False)
            index_20_6 = get_queue_index_collection('20.6', dou, check_unit=False)
            index_20_7 = get_queue_index_collection('20.7', dou, check_unit=False)
            index_20_8 = get_queue_index_collection('20.8', dou, check_unit=False)
            index_29_1 = ind_29_1(dou, self._report_start_date)
            index_29_2 = ind_29_2(dou)
            index_29_3 = ind_29_3(dou)
            if not calc_filial:
                index_19 = list(enrolled_index())
                index_21 = list(
                    enrolled_index(
                        group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.FAMILY)
                    )
                )

                indexes_22 = {}
                for ind in const.SIMPLE_INDEXES_22:
                    if ind == '22':
                        indexes_22[ind] = get_22_index(enrolled_index)
                        continue

                    hn = HealthNeedIdsProvider.get_health_need(ind)
                    if ind == '22.8.1':
                        indexes_22[ind] = get_22_8_x_index(
                            enrolled_index=enrolled_index,
                            health_need_list=hn,
                            children_filter='fed_report_exclude_for_22_8_1',
                        )
                    elif ind == '22.8.2':
                        indexes_22[ind] = get_22_8_x_index(
                            enrolled_index=enrolled_index,
                            health_need_list=hn,
                            children_filter='fed_report_exclude_for_22_8_2',
                        )
                    else:
                        indexes_22[ind] = get_22_x_index(enrolled_index, hn)

                index_23 = list(
                    enrolled_index(
                        group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.COMP)
                    )
                )

                index_24 = list(
                    enrolled_index(
                        group_filter=lambda group: (group.type and group.type.code == GroupTypeEnumerate.HEALTH)
                    )
                )

                index_25 = list(
                    enrolled_index(
                        group_filter=lambda group: (
                            group.type
                            and (
                                group.type.code == GroupTypeEnumerate.CARE
                                or group.type.code == GroupTypeEnumerate.YOUNG
                            )
                        )
                    )
                )

                index_26 = get_26_index(enrolled_index)
                index_27 = get_27_index(enrolled_index)
                index_28 = get_28_index(enrolled_index)
                index_30 = get_30_index(enrolled_index)
                index_30_1 = get_30_1_index(enrolled_index)
                index_30_2 = get_30_2_index(enrolled_index)

            for value in list(const.AGE_CATEGORIES_FULL.values()):
                current_year_enrolled_filter = get_enrolled_age_filter(value, DateMixin.get_current_calendar_year())
                on_date_enrolled_filter = get_enrolled_age_filter(value, datetime.date.today)
                next_calendar_year_enrolled = get_enrolled_age_filter(value, DateMixin.get_next_calendar_year)
                on_other_date_age_filter = get_age_for_date_filter(value)
                # Общая численность детей зачисленных в ДОО
                if not calc_filial:
                    enrolled['19'][value] = get_enrolled_count(index_19, current_year_enrolled_filter)
                    enrolled['19.1'][value] = get_enrolled_count(index_19, on_date_enrolled_filter)
                    enrolled['19.2'][value] = get_enrolled_count(index_19, next_calendar_year_enrolled)
                else:
                    set_zero_values(enrolled, ('19', '19.1', '19.2'), value)

                enrolled['19.3'][value] = ind_19_3(dou, report_start_date, age_range=value)

                on_date_filter = get_queue_age_filter(value, datetime.date.today)
                enrolled['20'][value] = get_queue_count(index_20, on_date_filter)
                enrolled['20.1'][value] = get_queue_count(index_20_1, on_date_filter)
                enrolled['20.2'][value] = get_queue_count(index_20_2, on_date_filter)
                enrolled['20.3'][value] = get_queue_count(index_20_3, on_date_filter)
                enrolled['20.5'][value] = get_queue_count(index_20_5, on_date_filter)
                enrolled['20.6'][value] = get_queue_count(index_20_6, on_date_filter)
                enrolled['20.7'][value] = get_queue_count(index_20_7, on_date_filter)
                enrolled['20.8'][value] = get_queue_count(index_20_8, on_date_filter)

                # Общая численность детей, зачисленных в группы для
                # детей с ограниченными возможностями здоровью
                if not calc_filial:
                    enrolled['21'][value] = get_enrolled_count(index_21, on_date_enrolled_filter)

                    # Общая численность детей, зачисленных в группы для
                    # детей с ограниченными возможностями здоровью
                    for ind in const.SIMPLE_INDEXES_22:
                        enrolled[ind][value] = get_enrolled_count(indexes_22[ind], on_date_enrolled_filter)

                    for main_index, sum_indexes in const.SUM_INDEXES_22.items():
                        enrolled[main_index][value] = sum_enrolled(value, *sum_indexes)
                else:
                    set_zero_values(
                        enrolled,
                        ('21', *const.SIMPLE_INDEXES_22, *list(const.SUM_INDEXES_22.keys())),
                        value,
                    )
                # Общее количество детей зачисленных в
                # оздоровительные и компенсирующие группы
                if not calc_filial:
                    enrolled['23'][value] = get_enrolled_count(index_23, on_date_enrolled_filter)
                    enrolled['24'][value] = get_enrolled_count(index_24, on_date_enrolled_filter)
                    enrolled['25'][value] = get_enrolled_count(index_25, on_date_enrolled_filter)
                    # Общая численность детей, зачисленных в
                    # группы круглосуточного пребывания детей
                    enrolled['26'][value] = get_enrolled_count(index_26, on_date_enrolled_filter)
                    # Общая численность детей, зачисленных в группы
                    # кратковременного пребывания детей
                    enrolled['27'][value] = get_enrolled_count(index_27, on_date_enrolled_filter)
                    # Общая численность детей, посещающих ДОО в режиме
                    # кратковременного пребывания
                    enrolled['28'][value] = get_enrolled_count(index_28, on_date_enrolled_filter)
                else:
                    set_zero_values(enrolled, ('23', '24', '25', '26', '27', '28'), value)

                if not calc_filial:
                    enrolled['30'][value] = get_enrolled_count(index_30, on_date_enrolled_filter)
                    enrolled['30.1'][value] = get_enrolled_count(index_30_1, on_date_enrolled_filter)
                    enrolled['30.2'][value] = get_enrolled_count(index_30_2, on_date_enrolled_filter)
                else:
                    set_zero_values(enrolled, ('30', '30.1', '30.2'), value)

                enrolled['29.1'][value] = get_enrolled_count(index_29_1, on_date_enrolled_filter)

                enrolled['29.2'][value] = get_enrolled_count(index_29_2, on_other_date_age_filter)

                enrolled['29.3'][value] = get_enrolled_count(index_29_3, next_calendar_year_enrolled)

                enrolled['20.4'][value] = get_queue_index('20.4', dou, age_range=value)

            # Общее количество детей зачисленных в семейные,
            # оздоровительные и компенсирующие группы
            if not calc_filial:
                enrolled['29'][const.ALL] = len(list(enrolled_index(query_filter='predictable_decrease_contingent')))
            else:
                enrolled['29'][const.ALL] = 0

            return enrolled

        enrolled = _inner(dou, self._report_start_date)
        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_enrolled = _inner(filial, self._report_start_date, calc_filial=True)

            self._merge_dicts(enrolled, filial_enrolled)

        self._update_cache(enrolled, self.ENROLLED)

        return enrolled

    @staticmethod
    def get_free_spaces_by_group(dou, report_start_date, prep_function=None):
        """
        Возвращает значения по свободным местам в группам для
        показателей 31 и 31_x.
        """
        group_index = Index(dou, report_start_date)
        if not group_index.is_calculated:
            common = []
            short_stay = []
            with_hn = []
            compensating = []
            health_group = []
        else:
            common = group_index.free_space_in_unit(group_filter=None, prep_function=prep_function)
            short_stay = group_index.free_space_in_unit(group_filter='short_stay', prep_function=prep_function)
            with_hn = group_index.free_space_in_unit(group_filter='with_health_need', prep_function=prep_function)
            compensating = group_index.free_space_in_unit(group_filter='compensating', prep_function=prep_function)
            health_group = group_index.free_space_in_unit(group_filter='health_group', prep_function=prep_function)

        return common, short_stay, with_hn, compensating, health_group

    def _collect_capacities(self, dou):
        def _inner(_dou, report_start_date, calc_filial=True):
            capacities = get_ordered_dict_of_ordered_dicts(
                [
                    '31',
                    '31.1',
                    '31.2',
                    '31.3',
                    '31.4',
                    '32',
                    '32.1',
                    '32.2',
                    '33',
                ]
            )

            common = []
            short_stay = []
            with_hn = []
            compensating = []
            health_group = []

            if calc_filial:
                common, short_stay, with_hn, compensating, health_group = self.get_free_spaces_by_group(
                    _dou, report_start_date
                )

            for value in list(const.AGE_CATEGORIES_EIGHT.values()):
                if calc_filial:
                    capacities['31'][value] = free_space_in_age_category(common, value)
                    capacities['31.1'][value] = free_space_in_age_category(with_hn, value)
                    capacities['31.2'][value] = free_space_in_age_category(compensating, value)
                    capacities['31.3'][value] = free_space_in_age_category(health_group, value)
                    capacities['31.4'][value] = free_space_in_age_category(short_stay, value)
                else:
                    zero_indexes = ('31', '31.1', '31.2', '31.3', '31.4')
                    set_zero_values(capacities, zero_indexes, value)

            direct_index = DirectIndex(_dou)
            capacities['32'][const.ALL] = direct_index.get_count(*self.list_last_id_directs_32)
            for value in list(const.AGE_CATEGORIES_FULL.values()):
                capacities['32.1'][value] = direct_index.get_count(
                    *self.list_last_id_directs_321, age_range=value, on_date=datetime.date.today
                )
                capacities['32.2'][value] = direct_index.get_count(
                    *self.list_last_id_directs_322, age_range=value, on_date=datetime.date.today
                )

            capacities['33'][const.ALL] = get_queue_index('33', _dou)

            return capacities

        capacities = _inner(dou, self._report_start_date)
        for filial in self._unit_helper.get_filial(dou).iterator():
            filial_capacities = _inner(filial, self._report_start_date, calc_filial=False)

            self._merge_dicts(capacities, filial_capacities)

        self._update_cache(capacities, self.CAPACITIES)

        return capacities
