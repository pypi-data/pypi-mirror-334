import json
import os

from future.builtins import (
    object,
    str,
)
from simple_report.converter.abstract import (
    FileConverter,
)
from simple_report.report import (
    SpreadsheetReport,
)
from simple_report.xlsx.document import (
    DocumentXLSX,
)

from kinder.core.dict.models import (
    DouType,
)
from kinder.core.unit.models import (
    StructureTypes,
    UnitStatus,
)

from gisdo import (
    constants as const,
    settings as gs_settings,
)
from gisdo.index.constants import (
    APPLICATION_INDEXES,
    CAPACITIES_INDEXES,
    ENROLLED_INDEXES,
    QUEUE_INDEXES,
)


class ReportFormReport(object):
    APPLICATION = 'applications'
    QUEUE = 'queues'
    ENROLLED = 'enrolled'
    CAPACITIES = 'capacities'

    PARTS = {
        APPLICATION: APPLICATION_INDEXES,
        QUEUE: QUEUE_INDEXES,
        ENROLLED: ENROLLED_INDEXES,
        CAPACITIES: CAPACITIES_INDEXES,
    }

    def __init__(self, result_name):
        templates = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
        self.template_name = os.path.join(templates, 'federal_report_5.xlsx')
        self.result_name = os.path.join(gs_settings.DOWNLOADS_DIR, result_name + '.xlsx')

        self.report = SpreadsheetReport(self.template_name, wrapper=DocumentXLSX, type=FileConverter.XLSX)

    def reset_page(self):
        """Сброс страницы на первую."""
        self.report.workbook.active_sheet = 0

    def flush_header(self, full_name, email, phone='', page=0):
        self.report.workbook.active_sheet = page
        header = self.report.get_section('header')
        header.flush({'full_name': full_name, 'email': email, 'phone': phone})

    def collect_row_data(self, report_form_row, date, ocato):
        mo = report_form_row.unit.get_mo()

        unit_dou_type = report_form_row.unit.dou_type
        if not unit_dou_type:
            unit_dou_type = DouType.objects.get(code=DouType.GOVERNMENT)

        row_data = {
            'mo': mo.name,
            'dou': report_form_row.unit.name,
            'date': str(date),
            'property_type': unit_dou_type.name,
            'status_dou': (UnitStatus.values[report_form_row.unit.status] if report_form_row.unit.status else ''),
            'structure_type': (StructureTypes.values[report_form_row.unit.structure_type]),
            'have_lic': 'Да' if report_form_row.unit.have_lic else 'Нет',
            'boss_fio': (report_form_row.unit.boss_fio if report_form_row.unit.boss_fio else ''),
            'work_hour': (report_form_row.unit.reception_time or 'с 6.30 до 18.30 часов'),
            'address': (report_form_row.unit.address_full if report_form_row.unit.address_full else ''),
            'site': (report_form_row.unit.site if report_form_row.unit.site else ''),
            'email': (report_form_row.unit.email if report_form_row.unit.email else ''),
            'phone': (report_form_row.unit.telephone if report_form_row.unit.telephone else ''),
            'doo_number': (report_form_row.unit.doo_number if report_form_row.unit.doo_number else ''),
        }

        row_data.update(ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.APPLICATION))
        row_data.update(ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.QUEUE))
        row_data.update(ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.ENROLLED))
        row_data.update(ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.CAPACITIES))

        return row_data

    def flush_row_data(self, data, page=0):
        self.report.workbook.active_sheet = page
        row = self.report.get_section('row')

        for portion in data:
            row.flush(portion)

    def build(self):
        self.report.build(self.result_name)

    @staticmethod
    def _collect_data(report_form_row, index_group):
        data = json.loads(getattr(report_form_row, index_group))

        result = {}

        age_slices = (
            const.AGE_CATEGORIES_FULL,
            const.AGE_CATEGORIES_EIGHT,
            const.AGE_CATEGORIES_CUT,
            {'ALL': const.ALL},
        )

        for index_id in ReportFormReport.PARTS[index_group]:
            for age_slice in age_slices:
                for age_category in age_slice:
                    index = data[index_id]
                    if age_slice[age_category] in index:
                        report_index_id = index_id.replace('.', '_')
                        report_age_cat = age_category.replace('-', '_').replace('.', '_')
                        result[report_index_id + '_%s' % report_age_cat] = index[age_slice[age_category]]

        return result
