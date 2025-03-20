import logging
import sys
from threading import Thread
import os
# from Server_3_free_threads.load_app import load_app
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
    # port, path_app, configfile = int(pars_args.port), pars_args.app, pars_args.configfile
    configfile = pars_args.configfile
    if configfile:
        pars_config = ParserConfigFile(configfile)
        if pars_config.open_file():
            host, port, path_app, socket_backlog = (pars_config.host, int(pars_config.port),
                                                    pars_config.app, int(pars_config.socket_backlog))
            if path_app:
                module = importlib.import_module(path_app)
                importlib.invalidate_caches()

                # возможно ошибочное решение
                # if load_app(path_app):
                #     module = importlib.import_module(path_app)
                #     importlib.invalidate_caches()
        else:
            return

    else:
        log.info("configfile не указан, сервер запущен в тестовом режиме")
    serv_act = ServerActions(host=host, port=port, backlog=socket_backlog)
    threads = (Thread(target=serv_act.accepting_connections),
               Thread(target=serv_act.reading_from_socket),
               Thread(target=serv_act.sending_to_socket, args=(module,)),
               Thread(target=serv_act.close_client_sock),)

    for elem in threads:
        elem.start()
    for elem in threads:
        elem.join()
