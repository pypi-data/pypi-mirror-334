import socket
from collections.abc import Iterable

class AdditionalMethodsMixin:

    @staticmethod
    def _recv_from_sock(sock: socket) -> bytes:
        total_data = b''
        while True:
            try:
                data = sock.recv(2048)
            except BlockingIOError:
                return total_data
            else:
                if data:
                    total_data += data
                else:
                    return total_data

    @staticmethod
    def _setup_headers(data: list) -> dict:
        headers = {}
        for elem in data[1:]:
            if elem:
                result = elem.split(': ')
                headers[result[0]] = result[1]
        return headers

    @staticmethod
    def _build_body(data: Iterable) -> bytes:
        total_data = b''
        for elem in data:
            total_data += elem
        return total_data
