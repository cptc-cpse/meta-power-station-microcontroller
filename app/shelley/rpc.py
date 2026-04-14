import json
import struct
from typing import Any, Dict

RPC_CHAR_DATA_UUID = "5f6d4f53-5f52-5043-5f64-6174615f5f5f"
RPC_CHAR_TX_CTL_UUID = "5f6d4f53-5f52-5043-5f74-785f63746c5f"
RPC_CHAR_RX_CTL_UUID = "5f6d4f53-5f52-5043-5f72-785f63746c5f"


def build_rpc_payload(method: str, params: Dict[str, Any] | None = None, request_id: int = 1) -> bytes:
    request = {
        "id": request_id,
        "src": "bleak",
        "method": method,
        "params": params or {},
    }
    return json.dumps(request, separators=(",", ":")).encode("utf-8")


def parse_rpc_response(raw_bytes: bytes) -> Dict[str, Any]:
    return json.loads(raw_bytes.decode("utf-8"))


def pack_length_header(payload: bytes) -> bytes:
    return struct.pack(">I", len(payload))
