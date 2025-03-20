from typing import Optional
import socket
import ssl

class Connection:
    """Handles network connections for MTProto communication.

    Args:
        host (str): The host address.
        port (int): The port number.
        use_ssl (bool): Whether to use SSL/TLS.
    """

    def __init__(self, host: str, port: int, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.socket: Optional[socket.socket] = None
        self.ssl_context: Optional[ssl.SSLContext] = None
        self.auth_key: Optional[bytes] = None
        self.server_salt: Optional[int] = None

    async def connect(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.use_ssl:
            self.ssl_context = ssl.create_default_context()
            self.socket = self.ssl_context.wrap_socket(self.socket, server_hostname=self.host)
        self.socket.connect((self.host, self.port))

    def send(self, data: bytes) -> None:
        if self.socket:
            self.socket.send(data)

    def receive(self, buffer_size: int = 4096) -> bytes:
        if self.socket:
            return self.socket.recv(buffer_size)
        raise ConnectionError("No active connection")

    async def close(self) -> None:
        if self.socket:
            self.socket.close()
            self.socket = None