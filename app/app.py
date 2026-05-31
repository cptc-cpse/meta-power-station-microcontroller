import asyncio
from typing import Any, Optional

from app.configuration import config as app_config

# Services
from app.services.application import ApplicationService

"""
This module serves as the main entry point for the application, orchestrating the BLE communication
with the Shelly device and the MQTT publishing of current measurements.
"""
# Set to 0 for normal operation.
# Set to 1 to test MQTT publishing without Bluetooth polling,
# or set to 2 to test Bluetooth polling without MQTT publishing. 
TEST_MODE = 0

async def main() -> None:
    """Set up the Shelly device and begin polling its status indefinitely."""
    config = app_config.get_config()
    application_service = ApplicationService(config)
    if TEST_MODE == 2:
        # Test mode: periodically poll the Shelly device and print the extracted readings without publishing to MQTT
        await application_service.test_polling()
    elif TEST_MODE == 1:
        # Test mode: periodically publish a test payload to MQTT without Bluetooth polling
        await application_service.test_publishing()   
    else:
        # Normal mode: Poll Shelly device and publish status'
        await application_service.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
