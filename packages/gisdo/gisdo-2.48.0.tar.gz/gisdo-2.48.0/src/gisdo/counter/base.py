import abc
from collections import (
    defaultdict,
)
from typing import (
    Dict,
    Generic,
    Iterable,
    List,
    Tuple,
    TypeVar,
)


T = TypeVar('T')


class CounterBase(Generic[T], metaclass=abc.ABCMeta):
    """
    Базовый счётчик

    При обработке значений может менять собственное состояние в методе handle
    При вызове get_count должен вернуть состояние в виде словаря
    {
        (<метка>, ...): результат подсчёта
    }

    Словарь нужен чтобы результаты работы счётчика можно было
    объединять с другими счётчиками
    """

    @abc.abstractmethod
    def handle(self, value: T) -> None:
        """
        Обработать объект и инкрементировать счётчик если нужно
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_count(self) -> Dict[Tuple[str, ...], int]:
        """
        Текущий результат подсчёта
        """
        raise NotImplementedError

    def count(self, iter: Iterable[T]) -> Dict[Tuple[str, ...], int]:
        """
        Посчитать все объекты в переданном итераторе
        """
        for row in iter:
            self.handle(row)

        return self.get_count()


class CounterSimple(CounterBase[T], metaclass=abc.ABCMeta):
    """
    Простой счётчик с проверкой значения
    """

    def __init__(self, *label: str) -> None:
        # Метка по которой можно будет найти результат счётчика
        self._label: Tuple[str, ...] = label
        # Счётчик
        self._count: int = 0

    @abc.abstractmethod
    def check(self, value: T) -> bool:
        """
        Проверить стоит ли учитывать переданное значение
        """
        raise NotImplementedError

    def handle(self, value: T) -> None:
        use = self.check(value)
        if use:
            self._count += 1

    def get_count(self) -> Dict[Tuple[str, ...], int]:
        return {self._label: self._count}


class CounterAll(CounterSimple[T]):
    """
    Простой счётчик которые учитывает любое переданное значение
    """

    def check(self, value: T) -> bool:
        return True


class CounterGroup(CounterBase[T]):
    """
    Группа счётчиков, компонует несколько счётчиков в один
    """

    def __init__(self, *label: str) -> None:
        self._counters: List[CounterBase[T]] = []
        # Дополнительный префикс к меткам счётчиков входящих в данный
        self._label: Tuple[str, ...] = label

    def register(self, counter: CounterBase[T]) -> None:
        """
        Зарегестрировать счётчик
        """
        self._counters.append(counter)

    def handle(self, value: T) -> None:
        for counter in self._counters:
            counter.handle(value)

    def get_count(self) -> Dict[Tuple[str, ...], int]:
        result = defaultdict(int)
        for counter in self._counters:
            local_cnt = counter.get_count()
            for local_label, count in local_cnt.items():
                result[(*self._label, *local_label)] += count

        return result


class CountGroupSelect(CounterGroup[T], metaclass=abc.ABCMeta):
    """
    Группы счётчиков с возможностью выбирать какой
    счётчик использовать для переданного значения

    Как правило в этом случае в качестве внутренних счётчиков
    следует использовать CounterAll

    Отличается от группы счётчиков тем что в случае с группой
    счётчиков будет вызван каждый внутренний счётчик,
    а тут будет вызван только один из них
    """

    @abc.abstractmethod
    def get_counter(self, value: T) -> CounterBase[T]:
        """
        Возвращает счётчик используемый для переданного значения
        """
        raise NotImplementedError

    def handle(self, value: T) -> None:
        counter = self.get_counter(value)
        counter.handle(value)


class CounterFilterBase(CounterBase[T]):
    """
    Базовый класс для счётчика фильтра

    Сначала проверяет что значение проходит
    по фильтру и потом передаёт его в счётчик

    Нужен чтобы заранее отсечь значение перед передачей его в группу счётчиков
    """

    def __init__(self, dest: CounterBase[T], *label: str) -> None:
        # Дополнительный префикс к метке базового счётчика
        self._label: Tuple[str, ...] = label
        # Базовый счётчик для передачи в него значений
        self._dest: CounterBase[T] = dest

    def get_count(self) -> Dict[Tuple[str, ...], int]:
        count = self._dest.get_count()
        return {(*self._label, *label): cnt for label, cnt in count.items()}


class CounterFilter(CounterFilterBase[T]):
    """
    Счётчик фильтр, учитывает значения 1 раз
    """

    @abc.abstractmethod
    def filter(self, value: T) -> bool:
        """
        Фильтрация значений
        """
        raise NotImplementedError

    def handle(self, value: T) -> bool:
        use = self.filter(value)
        if use:
            self._dest.handle(value)


class CounterFilterN(CounterFilterBase[T]):
    """
    Счётчик фильтр, учитывает значения N раз
    """

    @abc.abstractmethod
    def get_n(self, value: T) -> int:
        """
        Получить сколько раз учесть одно значение в счётчике
        """
        raise NotImplementedError

    def handle(self, value: T) -> bool:
        n = self.get_n(value)
        # Просто скармливаем одно и то же значение N раз
        # чтобы не терять совместимости с счётчиками, которое могут
        # учитывать значение лишь единожды за вызов handle
        for _ in range(n):
            self._dest.handle(value)
