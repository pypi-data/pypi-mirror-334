from __future__ import (
    print_function,
)

import logging

from django.core.management.base import (
    BaseCommand,
)

from m3.actions import (
    ApplicationLogicException,
)

from kinder.core.unit.models import (
    Unit,
    UnitKind,
)

from gisdo.models import (
    GisdoUnit,
)


log = logging.getLogger('gisdo')


class Command(BaseCommand):
    """Создает, если нет организаций гисдо, создает идентификатор"""

    def handle(self, *args, **kwargs):
        unsynchronized_units = Unit.objects.filter(gisdo__isnull=True)

        for unit in unsynchronized_units:
            g_unit = GisdoUnit(unit=unit)

            try:
                g_unit.create_doo_identity()
            except ApplicationLogicException as e:
                log.info(e.exception_message)
                print('Не удалось синхронизировать организацию: %s' % unit.name)
                continue

            g_unit.save()

        emty_code_units = Unit.objects.filter(gisdo__doo_identity__isnull=True, kind_id=UnitKind.DOU)
        for unit in emty_code_units:
            try:
                unit.gisdo.create_doo_identity()
            except ApplicationLogicException as e:
                log.info(e.exception_message)
                print('Не удалось создать doo_identity организацию: %s' % unit.name)
                continue
            unit.gisdo.save()
