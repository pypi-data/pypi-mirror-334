class Q3RconLibError(Exception):
    """Base Q3RconLib error class"""


class Q3RconLibLoginError(Q3RconLibError):
    """Exception raised on an invalid login attempt"""
