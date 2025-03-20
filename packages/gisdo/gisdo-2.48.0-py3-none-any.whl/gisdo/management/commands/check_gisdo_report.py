"""
Manage-команда проверяет условия Информики на основе последней/выбранной сборки

Команда осуществляет различные проверки для сборки ФО, которые осуществляются
на стороне Информики. В данном скрипте в основном проверяются проверки для
показателей 22.х (все показатели 22), 30.1, 30.2 и тэг ovz_deti для всех
организаций, которые входят в собранный отчёт ФО.

За основу скрипта был взят файл из gisdo/tests/checklist_tests.py, дополнительно
в текущем скрипте был добавлен удобный вывод ошибок в xlsx файл в виде таблицы,
в предыдущей же реализации можно было посмотреть только первый неудавшийся тест.
При доработке возможно стоит изменить структуру команды для возможности учета
также других проверок.

Запуск команды:
- Активировать виртуальное окружение
- Убедиться, что переменная PYTHONPATH включает путь к проекту EDUKNDG
- Установить переменные окружения:
    KINDER_CONFIG_PATH
    DJANGO_SETTINGS_MODULE
- Запустить manage команду. Примеры запуска:
    - Без параметров (команда сама найдет последний собранный отчёт ФО) и
        запустит проверки для него:

        python manage.py check_gisdo_report

    - Проверить определенную сборку ФО (для этого надо знать её id),
        например с id = 5:

        python manage.py check_gisdo_report --report_id 5

- После завершения команды в консоли будет одно из следующих сообщений:
    - "Ошибок не найдено" - в этом случае всё хорошо, ошибок в сборке ФО нет
    - "Данные об ошибках выведены в файл "НАЗВАНИЕ_ФАЙЛА"" - сформированный
        должен появиться в текущей директории
"""

import datetime
from collections import (
    defaultdict,
)
from functools import (
    partial,
)
from itertools import (
    chain,
)
from typing import (
    NamedTuple,
    Union,
)

import django
from django.core.management import (
    BaseCommand,
)
from tqdm import (
    tqdm,
)


django.setup()


from kinder.core.unit.models import (
    UnitKind,
)
from kinder.core.utils.excel import (
    WorkBookWriter,
)

from gisdo.constants import (
    AGE_CATEGORIES_FULL,
)
from gisdo.models import (
    ReportForm,
    ReportFormRow,
)
from gisdo.reports import (
    ReportFormReport,
)
from gisdo.service import (
    DouData,
    GroupData,
)


date_str = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M:%S')
OUTPUT_FILE_NAME = f'gisdo_ovz_deti_checklist_{date_str}.xlsx'
OUTPUT_HEADERS = [
    ('Проверка', 60),
    ('Значение ovz_deti', 30),
    ('Значение показателей', 30),
    ('id организации', 30),
    ('Название организации', 50),
]


def get_name(name, key):
    replaced_value = key.replace('-', '_').replace('.', '_')
    return f'{name}_{replaced_value}'


GROUP_ORIENT_KOMP_AND_KOMBI = (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)


def sum_ovz_deti_in_groups(groups):
    """Суммирует данные тега ovz_deti у данных групп

    Убирает дублирующие группы по id

    :param groups: Данные групп

    :return: Сумма тегов ovz_deti у групп
    """
    data = {group['id']: group['ovz_deti'] for group in groups}
    return sum(data.values())


def filter_dou_groups(dou_groups, orientation=None, ovz_type=None, ovz_type_new=None):
    """Возвращает генератор с фильтрацией по параметрам."""

    for group in dou_groups:
        if orientation and group['orientation'] not in orientation:
            continue

        if ovz_type and group['ovzType'] not in ovz_type:
            continue

        if ovz_type_new and group['ovz_type_new'] not in ovz_type_new:
            continue

        yield group


