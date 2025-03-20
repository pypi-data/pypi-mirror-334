import datetime
from typing import (
    Any,
)

from freezegun import (
    freeze_time,
)

from kinder.core.children.tests import (
    factory_child,
)
from kinder.core.declaration.enum import (
    DeclPortalEnum,
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
    GroupTypeEnumerate,
    HealthNeed,
    WorkType,
    WorkTypeEnumerate,
)
from kinder.core.direct.tests import (
    factory_direct,
)
from kinder.core.group.tests import (
    factory_group,
)
from kinder.core.unit.tests import (
    factory_unit,
)
from kinder.test.base import (
    BaseTC,
)

from gisdo.counter.base import (
    CounterAll,
    CounterBase,
    CounterFilter,
    CounterFilterN,
    CounterGroup,
    CounterSimple,
    CountGroupSelect,
)
from gisdo.counter.counter import *
from gisdo.counter.provider import (
    DataProvider,
)


# Сами классы абстрактные, поэтому делаем реализации для их проверки
class SimpleCounterTest(CounterSimple):
    """
    Простой счётчик принимает параметр n и срабатывает на числа делимые на n
    """

    def __init__(self, n: int, *label: str) -> None:
        super().__init__(*label)
        self._n = n

    def check(self, value: Any) -> bool:
        return value % self._n == 0


class CountGroupSelectTest(CountGroupSelect):
    """
    Счётчик с выбором выберет счётчик для первого возможного делителя числа
    из 2, 3, 5, 7 если нет то выберет счётчик под ключом 1
    """

    def __init__(self, *label: str) -> None:
        super().__init__(*label)
        self._prime_counters = {
            1: CounterAll('1'),
            2: CounterAll('2'),
            3: CounterAll('3'),
            5: CounterAll('5'),
            7: CounterAll('7'),
        }

        for counter in self._prime_counters.values():
            self.register(counter)

    def get_counter(self, value: Any) -> CounterBase:
        for i in [2, 3, 5, 7]:
            if value % i == 0:
                return self._prime_counters[i]

        return self._prime_counters[1]


class CounterFilterTest(CounterFilter):
    """
    Счётчик фильтр пропускающий только чётные числа
    """

    def filter(self, value: Any) -> bool:
        return value % 2 == 0


class CounterFilterNTest(CounterFilterN):
    """
    Счётчик-фильтр учитывающий переданное значение (N) N // 2 раз
    """

    def get_n(self, value: Any) -> int:
        return value // 2


class CounterTestCase(BaseTC):
    """
    Тесты счётчиков
    """

    def test_counter_simple(self):
        """
        Тест простого счётчика
        """
        counter = SimpleCounterTest(2, 'test')

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(counter.get_count(), {('test',): 5})

    def test_counter_all(self):
        """
        Тест счётчика учитывающего любое значение
        """
        counter = CounterAll('test')

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(counter.get_count(), {('test',): 10})

    def test_counter_group(self):
        """
        Тест группы счётчисков
        """
        counter_2 = SimpleCounterTest(2, '2')
        counter_3 = SimpleCounterTest(3, '3')
        counter_5 = SimpleCounterTest(5, '5')
        counter_all = CounterAll('all')

        counter = CounterGroup('test')
        counter.register(counter_2)
        counter.register(counter_3)
        counter.register(counter_5)
        counter.register(counter_all)

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(
            counter.get_count(), {('test', '2'): 5, ('test', '3'): 4, ('test', '5'): 2, ('test', 'all'): 10}
        )

    def test_counter_group_nested(self):
        """
        Тест вложенных групп счётчиков
        """
        counter_2 = SimpleCounterTest(2, '2')
        counter_3 = SimpleCounterTest(3, '3')
        counter_5 = SimpleCounterTest(5, '5')
        counter_all = CounterAll('all')

        counter_a = CounterGroup('a')
        counter_b = CounterGroup('b')

        counter_a.register(counter_2)
        counter_a.register(counter_3)
        counter_b.register(counter_5)
        counter_b.register(counter_all)

        counter = CounterGroup('test')
        counter.register(counter_a)
        counter.register(counter_b)

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(
            counter.get_count(),
            {('test', 'a', '2'): 5, ('test', 'a', '3'): 4, ('test', 'b', '5'): 2, ('test', 'b', 'all'): 10},
        )

    def test_counter_group_select(self):
        """
        Тест группы счётчиков с выбором
        """
        counter = CountGroupSelectTest('test')

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(
            counter.get_count(),
            {
                ('test', '1'): 1,
                ('test', '2'): 5,
                ('test', '3'): 2,
                ('test', '5'): 1,
                ('test', '7'): 1,
            },
        )

    def test_counter_filter(self):
        """
        Тест счётчика-фильтра
        """
        inner_counter = SimpleCounterTest(3, 'test')
        counter = CounterFilterTest(inner_counter)

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(counter.get_count(), {('test',): 2})

    def test_counter_filter_n(self):
        """
        Тест счётчика-фильтра учитывающего значения несколько раз
        """
        inner_counter = SimpleCounterTest(2, 'test')
        counter = CounterFilterNTest(inner_counter)

        for i in range(10):
            counter.handle(i)

        self.assertDictEqual(counter.get_count(), {('test',): 10})


