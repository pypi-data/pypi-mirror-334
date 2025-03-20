from typing import Optional
from .shared import Connection
import asyncio
import struct


class MTProtoReceiver:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.running = False
        self.task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        if not self.running:
            self.running = True
            self.task = asyncio.create_task(self._receive_loop())

    async def stop(self) -> None:
        if self.running:
            self.running = False
            if self.task:
                self.task.cancel()
                try:
                    await self.task
                except asyncio.CancelledError:
                    pass

    async def receive(self) -> bytes:
        return await self.queue.get()

    async def _receive_loop(self) -> None:
        while self.running:
            try:
                data = await self.connection.transport.read()
                message = self._parse_message(data)
                await self.queue.put(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                await self.queue.put(self._create_error_message(e))
                break

    def _parse_message(self, data: bytes) -> bytes:
        # Basic MTProto message parsing: auth_key_id, msg_id, seq_no, length, body
        if len(data) < 20:
            raise ValueError("Invalid message length")

        auth_key_id = struct.unpack("<q", data[:8])[0]
        msg_id = struct.unpack("<q", data[8:16])[0]
        length = struct.unpack("<i", data[16:20])[0]
        
        if len(data) < 20 + length:
            raise ValueError("Message truncated")

        body = data[20:20 + length]
        return body

    def _create_error_message(self, error: Exception) -> bytes:
        error_code = -1  # Generic error
        error_message = str(error).encode("utf-8")
        return struct.pack("<ii", 0xc4b9f9bb, error_code) + self._serialize_string(error_message)

    def _serialize_string(self, value: str) -> bytes:
        encoded = value.encode("utf-8")
        length = len(encoded)
        if length <= 253:
            padding = (4 - (length + 1) % 4) % 4
            return struct.pack("<B", length) + encoded + b"\x00" * padding
        padding = (4 - length % 4) % 4
        return b"\xfe" + struct.pack("<I", length)[:3] + encoded + b"\x00" * padding