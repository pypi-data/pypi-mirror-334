
class ResponseHeaders:

    def __init__(self):
        self._headers_str = None

    def start_response(self, status, response_headers, exc_info=None):
        headers = f'HTTP/1.1 {status}\r\n'
        for key, val in response_headers:
            headers += f'{key}: {val}\r\n'
        headers += 'Accept-Ranges: bytes\r\n\r\n'
        self._headers_str = headers

    @property
    def headers_str(self):
        return self._headers_str
