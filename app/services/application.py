import asyncio

from app.configuration.config import Config
from app.services.poller import PollerService
from app.services.publication import PublicationService
from app.models.power_reading import PowerReading

class ApplicationService:
    def __init__(self, config: Config):
        self.SLEEP_INTERVAL_SECONDS = config.sleep_interval_seconds
        self.poller_service = PollerService(config)
        self.publication_service = PublicationService(config)

    async def run_forever(self):
        """Run the application indefinitely, polling for readings and publishing them."""
        await self.poller_service.poller.setup_device()
        print(f"\n--- read status (polling every {self.SLEEP_INTERVAL_SECONDS} seconds indefinitely) ---")
        while True:
            readings = await self.poller_service.poll_to_readings()
            self.publication_service.publish_readings(readings)
            await asyncio.sleep(self.SLEEP_INTERVAL_SECONDS)

    async def test_publishing(self):
        """Test method to publish sample readings without polling."""
        print("Running in TEST_PUBLISH_MODE: Publishing test payload every", self.SLEEP_INTERVAL_SECONDS, "seconds")
        while True:
            test_reading = PowerReading(
                station_id="test_station",
                building_id="test_building",
                reading_type="current",
                unit="amps",
                value=5.0
            )
            self.publication_service.publish_reading(test_reading)
            await asyncio.sleep(self.SLEEP_INTERVAL_SECONDS)

    async def test_polling(self):
        """Test method to poll the Shelly device and print the extracted readings."""
        print("Running in TEST_POLL_MODE: Polling Shelly device every", self.SLEEP_INTERVAL_SECONDS, "seconds and printing extracted readings")
        while True:
            readings = await self.poller_service.poll_to_readings()
            print(f"Extracted Shelly Readings: {readings}")
            await asyncio.sleep(self.SLEEP_INTERVAL_SECONDS)