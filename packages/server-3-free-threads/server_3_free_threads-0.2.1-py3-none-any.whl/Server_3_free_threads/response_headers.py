
class ResponseHeaders:

    def __init__(self):
        self._headers = None

    def start_response(self, status, response_headers, exc_info=None):
        head = f'HTTP/1.1 {status}\r\n'
        for key, val in response_headers:
            head += f'{key}: {val}\r\n'
        head += '\r\n'
        self._headers = head

    @property
    def headers(self):
        return self._headers
