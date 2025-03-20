from __future__ import (
    absolute_import,
)

import logging
import uuid

import pkg_resources
from future.builtins import (
    map,
    object,
    str,
)

from educommon.m3.extensions.listeners import (
    DeclareContextListener,
)
from m3.actions import (
    ACD,
    Action,
    ControllerCache,
    OperationResult,
    PreJsonResult,
    utils,
)
from m3.actions.exceptions import (
    ApplicationLogicException,
)
from m3.actions.packs import (
    BaseDictionaryModelActions,
    DictListWindowAction,
)
from m3_ext.ui import (
    all_components as ext,
)
from m3_ext.ui.results import (
    ExtUIScriptResult,
)
from objectpack.actions import (
    ObjectPack,
)

from kinder.controllers import (
    obs,
)
from kinder.core.dict.models import (
    UnitKind,
)
from kinder.core.unit.actions import (
    UnitDictPack,
)
from kinder.core.unit.helpers import (
    get_ancestor_unit_by_kinds,
    get_mo_store,
)
from kinder.core.unit.models import (
    Unit,
)

from gisdo import (
    forms,
    settings as gs_settings,
)
from gisdo.logger import (
    Logger,
)

from .constants import (
    PERM_RELATED_TO_MO,
)
from .index_report.forms import (
    UnloadChildrenByIndexWindow,
)
from .index_report.tasks import (
    UnloadChildrenByIndexTask,
)
from .utils import (
    has_federal_report_permission,
)


log = logging.getLogger('gisdo')


@obs.subscribe
class AddFieldListenerEditWin(object):
    """Перехватчик создания окна редактирования организации.

    Добавляем в конец поле Не отправлять фед.отчетность если тип организации ДОО.
    """

    listen = ['kinder.core.unit.EditUnitDictPack/UnitEditWindowAction']

    def after(self, request, context, result):
        unit_id = getattr(context, 'id', -1)
        from .models import (
            GisdoUnit,
        )

        try:
            unit = Unit.objects.get(id=unit_id)
            gisdo_unit_id = unit.gisdo.id
            not_on_federal_report = unit.gisdo.not_on_federal_report
            related_to_mo_id = unit.gisdo.related_to_mo_id
        except (Unit.DoesNotExist, GisdoUnit.DoesNotExist):
            not_on_federal_report = False
            gisdo_unit_id = ''
            unit = None
            related_to_mo_id = None

        unit_pack = ControllerCache.find_pack('kinder.core.unit.actions.EditUnitDictPack')
        # на поле есть права и в родителях нет мо
        if unit:
            related_to_mo_enable = unit_pack.has_perm(request, PERM_RELATED_TO_MO) and not get_ancestor_unit_by_kinds(
                unit, [UnitKind.MO]
            )
        else:
            related_to_mo_enable = False

        extension_win = forms.GisdoUnitEditWindowBuilder.build_extension(result.data, related_to_mo_enable)

        extension_win.not_on_federal_report.checked = not_on_federal_report
        extension_win.history_grid.store.base_params.update(gisdo_unit_id=gisdo_unit_id)

        if unit and unit.kind_id == UnitKind.DOU:
            mo_store = get_mo_store(request.user)
            # ограничиваем стор
            extension_win.field__related_to_mo_id.set_store(ext.ExtDataStore(data=mo_store))
            if related_to_mo_id:
                extension_win.field__related_to_mo_id.value = related_to_mo_id

        if not has_federal_report_permission(request, 'PERM_SETTING_NOT_SEND_IN_FO'):
            extension_win.not_on_federal_report.disabled = True

        result.data = extension_win


