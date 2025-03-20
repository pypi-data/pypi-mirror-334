from functools import (
    lru_cache,
)
from itertools import (
    chain,
)

from kinder.core.dict.models import (
    HealthNeed,
    HealthNeedEnumerate as HNE,
)

from gisdo.algorithm.constants import (
    HealthNeedEnumsCollectorMap,
)


@lru_cache(maxsize=2)
def get_has_health_need_codes():
    """Возвращает все коды значений справочника кроме 'нет'"""
    return set(HealthNeed.objects.exclude(code=HNE.NOT).values_list('code', flat=True))


class HealthNeedIdsProvider(object):
    """Возвращает id справочника Ограниченные возможности здоровья по показателям"""

    values_map = HealthNeedEnumsCollectorMap

    @classmethod
    def get_health_need_22_1(cls):
        """Возвращает id справочников для показателя 22.1"""
        return cls.values_map.health_need_22_1

    @classmethod
    def get_health_need_22_1_1(cls):
        """Возвращает id справочников для показателя 22.1.1"""
        return cls.values_map.health_need_22_1_1

    @classmethod
    def get_health_need_22_1_2(cls):
        """Возвращает id справочников для показателя 22.1.2"""
        return cls.values_map.health_need_22_1_2

    @classmethod
    def get_health_need_22_2(cls):
        """Возвращает id справочников для показателя 22.2"""
        return cls.values_map.health_need_22_2

    @classmethod
    def get_health_need_22_3(cls):
        """Возвращает id справочников для показателя 22.3"""
        return cls.values_map.health_need_22_3

    @classmethod
    def get_health_need_22_3_1(cls):
        """Возвращает id справочников для показателя 22.3.1"""
        return cls.values_map.health_need_22_3_1

    @classmethod
    def get_health_need_22_3_2(cls):
        """Возвращает id справочников для показателя 22.3.2"""
        return cls.values_map.health_need_22_3_2

    @classmethod
    def get_health_need_22_4(cls):
        """Возвращает id справочников для показателя 22.4"""
        return cls.values_map.health_need_22_4

    @classmethod
    def get_health_need_22_5_1(cls):
        """Возвращает id справочников для показателя 22.5.1"""
        return cls.values_map.health_need_22_5_1

    @classmethod
    def get_health_need_22_5_2(cls):
        """Возвращает id справочников для показателя 22.5.2"""
        return cls.values_map.health_need_22_5_2

    @classmethod
    def get_health_need_22_6(cls):
        """Возвращает id справочников для показателя 22.6"""
        return cls.values_map.health_need_22_6

    @classmethod
    def get_health_need_22_7(cls):
        """Возвращает id справочников для показателя 22.7"""
        return cls.values_map.health_need_22_7

    @classmethod
    def get_health_need_22_8_2(cls):
        """Возвращает id справочников для показателя 22.8.2"""
        return cls.values_map.health_need_22_8_2

    @classmethod
    def get_health_need(cls, index_name):
        """Получение id справочников для показателей."""
        health_need_map = {
            '22.1': cls.get_health_need_22_1,
            '22.1.1': cls.get_health_need_22_1_1,
            '22.1.2': cls.get_health_need_22_1_2,
            '22.2': cls.get_health_need_22_2,
            '22.3': cls.get_health_need_22_3,
            '22.3.1': cls.get_health_need_22_3_1,
            '22.3.2': cls.get_health_need_22_3_2,
            '22.4': cls.get_health_need_22_4,
            '22.5.1': cls.get_health_need_22_5_1,
            '22.5.2': cls.get_health_need_22_5_2,
            '22.6': cls.get_health_need_22_6,
            '22.7': cls.get_health_need_22_7,
            '22.8.1': cls.get_health_need_22_8_1,
            '22.8.2': cls.get_health_need_22_8_2,
        }
        if index_name not in health_need_map:
            raise KeyError(f'Указан неверный индекс для поиска ({index_name}')
        return health_need_map[index_name]()

    @classmethod
    def get_not_health_need(cls):
        """Возвращает id справочников для значения без ограничений здоровья"""
        return cls.values_map.not_health_need

    @classmethod
    def get_health_need_22_x(cls):
        """Возвращает id справочника для показателей 22.x"""
        return list(
            chain.from_iterable(
                [
                    cls.get_health_need_22_1(),
                    cls.get_health_need_22_2(),
                    cls.get_health_need_22_3(),
                    cls.get_health_need_22_4(),
                    cls.get_health_need_22_5_1(),
                    cls.get_health_need_22_5_2(),
                    cls.get_health_need_22_6(),
                    cls.get_health_need_22_7(),
                    cls.get_health_need_22_8_2(),
                    cls.get_not_health_need(),
                ]
            )
        )

    @classmethod
    def get_health_need_22_8_1(cls):
        """Возвращает id справочников для показателя 22.8.1"""
        return tuple(set(get_has_health_need_codes()) - set(cls.get_health_need_22_x()))
