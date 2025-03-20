from __future__ import (
    absolute_import,
)

from django.apps import (
    AppConfig,
)


class GisdoConfig(AppConfig):
    name = 'gisdo'
    label = 'gisdo'
    verbose_name = 'фед. отчетность'

    def ready(self):
        from . import (
            signals,
        )
