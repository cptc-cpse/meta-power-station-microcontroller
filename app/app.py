import asyncio
from typing import Any, Optional

from app.shelley import poll as shelly_poll
from app.mqtt import publisher as mqtt_publisher
from app.configuration import config as app_config


"""
This module serves as the main entry point for the application, orchestrating the BLE communication
with the Shelly device and the MQTT publishing of current measurements.
"""

POLLING_INTERVAL_SECONDS : int = 10

# TODO: set these values when the broker and topics are ready
TOPIC = "clover_park/building_24/meta_power_station/station_alpha/current"

TEST_MODE = True  # Set to True to test MQTT publishing without Bluetooth polling

publisher : mqtt_publisher.Publisher 


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
    publisher.publish(TOPIC, payload)
    print(f"Published current to {TOPIC}: {payload}")


async def main() -> None:
    """Set up the Shelly device and begin polling its status indefinitely."""
    config = app_config.get_config()
    publisher = mqtt_publisher.Publisher(config)
    if TEST_MODE:
        # Test mode: periodically publish a test payload to MQTT without Bluetooth polling
        print("Running in TEST_MODE: Publishing test payload every", POLLING_INTERVAL_SECONDS, "seconds")
        while True:
            test_current = 5.0  # Example test current value
            payload = mqtt_publisher.build_current_payload(test_current)
            publisher.publish(TOPIC, payload)
            print(f"Test published to {TOPIC}: {payload}")
            await asyncio.sleep(POLLING_INTERVAL_SECONDS)
    else:
        # Normal mode: Poll Shelly device and publish status
        await shelly_poll.setup_device()
        await shelly_poll.poll_forever(interval=POLLING_INTERVAL_SECONDS, callback=publish_status)


if __name__ == "__main__":
    asyncio.run(main())
