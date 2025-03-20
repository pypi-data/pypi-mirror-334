from future.builtins import (
    map,
    object,
)

from m3.actions import (
    ControllerCache,
)
from m3_ext.ui import (
    all_components as ext,
)
from objectpack.ui import (
    model_fields_to_controls,
)

from kinder.controllers import (
    obs,
)
from kinder.core import (
    ui_helpers,
)
from kinder.core.forms import (
    BaseListWindow,
)
from kinder.plugins.helpers import (
    extend_plugins_template_globals,
)

from gisdo.constants import (
    ATTENDANCE_TRANSFER_TYPES,
    RESEND_AFTER_TIMES_LIST,
)
from gisdo.models import (
    GisdoUnit,
    InstallationType,
    ScheduleSettings,
)

from .settings import (
    RELATED_MO_PORTAL,
)


class ReportFormsListWindow(BaseListWindow):
    """
    Окно списка форм 'Федеральная отчетность'
    """

    def __init__(self, *a, **kw):
        super(ReportFormsListWindow, self).__init__(*a, **kw)
        self.grid_initialized = False
        self.template_globals = 'ui-js/report-forms-list-window.js'
        report_form_ap = ControllerCache.find_pack('gisdo.actions.ReportFormActionPack')
        self.build_window_url = report_form_ap.build_window_url
        self.view_window_url = report_form_ap.view_window_url
        self.settings_window_url = report_form_ap.settings_window_url
        self.unload_by_index_window_url = report_form_ap.unload_by_index_window_url
        self.unload_by_index_url = report_form_ap.unload_by_index_url

        self.read_only = True

    def init_grid_components(self):
        super(ReportFormsListWindow, self).init_grid_components()
        self.grid.handler_dblclick = 'gridDblClickHandler'
        if not self.grid_initialized:
            unload_by_index_btn = ext.ExtButton(
                text='Выгрузить детей по показателю/тегу',
                handler='unloadChildrenByIndex',
                icon_cls='icon-page-excel',
            )

            self.grid_initialized = True
            self.grid.top_bar._items = [
                ext.ExtButton(text='Собрать отчет', handler='sendReportTask', icon_cls='icon-clock-play'),
                ext.ExtButton(text='Удалить', handler='deleteValueGrid', icon_cls='icon-report-delete'),
                ext.ExtButton(text='Обновить', handler='refreshGridStore', icon_cls='table_refresh'),
                ext.ExtButton(text='Настройки', handler='settingsWindow', icon_cls='icon-table-gear'),
            ]
            self.grid.top_bar._items.append(unload_by_index_btn)
            self.grid.top_bar.unload_by_index_btn = unload_by_index_btn


class ReportFormBuildWindow(ext.ExtEditWindow):
    """
    Окно ввода параметров отчета
    """

    def __init__(self, pack, *args, **kwargs):
        super(ReportFormBuildWindow, self).__init__(*args, **kwargs)
        self.width, self.height = 400, 120
        self.title = 'Параметры сборки отчёта'
        self.modal = True

        self.minimizable = True
        self.form = ext.ExtForm()
        self.form.url = pack.save_tree_url

        self.unit = ext.ExtDictSelectField(
            anchor='100%',
            label='Организация',
            name='unit_id',
            allow_blank=False,
            hide_edit_trigger=True,
            hide_trigger=True,
            pack=pack.gisdo_pack.__class__,
        )
        self.form.items.extend([self.unit])
        self.buttons.extend(
            (
                ext.ExtButton(text='Запустить сборку', handler='submitForm', icon_cls='icon-clock-play'),
                ext.ExtButton(text='Отмена', handler='cancelForm'),
            )
        )


