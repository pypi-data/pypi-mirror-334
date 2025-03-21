import time
import logging
import sys
import select
import os
from Server_3_free_threads.classes.response_headers_class import ResponseHeaders
from Server_3_free_threads.classes.base_class import BaseClassMixin
from Server_3_free_threads.classes.additional_class import AdditionalMethodsMixin

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)

class ServerActions(BaseClassMixin, AdditionalMethodsMixin):

    def __init__(self, *args, **kwargs):
        BaseClassMixin.__init__(self, *args, **kwargs)

    def accepting_connections(self) -> None:
        """
        it's 1 step
        next step: reading_from_socket
        """

        """
        Поток, принимающий подключения
        """
        self._preparation_for_accept()
        with self._server_socket as sock:
            while True:
                # ожидание подключений
                conn, addr = sock.accept()
                # если флаг имеет значение false, то сокет устанавливается в неблокирующий режим
                conn.setblocking(False)
                # получение файлового дескриптора клиентского сокета
                fd = conn.fileno()
                # добавление подключения в словарь, чтобы получить его в потоке reading_from_socket,
                # так как объект _epoll_object_for_read возвращает набор из файловых дескрипторов
                self._connections_dict[str(fd)] = conn
                # регистрация дескриптора в epoll, с отслеживанием события готовности к чтению
                # с поведением пограничного триггера select.EPOLLET
                #---------------------------------------------------------------------------------------------
                # пограничный триггер срабатывает однажды, при условии,
                # что с момента последнего события не произошло событий записи в сокете
                # триггер уровня срабатывает если сокет не заблокирован, и пока не будет опустошён
                #--------------------------------------------------------------------------------------------
                self._epoll_object_for_read.register(
                    fd=fd, eventmask=select.EPOLLIN | select.EPOLLET
                )

    def reading_from_socket(self) -> None:
        """
        it's 2 step
        next step: sending_to_socket
        """

        """
        Поток читающий клиентские сокеты
        """

        while True:
            # ожидание дескрипторов, готовых для чтения
            fd_set = self._epoll_object_for_read.poll()
            for fd, event in fd_set:
                # удалите зарегистрированный файловый дескриптор из объекта epoll
                self._epoll_object_for_read.unregister(fd)
                # получение клиентского сокета
                sock = self._connections_dict.pop(str(fd))
                # чтение данных
                data = self._recv_from_sock(sock)
                if data:
                    data = data.decode()
                    # добавление (сокет, данные) в очередь для записи
                    # очередь очищается в _write_in_socket
                    self._deque_object_for_write.append((sock, data))
                    # установка события для начала отправки данных в сокеты
                    self._write_in_sock_event.set()
                else:
                    sock.close()

    def sending_to_socket(self, module) -> None:
        """
        it's 3 step
        next step: close_client_sock
        """

        """
        Поток отправляющий данные в сокет
        module - приложение WSGI
        """
        while True:
            self._write_in_sock_event.wait()
            while self._deque_object_for_write:
                self._write_in_socket(module, self._setup_environ())
            self._write_in_sock_event.clear()

    def _write_in_socket(self, module, environ):
        sock, data = self._deque_object_for_write.popleft()
        data_list_lines = data.splitlines()
        headers_request = self._setup_request_headers(data_list_lines)
        log.info(data_list_lines[0])
        method, path, _ = data_list_lines[0].split(' ')
        environ['PATH_INFO'] = path
        environ['REQUEST_METHOD'] = method
        environ['HTTP_COOKIE'] = headers_request.get("Cookie", "")
        app = module.application
        resp_headers = ResponseHeaders()
        # получение итератора с телом ответа из приложения,
        # максимальный размер одной части ответа в данном случае, равен 4096 bytes
        result = app(environ, resp_headers.start_response)
        # отправка заголовков ответа,
        # добавлен заголовок Accept-Ranges: bytes
        sock.send(resp_headers.headers_str.encode())
        for elem in result:
            try:
                # отправка тела ответа частями
                sock.send(elem)
            except BlockingIOError:
                pass
        self._all_client_sockets.append(sock)
        self._close_client_sock_event.set()

    def close_client_sock(self):
        """
        it's 4 step
        """

        """
        Поток, закрывающий клиентские сокеты
        """
        while True:
            self._close_client_sock_event.wait()
            # во время отладки выяснилось, что сокет закрывается раньше, чем завершается отправка ответа,
            # для обхода проблемы добавлена задержка перед обходом всех клиентских сокетов для их закрытия
            time.sleep(0.3)
            while self._all_client_sockets:
                sock = self._all_client_sockets.popleft()
                sock.close()
                self._close_client_sock_event.clear()

    def _setup_environ(self) -> dict:

        """
        Установка переменных окружения,
        environ передаётся в WSGI приложение
        """

        environ = dict(os.environ.items())
        environ['wsgi.input'] = sys.stdin
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = True
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once'] = False
        environ['SERVER_PORT'] = self._port
        environ['SERVER_NAME'] = self._domain
        return environ



