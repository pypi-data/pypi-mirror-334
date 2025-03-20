from __future__ import (
    absolute_import,
    unicode_literals,
)

import datetime

from future.builtins import (
    range,
)

from kinder.core.children.tests import (
    factory_child,
)
from kinder.core.declaration.tests import (
    factory_declaration,
)
from kinder.core.declaration_status.models import (
    DeclarationStatus,
)
from kinder.core.unit.models import (
    Unit,
    UnitKind,
)
from kinder.core.unit.tests import (
    factory_unit,
)

from gisdo.collector import (
    DataCollector,
)
from gisdo.models import (
    ReportForm,
    ReportFormRow,
)
from gisdo.service import (
    ReportService,
)
from gisdo.utils import (
    UnitHelper,
)

from .factory_gisdo import (
    GisdoUnitFactory,
)


def get_dou_for_mo(mo):
    """
    Возвращает список дочерних ДОУ
    :param mo:
    :return:
    """
    if mo.kind_id != UnitKind.MO:
        return []
    return list(mo.get_descendants().filter(kind__id=UnitKind.DOU))


class TestDataCollector(DataCollector):
    """Тестовый сборщик данных по ДОУ.

    Позволяет указывать только нужные для сбора группы данных для ускорения.

    collect_only - список типов данных, которые будут собираться:
        applications / queues / enrolled / capacities

    """

    collect_mapping = {
        'applications': '_collect_applications_data',
        'queues': '_collect_queue_data',
        'enrolled': '_collect_enrolled_data',
        'capacities': '_collect_capacities',
    }

    def __init__(self, mo, unit_helper, report_start_date, collect_only=None):
        super(TestDataCollector, self).__init__(mo, unit_helper, report_start_date)
        self.collect_only = collect_only

    def _dou_collect(self, report_form, dou):
        if self.collect_only is None:
            super(TestDataCollector, self)._dou_collect(report_form, dou)
        else:
            params = dict(report=report_form, unit=dou)

            for data_type, collect_func_name in list(self.collect_mapping.items()):
                collect_func = getattr(self, collect_func_name)
                params[data_type] = self.json_dumps(collect_func(dou) if data_type in self.collect_only else {})

            ReportFormRow.objects.get_or_create(**params)


class TestReportService(ReportService):
    """Запускает сборку отчета ФО в синхронном режиме,
    не рекомендуется для использования для реальных данных,
    только для тестовых, для небольшого объема,
    для проверки работоспособности тестов.

    Позволяет указывать только нужные для сбора группы данных для ускорения.

    collect_only - список данных которые будут собираться:
        'applications' / 'queues' / 'enrolled' / 'capacities'

    """

    def __init__(self, main_unit, set_progress_func=None, user=None, collect_only=None):
        super(TestReportService, self).__init__(main_unit, set_progress_func, user)
        self.collect_only = collect_only

    def _collect_data(self, mo_id, report_form_id):
        """копипаст gisdo.service.collect_data"""
        mo = Unit.objects.get(id=mo_id)
        report_form = ReportForm.objects.get(id=report_form_id)

        main_report_unit = report_form.unit
        unit_helper = UnitHelper(main_report_unit)

        data = None
        exception = None

        report_start_date = report_form.date.date()
        try:
            data = TestDataCollector(mo, unit_helper, report_start_date, self.collect_only).collect(report_form)
        # Отложенное исключение
        except Exception as e:
            exception = e
        return mo.id, data, exception

    def collect(self, send=True):
        collect_data_results = (
            self._collect_data(mo.id, self._report_form.id) for mo in self._unit_helper.get_report_units()
        )

        # Обрабатываем результаты завершившихся задач
        for mo_id, task_result, exception in collect_data_results:
            # Выбрасываем отложенное исключение
            if exception:
                raise exception
            self._update_data(task_result)

        self._create_region_report_form_row()

        self._report_form.in_progress = False
        self._report_form.date = datetime.datetime.now()
        self._report_form.save()


def make_dou_list(count_mo=3, count_dou=10):
    """Создает учреждения и ссылку в гисдо модели на них
    :param count_mo:
    :param count_dou:
    :return:
    """
    region = factory_unit.UnitRFactory()
    mo_list = []
    dou_list = []
    for i in range(0, count_mo):
        mo = factory_unit.UnitMoFactory(parent=region)
        mo_list.append(mo)
        for j in range(0, count_dou):
            dou = factory_unit.UnitDouFactory(parent=mo)
            GisdoUnitFactory(unit=dou)
            dou_list.append(dou)
    return region, mo_list, dou_list


def make_decl_list(mo_list, statuses, count_decl=10):
    """Создает рандомные заявления
    :param mo_list:
    :param statuses:
    :param count_decl:
    :return:
    """
    decl_list = []
    for mo in mo_list:
        dou_list = get_dou_for_mo(mo)
        for dou in dou_list:
            for status in statuses:
                for i in range(0, count_decl):
                    child = factory_child.ChildF.create()
                    decl_list.append(
                        factory_declaration.DeclarationF.create(
                            children=child, mo=mo, status=DeclarationStatus.get_by_code(status)
                        )
                    )
