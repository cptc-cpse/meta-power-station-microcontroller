import pytest
from app.configuration.config import Config
from app.services.poller import PollerService
from unittest.mock import patch

@pytest.fixture
def poller_service():
    """Fixture that provides a PollerService instance."""
    config = Config()
    return PollerService(config)

@pytest.mark.asyncio
async def test_poll_to_readings_happy_path(poller_service):
    """Test that poll_to_readings successfully polls the Shelly device and extracts readings."""
    # Arrange
    status = {"result": {"apower": 100, "voltage": 230, "current": 0.43, "temperature":{"tC": 25.0, "tF": 77.0}}}
    with patch.object(poller_service.poller, 'poll', return_value=status):
        # Act
        readings =await poller_service.poll_to_readings()

        # Assert
        # Verify that latest_readings is populated with expected data
        assert len(readings) == 3

@pytest.mark.asyncio
async def test_extract_readings_happy_path(poller_service):
    """Test that extract_readings successfully extracts readings from the Shelly status response."""
    # Arrange
    status = {"result": {"apower": 100, "voltage": 230, "current": 0.43, "temperature":{"tC": 25.0, "tF": 77.0}}}

    # Act
    readings = poller_service.extract_readings(status)

    # Assert
    # Verify that latest_readings is populated with expected data
    assert readings is not None
    assert len(readings) == 3
    for reading in readings:
        assert reading.station_id == poller_service.STATION_ID
        assert reading.building_id == poller_service.BUILDING_ID
        assert reading.reading_type in poller_service.READING_TYPES
        assert reading.unit == poller_service.READING_TYPES[reading.reading_type]
        assert reading.value is not None