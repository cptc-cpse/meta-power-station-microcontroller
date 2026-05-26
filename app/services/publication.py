import json

from app.configuration.config import Config
from app.models.power_reading import PowerReading


class PublicationService:
    """
    TODO: nice big docstring here
    
    """
    def __init__(self, config: Config):
        self.config = config

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