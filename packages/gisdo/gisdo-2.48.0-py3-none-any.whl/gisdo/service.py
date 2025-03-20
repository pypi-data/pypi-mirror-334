import base64
import datetime
import json
import socket
import sys
import time
import traceback
import zlib
from abc import (
    ABCMeta,
    abstractmethod,
)
from collections import (
    defaultdict,
)
from functools import (
    partial,
)

import suds
from celery import (
    group,
)
from celery.exceptions import (
    MaxRetriesExceededError,
)
from celery.result import (
    allow_join_result,
)
from dateutil.relativedelta import (
    relativedelta,
)
from django.db.models import (
    Q,
    Sum,
)
from django.template import (
    loader,
)
from django.utils import (
    timezone,
)
from django.utils.functional import (
    cached_property,
)
from future.builtins import (
    map,
    object,
    str,
)
from future.utils import (
    with_metaclass,
)
from suds.client import (
    Client,
)
from suds.sax.element import (
    Element,
)

from m3.plugins import (
    ExtensionManager,
)

from kinder.core.async_tasks.tasks import (
    celery_app,
)
from kinder.core.declaration.models import (
    Declaration,
)
from kinder.core.declaration_status.enum import (
    DSS,
)
from kinder.core.dict.models import (
    HNE,
    DouType,
    GroupTypeEnumerate,
    PostCategoryConstants,
    ProgramTypeEnum,
    UnitKind,
    WorkType,
)
from kinder.core.direct.models import (
    DRS,
    Direct,
)
from kinder.core.emie_unit.enum import (
    DisabilityConditionsEnum,
    EmieUnitRoomEnum,
)
from kinder.core.emie_unit.models import (
    DopService,
    EmieUnitModel,
)
from kinder.core.group.models import (
    Group,
    GroupStatusEnum,
    Pupil,
)
from kinder.core.journal.api import (
    get_attendance_without_holidays,
)
from kinder.core.unit.models import (
    BuildingTypes,
    FilialType,
    LocalityEnumerate,
    Unit,
)
from kinder.core.unit.payment.enum import (
    AgeEnumerate,
    PaymentTypeEnumerate,
    PaymentWorkTypeEnumerate,
)
from kinder.core.unit.payment.models import (
    CommonUnitPaymentInfo,
    GroupUnitPaymentInfo,
)

from gisdo import (
    constants as const,
    settings as gs_settings,
    xml_helpers,
)
from gisdo.exceptions import (
    ConnectingAtSendingReportException,
    DocumentCreateException,
    NoDataInMo,
    SendReportException,
    SOAPClientCreateException,
    XMLRenderException,
)
from gisdo.index.constants import (
    get_short_day_types,
)
from gisdo.index.enrolled import (
    Index,
)
from gisdo.logger import (
    Logger,
)
from gisdo.models import (
    AttendanceTransferType,
    GroupData as GroupDataModel,
    InstallationType,
    MOErrorResponse,
    ReportForm,
    ReportFormRow,
    ScheduleSettings,
)
from gisdo.utils import (
    DateMixin,
    get_file_url,
)

from .collector import (
    DataCollector,
    GisdoJsonDumpsMixin,
    ReportCacheMixin,
)
from .constants import (
    RESEND_FEDERAL_REPORT_ERRORS,
)
from .index.enrolled import (
    filters,
    kid_filters,
    ovz_filter,
)
from .index_report.helpers import (
    prep_directs_in_group_queries,
    prep_ind_29_1_queries,
    prep_ind_enrolled_data,
)
from .utils import (
    UnitHelper,
    get_report_date_or_today,
)
from .xml_helpers import (
    email_pattern,
    get_additional_info_by_dou,
    get_dou_filials,
    get_dou_status,
    get_dou_status_comment,
    get_dou_structure_type,
    get_dou_type,
    get_employers_in_dou_by_category,
    get_filial_num,
    get_groups_num,
    get_max_doo,
    get_num_advisory_centr,
    get_num_early_assistance,
    get_passport,
    get_unit_fias_house_guid,
    get_unit_license_partner_values,
    get_units_report,
    get_value,
    phone_pattern,
)


DEFAULT_WEAR_PERCENTAGE = 15


@celery_app.task(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)
def collect_data(mo_id, report_form_id):
    """Асинхронная задача сбора данных по организации.

    :param mo_id: kinder.core.unit.models.Unit - Муниципальное образование.
    :param report_form_id: Отчет.
    :return: mo, data, exception
    """
    mo = Unit.objects.get(id=mo_id)
    report_form = ReportForm.objects.get(id=report_form_id)

    main_report_unit = report_form.unit
    unit_helper = UnitHelper(main_report_unit)

    data = None
    exception = None

    report_start_date = report_form.date.date()

    try:
        data = DataCollector(mo, unit_helper, report_start_date).collect(report_form)

        GroupDataCollector(unit_helper, mo, report_start_date, report_form_id).collect()
    # Отложенное исключение
    except Exception as e:
        Logger.add_record(traceback.format_exc(), level=Logger.ERROR)
        exception = e
    return mo.id, data, exception


@celery_app.task(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)
def send_mo_data(mo_id, report_form_id, **kw):
    """Асинхронная задача отправки данных по организации.

    :param mo_id: kinder.core.unit.models.Unit - Муниципальное образование.
    :param report_form_id: Отчет.
    :param kw: Дополнительные параметры.
    :return: mo, exception
    """
    mo = Unit.objects.get(id=mo_id)
    report_form = ReportForm.objects.get(id=report_form_id)
    schedule_settings = ScheduleSettings.get_settings()
    exception = None
    try:
        send_report(report_form, schedule_settings, report_form.unit, mo)
    except (SOAPClientCreateException, ConnectingAtSendingReportException) as exc:
        # Произошла ошибка связанная с соединением сервера сервиса.
        # Перезапускаем таску через "countdown" максимум "max_retries" раз.
        try:
            Logger.add_record(
                f'Попытка {send_mo_data.request.retries}. '
                f'Ошибка соединения при отправке по МО "{mo.name}" '
                f'({exc.message}).',
                level=Logger.ERROR,
            )

            send_mo_data.retry(
                max_retries=kw.get('max_retries'),
                countdown=kw.get('countdown'),
            )
        except MaxRetriesExceededError:
            # Все возможные попытки не увенчались успехом.
            # Возвращаем исходную ошибку "exc".
            Logger.add_record(
                f'Все попытки отправки по МО "{mo.name}" не увенчались успехом.',
                level=Logger.ERROR,
            )
            exception = exc

    except Exception as e:
        # Произошла ошибка НЕ связанная с соединением сервера сервиса.
        Logger.add_record(
            f'Ошибка не связанная с соединением по МО "{mo.name}" {traceback.format_exc()}.',
            level=Logger.ERROR,
        )
        exception = e

    return mo.id, exception


def send_report(report_form, schedule_settings, main_report_unit, unit):
    """Функция выполяет отправку данных по организации.

    :param report_form: ReportForm отчет.
    :param schedule_settings: Настройки ФедОтч.
    :param main_report_unit: Территория в отчете.
    :param unit: Организация по которому отправляются данные.
    :return: list список не отправленных МО.

    """

    if not unit:
        unit = main_report_unit
    elif unit.kind.id not in [UnitKind.MO, UnitKind.REGION]:
        raise SendReportException()

    # Список МО по которым не удалось отправить данные
    not_send_mo = []
    region_data = unit.kind.id == UnitKind.REGION

    for mo in unit.get_descendants(include_self=True).filter(kind__id=UnitKind.MO):
        unit_helper = UnitHelper(main_report_unit)
        try:
            document = TemplateView(
                mo, report_form.date, schedule_settings, unit_helper, report_form, region_data=region_data
            )
            # Данные для региона передаются только в одном МО
            region_data = False
        except NoDataInMo as e:
            not_send_mo.append(mo.name)
            Logger.add_record(f'Ошибка {e.message} по МО; {mo.name}', level=Logger.WARNING)
            continue
        except Exception:
            Logger.add_record('\n'.join(traceback.format_exception(*sys.exc_info())), level=Logger.ERROR)
            raise DocumentCreateException()

        try:
            xml_content = render_xml_template(schedule_settings, document, mo.octmo)
        except NoDataInMo as e:
            not_send_mo.append(mo.name)
            Logger.add_record(
                f'Ошибка {e.message} по МО; {mo.name}',
                level=Logger.ERROR,
            )
            continue
        except Exception:
            Logger.add_record('\n'.join(traceback.format_exception(*sys.exc_info())), level=Logger.ERROR)
            raise XMLRenderException()

        try:
            error = ''
            Transport(schedule_settings).send(xml_content)
        except SendReportException as e:
            error = e.message
            raise
        finally:
            MOErrorResponse.objects.update_or_create(mo=mo, defaults={'error': error})

    return not_send_mo


def get_mo_for_resend_query():
    """Возвращает QuerySet с МО, при отправке которых произошла ошибка из
    RESEND_FEDERAL_REPORT_ERRORS"""

    errors_filter = Q()
    for error in RESEND_FEDERAL_REPORT_ERRORS:
        errors_filter |= Q(error__startswith=error)

    return MOErrorResponse.objects.filter(errors_filter)


def get_mo_for_resend_count():
    """Возвращает число МО, при отправке которых произошла ошибка из
    RESEND_FEDERAL_REPORT_ERRORS"""

    return get_mo_for_resend_query().count()


def resend_mo_data(report_id):
    """
    Переотправка ФО для МО, при отправке которых была получена ошибка из
    списка RESEND_FEDERAL_REPORT_ERRORS

    :param report_id: Идентификатор отчёта
    """

    schedule_settings = ScheduleSettings.get_settings()

    units_with_errors = get_mo_for_resend_query()
    units_with_errors_count = get_mo_for_resend_count()

    for attempt in range(schedule_settings.resend_count):
        send_data_tasks = group(
            send_mo_data.s(
                response.mo_id,
                report_id,
            )
            for response in units_with_errors
        )

        send_data_tasks_results = send_data_tasks.skew(start=1, stop=units_with_errors_count)(
            queue=gs_settings.CELERY_WORKER_TASK_QUEUE
        )

        for mo_id, exception in send_data_tasks_results.iterate():
            mo = Unit.objects.get(id=mo_id)
            attempt_log = f'Переотправка показателей по {mo}. Попытка {attempt + 1} ({str(timezone.now())})'
            if exception:
                yield {attempt_log: f'При переотправке данных произошла ошибка: {exception}'}
            else:
                units_with_errors_count -= 1
                yield {attempt_log: f'Данные успешно переотправлены'}

        if not units_with_errors_count:
            break


