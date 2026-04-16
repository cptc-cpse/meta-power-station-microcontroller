import json
from typing import Any

import paho.mqtt.client as mqtt


def build_current_payload(current_value: Any) -> str:
    """Build a compact JSON payload containing the current measurement.
    TODO: build a payload that matches the expected format for the MQTT topic subscribers.
    Args:
        current_value: The current measurement value to include in the payload.

    Returns:
        A JSON string with a compact current payload.
    """
    return json.dumps({"current": current_value}, separators=(",", ":"))


def publish(topic: str, payload: str, broker: str, port: int = 1883, qos: int = 1, retain: bool = False) -> None:
    """Publish an MQTT message to the specified broker and topic.

    Args:
        topic: MQTT topic to publish to.
        payload: JSON payload to send.
        broker: MQTT broker hostname or IP address.
        port: MQTT broker port number.
        qos: MQTT quality of service level.
        retain: Whether the message should be retained by the broker.

    Returns:
        None: The client publishes the message and then disconnects.
    """
    client = mqtt.Client()
    client.connect(broker, port, 60)
    client.publish(topic, payload, qos=qos, retain=retain)
    client.disconnect()
