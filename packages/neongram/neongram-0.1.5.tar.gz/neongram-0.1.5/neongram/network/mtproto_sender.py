from typing import Optional
from .shared import Connection
import asyncio
import struct
import time


class MTProtoSender:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.message_ids: set[int] = set()
        self.lock = asyncio.Lock()

    async def send(self, data: bytes) -> None:
        message = await self._create_message(data)
        await self.connection.transport.write(message)

    async def _create_message(self, data: bytes) -> bytes:
        msg_id = await self._generate_message_id()
        seq_no = await self.connection.next_sequence()
        
        # MTProto message format: auth_key_id (8), msg_id (8), seq_no (4), length (4), data
        header = struct.pack(
            "<qqii",
            self.connection.auth_key if self.connection.auth_key else 0,
            msg_id,
            seq_no,
            len(data)
        )
        return header + data

    async def _generate_message_id(self) -> int:
        async with self.lock:
            current_time = int(time.time() * 1000) << 32  # Milliseconds since epoch
            while True:
                msg_id = current_time | (len(self.message_ids) & 0xFFFE)  # Ensure even number
                if msg_id not in self.message_ids:
                    self.message_ids.add(msg_id)
                    return msg_id