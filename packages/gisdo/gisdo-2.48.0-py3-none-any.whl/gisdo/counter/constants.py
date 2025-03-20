from kinder.core.dict.models import (
    PrivilegeType,
)
from kinder.core.direct.models import (
    DRS,
)


# Используются в фильтрах, чтоб не создавать по несколько раз
DRS_NEW_CONFIRM = {DRS.NEW, DRS.CONFIRM}
DRS_REGISTER_DOGOVOR = {DRS.REGISTER, DRS.DOGOVOR}
PRIV_TYPE_MUN_REG = {PrivilegeType.MUN, PrivilegeType.REG}