class ReportFormViewWindow(ext.ExtWindow):
    """
    Просмотр данных отчета
    """

    def __init__(self, pack, *args, **kwargs):
        """
        @param : pack инстанспака фед отчетности
        @param : unit_pack иестанс пака реестра организаций с доп. фильтрацией
        """

        super(ReportFormViewWindow, self).__init__(*args, **kwargs)
        self.title = 'Показатели'
        self.maximized = True
        self.layout = 'fit'
        self.template_globals = 'ui-js/report-form-view-window.js'
        self.report_form_row_data_url = pack.report_form_row_data_action.get_absolute_url()
        self.closable = self.maximizable = self.minimizable = True
        self.excel_url = pack.excel_url
        self.send_url = pack.send_url
        self.panel = ext.ExtPanel(layout='border')
        self.units_tree = ext.ExtTree(
            allow_container_drop=False, region='west', url=pack.gisdo_pack.nodes_action.get_absolute_url()
        )
        self.units_tree.add_column(header='Выберите организацию', data_index='name', sortable=False)

        self.data_panel = ext.ExtTabPanel(region='center', auto_width=False)

        grid_attr = {
            'applications': 'Информация о заявлениях',
            'queues': 'Информация о детях в очереди',
            'enrolled': 'Информация о зачисленных детях',
            'capacities': 'Информация о свободных местах',
        }
        for key, val in list(grid_attr.items()):
            panel = ext.ExtPanel(layout='fit', title=val, header=True)
            setattr(self, '%s_grid' % key, ext.ExtGrid(anchor='100%', name=key, height=300))
            setattr(self, '%s_store' % key, ext.ExtDataStore())
            grid = getattr(self, '%s_grid' % key)
            grid.add_column(header='Показатель', data_index='name')
            grid.add_column(header='Количество', data_index='count')
            grid.set_store(getattr(self, '%s_store' % key))
            panel.items.append(grid)
            self.data_panel.items.append(panel)

        self.panel.items.extend([self.units_tree, self.data_panel])
        self.footer_bar = ext.ExtToolBar()
        self.save_xls_btn = ext.ExtButton(
            text='Сохранить в Excel файле', handler='saveInExcel', icon_cls='icon-page-excel'
        )
        self.send_btn = ext.ExtButton(text='Отправить отчет', handler='sendReport')
        self.footer_bar.items.extend([self.save_xls_btn, self.send_btn])
        self.items.append(self.panel)


