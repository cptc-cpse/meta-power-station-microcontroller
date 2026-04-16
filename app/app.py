import asyncio
from typing import Any, Optional

from app.shelley import poll as shelly_poll
from app.mqtt import publisher as mqtt_publisher


"""
This module serves as the main entry point for the application, orchestrating the BLE communication
with the Shelly device and the MQTT publishing of current measurements.
"""

POLLING_INTERVAL_SECONDS : int = 10

# TODO: set these values when the broker and topics are ready
BROKER = "mqtt.example.com"
PORT = 1883
TOPIC = "shelly/current"


def extract_current(status_response: Any) -> Optional[Any]:
    """Extract the current measurement from a Shelly status response.

    Args:
        status_response: The response payload from the Shelly RPC call.
            Typically a dictionary containing "result" or a raw status dict.

    Returns:
        The extracted current or power value, or None when no measurement
        can be found.
    """
    if not isinstance(status_response, dict):
        return None

    result = status_response.get("result", status_response)
    if isinstance(result, dict):
        if "current" in result:
            return result["current"]

        meters = result.get("meters")
        if isinstance(meters, list) and meters:
            first = meters[0]
            if isinstance(first, dict):
                # Prefer an explicit current reading, fall back to power.
                return first.get("current") or first.get("power")

    return None


async def publish_status(status: Any) -> None:
    """
    Publish the current value extracted from a Shelly status response.

    Args:
        status: Shelly status response payload to inspect for current value.

    Returns:
        None: If no current value is found; otherwise publishes payload.
    """
    current_value = extract_current(status)
    if current_value is None:
        print("Current value not found in status response; not publishing.")
        return

    payload = mqtt_publisher.build_current_payload(current_value)
    mqtt_publisher.publish(TOPIC, payload, BROKER, PORT)
    print(f"Published current to {TOPIC}: {payload}")


async def main() -> None:
    """Set up the Shelly device and begin polling its status indefinitely."""
    await shelly_poll.setup_device()

    # Use a callback when MQTT publishing is enabled.
    # await shelly_poll.poll_forever(callback=publish_status)
    await shelly_poll.poll_forever(interval=POLLING_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
