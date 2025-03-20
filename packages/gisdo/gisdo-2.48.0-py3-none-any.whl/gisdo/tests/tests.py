import datetime
import json
import unittest
from itertools import (
    chain,
)

import factory
from dateutil.relativedelta import (
    relativedelta,
)
from django.apps import (
    apps,
)
from django.core.cache import (
    cache,
)
from django.core.management import (
    call_command,
)
from django.db.models import (
    signals,
)
from django.template import (
    loader,
)
from django.test import (
    TestCase,
)
from factory.django import (
    mute_signals,
)
from future.builtins import (
    map,
    range,
)
from lxml import (
    etree,
)

from m3.plugins import (
    ExtensionManager,
)

from kinder.core.children.tests import (
    factory_child,
)
from kinder.core.declaration.models import (
    DeclarationStatusLog,
    DeclarationUnit,
)
from kinder.core.declaration.tests import (
    factory_declaration,
)
from kinder.core.declaration_status.enum import (
    DSS,
)
from kinder.core.declaration_status.models import (
    DeclarationStatus,
)
from kinder.core.dict.models import (
    HNE,
    DouType,
    GroupOrientationDocuments,
    GroupType,
    GroupTypeEnumerate,
    HealthNeed,
    WorkType,
)
from kinder.core.direct.models import (
    DRS,
    DirectStatus,
)
from kinder.core.direct.proxy import (
    DirectModel,
)
from kinder.core.direct.tests import (
    factory_direct,
)
from kinder.core.group.enum import (
    GroupStatusEnum,
)
from kinder.core.group.models import (
    Pupil,
)
from kinder.core.group.tests import (
    factory_group,
)
from kinder.core.unit.models import (
    FilialType,
    FilialTypeStatus,
    Unit,
    UnitKind,
    UnitStatus,
)
from kinder.core.unit.tests import (
    factory_unit,
)

from gisdo import (
    constants as const,
    xml_helpers,
)
from gisdo.alchemy_session import (
    session_scope,
)
from gisdo.algorithm.enrolled import (
    get_22_8_x_index,
    get_22_index,
    get_22_x_index,
    get_30_1_index,
    get_30_2_index,
)
from gisdo.algorithm.utils import (
    HealthNeedIdsProvider,
)
from gisdo.index import (
    ApplicationIndex,
    get_queue_index,
    get_queue_index_collection,
)
from gisdo.index.enrolled import (
    Index,
)
from gisdo.models import (
    ReportFormRow,
    ScheduleSettings,
)
from gisdo.service import (
    DouData,
    TemplateView,
)
from gisdo.tests.checklist_tests import (
    CheckListsTestCase,
)
from gisdo.tests.utils import (
    TestReportService,
    make_decl_list,
    make_dou_list,
)
from gisdo.utils import (
    DateMixin,
    UnitHelper,
)
from gisdo.xml_helpers import (
    get_filial_num,
)

from ..models import (
    GisdoUnit,
)
from .factory_gisdo import (
    GisdoUnitFactory,
)


class TestDbCheckListsTestCase(CheckListsTestCase):
    """Запускает проверки на пустой БД, только для проверки работоспособности
    тестов на проверки ФО, проверка самих данных уже собранных отчетов
     проходит в другом TestCase"""

    def setUp(self):
        self.report_form_row = self._create_data()
        self.mo = self.report_form_row.unit.get_mo()

    @staticmethod
    def _create_data():
        """Создаем видимость данных,
        чтобы класс сбора ФО не ругался что нет данных в МО
        """
        with mute_signals(signals.post_save):
            region, mo_list, dou_list = make_dou_list()
            make_decl_list(mo_list, [DSS.REGISTERED, DSS.PRIV_CONFIRMATING], count_decl=5)
        # сборка отчета
        report_service = TestReportService(region)
        report_service.collect()
        # запускаем тесты для 1 мо
        mo = mo_list[0]
        report_form_row = ReportFormRow.objects.get(report_id=report_service._report_form.id, unit=mo)
        return report_form_row


# todo: Правильно (хоть и медленней) переделать тесты на данные collect_report
class BaseGisdoReportTestCase(TestCase):
    """Базовый класс для тестов показателей gisdo.

    Позволяет указывать только нужные для сбора группы данных для ускорения.

    collect_only - список данных которые будут собираться:
        Показатели: 'applications', 'queues', 'enrolled', 'capacities'
        `None` - будут собираться все
        `()` - собираться не будут (подходит для XML)
    """

    collect_only = None

    def setUp(self):
        super(BaseGisdoReportTestCase, self).setUp()
        cache.clear()

    def collect_report(self, region):
        """Строит отчет региону.

        Возвращает форму отчетности.
        """
        report_service = TestReportService(
            region,
            collect_only=self.collect_only,
        )
        report_service.collect()
        return report_service._report_form

    @staticmethod
    def get_report_form_row(unit, report_form):
        """Возвращает строку с данными отчета по указанной организации."""
        return report_form.reportformrow_set.get(unit=unit)


class BaseXmlResultsTest(BaseGisdoReportTestCase):
    """Тестирует данные итоговой XML отчета."""

    collect_only = ()

    @staticmethod
    def _get_report_xml_string(mo, report_form):
        """Возвращает строку с XML данными отчета по конкретному МО"""
        document = TemplateView(
            mo,
            report_form.date,
            ScheduleSettings.get_settings(),
            UnitHelper(report_form.unit),
            report_form,
            region_data=False,
        )

        return loader.render_to_string('ws/gisdo_request_template_5_0.xml', {'doc': document}).encode('utf-8')


class UnitHelperTestCase(BaseGisdoReportTestCase):
    """
    Тесты для класса работы с деревом учреждений
    """

    def setUp(self):
        super(UnitHelperTestCase, self).setUp()
        with mute_signals(signals.post_save):
            self.region = factory_unit.UnitRFactory(name='Татарстан')
            self.mo_kazan = factory_unit.UnitMoFactory(name='Казань', parent=self.region)
            self.mo_kazan.save()
            self.mo_chelny = factory_unit.UnitMoFactory(name='Наб. Челны', parent=self.region)
            self.mo_chelny.save()
            self.mo_arsk = factory_unit.UnitMoFactory(name='Арск', parent=self.region)
            self.mo_arsk.save()
            self.mo_list = [self.mo_kazan, self.mo_chelny]
            self.count_dou_in_mo = 10
            for mo in self.mo_list:
                for dou_i in range(0, self.count_dou_in_mo):
                    dou = factory_unit.UnitDouFactory(
                        parent=mo,
                        name=dou_i,
                    )
                    GisdoUnitFactory(unit=dou)

    def test_mo_count(self):
        """Проверки:
        - в список мо для расчета, попадают только мо, под которыми есть доу
        :return:
        """
        self.unit_helper = UnitHelper(self.region)
        mo_count = len(list(self.unit_helper.get_report_units()))
        self.failUnlessEqual(len(self.mo_list), mo_count)

    def test_get_mo_units(self):
        """Проверка что в МО нужное колво доу попадает в ФО
        :return:
        """

        self.unit_helper = UnitHelper(self.region)
        # в мо 10 доу
        self.failUnlessEqual(len(self.unit_helper.get_mo_units(self.mo_kazan.id)), self.count_dou_in_mo)

        # одному Доу укажем "Относится к МО" Челны
        dou = self.unit_helper.get_mo_units(self.mo_kazan.id)[0]
        gisdo_unit = GisdoUnit.objects.get(unit=dou)
        gisdo_unit.related_to_mo = self.mo_chelny
        gisdo_unit.save()

        self.unit_helper = UnitHelper(self.region)
        # в мо Казань 9 доу
        self.failUnlessEqual(len(self.unit_helper.get_mo_units(self.mo_kazan.id)), self.count_dou_in_mo - 1)
        # в мо Челны 11 доу
        self.failUnlessEqual(len(self.unit_helper.get_mo_units(self.mo_chelny.id)), self.count_dou_in_mo + 1)


class FilialsTestCase(BaseGisdoReportTestCase):
    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(FilialsTestCase, self).setUp()
        self.region = factory_unit.UnitRFactory(name='Татарстан')
        mo = factory_unit.UnitMoFactory(name='Казань', parent=self.region)
        mo.save()
        self.dou = factory_unit.UnitDouFactory(parent=mo)
        self.dou.save()
        GisdoUnitFactory(unit=self.dou)
        self.filial = factory_unit.FilialFactory(parent=mo)
        GisdoUnitFactory(unit=self.filial)
        factory_unit.FilialDataFactory(head=self.dou, filial=self.filial)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_num_buildings(self):
        """не учитывать организации (корпуса/филиалы),
         у которых статус = "Закрыто", "Ликвидировано",
            "Присоединена у другой организации"
        :return:
        """
        # не факт групп в филиале
        self.assertEquals(0, get_filial_num(self.dou))

        # добавим группу
        factory_group.FactGroupF(unit=self.filial)
        self.assertEquals(1, get_filial_num(self.dou))
        # если учреждение в статусах "Закрыто", "Ликвидировано",
        # "Присоединена у другой организации"
        # не отдаем
        self.filial.status = UnitStatus.CLOSED
        self.filial.closed = True
        self.filial.save()
        self.assertEquals(0, get_filial_num(self.dou))

        self.filial.status = UnitStatus.LIQUIDATED
        self.filial.closed = False
        self.filial.save()
        self.assertEquals(0, get_filial_num(self.dou))


