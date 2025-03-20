from __future__ import (
    annotations,
)

from typing import (
    Any,
)

from .constants import (
    PERM_RELATED_TO_MO,
)


def get_gisdo_unit_pack_perm_dict(ext_result: Any = None) -> dict[str, str]:
    """Возвращает словарь с правами для добавления к EditUnitDictPack

    :param ext_result: Результат выполнения предыдущего
        обработчика точки расширения.

    :return: Словарь с данными формата: {Код права: Наименование права}

    """
    return {PERM_RELATED_TO_MO: 'Поле "Относится к МО"'}
