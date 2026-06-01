import asyncio

from app.configuration import config as app_config
from app.models.power_reading import PowerReading
from app.services.poller import PollerService
from app.services.publication import PublicationService

async def main():
    config = app_config.get_config()
    global SLEEP_INTERVAL_SECONDS, poller_service, publication_service
    SLEEP_INTERVAL_SECONDS = config.sleep_interval_seconds
    poller_service = PollerService(config)
    publication_service = PublicationService(config)

    test_mode = 0
    while test_mode not in [1, 2]:
        test_mode_input = input("What would you like to test?\n"+
                                "Enter 1 to test MQTT publishing without Bluetooth polling, "+
                                "or 2 to test Bluetooth polling without MQTT publishing: ")
        if test_mode_input in ["1", "2"]:
            test_mode = int(test_mode_input)
        else:
            print("Invalid input. Please enter 1 or 2.")
    if test_mode == 1:
        await test_publishing()
    elif test_mode == 2:
        await test_polling()

async def test_publishing():
    """Test method to publish sample readings without polling."""
    print("Running in TEST_PUBLISH_MODE: Publishing test payload every", SLEEP_INTERVAL_SECONDS, "seconds")
    counter = 0
    while True:
        test_reading = PowerReading(
            station_id="test_station",
            building_id="test_building",
            reading_type="current",
            unit="amps",
            value=counter
        )
        publication_service.publish_reading(test_reading)
        counter += 1
        await asyncio.sleep(SLEEP_INTERVAL_SECONDS)

async def test_polling():
    """Test method to poll the Shelly device and print the extracted readings."""
    print("Running in TEST_POLL_MODE: Polling Shelly device every", SLEEP_INTERVAL_SECONDS, "seconds and printing extracted readings")
    while True:
        readings = await poller_service.poll_to_readings()
        print(f"Extracted Shelly Readings: {readings}")
        await asyncio.sleep(SLEEP_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())