class QueueIndexTest(BaseGisdoReportTestCase):
    """
    Тесты для группы показателей "Информация о детях в очереди"
    """

    collect_only = ('queues',)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(QueueIndexTest, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Татарстан')
        mo = factory_unit.UnitMoFactory(parent=self.region)
        self.dou = factory_unit.UnitDouFactory(parent=mo)
        GisdoUnitFactory(unit=self.dou)

        self.combi_group = factory_group.FactGroupF(
            name='Комбинированная', unit=self.dou, type=GroupType.get_by_code(GroupTypeEnumerate.COMBI)
        )

        self.decl_list = []
        for i in range(0, 10):
            child = factory_child.ChildF.create()

            decl = factory_declaration.DeclarationF.create(
                children=child, mo=mo, status=DeclarationStatus.get_by_code(DSS.DUL_CONFIRMATING)
            )
            factory_declaration.DUnitF(declaration=decl, unit=self.dou)
            self.decl_list.append(decl)

    def test_7(self):
        """
        - Заявления в статусах "Зарегистрировано" и "Подтверждение льгот".
        - Заявления в других статусах, у которых есть привязанные
            направления в статусах в факт/план группы в статусах:
                "Заключение договора", "Подтверждено",
                "Направлен в ДОУ", "Предложено системой".
        - Исключены заявления в статусе "Желает изменить ДОО".
        - Исключены заявления детей у которых "есть зачисление":
            у ребенка есть хотя бы одно зачисление в статус группы которой
            "Фактическая" либо "Плановая",
            не учитываются временные зачисления и отчисления.
        - Дата желаемого зачисления текущий учебный год - >= 02.09.2015
          (т.е. все заявки позже этой даты (включительно)).
        - Дата расчета возраста: на 01.09.2015 (текущего календарного года).
        :return:
        """
        self.assertEquals(0, len(get_queue_index_collection('7', self.dou)))
        self.decl_list[0].status = DeclarationStatus.get_by_code(DSS.REGISTERED)
        self.decl_list[0].save()
        self.decl_list[1].status = DeclarationStatus.get_by_code(DSS.PRIV_CONFIRMATING)
        self.decl_list[1].save()
        self.assertEquals(0, len(get_queue_index_collection('7', self.dou)))

        self.decl_list[0].defer_demand = True
        self.decl_list[0].save()
        self.assertEquals(1, len(get_queue_index_collection('7', self.dou)))

    def test_181(self):
        """
        "Учитываются заявки в статусах ""Зарегистрировано""
        и ""Подтверждение льгот""
        + заявки в других статусах, у которых есть привязанные направления
        в статусах ""Подтверждено"", ""Предложено системой""
        - заявления в статусе ""Желает изменить ДОУ"".
        Дата желаемого зачисления <= 01.09.2015 (без желаемой датой зачисления),
        (01.09.текущего учебного года)
        :return:
        """

        self.assertEquals(0, len(get_queue_index_collection('18.1', self.dou)))
        self.decl_list[0].status = DeclarationStatus.get_by_code(DSS.REGISTERED)
        self.decl_list[0].save()
        self.decl_list[1].status = DeclarationStatus.get_by_code(DSS.PRIV_CONFIRMATING)
        self.decl_list[1].save()
        self.assertEquals(2, len(get_queue_index_collection('18.1', self.dou)))

        self.decl_list[3].status = DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU)
        self.assertEquals(2, len(get_queue_index_collection('18.1', self.dou)))
        direct = factory_direct.DirectFactory(group=self.combi_group, declaration=self.decl_list[4])
        self.assertEquals(3, len(get_queue_index_collection('18.1', self.dou)))
        DirectModel.change_status(direct, DirectStatus.objects.get(code=DRS.CONFIRM))
        self.assertEquals(3, len(get_queue_index_collection('18.1', self.dou)))

        self.decl_list[0].defer_demand = True
        self.decl_list[0].save()
        self.assertEquals(2, len(get_queue_index_collection('18.1', self.dou)))

    def test_18_4(self):
        """Тест показателя 18.4."""

        decl_1 = self.decl_list[0]
        decl_1.status = DeclarationStatus.get_by_code(DSS.REGISTERED)
        decl_1.save()
        direct_1 = factory_direct.DirectFactory(
            declaration=decl_1,
            status=DirectStatus.objects.get(code=DRS.NEW),
            temporary=False,
            group=self.combi_group,
        )

        decl_2 = self.decl_list[1]
        decl_2.status = DeclarationStatus.get_by_code(DSS.REGISTERED)
        decl_2.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        queues = json.loads(dou_report_form_row.queues)

        # Оба Заявления попадают
        self.assertEquals(
            2,
            sum(queues['18.4'].values()),
            'Ошибка в показателе 18.4 по организации %s' % self.dou.name,
        )

        direct_1.status = DirectStatus.objects.get(code=DRS.REGISTER)
        direct_1.save()
        factory_group.PupilF(grup=self.combi_group, children=decl_2.children)

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        queues = json.loads(dou_report_form_row.queues)

        # Заявление `decl_1` перестает попадать из-за статуса направления.
        # Заявление `decl_2` перестает попадать из-за зачисления.
        self.assertEquals(
            0,
            sum(queues['18.4'].values()),
            'Ошибка в показателе 18.4 по организации %s' % self.dou.name,
        )

    def test_18_4_two_directs(self):
        decl_1 = self.decl_list[0]
        decl_1.status = DeclarationStatus.get_by_code(DSS.REGISTERED)
        decl_1.save()

        direct_1 = factory_direct.DirectFactory(
            declaration=decl_1,
            temporary=False,
            group=self.combi_group,
        )

        direct_2 = factory_direct.DirectFactory(
            declaration=decl_1,
            temporary=False,
            group=self.combi_group,
        )
        direct_2.status = DirectStatus.objects.get(code=DRS.DOGOVOR)
        direct_2.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        queues = json.loads(dou_report_form_row.queues)

        # Заявление не попадает т.к. одно из направлений со статусом
        # "Заключение договора"
        self.assertEquals(
            0,
            sum(queues['18.4'].values()),
            'Ошибка в показателе 18.4 по организации %s' % self.dou.name,
        )


class CapacitiesIndexTest(BaseGisdoReportTestCase):
    """
    Тесты для группы показателей "Информация о свободных местах"
    """

    collect_only = ('capacities',)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(CapacitiesIndexTest, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Татарстан')
        mo = factory_unit.UnitMoFactory(parent=self.region)
        self.dou = factory_unit.UnitDouFactory(parent=mo)
        GisdoUnitFactory(unit=self.dou)
        self.decl_list = []
        for i in range(0, 10):
            child = factory_child.ChildF.create()

            decl = factory_declaration.DeclarationF.create(
                children=child, mo=mo, status=DeclarationStatus.get_by_code(DSS.DUL_CONFIRMATING)
            )
            factory_declaration.DUnitF(declaration=decl, unit=self.dou)
            self.decl_list.append(decl)

    def test_33_index(self):
        """
        Передается численность детей, снятых с учета в течение
        **текущего календарного года** по таким причинам:

        1. Не явился (код didnt_come)
        2. Отказано в услуге (код refused)
            в случае изменения заявления со статуса
            Зарегистрировано, Желает изменить ДОУ на статус
            Отказано в услуге
        3. Архивное (код archive)
            в случае изменения заявления со статуса
            Зарегистрировано на статус Архивное
        4. Архивное (код archive)
            в случае изменения заявления со статуса
            Желает изменить ДОУ на Архивное

        При расчета показателя 33 необходимо учитывать все заявления,
        у которых дата изменения статуса заявления входит в период с 01.01.хххх,
        где хххх - текущий год.
        :return:
        """

        self.assertEquals(0, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)
        # 1
        self.decl_list[0].change_status(DeclarationStatus.get_by_code(DSS.DIDNT_COME))
        self.assertEquals(1, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)
        # 2
        self.assertEquals(self.decl_list[1].status.code, DSS.DUL_CONFIRMATING, 'У заявления неверный статус')
        self.decl_list[1].change_status(DeclarationStatus.get_by_code(DSS.REFUSED))
        self.assertEquals(1, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)

        self.decl_list[2].change_status(DeclarationStatus.get_by_code(DSS.REGISTERED))
        self.decl_list[2].change_status(DeclarationStatus.get_by_code(DSS.REFUSED))
        self.assertEquals(2, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)

        self.decl_list[3].change_status(DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU))
        self.decl_list[3].change_status(DeclarationStatus.get_by_code(DSS.REFUSED))
        self.assertEquals(3, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)

        # 3
        self.decl_list[4].change_status(DeclarationStatus.get_by_code(DSS.ARCHIVE))
        self.assertEquals(
            3,
            get_queue_index('33', self.dou),
            'Кол-во не должно изменится, тк не выполнено условиечто статус был "Зарегистрировано"',
        )

        self.decl_list[4].change_status(DeclarationStatus.get_by_code(DSS.REGISTERED))
        self.decl_list[4].change_status(DeclarationStatus.get_by_code(DSS.ARCHIVE))
        self.assertEquals(4, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)
        # 4
        self.decl_list[5].change_status(DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU))
        self.decl_list[5].change_status(DeclarationStatus.get_by_code(DSS.ARCHIVE))
        self.assertEquals(5, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)

        # проверка на дату изменения
        DeclarationStatusLog.objects.filter(status=DeclarationStatus.get_by_code(DSS.ARCHIVE)).update(
            datetime=datetime.datetime.now() - relativedelta(years=1)
        )
        self.assertEquals(3, get_queue_index('33', self.dou), 'Ошибка по организации %s' % self.dou.name)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_32_x(self):
        today = datetime.date.today()
        decl = self.decl_list[0]
        group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )

        new_direct = factory_direct.DirectFactory.create(
            group=group, declaration=decl, date=today - datetime.timedelta(days=1)
        )

        old_direct = factory_direct.DirectFactory.create(
            group=group, declaration=decl, date=today - datetime.timedelta(days=2)
        )

        # последнее - зачислен / предпоследнее - не явился
        new_direct.status = DirectStatus.objects.get(code=DRS.ACCEPT)
        new_direct.save()
        old_direct.status = DirectStatus.objects.get(code=DRS.REJECT)
        old_direct.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        capacities = json.loads(dou_report_form_row.capacities)

        # должен попасть в 32 и 32.1
        self.assertEqual(sum(capacities['32'].values()), 1)
        self.assertEqual(sum(capacities['32.1'].values()), 1)
        self.assertEqual(sum(capacities['32.2'].values()), 0)

        # последнее - не явился / предпоследнее - зачислен
        new_direct.status = DirectStatus.objects.get(code=DRS.REJECT)
        new_direct.save()
        old_direct.status = DirectStatus.objects.get(code=DRS.ACCEPT)
        old_direct.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        capacities = json.loads(dou_report_form_row.capacities)

        # должен попасть в 32.1 и 32.2
        self.assertEqual(sum(capacities['32'].values()), 0)
        self.assertEqual(sum(capacities['32.1'].values()), 1)
        self.assertEqual(sum(capacities['32.2'].values()), 1)


