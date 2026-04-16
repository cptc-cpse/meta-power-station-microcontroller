import asyncio
import json
from typing import Any, Awaitable, Callable, Dict, Optional

from bleak import BleakClient

from app.shelley.rpc import (
    RPC_CHAR_DATA_UUID,
    RPC_CHAR_RX_CTL_UUID,
    RPC_CHAR_TX_CTL_UUID,
    build_rpc_payload,
    pack_length_header,
    parse_rpc_response,
)

ADDRESS = "30:30:F9:EB:DC:EE"


async def send_rpc(client: BleakClient, method: str, params: Optional[Dict[str, Any]] = None, request_id: int = 1) -> Dict[str, Any]:
    """Send a single RPC request to the Shelly device over BLE.

    Args:
        client: The BLE client connected to the Shelly device.
        method: The RPC method name to invoke.
        params: Optional parameters for the RPC request.
        request_id: Unique identifier for the request.

    Returns:
        Parsed Shelly RPC response as a dictionary.
    """
    payload = build_rpc_payload(method, params, request_id)

    await client.write_gatt_char(
        RPC_CHAR_TX_CTL_UUID,
        pack_length_header(payload),
        response=True,
    )
    await asyncio.sleep(0.5)

    await client.write_gatt_char(RPC_CHAR_DATA_UUID, payload, response=True)
    await asyncio.sleep(0.5)

    rx_len_raw = await client.read_gatt_char(RPC_CHAR_RX_CTL_UUID)
    rx_len = int.from_bytes(bytes(rx_len_raw[:4]), byteorder="big")

    buffer = bytearray()
    while len(buffer) < rx_len:
        chunk = await client.read_gatt_char(RPC_CHAR_DATA_UUID)
        if not chunk:
            break
        buffer.extend(chunk)
        await asyncio.sleep(0.1)

    # Parse only the expected response length from the buffer.
    return parse_rpc_response(bytes(buffer[:rx_len]))


async def call(
    address: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    request_id: int = 1,
    retries: int = 3,
) -> Dict[str, Any]:
    """Call a Shelly RPC method with retries and BLE connection management.

    Args:
        address: BLE address of the Shelly device.
        method: RPC method name.
        params: Optional method parameters.
        request_id: Base request ID for the RPC call.
        retries: Number of retry attempts if communication fails.

    Returns:
        The parsed Shelly RPC response dictionary.
    """
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            async with BleakClient(address, timeout=20.0) as client:
                print(f"Connected for {method}: {client.is_connected}")
                await asyncio.sleep(1.0)
                response = await send_rpc(client, method, params, request_id + attempt - 1)
                print(json.dumps(response, indent=2))
                return response
        except Exception as exc:
            last_err = exc
            print(f"{method} attempt {attempt} failed: {repr(exc)}")
            if attempt < retries:
                await asyncio.sleep(8)
    raise last_err


async def get_status(address: str = ADDRESS, retries: int = 3) -> Dict[str, Any]:
    """Fetch the current Shelly device status.

    Args:
        address: BLE address of the Shelly device.
        retries: Number of retry attempts if status retrieval fails.

    Returns:
        The Shelly status response dictionary.
    """
    return await call(address, "Switch.GetStatus", {"id": 0}, 400, retries=retries)


async def setup_device(address: str = ADDRESS) -> None:
    """Configure the Shelly device and ensure the relay is set on."""
    print("\n--- current config ---")
    await call(address, "Switch.GetConfig", {"id": 0}, 100)

    print("\n--- set config to detached ---")
    await call(
        address,
        "Switch.SetConfig",
        {
            "id": 0,
            "config": {
                "in_mode": "detached",
                "initial_state": "on",
            },
        },
        200,
    )

    await asyncio.sleep(8)

    print("\n--- turn relay on ---")
    await call(address, "Switch.Set", {"id": 0, "on": True}, 300)

    await asyncio.sleep(8)


async def poll_forever(
    address: str = ADDRESS,
    interval: int = 5,
    callback: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
) -> None:
    """Continuously poll Shelly status and optionally invoke a callback.

    Args:
        address: BLE address of the Shelly device.
        interval: Polling interval in seconds.
        callback: Optional async callback invoked with each status response.

    Returns:
        None: Runs indefinitely unless cancelled.
    """
    print("\n--- read status (polling every 5 seconds indefinitely) ---")
    poll_count = 0
    while True:
        poll_count += 1
        print(f"\nPoll {poll_count}:")
        status = await call(address, "Switch.GetStatus", {"id": 0}, 400)
        if callback:
            await callback(status)
        await asyncio.sleep(interval)
