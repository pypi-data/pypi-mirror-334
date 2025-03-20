from __future__ import (
    print_function,
)

from itertools import (
    chain,
)
from unittest import (
    SkipTest,
)

from django.test import (
    TestCase,
)

from kinder.core.unit.models import (
    UnitKind,
)

from gisdo.constants import (
    AGE_CATEGORIES_EIGHT,
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
from gisdo.xml_helpers import (
    NOT_CALCULATED_STATUSES,
    get_dou_status,
)


get_name = lambda name, key: '%s_%s' % (name, key.replace('-', '_').replace('.', '_'))


class CheckListsTestCase(TestCase):
    """Запускаем проверки на последнем собранном ФО, для всех ДОУ"""

    def setUp(self):
        try:
            self.report_form = ReportForm.objects.filter(in_progress=False).latest('date')
            self.report_form_row_query = ReportFormRow.objects.filter(
                report=self.report_form, unit__kind_id=UnitKind.DOU
            )
        except ReportForm.DoesNotExist:
            raise SkipTest('not found report')

    def _sum(self, name, data, age_cat=AGE_CATEGORIES_FULL):
        result = 0
        for key in list(age_cat.keys()):
            result += data[get_name(name, key)]
        return result

    def test_checklist(self):
        """Запускаем проверки на одном из МО"""
        if not hasattr(self, 'report_form'):
            raise SkipTest('not found report')

        print('Найден отчет %s ' % self.report_form.presentation)
        for report_form_row in self.report_form_row_query:
            print('запускаем тесты по %s' % report_form_row.unit)

            mo = report_form_row.unit.get_mo()
            app_result = ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.APPLICATION)
            queueu_result = ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.QUEUE)
            enrolled_result = ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.ENROLLED)
            capacities_result = ReportFormReport._collect_data(report_form_row, index_group=ReportFormReport.CAPACITIES)

            # проверки на суммы по возастным категориям
            self.assertTrue(
                self._sum('1_1', app_result) >= app_result['1_ALL'], 'Не выполнена проверка 1.1. >= 1 для %s' % mo
            )
            self.assertTrue(
                (self._sum('7_1', queueu_result) == self._sum('7', queueu_result)),
                'Не выполнена проверка 7.1.=7 для %s' % mo,
            )

            self.assertTrue(
                (self._sum('7_7', queueu_result) <= self._sum('7_1', queueu_result)),
                'Не выполнена проверка 7.7. <= 7.1 для %s' % mo,
            )
            self.assertTrue(
                (self._sum('7_5', queueu_result) == self._sum('7_6', queueu_result)),
                'Не выполнена проверка 7.6. = 7.5 для %s' % mo,
            )
            sum_9_1 = self._sum('9_1', queueu_result)
            self.assertTrue(
                (sum_9_1 == queueu_result['10_ALL'] + queueu_result['11_ALL']),
                'Не выполнена проверка 9.1 = 10 + 11 для %s' % mo,
            )
            self.assertTrue(sum_9_1 == self._sum('9', queueu_result), 'Не выполнена проверка 9.1.= 9 для %s' % mo)

            sum_10_1 = self._sum('10_1', queueu_result)
            self.assertTrue(sum_10_1 <= queueu_result['10_ALL'], 'Не выполнена проверка 10.1 <= 10 для %s' % mo)
            self.assertTrue(
                (
                    self._sum('18', queueu_result)
                    == self._sum('18_1', queueu_result)
                    == self._sum('18_2', queueu_result)
                ),
                'Не выполнена проверка 18 = 18.1.= 18.2 для %s' % mo,
            )
            sum_29 = enrolled_result['29_ALL']

            sum_19 = self._sum('19', enrolled_result)
            sum_19_1 = self._sum('19_1', enrolled_result)
            self.assertTrue(
                (sum_19 == sum_19_1 == self._sum('19_2', enrolled_result)),
                'Не выполнена проверка 19=19.1.=19.2 для %s' % mo,
            )
            self.assertTrue(sum_29 <= sum_19_1, 'Не выполнена проверка 29 <= 19.1 для %s' % mo)
            sum_19 = self._sum('19', enrolled_result)

            self.assertTrue(
                capacities_result['32_ALL'] <= self._sum('32_1', capacities_result),
                'Не выполнена проверка 32 <= 32.1 для %s' % mo,
            )

            self.assertTrue(
                self._sum('29_3', enrolled_result) <= self._sum('29_2', enrolled_result),
                'Не выполнена проверка 29.3. <= 29.2 для %s' % mo,
            )

            # в разрезе
            for key in list(AGE_CATEGORIES_FULL.keys()):
                age_7_2 = queueu_result[get_name('7_2', key)]
                age_7_4 = queueu_result[get_name('7_4', key)]
                age_18_1 = queueu_result[get_name('18_1', key)]
                age_18_4 = queueu_result[get_name('18_4', key)]
                age_19_1 = enrolled_result[get_name('19_1', key)]
                self.assertEqual(
                    app_result[get_name('1_1', key)],
                    (app_result[get_name('2_1', key)] + app_result[get_name('3_1', key)]),
                    'Не выполнена проверка 1.1 = 2.1+3.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (
                        app_result[get_name('4', key)]
                        >= app_result[get_name('4_1', key)] + app_result[get_name('4_2', key)]
                    ),
                    'Не выполнена проверка 4 >= 4.1+4.2 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (app_result[get_name('6', key)] <= app_result[get_name('1_1', key)]),
                    'Не выполнена проверка 6 <= 1.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('7_1', key)] >= (age_7_2 + queueu_result[get_name('7_3', key)]),
                    'Не выполнена проверка 7.1. >= 7.2. + 7.3 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(age_7_4 <= age_7_2, 'Не выполнена проверка 7.4 <=7.2 для %s в ВК %s' % (mo, key))
                self.assertTrue(
                    queueu_result[get_name('7_5', key)] >= (age_18_1 + age_7_2 - age_7_4),
                    'Не выполнена проверка 7.5. >= 18.1.+7.2.-7.4 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('9', key)] <= queueu_result[get_name('18', key)],
                    'Не выполнена проверка 9<=18 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('9_1', key)] <= age_18_1,
                    'Не выполнена проверка 9.1<=18.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('10_1', key)] <= queueu_result[get_name('9_1', key)],
                    'Не выполнена проверка 10.1 <= 9.1',
                )
                self.assertTrue(
                    (queueu_result[get_name('12', key)] <= age_18_1 + enrolled_result[get_name('20_2', key)]),
                    'Не выполнена проверка 12 <= 18.1 + 20.2. для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (queueu_result[get_name('13', key)] <= queueu_result[get_name('12', key)]),
                    'Не выполнена проверка 13 <= 12 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (queueu_result[get_name('13_1', key)] <= queueu_result[get_name('18_3', key)]),
                    'Не выполнена проверка 13.1 <= 18.3 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (queueu_result[get_name('14', key)] <= age_18_1 + enrolled_result[get_name('20', key)]),
                    'Не выполнена проверка 14 <= 18.1 + 20 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('15', key)] <= age_18_1,
                    'Не выполнена проверка 15 <= 18.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('16', key)] <= age_18_1,
                    'Не выполнена проверка 16 <= 18.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('17', key)] <= age_18_1,
                    'Не выполнена проверка 17 <= 18.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    queueu_result[get_name('17_1', key)] <= age_18_1,
                    'Не выполнена проверка 17.1 <= 18.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    age_18_4 <= queueu_result[get_name('18_5', key)],
                    'Не выполнена проверка 18.4 <= 18.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    age_18_4 <= age_18_1 + age_7_2 - age_7_4,
                    'Не выполнена проверка 18.4 <= 18.1 + 7.2 – 7.4 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    age_19_1
                    >= enrolled_result[get_name('21', key)]
                    + enrolled_result[get_name('22', key)]
                    + enrolled_result[get_name('24', key)],
                    'Не выполнена проверка 19.1 >= 21 + 22 + 24 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    age_19_1 >= enrolled_result[get_name('26', key)] + enrolled_result[get_name('27', key)],
                    'Не выполнена проверка 19.1. >= 26 + 27 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    age_19_1
                    >= enrolled_result[get_name('30', key)]
                    + enrolled_result[get_name('30_1', key)]
                    + enrolled_result[get_name('30_2', key)],
                    'Не выполнена проверка 19.1.>= 30 + 30.1 + 30.2 для %s в ВК %s' % (mo, key),
                )

                self.assertTrue(
                    enrolled_result[get_name('20_1', key)] <= enrolled_result[get_name('19_3', key)],
                    'Не выполнена проверка 20.1 <= 19.3 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_2', key)] <= enrolled_result[get_name('20', key)],
                    'Не выполнена проверка 20.2. <= 20 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_5', key)] >= enrolled_result[get_name('20', key)],
                    'Не выполнена проверка 20.5 >= 20 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_5', key)] <= queueu_result[get_name('18_5', key)],
                    'Не выполнена проверка 20.5 <= 18.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_6', key)] <= enrolled_result[get_name('20_5', key)],
                    'Не выполнена проверка 20.6 <= 20.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_7', key)] <= enrolled_result[get_name('20_5', key)],
                    'Не выполнена проверка 20.7 <= 20.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('20_8', key)] <= enrolled_result[get_name('20_5', key)],
                    'Не выполнена проверка 20.8 <= 20.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('21', key)] <= age_19_1,
                    'Не выполнена проверка 21 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('22', key)] <= age_19_1,
                    'Не выполнена проверка 22 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('22_1', key)] <= enrolled_result[get_name('22', key)],
                    'Не выполнена проверка 22.1 <= 22 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('22_5_1', key)] <= enrolled_result[get_name('22_5', key)],
                    'Не выполнена проверка 22.5.1 <= 22.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('22_5_2', key)] <= enrolled_result[get_name('22_5', key)],
                    'Не выполнена проверка 22.5.2 <= 22.5 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('23', key)] <= enrolled_result[get_name('22', key)],
                    'Не выполнена проверка 23 <= 22 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('24', key)] <= age_19_1,
                    'Не выполнена проверка 24 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('25', key)] <= age_19_1,
                    'Не выполнена проверка 25 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('26', key)] <= age_19_1,
                    'Не выполнена проверка 26 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('27', key)] <= age_19_1,
                    'Не выполнена проверка 27 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('28', key)] >= enrolled_result[get_name('27', key)],
                    'Не выполнена проверка 28 >= 27 для %s в ВК %s' % (mo, key),
                )

                self.assertTrue(
                    enrolled_result[get_name('29_1', key)] <= age_19_1,
                    'Не выполнена проверка 29.1. <= 19.1 для %s в ВК %s' % (mo, key),
                )

                self.assertTrue(
                    enrolled_result[get_name('30', key)] <= age_19_1,
                    'Не выполнена проверка 30 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('30_1', key)] <= age_19_1,
                    'Не выполнена проверка 30.1 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    enrolled_result[get_name('30_2', key)] <= age_19_1,
                    'Не выполнена проверка 30.2 <= 19.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    capacities_result[get_name('32_2', key)] <= capacities_result[get_name('32_1', key)],
                    'Не выполнена проверка 32.2 <= 32.1 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(
                    (enrolled_result[get_name('30_1', key)] + enrolled_result[get_name('30_2', key)])
                    >= (
                        enrolled_result[get_name('22_1', key)]
                        + enrolled_result[get_name('22_2', key)]
                        + enrolled_result[get_name('22_3', key)]
                        + enrolled_result[get_name('22_4', key)]
                        + enrolled_result[get_name('22_5', key)]
                        + enrolled_result[get_name('22_6', key)]
                        + enrolled_result[get_name('22_7', key)]
                        + enrolled_result[get_name('22_8', key)]
                    ),
                    'Не выполнена проверка 30.1.+ 30.2. >= 22.1.+22.2.+22.3.+22.4.+22.5.+22.6.+22.7.+22.8 для %s' % mo,
                )

            # в разрезе
            for key in list(AGE_CATEGORIES_EIGHT.keys()):
                age_31 = capacities_result[get_name('31', key)]
                age_31_1 = capacities_result[get_name('31_1', key)]
                age_31_2 = capacities_result[get_name('31_2', key)]
                age_31_3 = capacities_result[get_name('31_3', key)]
                age_31_4 = capacities_result[get_name('31_4', key)]
                self.assertTrue(
                    age_31 >= age_31_1 + age_31_3,
                    'Не выполнена проверка 31 > = 31.1. + 31.3 для %s в ВК %s' % (mo, key),
                )
                self.assertTrue(age_31_2 <= age_31_1, 'Не выполнена проверка 31.2 <= 31.1 для %s в ВК %s' % (mo, key))
                self.assertTrue(age_31_4 <= age_31, 'Не выполнена проверка 31.4 <= 31 для %s в ВК %s' % (mo, key))

            # enrolled в XML по всем группам учреждения равен показателю 19
            dou_data = DouData(report_form_row.unit, self.report_form)
            dou_groups = list(chain(*(building['groups'] for building in dou_data.buildings)))

            total_enrolled = sum(group['enrolled'] for group in dou_groups)
            self.assertEqual(
                total_enrolled, sum_19, 'Не выполнена проверка 19 == enrolled по всем группам учреждения для %s' % mo
            )

            # ovz_deti в XML по всем группам учреждения равен 30.1 + 30.2
            ovz_deti = sum(group['ovz_deti'] for group in dou_groups)
            self.assertEqual(
                ovz_deti,
                self._sum('30_1', enrolled_result) + self._sum('30_2', enrolled_result),
                'Не выполнена проверка 30.1 + 30.2 == ovz_deti по всем группам учреждения для %s' % mo,
            )
            # сумма значений показателя 22.1 равна сумме значений тег ovz_deti
            # в сумме по всем группам с тегом orientation=2 и 3 и
            # тегом ovz_type=1.
            ovz_deti_deafness = sum(
                group['ovz_deti']
                if (group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI) and group['ovzType'] == 1)
                else 0
                for group in dou_groups
            )
            self.assertEqual(
                ovz_deti_deafness,
                self._sum('22_1', enrolled_result),
                'Не выполнена проверка 22.1 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и тегом ovz_type=1'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.1.1 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=1.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 1
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_1_1', enrolled_result),
                'Не выполнена проверка 22.1.1 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=1'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.1.2 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=2.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 2
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_1_2', enrolled_result),
                'Не выполнена проверка 22.1.2 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=2'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.3.1 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=3.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 3
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_3_1', enrolled_result),
                'Не выполнена проверка 22.3.1 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=33'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.3.2 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=4.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 4
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_3_2', enrolled_result),
                'Не выполнена проверка 22.3.2 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=4'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.5.1 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=7.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 7
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_5_1', enrolled_result),
                'Не выполнена проверка 22.5.1 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=7'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.5.2 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=8.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 8
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_5_2', enrolled_result),
                'Не выполнена проверка 22.5.2 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=8'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.8.1 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=11.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 11
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_8_1', enrolled_result),
                'Не выполнена проверка 22.8.1 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=11'
                ' для %s' % mo,
            )
            # сумма значений показателя 22.8.2 равна сумме значений тега
            #  ovz_deti по всем группам с тегом orientation=2 и 3
            # и тегом ovz_type_new=12.
            self.assertEqual(
                sum(
                    group['ovz_deti']
                    if (
                        group['orientation'] in (GroupData.ORIENT_KOMP, GroupData.ORIENT_KOMBI)
                        and group['ovz_type_new'] == 12
                    )
                    else 0
                    for group in dou_groups
                ),
                self._sum('22_8_2', enrolled_result),
                'Не выполнена проверка 22.8.2 == ovz_deti по всем '
                'группам учреждения тегом orientation=2 и 3 и'
                ' тегом ovz_type_new=12'
                ' для %s' % mo,
            )

            # Проверка показателей детей с отличающимся режимом пребывания
            sum_enrolled_gkp = 0
            for g in dou_groups:
                self.assertTrue(
                    int(g['capacity']) >= int(g['capacity_gkp']),
                    'Нарушено условие {capacity_gkp} (capacity_gkp) <= '
                    '{capacity} (capacity) по группе id={group_id}'.format(
                        capacity=g['capacity'],
                        capacity_gkp=g['capacity_gkp'],
                        group_id=g['id'],
                    ),
                )
                self.assertTrue(
                    g['enrolled'] >= g['enrolled_gkp'],
                    'Нарушено условие {enrolled_gkp} (enrolled_gkp) <= '
                    '{enrolled} (enrolled) по группе id={group_id}'.format(
                        enrolled=g['enrolled'],
                        enrolled_gkp=g['enrolled_gkp'],
                        group_id=g['id'],
                    ),
                )
                self.assertTrue(
                    g['add_cont'] >= g['add_cont_gkp'],
                    'Нарушено условие {add_cont_gkp} (add_cont_gkp) <= '
                    '{add_cont} (add_cont) по группе id={group_id}'.format(
                        add_cont=g['add_cont'],
                        add_cont_gkp=g['add_cont_gkp'],
                        group_id=g['id'],
                    ),
                )

                sum_enrolled_gkp += g['enrolled_gkp']

            self.assertEqual(
                sum_enrolled_gkp,
                self._sum('28', enrolled_result),
                'Сумма показателей enrolled_gkp не равна сумме по показателю 28',
            )

            # проверка свободных мест по группам
            dou_is_unfunctioning = get_dou_status(report_form_row.unit) in NOT_CALCULATED_STATUSES
            total_groups_free_space = 0
            for g in dou_groups:
                calc_free_space = 0
                if not dou_is_unfunctioning:
                    calc_free_space = g['capacity'] - (g['enrolled'] + g['add_cont'] + g['transfer_space'])

                if calc_free_space <= 0:
                    self.assertEqual(
                        g['free_space'], 0, 'Сумма свободных мест по группе id={} должна равняться 0'.format(g['id'])
                    )
                else:
                    self.assertEqual(
                        g['free_space'],
                        calc_free_space,
                        'Сумма свободных мест по группе id={} должна равняться {}'.format(g['id'], calc_free_space),
                    )

                total_groups_free_space += g['free_space']

            unit_free_space = sum(capacities_result[get_name('31', key)] for key in list(AGE_CATEGORIES_EIGHT.keys()))

            self.assertEqual(
                unit_free_space,
                total_groups_free_space,
                'Сумма свободных мест по учреждению не сходится с суммой по группам',
            )

            # значение показателя 29 должно равняться сумме показателей
            # `reduction_school` по группам
            self.assertEqual(
                sum(group['reduction_school'] for group in dou_groups),
                sum_29,
                'Не выполнена проверка 29 == reduction_school по всем группам учреждения для %s' % mo,
            )
