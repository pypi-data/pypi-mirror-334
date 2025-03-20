class ReportGenerationException(Exception):
    """Ошибка создания отчета"""


class ErrorWithMessage(Exception):
    """Базовая ошибка с сообщением."""

    message = None

    def __init__(self, message=None):
        self.message = message or self.message
        super(ErrorWithMessage, self).__init__(self.message)


class SendReportException(ErrorWithMessage):
    """Ошибка отправки отчета"""

    message = 'Ошибка при отправке данных по МО'


class ConnectingAtSendingReportException(ErrorWithMessage):
    """Ошибка соедиения при отправке отчета"""

    message = 'Ошибка соединения с удаленным сервером при отправке данных по МО'


class SOAPClientCreateException(ErrorWithMessage):
    """Ошибка создания SOAP клиента"""

    message = 'Ошибка при создании SOAP клиента'


class ReportFormRowLogicException(Exception):
    """Ошибка в логике сохранения модели ReportFormRow"""


class LostReportFormRowException(Exception):
    """Исключение которое генерируется в случае если отчетность собрана а,
    данные отсутствуют"""


class XMLException(Exception):
    """Исключение при формировании файла"""


class XMLRenderException(ErrorWithMessage):
    """Исключение возникающее при рендеринге XML"""

    message = 'Ошибка при формировании XML'


class XMLWriteException(XMLException):
    """Исключение возникающее при записи XML файла"""


class DocumentCreateException(ErrorWithMessage):
    """Ошибка при создании документа"""

    message = 'Ошибка при формировании документа по МО'


class NoDataInMo(ErrorWithMessage):
    """
    В МО нет садов по которым собираются данные
    """

    message = 'В МО нет садов для отправки в ЛКИ'
