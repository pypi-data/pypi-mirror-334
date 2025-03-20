# mypy: disable-error-code="attr-defined"

import logging
import socket

from . import packet
from .error import Q3RconLibLoginError

logger = logging.getLogger(__name__)


class Base:
    def __init__(self, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__)
        defaultkwargs = {
            'host': 'localhost',
            'port': 28960,
            'password': '',
            'default_timeout': 0.05,
            'timeouts': {},
        }
        kwargs = defaultkwargs | kwargs
        for attr, val in kwargs.items():
            setattr(self, attr, val)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._request = packet.Request(self.password)
        self._response = packet.Response()

    def send(self, cmd: str) -> str:
        """send a rcon command to the server

        Args:
            cmd (str): command string that takes the form "<cmd> <args>"

        Returns:
            str: the entire command response (all fragments) as one string
        """
        timeout: float = self.timeouts.get(
            cmd.split(' ', maxsplit=1)[0], self.default_timeout
        )
        self._sock.settimeout(timeout)

        try:
            self._sock.sendto(
                self._request.encode(cmd),
                (socket.gethostbyname(self.host), self.port),
            )
            self.logger.debug(f'sending: {cmd}')
        except socket.gaierror:
            raise Q3RconLibLoginError(f"unable to resolve host '{self.host}'")

        fragments: list[str] = []
        try:
            while resp := self._sock.recv(2048):
                if len(resp) > len(self._response.header):
                    if resp.startswith(self._response.header):
                        fragments.append(self._response.decode(resp))
        except TimeoutError:
            self.logger.debug('finished collecting response fragments')

        return ''.join(fragments)

    def close(self):
        self._sock.close()
