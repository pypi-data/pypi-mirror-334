from future.builtins import (
    object,
)

from kinder.core.dict.models import (
    GroupTypeEnumerate,
)

from gisdo.algorithm.constants import (
    get_short_day_types,
)


class CommonCountAlgorithm(object):
    def get_result_set(self, cache):
        return cache


class ShortStayAlgorithm(object):
    def get_result_set(self, cache):
        result_set = []

        for group in cache:
            if group.work_type and (group.work_type.code in get_short_day_types()):
                result_set.append(group)

        return result_set


class HealthNeedAlgorithm(object):
    @staticmethod
    def _filter(group):
        return group.type and group.type.code in [GroupTypeEnumerate.COMBI, GroupTypeEnumerate.COMP]

    def get_result_set(self, cache):
        result_set = []

        for group in cache:
            # (#85387) Считать, как количество всех детей
            # зачисленных в группы типа "Оздоровительные"
            # или "Компенсирующие" без учета наличия
            # или отсутствия потребности по здоровью.
            if self._filter(group):
                result_set.append(group)

        return result_set


class CompensatingAlgorithm(HealthNeedAlgorithm):
    @staticmethod
    def _filter(group):
        return group.type and group.type.code == GroupTypeEnumerate.COMP


class HealthGroupAlgorithm(HealthNeedAlgorithm):
    @staticmethod
    def _filter(group):
        return group.type and group.type.code == GroupTypeEnumerate.HEALTH
