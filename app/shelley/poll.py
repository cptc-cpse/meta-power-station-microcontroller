import asyncio
import json

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


async def send_rpc(client, method, params=None, request_id=1):
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

    return parse_rpc_response(bytes(buffer[:rx_len]))


async def call(address, method, params=None, request_id=1, retries=3):
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


async def get_status(address=ADDRESS, retries=3):
    return await call(address, "Switch.GetStatus", {"id": 0}, 400, retries=retries)


async def setup_device(address=ADDRESS):
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


async def poll_forever(address=ADDRESS, interval=5, callback=None):
    print("\n--- read status (polling every 5 seconds indefinitely) ---")
    poll_count = 0
    while True:
        poll_count += 1
        print(f"\nPoll {poll_count}:")
        status = await call(address, "Switch.GetStatus", {"id": 0}, 400)
        if callback:
            await callback(status)
        await asyncio.sleep(interval)
