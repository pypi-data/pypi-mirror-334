import threading
from collections import deque
import socket
import logging
import sys
import select

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)

class InitClassMixin:

    def __init__(self, host, port, backlog, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self._socket_backlog = backlog
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._epoll_object_for_read = select.epoll()
        self._deque_object_for_write = deque()
        self._connections_dict = {}
        self._all_client_sockets = deque()
        self._write_in_sock_event = threading.Event()
        self._close_client_sock_event = threading.Event()
        self._response_cap = self._response_cap_method()

    def _preparation_for_accept(self):
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(self._socket_backlog)
        log.info("server listen, HOST: %s, PORT: %s", self._host, self._port)
        log.info("socket backlog: %s", self._socket_backlog)
        try:
            log.info(f'GIL enabled: {sys._is_gil_enabled()}')
        except AttributeError:
            pass

    @staticmethod
    def _response_cap_method():
        html = f'<h1 style="display: flex; justify-content: center; font-style: italic;">Test page</h1>'
        response = (f'HTTP/1.1 200 OK\r\n'
                    f'Content-Type: text/html\r\n'
                    f'Content-Length: {len(html)}\r\n'
                    f'Connection: close\r\n\r\n'
                    f'{html}\r\n')
        return response.encode()