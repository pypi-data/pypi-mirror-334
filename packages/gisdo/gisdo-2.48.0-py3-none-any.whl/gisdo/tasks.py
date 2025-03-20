import datetime
import logging
import traceback

from celery.result import (
    states,
)
from django.utils import (
    timezone,
)
from django.utils.safestring import (
    mark_safe,
)
from future.builtins import (
    range,
    str,
)

from educommon.async_task.models import (
    AsyncTaskStatus,
    AsyncTaskType,
)
from m3.actions import (
    ApplicationLogicException,
)

from kinder import (
    celery_app,
)
from kinder.core.async_tasks.tasks import (
    AsyncTask,
)
from kinder.core.helpers import (
    get_current_user,
)
from kinder.core.unit.models import (
    Unit,
    UnitKind,
)
from kinder.users.models import (
    UserProfile,
)

from gisdo import (
    settings as gs_settings,
)
from gisdo.exceptions import (
    ReportGenerationException,
)
from gisdo.logger import (
    Logger,
)
from gisdo.models import (
    GisdoUnit,
    ReportForm,
    ReportFormRow,
    ScheduleSettings,
)
from gisdo.reports import (
    ReportFormReport,
)
from gisdo.service import (
    ReportService,
    send_report,
)


log = logging.getLogger('gisdo')


def _get_report_progress(current_unit_num, units_count):
    """
    Подсчет прогресса выполнения.

    :param current_unit_num - порядковый номер текущей организации
    :param units_count - количество организаций

    """

    return int(100 * float(current_unit_num) / float(units_count))


class Report(AsyncTask):
    """
    Отчет по собранным показателям

    """

    description = 'Отчет по собранным показателям'
    stop_executing = False
    task_type = AsyncTaskType.REPORT
    state = {'values': {}, 'description': 'Неизвестно', 'progress': 'Неизвестно'}

    def process(self, result_name, report_id, full_name, email, phone, *args, **kwargs):
        """Выполнение задачи"""

        self.set_progress('Формирование отчета...', task_state=AsyncTaskStatus.STARTED)

        self.result_name = result_name
        report = ReportFormReport(result_name)

        try:
            report_form = ReportForm.objects.get(id=report_id)
        except ReportForm.DoesNotExist:
            raise ReportGenerationException('Отсутствуют данные по организации')

        report_form_rows = ReportFormRow.objects.filter(report=report_form)
        rows_count = report_form_rows.count()

        row_number = 0
        row_data = []
        for report_form_row in report_form_rows:
            try:
                not_on_federal_report = report_form_row.unit.gisdo.not_on_federal_report
            except GisdoUnit.DoesNotExist:
                raise ApplicationLogicException(
                    f'Организация c ID={report_form_row.unit.pk} не найдена в модуле "Фед. отчетности"'
                )
            if report_form_row.unit.kind.id == UnitKind.DOU and not not_on_federal_report:
                self.set_progress(
                    f'Пeчать показателей по {report_form_row.unit.display()}.'
                    f' ({_get_report_progress(row_number, rows_count)}%)'
                )

                parent_unit = report_form_row.unit.get_mo() or report_form.unit

                ocato = parent_unit.ocato if parent_unit else ''
                try:
                    row_data.append(report.collect_row_data(report_form_row, report_form.date, ocato))
                except (KeyError, UnicodeDecodeError):
                    err_msg = f'При печате показателей по {report_form_row.unit.display()} произошла ошибка'
                    raise KeyError(err_msg)

                row_number += 1

        self.set_progress('Печать показателей завершена. Выполняется выгрузка файла')

        for page in range(5):
            report.flush_header(full_name, email, phone, page)
            report.flush_row_data(sorted(row_data, key=lambda x: x['mo']), page)

        report.reset_page()

        report.build()

        url = f'{gs_settings.DOWNLOADS_URL}/{self.result_name}.xlsx'
        message_with_link = mark_safe(f'<a href="{url}" target="_blank">Отчет сформирован</a>')

        self.set_progress(
            'Формирование отчёта завершено.',
            values={str(timezone.now()): message_with_link},
            task_state=states.SUCCESS,
        )

        return self.state


class CollectUnitsDataTask(AsyncTask):
    """
    Сбор и сохранение данных по организациям
    """

    description = 'Подсчет показателей'

    def process(self, user_id, unit_id, **kwargs):
        """Выполнение задачи"""

        self.set_progress('Подсчет показателей...', task_state=AsyncTaskStatus.STARTED)

        unit = Unit.objects.get(id=unit_id)
        user = UserProfile.objects.get(id=user_id)

        ReportService(
            unit,
            self.set_progress,
            user=user,
        ).collect(send=False)

        return self._result_message('Формирование завершено', state=states.SUCCESS)


class SendUnitsDataTask(CollectUnitsDataTask):
    """Отправка данных по организации."""

    description = 'Отправка показателей'

    def process(self, report_id, **kwargs):
        """Выполнение задачи"""

        message = 'Отправка показателей завершена'
        state = states.SUCCESS

        self.set_progress('Подготовка к отправке данные МО')

        schedule_settings = ScheduleSettings.get_settings()
        report_form = ReportForm.objects.get(id=report_id)
        not_send_mo = []
        try:
            not_send_mo = send_report(report_form, schedule_settings, report_form.unit, report_form.unit)
        except Exception as e:
            now = str(datetime.datetime.now())

            Logger.add_record(traceback.format_exc(), level=Logger.ERROR)
            self.set_progress(values={now: (f'При передаче данных произошла ошибка: {e}')})

            message = 'Отправка показателей завершена с ошибками'
            state = states.FAILURE
            self.set_exception_state(e)
        else:
            report_form.sent_time = datetime.datetime.now()
            report_form.save()

        if len(not_send_mo) > 0:
            message += f', не отправлено мо : {", ".join(not_send_mo)}'

        return self._result_message(message, state=state)


class CollectUnitDataPeriodicTask(AsyncTask):
    """
    Подсчет и отправка показателей
    (для периодического выполнения с celery beat).
    """

    description = 'Подсчет и отправка показателей'

    def process(self, *args, **kwargs):
        """Выполнение задачи"""

        self.set_progress('Подсчет показателей...', task_state=AsyncTaskStatus.STARTED)

        user = get_current_user()

        highest_units = Unit.objects.filter(parent__isnull=True)
        if highest_units.count() == 1:
            unit = highest_units[0]
        else:
            raise ApplicationLogicException('В корне дерева организаций должен быть только один элемент')

        ReportService(
            unit,
            self.set_progress,
            user=user,
        ).collect(send=True)

        return self._result_message('Формирование завершено', state=states.SUCCESS)


celery_app.register_task(Report)
celery_app.register_task(CollectUnitsDataTask)
celery_app.register_task(SendUnitsDataTask)
celery_app.register_task(CollectUnitDataPeriodicTask)
