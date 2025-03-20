# coding:utf-8

import os
from multiprocessing.util import (
    register_after_fork,
)

from django.conf import (
    settings,
)
from kombu import (
    Queue,
)
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.pool import (
    NullPool,
)

from kinder import (
    version as kinder_version,
)
from kinder.config_parser import (
    ProjectConfig,
)


# -------------------------------------------------------
#: Настройки для Системы показателей
# -------------------------------------------------------
DEFAULT_CONFIG = {
    ('gisdo', 'PUSH_DATA_URL'): '',
    ('gisdo', 'PUSH_DATA_TIMEOUT'): 90,
    ('gisdo', 'FEDERAL_DISTRICT'): '',
    ('gisdo', 'GISDO_LOG_FILE'): 'gisdo.log',
    ('gisdo', 'AGE_CALCULATION_DATE'): 0,
    ('gisdo', 'NO_CONSIDER_PRIORITY'): False,
    ('gisdo', 'NO_TEMPORARY_PUPIL'): False,
    ('gisdo', 'CELERY_WORKER_TASK_QUEUE'): 'gisdo',
    ('gisdo', 'USE_MAX_OCCUPANCY'): None,
    ('gisdo', 'RELATED_MO_PORTAL'): True,
}

PROJECT_PATH = os.path.dirname(__file__)
filenames = getattr(settings, 'CONF_FILES', os.path.join(PROJECT_PATH, 'gisdo.conf'))

KINDER_VERSION = kinder_version.VERSION

conf = ProjectConfig(filenames=filenames, defaults=DEFAULT_CONFIG)
#: Адрес веб сервиса системы показателей
GISDO_WS_WSDL = conf.get('gisdo', 'PUSH_DATA_URL')
# таймаут на отправку данных
GISDO_TIMEOUT = conf.get_int('gisdo', 'PUSH_DATA_TIMEOUT')
#: Федеральный субъект, в котором установлена система
FEDERAL_DISTRICT = conf.get('gisdo', 'FEDERAL_DISTRICT')
# Файл с логами для данного приложения
GISDO_LOG_FILE = conf.get('gisdo', 'GISDO_LOG_FILE') or 'gisdo.log'
# Вариант расчета возраста ребенка
AGE_CALCULATION_DATE = conf.get_int('gisdo', 'AGE_CALCULATION_DATE')
# Учитывать ли при расчете приоритет организации.
# С отрицанием из-за того чтобы можно было по-умолчанию
# выставить значение "Учитывать".
NO_CONSIDER_PRIORITY = conf.get_bool('gisdo', 'NO_CONSIDER_PRIORITY')
# Учитывать ли временные зачисления
NO_TEMPORARY_PUPIL = conf.get_bool('gisdo', 'NO_TEMPORARY_PUPIL')
# Очередь celery worker'а
CELERY_WORKER_TASK_QUEUE = conf.get('gisdo', 'CELERY_WORKER_TASK_QUEUE')
# Код региона
REGION_CODE = settings.REGION_CODE
# Если надо переписать код региона в тэге parent_pay
REGION_CODE_FO = conf.get('region', 'REGION_CODE_FO') or ''
# Дублирую из садов.
DOWNLOADS_DIR = settings.DOWNLOADS_DIR
DOWNLOADS_URL = settings.DOWNLOADS_URL
# у плагина нет синхр. реализации, надо включать celery
CELERY_IMPORTS = settings.CELERY_IMPORTS if hasattr(settings, 'CELERY_IMPORTS') else tuple()
CELERY_IMPORTS += ('gisdo.tasks',)

CELERY_QUEUES = settings.CELERY_QUEUES
CELERY_QUEUES.append(Queue(CELERY_WORKER_TASK_QUEUE, routing_key=CELERY_WORKER_TASK_QUEUE))

# Некоторым регионам требуется передавать всегда только максимальную/нормативную
# наполняемость, не зависимо от поля "Использовать макс. наполн."
# в справочнике МО (unit.get_use_fact_norm_cnt()).
USE_MAX_OCCUPANCY = conf.get_bool('gisdo', 'USE_MAX_OCCUPANCY', allow_none=True)

database_engine = settings.DATABASES['default']
database_name = database_engine.get('NAME', '')
database_user = database_engine.get('USER', '')
database_password = database_engine.get('PASSWORD', '')
database_host = database_engine.get('HOST', '')
database_port = database_engine.get('PORT', '') or 5432
notation = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
    database_user,
    database_password,
    database_host,
    database_port,
    database_name,
)
# Пока без пула.
engine = create_engine(
    notation, echo=False, poolclass=NullPool, connect_args={'options': f'-c timezone={settings.TIME_ZONE}'}
)

# https://github.com/celery/celery/issues/1564
register_after_fork(engine, engine.dispose)

# при заполнении поля Относится к МО должен автоматически
# проставляться чек-бокс Не показывать на портале
RELATED_MO_PORTAL = conf.get_bool('gisdo', 'RELATED_MO_PORTAL')