@unittest.skipIf(
    not apps.is_installed('kinder.plugins.archival_directions'),
    'Не подключен плагин "Архивные направления" (archival_directions)',
)
class CapacitiesIndexTestWithArchivalDirections(CapacitiesIndexTest):
    """
    Тесты для группы показателей "Информация о свободных местах"
    c включенным плагином "Архивные направления".

    """

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(CapacitiesIndexTestWithArchivalDirections, self).setUp()

        call_command('archive_direct_status')

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_32_x_with_archival_directions(self):
        archive_status_code = ExtensionManager().execute(
            'kinder.plugins.archival_directions.extensions.get_archive_status_code'
        )

        today = datetime.date.today()
        decl = self.decl_list[0]
        group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )

        new_direct = factory_direct.DirectFactory.create(
            group=group, declaration=decl, date=today - datetime.timedelta(days=1)
        )

        old_direct = factory_direct.DirectFactory.create(
            group=group, declaration=decl, date=today - datetime.timedelta(days=2)
        )

        # последнее - архив / предпоследнее - зачислен
        new_direct.status = DirectStatus.objects.get(code=archive_status_code)
        new_direct.save()
        old_direct.status = DirectStatus.objects.get(code=DRS.ACCEPT)
        old_direct.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        capacities = json.loads(dou_report_form_row.capacities)

        # должен попасть в 32 и 32.1
        self.assertEqual(sum(capacities['32'].values()), 1)
        self.assertEqual(sum(capacities['32.1'].values()), 1)
        self.assertEqual(sum(capacities['32.2'].values()), 0)

        # последнее - не явился / предпоследнее - архив
        new_direct.status = DirectStatus.objects.get(code=DRS.REJECT)
        new_direct.save()
        old_direct.status = DirectStatus.objects.get(code=archive_status_code)
        old_direct.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        capacities = json.loads(dou_report_form_row.capacities)

        # должен попасть в 32.1 и 32.2
        self.assertEqual(sum(capacities['32'].values()), 0)
        self.assertEqual(sum(capacities['32.1'].values()), 1)
        self.assertEqual(sum(capacities['32.2'].values()), 1)


class ApplicationIndexTest(BaseGisdoReportTestCase):
    """
    Тесты для группы показателей "Информация о заявлениях"
    """

    collect_only = ('applications',)

    def test_sum_age_slice_equal_sum_delivery_slice(self):
        """
        Проверяем, чтобы сумма количества заявлений в разрезе возрастных
        категорий была равно сумме количества заявлений в разрезе типа подачи
        """

        units = Unit.objects.filter(kind__id=4)

        with session_scope() as session:
            for dou in units:
                index = ApplicationIndex(dou, session)
                sum_in_age_slice = 0
                for age in list(const.AGE_CATEGORIES_FULL.values()):
                    sum_in_age_slice += index.get_count(age_range=age)
                sum_in_delivery_slice = 0
                sum_in_delivery_slice += index.get_count(index_type=ApplicationIndex.COUNT_BY_DELIVERY, age_range=age)
                sum_in_delivery_slice += index.get_count(
                    index_type=ApplicationIndex.COUNT_BY_DELIVERY, portal=1, age_range=age
                )
                self.assertEquals(sum_in_age_slice, sum_in_delivery_slice, 'Ошибка по организации %s' % dou.name)


