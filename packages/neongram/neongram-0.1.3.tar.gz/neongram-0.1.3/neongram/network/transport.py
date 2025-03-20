from typing import Optional
import asyncio
import struct


class Transport:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        await self._send_init_packet()

    async def _send_init_packet(self) -> None:
        # TCP full transport identifier (0xef) with padding
        init_packet = b"\xef" + b"\x00" * 3
        await self.write(init_packet)

    async def write(self, data: bytes) -> None:
        if not self.writer:
            raise ConnectionError("Transport not connected")
        packet = self._prepare_packet(data)
        self.writer.write(packet)
        await self.writer.drain()

    def _prepare_packet(self, data: bytes) -> bytes:
        length = len(data)
        if length >= 0x7f:
            return struct.pack("<I", length << 2 | 1) + data
        return struct.pack("<B", length) + data

    async def read(self) -> bytes:
        if not self.reader:
            raise ConnectionError("Transport not connected")
        length_data = await self.reader.readexactly(1)
        length = struct.unpack("<B", length_data)[0]

        if length == 0x7f:
            length_data = await self.reader.readexactly(3)
            length = struct.unpack("<I", length_data + b"\x00")[0] >> 2

        return await self.reader.readexactly(length)

    async def close(self) -> None:
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.reader = None
        self.writer = None