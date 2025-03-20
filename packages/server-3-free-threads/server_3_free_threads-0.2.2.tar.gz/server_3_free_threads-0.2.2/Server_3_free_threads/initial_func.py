import logging
import sys
from threading import Thread
import os
from Server_3_free_threads.parser_args import ParserCommandLineArgs
from Server_3_free_threads.server_actions import ServerActions
from Server_3_free_threads.parser_config import ParserConfigFile
import importlib

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)


def main():
    sys.path.append(os.getcwd())

    host = '127.0.0.1'
    port = 8888
    socket_backlog = 200
    module = None

    pars_args = ParserCommandLineArgs()
    pars_args.find_args()
    configfile = pars_args.configfile
    if configfile:
        pars_config = ParserConfigFile(configfile)
        if pars_config.open_file():
            host, port, path_app, socket_backlog = (pars_config.host, int(pars_config.port),
                                                    pars_config.app, int(pars_config.socket_backlog))
            if path_app:
                module = importlib.import_module(path_app)
                importlib.invalidate_caches()
        else:
            return

    else:
        log.info("configfile не указан, сервер запущен в тестовом режиме")
    serv_actions = ServerActions(host=host, port=port, backlog=socket_backlog)
    if module:
        send_in_sock_thread = Thread(target=serv_actions.sending_to_socket, args=(module,))
    else:
        send_in_sock_thread = Thread(target=serv_actions.sending_to_socket_test)

    threads = (Thread(target=serv_actions.accepting_connections),
               Thread(target=serv_actions.reading_from_socket),
               send_in_sock_thread,
               Thread(target=serv_actions.close_client_sock),)

    for elem in threads:
        elem.start()
    for elem in threads:
        elem.join()
