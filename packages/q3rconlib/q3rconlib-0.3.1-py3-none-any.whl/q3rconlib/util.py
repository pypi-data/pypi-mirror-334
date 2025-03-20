import functools
import time

from .error import Q3RconLibLoginError


def timeout(func):
    """Attempts a rcon login until time elapsed is greater than {Q3Rcon}._login_timeout"""

    @functools.wraps(func)
    def wrapper(*args):
        rcon, *_ = args

        err = None
        start = time.time()
        while time.time() < start + rcon.login_timeout:
            try:
                if not (resp := func(*args)):
                    raise TimeoutError('timeout attempting to login')

                if resp in (
                    'Bad rcon',
                    'Bad rconpassword.',
                    'Invalid password.',
                ):
                    raise Q3RconLibLoginError('Invalid rcon password.')
                elif (
                    resp == 'No rconpassword set on server or '
                    'password is shorter than 8 characters.\n'
                ):
                    raise Q3RconLibLoginError(
                        'No rcon password set on server or password is shorter than 8 characters.'
                    )

                err = None
                break
            except TimeoutError as e:
                err = e
                rcon.logger.debug(f'{type(e).__name__}: {e}... retrying login attempt')
                continue

        if err:
            raise Q3RconLibLoginError(str(err))

    return wrapper
