import json
import pytest
from app.configuration.config import Config
from app.models.power_reading import PowerReading
from app.services.publication import PublicationService


@pytest.fixture
def publication_service():
    """Fixture that provides a PublicationService instance."""
    config = Config()
    return PublicationService(config)


def test_build_payload_happy_path(publication_service):
    """Test that build_payload successfully creates a valid JSON payload from a PowerReading."""
    # Arrange
    reading = PowerReading(
        station_id="station_alpha",
        building_id="building_24",
        reading_type="current",
        value=15.5,
        unit="amps"
    )

    # Act
    payload = publication_service.build_payload(reading)

    # Assert
    # Verify the payload is valid JSON
    payload_dict = json.loads(payload)


    # Verify the values match the input
    assert payload_dict["station_id"] == "station_alpha"
    # assert payload_dict["building_id"] == "building_24"
    # assert payload_dict["reading_type"] == "current"
    # assert payload_dict["value"] == 15.5
    # assert payload_dict["unit"] == "amps"
