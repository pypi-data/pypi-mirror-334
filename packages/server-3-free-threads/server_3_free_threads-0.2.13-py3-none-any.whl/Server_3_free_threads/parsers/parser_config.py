from pathlib import Path
import os
import re
import logging
from Server_3_free_threads.parsers.base import BaseMixin


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(filename)s:%(funcName)s] %(message)s')
log = logging.getLogger(__name__)


class ParserConfigFile(BaseMixin):

    """
    Класс реализующий парсинг файла конфигурации
    """

    def __init__(self, path):
        self._path = path
        self._abs_path = Path(os.getcwd())
        self._full_path = None
        self._full_path_exist = False

        self._port = None
        self._host = None
        self._app = None
        self._socket_backlog = None
        self._domain = None

        self._port_re = re.compile(r'PORT=(?P<port>\d{0,4})')
        self._app_re = re.compile(r'APP=(?P<app>.+)')
        self._backlog_re = re.compile(r'SOCKET_BACKLOG=(?P<backlog>\d{0,4})')
        self._host_re = re.compile(r'HOST=(?P<host>.+)')
        self._domain_re = re.compile(r'DOMAIN=(?P<domain>.+)')

    def check_path(self):

        """
        Проверка существования пути к файлу
        """
        full_path = self._abs_path.joinpath(self._path)
        if full_path.exists():
            log.info("file config exist")
            self._full_path = full_path
            self._full_path_exist = True
            return True

        else:
            self._full_path_exist = False
            log.info("file config don't exist")
            return False

    def parsing_file(self):

        """
        Парсинг файла конфигурации
        """

        if self._full_path_exist:
            with open(self._full_path, 'r') as file:
                for line in file.readlines():
                    result_port = self.pars_func(param=line, group='port', re_pattern=self._port_re)
                    result_app = self.pars_func(param=line, group='app', re_pattern=self._app_re)
                    result_host = self.pars_func(param=line, group='host', re_pattern=self._host_re)
                    result_backlog = self.pars_func(param=line, group='backlog', re_pattern=self._backlog_re)
                    result_domain = self.pars_func(param=line, group='domain', re_pattern=self._domain_re)

                    if result_port:
                        self._port = result_port
                    if result_app:
                        self._app = result_app
                    if result_host:
                        self._host = result_host
                    if result_backlog:
                        self._socket_backlog = result_backlog
                    if result_domain:
                        self._domain = result_domain

    @property
    def port(self):
        return self._port

    @property
    def host(self):
        return self._host

    @property
    def app(self):
        return self._app

    @property
    def socket_backlog(self):
        return self._socket_backlog

    @property
    def domain(self):
        return self._domain