class EnrolledIndexTest(BaseXmlResultsTest):
    """
    Тесты для группы показателей "Информация о зачисленных детях"
    Важно! У класса gisdo.index.enrolled.Index cписок групп кешируется,
    поэтому при изменение группы неоходимо создавать новый инстанс индекса
    """

    collect_only = ('enrolled',)

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(EnrolledIndexTest, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Татарстан')

        self.mo = factory_unit.UnitMoFactory(parent=self.region, name='МО')

        self.dou = factory_unit.UnitDouFactory(parent=self.mo, name='ДОО')
        GisdoUnitFactory(unit=self.dou)

        self.filial = factory_unit.FilialFactory(parent=self.mo, name='Филиал')
        GisdoUnitFactory(unit=self.filial)
        factory_unit.FilialDataFactory(head=self.dou, filial=self.filial)

        self.child_list = []
        for i in range(0, 10):
            self.child_list.append(factory_child.ChildF.create())

        self.comp_group = factory_group.FactGroupF(
            name='Компенсирующая',
            unit=self.dou,
            type=GroupType.get_by_code(GroupTypeEnumerate.COMP),
        )
        self.health_group = factory_group.FactGroupF(
            name='Оздоровительная',
            unit=self.dou,
            type=GroupType.get_by_code(GroupTypeEnumerate.HEALTH),
        )
        self.combi_group = factory_group.FactGroupF(
            name='Комбинированная',
            unit=self.dou,
            type=GroupType.get_by_code(GroupTypeEnumerate.COMBI),
        )
        self.fact_group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )
        self.plan_group = factory_group.PlanGroupF(
            name='Плановая',
            unit=self.dou,
            room=self.fact_group.room,
        )
        self.filial_fact_group = factory_group.FactGroupF(
            name='Фактическая филиала',
            unit=self.filial,
        )
        self.filial_plan_group = factory_group.PlanGroupF(
            name='Плановая филиала',
            unit=self.filial,
            room=self.filial_fact_group.room,
        )
        self.filial_fact_short_wt_group = factory_group.FactGroupF(
            name='Фактическая кратковременная филиала',
            unit=self.filial,
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
        )
        self.filial_plan_short_wt_group = factory_group.PlanGroupF(
            name='Плановая кратковременная филиала',
            unit=self.filial,
            room=self.filial_fact_short_wt_group.room,
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
        )
        self.short_wt_fact_group = factory_group.FactGroupF(
            name='Фактическая кратковременного пребывания',
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
            unit=self.dou,
        )
        self.full_wt_fact_group = factory_group.FactGroupF(
            name='Фактическая полного дня',
            work_type=factory_group.WorkTypeF(code=WorkType.FULL),
            unit=self.dou,
        )
        self.short_wt_plan_group = factory_group.PlanGroupF(
            name='Плановая кратковременного пребывания',
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
            unit=self.dou,
            room=self.short_wt_fact_group.room,
        )
        self.short_wt_filial_fact_group = factory_group.FactGroupF(
            name='Фактическая кратковременного пребывания филиала',
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
            unit=self.filial,
        )
        self.short_wt_filial_plan_group = factory_group.PlanGroupF(
            name='Плановая кратковременного пребывания филиала',
            work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
            unit=self.filial,
            room=self.short_wt_filial_fact_group.room,
        )

    def test_enrolled_index_fact_priority_main_to_filial(self):
        """В случае если ребенок числился в факт. группе в головной
        организации, а в плановой группе был переведен в филиал или корпус,
        такого ребенка необходимо учитывать в расчете 1 раз по факт. группе
        """
        enrolled_index = Index(self.dou)

        factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.filial_plan_group, children=self.child_list[0])

        self.assertEquals(1, len(list(enrolled_index())))

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)
        groups = list(chain(*(building['groups'] for building in dou_data.buildings)))

        main_enrolled = [g for g in groups if g['id'] == self.fact_group.id][0]['enrolled']
        self.assertEquals(1, main_enrolled)

        total_enrolled = sum(group['enrolled'] for group in groups)
        self.assertEquals(1, total_enrolled)

    def test_enrolled_index_fact_priority_filial_to_main(self):
        """В случае если ребенок числился в факт. группе в филиальной
        организации, а в плановой группе был переведен в головную организацию,
        такого ребенка необходимо учитывать в расчете 1 раз по факт. группе
        """
        enrolled_index = Index(self.dou)

        factory_group.PupilF(grup=self.plan_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.filial_fact_group, children=self.child_list[0])

        self.assertEquals(1, len(list(enrolled_index())))

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)
        groups = list(chain(*(building['groups'] for building in dou_data.buildings)))

        filial_enrolled = [g for g in groups if g['id'] == self.filial_fact_group.id][0]['enrolled']
        self.assertEquals(1, filial_enrolled)

        total_enrolled = sum(group['enrolled'] for group in groups)
        self.assertEquals(1, total_enrolled)

    def test_enrolled_includes_filials(self):
        """В список зачисленных по ДОО попадают также дети связанных филиалов"""
        enrolled_index = Index(self.dou)

        factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.filial_fact_group, children=self.child_list[1])

        self.assertEquals(2, len(list(enrolled_index())))

    def test_enrolled_index_unique_different_groups(self):
        """В список зачисленных ребенок должен попадать 1 раз
        в случае если он зачислен в две разные группы
        """
        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[0])

        self.assertEquals(len(list(enrolled_index())), 1)

    def test_enrolled_index_unique_same_group(self):
        """В список зачисленных ребенок должен попадать 1 раз
        в случае если он зачислен в одну и ту же группу
        """
        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])

        self.assertEquals(len(list(enrolled_index())), 1)

    def test_enrolled_index_fact_priority(self):
        """В список зачисленных ребенок приоритетно попадает
        по фактическим группам
        """
        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.plan_group, children=self.child_list[0])
        fact_pupil_0 = factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])

        fact_pupil_1 = factory_group.PupilF(grup=self.fact_group, children=self.child_list[1])
        factory_group.PupilF(grup=self.plan_group, children=self.child_list[1])

        pupils_fact_group_filtered_count = (
            Pupil.objects.filter(enrolled_index.pupil_filter).filter(id__in=(fact_pupil_0.id, fact_pupil_1.id)).count()
        )

        self.assertEquals(pupils_fact_group_filtered_count, 2)

    def test_191(self):
        """
        Количество детей в текущих группах.
         Временно зачисленные учитываются, временно отчисленные нет.
        :return:
        """
        enrolled_index = Index(self.dou)
        index_19 = list(enrolled_index())
        self.assertEquals(0, len(index_19), 'Показатель 19 не 0')

        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        factory_group.PupilF(grup=self.health_group, temporary=True, children=self.child_list[2])

        self.assertEquals(3, len(list(enrolled_index())))

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_20_8(self):
        """
        Показатель 20.8

        То же что и 20.5-й, но остаются только те заявления
        дети в которых зачислены в ДОО с типом:
            НЕ муниципальная/федеральная/государственная,
        и планируют перейти в ДОО с типом:
        муниципальная/федеральная/государственная.
        """
        self.government_dou = factory_unit.UnitDouFactory(
            parent=self.mo, dou_type=DouType.objects.get(code=DouType.MUNICIPAL)
        )
        GisdoUnitFactory(unit=self.government_dou)
        self.private_dou = factory_unit.UnitDouFactory(
            parent=self.mo, dou_type=DouType.objects.get(code=DouType.IP_WITH_LICENSE)
        )
        GisdoUnitFactory(unit=self.private_dou)

        self.government_group = factory_group.FactGroupF(
            unit=self.government_dou,
        )
        self.private_group = factory_group.FactGroupF(unit=self.private_dou)

        # учится в гос. и имеет заявление в частный (не подходит)
        factory_group.PupilF(grup=self.government_group, children=self.child_list[0])
        DeclarationUnit.objects.create(
            declaration=factory_declaration.DeclarationF(
                children=self.child_list[1],
                mo=self.mo,
                status=DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU),
            ),
            unit=self.private_dou,
        )

        # учится в гос. и имеет заявление в гос. (не подходит)
        factory_group.PupilF(grup=self.government_group, children=self.child_list[1])
        DeclarationUnit.objects.create(
            declaration=factory_declaration.DeclarationF(
                children=self.child_list[1],
                mo=self.mo,
                status=DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU),
            ),
            unit=self.government_dou,
        )

        # учится в частном и имеет заявление в гос (подходит)
        factory_group.PupilF(grup=self.private_group, children=self.child_list[2])
        DeclarationUnit.objects.create(
            declaration=factory_declaration.DeclarationF(
                children=self.child_list[2],
                mo=self.mo,
                status=DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU),
            ),
            unit=self.government_dou,
        )

        # учится в частном и имеет заявление в частный (не подходит)
        factory_group.PupilF(grup=self.government_group, children=self.child_list[3])
        DeclarationUnit.objects.create(
            declaration=factory_declaration.DeclarationF(
                children=self.child_list[3],
                mo=self.mo,
                status=DeclarationStatus.get_by_code(DSS.WANT_CHANGE_DOU),
            ),
            unit=self.private_dou,
        )

        report_form = self.collect_report(self.region)
        gov_report_form_row = self.get_report_form_row(self.government_dou, report_form)
        priv_report_form_row = self.get_report_form_row(self.private_dou, report_form)

        gov_enrolled = json.loads(gov_report_form_row.enrolled)
        priv_enrolled = json.loads(priv_report_form_row.enrolled)

        # итого по гос саду 0
        self.assertEquals(
            0,
            sum(gov_enrolled['20.8'].values()),
            'Ошибка в показателе 20_8 по организации %s' % self.government_dou.name,
        )

        # итого по частному саду 1
        self.assertEquals(
            1, sum(priv_enrolled['20.8'].values()), 'Ошибка в показателе 20_8 по организации %s' % self.private_dou.name
        )

    def test_22(self):
        """
        Общая численность детей, зачисленных в группы для детей с ОВЗ.
        Количество детей в текущих группах с направленностью "Комбинированноая"
         или/и "Компенсирующая".Временно отчисленные не учитываются.
        :return:
        """
        enrolled_index = Index(self.dou)
        self.assertEquals(0, len(get_22_index(enrolled_index)), 'Показатель 22 не 0')

        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        factory_group.PupilF(grup=self.health_group, children=self.child_list[2])

        self.assertEquals(2, len(get_22_index(enrolled_index)))

    def test_221(self):
        """
        Передается общая численность детей с ОВЗ, зачисленных в
        группы компенсирующей и комбинированной направленности для детей с
        нарушением слуха.
        Количество детей в группе "Компенсирующая" с овз = с нарушением слуха
        (deafness, hardofhearing). Дети в комбинированных группа
        с овз =(deafness, hardofhearing) у которых в карточке ребенка есть овз
        (если у ребенка выбран ОВЗ оздор. типа эти дети попадают в показатель
        только при наличии заполненного поля Документ, подтверждающий ОВЗ)
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются.
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_1 = HealthNeedIdsProvider.get_health_need_22_1()

        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_1)), 'Показатель 22.1 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.DEAFNESS)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_1)))

        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.HARDOFHEARTING)
        self.combi_group.health_need = health_need
        self.combi_group.save()
        self.child_list[1].health_need = health_need
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_1)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_1)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_1)))

    def test_222(self):
        """
        Количество детей в группе "Компенсирующая" с овз = с нарушением речи
        (speach, phonetics). Дети в комбинированных группа
        с овз =(speach, phonetics) у которых в карточке ребенка есть овз
        (если у ребенка выбран ОВЗ оздор. типа эти дети попадают в показатель
        только при наличии заполненного поля Документ, подтверждающий ОВЗ)
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются.
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_2 = HealthNeedIdsProvider.get_health_need_22_2()

        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_2)), 'Показатель 22.2 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.SPEACH)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_2)))

        enrolled_index = Index(self.dou)
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.PHONETICS)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.PHONETICS)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_2)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_2)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_2)))

    def test_223(self):
        """
        Количество детей в группе "Компенсирующая" с овз =
        для детей с нарушением зрения(blindness, AMAUROSIS).
        Дети в комбинированных группа с овз = (blindness, AMAUROSIS)
        у которых в карточке ребенка овз (
        если у ребенка выбран ОВЗ оздор. типа ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ).
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_3 = HealthNeedIdsProvider.get_health_need_22_3()

        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_3)), 'Показатель 22.3 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.BLINDNESS)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_3)))

        enrolled_index = Index(self.dou)
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.AMAUROSIS)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.AMAUROSIS)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_3)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_3)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_3)))

    def test_224(self):
        """
        Количество детей в группе "Компенсирующая" с овз = с нарушением интел.
        (backwardnesslight, backwardnesshard). Дети в комбинированных группа
        с овз =(backwardnesslight, backwardnesshard)
        у которых в карточке ребенка есть овз
        (если у ребенка выбран ОВЗ оздор. типа эти дети попадают в показатель
        только при наличии заполненного поля Документ, подтверждающий ОВЗ)
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются.
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_4 = HealthNeedIdsProvider.get_health_need_22_4()
        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_4)), 'Показатель 22.4 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.BACKHARD)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_4)))

        enrolled_index = Index(self.dou)
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.BACKLIGHT)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.BACKLIGHT)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_4)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_4)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_4)))

    def test_22_5_1(self):
        """
        Показатель 22.5.1

        Количество детей в группе "Компенсирующая" с овз =
         для детей с задержкой психического развития.(backwardness).
        Дети в комбинированных группа с овз = (backwardness)
        у которых в карточке ребенка овз (
        если у ребенка выбран ОВЗ оздор. типа ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ).
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """

        # пропадает по комп. группе
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.BACK)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])

        # пропадает по комб. группе
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.BACK)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.BACK)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])

        # пропадает по комб. группе при наличии документа
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # итого 3
        self.assertEquals(
            3, sum(enrolled['22.5.1'].values()), 'Ошибка в показателе 22.5.1 по организации %s' % self.dou.name
        )

        # не попадает (по типу группы)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.INVALIDITY)
        self.comp_group.save()

        # не попадает по комб. группе (нет ОВЗ)
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.NOT)
        self.child_list[1].save()

        # не попадает по комб. группе (нет документа)
        self.child_list[2].health_need_confirmation = None
        self.child_list[2].save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # осталось 0
        self.assertEquals(
            0, sum(enrolled['22.5.1'].values()), 'Ошибка в показателе 22.5.1 по организации %s' % self.dou.name
        )

    def test_22_5_2(self):
        """
        Показатель 22.5.2

        Количество детей в группе "Компенсирующая" с овз =
         для детей с задержкой психического развития.(autism).
        Дети в комбинированных группа с овз = (autism)
        у которых в карточке ребенка овз (
        если у ребенка выбран ОВЗ оздор. типа ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ).
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """

        # пропадает по комп. группе
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.AUTISM)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])

        # пропадает по комб. группе
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.AUTISM)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.AUTISM)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])

        # пропадает по комб. группе при наличии документа
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # итого 3
        self.assertEquals(
            3, sum(enrolled['22.5.2'].values()), 'Ошибка в показателе 22.5.2 по организации %s' % self.dou.name
        )

        # не попадает (по типу группы)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.INVALIDITY)
        self.comp_group.save()

        # не пропадает по комб. группе (нет ОВЗ)
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.NOT)
        self.child_list[1].save()

        # не пропадает по комб. группе (нет документа)
        self.child_list[2].health_need_confirmation = None
        self.child_list[2].save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # осталось 0
        self.assertEquals(
            0, sum(enrolled['22.5.2'].values()), 'Ошибка в показателе 22.5.2 по организации %s' % self.dou.name
        )

    def test_226(self):
        """
        Количество детей в группе "Компенсирующая" с овз =
        для детей с нарушением опорно-двигательного аппарата (disablement)
        Дети в комбинированных группа с овз = (disablement)
        у которых в карточке ребенка овз (
        если у ребенка выбран ОВЗ оздор. типа ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ).
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_6 = HealthNeedIdsProvider.get_health_need_22_6()

        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_6)), 'Показатель 22.6 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.DISABLEMENT)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_6)))

        enrolled_index = Index(self.dou)
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.DISABLEMENT)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.DISABLEMENT)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_6)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_6)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_6)))

    def test_227(self):
        """
        Количество детей в группе "Компенсирующая" с овз =
        для детей со сложным дефектом(invalidity).
        Дети в комбинированных группа с овз = (invalidity)
        у которых в карточке ребенка овз (
        если у ребенка выбран ОВЗ оздор. типа ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ).
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_7 = HealthNeedIdsProvider.get_health_need_22_7()

        self.assertEquals(0, len(get_22_x_index(enrolled_index, health_need_22_7)), 'Показатель 22.7 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.INVALIDITY)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_x_index(enrolled_index, health_need_22_7)))

        enrolled_index = Index(self.dou)
        self.combi_group.health_need = HealthNeed.get_by_code(HNE.INVALIDITY)
        self.combi_group.save()
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.INVALIDITY)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_7)))

        # для этих ОВЗ только при наличие документа
        enrolled_index = Index(self.dou)
        health_need = HealthNeed.get_by_code(HNE.SICK)
        self.child_list[2].health_need = health_need
        self.child_list[2].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[2])
        self.assertEquals(2, len(get_22_x_index(enrolled_index, health_need_22_7)))
        self.child_list[2].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        self.child_list[2].save()
        self.assertEquals(3, len(get_22_x_index(enrolled_index, health_need_22_7)))

    def test_228(self):
        """
        Количество детей в группе "Компенсирующая" с овз =
        для детей с иными ограниченными возможностями здоровья.
        постоянно зачисленные, временно зачисленные в фактическую группу.
        Временно отчисленные не учитываются
        :return:
        """
        enrolled_index = Index(self.dou)
        health_need_22_8_1 = HealthNeedIdsProvider.get_health_need_22_8_1()
        health_need_22_8_2 = HealthNeedIdsProvider.get_health_need_22_8_2()

        index_22_8_1 = get_22_8_x_index(enrolled_index, health_need_22_8_1)
        index_22_8_2 = get_22_8_x_index(enrolled_index, health_need_22_8_2)
        self.assertEquals(0, len(index_22_8_1 + index_22_8_2), 'Показатель 22.8 не 0')

        enrolled_index = Index(self.dou)
        self.comp_group.health_need = HealthNeed.get_by_code(HNE.RESTRICTION)
        self.comp_group.save()
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(1, len(get_22_8_x_index(enrolled_index, health_need_22_8_1)))

        enrolled_index = Index(self.dou)
        self.child_list[1].health_need = HealthNeed.get_by_code(HNE.DEAFNESS)
        self.child_list[1].save()
        factory_group.PupilF(grup=self.combi_group, children=self.child_list[1])
        self.assertEquals(1, len(get_22_8_x_index(enrolled_index, health_need_22_8_2)))

    def test_27(self):
        """
        Общая численность детей, зачисленных в группы кратковременного
        пребывания детей.

        Передается общая численность детей, зачисленных в группы
        кратковременного пребывания.
        """

        # ребенок должен попасть только один раз
        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.short_wt_plan_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.short_wt_filial_fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.short_wt_filial_plan_group, children=self.child_list[0])

        # попадает по фактической
        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[1])

        # попадает по плановой
        factory_group.PupilF(grup=self.short_wt_plan_group, children=self.child_list[2])

        # попадает из фактической филиала
        factory_group.PupilF(grup=self.short_wt_filial_fact_group, children=self.child_list[3])

        # попадает из плановой филиала
        factory_group.PupilF(grup=self.short_wt_filial_fact_group, children=self.child_list[4])

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # итого 5
        self.assertEquals(5, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)

    def test_28(self):
        """
        Общая численность детей, посещающих ДОО в режиме
        кратковременного пребывания.
        Описание: Передается общая численность детей, посещающих ДОО в
        режиме кратковременного пребывания вне зависимости от режима работы
        группы.
        """

        # попадает по фактической по режиму работы
        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[0])

        # попадает по фактической по режиму работы
        # (особый режим также кратковременный)
        factory_group.PupilF(
            grup=self.short_wt_fact_group,
            children=self.child_list[1],
            actual_work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
        )

        # попадает по плановой по режиму работы
        factory_group.PupilF(grup=self.short_wt_plan_group, children=self.child_list[2])

        # должен был попасть по фактической по режиму работы
        # но не исключается, из-за указанного другого режима работы
        factory_group.PupilF(
            grup=self.short_wt_fact_group,
            children=self.child_list[3],
            actual_work_type=factory_group.WorkTypeF(code=WorkType.ALLDAY),
        )

        # не должен был попасть по фактической по режиму работы
        # но попадает, т.к. указан кратковременный режим пребывания
        factory_group.PupilF(
            grup=self.fact_group,
            children=self.child_list[4],
            actual_work_type=factory_group.WorkTypeF(code=WorkType.SHORT),
        )

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # итого 5
        self.assertEquals(5, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)

    def test_27_28_enrolled_gkp_1(self):
        """
        Тест сходимости показателей 27, 28 и `enrolled_gkp`.

        Ребенок 0 - Фактическая кратковременная группа
        Ребенок 1 - Плановая кратковременная группа

        :return:
        """

        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.short_wt_plan_group, children=self.child_list[1])

        self.short_wt_plan_group.room = self.short_wt_fact_group.room
        self.short_wt_plan_group.save()

        # Попадают оба и в 27 и в 28 и в enrolled_gkp
        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(2, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(2, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEqual(
            2,
            enrolled_gkp,
            'Ошибка в enrolled_gkp по организации %s' % self.dou.name,
        )

    def test_27_28_enrolled_gkp_2(self):
        """
        Тест сходимости показателей 27, 28 и `enrolled_gkp`.

        Ребенок 0 - Фактическая группа полного дня (не попадает)
        Ребенок 1 - Плановая кратковременная группа

        :return:
        """

        factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])
        pupil_1 = factory_group.PupilF(
            grup=self.short_wt_plan_group,
            children=self.child_list[1],
        )

        self.short_wt_plan_group.room = self.fact_group.room
        self.short_wt_plan_group.save()

        # Ребенок 1.
        # Не попадает в 27
        # Попадает в 28 и enrolled_gkp (вне зависимости от особого режима)
        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(0, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(1, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(1, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

        # Ребенок 1.
        # Не попадает в 27
        # Попадает в 28 и enrolled_gkp (вне зависимости от особого режима)
        pupil_1.actual_work_type = factory_group.WorkTypeF(code=WorkType.SHORT)
        pupil_1.save()

        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(0, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(1, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(1, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

        # Ребенок 1.
        # Не попадает в 27.
        # Попадает в 28 и enrolled_gkp (по особому режиму работы)
        self.short_wt_plan_group.work_type = factory_group.WorkTypeF(code=WorkType.FULL)
        self.short_wt_plan_group.save()

        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(0, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(1, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(1, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

        # Ребенок 1.
        # Не попадает никуда
        pupil_1.actual_work_type = None
        pupil_1.save()

        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(0, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(0, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(0, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

    def test_27_28_enrolled_gkp_3(self):
        """
        Тест сходимости показателей 27, 28 и `enrolled_gkp`.

        Ребенок 0 - Фактическая кратковременная группа
        Ребенок 1 - Плановая группа полного дня

        :return:
        """

        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.plan_group, children=self.child_list[1])

        self.plan_group.room = self.short_wt_fact_group.room
        self.plan_group.save()

        # Попадают оба и в 27 и в 28 и в enrolled_gkp
        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(2, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(2, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(2, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

    def test_27_28_enrolled_gkp_4(self):
        """
        Тест сходимости показателей 27, 28 и `enrolled_gkp`.

        Ребенок 0 - Фактическая кратковременная группа
        Ребенок 1 - Фактическая группа полного дня, но ребенок
        посещает ДОО с режимом КП (но не из санпина)

        :return:
        """

        factory_group.PupilF(grup=self.short_wt_fact_group, children=self.child_list[0])
        pupil_1 = factory_group.PupilF(grup=self.full_wt_fact_group, children=self.child_list[1])

        # Ребенок 0
        # Попадает и в 27, и в 28, и в enrolled_gkp
        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(1, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(1, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(1, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

        # Ребенок 1
        # Попадает в 28 и в enrolled_gkp, не попадает в 27
        custom_work_type_code = '2'
        pupil_1.actual_work_type = factory_group.WorkTypeF(code=custom_work_type_code)
        pupil_1.save()

        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml_root = etree.fromstring(self._get_report_xml_string(self.mo, report_form))
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        self.assertEquals(1, sum(enrolled['27'].values()), 'Ошибка в показателе 27 по организации %s' % self.dou.name)
        self.assertEquals(2, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(2, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

    def test_28_enrolled_gkp(self):
        """
        Тест сходимости показателей 28 и `enrolled_gkp`.

        Ребенок 0 - Фактическая  группа полного дня
        Ребенок 0 - Плановая кратковременная группа филиала

        Плановая кратковременная группа филиала связана
        с некратковременной фактической филиала.

        :return:
        """

        factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])
        factory_group.PupilF(grup=self.filial_plan_short_wt_group, children=self.child_list[0])

        self.filial_plan_short_wt_group.room = self.filial_fact_group.room
        self.filial_plan_short_wt_group.save()

        report_form = self.collect_report(self.region)
        dou_report_form_row = self.get_report_form_row(self.dou, report_form)
        enrolled = json.loads(dou_report_form_row.enrolled)

        xml = self._get_report_xml_string(self.mo, report_form)

        xml_root = etree.fromstring(xml)
        enrolled_gkp = sum(map(int, xml_root.xpath("//*[local-name()='group']/@enrolled_gkp")))

        # Не должен попадать никуда
        self.assertEquals(0, sum(enrolled['28'].values()), 'Ошибка в показателе 28 по организации %s' % self.dou.name)
        self.assertEquals(0, enrolled_gkp, 'Ошибка в enrolled_gkp по организации %s' % self.dou.name)

    def test_30(self):
        """
        Численность детей-инвалидов, не имеющих ОВЗ.

        Передается численность детей-инвалидов, зачисленных в ДОО, не имеющих
        ограниченных возможностей здоровья.

        Расчет:
        - Дети в чек боксом "ребенок-инвалид" для временно зачисленных и
            зачисленных в фактические группы.
        - На текущую дату.
        - Разбивка по возрастам - 16 категорий.
        """

        # попадает
        # не в комп. группе
        # значение ОВЗ - "нет"
        # нет подтверждающего документа
        self.child_list[0].health_need_id = HealthNeed.get_by_code(HNE.NOT)
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[0])

        # попадает
        # не в комп. группе
        # значение ОВЗ - пусто
        # есть подтверждающий документ
        self.child_list[1].health_need_id = None
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[1])

        # попадает
        # не в комп. группе
        # значение ОВЗ - "с туберкулезной интоксикацией"
        # нет подтверждающего документа (пустой)
        self.child_list[2].health_need_id = HealthNeed.get_by_code(HNE.PHTHISIS)
        self.child_list[2].health_need_confirmation = None
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[2])

        # попадает
        # не в комп. группе
        # значение ОВЗ - "с туберкулезной интоксикацией"
        # нет подтверждающего документа
        self.child_list[3].health_need_id = HealthNeed.get_by_code(HNE.PHTHISIS)
        self.child_list[3].health_need_confirmation = None
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[3])

        # В показателе только дети с инвалидностью
        for ch in self.child_list[:4]:
            ch.is_invalid = True
            ch.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # итого 4
        self.assertEquals(4, sum(enrolled['30'].values()), 'Ошибка в показателе 30 по организации %s' % self.dou.name)

        # не попадает
        # !в комп. группе
        # значение ОВЗ - "с туберкулезной интоксикацией"
        # нет подтверждающего документа
        self.child_list[4].health_need_id = HealthNeed.get_by_code(HNE.PHTHISIS)
        self.child_list[4].health_need_confirmation = None
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[4])

        # не попадает
        # не в комп. группе
        # !значение ОВЗ - "глухие дети"
        # есть подтверждающий документ
        health_need = HealthNeed.get_by_code(HNE.DEAFNESS)
        self.child_list[5].health_need = health_need
        self.child_list[5].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[5])

        # не попадает
        # не в комп. группе
        # !значение ОВЗ - "глухие дети"
        # нет подтверждающего документа
        self.child_list[6].health_need_id = HealthNeed.get_by_code(HNE.DEAFNESS)
        self.child_list[6].health_need_confirmation = None
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[6])

        # не попадает
        # не в комп. группе
        # значение ОВЗ - "с туберкулезной интоксикацией"
        # !есть подтверждающий документ
        health_need = HealthNeed.get_by_code(HNE.PHTHISIS)
        self.child_list[7].health_need = health_need
        self.child_list[7].health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        factory_group.PupilF(grup=self.fact_group, children=self.child_list[7])

        # В показателе только дети с инвалидностью
        for ch in self.child_list[4:8]:
            ch.is_invalid = True
            ch.save()

        dou_report_form_row = self.get_report_form_row(self.dou, self.collect_report(self.region))
        enrolled = json.loads(dou_report_form_row.enrolled)

        # все равно 4
        self.assertEquals(4, sum(enrolled['30'].values()), 'Ошибка в показателе 30 по организации %s' % self.dou.name)

    def test_301(self):
        """
        Численность детей-инвалидов, имеющих ограниченные возможности здоровья.

        Передается численность детей-инвалидов, зачисленных в ДОО,
        имеющих ограниченние возможностей здоровья, посещающих группы любой
        направленности (т.е. считаем всех детей с чек-боксов ребенок-инвалид
        во всех группах).
        При этом, если у ребенка выбран ОВЗ типа "часто болеющие",
        "с туберкулезной интоксикацией",
        "другие, с необходимостью комплексных оздоровительных мероприятий" ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ.
        :return:
        """

        enrolled_index = Index(self.dou)
        self.assertEquals(0, len(get_30_1_index(enrolled_index)), 'Показатель 30.1 не 0')

        # В показателе только дети с инвалидностью
        for ch in self.child_list:
            ch.is_invalid = True
            ch.save()
        # зачислим первого ребенка в компенс. группу
        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(
            1,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей в компенсирующих группах с инвалидностью',
        )

        # зачислим второго ребенка в оздоровительную группу
        enrolled_index = Index(self.dou)
        child = self.child_list[1]
        factory_group.PupilF(grup=self.health_group, children=child)
        self.assertEquals(
            2,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей в оздор. группах с инвалидностью и ОВЗ не из списка',
        )

        health_need = HealthNeed.get_by_code(HNE.PHTHISIS)
        child.health_need = health_need
        child.save()
        self.assertEquals(
            1,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей в оздор. группах с '
            'инвалидностью и ОВЗ из списка только при наличие документа',
        )

        child.health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        child.save()
        self.assertEquals(
            2,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей в оздор. группах с '
            'инвалидностью и ОВЗ из списка только при наличие документа',
        )

        # в группах с типом отличным от оздор. и компенс.
        # проверяется наличие ОВЗ
        enrolled_index = Index(self.dou)
        child = self.child_list[2]
        factory_group.PupilF(grup=self.combi_group, children=child)
        # С ОВЗ для оздоровитеьных групп, но с типом не оздоровительная,
        # ребенок не попадет в показатель
        health_need = HealthNeed.get_by_code(HNE.PHTHISIS)
        child.health_need = health_need
        child.save()
        self.assertEquals(
            2,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп',
        )

        child.health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        child.save()
        self.assertEquals(
            3,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп, '
            'либо с подтверждением',
        )

        enrolled_index = Index(self.dou)
        child = self.child_list[3]
        factory_group.PupilF(grup=self.combi_group, children=child)
        child.health_need = HealthNeed.get_by_code(HNE.DEAFNESS)
        child.save()
        self.assertEquals(
            4,
            len(get_30_1_index(enrolled_index)),
            'Показатель 30.1 учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп',
        )

    def test_302(self):
        """
        Численность детей, не имеющих инвалидности,
        но имеющих ограниченные возможности здоровья.
        Передается численность детей, зачисленных в ДОО,
        не имеющих инвалидности, но имеющих ограниченныых возможностей
        здоровья, посещающих группы любой направленности.
        При этом, если у ребенка выбран ОВЗ типа "часто болеющие",
        "с туберкулезной интоксикацией",
        "другие, с необходимостью комплексных оздоровительных мероприятий" ,
        эти дети попадают в показатель только при наличии заполненного поля
        Документ, подтверждающий ОВЗ
        Отличие от тестов на 30.1 только отсутсвием признака инвалид детей
        :return:
        """
        enrolled_index = Index(self.dou)
        self.assertEquals(0, len(get_30_2_index(enrolled_index)), 'Показатель 30.2 не 0')

        # зачислим первого ребенка в компенс. группу
        enrolled_index = Index(self.dou)
        factory_group.PupilF(grup=self.comp_group, children=self.child_list[0])
        self.assertEquals(
            1,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2 учитывает детей в компенсирующих группах с без инвалидности',
        )

        # зачислим второго ребенка в оздоровительную группу
        enrolled_index = Index(self.dou)
        child = self.child_list[1]
        factory_group.PupilF(grup=self.health_group, children=child)
        self.assertEquals(
            2,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2 учитывает детей в оздор. группах без инвалидности и ОВЗ не из списка',
        )

        health_need = HealthNeed.get_by_code(HNE.PHTHISIS)
        child.health_need = health_need
        child.save()
        self.assertEquals(
            1,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2учитывает детей в оздор. группах без '
            'инвалидности и ОВЗ из списка только при наличие документа',
        )

        child.health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        child.save()
        self.assertEquals(
            2,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2учитывает детей в оздор. группах без '
            'инвалидности и ОВЗ из списка только при наличие документа',
        )

        # в группах с типом отличным от оздор. и компенс.
        # проверяется наличие ОВЗ
        enrolled_index = Index(self.dou)
        child = self.child_list[2]
        factory_group.PupilF(grup=self.combi_group, children=child)
        # С ОВЗ для оздоровитеьных групп, но с типом не оздоровительная,
        # ребенок не попадет в показатель
        health_need = HealthNeed.get_by_code(HNE.PHTHISIS)
        child.health_need = health_need
        child.save()
        self.assertEquals(
            2,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп',
        )

        child.health_need_confirmation = GroupOrientationDocuments.objects.get(
            desired_group_type=health_need.group_type
        )
        child.save()
        self.assertEquals(
            3,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп, '
            'либо с подтверждением',
        )

        enrolled_index = Index(self.dou)
        child = self.child_list[3]
        factory_group.PupilF(grup=self.combi_group, children=child)
        child.health_need = HealthNeed.get_by_code(HNE.DEAFNESS)
        child.save()
        self.assertEquals(
            4,
            len(get_30_2_index(enrolled_index)),
            'Показатель 30.2учитывает детей не в оздор. и не комп. группах с '
            'инвалидностью и ОВЗ, отличным от ОВЗ для оздор. групп',
        )

    # def test_sum_disabled_group_equals_sum_correct_and_health_groups(self):
    #     TODO: проверить актуален ли тест
    #     """
    #     Сумма показателей "Количества детей в группах для детей с
    #     ограниченными возможностями" в разрезе возрастных
    #     категорий должно равняться сумме "Количества детей
    #      в оздоровительных группах" и
    #     "Количество детей в компенсирующих группах
    #     """
    #
    #     units = Unit.objects.filter(kind__id=4)
    #
    #     with session_scope() as session:
    #         for dou in units:
    #             index = EnrolledIndex(dou, session)
    #             sum_in_disabled_group_age_slice = 0
    #             for age in const.AGE_CATEGORIES_FULL.values():
    #                 sum_in_disabled_group_age_slice += index.get_count(
    #                     age_range=age,
    #                     index_type=EnrolledIndex.COUNT_DISABLED).count()
    #             sum_in_correct_and_health_groups = 0
    #             sum_in_correct_and_health_groups += index.get_count(
    #                 index_type=EnrolledIndex.COUNT_CORRECT).count()
    #             sum_in_correct_and_health_groups += index.get_count(
    #                 index_type=EnrolledIndex.COUNT_HEALTH).count()
    #
    #             self.assertEqual(sum_in_disabled_group_age_slice,
    #                              sum_in_correct_and_health_groups,
    #                              u'Ошибка по организации %s' % dou.name)


class AdvisoryCentrTest(BaseGisdoReportTestCase):
    """
    При наличии филиалов/корпусов (если у всех не заполнено КЦ) данные по нему пусты.
    Если хот бы у одного заполнено advisory_centr fact="1" (данные в сумме),
    То на уровне головного стоит пометка, все цифры суммируются
    """

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(AdvisoryCentrTest, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Департамент образования и науки Тюменской области')

        self.mo = factory_unit.UnitMoFactory(parent=self.region)
        self.raion = factory_unit.UnitMoFactory(parent=self.mo, kind_id=UnitKind.RAION, name='МАДОУ д/с № 100 общий')

        self.dou = factory_unit.UnitDouFactory(parent=self.raion, name='МАДОУ д/с № 100 (корпуса 1, 2) г.Тюмени')
        GisdoUnitFactory(unit=self.dou)

        self.filial = factory_unit.FilialFactory(parent=self.raion, name='МАДОУ д/с № 100 (корпус 3) г.Тюмени')
        GisdoUnitFactory(unit=self.filial)
        factory_unit.FilialDataFactory(head=self.dou, filial=self.filial)

    def test_dou_advisory_centr(self):
        """
        Условие:
            в головной организации указаны данные о наличии КЦ
        advisory_centr fact="1" и заполнены данные
        """
        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)
        self.assertEqual(dou_data.organization['fact'], 0)

        self.dou.ext_unit.counseling_center = True
        self.dou.ext_unit.save()
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)
        self.assertEqual(dou_data.organization['fact'], 1)

    def test_filial_advisory_centr(self):
        """
        Условие:
            в филиале указаны данные о наличии КЦ
        advisory_centr fact="1" и заполнены данные
        """
        report_service = TestReportService(self.region)
        report_service.collect()
        self.filial.ext_unit.counseling_center = True
        self.filial.ext_unit.save()
        dou_data = DouData(self.dou, report_service._report_form)
        self.assertEqual(dou_data.organization['fact'], 1)


class EmptyBuildingsTest(BaseGisdoReportTestCase):
    """Тестирование случаев отсутствия в филиале/головной организации
    учеников/групп.

    Во всех тестах также проверяется соответствие
    organization/num_building и числа переданных buildings.
    """

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(EmptyBuildingsTest, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Татарстан')

        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(parent=self.mo)
        GisdoUnitFactory(unit=self.dou)

        self.filial = factory_unit.FilialFactory(parent=self.mo)
        GisdoUnitFactory(unit=self.filial)
        factory_unit.FilialDataFactory(head=self.dou, filial=self.filial)

        self.child = factory_child.ChildF.create()

    def test_empty_buildings_no_filial_groups(self):
        """
        Условие:
            в головной организации есть дети
            в филиале нет детей (нет групп)

        Отправляемые значения:
            один building(головной)
            значение free_space и показатели 31.x считаются

        Статус "функционирует" можно не проверять
        """
        with mute_signals(signals.post_save):
            self.group = factory_group.FactGroupF(unit=self.dou)
        factory_group.PupilF(grup=self.group, children=self.child)

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 1)
        self.assertEqual(dou_data.organization['num_building'], 1)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)

        total_groups_free_space = 0
        for group in groups:
            self.assertNotEqual(group['free_space'], 0)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_main_groups(self):
        """
        Условие:
            в головной организации нет детей (нет групп)
            в филиале есть дети

        Отправляемые значения:
            один building (филиал)
            значение free_space и показатели 31.x считаются

        статус "функционирует" зданий можно не проверять
        """
        with mute_signals(signals.post_save):
            self.filial_group = factory_group.FactGroupF(unit=self.filial)
        factory_group.PupilF(grup=self.filial_group, children=self.child)

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 1)
        self.assertEqual(dou_data.organization['num_building'], 1)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)

        total_groups_free_space = 0
        for group in groups:
            self.assertNotEqual(group['free_space'], 0)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_main_pupils(self):
        """
        Условие:
            В головной организации нет детей (есть группы)
            в филиале есть дети

        Отправляемые значения:
            два building (филиал и головное)
            значение free_space и показатели 31.x считаются

        статус "функционирует" зданий можно не проверять
        """
        with mute_signals(signals.post_save):
            self.group = factory_group.FactGroupF(unit=self.dou)
            self.filial_group = factory_group.FactGroupF(unit=self.filial)
        factory_group.PupilF(grup=self.filial_group, children=self.child)

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 2)
        self.assertEqual(dou_data.organization['num_building'], 2)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)

        total_groups_free_space = 0
        for group in groups:
            self.assertNotEqual(group['free_space'], 0)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_filial_pupils(self):
        """
        Условие:
            в головной организации есть дети
            в филиале нет детей (есть группы)

        Отправляемые значения:
            два building (филиал и головное)
            значение free_space и показатели 31.x считаются

        статус "функционирует" зданий можно не проверять
        """
        with mute_signals(signals.post_save):
            self.group = factory_group.FactGroupF(unit=self.dou)
            self.filial_group = factory_group.FactGroupF(unit=self.filial)
        factory_group.PupilF(grup=self.group, children=self.child)

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 2)
        self.assertEqual(dou_data.organization['num_building'], 2)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)

        total_groups_free_space = 0
        for group in groups:
            self.assertNotEqual(group['free_space'], 0)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_main_groups_no_filial_pupils_not_func(self):
        """
        Условие:
            в головной организации нет детей (нет групп)
            в филиале нет детей (есть группы)
            головная организация не функционирует

        Отправляемые значения:
            один building (филиал)
            значение free_space и показатели 31.x приравниваем 0

        статус смотрим у головной организации
        """
        with mute_signals(signals.post_save):
            self.filial_group = factory_group.FactGroupF(unit=self.filial)
        self.dou.status = UnitStatus.RECONSTRUCTION

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 1)
        self.assertEqual(dou_data.organization['num_building'], 1)

        self.assertEqual(dou_data.organization['status'], xml_helpers.RECONSTRUCTION)

        total_groups_free_space = 0
        for group in groups:
            self.assertEqual(group['free_space'], 0)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_main_groups_no_filial_pupils_func(self):
        """
        Условие:
            в головной организации нет детей (нет групп)
            в филиале нет детей (есть группы)
            головная организация функционирует

        Отправляемые значения:
            один building (филиал)
            значение free_space и показатели 31.x считаются

        статус передаем "Работает"
        """
        with mute_signals(signals.post_save):
            self.filial_group = factory_group.FactGroupF(unit=self.filial)
        self.dou.status = UnitStatus.NONE

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)
        groups = list(chain(*(building['groups'] for building in buildings)))

        self.assertEqual(len(buildings), 1)
        self.assertEqual(dou_data.organization['num_building'], 1)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)

        total_groups_free_space = 0
        for group in groups:
            self.assertEqual(group['free_space'], self.filial_group.max_count)
            total_groups_free_space += group['free_space']

        enrolled_index = Index(self.dou)
        self.assertEqual(total_groups_free_space, sum(enrolled_index.free_space_in_unit().values()))

    def test_empty_buildings_no_main_groups_no_filial_groups_not_func(self):
        """
        Условие:
            в головной организации нет детей (нет групп)
            в филиале нет детей (нет групп)

        Отправляемые значения:
            building нет

        статус смотрим у головной организации
        если функционирует - передаем "Контингент отсутствует"
        в начале смотрим статус который выставлен
        """
        self.dou.status = UnitStatus.RECONSTRUCTION

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)

        self.assertEqual(len(buildings), 0)
        self.assertEqual(dou_data.organization['num_building'], 0)

        self.assertEqual(dou_data.organization['status'], xml_helpers.RECONSTRUCTION)

    def test_empty_buildings_no_main_groups_no_filial_groups_func(self):
        """
        Условие:
            в головной организации нет детей (нет групп)
            в филиале нет детей (нет групп)

        Отправляемые значения:
            building нет

        статус смотрим у головной организации
        если функционирует - передаем "Работает"
        в начале смотрим статус который выставлен
        """
        self.dou.status = UnitStatus.NONE

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        buildings = list(dou_data.buildings)

        self.assertEqual(len(buildings), 0)
        self.assertEqual(dou_data.organization['num_building'], 0)

        self.assertEqual(dou_data.organization['status'], xml_helpers.WORK)


