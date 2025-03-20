
class ResponseHeaders:

    def __init__(self):
        self._headers_str = None
        # self._headers = {}

    def start_response(self, status, response_headers, exc_info=None):
        head = f'HTTP/1.1 {status}\r\n'
        for key, val in response_headers:
            # self._headers[key] = val
            head += f'{key}: {val}\r\n'
        head += 'Accept-Ranges: bytes\r\n'
        head += '\r\n'
        self._headers_str = head

    @property
    def headers_str(self):
        return self._headers_str

    # @property
    # def headers(self):
    #     return self._headers
