import datetime

from gisdo.constants import (
    AGE_CATEGORIES_EIGHT,
    AGE_CATEGORIES_FULL,
)
from gisdo.utils import (
    AgeDeltas,
)


def get_age_full_label(date_of_birth: datetime.date, on_date: datetime.date) -> str:
    """
    Получить метку возраста при разделении на 16 категорий из даты рождения
    """
    for label in (
        '2-6-MONTHS',
        '0.5-1-YEARS',
        '1-1.5-YEARS',
        '1.5-2-YEARS',
        '2-2.5-YEARS',
        '2.5-3-YEARS',
        '3-3.5-YEARS',
        '3.5-4-YEARS',
        '4-4.5-YEARS',
        '4.5-5-YEARS',
        '5-5.5-YEARS',
        '5.5-6-YEARS',
        '6-6.5-YEARS',
        '6.5-7-YEARS',
        '7-7.5-YEARS',
    ):
        cat = AGE_CATEGORIES_FULL[label]
        down, up = AgeDeltas.get_category_deltas(cat, on_date)
        if label == '2-6-MONTHS' and down < date_of_birth:
            return label
        elif down < date_of_birth <= up:
            return label

    return '7.5-99-YEARS'


def get_age_half_label(date_of_birth: datetime.date, on_date: datetime.date) -> str:
    """
    Получить метку возраста при разделении на 8 категорий из даты рождения
    """
    for label in (
        '2-1-YEARS',
        '1-2-YEARS',
        '2-3-YEARS',
        '3-4-YEARS',
        '4-5-YEARS',
        '5-6-YEARS',
        '6-7-YEARS',
    ):
        cat = AGE_CATEGORIES_EIGHT[label]
        down, up = AgeDeltas.get_category_deltas(cat, on_date)
        if down < date_of_birth <= up:
            return label

    return '7-7.5-YEARS'