def render_xml_template(schedule_settings, document, octmo):
    """Функция подготавливает данные к отправке.

    1) Рендерим шаблон документом document.
    2) Сжимаем, при включенной настройке.
    3) Кодируем в base64.

    """

    xml_string = loader.render_to_string('ws/gisdo_request_template_5_0.xml', {'doc': document}).encode('utf-8')

    ExtensionManager().execute('write_xml', xml_string, octmo)

    if schedule_settings.zip_xml:
        xml_string = zlib.compress(xml_string)[2:-4]

    encoded_xml = base64.b64encode(xml_string)

    return encoded_xml


class ReportService(GisdoJsonDumpsMixin, ReportCacheMixin):
    """Сборщик и отправщик данных фед. отчетности."""

    def __init__(self, main_unit, set_progress_func=None, user=None):
        super(ReportService, self).__init__()

        self._unit_helper = UnitHelper(main_unit)
        self._report_form = ReportForm.objects.create(
            user=user,
            unit=main_unit,
            in_progress=True,
        )
        self._set_progress = set_progress_func or (lambda x: x)
        self._schedule_settings = ScheduleSettings.get_settings()

    @cached_property
    def mo_count(self):
        return len(list(self._unit_helper.get_report_units()))

    def _update_data(self, mo_data):
        if self._unit_helper.is_region:
            self._update_cache(mo_data[self.APPLICATIONS], self.APPLICATIONS)
            self._update_cache(mo_data[self.QUEUES], self.QUEUES)
            self._update_cache(mo_data[self.ENROLLED], self.ENROLLED)
            self._update_cache(mo_data[self.CAPACITIES], self.CAPACITIES)

    def _create_region_report_form_row(self):
        """Создает строку отчета с данными по региону."""
        if self._unit_helper.is_region:
            ReportFormRow.objects.update_or_create(
                report=self._report_form,
                unit=self._unit_helper.get_main_unit(),
                defaults=dict(
                    applications=self.json_dumps(self._cache[self.APPLICATIONS]),
                    queues=self.json_dumps(self._cache[self.QUEUES]),
                    enrolled=self.json_dumps(self._cache[self.ENROLLED]),
                    capacities=self.json_dumps(self._cache[self.CAPACITIES]),
                ),
            )

    def _collect_mo_data(self):
        """Сборка отчетов по каждому МО."""

        # Создаем группу параллельно выполняющихся подзадач
        # Каждая задача отвечает за подсчет показателей отдельного МО
        collect_data_tasks = group(
            collect_data.s(mo.id, self._report_form.id) for mo in self._unit_helper.get_report_units()
        )

        collect_data_tasks_results = collect_data_tasks(queue=gs_settings.CELERY_WORKER_TASK_QUEUE)

        mo_for_send = []
        with allow_join_result():
            for current_mo_num, (mo_id, task_result, exception) in enumerate(collect_data_tasks_results.iterate(), 1):
                self._set_progress(f'Обработано МО: {current_mo_num} из {self.mo_count}')

                mo = Unit.objects.get(id=mo_id)
                if exception:
                    status_msg = f'Во время сбора данных по {mo} произошла ошибка: {exception}'
                else:
                    self._update_data(task_result)
                    mo_for_send.append(mo)
                    status_msg = f'Данные по {mo} успешно собраны'

                self._set_progress(values={str(timezone.now()): status_msg})

        self._create_region_report_form_row()

        self._report_form.in_progress = False
        self._report_form.save()

        return mo_for_send

    def _send_mo_data(self, mo_for_send):
        """Отправка успешно собранных отчетов."""

        self._set_progress('Подготовка к отправке данных МО')

        minutes, max_retries = self._schedule_settings.get_interval_and_count_retries()

        # Создаем группу параллельно выполняющихся подзадач
        # Каждая задача отвечает за отправку показателей отдельного МО
        # Замечание: если подзадача выполнилась с ошибкой связанной с
        #   недоступностью сервера, то она будет перезапущена через
        #   "countdown" секунд максимум "max_retries" раз.
        #   И только по завершению всех возможных попыток всех подзадач
        #   группа подзадач считается выполненной.
        send_data_tasks = group(
            send_mo_data.s(mo.id, self._report_form.id, countdown=minutes * 60, max_retries=max_retries)
            for mo in mo_for_send
        )

        # добавляем задержку каждой подзадачи на 1 секунду

        # Из-за бага в celery приходится делать принт чтоб задачи не потерялись
        # Исправили в 5.1.0 (https://github.com/celery/celery/commit/7dc76ff3bd93ffca9abcc8130b6eea436a6bae49)
        # Так что после перехода на celery 5 можно убрать
        print(send_data_tasks)
        send_data_tasks_results = send_data_tasks.skew(start=1, stop=len(mo_for_send))(
            queue=gs_settings.CELERY_WORKER_TASK_QUEUE
        )

        send_error_count = 0
        with allow_join_result():
            for current_mo_num, (mo_id, exception) in enumerate(send_data_tasks_results.iterate(), 1):
                self._set_progress(f'Отправлены данные МО: {current_mo_num} из {self.mo_count}')

                mo = Unit.objects.get(id=mo_id)
                if exception:
                    status_msg = f'При передаче данных по {mo} произошла ошибка: {exception}'
                    send_error_count += 1
                else:
                    status_msg = f'Данные по {mo} успешно отправлены'

                self._set_progress(values={str(timezone.now()): status_msg})

        # Если все пакеты были отправлены то считаем что отчет отправлен
        if send_error_count == 0:
            self._report_form.sent_time = timezone.now()
            self._report_form.save()
        else:
            self._set_progress('Переотправка запросов')
            errors_before_resending = get_mo_for_resend_count()

            for result in resend_mo_data(self._report_form.id):
                self._set_progress(values=result)

            resent = errors_before_resending - get_mo_for_resend_count()

            if resent == send_error_count:
                self._report_form.sent_time = timezone.now()
                self._report_form.save()

    def collect(self, send=True):
        mo_for_send = self._collect_mo_data()
        if send:
            self._send_mo_data(mo_for_send)


class IndicesProcessor(object):
    """
    Генерирует правильный вид показателей для вставки их в xml
    """

    AGE_CATEGORIES_MAP = {
        const.ALL: 'all',
        const.AGE_CATEGORIES_FULL['2-6-MONTHS']: 'h_00_05',
        const.AGE_CATEGORIES_FULL['0.5-1-YEARS']: 'h_05_10',
        const.AGE_CATEGORIES_FULL['1-1.5-YEARS']: 'h_10_15',
        const.AGE_CATEGORIES_FULL['1.5-2-YEARS']: 'h_15_20',
        const.AGE_CATEGORIES_FULL['2-2.5-YEARS']: 'h_20_25',
        const.AGE_CATEGORIES_FULL['2.5-3-YEARS']: 'h_25_30',
        const.AGE_CATEGORIES_FULL['3-3.5-YEARS']: 'h_30_35',
        const.AGE_CATEGORIES_FULL['3.5-4-YEARS']: 'h_35_40',
        const.AGE_CATEGORIES_FULL['4-4.5-YEARS']: 'h_40_45',
        const.AGE_CATEGORIES_FULL['4.5-5-YEARS']: 'h_45_50',
        const.AGE_CATEGORIES_FULL['5-5.5-YEARS']: 'h_50_55',
        const.AGE_CATEGORIES_FULL['5.5-6-YEARS']: 'h_55_60',
        const.AGE_CATEGORIES_FULL['6-6.5-YEARS']: 'h_60_65',
        const.AGE_CATEGORIES_FULL['6.5-7-YEARS']: 'h_65_70',
        const.AGE_CATEGORIES_FULL['7-7.5-YEARS']: 'h_70_75',
        const.AGE_CATEGORIES_FULL['7.5-99-YEARS']: 'h_75_e',
        const.AGE_CATEGORIES_EIGHT['2-1-YEARS']: 'y_0_1',
        const.AGE_CATEGORIES_EIGHT['1-2-YEARS']: 'y_1_2',
        const.AGE_CATEGORIES_EIGHT['2-3-YEARS']: 'y_2_3',
        const.AGE_CATEGORIES_EIGHT['3-4-YEARS']: 'y_3_4',
        const.AGE_CATEGORIES_EIGHT['4-5-YEARS']: 'y_4_5',
        const.AGE_CATEGORIES_EIGHT['5-6-YEARS']: 'y_5_6',
        const.AGE_CATEGORIES_EIGHT['6-7-YEARS']: 'y_6_7',
        const.AGE_CATEGORIES_EIGHT['7-7.5-YEARS']: 'y_7_e',
    }

    @staticmethod
    def process(dirty_indices):
        result = []

        def get_valid_index(index):
            return 'ind_{0}'.format(index.replace('.', '_'))

        def get_valid_age_category(age_category):
            try:
                return IndicesProcessor.AGE_CATEGORIES_MAP[age_category]
            except KeyError:
                return age_category

        for dirty_index in dirty_indices:
            index = {
                'name': get_valid_index(dirty_index),
                'age_categories': [],
            }

            for dirty_age_category in dirty_indices[dirty_index]:
                index['age_categories'].append(
                    {
                        'name': get_valid_age_category(dirty_age_category),
                        'value': str(dirty_indices[dirty_index][dirty_age_category]),
                    }
                )

            result.append(index)

        return result


class CounterProxy(object):
    @staticmethod
    def transform(counter):
        result = []
        for index_id in counter:
            index = {'id': index_id, 'indexes': []}

            for age_cat in counter[index_id]:
                index['indexes'].append({'category': age_cat, 'count': counter[index_id][age_cat]})

            result.append(index)

        return result


