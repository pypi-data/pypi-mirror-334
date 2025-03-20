import threading
import time
from collections import deque
import socket
import logging
import sys
import select
import os
from Server_3_free_threads.response_headers import ResponseHeaders


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)


class ServerActions:

    def __init__(self, host, port, backlog):
        self._host = host
        self._port = port
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

    def accepting_connections(self) -> None:
        """
        it's first step
        next step: reading_from_socket
        """
        self._preparation_for_accept()
        with self._server_socket as sock:
            while True:
                conn, addr = sock.accept()
                conn.setblocking(False)
                fd = conn.fileno()
                # log.info(f'fd = {fd}')
                self._connections_dict[str(fd)] = conn
                self._epoll_object_for_read.register(
                    fd=fd, eventmask=select.EPOLLIN | select.EPOLLET
                )

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

    def reading_from_socket(self) -> None:
        """
        next step: sending_to_socket
        """
        while True:
            fd_set = self._epoll_object_for_read.poll()
            for fd, event in fd_set:
                # log.info(f'fd = {fd}, ready read')
                self._epoll_object_for_read.unregister(fd)
                sock = self._connections_dict.pop(str(fd))
                data = self._recv_from_sock(sock)
                if data:
                    data = data.decode()
                    self._deque_object_for_write.append((sock, data))
                    self._write_in_sock_event.set()
                else:
                    sock.close()

    def sending_to_socket(self, module) -> None:
        app_django = None
        if module:
            app_django = module.application
        while True:
            self._write_in_sock_event.wait()
            # log.info(f'get event write, in sending to socket')
            sock, data = self._clear_deque_for_write()
            self._write_in_sock_event.clear()
            self._write_in_socket(app_django, self._setup_environ(), sock, data)

    def _clear_deque_for_write(self):
        while self._deque_object_for_write:
            sock, data = self._deque_object_for_write.popleft()
            return sock, data

    def _write_in_socket(self, app_django, environ, sock, data):
        data_list_lines = data.splitlines()
        headers_request = self._setup_headers(data_list_lines)
        log.info(f'headers: \n{headers_request}')
        method, path, _ = data_list_lines[0].split(' ')
        environ['PATH_INFO'] = path
        environ['REQUEST_METHOD'] = method
        cookie = headers_request.get("Cookie")
        if cookie:
            environ['HTTP_COOKIE'] = cookie
        if app_django:
            resp_headers = ResponseHeaders()
            result = app_django(environ, resp_headers.start_response)
            for elem in result:
                response = resp_headers.headers.encode() + elem
                sock.sendall(response)
        else:
            sock.sendall(self._response_cap)
            # log.info(f'fd = {sock.fileno()}, sendall')
        self._all_client_sockets.append(sock)
        self._close_client_sock_event.set()

    def close_client_sock(self):
        while True:
            self._close_client_sock_event.wait()
            time.sleep(0.3)
            while self._all_client_sockets:
                sock = self._all_client_sockets.popleft()
                # log.info(f'fd = {sock.fileno()}, close socket')
                sock.close()
                self._close_client_sock_event.clear()

    @staticmethod
    def _response_cap_method():
        html = f'<h1 style="display: flex; justify-content: center; font-style: italic;">Test page</h1>'
        response = (f'HTTP/1.1 200 OK\r\n'
                    f'Content-Type: text/html\r\n'
                    f'Content-Length: {len(html)}\r\n'
                    f'Connection: close\r\n\r\n'
                    f'{html}\r\n')
        return response.encode()

    def _setup_environ(self):
        environ = dict(os.environ.items())
        environ['wsgi.input'] = sys.stdin
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = True
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once'] = False
        environ['SERVER_PORT'] = self._port
        environ['SERVER_NAME'] = 'localhost'
        return environ

    def _setup_headers(self, data):
        headers = {}
        for elem in data[1:]:
            if elem:
                log.info(elem)
                result = elem.split(': ')
                log.info(result)
                headers[result[0]] = result[1]
        return headers

