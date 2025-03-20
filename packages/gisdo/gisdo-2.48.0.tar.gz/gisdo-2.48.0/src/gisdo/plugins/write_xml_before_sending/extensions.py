import os
from datetime import (
    datetime,
)

from .settings import (
    XML_SAVING_DIRECTORY_PATH as PATH,
)


def write_xml(xml, octmo, *args, **kwargs):
    """Сохраняет указанный xml файл в соответствии с настройками"""
    if xml:
        time = str(datetime.now().isoformat(timespec='minutes'))
        with open(os.path.join(PATH, f'Dou_{octmo}_{time}.xml'), 'wb') as f:
            f.write(xml)
