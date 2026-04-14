import asyncio

from app.shelley import poll as shelly_poll
from app.mqtt import publisher as mqtt_publisher

BROKER = "mqtt.example.com"
PORT = 1883
TOPIC = "shelley/current"


def extract_current(status_response):
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
                return first.get("current") or first.get("power")
    return None


async def publish_status(status):
    current_value = extract_current(status)
    if current_value is None:
        print("Current value not found in status response; not publishing.")
        return

    payload = mqtt_publisher.build_current_payload(current_value)
    mqtt_publisher.publish(TOPIC, payload, BROKER, PORT)
    print(f"Published current to {TOPIC}: {payload}")


async def main():
    await shelly_poll.setup_device()
    await shelly_poll.poll_forever(callback=publish_status)


if __name__ == "__main__":
    asyncio.run(main())
