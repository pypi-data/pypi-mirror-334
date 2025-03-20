import logging
from typing import Self

from . import util
from .base import Base
from .error import Q3RconLibLoginError

logger = logging.getLogger(__name__)


class Q3Rcon:
    def __init__(self, **kwargs):
        self.logger = logger.getChild(self.__class__.__name__)
        self.login_timeout = kwargs.pop('login_timeout', 2)

        self._base = Base(**kwargs)

    def __enter__(self) -> Self:
        try:
            self._login()
            self.logger.info(f'Successfully established {self}')
        except Q3RconLibLoginError as e:
            self.logger.error(f'{type(e).__name__}: {e}')
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._base.close()

    def __repr__(self) -> str:
        return (
            type(self).__name__
            + "(hostname='{host}', port={port}, password='{password}', default_timeout={default_timeout})".format(
                **self._base.__dict__
            )
        )

    def __str__(self) -> str:
        return 'rcon connection to {host}:{port}'.format(**self._base.__dict__)

    @property
    def host(self) -> str:
        return self._base.host

    @property
    def port(self) -> int:
        return self._base.port

    @util.timeout
    def _login(self):
        return self.send('login')

    def send(self, cmd: str) -> str:
        return self._base.send(cmd)


def request_q3rcon_obj(**kwargs) -> Q3Rcon:
    """Interface entry point, use it to request a Q3Rcon object.

    Returns:
        Q3Rcon: A class implementing the Q3 Rcon protocol
    """
    cls = Q3Rcon
    return cls(**kwargs)