class UnitsTests(BaseGisdoReportTestCase):
    """Тестирует данные по заполнению информации организаций"""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(UnitsTests, self).setUp()

        self.region = factory_unit.UnitRFactory(name='Татарстан')

        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(parent=self.mo)
        GisdoUnitFactory(unit=self.dou)

        self.filial = factory_unit.FilialFactory(parent=self.mo)
        GisdoUnitFactory(unit=self.filial)
        factory_unit.FilialDataFactory(head=self.dou, filial=self.filial)

        self.child_list = []
        for i in range(0, 2):
            self.child_list.append(factory_child.ChildF.create())

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_units_with_filials(self):
        """
        Условие:
            у головной организации есть филиал.
            Проверить как отображается в отчёте атрибут филиал у
            организации-филиала
        """
        self.group = factory_group.FactGroupF(unit=self.dou)
        self.filial_group = factory_group.FactGroupF(unit=self.filial)
        factory_group.PupilF(grup=self.group, children=self.child_list[0])
        factory_group.PupilF(grup=self.filial_group, children=self.child_list[1])

        report_service = TestReportService(self.region)
        report_service.collect()
        dou_data = DouData(self.dou, report_service._report_form)

        # получение организаций в отчёте
        buildings = list(dou_data.buildings)

        for building in buildings:
            if building['name'] == self.filial.full_name:
                # если организация филиал
                # то у неё должен быть заполнен тег filial 1
                self.assertEquals(building['filial'], 1)
            else:
                # у родительской он должен быть 0
                self.assertEquals(building['filial'], 0)