class TestNames:
    """Класс для хранения названий проверок."""

    sum_30_1_and_30_2 = '30.1 + 30.2 == ovz_deti'
    sum_22_1_and_ovz_orientation_2_or_3 = '22.1 == ovz_deti c orientation=2 и 3 и ovz_type=1'
    sum_22_1_1_and_ovz_orientation_2_or_3 = '22.1 == ovz_deti c orientation=2 и 3 и ovz_type_new=1'
    sum_22_1_2_and_ovz_orientation_2_or_3 = '22.1.2 == ovz_deti c orientation=2 и 3 и ovz_type_new=2'
    sum_22_2_and_ovz_orientation_2_or_3 = '22.2 == ovz_deti c orientation=2 и 3 и ovz_type=2'
    sum_22_3_1_and_ovz_orientation_2_or_3 = '22.3.1 == ovz_deti c orientation=2 и 3 и ovz_type_new=3'
    sum_22_3_2_and_ovz_orientation_2_or_3 = '22.3.2 == ovz_deti c orientation=2 и 3 и ovz_type_new=4'
    sum_22_5_1_and_ovz_orientation_2_or_3 = '22.5.1 == ovz_deti c orientation=2 и 3 и ovz_type_new=7'
    sum_22_5_2_and_ovz_orientation_2_or_3 = '22.5.2 == ovz_deti c orientation=2 и 3 и ovz_type_new=8'
    sum_22_8_1_and_ovz_orientation_2_or_3 = '22.8.1 == ovz_deti c orientation=2 и 3 и ovz_type_new=11'
    sum_22_8_2_and_ovz_orientation_2_or_3 = '22.8.2 == ovz_deti c orientation=2 и 3 и ovz_type_new=12'
    sum_22_x_and_sum_ovz_orientation_2_or_3 = (
        '22.1+22.2.+22.3.+22.4.+22.5.+22.6.+22.7.+22.8 == sum(ovz_deti) c orientation=2 и 3'
    )


class OvzDetiErrorData(NamedTuple):
    """NamedTuple для хранения строк отчета."""

    test_name: str
    ovz_deti: Union[str, int]
    index_data: Union[str, int]
    unit_id: int
    unit_name: str


def get_error_data_if_not_equal(test_name, ovz_data, index_data, unit):
    """Создание строки отчёта, если данные показателей не совпадают."""
    if ovz_data != index_data:
        return OvzDetiErrorData(test_name, ovz_data, index_data, unit.id, unit.name)


