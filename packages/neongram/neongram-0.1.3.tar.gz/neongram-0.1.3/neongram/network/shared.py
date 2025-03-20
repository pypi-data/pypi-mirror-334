from typing import Optional
import socket
import ssl
import asyncio
from neongram.utils.binary_writer import BinaryWriter

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
        self.ssl_context = self._create_ssl_context() if use_ssl else None
        self.auth_key: Optional[bytes] = None
        self.server_salt: Optional[int] = None
        self.connected = False

    def _create_ssl_context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        context.load_default_certs(purpose=ssl.Purpose.SERVER_AUTH)
        print(f"TLS Minimum Version: {context.minimum_version}")
        print(f"TLS Maximum Version: {context.maximum_version}")
        print(f"Supported Ciphers: {context.get_ciphers()}")
        return context

    async def connect(self) -> None:
        loop = asyncio.get_event_loop()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if (self.use_ssl and self.ssl_context):
                print(f"Connecting to {self.host}:{self.port} with SSL")
                self.socket = self.ssl_context.wrap_socket(
                    self.socket,
                    server_hostname=self.host,
                    do_handshake_on_connect=True  # Ensure handshake happens here
                )
                # Print SSL details after handshake
                print(f"Negotiated Protocol: {self.socket.version()}")
                print(f"Negotiated Cipher: {self.socket.cipher()}")
            await loop.run_in_executor(None, self.socket.connect, (self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Connection failed: {e}")
            raise ConnectionError(f"Failed to connect: {e}")

    def send(self, data: bytes) -> None:
        if not self.socket or not self.connected:
            raise ConnectionError("No active connection")
        writer = BinaryWriter()
        writer.write_int(0xeeeeeeee)  # MTProto header
        writer.write_int(len(data))   # Length of payload
        writer.write_bytes(data)      # Payload
        self.socket.send(writer.get_bytes())

    async def receive(self, buffer_size: int = 4096) -> bytes:
        if not self.socket or not self.connected:
            raise ConnectionError("No active connection")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, self.socket.recv, buffer_size)
        if not data:
            raise ConnectionError("Connection closed by server")
        return data

    async def close(self) -> None:
        if self.socket and self.connected:
            self.socket.close()
            self.connected = False
            self.socket = None
            print("Connection closed")