class XmlMunicipalityTest(BaseXmlResultsTest):
    """Тестирует показатели `municipality` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlMunicipalityTest, self).setUp()

        self.max_doo_region = factory_unit.UnitRFactory(
            max_desired_dou=55,
        )

        self.no_max_doo_region = factory_unit.UnitRFactory()

        self.mo_1 = factory_unit.UnitMoFactory(
            parent=self.max_doo_region,
            max_desired_dou=5,
        )
        GisdoUnitFactory(unit=factory_unit.UnitDouFactory(parent=self.mo_1))

        self.mo_2 = factory_unit.UnitMoFactory(parent=self.max_doo_region)
        GisdoUnitFactory(unit=factory_unit.UnitDouFactory(parent=self.mo_2))

        self.mo_3 = factory_unit.UnitMoFactory(parent=self.no_max_doo_region)
        self.good_dou = factory_unit.UnitDouFactory(parent=self.mo_3)
        self.closed_dou = factory_unit.UnitDouFactory(
            parent=self.mo_3,
            status=UnitStatus.CLOSED,
        )
        self.filial_dou = factory_unit.UnitDouFactory(
            parent=self.mo_3,
            is_filial=FilialType.FILIAL,
        )
        factory_unit.FilialDataFactory(
            head=self.good_dou,
            filial=self.filial_dou,
        )

        GisdoUnitFactory(unit=self.good_dou)
        GisdoUnitFactory(unit=self.closed_dou)
        GisdoUnitFactory(unit=self.filial_dou)

    def test_max_doo(self):
        max_doo_region_form = self.collect_report(self.max_doo_region)
        no_max_doo_region_form = self.collect_report(self.no_max_doo_region)

        test_results_map = {
            # результат из max_desired_dou самого МО
            (self.mo_1, max_doo_region_form): 5,
            # результат из max_desired_dou РЕГИОНА
            (self.mo_2, max_doo_region_form): 55,
            # в МО и РЕГИОНЕ не указан
            # берем по числу ДОО (закрытый ДОО и филиал не попадают)
            (self.mo_3, no_max_doo_region_form): 1,
        }

        for (mo, report_form), max_doo in test_results_map.items():
            root = etree.fromstring(self._get_report_xml_string(mo, report_form))

            xml_max_doo = root.xpath("//*[local-name()='municipality']")[0].get('max_doo')

            self.assertEqual(max_doo, int(xml_max_doo))


class XmlEarlyAssistantTest(BaseXmlResultsTest):
    """Тестирует показатели `organization/early_assistant` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlEarlyAssistantTest, self).setUp()

        self.region = factory_unit.UnitRFactory()
        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Основное',
        )
        self.filial_dou = factory_unit.FilialFactory(
            parent=self.mo,
            name='Филиал',
        )
        self.filial_data = factory_unit.FilialDataFactory(head=self.dou, filial=self.filial_dou)

        GisdoUnitFactory(unit=self.dou)
        GisdoUnitFactory(unit=self.filial_dou)

    def _get_dou_early_assistant(self):
        """Строит XML и возвращает содержимое тега `early_assistant`."""
        region_form = self.collect_report(self.region)
        root = etree.fromstring(self._get_report_xml_string(self.mo, region_form))

        # смотрим только основное ДОО
        return root.xpath(
            "//*[local-name()='organization' and @name='{}']/*[local-name()='early_assistant']".format(self.dou.name)
        )[0]

    def test_fact_attribute(self):
        """Тестирует показатель `fact`."""

        # только 1 атрибут - fact со значением 0
        self.dou.ext_unit.early_help_service = False
        self.dou.ext_unit.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('0', early_assistant.get('fact'))
        self.assertEqual(1, len(early_assistant.attrib))

        # 11 атрибутов включая `fact` со значением 1
        self.dou.ext_unit.early_help_service = True
        self.dou.ext_unit.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('1', early_assistant.get('fact'))
        self.assertEqual(11, len(early_assistant.attrib))

        # только 1 атрибут - fact со значением 0
        self.dou.ext_unit.delete()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('0', early_assistant.get('fact'))
        self.assertEqual(1, len(early_assistant.attrib))

    def test_sum_attribute(self):
        """Тестирует показатель являющийся суммой по ДОО и филиалам.

        На примере `num_hits_personally`, остальные должны считаться аналогично.
        """
        self.dou.ext_unit.early_help_service = True

        # сумма ДОО и подтвержденных филиалов
        self.dou.ext_unit.u_num_hits_personally = 3
        self.dou.ext_unit.save()
        self.filial_dou.ext_unit.u_num_hits_personally = 5
        self.filial_dou.ext_unit.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('8', early_assistant.get('num_hits_personally'))

        # неподтвержденный филиал не считается
        self.filial_data.status = FilialTypeStatus.UNKNOWN
        self.filial_data.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('3', early_assistant.get('num_hits_personally'))

    def test_bool_attribute(self):
        """
        Тестирует показатель имющий True, если он True либо в ДОО либо
        в любом из филиалов, иначе False.

        На примере `forma_2/early_psychological_help`,
        остальные должны считаться аналогично.
        """
        self.dou.ext_unit.early_help_service = True

        # по основному ДОО
        self.dou.ext_unit.early_psychological_help = True
        self.dou.ext_unit.save()
        self.filial_dou.ext_unit.early_psychological_help = False
        self.filial_dou.ext_unit.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('1', early_assistant.get('forma_2'))

        # по подтвержденному филиалу
        self.dou.ext_unit.early_psychological_help = False
        self.dou.ext_unit.save()
        self.filial_dou.ext_unit.early_psychological_help = True
        self.filial_dou.ext_unit.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('1', early_assistant.get('forma_2'))

        # неподтвержденный филиал не считается
        self.filial_data.status = FilialTypeStatus.UNKNOWN
        self.filial_data.save()
        early_assistant = self._get_dou_early_assistant()

        self.assertEqual('0', early_assistant.get('forma_2'))


