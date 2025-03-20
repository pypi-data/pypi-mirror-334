from typing import Optional
import os
import asyncio
from neongram.parser.tl_object import TLObject, TLFunction
from neongram.network.encryption import generate_auth_key
from neongram.client.client import NeonClient

class Auth:
    """Handles authentication flows for NeonClient.

    Args:
        client (NeonClient): The associated client instance.
    """
    def __init__(self, token):
        self.token = token

    async def authenticate(self) -> None:
        if self.client.bot_token:
            await self._auth_bot()
        else:
            await self._auth_user()

    async def _auth_user(self) -> None:
        if not self.client.phone_number:
            self.client.phone_number = await self._prompt("Phone number: ")
        await self._send_code()
        code = self.client.phone_code or await self._prompt("Enter code: ")
        await self._sign_in(code)
        self.client.session.session_id = await self._generate_session_id()

    async def _auth_bot(self) -> None:
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
        from neongram.methods import AuthSendCode
        request = AuthSendCode()
        request.values["phone_number"] = self.client.phone_number
        request.values["api_id"] = self.client.api_id
        request.values["api_hash"] = self.client.api_hash
        request.values["settings"] = {"_": "codeSettings"}
        response = await self.client.invoke(request)
        self.phone_code_hash = self._parse_sent_code(response)

    async def _sign_in(self, code: str) -> None:
        from neongram.methods import AuthSignIn
        request = AuthSignIn()
        request.values["phone_number"] = self.client.phone_number
        request.values["phone_code_hash"] = self.phone_code_hash
        request.values["phone_code"] = code
        if self.client.password:
            request.values["password"] = self.client.password
        response = await self.client.invoke(request)
        if hasattr(response, "_") and response._ == "auth.authorizationSignUpRequired":
            await self._handle_two_step(response)
        auth_key, server_salt = await self._perform_dh_exchange()
        self.client.session.auth_key = auth_key
        self.client.session.server_salt = server_salt

    async def check_two_steps(self) -> bool:
        from neongram.methods import AuthSignIn
        request = AuthSignIn()
        request.values["phone_number"] = self.client.phone_number
        request.values["phone_code_hash"] = self.phone_code_hash
        request.values["phone_code"] = "dummy_code" 
        response = await self.client.invoke(request)
        return hasattr(response, "_") and response._ in ("auth.authorizationSignUpRequired", "account.password")

    async def _handle_two_step(self, response: TLObject) -> None:
        if hasattr(response, "_") and response._ == "auth.authorizationSignUpRequired":
            password = await self._prompt("Enter password for two-step verification: ")
            self.client.password = password
            from neongram.methods import AuthSignIn
            request = AuthSignIn()
            request.values["phone_number"] = self.client.phone_number
            request.values["phone_code_hash"] = self.phone_code_hash
            request.values["phone_code"] = "dummy_code"
            request.values["password"] = password
            await self.client.invoke(request)

    async def _perform_dh_exchange(self) -> tuple[bytes, int]:
        nonce = await asyncio.get_event_loop().run_in_executor(None, os.urandom, 16)
        req_pq = TLFunction("req_pq_multi", 0xbe7e8ef1, [{"name": "nonce", "type": "int128"}], "ResPQ")
        req_pq.values["nonce"] = int.from_bytes(nonce, "little")
        res_pq = await self.client.invoke(req_pq)
        auth_key = await generate_auth_key(self.client.connection, nonce)
        server_salt = int.from_bytes(await asyncio.get_event_loop().run_in_executor(None, os.urandom, 8), "little")
        return auth_key, server_salt

    async def _prompt(self, message: str) -> str:
        return await asyncio.get_event_loop().run_in_executor(None, input, message)

    async def _generate_session_id(self) -> int:
        return int.from_bytes(await asyncio.get_event_loop().run_in_executor(None, os.urandom, 8), "little")

    # def _parse_sent_code(self, response: bytes) -> str:
    #     return "dummy_hash"  # Placeholder; requires deserialization