import asyncio

from app.configuration import config as app_config
from app.services.application import ApplicationService

async def main() -> None:
    """Set up the Shelly device and begin polling its status indefinitely."""
    config = app_config.get_config()
    application_service = ApplicationService(config)
    await application_service.run_forever()

if __name__ == "__main__":
    asyncio.run(main())
