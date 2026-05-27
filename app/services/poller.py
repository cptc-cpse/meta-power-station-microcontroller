from app.configuration.config import Config
from app.shelley.poll import Poller

class PollerService:
    """
    Service responsible for managing the Poller instance and its configuration.
    """

    def __init__(self, config: Config):
        self.poller = Poller(config)
        self.READING_TYPES = config.reading_types
        self.STATION_ID = config.station_id
        self.BUILDING_ID = config.building_id
        self.latest_readings = []

    async def poll_to_readings(self):
        """
        Polls the Shelly device and converts the readings into a structured format.
        """
        await self.poller.start()
        await self.extract_readings()

    async def extract_readings(self):
        """
        Extracts the latest readings from the Poller and stores them in the latest_readings list.
        """
        # Assuming the Poller has a method to get the latest readings
        self.latest_readings = await self.poller.get_latest_readings()   

