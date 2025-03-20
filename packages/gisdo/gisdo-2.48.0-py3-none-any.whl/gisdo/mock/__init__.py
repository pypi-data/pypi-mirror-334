# coding=utf-8

import os
from distutils.dir_util import (
    copy_tree,
    mkpath,
)


def create_mock_server(path):
    """Создания Mock-сервера для приёма федеральной отчётности
    по указанному пути."""

    # Копируем исходники
    copy_tree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'), path)

    # Создаём папку для хранения отчётов
    mkpath(os.path.join(path, 'xml', '3'))