class XmlCommetStatusTest(BaseXmlResultsTest):
    """Тестирует показатели `commet_status` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlCommetStatusTest, self).setUp()

        self.region = factory_unit.UnitRFactory()
        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Основное',
        )
        GisdoUnitFactory(unit=self.dou)

    def _get_organization(self):
        """Строит XML и возвращает содержимое тега `organization`."""
        region_form = self.collect_report(self.region)
        root = etree.fromstring(self._get_report_xml_string(self.mo, region_form))

        # смотрим только основное ДОО
        return root.xpath("//*[local-name()='organization' and @name='{}']".format(self.dou.name))[0]

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_commet_status_attr_presence(self):
        """Тестирует наличие атрибута `commet_status`."""

        # Должен передаваться (статус в отличный от 1)
        self.dou.status = UnitStatus.RECONSTRUCTION
        self.dou.end_date = datetime.datetime.now()
        self.dou.save()
        organization = self._get_organization()

        self.assertTrue('commet_status' in organization.attrib)

        # Не должен передаваться, т.к. является функционирующим:
        self.dou.status = UnitStatus.NONE
        self.dou.end_date = None
        self.dou.save()
        organization = self._get_organization()

        self.assertTrue('commet_status' not in organization.attrib)

        # Не должен передаваться (статус в информике - 1)
        fact_group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )
        child = factory_child.ChildF.create()
        factory_group.PupilF(grup=fact_group, children=child)

        organization = self._get_organization()

        self.assertTrue('commet_status' not in organization.attrib)


class XmlStatusBuildingTest(BaseXmlResultsTest):
    """Тестирует показатели `status_building` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlStatusBuildingTest, self).setUp()

        self.region = factory_unit.UnitRFactory()
        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Основное',
        )
        self.fact_group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )

        self.filial_dou = factory_unit.FilialFactory(
            parent=self.mo,
            name='Филиал',
        )
        self.filial_data = factory_unit.FilialDataFactory(head=self.dou, filial=self.filial_dou)
        self.filial_fact_group = factory_group.FactGroupF(
            name='Фактическая филиала',
            unit=self.filial_dou,
        )

        GisdoUnitFactory(unit=self.dou)
        GisdoUnitFactory(unit=self.filial_dou)

    def _get_dou_buildings(self):
        """Строит XML и возвращает содержимое тега `status_building`."""
        region_form = self.collect_report(self.region)
        root = etree.fromstring(self._get_report_xml_string(self.mo, region_form))

        return root.xpath("//*[local-name()='building']")

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_status_building(self):
        self.dou.status = UnitStatus.NONE  # рабочий ДОО
        self.dou.save()
        self.filial_dou.status = UnitStatus.RECONSTRUCTION
        self.filial_dou.save()  # нерабочий филиал

        buildings = self._get_dou_buildings()
        dou_building = [b for b in buildings if b.attrib['name'] == self.dou.name][0]
        filial_building = [b for b in buildings if b.attrib['name'] == self.filial_dou.name][0]

        self.assertEqual(dou_building.attrib.get('status_building'), '1')
        self.assertEqual(filial_building.attrib.get('status_building'), '0')

        self.dou.status = UnitStatus.SUSPENDED  # нерабочий ДОО
        self.dou.save()
        self.filial_dou.status = UnitStatus.MISSING_CONTINGENT  # рабочий Филиал
        self.filial_dou.save()

        buildings = self._get_dou_buildings()
        dou_building = [b for b in buildings if b.attrib['name'] == self.dou.name][0]
        filial_building = [b for b in buildings if b.attrib['name'] == self.filial_dou.name][0]

        self.assertEqual(dou_building.attrib.get('status_building'), '0')
        self.assertEqual(filial_building.attrib.get('status_building'), '1')


