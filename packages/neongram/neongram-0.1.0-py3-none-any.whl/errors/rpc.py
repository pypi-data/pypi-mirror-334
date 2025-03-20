from typing import Dict, Any, Optional
import struct
import asyncio
from neongram.network.shared import Connection
from neongram.parser.tl_object import TLFunction
from ..client import NeonClient
from neongram.errors.exceptions import RPCError


class RPC:
    def __init__(self, client: NeonClient):
        self.client = client
        self.pending_requests: Dict[int, asyncio.Future] = {}
        self.next_msg_id = 0
        self.lock = asyncio.Lock()

    async def call(self, function: TLFunction, timeout: float = 10.0) -> Any:
        """Execute an RPC call and await the response.

        Args:
            function (TLFunction): The TL function to call.
            timeout (float): Maximum time to wait for response in seconds.

        Returns:
            Any: Deserialized response data.

        Raises:
            RPCError: If the server returns an error.
        """
        msg_id = await self._generate_msg_id()
        future = self._create_future(msg_id)
        serialized = function.serialize()

        try:
            await self.client.connection.send(serialized)
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            future.cancel()
            raise RPCError(-1, "Request timed out")
        finally:
            if msg_id in self.pending_requests:
                del self.pending_requests[msg_id]

    async def _generate_msg_id(self) -> int:
        async with self.lock:
            current = self.next_msg_id
            self.next_msg_id += 2  # Ensure even numbers for client messages
            return current

    def _create_future(self, msg_id: int) -> asyncio.Future:
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[msg_id] = future
        return future

    async def handle_response(self, data: bytes) -> None:
        """Process incoming RPC responses and resolve pending requests.

        Args:
            data (bytes): Raw response data from the server.
        """
        msg_id = struct.unpack("<q", data[8:16])[0]
        if msg_id in self.pending_requests:
            future = self.pending_requests[msg_id]
            if data.startswith(b"\xf3\x5c\x6d\x01"):  # rpc_result
                length = struct.unpack("<i", data[20:24])[0]
                result = data[24:24 + length]
                future.set_result(result)
            elif data.startswith(b"\xc4\xb9\xf9\xbb"):  # rpc_error
                error_code = struct.unpack("<i", data[4:8])[0]
                error_message = data[12:].decode("utf-8", errors="ignore").split("\x00")[0]
                future.set_exception(RPCError(error_code, error_message))
            else:
                future.set_exception(RPCError(-1, "Unknown response type"))