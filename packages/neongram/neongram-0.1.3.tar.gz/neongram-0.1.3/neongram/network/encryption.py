from typing import Tuple
import asyncio
import hashlib
import struct
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .shared import Connection
from ..parser.tl_object import TLFunction


class Encryption:
    @staticmethod
    def aes_ige_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Encrypt data using AES-256 in IGE mode.

        Args:
            data (bytes): Data to encrypt.
            key (bytes): 32-byte encryption key.
            iv (bytes): 32-byte initialization vector.

        Returns:
            bytes: Encrypted data.
        """
        cipher = Cipher(algorithms.AES(key), modes.IGE(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded = Encryption._pad_data(data)
        return encryptor.update(padded) + encryptor.finalize()

    @staticmethod
    def aes_ige_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt data using AES-256 in IGE mode.

        Args:
            data (bytes): Data to decrypt.
            key (bytes): 32-byte decryption key.
            iv (bytes): 32-byte initialization vector.

        Returns:
            bytes: Decrypted data.
        """
        cipher = Cipher(algorithms.AES(key), modes.IGE(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(data) + decryptor.finalize()
        return Encryption._unpad_data(decrypted)

    @staticmethod
    def _pad_data(data: bytes) -> bytes:
        padding_length = 16 - (len(data) % 16) if len(data) % 16 else 16
        return data + os.urandom(padding_length)

    @staticmethod
    def _unpad_data(data: bytes) -> bytes:
        return data[:-data[-1]] if data[-1] <= 16 else data

    @staticmethod
    def generate_message_key(auth_key: bytes, msg: bytes) -> bytes:
        """Generate a message key for MTProto encryption.

        Args:
            auth_key (bytes): Full 256-byte authorization key.
            msg (bytes): Message data (including header).

        Returns:
            bytes: 16-byte message key.
        """
        x = 0  # Client-to-server
        sha256 = hashlib.sha256(auth_key[88 + x : 88 + x + 32] + msg).digest()
        return sha256[8:24]

    @staticmethod
    def generate_aes_key_iv(auth_key: bytes, msg_key: bytes, is_server: bool = False) -> Tuple[bytes, bytes]:
        """Generate AES key and IV for MTProto encryption.

        Args:
            auth_key (bytes): Full 256-byte authorization key.
            msg_key (bytes): 16-byte message key.
            is_server (bool): True if server-side, False if client-side.

        Returns:
            Tuple[bytes, bytes]: 32-byte AES key and 32-byte IV.
        """
        x = 8 if is_server else 0
        sha256_a = hashlib.sha256(msg_key + auth_key[x : x + 36]).digest()
        sha256_b = hashlib.sha256(auth_key[x + 40 : x + 76] + msg_key).digest()
        aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
        aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
        return aes_key, aes_iv


async def generate_auth_key(connection: Connection, nonce: bytes) -> bytes:
    """Perform Diffie-Hellman key exchange to generate an authorization key.

    Args:
        connection (Connection): Active MTProto connection.
        nonce (bytes): 16-byte nonce from the client.

    Returns:
        bytes: 256-byte authorization key.
    """
    req_pq = TLFunction("req_pq_multi", 0xbe7e8ef1, [{"name": "nonce", "type": "int128"}], "ResPQ")
    req_pq.values["nonce"] = int.from_bytes(nonce, "little")
    res_pq_raw = await connection.send(req_pq.serialize())
    res_pq = await connection.receive()

    # Parse res_pq (simplified; real parsing would use TL deserialization)
    server_nonce = res_pq[12:28]  
    pq = int.from_bytes(res_pq[28:36], "little")  
    fingerprints = struct.unpack("<q", res_pq[44:52])[0]  

    p, q = Encryption._factorize_pq(pq)

    p_bytes = p.to_bytes((p.bit_length() + 7) // 8, "little")
    q_bytes = q.to_bytes((q.bit_length() + 7) // 8, "little")
    encrypted_data = Encryption._prepare_inner_data(nonce, server_nonce, p_bytes, q_bytes)
    req_dh = TLFunction(
        "req_DH_params",
        0xd712e4be,
        [
            {"name": "nonce", "type": "int128"},
            {"name": "server_nonce", "type": "int128"},
            {"name": "p", "type": "string"},
            {"name": "q", "type": "string"},
            {"name": "public_key_fingerprint", "type": "long"},
            {"name": "encrypted_data", "type": "bytes"},
        ],
        "Server_DH_Params",
    )
    req_dh.values["nonce"] = int.from_bytes(nonce, "little")
    req_dh.values["server_nonce"] = int.from_bytes(server_nonce, "little")
    req_dh.values["p"] = p_bytes
    req_dh.values["q"] = q_bytes
    req_dh.values["public_key_fingerprint"] = fingerprints
    req_dh.values["encrypted_data"] = encrypted_data
    res_dh_raw = await connection.send(req_dh.serialize())
    res_dh = await connection.receive()
    
    g = 3  # Hardcoded for Telegram DH
    dh_prime = int.from_bytes(bytes.fromhex("c71caeb9c6b1c9048e6c522f70f13f73980d40238e3e21c14934d037563d930f48198a0aa7c14058229493d22530f4dbfa336f6e0ac925139543aed44cce7c3720fd51f69458705ac68cd4fe6b6b13abdc9746512969328454f18faf8c595f642477fe96bb2a941d5bcd1d4ac8cc49880708fa9b378e3c4f3a9060bee67cf9a4a4a695811051907e162753b56b0f6b410dba74d8a84b2a14b3144e0ef1284754fd17ed950d5965b4b9dd46582db1178d169c6bc465b0d6ff9ca3928fef5b9ae4e418fc15e83ebea0f87fa9ff5ad434838f806061b0f85c921f500b692c035f5f6b5fd92d9a8f5"), "big")
    a = int.from_bytes(os.urandom(256), "little") % dh_prime
    g_a = pow(g, a, dh_prime)
    g_a_bytes = g_a.to_bytes(256, "little")
    inner_data = Encryption._prepare_dh_inner_data(nonce, server_nonce, g_a_bytes)
    encrypted_inner = Encryption._encrypt_inner_data(inner_data)
    set_dh = TLFunction(
        "set_client_DH_params",
        0xf5045f1f,
        [
            {"name": "nonce", "type": "int128"},
            {"name": "server_nonce", "type": "int128"},
            {"name": "encrypted_data", "type": "bytes"},
        ],
        "SetClientDHParamsAnswer",
    )
    set_dh.values["nonce"] = int.from_bytes(nonce, "little")
    set_dh.values["server_nonce"] = int.from_bytes(server_nonce, "little")
    set_dh.values["encrypted_data"] = encrypted_inner
    await connection.send(set_dh.serialize())
    dh_answer = await connection.receive()
    server_g_b = int.from_bytes(dh_answer[20:276], "little") 
    auth_key = pow(server_g_b, a, dh_prime).to_bytes(256, "little")
    return auth_key


class Encryption:
    @staticmethod
    def _factorize_pq(pq: int) -> Tuple[int, int]:
        for i in range(2, int(pq ** 0.5) + 1):
            if pq % i == 0:
                return i, pq // i
        return pq, 1

    @staticmethod
    def _prepare_inner_data(nonce: bytes, server_nonce: bytes, p: bytes, q: bytes) -> bytes:
        data = (
            b"\x83\x4e\x81\x6f"  # p_q_inner_data constructor
            + nonce
            + server_nonce
            + os.urandom(16)  # new_nonce
            + Encryption._serialize_string(p)
            + Encryption._serialize_string(q)
        )
        return hashlib.sha1(data).digest() + data

    @staticmethod
    def _prepare_dh_inner_data(nonce: bytes, server_nonce: bytes, g_a: bytes) -> bytes:
        data = (
            b"\x3e\x05\x47\xdb"  # client_DH_inner_data constructor
            + nonce
            + server_nonce
            + struct.pack("<q", 0)  # retry_id
            + g_a
        )
        return hashlib.sha1(data).digest() + data

    @staticmethod
    def _encrypt_inner_data(data: bytes) -> bytes:
        # In practice, this uses RSA with Telegram's public key; here we simulate
        return data  # Placeholder; real RSA encryption needed

    @staticmethod
    def _serialize_string(data: bytes) -> bytes:
        length = len(data)
        if length <= 253:
            padding = (4 - (length + 1) % 4) % 4
            return struct.pack("<B", length) + data + b"\x00" * padding
        padding = (4 - length % 4) % 4
        return b"\xfe" + struct.pack("<I", length)[:3] + data + b"\x00" * padding