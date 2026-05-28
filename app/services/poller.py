from typing import Any, Optional

from app.shelley.poll import Poller
from app.configuration.config import Config
from app.models.power_reading import PowerReading
import logging


class PollerService:
    """
    Service responsible for managing the Poller instance and its configuration.
    """

    def __init__(self, config: Config):
        self.poller = Poller(config)
        self.READING_TYPES = config.reading_types
        self.STATION_ID = config.station_id
        self.BUILDING_ID = config.building_id

    async def poll_to_readings(self) -> list[PowerReading]:
        """
        Poll the Shelly device for status and extract power readings as a list of PowerReading objects.

        Returns:
            A list of PowerReading objects extracted from the Shelly status response.
        """
        status = await self.poller.poll()
        return self.extract_readings(status)

    def extract_readings(self, status: dict) -> list[PowerReading]:
        """
        Extract readings from the Shelly status response and return them as a list of PowerReading objects.
        
        Params:
            status: The Shelly status response dictionary.
        
        Returns:
            A list of PowerReading objects extracted from the status response.
        """

        readings = []
        result = status.get("result", status)
        if isinstance(result, dict):
            for reading_type, unit in self.READING_TYPES.items():
                value = result.get(reading_type)
                if value is not None:
                    reading = PowerReading(
                        station_id=self.STATION_ID,
                        building_id=self.BUILDING_ID,
                        reading_type=reading_type,
                        unit=unit,
                        value=value
                    )
                    readings.append(reading)
        else:
            logging.warning("Unexpected status format: 'result' is not a dict.")
        return readings

    


    


