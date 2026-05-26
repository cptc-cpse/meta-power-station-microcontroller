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

        return ""