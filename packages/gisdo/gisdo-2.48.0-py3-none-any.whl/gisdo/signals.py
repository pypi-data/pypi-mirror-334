from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import (
    receiver,
)

from kinder.core.unit.models import (
    Unit,
)


@receiver(pre_delete, sender=Unit)
def delete_gisdo_unit(instance, **kwargs):
    """Удаляет расширение модели организации."""
    if hasattr(instance, 'gisdo'):
        instance.gisdo.delete()
