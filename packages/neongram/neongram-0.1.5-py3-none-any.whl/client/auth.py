# neongram/auth.py
from typing import Optional, Tuple
import asyncio
from neongram.parser.tl_object import TLFunction, TLObject
import os
from neongram.utils.binary_writer import BinaryWriter
from neongram.utils.binary_reader import BinaryReader

class Auth:
    """Handles authentication flows for NeonClient."""

    def __init__(self, client):
        from neongram.client.client import NeonClient
        self.client = client
        self.phone_code_hash: Optional[str] = None

    async def authenticate(self) -> None:
        """Authenticates the client, either as a user or a bot."""
        if self.client.bot_token:
            await self._auth_bot()
        else:
            await self._auth_user()

    async def _auth_user(self) -> None:
        """Authenticates a user with phone number and code."""
        if not self.client.phone_number:
            self.client.phone_number = await self._prompt("Phone number: ")
        await self._send_code()
        code = self.client.phone_code or await self._prompt("Enter code: ")
        await self._sign_in(code)
        self.client.session.session_id = await self._generate_session_id()

    async def _auth_bot(self) -> None:
        """Authenticates a bot using a bot token."""
        from neongram.methods import AuthImportBotAuthorization
        request = AuthImportBotAuthorization()
        request.values["api_id"] = self.client.api_id
        request.values["api_hash"] = self.client.api_hash
        request.values["bot_auth_token"] = self.client.bot_token
        response = await self.client.invoke(request)
        auth_key, server_salt = await self._perform_dh_exchange()
        self.client.session.auth_key = auth_key
        self.client.session.server_salt = server_salt
        self.client.session.session_id = await self._generate_session_id()

    async def _send_code(self) -> None:
        """Sends a code to the user's phone number."""
        from neongram.methods import AuthSendCode
        request = AuthSendCode()
        request.values["phone_number"] = self.client.phone_number
        request.values["api_id"] = self.client.api_id
        request.values["api_hash"] = self.client.api_hash
        request.values["settings"] = {"_": "codeSettings", "flags": 0}  # Example flag
        response = await self.client.invoke(request)
        self.phone_code_hash = self._parse_sent_code(response)

    async def _sign_in(self, code: str) -> None:
        """Signs in the user with the provided code."""
        from neongram.methods import AuthSignIn
        request = AuthSignIn()
        request.values["phone_number"] = self.client.phone_number
        request.values["phone_code_hash"] = self.phone_code_hash
        request.values["phone_code"] = code
        if self.client.password:
            request.values["password"] = self.client.password
            request.values["flags"] = 1  # Example flag for password
        response = await self.client.invoke(request)
        if hasattr(response, "_") and response._ == "auth.authorizationSignUpRequired":
            await self._handle_two_step(response)
        auth_key, server_salt = await self._perform_dh_exchange()
        self.client.session.auth_key = auth_key
        self.client.session.server_salt = server_salt

    async def check_two_steps(self) -> bool:
        """Checks if two-step verification is enabled."""
        from neongram.methods import AuthSignIn
        request = AuthSignIn()
        request.values["phone_number"] = self.client.phone_number
        request.values["phone_code_hash"] = self.phone_code_hash
        request.values["phone_code"] = "dummy_code"
        response = await self.client.invoke(request)
        return hasattr(response, "_") and response._ in ("auth.authorizationSignUpRequired", "account.password")

    async def _handle_two_step(self, response: TLObject) -> None:
        """Handles two-step verification if required."""
        if hasattr(response, "_") and response._ == "auth.authorizationSignUpRequired":
            password = await self._prompt("Enter password for two-step verification: ")
            self.client.password = password
            from neongram.methods import AuthSignIn
            request = AuthSignIn()
            request.values["phone_number"] = self.client.phone_number
            request.values["phone_code_hash"] = self.phone_code_hash
            request.values["phone_code"] = "dummy_code"
            request.values["password"] = password
            request.values["flags"] = 1
            await self.client.invoke(request)

    async def _perform_dh_exchange(self) -> Tuple[bytes, int]:
        """Performs a simplified Diffie-Hellman key exchange (placeholder)."""
        nonce = await asyncio.get_event_loop().run_in_executor(None, os.urandom, 16)
        req_pq = TLFunction("req_pq_multi", 0xBE7E8EF1, [{"name": "nonce", "type": "int128"}], "ResPQ")
        req_pq.values["nonce"] = int.from_bytes(nonce, "little")
        response = await self.client.invoke(req_pq)
        # Simplified: In production, implement full DH exchange with Telegram's protocol
        auth_key = await asyncio.get_event_loop().run_in_executor(None, os.urandom, 256)
        server_salt = int.from_bytes(await asyncio.get_event_loop().run_in_executor(None, os.urandom, 8), "little")
        return auth_key, server_salt

    async def _prompt(self, message: str) -> str:
        """Prompts the user for input."""
        return await asyncio.get_event_loop().run_in_executor(None, input, message)

    async def _generate_session_id(self) -> int:
        """Generates a session ID."""
        return int.from_bytes(await asyncio.get_event_loop().run_in_executor(None, os.urandom, 8), "little")

    def _parse_sent_code(self, response: bytes) -> str:
        """Parses the phone_code_hash from the auth.sendCode response."""
        reader = BinaryReader(response)
        reader.read_int()  # Constructor ID (simplified)
        phone_code_hash = reader.read_string()
        return phone_code_hash