@obs.subscribe
class AddFieldListenerAddWin(object):
    """Перехватчик создания окна создания организации.

    Добавляем в конец поле Не отправлять фед.отчетность если тип организации ДОО.
    """

    listen = ['kinder.core.unit.EditUnitDictPack/UnitAddWindowAction']

    def after(self, request, context, result):
        parent_id = getattr(context, 'parent_id', None)

        try:
            parent = Unit.objects.get(id=parent_id)
        except Unit.DoesNotExist:
            parent = None

        unit_pack = ControllerCache.find_pack('kinder.core.unit.actions.EditUnitDictPack')
        # на поле есть права и в родителях нет мо
        if parent:
            related_to_mo_enable = unit_pack.has_perm(request, PERM_RELATED_TO_MO) and not get_ancestor_unit_by_kinds(
                parent, [UnitKind.MO]
            )
        else:
            related_to_mo_enable = False
        extension_win = forms.GisdoUnitEditWindowBuilder.build_extension(result.data, related_to_mo_enable)

        extension_win.not_on_federal_report.checked = False
        extension_win.history_grid.store.base_params.update(gisdo_unit_id='')

        mo_store = get_mo_store(request.user)
        # ограничиваем стор
        extension_win.field__related_to_mo_id.set_store(ext.ExtDataStore(data=mo_store))
        if not has_federal_report_permission(request, 'PERM_SETTING_NOT_SEND_IN_FO'):
            extension_win.not_on_federal_report.disabled = True

        result.data = extension_win


@obs.subscribe
class SaveFieldListener(DeclareContextListener):
    """Перехватчик сохранения окна редактирования организации.

    Сохраняем поле Не отправлять фед.отчетность в модели GisdoUnit.
    """

    listen = ['kinder.core.unit.EditUnitDictPack/UnitSaveAction']

    def _declare_additional_context(self):
        return {'not_on_federal_report': {'type': 'js_checkbox', 'default': False}}

    def after(self, request, context, result):
        from .models import (
            GisdoUnit,
        )

        unit_id = result.data.get('id', -1)
        unit = Unit.objects.get(id=unit_id)

        try:
            g_unit = GisdoUnit.objects.get(unit=unit)

            # Если нет идентификатора, то формируем его
            if not g_unit.doo_identity:
                g_unit.create_doo_identity()
        except GisdoUnit.DoesNotExist:
            g_unit = GisdoUnit(unit=unit)
            try:
                g_unit.create_doo_identity()
            except ApplicationLogicException as e:
                # Если создавалось новое ДОУ
                if not hasattr(context, 'unit_id'):
                    Unit.objects.filter(id=unit_id).delete()
                raise ApplicationLogicException(e.exception_message)

        not_on_federal_report = getattr(context, 'not_on_federal_report', False)

        if has_federal_report_permission(request, 'PERM_SETTING_NOT_SEND_IN_FO'):
            g_unit.not_on_federal_report = not_on_federal_report

        g_unit.related_to_mo_id = context.related_to_mo_id or None
        g_unit.save()

        # Возвращаем ответ в исходное положение.
        result.data = None


