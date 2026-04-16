import json
import struct
from typing import Any, Dict

"""
This module defines the RPC communication logic for interacting with Shelly devices over BLE,
"""


# RPC characteristic UUIDs for Shelly BLE communication.
# https://kb.shelly.cloud/knowledge-base/kbsa-communicating-with-shelly-devices-via-bluetoo
RPC_CHAR_DATA_UUID = "5f6d4f53-5f52-5043-5f64-6174615f5f5f"
RPC_CHAR_TX_CTL_UUID = "5f6d4f53-5f52-5043-5f74-785f63746c5f"
RPC_CHAR_RX_CTL_UUID = "5f6d4f53-5f52-5043-5f72-785f63746c5f"


def build_rpc_payload(method: str, params: Dict[str, Any] | None = None, request_id: int = 1) -> bytes:
    """
    Build the BLE RPC payload for a Shelly device request.

    Args:
        method: The RPC method name to invoke.
        params: Optional parameters for the RPC call.
        request_id: Unique request identifier for the call.

    Returns:
        The serialized JSON RPC payload as UTF-8 bytes.
    """
    request = {
        "id": request_id,
        "src": "bleak",
        "method": method,
        "params": params or {},
    }
    return json.dumps(request, separators=(",", ":")).encode("utf-8")


def parse_rpc_response(raw_bytes: bytes) -> Dict[str, Any]:
    """
    Parse a raw BLE RPC response payload into a Python dictionary.

    Args:
        raw_bytes: The raw bytes returned by the BLE RPC response.

    Returns:
        The parsed response data as a dictionary.
    """
    return json.loads(raw_bytes.decode("utf-8"))


def pack_length_header(payload: bytes) -> bytes:
    """
    Pack the length of the payload as a 4-byte big-endian header.

    Args:
        payload: The payload bytes to prefix with a length header.

    Returns:
        The 4-byte big-endian length prefix.
    """
    return struct.pack(">I", len(payload))
