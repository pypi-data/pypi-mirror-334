import json
from functools import (
    reduce,
)

from future.builtins import (
    object,
)

from gisdo.constants import (
    AGE_CATEGORIES_ALL,
    AGE_CATEGORIES_CUT,
    AGE_CATEGORIES_EIGHT,
    AGE_CATEGORIES_FULL,
    RESET_METRICS,
)
from gisdo.index.constants import (
    APPLICATION_INDEXES,
    CAPACITIES_INDEXES,
    ENROLLED_INDEXES,
    QUEUE_INDEXES,
)
from gisdo.utils import (
    reset_metric_values,
)


class UIProxy(object):
    APPLICATION = 'applications'
    QUEUE = 'queues'
    ENROLLED = 'enrolled'
    CAPACITIES = 'capacities'

    PARTS = {
        APPLICATION: APPLICATION_INDEXES,
        QUEUE: QUEUE_INDEXES,
        ENROLLED: ENROLLED_INDEXES,
        CAPACITIES: CAPACITIES_INDEXES,
    }

    def __init__(self, report_form_rows):
        self._report_form_rows = report_form_rows

    def _get_part(self, report_part):
        parts = []
        for report_form_row in self._report_form_rows:
            parts.append(json.loads(getattr(report_form_row, report_part)))

        def aggregate(left_part, right_part):
            for attribute, value in left_part.items():
                if attribute in right_part:
                    right_value = right_part[attribute]
                    if attribute in RESET_METRICS:
                        # Показатели №8 нельзя посчитать на ходу.
                        # Чтобы не отображалась конкатенация значений в интерфейсе.
                        # Обнуляем значения показателей.
                        reset_metric_values(value, reset_value='-')
                    elif isinstance(value, dict) and isinstance(right_value, dict):
                        left_part[attribute] = aggregate(value, right_value)
                    else:
                        left_part[attribute] = value + right_value
            return left_part

        # Агрегируем данные
        part = reduce(aggregate, parts)

        return part

    @staticmethod
    def _get_index_age_category(part, index_id):
        index = part[index_id]

        for age_class in (AGE_CATEGORIES_CUT, AGE_CATEGORIES_EIGHT, AGE_CATEGORIES_FULL, AGE_CATEGORIES_ALL):
            for age_cat in index:
                if age_cat not in list(age_class.values()):
                    break
            else:
                return age_class

    def _get_ui_part(self, part_name):
        part_ui_data = []
        current_pos = 1
        part = self._get_part(part_name)
        for index_id in self.PARTS[part_name]:
            age_class = UIProxy._get_index_age_category(part, index_id)

            for age_category in age_class:
                count = part[index_id][age_class[age_category]]
                verbose_present = self.PARTS[part_name][index_id]
                try:
                    verbose_present = verbose_present % age_class[age_category]
                except Exception:
                    pass
                part_ui_data.append((current_pos, verbose_present, count))
                current_pos += 1

        return part_ui_data

    def get_ui_data(self):
        applications = self._get_ui_part(self.APPLICATION)
        queues = self._get_ui_part(self.QUEUE)
        enrolled = self._get_ui_part(self.ENROLLED)
        capacities = self._get_ui_part(self.CAPACITIES)

        return (applications, queues, enrolled, capacities)