class ReportFormActionPack(BaseDictionaryModelActions):
    """Экшен пак работы с объектами модели ReportForm."""

    from .models import (
        ReportForm,
    )

    url = '/report-forms'
    verbose_name = 'Федеральная отчетность'
    title = verbose_name
    model = ReportForm
    list_columns = [
        ('date', 'Дата отчета'),
        ('sent', 'Отправлен'),
        ('user.get_fio', 'Пользователь'),
        ('unit.name', 'Территория'),
        ('progress', 'Активная сборка'),
    ]
    list_sort_order = ['-date']
    list_form = forms.ReportFormsListWindow
    need_check_permission = True

    #: создание формы
    PERM_ADD = 'add'
    #: удаление формы
    PERM_DELETE = 'delete'
    #: отправка формы на фед.уровень
    PERM_SEND = 'send'
    #: редактирование формы
    PERM_EDIT = 'edit'
    #: настройка "Не отправлять в фед. отчетность"
    PERM_SETTING_NOT_SEND_IN_FO = 'not_send_in_fo_setting'
    PERM_EDIT_ATTENDANCE_TRANSFER_TYPE = 'edit_attendance_transfer_type'
    # Права на отчет "Выгрузка детей по показателю/тегу"
    PERM_UNLOAD_BY_INDEX = 'unload_by_index'

    sub_permissions = {
        PERM_ADD: 'Создание формы',
        PERM_EDIT: 'Редактирование',
        PERM_DELETE: 'Удаление формы',
        PERM_SEND: 'Отправка на Фед.уровень',
        PERM_SETTING_NOT_SEND_IN_FO: 'Настройка "Не отправлять в фед.отчет"',
        PERM_EDIT_ATTENDANCE_TRANSFER_TYPE: 'Изменение способа передачи посещаемости',
        PERM_UNLOAD_BY_INDEX: 'Выгрузка детей по показателю/тегу',
    }

    def __init__(self):
        super(ReportFormActionPack, self).__init__()
        self._init_actions()

    def _init_actions(self):
        """Инициализация экшенов пака."""
        #: данные отчета по организации
        self.report_form_row_data_action = ReportFormRowDataAction()
        #: запуск таска на подсчет показателей организации и её дочерних
        self.report_form_row_collect_action = ReportFormRowCollectAction()
        #: рендер отчета в .xls формат
        self.report_form_row_excel_action = ReportFormRowToExcelAction()
        #: вызов окна сборки отчета
        self.report_form_build_window_action = ReportFormBuildWindowAction()
        #: вызов окна просмотра отчета
        self.report_form_view_window_action = ReportFormViewWindowAction()
        #: отправка отчета
        self.report_form_send_action = ReportFormSentAction()
        #: вызов окна настроек сборки
        self.report_form_settings_window_action = ReportFormSettingsWindowAction()
        #: сохранение настроек сборки
        self.report_form_settings_save_action = ReportFormSettingsSaveAction()
        # Выгрузка результата подсчета показателей ФО в Excel
        self.unload_children_by_index_window_action = UnloadChildrenByIndexWindowAction()
        self.unload_children_by_index_action = UnloadChildrenByIndexAction()

        self.actions.remove(self.list_window_action)
        self.list_window_action = ListWindowAction()
        self.actions.append(self.list_window_action)

        self.actions.extend(
            [
                self.report_form_row_data_action,
                self.report_form_row_collect_action,
                self.report_form_build_window_action,
                self.report_form_view_window_action,
                self.report_form_row_excel_action,
                self.report_form_send_action,
                self.report_form_settings_window_action,
                self.report_form_settings_save_action,
                self.unload_children_by_index_window_action,
                self.unload_children_by_index_action,
            ]
        )

    @property
    def gisdo_pack(self):
        if not hasattr(self, '_gisdo_pack'):
            self._gisdo_pack = ControllerCache.find_pack(GisdoUnitDictPack)

        return self._gisdo_pack

    @property
    def build_window_url(self):
        """URL вызова окна сборки отчета."""
        return self.report_form_build_window_action.get_absolute_url()

    @property
    def save_tree_url(self):
        """URL запуска таска на подсчет показателей."""
        return self.report_form_row_collect_action.get_absolute_url()

    @property
    def settings_window_url(self):
        """URL вызова окна настроек сборки."""
        return self.report_form_settings_window_action.get_absolute_url()

    @property
    def settings_save_url(self):
        """URL сохранения настроек сборки."""
        return self.report_form_settings_save_action.get_absolute_url()

    @property
    def view_window_url(self):
        """URL вызова окна просмотра отчета."""
        return self.report_form_view_window_action.get_absolute_url()

    @property
    def excel_url(self):
        """URL рендера отчета в .xls формат."""
        return self.report_form_row_excel_action.get_absolute_url()

    @property
    def send_url(self):
        """URL отправки отчета."""
        return self.report_form_send_action.get_absolute_url()

    @property
    def unload_by_index_window_url(self):
        """URL показа окна отчета "Выгрузка детей по показателю/тегу"."""
        return self.unload_children_by_index_window_action.get_absolute_url()

    @property
    def unload_by_index_url(self):
        """URL формирования отчета "Выгрузка детей по показателю/тегу"."""
        return self.unload_children_by_index_action.get_absolute_url()

    def delete_row(self, objs):
        """Удаление отчета и всех дочерних ReportFormRow объектов."""
        for obj in objs:
            obj.reportformrow_set.all().delete()
            obj.groupdata_set.all().delete()
        return super(ReportFormActionPack, self).delete_row(objs)

    def modify_rows_query(self, query, request, context):
        return query.select_related('unit', 'user')

    def get_rows_modified(self, offset, limit, filter_, user_sort='', request=None, context=None):
        if user_sort:
            user_sort = self.prepare_user_sort(user_sort)

        return super().get_rows_modified(offset, limit, filter_, user_sort, request, context)

    def get_rows(self, offset, limit, filter, user_sort=''):
        if user_sort:
            user_sort = self.prepare_user_sort(user_sort)

        return super(ReportFormActionPack, self).get_rows(offset, limit, filter, user_sort=user_sort)

    def prepare_user_sort(self, user_sort):
        """Заменяет поля сортировки для поиска в бд."""
        user_sort = user_sort.replace('sent', 'sent_time')
        user_sort = user_sort.replace('progress', 'in_progress')
        user_sort = user_sort.replace('unit.name', 'unit__name')
        user_sort = user_sort.replace('user.get_fio', 'user__fname')
        return user_sort

    def extend_menu(self, menu):
        return menu.Item(name=self.title, pack=self.list_window_action)


