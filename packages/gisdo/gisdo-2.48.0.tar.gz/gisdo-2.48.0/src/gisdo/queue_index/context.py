import datetime

from kinder.core.queue_api.context.base import (
    BaseContext,
)


class Context(BaseContext):
    params = ['first_dou_only', 'on_date']

    def __init__(self, unit, on_date=datetime.date.today, first_dou_only=False, select_fields=None):
        self.context_filters = []
        self.unit = self.unit_inst = unit
        self.on_date = on_date
        self.first_dou_only = first_dou_only
        self.select_fields = select_fields
