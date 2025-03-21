import socket

class AdditionalMethodsMixin:

    """
    Дополнительный класс со вспомогательными методами
    """

    @staticmethod
    def _recv_from_sock(sock: socket) -> bytes:

        """
        Метод для чтения из клиентского сокета
        """

        total_data = b''
        while True:
            try:
                data = sock.recv(2048)
            except BlockingIOError:
                return total_data
            else:
                # во время отладки выяснилось что браузер открывает подключения "на шаг вперёд",
                # одно с запросом, и второе пустое, которое потом возвращается объектом epoll через ~2min
                if data:
                    total_data += data
                else:
                    return total_data

    @staticmethod
    def _setup_request_headers(data: list) -> dict:

        """
        Метод собирает заголовки запроса, из списка строк в словарь
        """

        headers = {}
        for elem in data[1:]:
            if elem:
                key, val = elem.split(': ')
                headers[key] = val
        return headers
