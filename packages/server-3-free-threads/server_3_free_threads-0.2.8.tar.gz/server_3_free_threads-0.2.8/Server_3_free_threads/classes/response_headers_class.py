
class ResponseHeaders:

    """
    Класс для сборки заголовков ответа в строку
    """

    def __init__(self):
        self._headers_str = None

    def start_response(self, status, response_headers, exc_info=None):

        """
        Метод передаётся в WSGI приложение
        """

        headers = f'HTTP/1.1 {status}\r\n'
        for key, val in response_headers:
            headers += f'{key}: {val}\r\n'
        # HTTP заголовок ответа Accept-Ranges — это маркер, который использует сервер,
        # чтобы уведомить клиента о поддержке "запросов по кускам"
        headers += 'Accept-Ranges: bytes\r\n\r\n'
        self._headers_str = headers

    @property
    def headers_str(self):
        return self._headers_str