class XmlActivityTest(BaseXmlResultsTest):
    """Тестирует показатели `group/activity` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlActivityTest, self).setUp()

        self.region = factory_unit.UnitRFactory()
        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Основное',
        )
        self.fact_group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
            type=GroupType.get_by_code(GroupTypeEnumerate.DEV),
        )

        self.filial_dou = factory_unit.FilialFactory(
            parent=self.mo,
            name='Филиал',
        )
        self.filial_data = factory_unit.FilialDataFactory(head=self.dou, filial=self.filial_dou)
        self.filial_fact_group = factory_group.FactGroupF(
            name='Фактическая филиала',
            unit=self.filial_dou,
            type=GroupType.get_by_code(GroupTypeEnumerate.DEV),
        )

        GisdoUnitFactory(unit=self.dou)
        GisdoUnitFactory(unit=self.filial_dou)

    def _get_groups_activities(self):
        """Строит XML и возвращает содержимое тега `activity`."""
        region_form = self.collect_report(self.region)
        root = etree.fromstring(self._get_report_xml_string(self.mo, region_form))

        return root.xpath("//*[local-name()='group']/@activity")

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_status_building(self):
        self.dou.status = UnitStatus.NONE  # рабочий ДОО
        # have_lic == False и нет Факт группы в статусах
        # => organization/license = 2
        self.dou.have_lic = False
        self.dou.group_set.filter(status=GroupStatusEnum.FACT).delete()
        self.dou.save()

        for activity in self._get_groups_activities():
            self.assertEqual(activity, '2')


class XmlPartnerTest(BaseXmlResultsTest):
    """Тестирует показатели `group/partner` итоговой XML."""

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def setUp(self):
        super(XmlPartnerTest, self).setUp()

        self.region = factory_unit.UnitRFactory()
        self.mo = factory_unit.UnitMoFactory(parent=self.region)

        self.dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Основное',
        )

        self.other_dou = factory_unit.UnitDouFactory(
            parent=self.mo,
            name='Другое',
        )

        self.fact_group = factory_group.FactGroupF(
            name='Фактическая',
            unit=self.dou,
        )

        self.filial_dou = factory_unit.FilialFactory(
            parent=self.mo,
            name='Филиал',
        )
        self.filial_data = factory_unit.FilialDataFactory(head=self.dou, filial=self.filial_dou)
        self.filial_fact_group = factory_group.FactGroupF(
            name='Фактическая филиала',
            unit=self.filial_dou,
        )

        GisdoUnitFactory(unit=self.dou)
        GisdoUnitFactory(unit=self.other_dou)
        GisdoUnitFactory(unit=self.filial_dou)

        self.other_dou.gisdo.create_doo_identity()
        self.other_dou.gisdo.save()

    def _get_groups(self):
        """Строит XML и возвращает содержимое тега `partner`."""
        region_form = self.collect_report(self.region)
        root = etree.fromstring(self._get_report_xml_string(self.mo, region_form))

        return root.xpath("//*[local-name()='group']")

    @factory.django.mute_signals(signals.pre_save, signals.post_save)
    def test_status_building(self):
        self.dou.status = UnitStatus.NONE  # рабочий ДОО
        self.dou.have_lic = False
        self.dou.save()

        self.fact_group.edu_unit = self.other_dou
        self.fact_group.save()

        self.filial_fact_group.edu_unit = self.other_dou
        self.filial_fact_group.save()

        for group in self._get_groups():
            self.assertEqual(group.get('partner_group'), '1')
            self.assertEqual(
                group.get('partner'),
                self.other_dou.gisdo.doo_identity,
            )
