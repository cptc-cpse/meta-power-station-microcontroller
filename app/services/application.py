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