class TemplateView(object):
    """Объект, который рендерится в шаблон XML."""

    def __init__(self, mo, date, schedule_settings, unit_helper, report_form, region_data=False):
        self._mo = mo

        try:
            self._region = self._mo.get_ancestors(include_self=True).get(kind=UnitKind.REGION)
        except Unit.DoesNotExist:
            self._region = None

        self._date = date.date()
        self._gisdo_settings = schedule_settings
        self._unit_helper = unit_helper
        self._report_form = report_form
        self._region_data = region_data

    @property
    def header(self):
        """Данные для заголовка XML.

        То, что передается в теге system.

        """

        return {
            'own_server': self._gisdo_settings.server_location,
            'system_name': self._gisdo_settings.system_name,
            'version': gs_settings.KINDER_VERSION,
            'email': self._gisdo_settings.email,
            'install_type': (
                self._gisdo_settings.installation_type
                if self._gisdo_settings.installation_type
                else InstallationType.REGIONAL
            ),
        }

    @property
    def parent_pay(self):
        """Данные род платы."""

        data = {
            'has_region_data': self._region_data,
            'founders': [],
            'max_pay': None,
            'mid_pay': None,
            'crit_npa': None,
        }
        if self._region is not None:
            has_gov = (
                self._region.get_descendants().filter(kind=UnitKind.DOU, dou_type__code=DouType.GOVERNMENT).exists()
            )
        else:
            has_gov = self._mo.get_descendants().filter(kind=UnitKind.DOU, dou_type__code=DouType.GOVERNMENT).exists()

        has_mun = self._mo.get_descendants().filter(kind=UnitKind.DOU, dou_type__code=DouType.MUNICIPAL).exists()

        if self._region is not None:
            data['max_pay'] = ParentPayData(unit=self._region).get_parent_pay_data_for_payment(
                PaymentTypeEnumerate.MAX_PAY
            )

            data['mid_pay'] = ParentPayData(unit=self._region).get_parent_pay_data_for_payment(
                PaymentTypeEnumerate.MID_PAY
            )

        # Добавляем founders если у региона подчиненные сады типа `GOVERNMENT`.
        # Передаем founders для всех МО, если задан REGION_CODE_FO
        # Если не передан - только в первом МО
        if has_gov and (self._region_data or gs_settings.REGION_CODE_FO):
            data['founders'].append(
                ParentPayData(unit=self._region).get_parent_pay_data_for_payment(PaymentTypeEnumerate.PAY)
            )

        if has_mun:
            data['founders'].append(
                ParentPayData(unit=self._mo).get_parent_pay_data_for_payment(PaymentTypeEnumerate.PAY)
            )

        if self._region:
            region_payment_info = ParentPayData(unit=self._region).get_payment_info(PaymentTypeEnumerate.PAY)
        else:
            region_payment_info = None

        if region_payment_info is not None:
            if region_payment_info.need_criterion_legal_act_doc:
                data['crit_npa'] = get_file_url(region_payment_info, 'need_criterion_legal_act_doc')
            elif region_payment_info.need_criterion_legal_act_url:
                data['crit_npa'] = region_payment_info.need_criterion_legal_act_url
            else:
                data['crit_npa'] = ''

        if data.get('crit_npa'):
            data['crit_npa'] = data['crit_npa']
        else:
            data['crit_npa'] = ''

        return data

    @cached_property
    def municipality_unit(self):
        """Данные по муниципальным образованиям."""

        try:
            ext_unit = self._mo.ext_unit
            addr_binding_url = ext_unit.addr_binding_url
            service_info_url = ext_unit.service_info_url
        except EmieUnitModel.DoesNotExist:
            ext_unit = None
            addr_binding_url = None
            service_info_url = None

        (
            no_doo_act_0_3,
            no_doo_act_3_7,
            no_doo_def_0_3,
            no_doo_def_3_7,
            medic_0_3,
            medic_3_7,
            family_0_3,
            family_3_7,
        ) = self.municipality_common_info()

        try:
            reg_octmo = self._mo.get_ancestors(include_self=True).get(kind=UnitKind.REGION).octmo or ''
        except Unit.DoesNotExist:
            reg_octmo = ''

        def _check_value(name, default='нет'):
            return getattr(self._mo, name, default) or default

        dou_list = self._unit_helper.get_mo_units(self._mo.id)

        return {
            'oktmo': (self._mo.octmo or '')[:8],
            'reg_oktmo': gs_settings.REGION_CODE_FO or reg_octmo[:2],
            'epgu_link': _check_value('epgu_link', ''),
            'rpgu_link': _check_value('rpgu_link', ''),
            'name_mouo': _check_value('full_name', self._mo.name),
            'site_mouo': get_value(self._mo.site, 'нет'),
            'address_mouo': _check_value('address_full'),
            'email_mouo': (
                self._mo.email if self._mo.email and email_pattern.match(self._mo.email) is not None else 'нет'
            ),
            'phones_mouo': (
                self._mo.telephone
                if self._mo.telephone and phone_pattern.match(self._mo.telephone) is not None
                else 'нет'
            ),
            'time_mouo': _check_value('reception_time'),
            'regulation': get_value(service_info_url or get_file_url(ext_unit, 'service_info_doc')),
            'fix_area': get_value(addr_binding_url or get_file_url(ext_unit, 'addr_binding_doc')),
            'max_doo': get_max_doo(self._mo),
            'num_advisory_centr': get_num_advisory_centr(dou_list),
            'num_early_assistance': get_num_early_assistance(dou_list),
            'no_doo_act_0_3': no_doo_act_0_3,
            'no_doo_act_3_7': no_doo_act_3_7,
            'no_doo_def_0_3': no_doo_def_0_3,
            'no_doo_def_3_7': no_doo_def_3_7,
            'medic_0_3': medic_0_3,
            'medic_3_7': medic_3_7,
            'family_0_3': family_0_3,
            'family_3_7': family_3_7,
        }

    def municipality_common_info(self):
        """Данные, которые будут рендерятся в тег common."""

        today = timezone.now().date()

        no_doo_act_0_3 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=3),
                children__date_of_birth__lt=today,
                mo=self._mo,
                is_registered_in_absence=True,
            )
            .filter(Q(desired_date__lte=DateMixin.get_current_calendar_year_start()) | Q(desired_date__isnull=True))
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )
        no_doo_act_3_7 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=7),
                children__date_of_birth__lte=today - relativedelta(years=3),
                mo=self._mo,
                is_registered_in_absence=True,
            )
            .filter(Q(desired_date__lte=DateMixin.get_current_calendar_year_start()) | Q(desired_date__isnull=True))
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )

        no_doo_def_0_3 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=3),
                children__date_of_birth__lt=today,
                mo=self._mo,
                is_registered_in_absence=True,
            )
            .filter(Q(desired_date__gt=DateMixin.get_current_calendar_year_start()))
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )
        no_doo_def_3_7 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=7),
                children__date_of_birth__lte=today - relativedelta(years=3),
                mo=self._mo,
                is_registered_in_absence=True,
            )
            .filter(Q(desired_date__gt=DateMixin.get_current_calendar_year_start()))
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )

        medic_0_3 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=3),
                children__date_of_birth__lt=today,
                mo=self._mo,
                is_not_attending=True,
            )
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )
        medic_3_7 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=7),
                children__date_of_birth__lte=today - relativedelta(years=3),
                mo=self._mo,
                is_not_attending=True,
            )
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )

        family_0_3 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=3),
                children__date_of_birth__lt=today,
                mo=self._mo,
                is_preschool_education=True,
            )
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )
        family_3_7 = (
            Declaration.objects.filter(
                children__date_of_birth__gte=today - relativedelta(years=7),
                children__date_of_birth__lte=today - relativedelta(years=3),
                mo=self._mo,
                is_preschool_education=True,
            )
            .exclude(status__code=DSS.ARCHIVE)
            .count()
        )

        return (
            no_doo_act_0_3,
            no_doo_act_3_7,
            no_doo_def_0_3,
            no_doo_def_3_7,
            medic_0_3,
            medic_3_7,
            family_0_3,
            family_3_7,
        )

    @property
    def units(self):
        """Данные по садам внутри муниципального образования."""

        dou_list = get_units_report(self._mo, self._unit_helper.get_mo_units(self._mo.id))

        # Признак наличия садов, по которым можно собрать данные
        have_data = len(dou_list)

        if not have_data:
            raise NoDataInMo(f'Нет садов в МО {self._mo} пригодных для отправки')

        for dou in dou_list:
            yield DouData(dou, self._report_form)


def get_ext_unit_param(unit, name, default):
    try:
        return getattr(unit.ext_unit, name, default)
    except EmieUnitModel.DoesNotExist:
        return default


_GROUP_TYPE_MAPPING = {
    GroupTypeEnumerate.DEV: '1',
    GroupTypeEnumerate.COMP: '2',
    GroupTypeEnumerate.COMBI: '3',
    GroupTypeEnumerate.HEALTH: '4',
    GroupTypeEnumerate.CARE: '56',
    GroupTypeEnumerate.FAMILY: '7',
}

_WORK_TYPE_MAPPING = {
    PaymentWorkTypeEnumerate.SHORT: '1',
    PaymentWorkTypeEnumerate.ABREV: '2',
    PaymentWorkTypeEnumerate.FULL: '3',
    PaymentWorkTypeEnumerate.EXTEND: '4',
    PaymentWorkTypeEnumerate.ALLDAY: '5',
}

_AGE_TYPE_MAPPING = {
    AgeEnumerate.AGE_0_3: 'age_0_3',
    AgeEnumerate.AGE_GT_3: 'age_3_8',
    AgeEnumerate.AGE_MIXED: 'age_mix',
}


class ParentPayData(object):
    """Данные по род плате."""

    def __init__(self, unit):
        self.unit = unit

        if self.unit.kind_id == UnitKind.REGION:
            self.oktmo = gs_settings.REGION_CODE_FO or (self.unit.octmo or '')[:2]
        else:
            self.oktmo = (self.unit.octmo or '')[:8]

    def get_payment_info(self, payment_type):
        """Данные оплаты (файлы)."""

        try:
            return CommonUnitPaymentInfo.objects.get(unit=self.unit, payment_type=payment_type)
        except CommonUnitPaymentInfo.DoesNotExist:
            return None

    @staticmethod
    def build_key(work_type, group_type, age_type):
        """Построение ключа для показателя."""

        return (
            f'or_{_GROUP_TYPE_MAPPING[group_type]}_time_{_WORK_TYPE_MAPPING[work_type]}_{_AGE_TYPE_MAPPING[age_type]}'
        )

    def get_parent_pay_data_for_payment(self, payment_type):
        """Получение всех данных для переданного типа оплаты."""

        result = {}

        for group_type in list(GroupTypeEnumerate.values.keys()):
            for work_type in list(PaymentWorkTypeEnumerate.values.keys()):
                for age_type in list(AgeEnumerate.values.keys()):
                    try:
                        result[self.build_key(work_type, group_type, age_type)] = self.get_parent_pay_data(
                            payment_type, work_type, group_type, age_type
                        )
                    except KeyError:
                        continue

        payment_info = self.get_payment_info(payment_type)

        if payment_info and payment_info.npa_pay_doc:
            result['npa_pay'] = get_file_url(payment_info, 'npa_pay_doc')
        elif payment_info and payment_info.npa_pay_url:
            result['npa_pay'] = payment_info.npa_pay_url
        else:
            result['npa_pay'] = ''

        if result['npa_pay']:
            result['npa_pay'] = result['npa_pay']

        result['type_pay'] = (payment_info and payment_info.type_pay) or ''
        result['change_pay'] = (payment_info and payment_info.change_pay) or ''

        result['oktmo'] = self.oktmo

        return result

    def get_parent_pay_data(self, payment_type, work_type, group_type, age_type):
        """Получение данных о род плате по заданным параметрам."""

        try:
            value = GroupUnitPaymentInfo.objects.get(
                unit=self.unit,
                payment_type=payment_type,
                group_type=group_type,
                age_type=age_type,
                work_type=work_type,
            ).value
        except GroupUnitPaymentInfo.DoesNotExist:
            return '0'

        return '{:.2f}'.format(value)


