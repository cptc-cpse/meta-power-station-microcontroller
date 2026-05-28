import json

from app.configuration.config import Config
from app.models.power_reading import PowerReading
from app.mqtt.publisher import Publisher  


class PublicationService:
    """
    Service responsible for building MQTT topics and payloads from power readings,
    and using the Publisher to send messages to the MQTT broker.
    
    """
    def __init__(self, config: Config):
        self.publisher = Publisher(config)

    def build_payload(self, reading: PowerReading) -> str:
        """
        Builds the message payload to be published to MQTT. 

        Params:
            reading(Reading): One power reading component
        
        Returns:
            A JSON string with the payload to be published to MQTT.
        """
        # TODO: do we prefer that power reading is a dataclass? 
        payload = {
            "station_id": reading.station_id,
            "building_id": reading.building_id,
            "reading_type": reading.reading_type,
            "value": reading.value,
            "unit": reading.unit
        }
        return json.dumps(payload)
    
    def build_topic(self, reading: PowerReading) -> str:
        """
        Builds the MQTT topic string based on the power reading information.

        Params:
            reading(Reading): One power reading component
        
        Returns:
            A string representing the MQTT topic to which to publish.
        """
        return f"clover_park/{reading.building_id}/power_station/{reading.station_id}/{reading.reading_type}"
    
    def publish_reading(self, reading: PowerReading):
        """
        Publishes a power reading to MQTT by building the topic and payload, 
        then using the Publisher to send the message.
        Params:
            reading(Reading): One power reading component
        """

        topic = self.build_topic(reading)
        payload = self.build_payload(reading)
        self.publisher.publish(topic, payload)
        print(f"Published to {topic}: {payload}")

    def publish_readings(self, readings: list[PowerReading]):
        """
        Publishes a list of power readings to MQTT by building the topic and payload for each, 
        then using the Publisher to send the messages.
        Params:
            readings(list[Reading]): A list of power reading components
        """
        for reading in readings:
            self.publish_reading(reading)