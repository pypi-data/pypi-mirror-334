import time
import logging
import sys
import select
import os
from Server_3_free_threads.response_headers import ResponseHeaders
from Server_3_free_threads.init_class import InitClassMixin
from Server_3_free_threads.additional_class import AdditionalMethodsMixin

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)

class ServerActions(InitClassMixin, AdditionalMethodsMixin):

    def __init__(self, *args, **kwargs):
        InitClassMixin.__init__(self, *args, **kwargs)

    def accepting_connections(self) -> None:
        """
        it's 1 step
        next step: reading_from_socket
        """
        self._preparation_for_accept()
        with self._server_socket as sock:
            while True:
                conn, addr = sock.accept()
                conn.setblocking(False)
                fd = conn.fileno()
                self._connections_dict[str(fd)] = conn
                self._epoll_object_for_read.register(
                    fd=fd, eventmask=select.EPOLLIN | select.EPOLLET
                )

    def reading_from_socket(self) -> None:
        """
        it's 2 step
        next step: sending_to_socket
        """
        while True:
            fd_set = self._epoll_object_for_read.poll()
            for fd, event in fd_set:
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
        """
        it's 3 step
        next step: close_client_sock
        """
        while True:
            self._write_in_sock_event.wait()
            while self._deque_object_for_write:
                self._write_in_socket(module, self._setup_environ())
            self._write_in_sock_event.clear()

    def _write_in_socket(self, module, environ):
        sock, data = self._deque_object_for_write.popleft()
        data_list_lines = data.splitlines()
        headers_request = self._setup_headers(data_list_lines)
        log.info(data_list_lines[0])
        method, path, _ = data_list_lines[0].split(' ')
        environ['PATH_INFO'] = path
        environ['REQUEST_METHOD'] = method
        environ['HTTP_COOKIE'] = headers_request.get("Cookie")
        # cookie = headers_request.get("Cookie")
        # if cookie:
        #     environ['HTTP_COOKIE'] = cookie
        app_django = module.application
        resp_headers = ResponseHeaders()
        result = app_django(environ, resp_headers.start_response)
        sock.send(resp_headers.headers_str.encode())
        for elem in result:
            try:
                sock.send(elem)
            except BlockingIOError:
                pass
        self._all_client_sockets.append(sock)
        self._close_client_sock_event.set()

    def close_client_sock(self):
        """
        it's 4 step
        """
        while True:
            self._close_client_sock_event.wait()
            time.sleep(0.3)
            while self._all_client_sockets:
                sock = self._all_client_sockets.popleft()
                sock.close()
                self._close_client_sock_event.clear()

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
        environ['SERVER_NAME'] = self._server_name
        return environ

    def sending_to_socket_test(self) -> None:
        while True:
            self._write_in_sock_event.wait()
            while self._deque_object_for_write:
                self.write_in_socket_test()
            self._write_in_sock_event.clear()

    def write_in_socket_test(self):
        sock, data = self._deque_object_for_write.popleft()
        sock.sendall(self._response_cap)
        self._all_client_sockets.append(sock)
        self._close_client_sock_event.set()

