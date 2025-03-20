import threading
from collections import deque
import socket
import logging
import sys
import select

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)

class BaseClassMixin:

    def __init__(self, host, port, backlog, server_name):
        # хост
        self._host = host
        # порт
        self._port = port
        # имя сервера, которое указывается в заголовке ответа
        self._server_name = server_name
        # этот параметр у socket.listen(backlog) определяет размер очереди ожидающих подключение
        self._socket_backlog = backlog
        # инициализация сокета TCP с семейством адресов AF_INET, которое характеризуется парой (host, port)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # объект опроса для событий ввода-вывода, поддерживается только в Linux 2.5.44 и новее
        self._epoll_object_for_read = select.epoll()
        # очередь сокетов для записи
        self._deque_object_for_write = deque()
        # принятые подключения, где key - файловый дескриптор, value - клиентский сокет
        self._connections_dict = {}
        # очередь клиентских сокетов для их закрытия, так как нужна небольшая задержка(~0.3ms) после записи в них ответа
        self._all_client_sockets = deque()
        # событие для записи в клиентский сокет, возникает после прочтения сокета
        self._write_in_sock_event = threading.Event()
        # событие для закрытия клиентского сокета, возникает после записи в сокет
        self._close_client_sock_event = threading.Event()
        # заглушка ответа, используется для работы сервера если configfile не указан
        self._response_cap = self._response_cap_method()

    def _preparation_for_accept(self):

        """
        Метод вызывается перед циклом, принимающем подключения
        """

        #  Для работы с параметрами на уровне API сокета в level указывается значение SOL_SOCKET
        # Параметр optname SO_REUSEADDR позволяет прослушивающему серверу запуститься и с помощью функции bind
        # связаться со своим заранее известным портом, даже если существуют ранее установленные соединения,
        # использующие этот порт в качестве своего локального порта
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # привяжите сокет к адресу
        self._server_socket.bind((self._host, self._port))
        # Разрешите серверу принимать подключения. Если указано количество ожидающих подключений,
        # оно должно быть не меньше 0 (если оно меньше, устанавливается значение 0);
        # оно указывает количество непринятых подключений, которые система допустит,
        # прежде чем отклонить новые подключения.
        self._server_socket.listen(self._socket_backlog)
        log.info("server listen, HOST: %s, PORT: %s", self._host, self._port)
        log.info("socket backlog: %s", self._socket_backlog)
        try:
            #  это функция, которая проверяет, включён ли GIL (Global Interpreter Lock)
            #  в текущем интерпретаторе Python
            log.info(f'GIL enabled: {sys._is_gil_enabled()}')
        except AttributeError:
            pass

    def sending_to_socket_test(self) -> None:

        """
        Метод запускается в отдельном потоке, когда configfile не указан,
        служит для отправки ответа клиентскому сокету
        """

        while True:
            self._write_in_sock_event.wait()
            while self._deque_object_for_write:
                self._write_in_socket_test()
            self._write_in_sock_event.clear()

    def _write_in_socket_test(self) -> None:
        sock, data = self._deque_object_for_write.popleft()
        sock.sendall(self._response_cap)
        self._all_client_sockets.append(sock)
        self._close_client_sock_event.set()

    @staticmethod
    def _response_cap_method() -> bytes:

        """
        Такой ответ отправляется клиенту, когда configfile неуказан
        """

        html = f'<h1 style="display: flex; justify-content: center; font-style: italic;">Test page</h1>'
        response = (f'HTTP/1.1 200 OK\r\n'
                    f'Content-Type: text/html\r\n'
                    f'Content-Length: {len(html)}\r\n'
                    f'Connection: close\r\n\r\n'
                    f'{html}\r\n')
        return response.encode()