import asyncio
import json
import struct
from bleak import BleakClient

ADDRESS = "30:30:F9:EB:DC:EE"

RPC_CHAR_DATA_UUID   = "5f6d4f53-5f52-5043-5f64-6174615f5f5f"
RPC_CHAR_TX_CTL_UUID = "5f6d4f53-5f52-5043-5f74-785f63746c5f"
RPC_CHAR_RX_CTL_UUID = "5f6d4f53-5f52-5043-5f72-785f63746c5f"


async def shelly_rpc(client, method, params=None, request_id=1):
    req = {
        "id": request_id,
        "src": "bleak",
        "method": method,
        "params": params or {}
    }
    payload = json.dumps(req, separators=(",", ":")).encode("utf-8")

    await client.write_gatt_char(
        RPC_CHAR_TX_CTL_UUID,
        struct.pack(">I", len(payload)),
        response=True
    )
    await asyncio.sleep(0.5)

    await client.write_gatt_char(
        RPC_CHAR_DATA_UUID,
        payload,
        response=True
    )
    await asyncio.sleep(0.5)

    rx_len_raw = await client.read_gatt_char(RPC_CHAR_RX_CTL_UUID)
    rx_len = struct.unpack(">I", bytes(rx_len_raw[:4]))[0]

    buf = bytearray()
    while len(buf) < rx_len:
        chunk = await client.read_gatt_char(RPC_CHAR_DATA_UUID)
        if not chunk:
            break
        buf.extend(chunk)
        await asyncio.sleep(0.1)

    return json.loads(bytes(buf[:rx_len]).decode("utf-8"))


async def call(method, params=None, request_id=1, retries=3):
    last_err = None
    for attempt in range(retries):
        try:
            async with BleakClient(ADDRESS, timeout=20.0) as client:
                print(f"Connected for {method}: {client.is_connected}")
                await asyncio.sleep(1.0)
                resp = await shelly_rpc(client, method, params, request_id + attempt)
                print(json.dumps(resp, indent=2))
                return resp
        except Exception as e:
            last_err = e
            print(f"{method} attempt {attempt + 1} failed: {repr(e)}")
            await asyncio.sleep(8)
    raise last_err


async def main():
    print("\n--- current config ---")
    await call("Switch.GetConfig", {"id": 0}, 100)

    print("\n--- set config to detached ---")
    await call("Switch.SetConfig", {
        "id": 0,
        "config": {
            "in_mode": "detached",
            "initial_state": "on"
        }
    }, 200)

    await asyncio.sleep(8)

    print("\n--- turn relay on ---")
    await call("Switch.Set", {"id": 0, "on": True}, 300)

    await asyncio.sleep(8)

    print("\n--- read status (polling every 5 seconds indefinitely) ---")
    poll_count = 0
    while True:
        poll_count += 1
        print(f"\nPoll {poll_count}:")
        await call("Switch.GetStatus", {"id": 0}, 400)
        await asyncio.sleep(5)

    print("\n--- read config again ---")
    await call("Switch.GetConfig", {"id": 0}, 500)


asyncio.run(main())