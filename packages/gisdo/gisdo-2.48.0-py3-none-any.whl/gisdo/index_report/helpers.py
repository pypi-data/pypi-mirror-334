from collections import (
    defaultdict,
    namedtuple,
)
from functools import (
    partialmethod,
)
from itertools import (
    chain,
)
from typing import (
    List,
)

from django.db.models import (
    CharField,
    QuerySet,
    Value,
)

from kinder.core.children.models import (
    Children,
)

from ..algorithm.enrolled import (
    get_22_x_index,
)
from .constants import (
    DataTypes,
    DataTypes as DT,
)


# namedtuple для описания строки отчёта
ReportRecord = namedtuple('ReportRecord', ['unit_name', 'age_cat', 'data_type', 'data_id', 'value'])


class ReportQuery:
    """Класс для обработки запросов для отчёта."""

    # Значения values_list для запросов различных моделей
    children_values_list = ('id', 'date_of_birth', 'fullname', 'model', 'id')
    declaration_values_list = pupils_values_list = deduct_values_list = (
        'children_id',
        'children__date_of_birth',
        'children__fullname',
        'model',
        'id',
    )
    direct_values_list = (
        'declaration__children_id',
        'declaration__children__date_of_birth',
        'declaration__children__fullname',
        'model',
        'id',
    )

    # Словарь для соответствия типа данных и values_list для запроса
    type_to_values_list = {
        DT.DIRECT: direct_values_list,
        DT.DECLARATION: declaration_values_list,
        DT.CHILD: children_values_list,
        DT.PUPIL: pupils_values_list,
        DT.DEDUCT: deduct_values_list,
    }

    @classmethod
    def get(cls, data_type, query):
        """Получения запроса с необходимыми данными для отчёта

        :param data_type: Тип данных
        :param query: Запрос

        :return: Запрос с необходимыми данными для запроса
        """
        return query.annotate(model=Value(data_type, output_field=CharField())).values_list(
            *cls.type_to_values_list[data_type]
        )

    # Методы для получения запросов для различных моделей
    get_child_query = partialmethod(get, DT.CHILD)
    get_direct_query = partialmethod(get, DT.DIRECT)
    get_declaration_query = partialmethod(get, DT.DECLARATION)
    get_pupil_query = partialmethod(get, DT.PUPIL)
    get_deduct_query = partialmethod(get, DT.DEDUCT)


def prepare_enrolled_index_queries(enrolled_in_group_fact, enrolled_in_group_plan):
    """Функция получения доп. данных для enrolled индекса."""

    return list(
        chain(
            ReportQuery.get_pupil_query(enrolled_in_group_fact),
            ReportQuery.get_pupil_query(enrolled_in_group_plan),
        )
    )


def prepare_direct_index_queries(qs_direct: QuerySet, qs_pupil: QuerySet) -> list:
    """Функция получения доп. данных для DirectIndex."""

    return list(
        chain(
            ReportQuery.get_direct_query(qs_direct),
            ReportQuery.get_pupil_query(qs_pupil),
        )
    )


def prepare_31_x_index(
    occupancy: int, enrolled_count: int, directs_count: int, vacant_places: int, free_space: int
) -> str:
    """Формирует вывод для показателей 31 и 31_x."""

    index_31_x_string = (
        f'Наполняемость: {occupancy}\n'
        f'Зачислений: {enrolled_count}\n'
        f'Направлений: {directs_count}\n'
        f'Мест для перевода: {vacant_places}\n\n'
        f'Итого свободных мест: {free_space}'
    )

    return index_31_x_string


def prep_ind_19_3_queries(*queries):
    """Функция получения доп. данных для индекса 19_3."""

    (direct_in_group, direct_count_in_bounded_group, pupil_direct_in_bounded_group) = queries

    return list(
        chain(
            direct_in_group.values_list('declaration__children_id', 'declaration__children__date_of_birth'),
            direct_count_in_bounded_group.values_list(
                'declaration__children_id', 'declaration__children__date_of_birth'
            ),
            pupil_direct_in_bounded_group.values_list('children_id', 'children__date_of_birth'),
        )
    )


def prep_ind_29_1_queries(*queries):
    """Функция получения доп. данных для индекса 29_1."""

    direct_query, pupil_query = queries
    result = {
        row[0]: row
        for row in chain(
            ReportQuery.get_direct_query(direct_query),
            # Как направления считаем и зачисления, дата зачисления по приказу
            # которых больше контрольной даты
            ReportQuery.get_pupil_query(pupil_query),
        )
    }
    return result.values()


def prep_ind_29_2_query(deduct_query: QuerySet) -> list:
    """Функция получения доп. данных для индекса 29_2."""
    # Возраст считается на дату отчисления, поэтому её тоже берём
    # (вставляем 3 элементом)
    values_list = list(ReportQuery.deduct_values_list)
    values_list.insert(2, 'date')

    query = (
        ReportQuery.get_deduct_query(deduct_query)
        .values_list(*values_list)
        .order_by('children_id', '-date')
        .distinct('children_id')
    )
    return list(query)


def prep_in_29_2_data(query_data: List[tuple]) -> List[list]:
    """Функция подготовки данных для индекса 29_2."""
    # Берем всё, кроме 3 элемента, т.е. убираем дату отчисления
    return [[*data[:2], *data[3:]] for data in query_data]


def prep_ind_29_3_query(deduct_query: QuerySet) -> list:
    """Функция получения доп. данных для индекса 29_3."""
    query = ReportQuery.get_deduct_query(deduct_query).order_by('children_id', '-date').distinct('children_id')
    return list(query)


def prep_directs_in_group_queries(*queries):
    """Подготовка запросов для directs_in_group (индекс 31)."""

    return list(
        chain(
            ReportQuery.get_direct_query(queries[0]),
            ReportQuery.get_direct_query(queries[1]),
            ReportQuery.get_pupil_query(queries[2]),
        )
    )


def prep_ind_enrolled_data(children_enrollments):
    """Функция получения доп. данных для индекса enrolled."""

    children_data = ReportQuery.get_child_query(Children.objects.filter(id__in=children_enrollments.keys()))

    group_enrollments = defaultdict(list)

    for children_id, group_id in children_enrollments.items():
        children_info = {t[0]: t for t in [a for a in children_data]}
        group_enrollments[group_id].append(children_info.get(children_id))

    return group_enrollments


def get_count_data(collection, age_filter=lambda x: x):
    """Возвращает записи в коллекции подходящие под фильтр.

    Функция применяет фильтр age_filter к коллекции collection и возвращает
    отфильтрованные записи.
    """

    return [
        (
            declaration.get('children_id'),
            declaration.get('children__date_of_birth'),
            declaration.get('children__fullname'),
            DataTypes.CHILD,
            declaration.get('children_id'),
        )
        for declaration in collection
        if age_filter(declaration)
    ]
