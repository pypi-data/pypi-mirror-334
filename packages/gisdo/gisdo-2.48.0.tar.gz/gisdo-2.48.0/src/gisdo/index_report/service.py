import traceback

from celery import (
    group,
)
from celery.result import (
    allow_join_result,
)
from django.utils import (
    timezone,
)
from django.utils.functional import (
    cached_property,
)

from kinder.core.unit.models import (
    Unit,
)

from gisdo import (
    settings as gs_settings,
)
from gisdo.logger import (
    Logger,
)
from gisdo.models import (
    ScheduleSettings,
)
from gisdo.service import (
    ReportService,
)
from gisdo.utils import (
    UnitHelper,
)

from .tasks import (
    build_mo_data,
    collect_data,
)


class IndexReportService(ReportService):
    """Сборщик и построитель отчета "Выгрузка детей по показателю/тегу"."""

    def __init__(self, main_unit, indexes, set_progress_func=None, user=None):
        # Перекрыт, для того, чтобы не создавать объект ReportForm
        super(ReportService, self).__init__()

        self._unit_helper = UnitHelper(main_unit)
        self.main_report_unit = main_unit
        self.indexes = indexes

        self._set_progress = set_progress_func or (lambda x: x)
        self._schedule_settings = ScheduleSettings.get_settings()

    @cached_property
    def mo_count(self):
        return len(list(self._unit_helper.get_report_units()))

    def _collect_mo_data(self):
        """Сборка отчетов по каждому МО."""

        # Создаем группу параллельно выполняющихся подзадач
        # Каждая задача отвечает за подсчет показателей отдельного МО
        collect_data_tasks = group(
            collect_data.s(mo.id, self.main_report_unit, self.indexes) for mo in self._unit_helper.get_report_units()
        )

        collect_data_tasks_results = collect_data_tasks(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)

        mo_data_for_report = []
        with allow_join_result():
            for current_mo_num, (mo_id, task_result, exception) in enumerate(collect_data_tasks_results.iterate(), 1):
                self._set_progress(f'Обработано МО: {current_mo_num} из {self.mo_count}')

                mo = Unit.objects.get(id=mo_id)
                if exception:
                    status_msg = f'Во время сбора данных по {mo} произошла ошибка: {exception}'
                else:
                    mo_data_for_report.append(task_result)
                    status_msg = f'Данные по {mo} успешно собраны'

                self._set_progress(values={str(timezone.now()): status_msg})

        return mo_data_for_report

    def _build_report_data(self, mo_data_for_build):
        """Построение данных в xlsx отчет"""

        self._set_progress('Подготовка к формированнию данных отчета по показателям/тегу')

        result_name = None
        try:
            result_name = build_mo_data(mo_data_for_build, self.indexes)
            status_msg = f'Данные успешно сформированы'
        except Exception as e:
            Logger.add_record(traceback.format_exc(), level=Logger.ERROR)
            status_msg = f'При формировании данных произошла ошибка: {e}'
        self._set_progress(values={str(timezone.now()): status_msg})

        return result_name

    def collect_and_build(self):
        mo_data_for_build = self._collect_mo_data()
        result_name = self._build_report_data(mo_data_for_build)

        return result_name
