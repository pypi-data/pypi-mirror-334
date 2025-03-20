from typing import (
    Dict,
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
from gisdo.counter.declaration import (
    ChildrenRow,
)

from . import (
    filters,
)


class CounterAgeFull(CountGroupSelect[ChildrenRow]):
    """
    Разделяет счётчик на 16 счётчиков по возрастным категориям
    """

    def __init__(self, *label: str) -> None:
        super().__init__(*label)
        self._counters_idx: Dict[str, CounterBase] = {
            '2-6-MONTHS': CounterAll('2-6-MONTHS'),
            '0.5-1-YEARS': CounterAll('0.5-1-YEARS'),
            '1-1.5-YEARS': CounterAll('1-1.5-YEARS'),
            '1.5-2-YEARS': CounterAll('1.5-2-YEARS'),
            '2-2.5-YEARS': CounterAll('2-2.5-YEARS'),
            '2.5-3-YEARS': CounterAll('2.5-3-YEARS'),
            '3-3.5-YEARS': CounterAll('3-3.5-YEARS'),
            '3.5-4-YEARS': CounterAll('3.5-4-YEARS'),
            '4-4.5-YEARS': CounterAll('4-4.5-YEARS'),
            '4.5-5-YEARS': CounterAll('4.5-5-YEARS'),
            '5-5.5-YEARS': CounterAll('5-5.5-YEARS'),
            '5.5-6-YEARS': CounterAll('5.5-6-YEARS'),
            '6-6.5-YEARS': CounterAll('6-6.5-YEARS'),
            '6.5-7-YEARS': CounterAll('6.5-7-YEARS'),
            '7-7.5-YEARS': CounterAll('7-7.5-YEARS'),
            '7.5-99-YEARS': CounterAll('7.5-99-YEARS'),
        }

        for counter in self._counters_idx.values():
            self.register(counter)

    def get_counter(self, value: ChildrenRow) -> CounterBase:
        return self._counters_idx[value.age_full]


class CounterAgeHalf(CountGroupSelect[ChildrenRow]):
    """
    Разделяет счётчик на 8 счётчиков по возрастным категориям
    """

    def __init__(self, *label: str) -> None:
        super().__init__(*label)
        self._counters_idx: Dict[str, CounterBase] = {
            '2-1-YEARS': CounterAll('2-1-YEARS'),
            '1-2-YEARS': CounterAll('1-2-YEARS'),
            '2-3-YEARS': CounterAll('2-3-YEARS'),
            '3-4-YEARS': CounterAll('3-4-YEARS'),
            '4-5-YEARS': CounterAll('4-5-YEARS'),
            '5-6-YEARS': CounterAll('5-6-YEARS'),
            '6-7-YEARS': CounterAll('6-7-YEARS'),
            '7-7.5-YEARS': CounterAll('7-7.5-YEARS'),
        }

        for counter in self._counters_idx.values():
            self.register(counter)

    def get_counter(self, value: ChildrenRow) -> CounterBase:
        return self._counters_idx[value.age_half]


class CounterAgeFullSep(CounterAgeFull):
    """
    CounterAgeFull, но считает возраст на первое сентября текущего года
    """

    def get_counter(self, value: ChildrenRow) -> CounterBase:
        return self._counters_idx[value.age_full_sep]


class CounterAgeFullNextSep(CounterAgeFull):
    """
    CounterAgeFull, но считает возраст на первое сентября следующего года
    """

    def get_counter(self, value: ChildrenRow) -> CounterBase:
        return self._counters_idx[value.age_full_next_sep]


# Счётчики соответствующие показателям


class Counter_1(CounterSimple[ChildrenRow]):
    """
    Счётчик для показателя 1
    """

    def check(self, value: ChildrenRow) -> bool:
        return filters.filter_1(value) > 0


class Counter_1_1(CounterFilterN[ChildrenRow]):
    """
    Счётчик для показателя 1.1
    """

    def get_n(self, value: ChildrenRow) -> int:
        return filters.filter_1(value)


class Counter_2_1(CounterFilterN[ChildrenRow]):
    """
    Счётчик для показателя 2.1
    """

    def get_n(self, value: ChildrenRow) -> int:
        return filters.filter_2(value)


class Counter_3_1(CounterFilterN[ChildrenRow]):
    """
    Счётчик для показателя 3.1
    """

    def get_n(self, value: ChildrenRow) -> int:
        return filters.filter_3(value)


class Counter_4(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 4
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_4(value)


class Counter_4_1(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 4.1
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_4_1(value)


class Counter_4_2(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 4.2
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_4_2(value)


class Counter_5(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 5
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_5(value)


class Counter_6(CounterFilterN[ChildrenRow]):
    """
    Счётчик для показателя 6
    """

    def get_n(self, value: ChildrenRow) -> int:
        return filters.filter_6(value)


class Counter_7(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7(value)


class Counter_7_2(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7.2
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7_2(value)


class Counter_7_3(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7.3
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7_3(value)


class Counter_7_4(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7.4
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7_4(value)


class Counter_7_5(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7.5
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7_5(value)


class Counter_7_7(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 7.7
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_7_7(value)


class Counter_9(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 9
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_9(value)


class Counter_10(CounterSimple[ChildrenRow]):
    """
    Счётчик для показателя 10
    """

    def check(self, value: ChildrenRow) -> bool:
        return filters.filter_10(value)


class Counter_10_1(CounterFilter[ChildrenRow]):
    """
    Счётчик для показателя 10.1
    """

    def filter(self, value: ChildrenRow) -> bool:
        return filters.filter_10_1(value)


class Counter_11(CounterSimple[ChildrenRow]):
    """
    Счётчик для показателя 11
    """

    def check(self, value: ChildrenRow) -> bool:
        return filters.filter_11(value)


def get_main_counter() -> CounterBase[ChildrenRow]:
    """
    Основной счётчик для ФО
    """
    main = CounterGroup()

    main.register(Counter_1('1'))
    main.register(Counter_1_1(CounterAgeFull(), '1.1'))
    main.register(Counter_2_1(CounterAgeFull(), '2.1'))
    main.register(Counter_3_1(CounterAgeFull(), '3.1'))
    main.register(Counter_4(CounterAgeFull(), '4'))
    main.register(Counter_4_1(CounterAgeFull(), '4.1'))
    main.register(Counter_4_2(CounterAgeFull(), '4.2'))
    main.register(Counter_5(CounterAgeFull(), '5'))
    main.register(Counter_6(CounterAgeFull(), '6'))
    # main.register(Counter_7(CounterAgeFullSep(), '7'))
    # # 7.1 то же что и 7, но с другой датой для расчёта возраста
    # main.register(Counter_7(CounterAgeFull(), '7.1'))
    # main.register(Counter_7_2(CounterAgeFull(), '7.2'))
    # main.register(Counter_7_3(CounterAgeFull(), '7.3'))
    # main.register(Counter_7_4(CounterAgeFull(), '7.4'))
    # main.register(Counter_7_5(CounterAgeFull(), '7.5'))
    # # 7.6 то же что и 7.5, но с другой датой для расчёта возраста
    # main.register(Counter_7_5(CounterAgeFullNextSep(), '7.6'))
    # main.register(Counter_7_7(CounterAgeFull(), '7.7'))
    # # Показатель 8.х не считается тут
    # main.register(Counter_9(CounterAgeFullSep(), '9'))
    # # 9.1 то же что и 9, но с другой датой для расчёта возраста
    # main.register(Counter_9(CounterAgeFull(), '9.1'))
    # main.register(Counter_10('10'))
    # # TODO: написано что на 1 сентября след года, но в оригинале считает на текущую дату
    # main.register(Counter_10_1(CounterAgeFull(), '10.1'))
    # main.register(Counter_11('11'))

    return main
