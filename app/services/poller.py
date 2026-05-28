from typing import Any, Optional

from app.shelley.poll import Poller
from app.configuration.config import Config
from app.models.power_reading import PowerReading


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

    def poll_to_readings(self):
        """
        Poll_to_readings should return the latest readings
        """
        print("Latest readings:", self.latest_readings)
        return self.latest_readings

    async def extract_readings(self):
        """
        Extract_readings() should take in a status as a parameter, 
        and using the data from that and the configured variables, 
        create a PowerReading. If the poll() method returns the status, 
        then we could just have extract_readings() return the readings 
        for poll_to_readings() to use more directly, rather than setting
        latest_readings.
        """

        status = await self.poller.poll()

        if status is not None:
            reading = PowerReading(
                reading_type=status.get("reading_type", "current"),
                unit=status.get("unit", "amp"),
                value=status.get("value", 0.0),
            )
            self.latest_readings.append(reading)
            return self.poll_to_readings()
        else:
            print("No status received from Shelly device during polling.")

    


    


