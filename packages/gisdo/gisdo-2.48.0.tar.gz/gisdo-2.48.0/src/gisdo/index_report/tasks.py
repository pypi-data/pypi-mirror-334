import datetime
import traceback

from celery.result import (
    states,
)
from django.utils.safestring import (
    mark_safe,
)

from educommon.async_task.models import (
    AsyncTaskStatus,
)

from kinder.core.async_tasks.tasks import (
    AsyncTask,
    celery_app,
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
from gisdo.utils import (
    UnitHelper,
)


@celery_app.task(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)
def collect_data(mo_id, main_report_unit, indexes):
    """
    Асинхронная задача сбора данных по организации.

    :param mo_id: kinder.core.unit.models.Unit - Муниципальное образование.
    :param main_report_unit: Организация отчета.
    :param indexes: Индексы по которым идет сборка
    """

    mo = Unit.objects.get(id=mo_id)
    unit_helper = UnitHelper(main_report_unit)

    data = None
    exception = None

    report_start_date = datetime.date.today()

    from .collector import (
        ReportDataCollector,
    )

    try:
        data = ReportDataCollector(mo, unit_helper, report_start_date, indexes).collect()
    except Exception as e:
        Logger.add_record(traceback.format_exc(), level=Logger.ERROR)
        exception = e
    return mo.id, data, exception


@celery_app.task(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)
def build_mo_data(mo_data, indexes, **kw):
    """Задача построения отчета"""
    from .reports import (
        IndexReport,
    )

    report = IndexReport(mo_data, indexes)
    result_name = report.build()

    return result_name


class UnloadChildrenByIndexTask(AsyncTask):
    """Задача отчета "Выгрузка детей по показателю/тегу ФО"."""

    description = 'Выгрузка детей по показателю/тегу ФО.'
    queue = gs_settings.CELERY_WORKER_TASK_QUEUE

    def process(self, *args, **kwargs):
        unit_id = kwargs.get('unit_id')
        indexes = kwargs.get('indexes', [])

        self.set_progress('Подсчет показателей...', task_state=AsyncTaskStatus.STARTED)

        unit = Unit.objects.get(id=unit_id)

        from .service import (
            IndexReportService,
        )

        result_name = IndexReportService(unit, indexes, self.set_progress).collect_and_build()

        url = f'{gs_settings.DOWNLOADS_URL}/{result_name}.xlsx'
        message_with_link = mark_safe(f'<a href="{url}" target="_blank">Открыть</a>')
        self.set_progress(values={'Ссылка на скачивание файла': message_with_link})

        return self._result_message('Формирование отчёта завершено.', state=states.SUCCESS)


celery_app.register_task(UnloadChildrenByIndexTask)
