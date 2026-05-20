import json
from typing import Any

import paho.mqtt.client as mqtt

from app.configuration import config

class Publisher:
    """Handles MQTT publishing of payloads to specific topics, 
    with configuration for broker address, port, QoS, and retain settings.
    """
    def __init__(self, config: config.Config):
        #MQTT broker hostname or IP address.
        self.BROKER = config.mqtt_broker_address
        #MQTT broker port number.
        self.PORT = config.mqtt_broker_port
        #MQTT Quality of Service level (0, 1, or 2) for message delivery.
        self.QOS = config.mqtt_qos
        #Whether the message should be retained by the broker.
        self.RETAIN = config.mqtt_retain
        #A last will message that the MQTT client will publish if it disconnects unexpectedly.
        self.LAST_WILL_MESSAGE = f"{config.station_id} in {config.building_id} has disconnected"
        #The MQTT topic for the last will message, indicating the status of the power station.
        self.LAST_WILL_TOPIC = f"clover_park/{config.building_id}/meta_power_station/{config.station_id}/status"

    def publish(self, topic: str, payload: str) -> None:
        """Publish an MQTT message to the specified broker and topic.

        Args:
            topic: MQTT topic to publish to.
            payload: JSON payload to send.

        Returns:
            None: The client publishes the message and then disconnects.
        """
        client = mqtt.Client()
        client.connect(self.BROKER, self.PORT, 60)
        client.will_set(self.LAST_WILL_TOPIC, self.LAST_WILL_MESSAGE, qos=self.QOS, retain=self.RETAIN)
        client.publish(topic, payload, qos=self.QOS, retain=self.RETAIN)
        client.disconnect()

#This won't be part of the publisher class, 
#it will be altered and moved to the publisher service once that's created
def build_current_payload(current_value: Any) -> str:
    """Build a compact JSON payload containing the current measurement.
    TODO: build a payload that matches the expected format for the MQTT topic subscribers.
    Args:
        current_value: The current measurement value to include in the payload.

    Returns:
        A JSON string with a compact current payload.
    """
    return json.dumps({"current": current_value}, separators=(",", ":"))



