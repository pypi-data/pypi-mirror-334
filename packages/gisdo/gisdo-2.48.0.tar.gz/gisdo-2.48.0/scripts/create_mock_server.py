#!/usr/bin/env python
# coding=utf-8
"""
Скрипт для создания Mock-сервера для приёма федеральной отчётности

Использование:


1. Выполнить create_mock_server <path>
2. Перейти в папку где был создан сервер
3. Создать новое виртуальное окружение
4. Выполнить pip install -r requirements.txt
5. Отредактировать файл settings.py
6. Запустить сервер командой python server.py
"""

import argparse

from gisdo.mock import (
    create_mock_server,
)


def main():
    parser = argparse.ArgumentParser(description='Создание mock-сервера для принятия федеральной отчётности')

    parser.add_argument('path', help='Путь для создания сервера')
    args = parser.parse_args()

    create_mock_server(args.path)


if __name__ == '__main__':
    main()