class ListWindowAction(DictListWindowAction):
    need_check_permission = True
    verbose_name = 'Просмотр'

    def run(self, request, context):
        win = self.create_window(request, context, mode=0)
        self.create_columns(win.grid, self.parent.list_columns)
        self.configure_list(win)

        handler_dblclick = win.grid.handler_dblclick
        # проверим право редактирования
        if not self.parent.has_sub_permission(request.user, self.parent.PERM_EDIT, request):
            tuple(el.make_read_only() for el in win.grid.top_bar._items if el.text != 'Обновить')

        if not self.parent.has_sub_permission(request.user, self.parent.PERM_UNLOAD_BY_INDEX, request):
            win.grid.top_bar.unload_by_index_btn.disabled = True
            win.grid.top_bar.unload_by_index_btn.hidden = True

        win.grid.handler_dblclick = handler_dblclick

        return ExtUIScriptResult(self.parent.get_list_window(win))


class ReportFormRowDataAction(Action):
    """Данные по конкретной организации для окна редактирования ReportForm."""

    url = '/report-form-row-data'
    verbose_name = 'Данные для формы отчета'

    def context_declaration(self):
        return [ACD(name='unit_id', type=int, required=True), ACD(name='report_form_id', type=int, required=True)]

    def run(self, request, context):
        """Получение данных по id объекта и отправка обратно в клиент, в формате для отображения."""
        from gisdo.proxy import (
            UIProxy,
        )

        from .models import (
            ReportFormRow,
        )

        report_form_rows = []
        try:
            report_form_rows.append(
                ReportFormRow.objects.get(unit_id=context.unit_id, report_id=context.report_form_id)
            )
        except ReportFormRow.DoesNotExist:
            report_form_rows = []

        if not report_form_rows:
            try:
                unit = Unit.objects.get(id=context.unit_id)
            except Unit.DoesNotExist:
                unit = None

            if unit is not None:
                report_form_rows = ReportFormRow.objects.filter(
                    report_id=context.report_form_id,
                    unit__kind_id=UnitKind.DOU,
                    unit__lft__gt=unit.lft,
                    unit__rght__lt=unit.rght,
                )

        if not report_form_rows:
            return OperationResult.by_message('Отсутствуют данные по организации')

        try:
            a, q, e, c = UIProxy(report_form_rows).get_ui_data()
            result = {
                'applications': a,
                'queues': q,
                'enrolled': e,
                'capacities': c,
            }
        except Exception:
            return OperationResult.by_message('Извините. Отчет временно не доступен')
        return PreJsonResult(data=result)


class ReportFormRowCollectAction(Action):
    """Сохранение данных по организации и её дочерним организациям."""

    url = '/save-report-form-row'
    verbose_name = 'Сохранение данных по дереву организаций'

    def context_declaration(self):
        return (ACD(name='unit_id', type=int, required=True),)

    def run(self, request, context):
        """Создание нового объекта ReportForm и запуск таска на подсчет показателей по ней и дочерним организациям."""
        from . import (
            tasks,
        )

        unit = Unit.objects.get(id=context.unit_id)
        if unit.kind.id not in [UnitKind.MO, UnitKind.REGION]:
            return OperationResult.by_message('Создание отчета выполняется с уровня не ниже МО.')

        user_id = request.user.get_profile().id
        tasks.CollectUnitsDataTask().apply_async(
            (user_id, unit.id),
            None,
            description='Подсчет показателей: %s.' % unit.name,
            queue=gs_settings.CELERY_WORKER_TASK_QUEUE,
        )

        return OperationResult(message='Подсчет показателей начался в фоновом режиме.')


