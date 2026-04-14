import json
from typing import Any

import paho.mqtt.client as mqtt


def build_current_payload(current_value: Any) -> str:
    return json.dumps({"current": current_value}, separators=(",", ":"))


def publish(topic: str, payload: str, broker: str, port: int = 1883, qos: int = 1, retain: bool = False) -> None:
    client = mqtt.Client()
    client.connect(broker, port, 60)
    client.publish(topic, payload, qos=qos, retain=retain)
    client.disconnect()