class ReportFormSettingsWindow(ext.ExtEditWindow):
    """
    Окно редактирования настроек
    """

    FIELD_LIST = ('server_location',)

    def __init__(self, create_new=False, *args, **kwargs):
        super(ReportFormSettingsWindow, self).__init__(*args, **kwargs)
        self.template_globals = 'ui-js/gisdo-settings-window.js'
        self.create_new = create_new
        self.width, self.height = 400, 600
        self.title = 'Настройки сборки отчёта'
        self.modal = True

        self.minimizable = True
        self.form = ext.ExtForm()
        self.form.label_width = 200
        self.form.url = ControllerCache.find_pack('gisdo.actions.ReportFormActionPack').save_tree_url

        self.id = ext.ExtHiddenField(name='id')

        self.time = ext.ExtTimeField(
            anchor='100%', allow_blank=False, label='Время сборки отчета (ежедневно)', name='time', format='H:i'
        )

        self.is_active = ext.ExtCheckBox(
            label='Автосборка', box_label='Включить автоматический сбор показателей', name='is_active'
        )

        self.push_login = ext.ExtStringField(anchor='100%', label='Логин', name='push_login', allow_blank=False)

        self.push_password = ext.ExtStringField(anchor='100%', label='Пароль', name='push_password', allow_blank=False)

        self.resend_count = ext.ExtNumberField(
            anchor='100%',
            label='Повторы отправки при неудаче',
            name='resend_count',
            allow_decimals=False,
            allow_negative=False,
            max_value=5,
            min_value=1,
            allow_blank=False,
        )

        self.resend_after_time = ext.ExtComboBox(
            label='Запускать автоматическую отправку после неудачной попытки через (минут)',
            name='resend_after_time',
            display_field='name',
            value_field='id',
            anchor='100%',
            allow_blank=True,
            trigger_action_all=True,
            # editable=False
        )
        self.resend_after_time.set_store(ext.ExtDataStore(RESEND_AFTER_TIMES_LIST))

        self.attendance_transfer_type = ext.ExtComboBox(
            label='Способ передачи посещаемости',
            name='attendance_transfer_type',
            display_field='name',
            value_field='id',
            anchor='100%',
            allow_blank=False,
            trigger_action_all=True,
            editable=False,
        )
        self.attendance_transfer_type.set_store(ext.ExtDataStore(ATTENDANCE_TRANSFER_TYPES))

        self.zip_xml = ext.ExtCheckBox(label='Сжатие', box_label='Включить сжатие в zip при отправке', name='zip_xml')

        self.async_send = ext.ExtCheckBox(
            label='Асинхронная отправка', box_label='Асинхронная отправка данных', name='async_send', hidden=True
        )

        self.field_set = ext.ExtFieldSet(anchor='100%', label_width=150, title='Сведения о системе')

        self.system_name_fld = ext.ExtStringField(
            name='system_name', label='Наименование системы', anchor='100%', allow_blank=False
        )
        self.system_version_fld = ext.ExtStringField(
            name='system_version', label='Версия', anchor='100%', allow_blank=True, read_only=True
        )
        self.module_version_fld = ext.ExtStringField(
            name='module_version', label='Версия модуля', anchor='100%', allow_blank=True, read_only=True
        )
        self.email_fld = ext.ExtStringField(
            name='email',
            allow_blank=False,
            anchor='100%',
            max_length=30,
            label='E-mail контактного лица',
            vtype='email',
        )

        self._controls = list(
            map(ui_helpers.anchor100, model_fields_to_controls(ScheduleSettings, self, self.FIELD_LIST))
        )
        ui_helpers.add_multiline_field_template(self.field__server_location)
        self.installation_type = ext.ExtComboBox(
            allow_blank=True,
            name='installation_type',
            label='Тип установки',
            anchor='100%',
            display_field='name',
            value_field='id',
            editable=False,
            trigger_action=ext.ExtComboBox.ALL,
        )
        self.installation_type.set_store(ext.ExtDataStore(list(InstallationType.values.items())))

        self.field_set.items.extend(
            [
                self.system_name_fld,
                self.system_version_fld,
                self.module_version_fld,
                self.email_fld,
                self.installation_type,
            ]
            + self._controls
        )

        self.form.items.extend(
            [
                self.id,
                self.time,
                self.is_active,
                self.resend_count,
                self.resend_after_time,
                self.attendance_transfer_type,
                self.zip_xml,
                self.async_send,
                self.push_login,
                self.push_password,
                self.field_set,
            ]
        )
        self.buttons.extend(
            (ext.ExtButton(text='Сохранить', handler='submitForm'), ext.ExtButton(text='Отмена', handler='cancelForm'))
        )


class GisdoUnitEditWindowBuilder(object):
    """
    Переопределен для реализации дополнительный контролов,
    специфичных для gisdo
    """

    field_fabric_params = [
        'related_to_mo_id',
    ]

    @staticmethod
    def build_extension(parent_win, related_to_mo_enable):
        parent_win.related_to_mo_enable = related_to_mo_enable
        parent_win.related_mo_portal = RELATED_MO_PORTAL

        extend_plugins_template_globals(parent_win, 'ui-js/gisdo-unit-edit-window.js', 'unit-edit-window.js')

        model_fields_to_controls(
            GisdoUnit, parent_win, GisdoUnitEditWindowBuilder.field_fabric_params, model_register=obs
        )

        parent_win.field__related_to_mo_id.__dict__.update(
            **dict(
                anchor='100%',
                hide_dict_select_trigger=True,
                hide_edit_trigger=True,
                hide_clear_trigger=False,
                flex=10,
                allow_blank=True,
                hidden=True,
            )
        )

        not_on_federal_report = ext.ExtCheckBox(
            label='Не отправлять фед.отчетность', name='not_on_federal_report', hidden=True
        )
        if hasattr(parent_win, 'set_control_on_main_tab') and callable(parent_win.set_control_on_main_tab):
            parent_win.set_control_on_main_tab(not_on_federal_report, 'not_on_federal_report')
            parent_win.set_control_on_main_tab(parent_win.field__related_to_mo_id, 'related_to_mo_id')
        return parent_win
