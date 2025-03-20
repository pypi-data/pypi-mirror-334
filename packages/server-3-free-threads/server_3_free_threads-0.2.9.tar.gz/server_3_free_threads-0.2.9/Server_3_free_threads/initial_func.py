import logging
import sys
from threading import Thread
import os
from Server_3_free_threads.parsers.parser_args import ParserCommandLineArgs
from Server_3_free_threads.classes.server_actions_class import ServerActions
from Server_3_free_threads.parsers.parser_config import ParserConfigFile
import importlib

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)


def main():
    # добавления пути терминала в sys.path, нужно для импортирования приложения WSGI
    sys.path.append(os.getcwd())
    # параметры по умолчанию
    host = '127.0.0.1'
    port = 8888
    # этот параметр у socket.listen(backlog) определяет размер очереди ожидающих подключение
    socket_backlog = 200
    # модуль приложения WSGI
    module = None
    # domain
    domain = 'localhost'
    # инициализация парсера командной строки
    pars_args = ParserCommandLineArgs()
    # проверяется существования параметров
    if pars_args.check_args():
        pars_args.find_args()
        # получение значения configfile
        configfile = pars_args.configfile
        # инициализация парсера файла конфигурации
        pars_config = ParserConfigFile(configfile)
        # проверка существования пути файла конфигурации
        if pars_config.check_path():
            # парсинг файла
            pars_config.parsing_file()
            # получение обязательных параметров
            host, port, path_app, socket_backlog, domain = (pars_config.host, int(pars_config.port),
                                                pars_config.app, int(pars_config.socket_backlog), pars_config.domain)
            if path_app:
                # импорт приложения WSGI
                module = importlib.import_module(path_app)
                # Обновите внутренние кэши искателей, хранящиеся в sys.meta_path.
                # Если искатель реализует invalidate_caches(), то он будет вызван для обновления.
                # Эта функция должна вызываться, если какие-либо модули создаются/устанавливаются
                # во время работы вашей программы, чтобы гарантировать, что все искатели заметят
                # существование нового модуля.
                importlib.invalidate_caches()

    else:
        log.info("параметр configfile не указан в командной строке, использованы значения по умолчанию")
        log.info("сервер запущен в тестовом режиме")
    # инициализация класса сервера
    serv_actions = ServerActions(host=host, port=port, backlog=socket_backlog, domain=domain)
    if module:
        # если приложение WSGI импортировано, запустить сервер в рабочем режиме
        send_in_sock_thread = Thread(target=serv_actions.sending_to_socket, args=(module,))
    else:
        # если приложение WSGI не импортировано, запустить сервер в тестовом режиме
        send_in_sock_thread = Thread(target=serv_actions.sending_to_socket_test)

                # поток, принимающий подключения
    threads = (Thread(target=serv_actions.accepting_connections),
               # поток, читающий данные из клиентского сокета
               Thread(target=serv_actions.reading_from_socket),
               # поток, отправляющий данные в клиентский сокет
               send_in_sock_thread,
               # поток, закрывающий клиентские сокеты
               Thread(target=serv_actions.close_client_sock),)

    for elem in threads:
        elem.start()
    for elem in threads:
        elem.join()