class DouData(object):
    """Класс формирует данные по ДОУ, которые рендерятся в шаблон."""

    def __init__(self, unit, report_form):
        self._unit = unit
        self._report_form = report_form

    @property
    def unit_id(self):
        """Возвращает id организации."""
        return self._unit.id

    def _advisory_centr(self):
        """заполняем настройки Сведения о консультационных центрах
        :return:
        """

        def _sum_data_advisory_centr(data_advisory_centr, get_param_unit):
            data_advisory_centr['fact'] = (
                1
                if (get_param_unit(name='counseling_center', default=False) or data_advisory_centr['fact'] == 1)
                else 0
            )

            data_advisory_centr['num_hits_personally'] += get_param_unit(name='num_hits_personally')
            data_advisory_centr['num_hits_distant'] += get_param_unit(name='num_hits_distant')
            data_advisory_centr['num_staff_member'] += get_param_unit(name='num_staff_member')
            data_advisory_centr['num_freelancer'] += get_param_unit(name='num_freelancer')

            #  1 = true, 0 = false, смотрим и у головой и филиалов и корпусов,
            #  если хотя бы у одного заполнено передаем 1
            data_advisory_centr['forma_1'] = (
                1
                if (get_param_unit(name='methodical_help', default=False) or data_advisory_centr['forma_1'] == 1)
                else 0
            )
            data_advisory_centr['forma_2'] = (
                1
                if (get_param_unit(name='psychpedagogical_help', default=False) or data_advisory_centr['forma_2'] == 1)
                else 0
            )
            data_advisory_centr['forma_3'] = (
                1
                if (get_param_unit(name='diagnostic_help', default=False) or data_advisory_centr['forma_3'] == 1)
                else 0
            )
            data_advisory_centr['forma_4'] = (
                1
                if (get_param_unit(name='consultation_help', default=False) or data_advisory_centr['forma_4'] == 1)
                else 0
            )

            data_advisory_centr['num_parent'] += get_param_unit(name='num_parent')
            data_advisory_centr['num_parent_family_0_15'] += get_param_unit(name='num_parent_family_0_15')
            data_advisory_centr['num_parent_family_15_3'] += get_param_unit(name='num_parent_family_15_3')
            data_advisory_centr['num_parent_family_3_7'] += get_param_unit(name='num_parent_family_3_7')
            data_advisory_centr['num_parent_family_7_8'] += get_param_unit(name='num_parent_family_7_8')
            data_advisory_centr['num_parent_not_edu_0_3'] += get_param_unit(name='num_parent_not_edu_0_3')
            data_advisory_centr['num_parent_not_edu_3_7'] += get_param_unit(name='num_parent_not_edu_3_7')
            data_advisory_centr['num_parent_not_edu_7_8'] += get_param_unit(name='num_parent_not_edu_7_8')
            data_advisory_centr['num_child'] += get_param_unit(name='num_child')
            data_advisory_centr['num_child_family_0_15'] += get_param_unit(name='num_child_family_0_15')
            data_advisory_centr['num_child_family_15_3'] += get_param_unit(name='num_child_family_15_3')
            data_advisory_centr['num_child_family_3_7'] += get_param_unit(name='num_child_family_3_7')
            data_advisory_centr['num_child_family_7_8'] += get_param_unit(name='num_child_family_7_8')
            data_advisory_centr['num_child_not_edu_0_3'] += get_param_unit(name='num_child_not_edu_0_3')
            data_advisory_centr['num_child_not_edu_3_7'] += get_param_unit(name='num_child_not_edu_3_7')
            data_advisory_centr['num_child_not_edu_7_8'] += get_param_unit(name='num_child_not_edu_7_8')

        data_advisory_centr = defaultdict(int)
        get_param_unit = partial(get_ext_unit_param, unit=self._unit, default=0)
        # Рассчитаем для головной
        _sum_data_advisory_centr(data_advisory_centr, get_param_unit)
        filials = xml_helpers.get_dou_filials(self._unit).select_related('filial')
        # Рассчитаем для филиалов
        for filial in (fd.filial for fd in filials.iterator()):
            get_param_unit = partial(get_ext_unit_param, unit=filial, default=0)
            _sum_data_advisory_centr(data_advisory_centr, get_param_unit)

        if data_advisory_centr['fact'] == 1:
            del data_advisory_centr['fact']
            param = {'fact': 1, 'data_advisory_centr': dict(data_advisory_centr)}
        else:
            param = {'fact': 0, 'data_advisory_centr': {}}
        return param

    def _get_early_assistant_data(self):
        """Данные для organization/early_assistant."""

        if (not hasattr(self._unit, 'ext_unit') or not self._unit.ext_unit.early_help_service) and not get_dou_filials(
            self._unit
        ).filter(filial__ext_unit__early_help_service=True).exists():
            result = {'fact': 0}
        else:
            result = {'fact': 1}

            dou_with_filials_query = Unit.objects.filter(
                Q(id=self._unit.id) | Q(id__in=get_dou_filials(self._unit).values_list('filial_id', flat=True))
            )

            fields_prefix = 'ext_unit__'

            # передаем суммы указанных показателей по учреждению и его филиалам
            fields_for_total = (
                ('u_num_hits_personally', 'num_hits_personally'),
                ('u_num_hits_distant', 'num_hits_distant'),
                ('num_parent_0_3', 'num_parent_0_3'),
                ('num_parent_3_8', 'num_parent_3_8'),
                ('num_child_0_3', 'num_child_0_3'),
                ('num_child_3_8', 'num_child_3_8'),
            )

            result.update(
                dou_with_filials_query.aggregate(
                    **{name_in_xml: Sum(fields_prefix + field_name) for field_name, name_in_xml in fields_for_total}
                )
            )

            # показатели которые смотрим и у головой и филиалов и корпусов,
            # если хотя бы у одного True - передаем 1 иначе 0
            fields_to_check = (
                ('early_methodical_help', 'forma_1'),
                ('early_psychological_help', 'forma_2'),
                ('early_diagnostical_help', 'forma_3'),
                ('early_consulting_help', 'forma_4'),
            )

            for field_name, name_in_xml in fields_to_check:
                filter_params = {fields_prefix + field_name: True}
                result.update({name_in_xml: int(dou_with_filials_query.filter(**filter_params).exists())})

        return result

    @cached_property
    def organization(self):
        """Данные для рендеринга в тег organization."""

        try:
            ext_unit = self._unit.ext_unit
            have_lekoteka = 1 if ext_unit.have_lekoteka else 0
            have_child_support_center = 1 if ext_unit.have_child_support_center else 0
            meal_serving_type = ext_unit.meal_serving_type or ''
        except EmieUnitModel.DoesNotExist:
            ext_unit = None
            meal_serving_type = ''
            have_lekoteka = 0
            have_child_support_center = 0

        num_filial = get_filial_num(self._unit)

        if Group.objects.filter(unit=self._unit, status=GroupStatusEnum.FACT).exists():
            num_building = num_filial + 1
        else:
            num_building = num_filial
        dou_status = get_dou_status(self._unit)

        license_, partner_doo = get_unit_license_partner_values(self._unit)

        result = {
            'code': self._unit.gisdo.doo_identity,
            'name': self._unit.name,
            'type': get_dou_type(self._unit),
            'status': dou_status,
            'commet_status': get_dou_status_comment(dou_status, self._unit),
            'structure': get_dou_structure_type(self._unit),
            'director': self._unit.boss_fio or 'нет',
            'worktime': (self._unit.reception_time or 'с 6.30 до 18.30 часов'),
            'license': license_,
            'type_area': (2 if self._unit.locality == LocalityEnumerate.RURAL else 1),
            'fias_org_guid': get_unit_fias_house_guid(self._unit),
            'org_address': (self._unit.address_full if self._unit.address_full else 'нет'),
            'website': get_value(self._unit.site, ''),
            'email': (
                self._unit.email
                if self._unit.email and (self._unit.email == 'нет' or email_pattern.match(self._unit.email) is not None)
                else ''
            ),
            'phone': (
                self._unit.telephone
                if self._unit.telephone and phone_pattern.match(self._unit.telephone) is not None
                else 'нет'
            ),
            'doo_number': self._unit.doo_number,
            'additional_education': get_additional_info_by_dou(self._unit),
            'features': get_additional_info_by_dou(self._unit, model=DopService),
            'num_filial': num_filial,
            'num_building': num_building,
            'num_group': get_groups_num(self._unit),
            'partner_doo': partner_doo,
            'lekoteka': have_lekoteka,
            'centre_game': have_child_support_center,
            'meal_serving_type': meal_serving_type,
            'passport': get_passport(ext_unit),
            'early_assistant_data': self._get_early_assistant_data(),
        }
        result.update(self._advisory_centr())
        return result

    @property
    def indices(self):
        """Показатели."""

        rows = ReportFormRow.objects.filter(unit=self._unit, report=self._report_form)

        indices = []
        for row in rows:
            index = {}
            index.update(json.loads(row.applications))
            index.update(json.loads(row.queues))
            index.update(json.loads(row.enrolled))
            index.update(json.loads(row.capacities))
            indices.extend(IndicesProcessor.process(index))

        return indices

    @property
    def buildings(self):
        """Данные по зданиям."""

        def get_building_type(unit):
            return unit.building_type or BuildingTypes.TYPICAL

        def get_depreciation(unit):
            return unit.percent_of_wear if self._unit.percent_of_wear is not None else str(DEFAULT_WEAR_PERCENTAGE)

        filials = xml_helpers.get_dou_filials(self._unit).select_related('filial')

        report_date = self._report_form.date.date() if self._report_form else datetime.date.today()

        parent_group_data = ParentGroupData(
            self._unit, report_date, filials, report_id=self._report_form.id if self._report_form else None
        )

        # головная организация передается только если у нее есть группы
        if xml_helpers.has_fact_groups(self._unit):
            type_building = get_building_type(self._unit)

            filial_flag = 1 if self._unit.is_filial == FilialType.FILIAL else 0

            filial_attr = 0 if type_building == BuildingTypes.SPECIAL_ADDITIONAL else filial_flag

            yield {
                'fias_house_guid': get_unit_fias_house_guid(self._unit),
                'id': '1' + str(self._unit.id),
                'name': self._unit.name,
                'plain_address': self._unit.address_full or 'нет',
                'depreciation': get_depreciation(self._unit),
                'building_type_area': (self._unit.locality or LocalityEnumerate.RURAL),
                'type_building': type_building,
                'filial': filial_attr,
                'groups': parent_group_data.groups,
                'status_building': str(xml_helpers.get_dou_status_building(self._unit, '')),
                'cabinet_psychologist': get_ext_unit_param(
                    self._unit, 'cabinet_psychologist', EmieUnitRoomEnum.NOT_EXISTS
                ),
                'cabinet_defectologist': get_ext_unit_param(
                    self._unit, 'cabinet_defectologist', EmieUnitRoomEnum.NOT_EXISTS
                ),
                'cabinet_logopedist': get_ext_unit_param(self._unit, 'cabinet_logopedist', EmieUnitRoomEnum.NOT_EXISTS),
                'cabinet_med': get_ext_unit_param(self._unit, 'cabinet_med', EmieUnitRoomEnum.NOT_EXISTS),
                'sport_gym': get_ext_unit_param(self._unit, 'gym', EmieUnitRoomEnum.NOT_EXISTS),
                'meeting_room': get_ext_unit_param(self._unit, 'music_room', EmieUnitRoomEnum.NOT_EXISTS),
                'pool': get_ext_unit_param(self._unit, 'swimming_pool', EmieUnitRoomEnum.NOT_EXISTS),
                'oda_territory': get_ext_unit_param(
                    self._unit, 'oda_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'oda_entrance': get_ext_unit_param(
                    self._unit, 'oda_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'oda_way': get_ext_unit_param(self._unit, 'oda_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'oda_room': get_ext_unit_param(self._unit, 'oda_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'oda_washroom': get_ext_unit_param(
                    self._unit, 'oda_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'oda_communication': get_ext_unit_param(
                    self._unit, 'oda_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'oda_path': get_ext_unit_param(self._unit, 'oda_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'oda_equipment': get_ext_unit_param(
                    self._unit, 'oda_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'vision_territory': get_ext_unit_param(
                    self._unit, 'vision_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'vision_entrance': get_ext_unit_param(
                    self._unit, 'vision_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'vision_way': get_ext_unit_param(self._unit, 'vision_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'vision_room': get_ext_unit_param(self._unit, 'vision_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'vision_washroom': get_ext_unit_param(
                    self._unit, 'vision_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'vision_communication': get_ext_unit_param(
                    self._unit, 'vision_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'vision_path': get_ext_unit_param(self._unit, 'vision_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'vision_equipment': get_ext_unit_param(
                    self._unit, 'vision_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'ear_territory': get_ext_unit_param(
                    self._unit, 'ear_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'ear_entrance': get_ext_unit_param(
                    self._unit, 'ear_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'ear_way': get_ext_unit_param(self._unit, 'ear_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'ear_room': get_ext_unit_param(self._unit, 'ear_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'ear_washroom': get_ext_unit_param(
                    self._unit, 'ear_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'ear_communication': get_ext_unit_param(
                    self._unit, 'ear_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
                'ear_path': get_ext_unit_param(self._unit, 'ear_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                'ear_equipment': get_ext_unit_param(
                    self._unit, 'ear_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                ),
            }

        for filial in (fd.filial for fd in filials.iterator()):
            # филиал передается только если у него есть группы
            if xml_helpers.has_fact_groups(filial):
                type_building = get_building_type(filial)

                filial_flag = 1 if filial.is_filial == FilialType.FILIAL else 0

                filial_attr = 0 if type_building == BuildingTypes.SPECIAL_ADDITIONAL else filial_flag

                yield {
                    'fias_house_guid': get_unit_fias_house_guid(filial),
                    'id': filial.id,
                    'name': filial.name,
                    'plain_address': filial.address_full or 'нет',
                    'depreciation': get_depreciation(filial),
                    'building_type_area': (self._unit.locality or LocalityEnumerate.RURAL),
                    'type_building': type_building,
                    'filial': filial_attr,
                    'groups': FilialGroupData(
                        filial,
                        parent_group_data,
                        report_date,
                        report_id=self._report_form.id if self._report_form else None,
                    ).groups,
                    'status_building': str(xml_helpers.get_dou_status_building(filial, '')),
                    'cabinet_psychologist': get_ext_unit_param(
                        filial, 'cabinet_psychologist', EmieUnitRoomEnum.NOT_EXISTS
                    ),
                    'cabinet_defectologist': get_ext_unit_param(
                        filial, 'cabinet_defectologist', EmieUnitRoomEnum.NOT_EXISTS
                    ),
                    'cabinet_logopedist': get_ext_unit_param(filial, 'cabinet_logopedist', EmieUnitRoomEnum.NOT_EXISTS),
                    'cabinet_med': get_ext_unit_param(filial, 'cabinet_med', EmieUnitRoomEnum.NOT_EXISTS),
                    'sport_gym': get_ext_unit_param(filial, 'gym', EmieUnitRoomEnum.NOT_EXISTS),
                    'meeting_room': get_ext_unit_param(filial, 'music_room', EmieUnitRoomEnum.NOT_EXISTS),
                    'pool': get_ext_unit_param(filial, 'swimming_pool', EmieUnitRoomEnum.NOT_EXISTS),
                    'oda_territory': get_ext_unit_param(
                        filial, 'oda_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'oda_entrance': get_ext_unit_param(
                        filial, 'oda_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'oda_way': get_ext_unit_param(filial, 'oda_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'oda_room': get_ext_unit_param(filial, 'oda_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'oda_washroom': get_ext_unit_param(
                        filial, 'oda_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'oda_communication': get_ext_unit_param(
                        filial, 'oda_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'oda_path': get_ext_unit_param(filial, 'oda_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'oda_equipment': get_ext_unit_param(
                        filial, 'oda_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'vision_territory': get_ext_unit_param(
                        filial, 'vision_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'vision_entrance': get_ext_unit_param(
                        filial, 'vision_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'vision_way': get_ext_unit_param(filial, 'vision_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'vision_room': get_ext_unit_param(filial, 'vision_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'vision_washroom': get_ext_unit_param(
                        filial, 'vision_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'vision_communication': get_ext_unit_param(
                        filial, 'vision_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'vision_path': get_ext_unit_param(filial, 'vision_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'vision_equipment': get_ext_unit_param(
                        filial, 'vision_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'ear_territory': get_ext_unit_param(
                        filial, 'ear_territory', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'ear_entrance': get_ext_unit_param(
                        filial, 'ear_entrance', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'ear_way': get_ext_unit_param(filial, 'ear_way', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'ear_room': get_ext_unit_param(filial, 'ear_room', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'ear_washroom': get_ext_unit_param(
                        filial, 'ear_washroom', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'ear_communication': get_ext_unit_param(
                        filial, 'ear_communication', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                    'ear_path': get_ext_unit_param(filial, 'ear_path', DisabilityConditionsEnum.NOT_IMPLEMENTED),
                    'ear_equipment': get_ext_unit_param(
                        filial, 'ear_equipment', DisabilityConditionsEnum.NOT_IMPLEMENTED
                    ),
                }

    @cached_property
    def specialists(self):
        """Данные по специалистам."""

        PSYCHOLOGIST_LIST = [PostCategoryConstants.PSYCHOLOGIST]
        LOGOPEDIST_LIST = [PostCategoryConstants.SPEECH_THERAPIST]
        DEFECTOLOGIST_LIST = [
            PostCategoryConstants.THERAPIST,
            PostCategoryConstants.OLIGOPHREN,
            PostCategoryConstants.SURDO,
            PostCategoryConstants.TIFLO,
        ]
        OLIGOPHREN_LIST = [PostCategoryConstants.OLIGOPHREN]
        SURDO_LIST = [PostCategoryConstants.SURDO]
        TIFLO_LIST = [PostCategoryConstants.TIFLO]
        LFK_LIST = [PostCategoryConstants.LFK]
        AFK_LIST = [PostCategoryConstants.AFK]
        SOCIAL_LIST = [PostCategoryConstants.SOCIAL_EDUCATOR]
        MED_LIST = [
            PostCategoryConstants.NURSE,
            PostCategoryConstants.DOCTOR,
            PostCategoryConstants.NEUROLOG,
            PostCategoryConstants.OPHTHALMOLOGIST,
            PostCategoryConstants.AUDIOLOGIST,
        ]
        PEDIATR_LIST = [PostCategoryConstants.DOCTOR]
        NEUROLOG_LIST = [PostCategoryConstants.NEUROLOG]
        OPHTALMOLOGIST_LIST = [PostCategoryConstants.OPHTHALMOLOGIST]
        AUDIOLOGIST_LIST = [PostCategoryConstants.AUDIOLOGIST]

        dou_ids = [self._unit.id]
        filials = xml_helpers.get_dou_filials_and_building_ids(self._unit.id)
        if filials:
            dou_ids.extend([item['id'] for item in filials])
        return {
            'num_s_psychologist': get_employers_in_dou_by_category(dou_ids, PSYCHOLOGIST_LIST),
            'num_s_logopedist': get_employers_in_dou_by_category(dou_ids, LOGOPEDIST_LIST),
            'num_s_defectologist': get_employers_in_dou_by_category(dou_ids, DEFECTOLOGIST_LIST),
            'num_s_oligophren': get_employers_in_dou_by_category(dou_ids, OLIGOPHREN_LIST),
            'num_s_surdo': get_employers_in_dou_by_category(dou_ids, SURDO_LIST),
            'num_s_tiflo': get_employers_in_dou_by_category(dou_ids, TIFLO_LIST),
            'num_s_lfk': get_employers_in_dou_by_category(dou_ids, LFK_LIST),
            'num_s_afk': get_employers_in_dou_by_category(dou_ids, AFK_LIST),
            'num_s_social': get_employers_in_dou_by_category(dou_ids, SOCIAL_LIST),
            'num_s_med': get_employers_in_dou_by_category(dou_ids, MED_LIST),
            'num_s_pediatr': get_employers_in_dou_by_category(dou_ids, PEDIATR_LIST),
            'num_s_neurolog': get_employers_in_dou_by_category(dou_ids, NEUROLOG_LIST),
            'num_s_ophthalmologist': get_employers_in_dou_by_category(dou_ids, OPHTALMOLOGIST_LIST),
            'num_s_audiologist': get_employers_in_dou_by_category(dou_ids, AUDIOLOGIST_LIST),
            'num_f_psychologist': get_employers_in_dou_by_category(dou_ids, PSYCHOLOGIST_LIST, part_time=True),
            'num_f_logopedist': get_employers_in_dou_by_category(dou_ids, LOGOPEDIST_LIST, part_time=True),
            'num_f_defectologist': get_employers_in_dou_by_category(dou_ids, DEFECTOLOGIST_LIST, part_time=True),
            'num_f_oligophren': get_employers_in_dou_by_category(dou_ids, OLIGOPHREN_LIST, part_time=True),
            'num_f_surdo': get_employers_in_dou_by_category(dou_ids, SURDO_LIST, part_time=True),
            'num_f_tiflo': get_employers_in_dou_by_category(dou_ids, TIFLO_LIST, part_time=True),
            'num_f_lfk': get_employers_in_dou_by_category(dou_ids, LFK_LIST, part_time=True),
            'num_f_afk': get_employers_in_dou_by_category(dou_ids, AFK_LIST, part_time=True),
            'num_f_social': get_employers_in_dou_by_category(dou_ids, SOCIAL_LIST, part_time=True),
            'num_f_med': get_employers_in_dou_by_category(dou_ids, MED_LIST, part_time=True),
            'num_f_pediatr': get_employers_in_dou_by_category(dou_ids, PEDIATR_LIST, part_time=True),
            'num_f_neurolog': get_employers_in_dou_by_category(dou_ids, NEUROLOG_LIST, part_time=True),
            'num_f_ophthalmologist': get_employers_in_dou_by_category(dou_ids, OPHTALMOLOGIST_LIST, part_time=True),
            'num_f_audiologist': get_employers_in_dou_by_category(dou_ids, AUDIOLOGIST_LIST, part_time=True),
        }


class GroupData(with_metaclass(ABCMeta, object)):
    """Данные по группам для рендеринга в шаблон."""

    SKIP_VALUE = -1

    OVZ_VALUES = {
        HNE.DEAFNESS: 1,
        HNE.HARDOFHEARTING: 1,
        HNE.SPEACH: 2,
        HNE.PHONETICS: 2,
        HNE.BLINDNESS: 3,
        HNE.AMAUROSIS: 3,
        HNE.BACKLIGHT: 4,
        HNE.BACKHARD: 4,
        HNE.BACK: 5,
        HNE.AUTISM: 5,
        HNE.DISABLEMENT: 6,
        HNE.INVALIDITY: 7,
        'other': 8,
    }

    WELLNESS = {
        HNE.PHTHISIS: 1,
        HNE.SICK: 2,
        HNE.OTHER: 3,
        HNE.ALLERGOPATHOLOGY: 4,
        HNE.DIABETES: 5,
        HNE.RESPIRATORY: 6,
        HNE.CARDIOVASCULAR: 7,
        HNE.NEPHRO_UROL: 8,
        HNE.CELIAC: 9,
    }

    WORKTYPE = {
        WorkType.SHORT: 1,
        WorkType.ABREV: 2,
        WorkType.FULL: 3,
        WorkType.EXTEND: 4,
        WorkType.ALLDAY: 5,
    }
    ORIENT_DEV = 1
    ORIENT_KOMP = 2
    ORIENT_KOMBI = 3
    ORIENT_HEALTH = 4
    ORIENT_YOUNG = 5
    ORIENT_CARE = 6
    ORIENT_FAMILY = 7

    NEW_HN_MAP = {
        HNE.DEAFNESS: 1,
        HNE.HARDOFHEARTING: 2,
        HNE.AMAUROSIS: 3,
        HNE.BLINDNESS: 4,
        HNE.SPEACH: 5,
        HNE.PHONETICS: 5,
        HNE.DISABLEMENT: 6,
        HNE.BACK: 7,
        HNE.AUTISM: 8,
        HNE.BACKLIGHT: 9,
        HNE.BACKHARD: 9,
        HNE.INVALIDITY: 10,
        HNE.COCHLEAR_IMPL: 12,
        'other': 11,
    }

    EXTRA_HN_MAP = {
        HNE.DEAFNESS: 1,
        HNE.HARDOFHEARTING: 2,
        HNE.AMAUROSIS: 3,
        HNE.BLINDNESS: 4,
        HNE.SPEACH: 5,
        HNE.DISABLEMENT: 6,
        HNE.BACK: 7,
        HNE.AUTISM: 8,
        HNE.BACKLIGHT: 9,
        HNE.BACKHARD: 9,
        HNE.INVALIDITY: 10,
        HNE.ADHD: 11,
        HNE.COCHLEAR_IMPL: 12,
        'other': 0,
    }

    def __init__(self, dou, report_start_date, report_id=None, prep_enrollments_func=None):
        self._dou = dou
        self._group_index = Index(dou, report_start_date)
        self._report_start_date = report_start_date
        self._report_id = report_id
        self._prep_enrollments_func = prep_enrollments_func
        self._loaded_data = None

        self.load_data()

    @staticmethod
    def get_age_range(group):
        """Возрастная категория группы."""

        def get_range(x):
            """Разбиваем отрезок на age_from, age_to."""

            return list(map(float, x.split('-')))

        if group.sub_age_cat:
            age_from, age_to = get_range(group.sub_age_cat.code)
        elif group.age_cat:
            age_from, age_to = get_range(group.age_cat.code)
        else:
            age_from, age_to = 1.0, 7.0

        if not age_from:
            age_from = 0.2

        return age_from, age_to

    @classmethod
    def _get_partner_info(cls, group):
        """Фукнция формирующая информацию о партнерстве группы."""

        dou = group.unit

        if dou.have_lic or group.edu_unit is None or group.edu_unit.gisdo is None:
            return 2, 'нет'
        else:
            return 1, group.edu_unit.gisdo.doo_identity

    @classmethod
    def _get_group_ovz_type(cls, group):
        if group.health_need:
            return cls.OVZ_VALUES.get(group.health_need.code, cls.OVZ_VALUES['other'])
        else:
            return cls.OVZ_VALUES['other']

    @classmethod
    def _get_ovz_type_new(cls, group):
        """значения из поля Ограниченные возможности здоровья"""

        if group.health_need:
            return cls.NEW_HN_MAP.get(group.health_need.code, cls.NEW_HN_MAP['other'])
        else:
            return cls.NEW_HN_MAP['other']

    @classmethod
    def _get_ovz_type_dop(cls, group):
        """значения из поля "Доп. тип ОВЗ"""

        if group.extra_health_need:
            return cls.EXTRA_HN_MAP.get(group.extra_health_need, cls.EXTRA_HN_MAP['other'])
        else:
            return cls.EXTRA_HN_MAP['other']

    @classmethod
    def _get_group_wellness(cls, group):
        if group.health_need:
            return cls.WELLNESS.get(group.health_need.code, cls.WELLNESS[HNE.OTHER])
        else:
            return cls.WELLNESS['other']

    @classmethod
    def _get_group_orientation(cls, group):
        """Возвращает значение для тэга orientation(Направленность группы)"""

        orientation_value = {
            GroupTypeEnumerate.DEV: {'orientation': cls.ORIENT_DEV},
            GroupTypeEnumerate.COMP: {
                'orientation': cls.ORIENT_KOMP,
                'ovzType': cls._get_group_ovz_type(group),
                'ovz_type_new': cls._get_ovz_type_new(group),
                'ovz_type_dop': cls._get_ovz_type_dop(group),
            },
            GroupTypeEnumerate.COMBI: {
                'orientation': cls.ORIENT_KOMBI,
                'ovzType': cls._get_group_ovz_type(group),
                'ovz_type_new': cls._get_ovz_type_new(group),
                'ovz_type_dop': cls._get_ovz_type_dop(group),
            },
            GroupTypeEnumerate.HEALTH: {
                'orientation': cls.ORIENT_HEALTH,
                'wellness': cls._get_group_wellness(group),
                'ovz_type_dop': cls.SKIP_VALUE,
            },
            GroupTypeEnumerate.YOUNG: {
                'orientation': cls.ORIENT_YOUNG,
                'ovz_type_dop': cls.SKIP_VALUE,
            },
            GroupTypeEnumerate.CARE: {
                'orientation': cls.ORIENT_CARE,
                'ovz_type_dop': cls.SKIP_VALUE,
            },
            GroupTypeEnumerate.FAMILY: {
                'orientation': cls.ORIENT_FAMILY,
                'ovz_type_dop': cls.SKIP_VALUE,
            },
        }

        if group.type and (
            group.type.code
            in (
                GroupTypeEnumerate.COMP,
                GroupTypeEnumerate.COMBI,
                GroupTypeEnumerate.HEALTH,
                GroupTypeEnumerate.YOUNG,
                GroupTypeEnumerate.CARE,
                GroupTypeEnumerate.FAMILY,
            )
        ):
            return orientation_value[group.type.code]

        return orientation_value[GroupTypeEnumerate.DEV]

    @classmethod
    def _get_group_work_time(cls, group):
        """Возвращает значение режима работы группы для фед. отчет."""

        def normalize_work_type_code(code):
            if code in [WorkType.ABREV, WorkType.ALLDAY, WorkType.EXTEND, WorkType.FULL, WorkType.SHORT]:
                return code
            else:
                try:
                    torn_code = code.split('-')
                except AttributeError:
                    # Код может быть не заполнен
                    return WorkType.FULL

            map_code = torn_code[0]
            map_code = map_code.replace(',', '.')

            try:
                numeric_map_code = float(map_code)
            except ValueError:
                # Если код не число, то передаем "Полного дня (10,5-12 часов)"
                return WorkType.FULL

            if 1 <= numeric_map_code < 8:
                code_compliance = WorkType.SHORT
            elif 8 <= numeric_map_code < 10.5:
                code_compliance = WorkType.ABREV
            elif 10.5 <= numeric_map_code < 12.5:
                code_compliance = WorkType.FULL
            elif 12.5 <= numeric_map_code < 24:
                code_compliance = WorkType.EXTEND
            elif numeric_map_code == 24:
                code_compliance = WorkType.ALLDAY
            else:
                code_compliance = WorkType.FULL

            return code_compliance

        if group.work_type:
            normalize_code = normalize_work_type_code(group.work_type.code)
            return cls.WORKTYPE[normalize_code]
        else:
            return cls.WORKTYPE[WorkType.FULL]

    def _get_days(self, group):
        """Посещаемость в группе на всех детей на текущий календарный месяц,
        без учета сб и воскресенья или количество дето-дней в группе,
        если сборка отчета происходит по количеству дето-дней.

        """

        attendance_transfer_type = ScheduleSettings.get_settings().attendance_transfer_type
        if attendance_transfer_type == AttendanceTransferType.CHILD_DAYS:
            child_days = group.child_days_amount
            return child_days if child_days else 0
        return get_attendance_without_holidays(group)

    def _get_invalid(self, group):
        """кол-во детей с отметкой инвалид"""

        return self.get_enrollments_count(group, child_filter='invalid')

    def _get_add_cont_ovz(self, group, default, prep_func=None):
        """направления с ОВЗ"""

        if group.type.code == GroupTypeEnumerate.COMP:
            return default
        else:
            child_filter = 'fed_report_exclude'
            if group.type.code == GroupTypeEnumerate.HEALTH:
                child_filter = 'with_ovz_doc'
            return self._group_index.directs_in_group(
                group, children_filter=child_filter, ovz_filter=ovz_filter, prep_direct_func=prep_func
            )

    def _get_educator(self, group):
        """кол-во воспитателей"""

        if group.type.code in (GroupTypeEnumerate.CARE, GroupTypeEnumerate.YOUNG):
            return 0
        else:
            return group.educators.count()

    def _get_reduction_other_count(self, group, prep_func=None):
        """Показатель 29.1.

        Прогнозируемое уменьшение контингента воспитанников
        в текущем учебном году.

        :param group: Группа
        :type group: Group

        :param prep_func: Функция для обработки направлений и зачислений и для изменения результата функции
        :type prep_func: function

        :return: Количество направлений и плановых зачислений
        :rtype: int
        """

        date_in_order = get_report_date_or_today(self._report_start_date)

        children_ids = set()
        qs = Pupil.objects.filter(temporary_deduct=False)
        # дети в фактических группах
        children_in_fact = qs.filter(grup=group, grup__status=GroupStatusEnum.FACT).values_list(
            'children_id', flat=True
        )

        # дети в плановых группах
        children_in_plan = (
            qs.filter(Q(grup__room_id__isnull=False, grup__room_id=group.room_id))
            .filter(
                Q(date_in_order__lte=date_in_order) | Q(date_in_order__isnull=True), grup__status=GroupStatusEnum.PLAN
            )
            .exclude(
                children_id__in=qs.filter(grup__unit=group.unit, grup__status=GroupStatusEnum.FACT).values_list(
                    'children_id', flat=True
                )
            )
            .values_list('children_id', flat=True)
        )

        children_ids.update(children_in_fact, children_in_plan)

        # направления в группу в статусе "Направлен в ДОУ",
        # "Заключение договора" для детей,
        # у кого есть зачисления в плановую или фактическую группу
        # в другое ДОО
        direct = (
            Direct.objects.filter(
                status__code__in=(DRS.REGISTER, DRS.DOGOVOR),
                group__status__in=(GroupStatusEnum.FACT, GroupStatusEnum.PLAN),
            )
            .filter(declaration__children_id__in=children_ids)
            .exclude(
                # направление в другое ДОО
                group__unit=group.unit
            )
            .values_list('declaration__children_id', flat=True)
        )

        # Как направления считаем и зачисления, дата зачисления по приказу
        # которых больше текущей
        pupil = (
            Pupil.objects.filter(
                children_id__in=children_ids,
                date_in_order__gt=date_in_order,
                grup__status=GroupStatusEnum.PLAN,
            )
            .exclude(grup__unit=group.unit)
            .values_list('children_id', flat=True)
        )

        if not prep_func is None:
            return prep_func(direct, pupil)

        return set(list(direct) + list(pupil))

    @property
    def parent_organization(self):
        """Родительская организация.

        Та которая выше в XML в теге organization.

        """

        return

    def _get_activity(self, group, orientation):
        """Возвращает значение тега `activity` для группы."""

        if group.edu_unit_id is not None:
            return 1
        license_, _ = get_unit_license_partner_values(self.parent_organization)
        if license_ == xml_helpers.NO_LICENSE:
            # В организации с тегом license 2 (NO_LICENSE)
            # тег activity у всех групп должен быть 2
            return 2
        elif orientation in (self.ORIENT_YOUNG, self.ORIENT_CARE):
            return 2
        else:
            return 1

    @classmethod
    def _get_program(cls, group, activity, orientation):
        """Возвращает значение тега `program` для группы.

        если у группы выбрано значение поля
            "Получение образования в другой ДОО" (не пустое),
            то передаем значение program=1
        если у группы указан вид деятельности activity=2, то program=0
        если у группы указана направленность orientation=2, то program=0
        если у группы указана направленность orientation=1 или 4, то program=1;
        Остается группы "Семейные" и "Комбинированные"
        если у группы указана направленность orientation=7,
            смотрим на заполненность поле "Программа",
            если выбрана, то program=1; иначе 0
        для orientation ="3" (Комбинированная группа) передаем program = 1
            (вне зависимости от выбранной образовательной программы)
        для остальных случаев передаем 1

        """

        if group.edu_unit_id is not None:
            return 1
        if activity == 2:
            return 0
        elif orientation == cls.ORIENT_KOMP:
            return 0
        elif orientation in (cls.ORIENT_DEV, cls.ORIENT_HEALTH):
            return 1
        elif orientation == cls.ORIENT_FAMILY:
            return 0 if group.program_id is None else 1
        elif orientation == cls.ORIENT_KOMBI:
            return 1
        else:
            return 1

    def _get_program_ovz(self, _group, data):
        """
        Возвращает значение тега "program_ovz" для группы

        - если у группы указан вид деятельности activity=2, то program_ovz=0;

        - если у группы указана направленность orientation=2, то program_ovz=1;

        - если у группы указана направленность orientation=1,3,4,7 смотрим на
        заполненность поле "Программа", если выбрана и тип программы
        "Адаптированная" то program_ovz=1, иначе 0;

        Для всех остальных случаев передаем 1

        :param _group: Группа
        :type _group: Group
        :param data: Словарь со значениями
        :type data: dict

        :return: значение тега "program_ovz"
        :rtype: int

        """

        syllabus = getattr(_group.program, 'syllabus', None)
        program_type = getattr(syllabus, 'program_type', None)

        program_type_is_adapted = False

        # Пытаемся получить "Тип программы" образовательной программы группы
        if program_type and program_type.filter(code=ProgramTypeEnum.ADAPTED).exists():
            program_type_is_adapted = True

        if data['activity'] == 2:
            return 0
        elif data['orientation'] == self.ORIENT_KOMP:
            return 1
        elif data['orientation'] in (self.ORIENT_DEV, self.ORIENT_KOMBI, self.ORIENT_HEALTH, self.ORIENT_FAMILY):
            if program_type_is_adapted:
                return 1
            else:
                return 0
        else:
            return 1

    def collect_data(self):
        """
        Запись данных в БД
        """
        if self._report_id is None:
            return

        self._loaded_data = []

        for data in self.get_groups_data():
            GroupDataModel.objects.create(report_id=self._report_id, unit=self._dou, data=data)
            self._loaded_data.append(data)

    def load_data(self):
        """
        Получение данных из БД
        """
        if self._report_id is None:
            return

        if not GroupDataModel.objects.filter(report_id=self._report_id, unit=self._dou).exists():
            self.collect_data()
        else:
            self._loaded_data = []
            for group_data in GroupDataModel.objects.filter(report_id=self._report_id, unit=self._dou).iterator():
                self._loaded_data.append(group_data.data)

    @property
    def groups(self):
        """
        Данные по группам
        """
        if self._loaded_data:
            for group_data in self._loaded_data:
                yield group_data
        else:
            yield from self.get_groups_data()

    def get_groups_data(self):
        """
        Получить данные по группам
        """
        for group in (
            Group.objects.filter(status=GroupStatusEnum.FACT, unit=self._dou)
            .select_related('unit', 'type', 'work_type', 'program__syllabus', 'age_cat', 'health_need')
            .order_by('id')
        ):
            # подсчет использует enrollment который учитывает возможность
            # того, что один ребенок может быть зачислен несколько раз в
            # разные филиалы и само родительское учреждение

            age_from, age_to = self.get_age_range(group)

            capacity = self._group_index.get_capacity_in_group(group)
            enrolled = self.get_enrollments_count(group, prep_enrollments_func=prep_ind_enrolled_data)
            transfer_space = group.vacant_places

            add_cont_children = self._group_index.directs_in_group(
                group, prep_direct_func=prep_directs_in_group_queries
            )
            add_cont = len(add_cont_children)
            if self.get_parent_dou_status() in xml_helpers.NOT_CALCULATED_STATUSES:
                free_space = 0
            else:
                free_space = capacity - len(enrolled) - add_cont - transfer_space
                free_space = free_space if free_space > 0 else 0

            if (
                hasattr(group, 'work_type')
                and hasattr(group.work_type, 'code')
                and group.work_type.code in get_short_day_types()
            ):
                capacity_gkp = capacity
                enrolled_gkp = len(enrolled)
                enrolled_gkp_children = enrolled
                add_cont_gkp = add_cont
                add_cont_gkp_children = add_cont_children

            else:
                capacity_gkp = group.short_count

                enrolled_gkp_children = self.get_enrollments_count(
                    group,
                    child_filter='short_time_only',
                    only_first_enrollment=True,
                    prep_enrollments_func=prep_ind_enrolled_data,
                )
                enrolled_gkp = len(enrolled_gkp_children)

                add_cont_gkp_children = self._group_index.directs_in_group(
                    group,
                    'short_time_directs',
                    pupil_filter='short_time_pupils',
                    prep_direct_func=prep_directs_in_group_queries,
                )
                add_cont_gkp = len(add_cont_gkp_children)

            add_cont_ovz_children = self._get_add_cont_ovz(
                group, add_cont_children, prep_func=prep_directs_in_group_queries
            )
            reduction_school_children = self.get_enrollments_count(
                group,
                query_filter='predictable_decrease_contingent',
                prep_enrollments_func=prep_ind_enrolled_data,
            )
            reduction_other_children = self._get_reduction_other_count(group, prep_func=prep_ind_29_1_queries)

            data = {
                'id': group.id,
                'doo_name': group.unit.name,
                'group_name': group.name,
                'ageFrom': age_from,
                'ageTo': age_to,
                'ovzType': '',
                'wellness': '',
                'add_cont': add_cont,
                'add_cont_children': add_cont_children,
                'add_cont_gkp': add_cont_gkp,
                'add_cont_gkp_children': add_cont_gkp_children,
                'add_cont_ovz': len(add_cont_ovz_children),
                'add_cont_ovz_children': add_cont_ovz_children,
                'subgroup': (group.subgroup_number if group.subgroup_number else 1),
                'transfer_space': transfer_space,
                'enrolled': len(enrolled),
                'enrolled_gkp': enrolled_gkp,
                'enrolled_gkp_children': enrolled_gkp_children,
                'work_time_group': self._get_group_work_time(group),
                'free_space': free_space,
                'capacity': capacity,
                'capacity_gkp': get_value(capacity_gkp, '0'),
                'days': self._get_days(group),
                'size': group.area,
                'invalid': self.get_enrollments_count(
                    group,
                    child_filter='invalid',
                ),
                'reduction_school': len(reduction_school_children),
                'reduction_school_children': reduction_school_children,
                'reduction_other': len(reduction_other_children),
                'reduction_other_children': list(reduction_other_children),
                'educator': self._get_educator(group),
            }

            data.update(self._get_group_orientation(group))
            # Количество детей, у которых поле "ОВЗ" заполнено,
            # все кроме пусто и значения "Нет"
            if data['orientation'] == self.ORIENT_KOMP:  # Компенсирующая
                data['ovz_deti_children'] = enrolled
            else:
                data['ovz_deti_children'] = self.get_enrollments_count(
                    group, child_filter='fed_report_exclude', prep_enrollments_func=prep_ind_enrolled_data
                )

            data['ovz_deti'] = len(data['ovz_deti_children'])

            data['activity'] = self._get_activity(group, data['orientation'])

            data['program'] = self._get_program(group, data['activity'], data['orientation'])

            data['program_ovz'] = self._get_program_ovz(group, data)

            if group.name:
                data.update({'name': group.name})
            else:
                data.update({'name': 'нет'})

            partner_group, partner = self._get_partner_info(group)
            data['partner_group'] = partner_group
            data['partner'] = partner

            yield data

    @abstractmethod
    def get_enrollments_count(
        self, group, query_filter='default', child_filter=None, only_first_enrollment=False, prep_enrollments_func=None
    ):
        """Возвращает число детей в группе согласно фильтрам.

        Важно различать фильтры!:
            - query_filter: код фильтра `filters` из `gisdo.index.enrolled`
            - child_filter: код фильтра `kid_filters` из `gisdo.index.enrolled`
            - only_first_enrollment: считать только первое приоритетное
                зачисление.

        """

    def get_parent_dou_status(self):
        return get_dou_status(self._dou)


class ParentGroupData(GroupData):
    """Данные по группам для рендеринга в шаблон родительского учреждения

    Считает также чисто зачислений детей по филиалам для того, чтобы
    исключить попадание одних и тех же детей дважды из филиала и
    родительского учреждения. Приоритет отдается фактическим зачислениям.

    """

    def __init__(self, dou, report_start_date, filials_data, report_id=None, prep_enrollments_func=None):
        self._filials_data = filials_data
        self._group_enrollments_cache = {}

        super(ParentGroupData, self).__init__(dou, report_start_date, report_id, prep_enrollments_func)

    def _group_enrollments_count(
        self, query_filter='default', child_filter=None, only_first_enrollment=False, prep_enrollments_func=None
    ):
        kid_filter = kid_filters.get(child_filter, Q())
        if callable(kid_filter):
            kid_filter = kid_filter()
        filter_ = filters.get(query_filter, filters['default'])()
        children_enrollments = {}
        index = self._group_index

        unit_with_filials_ids = [fd.filial.id for fd in self._filials_data] + [index.dou.id]
        already_enrolled = set()
        # приоритет сначала у фактических зачислений
        for group in index.groups:
            enrolled_in_fact = index.enrolled_in_group_fact(group.id)
            for children_id, group_id in enrolled_in_fact.filter(
                index.pupil_filter,
                kid_filter,
                filter_,
            ).values_list(
                'children_id',
                'grup_id',
            ):
                if not only_first_enrollment or children_id not in already_enrolled:
                    if children_id not in children_enrollments:
                        children_enrollments[children_id] = group_id

            already_enrolled.update(enrolled_in_fact.values_list('children_id', flat=True))

        # затем плановые зачисления
        for group in index.groups:
            enrolled_in_plan = index.enrolled_in_group_plan(group)
            for children_id, group_id, room_id in (
                index.enrolled_in_group_plan(group)
                .filter(
                    index.pupil_filter,
                    kid_filter,
                    filter_,
                )
                .values_list('children_id', 'grup_id', 'grup__room_id')
            ):
                if children_id not in children_enrollments:
                    # для плановой группы берем соотв. фактическую
                    fact_group = Group.objects.filter(
                        unit__in=unit_with_filials_ids, room_id=room_id, status=GroupStatusEnum.FACT
                    ).first()

                    if fact_group and (not only_first_enrollment or children_id not in already_enrolled):
                        children_enrollments[children_id] = fact_group.id

            already_enrolled.update(enrolled_in_plan.values_list('children_id', flat=True))

        if prep_enrollments_func:
            return prep_enrollments_func(children_enrollments)

        group_enrollments = defaultdict(int)
        for children_id, group_id in children_enrollments.items():
            group_enrollments[group_id] += 1

        return group_enrollments

    def get_enrollments_count(
        self, group, query_filter='default', child_filter=None, only_first_enrollment=False, prep_enrollments_func=None
    ):
        if (query_filter, child_filter, only_first_enrollment) not in self._group_enrollments_cache:
            enrollments_count = self._group_enrollments_count(
                query_filter, child_filter, only_first_enrollment, prep_enrollments_func=prep_enrollments_func
            )
            self._group_enrollments_cache[(query_filter, child_filter, only_first_enrollment)] = enrollments_count
            return enrollments_count[group.id]

        return self._group_enrollments_cache[(query_filter, child_filter, only_first_enrollment)][group.id]

    @property
    def parent_organization(self):
        return self._dou


class FilialGroupData(GroupData):
    """Данные по группам для рендеринга в шаблон родительского филиала"""

    def __init__(self, dou, parent_group_data, report_start_date, report_id=None, prep_enrollments_func=None):
        self.parent_group_data = parent_group_data

        super(FilialGroupData, self).__init__(dou, report_start_date, report_id, prep_enrollments_func)

    def get_enrollments_count(
        self, group, query_filter='default', child_filter=None, only_first_enrollment=False, prep_enrollments_func=None
    ):
        return self.parent_group_data.get_enrollments_count(
            group, query_filter, child_filter, only_first_enrollment, prep_enrollments_func=prep_enrollments_func
        )

    def get_parent_dou_status(self):
        return self.parent_group_data.get_parent_dou_status()

    @property
    def parent_organization(self):
        return self.parent_group_data._dou


class GroupDataCollector(object):
    """
    Собирает данные группы для передачи в отчёте
    """

    def __init__(self, unit_helper, mo, report_start_date, report_id):
        self._unit_helper = unit_helper
        self._mo = mo
        self._group_data_params = {'report_start_date': report_start_date, 'report_id': report_id}

    def collect(self):
        dou_list = get_units_report(self._mo, self._unit_helper.get_mo_units(self._mo.id))

        for dou in dou_list:
            filials_data = xml_helpers.get_dou_filials(dou).select_related('filial')

            parent_group_data = ParentGroupData(dou=dou, filials_data=filials_data, **self._group_data_params)
            parent_group_data.collect_data()

            for filial in (fd.filial for fd in filials_data.iterator()):
                filial_group_data = FilialGroupData(
                    dou=filial, parent_group_data=parent_group_data, **self._group_data_params
                )
                filial_group_data.collect_data()


class Transport(object):
    """Отправщик отчетов."""

    NETWORK_PROBLEMS = (socket.timeout, suds.WebFault, IOError)

    def __init__(self, schedule_settings):
        self._settings = schedule_settings
        self._client = self._create_client()

    def _create_client(self):
        try:
            header = Element('Authentication', ns=('ns1', 'http://eo.edu.ru'))
            header.append(Element('Login', ns=('ns1', 'http://eo.edu.ru')).setText(self._settings.push_login))
            header.append(Element('Password', ns=('ns1', 'http://eo.edu.ru')).setText(self._settings.push_password))
            client = Client(url=gs_settings.GISDO_WS_WSDL, timeout=gs_settings.GISDO_TIMEOUT)
            client.set_options(soapheaders=(header,))
        except Exception as e:
            Logger.add_record(f'Ошибка при создании SOAP клиента: {traceback.format_exc()}')
            raise SOAPClientCreateException from e
        return client

    def _get_send_method(self):
        if self._settings.zip_xml:
            if self._settings.async_send:
                method = 'PushZipDataAsync'
            else:
                method = 'PushZipData'
        else:
            method = 'PushData'

        return method

    def _get_number_of_attempts(self):
        return int(self._settings.resend_count)

    def send(self, content):
        method = self._get_send_method()

        # Преобразовать байтовое представление в юникодную строку.
        # Иначе client преобразует в строку с помощью str, что нарушит формат.
        # Например, 'b'...''.
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        attempts = 1
        error_msg = None
        error_inst = None
        while attempts <= self._get_number_of_attempts():
            try:
                result = getattr(self._client.service, method)(data=content, schema='3.0')
            except self.NETWORK_PROBLEMS as error:
                error_inst = error
                error_msg = str(error)
                Logger.add_record(
                    f'Попытка {attempts}. Ошибка подключения: {error_msg}',
                    level=Logger.ERROR,
                )
                time.sleep(attempts * 10)  # лучше немного подождать
                attempts += 1
            except Exception as error:
                error_inst = error
                error_msg = str(error)
                break
            else:
                if not result['Result']:
                    Logger.add_record('Тип ошибки: Пришёл ответ с Result=false', level=Logger.ERROR)
                    error_msg = result['Message']
                break

        if error_msg:
            if error_inst is not None:
                Logger.add_record(f'Тип ошибки: {str(error_inst.__class__)}', level=Logger.ERROR)
            Logger.add_record(f'Сообщение об ошибке: {str(error_msg)}', level=Logger.ERROR)
            if isinstance(error_inst, self.NETWORK_PROBLEMS):
                raise ConnectingAtSendingReportException()
            raise SendReportException(error_msg)
