import json
from unittest.mock import patch
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
    assert payload_dict["building_id"] == "building_24"
    assert payload_dict["reading_type"] == "current"
    assert payload_dict["value"] == 15.5
    assert payload_dict["unit"] == "amps"

def test_build_topic_happy_path(publication_service):
    """Test that build_topic successfully creates the correct MQTT topic string from a PowerReading."""
    # Arrange
    reading = PowerReading(
        station_id="station_alpha",
        building_id="building_24",
        reading_type="voltage",
        value=15.5,
        unit="volts"
    )

    # Act
    topic = publication_service.build_topic(reading)

    # Assert
    expected_topic = "clover_park/building_24/power_station/station_alpha/voltage"
    assert topic == expected_topic

def test_publish_reading_happy_path(publication_service):
    with patch('app.mqtt.publisher.Publisher.publish') as mock_publish:
        # Arrange
        reading = PowerReading(
            station_id="station_alpha",
            building_id="building_24",
            reading_type="current",
            value=15.5,
            unit="amps"
        )

        # Act
        publication_service.publish_reading(reading)

        # Assert
        mock_publish.assert_called_once()

def test_publish_readings_happy_path(publication_service):
    with patch('app.mqtt.publisher.Publisher.publish') as mock_publish:
        # Arrange
        readings = [
            PowerReading(
                station_id="station_alpha",
                building_id="building_24",
                reading_type="current",
                value=15.5,
                unit="amps"
            ),
            PowerReading(
                station_id="station_alpha",
                building_id="building_24",
                reading_type="voltage",
                value=120.0,
                unit="volts"
            )
        ]

        # Act
        publication_service.publish_readings(readings)

        # Assert
        assert mock_publish.call_count == 2