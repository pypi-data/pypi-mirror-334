from django.conf import (
    settings,
)
from django.core.exceptions import (
    ImproperlyConfigured,
)


def get_param(section, name, default):
    result = str(settings.CONF.get(section, name))
    return result or default


# Директория, предназначенная для хранения xml отчетов
XML_SAVING_DIRECTORY_PATH = get_param('gisdo', 'XML_SAVING_DIRECTORY_PATH', None)


if XML_SAVING_DIRECTORY_PATH is None:
    raise ImproperlyConfigured('Укажите путь до директории, предназначенной для хранения xml отчетов')
