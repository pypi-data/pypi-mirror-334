from abc import (
    ABCMeta,
    abstractmethod,
)

from future.builtins import (
    object,
)
from future.utils import (
    with_metaclass,
)

from m3.actions.exceptions import (
    ApplicationLogicException,
)


class BaseIndex(with_metaclass(ABCMeta, object)):
    """
    Базовый класс для показателей
    """

    def __init__(self, unit, session=None):
        self.unit = unit
        self.unit.unit_mo_id = self.unit_mo_id = unit.get_mo().id
        self.dou_type = unit.dou_type

        self.session = session

    @classmethod
    def get_algorithm(cls, index_type):
        try:
            clazz = cls.ALGORITHM_MAP[index_type]
        except KeyError:
            raise ApplicationLogicException('Такой показатель не реализован')

        return clazz

    @abstractmethod
    def get_count(self, **kwargs):
        raise NotImplementedError
