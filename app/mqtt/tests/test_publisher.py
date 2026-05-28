from app.configuration import config as app_config
from app.mqtt import publisher as mqtt_publisher
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def config():
    """Fixture that provides a Config instance."""
    return app_config.Config()

def test_publisher_initializes_with_config(config):
    publisher = mqtt_publisher.Publisher(config)

    assert publisher.BROKER == config.mqtt_broker_address
    assert publisher.PORT == config.mqtt_broker_port
    assert publisher.QOS == config.mqtt_qos
    assert publisher.RETAIN == config.mqtt_retain
    assert publisher.LAST_WILL_MESSAGE == f"{config.station_id} in {config.building_id} has disconnected"
    assert publisher.LAST_WILL_TOPIC == f"clover_park/{config.building_id}/meta_power_station/{config.station_id}/status"

def test_publisher_publish_method(config):
    # Fake MQTT client so no real broker connection happens
    mock_client = MagicMock()

    # Fake publish result returned by client.publish()
    mock_result = MagicMock()
    mock_result.rc = 0
    mock_client.publish.return_value = mock_result

    # Patch mqtt.Client where Publisher uses it
    with patch("paho.mqtt.client.Client", return_value=mock_client):
        publisher = mqtt_publisher.Publisher(config)
        publisher.publish("test/topic", '{"current": 5}')

    # Verify the expected MQTT calls happened
    mock_client.connect.assert_called_once()
    mock_client.publish.assert_called_once()
    mock_result.wait_for_publish.assert_called_once_with(3)
    mock_client.disconnect.assert_called_once()