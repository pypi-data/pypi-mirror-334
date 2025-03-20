from typing import Optional


class MTProtoException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RPCError(MTProtoException):
    """Exception for RPC-specific errors from Telegram server.

    Args:
        error_code (int): Error code returned by the server.
        error_message (str): Detailed error message.
    """

    def __init__(self, error_code: int, error_message: str):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(f"RPC Error {error_code}: {error_message}")


class ConnectionError(MTProtoException):
    def __init__(self, message: str = "Connection failed"):
        super().__init__(message)


class AuthenticationError(MTProtoException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class TimeoutError(MTProtoException):
    def __init__(self, message: str = "Operation timed out"):
        super().__init__(message)