import asyncio
from typing import Any, Optional

from app.configuration import config as app_config

# Services
from app.services.application import ApplicationService

"""
This module serves as the main entry point for the application, orchestrating the BLE communication
with the Shelly device and the MQTT publishing of current measurements.
"""

# Set to 1 to test MQTT publishing without Bluetooth polling,
# or set to 2 to test Bluetooth polling without MQTT publishing. Set to 0 for normal operation.
TEST_MODE = 0   

async def main() -> None:
    """Set up the Shelly device and begin polling its status indefinitely."""
    config = app_config.get_config()
    application_service = ApplicationService(config)
    if TEST_MODE == 2:
        print("Running in TEST_POLL_MODE: Polling Shelly device once and publishing status")
        while True:
            print(f"Extracted Shelly Readings: ")
    elif TEST_MODE == 1:
        # Test mode: periodically publish a test payload to MQTT without Bluetooth polling
        print("Running in TEST_MODE: Publishing test payload every  seconds")
        
    else:
        # Normal mode: Poll Shelly device and publish status'
        await application_service.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
