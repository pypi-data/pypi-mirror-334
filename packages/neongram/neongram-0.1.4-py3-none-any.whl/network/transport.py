import asyncio
import socket
from typing import Optional, Tuple

class TCP:
    def __init__(self, ipv6: bool, proxy: Optional[dict]):
        self.ipv6 = ipv6
        self.proxy = proxy
        self.socket: Optional[socket.socket] = None

    async def connect(self, address: Tuple[str, int]):
        raise NotImplementedError

    async def send(self, data: bytes):
        raise NotImplementedError

    async def recv(self) -> Optional[bytes]:
        raise NotImplementedError

    async def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

class TCPAbridged(TCP):
    async def connect(self, address: Tuple[str, int]):
        self.socket = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        await asyncio.get_event_loop().run_in_executor(None, self.socket.connect, address)
        # Abridged protocol handshake (send 0xEF as per MTProto abridged spec)
        self.socket.send(b"\xEF")

    async def send(self, data: bytes):
        if not self.socket:
            raise ConnectionError("Socket not connected")
        length = (len(data) // 4).to_bytes(1, "little")
        await asyncio.get_event_loop().run_in_executor(None, self.socket.send, length + data)

    async def recv(self) -> Optional[bytes]:
        if not self.socket:
            raise ConnectionError("Socket not connected")
        length_byte = await asyncio.get_event_loop().run_in_executor(None, self.socket.recv, 1)
        if not length_byte:
            return None
        length = int.from_bytes(length_byte, "little") * 4
        data = b""
        while len(data) < length:
            chunk = await asyncio.get_event_loop().run_in_executor(None, self.socket.recv, length - len(data))
            if not chunk:
                raise ConnectionError("Connection closed by server")
            data += chunk
        return data