class GisdoCheckListsOvzDeti:
    """Запускаем проверки на последнем собранном ФО, для всех ДОУ"""

    def __init__(self, report_id=None):
        """
        :param report_id: id отчета ФО для проверки. Если не указан, будет
            найден последний
        """
        try:
            if report_id:
                self.report_form = ReportForm.objects.get(id=report_id)
                if self.report_form.in_progress:
                    raise Exception('Отчёт ещё собирается')
            else:
                self.report_form = ReportForm.objects.filter(in_progress=False).latest('date')
        except ReportForm.DoesNotExist:
            raise Exception('Подходящий отчёт ФО не найден')

        self.report_form_row_query = ReportFormRow.objects.filter(
            report=self.report_form,
            unit__kind_id=UnitKind.DOU,
        )

    def _sum(self, name, data, age_cat=AGE_CATEGORIES_FULL):
        """Суммирование данных по возрастным категориям."""
        result = 0
        for key in list(age_cat.keys()):
            result += data[get_name(name, key)]
        return result

    def check(self):
        """Запускаем проверки на всех организациях"""
        report = self.report_form
        print(f'Найден отчет "{report.presentation}" (id={report.id})')

        report_rows_count = self.report_form_row_query.count()
        if not report_rows_count:
            raise Exception('Нет данных об организациях в отчёте')

        all_errors_data = defaultdict(list)

        for report_form_row in tqdm(
            self.report_form_row_query.iterator(chunk_size=100),
            total=report_rows_count,
            desc='Обработка организаций в отчёте',
        ):
            for error_data in self.get_report_form_row_errors(report_form_row):
                if error_data:
                    all_errors_data[error_data.test_name].append(error_data)

        if not any(bool(v) for v in all_errors_data.values()):
            print('Ошибок не найдено')
            return

        self.write_errors_to_file(all_errors_data)

    @staticmethod
    def write_errors_to_file(all_errors_data):
        """Вывод данных об ошибках в файл."""

        with WorkBookWriter(OUTPUT_FILE_NAME, OUTPUT_HEADERS) as writer:
            sorted_dict_items = sorted(all_errors_data.items(), key=lambda x: x[0])

            for name, error_data_list in sorted_dict_items:
                if not error_data_list:
                    continue
                for error_data in error_data_list:
                    writer.write_row_data(error_data)
        print(f'Данные об ошибках выведены в файл "{OUTPUT_FILE_NAME}"')

    def get_report_form_row_errors(self, report_form_row):
        """Генератор, который возвращает ошибки для отчёта по организации."""

        unit = report_form_row.unit
        enrolled_result = ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.ENROLLED)

        # enrolled в XML по всем группам учреждения равен показателю 19
        dou_data = DouData(report_form_row.unit, self.report_form)
        dou_groups = list(chain(*(building['groups'] for building in dou_data.buildings)))

        # Настройка фильтрации групп
        filter_groups = partial(filter_dou_groups, dou_groups)
        komp_and_kombi_groups = partial(filter_groups, orientation=GROUP_ORIENT_KOMP_AND_KOMBI)

        # ovz_deti в XML по всем группам учреждения равен 30.1 + 30.2
        yield get_error_data_if_not_equal(
            TestNames.sum_30_1_and_30_2,
            sum_ovz_deti_in_groups(dou_groups),
            self._sum('30_1', enrolled_result) + self._sum('30_2', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.1 равна сумме значений тег ovz_deti
        # в сумме по всем группам с тегом orientation=2 и 3 и
        # тегом ovz_type=1.
        ovz_deti_deafness_1 = sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type=[1]))
        yield get_error_data_if_not_equal(
            TestNames.sum_22_1_and_ovz_orientation_2_or_3,
            ovz_deti_deafness_1,
            self._sum('22_1', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.1.1 равна сумме значений тега
        #  ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=1.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_1_1_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[1])),
            self._sum('22_1_1', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.1.2 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=2.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_1_2_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[2])),
            self._sum('22_1_2', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.2 равна сумме значений тег ovz_deti
        # в сумме по всем группам с тегом orientation=2 и 3 и
        # тегом ovz_type=2.
        ovz_deti_deafness_2 = sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type=[2]))
        yield get_error_data_if_not_equal(
            TestNames.sum_22_2_and_ovz_orientation_2_or_3,
            ovz_deti_deafness_2,
            self._sum('22_2', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.3.1 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=3.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_3_1_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[3])),
            self._sum('22_3_1', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.3.2 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=4.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_3_2_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[4])),
            self._sum('22_3_2', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.5.1 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=7.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_5_1_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[7])),
            self._sum('22_5_1', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.5.2 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=8.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_5_2_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[8])),
            self._sum('22_5_2', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.8.1 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=11.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_8_1_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[11])),
            self._sum('22_8_1', enrolled_result),
            unit,
        )

        # сумма значений показателя 22.8.2 равна сумме значений тега
        # ovz_deti по всем группам с тегом orientation=2 и 3
        # и тегом ovz_type_new=12.
        yield get_error_data_if_not_equal(
            TestNames.sum_22_8_2_and_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups(ovz_type_new=[12])),
            self._sum('22_8_2', enrolled_result),
            unit,
        )

        # Сумма 22.1+22.2.+22.3.+22.4.+22.5.+22.6.+22.7.+22.8 равна
        # числу детей с ОВЗ (тег ovz_deti в сумме по всем группам
        # с тегом orientation=2 и 3)
        sum_22 = sum(self._sum(f'22_{x}', enrolled_result) for x in range(1, 9))
        yield get_error_data_if_not_equal(
            TestNames.sum_22_x_and_sum_ovz_orientation_2_or_3,
            sum_ovz_deti_in_groups(komp_and_kombi_groups()),
            sum_22,
            unit,
        )


class Command(BaseCommand):
    """Проверяет сборку ФО на ошибки."""

    def add_arguments(self, parser):
        parser.add_argument('--report_id', type=int, help='id отчета для проверки')

    def handle(self, *args, **kwargs):
        check_list_obj = GisdoCheckListsOvzDeti(kwargs['report_id'])
        check_list_obj.check()