class ReportFormRowToExcelAction(Action):
    """Рендер отчета в .xls фомат."""

    url = '/excel'
    verbose_name = 'Генерация excel'

    def context_declaration(self):
        return [
            ACD(name='report_id', type=int, required=True, verbose_name='id отчета'),
            ACD(name='unit_id', type=int, required=True, verbose_name='id организации'),
        ]

    def run(self, request, context):
        """Создание отчета в excel средствами excel_reporting."""
        from . import (
            tasks,
        )

        if not gs_settings.REGION_CODE:
            return OperationResult.by_message('Не задан код региона')
        result_name = str(uuid.uuid4())[:16]

        full_name = ' '.join([request.user.last_name, request.user.first_name])
        email = request.user.email
        phone = ''

        tasks.Report().apply_async(
            (
                result_name,
                context.report_id,
                full_name,
                email,
                phone,
            ),
            None,
            queue=gs_settings.CELERY_WORKER_TASK_QUEUE,
        )

        return OperationResult(message='Формирование отчета началось в фоновом режиме.')


class ReportFormBuildWindowAction(Action):
    """Вызов окна ввода параметров формирования отчета."""

    url = '/build'
    verbose_name = 'Формирование отчета'

    def run(self, request, context):
        return ExtUIScriptResult(forms.ReportFormBuildWindow(self.parent))


class ReportFormViewWindowAction(Action):
    """Окно отображения отчета."""

    url = '/view'
    verbose_name = 'Просмотр отчета'

    def context_declaration(self):
        return (ACD(name='id', type=int, required=True, verbose_name='id отчета'),)

    def run(self, request, context):
        """Окно просмотра отчета не вызывается для отчетов, находящихся в процессе сборки."""
        from .models import (
            ReportForm,
        )

        try:
            report_form = ReportForm.objects.get(id=context.id)
            if not report_form.in_progress:
                win = forms.ReportFormViewWindow(pack=self.parent)
                if not self.parent.has_sub_permission(request.user, self.parent.PERM_SEND, request):
                    win.send_btn.make_read_only()
                result = ExtUIScriptResult(win)
            else:
                result = OperationResult(
                    message='Отчет находится в процессе сборки. '
                    'Вы можете увидеть прогресс сборки в меню '
                    '(Администрирование -> Запущенные задачи)'
                )
        except ReportForm.DoesNotExist:
            result = OperationResult.by_message('Отчет не найден в базе')

        return result


class ReportFormSentAction(Action):
    """Отправка отчета."""

    url = '/send'
    verbose_name = 'Отправка отчета'

    def context_declaration(self):
        return (ACD(name='report_id', required=True, type=int),)

    def run(self, request, context):
        """Запуск асинхронной задачи отправки показателей
        на веб-сервис в формате xml.
        """
        from . import (
            tasks,
        )

        tasks.SendUnitsDataTask().apply_async(
            (context.report_id,), None, description='Отправка показателей', queue=gs_settings.CELERY_WORKER_TASK_QUEUE
        )

        return OperationResult(message='Отправка показателей началась в фоновом режиме.')


class ReportFormSettingsWindowAction(Action):
    """Окно отображения настроек сборки отчета."""

    url = '/settings'
    verbose_name = 'Настройки сбора отчета'

    def run(self, request, context):
        from .models import (
            ScheduleSettings,
        )

        schedule_settings = ScheduleSettings.get_settings()
        window = forms.ReportFormSettingsWindow()
        window.system_version_fld.value = gs_settings.KINDER_VERSION

        try:
            version = pkg_resources.get_distribution('gisdo').version
        except pkg_resources.DistributionNotFound:
            version = 'unknown'
        window.module_version_fld.value = version

        window.form.from_object(schedule_settings)
        window.form.url = self.parent.settings_save_url
        gisdo_pack = ControllerCache.find_pack('gisdo.actions.ReportFormActionPack')
        if not self.parent.has_perm(request, gisdo_pack.PERM_EDIT_ATTENDANCE_TRANSFER_TYPE):
            window.attendance_transfer_type.read_only = True
        return ExtUIScriptResult(window)