@freeze_time('2020-09-03')
class CounterAgeTestCase(BaseTC):
    """
    Тесты счётчиков по возрастам детей
    """

    def _spawn_child(self, date_of_birth):
        """
        Создать ребёнка с заявкой
        """
        child = factory_child.ChildF.create(date_of_birth=date_of_birth)

        declaration = factory_declaration.DeclarationF(children=child, mo=self.mo, date=datetime.date(2020, 5, 4))

        factory_declaration.DUnitF(declaration=declaration, unit=self.unit)

    def setUp(self):
        super().setUp()
        self.maxDiff = None

        self.mo = factory_unit.UnitMoFactory()
        self.unit = factory_unit.UnitDouFactory(parent=self.mo)

        # возраст на дату отчёта / на текущее 1.09 / на следующее 1.09
        self._spawn_child(datetime.date(2020, 9, 2))  # 0.01y / -0.01y / 0.99y
        self._spawn_child(datetime.date(2020, 3, 2))  # 0.51y / 0.49y / 1.49y

        self._spawn_child(datetime.date(2019, 9, 2))  # 1.01y / 0.99y / 1.99y
        self._spawn_child(datetime.date(2019, 3, 2))  # 1.51y / 1.49y / 2.49y

        self._spawn_child(datetime.date(2017, 9, 2))  # 3.01y / 2.99y / 3.99y
        self._spawn_child(datetime.date(2017, 3, 2))  # 3.51y / 3.49y / 4.49y

        self._spawn_child(datetime.date(2015, 9, 2))  # 5.01y / 4.99y / 5.99y
        self._spawn_child(datetime.date(2015, 3, 2))  # 5.51y / 5.49y / 6.49y

        self._spawn_child(datetime.date(2013, 9, 2))  # 7.01y / 6.99y / 7.99y
        self._spawn_child(datetime.date(2013, 3, 2))  # 7.51y / 7.49y / 8.49y

        provider = DataProvider(self.unit)
        self.data = list(provider.get_rows())

    def test_age_full(self):
        """
        16 счётчиков на текущую дату
        """
        counter = CounterAgeFull()
        counter.count(self.data)

        self.assertDictEqual(
            counter.get_count(),
            {
                ('2-6-MONTHS',): 1,
                ('0.5-1-YEARS',): 1,
                ('1-1.5-YEARS',): 1,
                ('1.5-2-YEARS',): 1,
                ('2-2.5-YEARS',): 0,
                ('2.5-3-YEARS',): 0,
                ('3-3.5-YEARS',): 1,
                ('3.5-4-YEARS',): 1,
                ('4-4.5-YEARS',): 0,
                ('4.5-5-YEARS',): 0,
                ('5-5.5-YEARS',): 1,
                ('5.5-6-YEARS',): 1,
                ('6-6.5-YEARS',): 0,
                ('6.5-7-YEARS',): 0,
                ('7-7.5-YEARS',): 1,
                ('7.5-99-YEARS',): 1,
            },
        )

    def test_age_half(self):
        """
        8 счётчиков на текущую дату
        """
        counter = CounterAgeHalf()
        counter.count(self.data)

        self.assertDictEqual(
            counter.get_count(),
            {
                ('2-1-YEARS',): 2,
                ('1-2-YEARS',): 2,
                ('2-3-YEARS',): 0,
                ('3-4-YEARS',): 2,
                ('4-5-YEARS',): 0,
                ('5-6-YEARS',): 2,
                ('6-7-YEARS',): 0,
                ('7-7.5-YEARS',): 2,
            },
        )

    def test_age_full_sep(self):
        """
        16 счётчиков на текущее 1.09
        """
        counter = CounterAgeFullSep()
        counter.count(self.data)

        self.assertDictEqual(
            counter.get_count(),
            {
                ('2-6-MONTHS',): 2,
                ('0.5-1-YEARS',): 1,
                ('1-1.5-YEARS',): 1,
                ('1.5-2-YEARS',): 0,
                ('2-2.5-YEARS',): 0,
                ('2.5-3-YEARS',): 1,
                ('3-3.5-YEARS',): 1,
                ('3.5-4-YEARS',): 0,
                ('4-4.5-YEARS',): 0,
                ('4.5-5-YEARS',): 1,
                ('5-5.5-YEARS',): 1,
                ('5.5-6-YEARS',): 0,
                ('6-6.5-YEARS',): 0,
                ('6.5-7-YEARS',): 1,
                ('7-7.5-YEARS',): 1,
                ('7.5-99-YEARS',): 0,
            },
        )

    def test_age_full_next_sep(self):
        """
        16 счётчиков на следующее 1.09
        """
        counter = CounterAgeFullNextSep()
        counter.count(self.data)

        self.assertDictEqual(
            counter.get_count(),
            {
                ('2-6-MONTHS',): 0,
                ('0.5-1-YEARS',): 1,
                ('1-1.5-YEARS',): 1,
                ('1.5-2-YEARS',): 1,
                ('2-2.5-YEARS',): 1,
                ('2.5-3-YEARS',): 0,
                ('3-3.5-YEARS',): 0,
                ('3.5-4-YEARS',): 1,
                ('4-4.5-YEARS',): 1,
                ('4.5-5-YEARS',): 0,
                ('5-5.5-YEARS',): 0,
                ('5.5-6-YEARS',): 1,
                ('6-6.5-YEARS',): 1,
                ('6.5-7-YEARS',): 0,
                ('7-7.5-YEARS',): 0,
                ('7.5-99-YEARS',): 2,
            },
        )


