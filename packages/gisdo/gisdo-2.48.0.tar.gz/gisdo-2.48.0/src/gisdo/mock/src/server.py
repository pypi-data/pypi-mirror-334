# coding=utf-8

import base64
import logging
import os
import re
import traceback
from collections import (
    namedtuple,
)
from datetime import (
    datetime,
)
from uuid import (
    uuid4,
)

from bottle import (
    Bottle,
    jinja2_view,
    request,
    response,
    run,
    static_file,
)
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from lxml import (
    etree,
)


app = application = Bottle()
# Константы с путями до статики
XML_PATH = os.path.join('.', 'xml', '3')
SCHEMA_PATH = os.path.join('.', 'schema', '3')
STATIC_PATH = os.path.join('.', 'static')
LOG_PATH = os.path.join('.', 'log')


# Старые отчёты
OldReport = namedtuple('Report', ['filename', 'report_date', 'pretty_date'])


if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

logger = logging.getLogger('gisdo_mock')

logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(LOG_PATH, 'mock_errors.log'))
formatter = logging.Formatter('[%(asctime)s] %(message)s')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def update_schema_xml(wsdl_host, wsdl_port):
    """Рендерит файлы схемы согласно параметрам сервера."""
    env = Environment(loader=FileSystemLoader(SCHEMA_PATH))
    push_data_template = env.get_template('pushData.xml.template')
    push_data_in_template = env.get_template('pushDataIn.xml.template')

    with open(os.path.join(SCHEMA_PATH, 'pushData.xml'), 'wb') as f:
        f.write(push_data_template.render(host=wsdl_host, port=wsdl_port).encode())

    with open(os.path.join(SCHEMA_PATH, 'pushDataIn.xml'), 'wb') as f:
        f.write(push_data_in_template.render().encode())


class Report(object):
    """Класс для работы с отчётами."""

    # Формат даты в названии
    datetime_format = '%Y-%m-%d_%H:%M:%S'
    # Шаблон названия
    template = 'gisdo-3_0-{date}-{id}.xml'
    # Регулярка для парсинга названия
    regexp = re.compile(
        r'^gisdo-3_0'
        r'-(?P<date>\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})'
        r'-(?P<id>[0-9a-f]{32})\.xml$'
    )

    def __init__(self, report_id=None, report_date=None):
        self.report_id = report_id or uuid4().hex
        self.report_date = report_date or datetime.now()

    @classmethod
    def from_filename(cls, filename):
        """Создаёт объект из названия файла."""
        match = cls.regexp.search(filename)

        if match is None:
            # Файл старый используем OldReport
            date = filename.replace('gisdo-3_0-', '').replace('.xml', '')
            return OldReport(filename, datetime.min, date)

        report_date = datetime.strptime(match.group('date'), cls.datetime_format)
        report_id = match.group('id')

        return cls(report_id=report_id, report_date=report_date)

    @property
    def filename(self):
        """Название файла."""
        return self.template.format(date=self.formatted_date, id=self.report_id)

    @property
    def formatted_date(self):
        """Сформатированная дата для использования в названии."""
        return self.report_date.strftime(self.datetime_format)

    @property
    def pretty_date(self):
        """Читабельная дата."""
        return self.report_date.strftime('%d.%m.%Y %H:%M:%S')


@app.get('/service')
def get_wsdl():
    if 'wsdl' in request.GET:
        response.headers['Content-Type'] = 'text/xml;charset=UTF-8'
        if request.GET['wsdl'] == 'PushDataServiceSoap.wsdl':
            return static_file('pushDataIn.xml', root=SCHEMA_PATH)
        else:
            return static_file('pushData.xml', root=SCHEMA_PATH)


@app.post('/service/')
@app.post('/service')
def save_xml():
    try:
        request_xml = etree.fromstring(request.body.read())
        report = Report()
        filename = os.path.join(XML_PATH, report.filename)

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w') as f:
            f.write(
                base64.b64decode(request_xml.find('.//{{{0}}}data'.format('http://eo.edu.ru')).text).decode('utf-8')
            )

        response.headers['Content-Type'] = 'text/xml;charset=UTF-8'
    except Exception:
        logger.error(traceback.format_exc())

    return (
        '<soap:Envelope '
        'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body><PushZipDataAsyncResponse xmlns="http://eo.edu.ru">'
        '<PushZipDataAsyncResult><Result>true</Result><Message></Message>'
        '</PushZipDataAsyncResult></PushZipDataAsyncResponse></soap:Body>'
        '</soap:Envelope>'
    )


@app.get('/')
@jinja2_view('index.html', template_lookup=['templates'])
def main():
    try:
        file_names = os.listdir(XML_PATH)
    except OSError:
        return dict(reports=[])

    reports = tuple(Report.from_filename(filename) for filename in file_names)

    return dict(reports=sorted(reports, key=lambda r: (r.report_date, r.filename), reverse=True))


@app.get('/xml/3/<filename>')
def get_xml(filename):
    response.headers['Content-Type'] = 'text/xml;charset=UTF-8'
    return static_file(filename, root=XML_PATH)


@app.get('/static/<dirname>/<filename>')
def static(dirname, filename):
    return static_file(filename, root=os.path.join(STATIC_PATH, dirname))


if __name__ == '__main__':
    from settings import *

    update_schema_xml(WSDL_HOST, WSDL_POST)
    run(app=app, host=HOST, port=PORT)