class ReportFormSettingsSaveAction(Action):
    """Сохранение настроек сборки."""

    url = '/settings-save'
    verbose_name = 'Сохранение настроек сбора отчета'

    def context_declaration(self):
        return (ACD(name='id', type=int, verbose_name='id'),)

    def run(self, request, context):
        """В случае соответсвующих настроек создаем периодические таски."""
        from .models import (
            ScheduleSettings,
            TaskScheduler,
        )

        def get_row(_id):
            return ScheduleSettings.objects.get(id=_id)
        schedule_settings = utils.bind_request_form_to_object(request, get_row, forms.ReportFormSettingsWindow)
        try:
            schedule_settings.save()
            list(map(TaskScheduler.terminate, TaskScheduler.objects.all()))
            if schedule_settings.is_active:
                ts = TaskScheduler.schedule_every(
                    'gisdo.tasks.CollectUnitDataPeriodicTask',
                    schedule_settings.time.hour,
                    schedule_settings.time.minute,
                )
                ts.start()
        except Exception as error:
            return OperationResult.by_message(error.message.decode('utf-8'))
        else:
            return OperationResult()


class GisdoUnitDictPack(UnitDictPack):
    url = r'/gisdo'
    _is_primary_for_model = False

    def get_nodes(self, parent_id, filter, branch_id=None, request=None, context=None, filter_by_profile_units=False):
        from .models import (
            GisdoUnit,
        )

        nodes = super().get_nodes(parent_id, filter, branch_id, request, context, filter_by_profile_units)
        g_units = []
        for node in nodes:
            try:
                if not node.gisdo.not_on_federal_report:
                    g_units.append(node)
            except GisdoUnit.DoesNotExist:
                Logger.add_record(
                    'Организация %s с ID=%d не найдено в модуле "ФО"' % (node.name, node.pk), level=Logger.WARNING
                )
        return g_units


class GisdoReportFormDictPack(ObjectPack):
    from .models import (
        ReportForm,
    )

    model = ReportForm
    _is_primary_for_model = False

    column_name_on_select = 'presentation'

    title = 'Федеральная отчетность'

    list_sort_order = ['-date']

    select_related = ['user', 'unit']

    columns = [
        {'data_index': 'date', 'header': 'Дата отчета'},
        {'data_index': 'sent', 'header': 'Отправлен'},
        {'data_index': 'user.get_fio', 'header': 'Пользователь'},
        {'data_index': 'unit', 'header': 'Территория'},
        {'data_index': 'progress', 'header': 'Активная сборка'},
        {'data_index': 'presentation', 'hidden': True},
    ]

    def get_rows_query(self, request, context):
        unit_id = getattr(context, 'unit_id', request.user.get_profile().unit.id)

        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            raise ApplicationLogicException('Организация с ID={0} не найдено'.format(unit_id))

        region = unit.get_ancestors(include_self=True).filter(kind=UnitKind.REGION).first()

        return self.model.objects.filter(
            in_progress=False,
            unit__in=(region, unit),
            unit__kind__id__in=(UnitKind.MO, UnitKind.REGION),
        ).select_related(*self.select_related)


class UnloadChildrenByIndexWindowAction(Action):
    """Экшен показа окна отчета "Выгрузка детей по показателю/тегу"."""

    url = '/unload_by_index_window'

    def run(self, request, context):
        return ExtUIScriptResult(UnloadChildrenByIndexWindow(self.parent))


class UnloadChildrenByIndexAction(Action):
    """Экшен формирования отчета "Выгрузка детей по показателю/тегу"."""

    url = '/unload_by_index'

    def context_declaration(self):
        context = super().context_declaration() or {}

        context.update(
            {
                'unit_id': {'type': int, 'required': True},
                'indexes': {'type': 'str_list', 'required': True},
            }
        )

        return context

    def run(self, request, context):
        unit = Unit.objects.get(id=context.unit_id)
        if unit.kind.id not in [UnitKind.MO, UnitKind.REGION]:
            return OperationResult.by_message('Формирование отчета выполняется с уровня не ниже МО.')

        UnloadChildrenByIndexTask().apply_async(kwargs={'unit_id': context.unit_id, 'indexes': context.indexes})

        return OperationResult(message='Формирование отчета началось в фоновом режиме.')