@freeze_time('2020-09-03')
class CounterFilterTestCase(BaseTC):
    """
    Тесты счётчиков для отдельных показателей
    """

    def _create_child(self, **params):
        """
        Создать ребёнка
        """
        return factory_child.ChildF.create(**params)

    def _create_declaration(self, child, **params):
        """
        Создать заявку для ребёнка
        """
        declaration = factory_declaration.DeclarationF.create(children=child, **params)
        factory_declaration.DUnitF(declaration=declaration, unit=self.unit_0)

        return declaration

    def _use_counter(self, counter):
        """
        Использовать счётчик и получить результат подсчёта
        """
        provider = DataProvider(self.unit_0)
        data = list(provider.get_rows())

        counter.count(data)
        return counter.get_count()

    def setUp(self):
        super().setUp()
        self.maxDiff = None

        self.mo = factory_unit.UnitMoFactory()
        self.unit_0 = factory_unit.UnitDouFactory(parent=self.mo)
        self.unit_1 = factory_unit.UnitDouFactory(parent=self.mo)

        self.group_0 = factory_group.FactGroupF(unit=self.unit_0)
        self.group_1 = factory_group.FactGroupF(unit=self.unit_1)

    def test_counter_1(self):
        """
        Тест счётчика для показателя 1
        """
        self._create_declaration(self._create_child(), portal=DeclPortalEnum.SYSTEM, date=datetime.date(2020, 1, 1))

        self._create_declaration(self._create_child(), portal=DeclPortalEnum.PORTAL, date=datetime.date(2020, 1, 1))

        self._create_declaration(self._create_child(), portal=DeclPortalEnum.PORTAL, date=datetime.date(2019, 12, 31))

        counter = Counter_1('test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 2})

    def test_counter_2_1(self):
        """
        Тест счётчика для показателя 2.1
        """
        self._create_declaration(self._create_child(), portal=DeclPortalEnum.SYSTEM, date=datetime.date(2020, 1, 1))

        self._create_declaration(self._create_child(), portal=DeclPortalEnum.PORTAL, date=datetime.date(2020, 1, 1))

        counter = Counter_2_1(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})

    def test_counter_3_1(self):
        """
        Тест счётчика для показателя 3.1
        """
        self._create_declaration(self._create_child(), portal=DeclPortalEnum.SYSTEM, date=datetime.date(2020, 1, 1))

        self._create_declaration(self._create_child(), portal=DeclPortalEnum.PORTAL, date=datetime.date(2020, 1, 1))

        counter = Counter_3_1(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})

    def test_counter_4(self):
        """
        Тест счётчика для показателя 4
        """
        status_registered = DeclarationStatus.objects.get(code=DSS.REGISTERED)
        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 9, 1),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 8, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        counter = Counter_4(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})

    def test_counter_4_1(self):
        """
        Тест счётчика для показателя 4.1
        """
        status_registered = DeclarationStatus.objects.get(code=DSS.REGISTERED)
        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(
                health_need=HealthNeed.objects.filter(group_type__code=GroupTypeEnumerate.COMP).first(),
            ),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 9, 1),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 8, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        counter = Counter_4_1(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})

    def test_counter_4_2(self):
        """
        Тест счётчика для показателя 4.2
        """
        status_registered = DeclarationStatus.objects.get(code=DSS.REGISTERED)
        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(
                health_need=HealthNeed.objects.filter(group_type__code=GroupTypeEnumerate.HEALTH).first(),
            ),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 9, 1),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 8, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        counter = Counter_4_2(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})

    def test_counter_5(self):
        """
        Тест счётчика для показателя 5
        """
        status_registered = DeclarationStatus.objects.get(code=DSS.REGISTERED)
        status_want_change_dou = DeclarationStatus.objects.get(code=DSS.WANT_CHANGE_DOU)
        status_priv_confirmating = DeclarationStatus.objects.get(code=DSS.PRIV_CONFIRMATING)

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        c0 = self._create_child()
        c1 = self._create_child()

        factory_group.PupilF(children=c0)
        factory_group.PupilF(children=c1)

        d0 = self._create_declaration(
            c0, status=status_registered, date=datetime.date(2020, 9, 1), desired_date=datetime.date(2021, 8, 30)
        )

        factory_direct.DirectFactory(group=self.group_0, declaration=d0)

        self._create_declaration(
            c1, status=status_priv_confirmating, date=datetime.date(2020, 9, 1), desired_date=datetime.date(2021, 8, 30)
        )

        self._create_declaration(
            self._create_child(),
            status=status_want_change_dou,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 9, 1),
            desired_date=datetime.date(2021, 9, 1),
        )

        self._create_declaration(
            self._create_child(),
            status=status_registered,
            date=datetime.date(2020, 8, 1),
            desired_date=datetime.date(2021, 8, 30),
        )

        counter = Counter_5(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 3})

    def test_counter_6(self):
        """
        Тест счётчика показателя 6
        """
        self._create_declaration(self._create_child(), date=datetime.date(2020, 1, 1))

        self._create_declaration(
            self._create_child(),
            work_type=WorkType.objects.get(code=WorkTypeEnumerate.SHORT),
            date=datetime.date(2020, 1, 1),
        )

        counter = Counter_6(CounterAll(), 'test')

        self.assertDictEqual(self._use_counter(counter), {('test',): 1})
