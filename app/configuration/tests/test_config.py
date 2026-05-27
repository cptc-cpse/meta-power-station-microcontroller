from app.configuration import config as app_config
from app.configuration.config import Config
import pytest
import json
from unittest.mock import patch, mock_open, MagicMock

def test_config_has_expected_defaults():
    """Test that the Config class has the expected default values."""
    config = Config()

    assert config.station_id == "station_alpha"
    assert config.building_id == "building_24"
    assert config.mqtt_broker_address == "192.168.1.115"
    assert config.mqtt_broker_port == 1883
    assert config.mqtt_qos == 1
    assert config.mqtt_retain is False
    assert config.shelley_address == "30:30:F9:EB:DC:EE"
    assert config.reading_types == {
        "current": "amps",
        "apower": "watts",
        "voltage": "volts",
    }
    assert config.sleep_interval_seconds == 10
    assert config.CONFIG_VERSION == 1

def test_create_config_creates_valid_config():
    """Test that the create_config function creates a valid Config object with simulated user input.
    It ignores invalid input and continues to prompt until valid input is provided."""
    user_inputs = [
        "invalid station id",  # invalid station_id
        "station_test",  # station_id
        "invalid building id",  # invalid building_id
        "building_1",    # building_id
        "invalid mqtt broker address",  # invalid mqtt_broker_address
        "192.168.1.1",   # mqtt_broker_address
        "invalid mqtt broker port",  # invalid mqtt_broker_port
        "1883",          # mqtt_broker_port
        "invalid mqtt qos",  # invalid mqtt_qos
        "2",             # mqtt_qos
        "invalid mqtt retain",  # invalid mqtt_retain
        "true",         # mqtt_retain
        "invalid shelley address",  # invalid shelley_address
        "AA:BB:CC:DD:EE:FF",  # shelley_address
        "invalid sleep interval",  # invalid sleep_interval_seconds
        "5",             # sleep_interval_seconds
        # Reading types: start with default {current, apower, voltage}
        "invalid reading type",  # invalid reading type
        "current",       # removes current
        "apower",        # removes apower
        "voltage",       # removes voltage (now empty)
        "current",       # adds current
        "apower",        # adds apower
        "",              # finish reading types
    ]
    
    m_open = mock_open()
    with patch("builtins.input", side_effect=user_inputs):
        with patch("builtins.open", m_open):
            config = app_config.create_config()
            
            assert config.station_id == "station_test"
            assert config.building_id == "building_1"
            assert config.mqtt_broker_address == "192.168.1.1"
            assert config.mqtt_broker_port == 1883
            assert config.mqtt_qos == 2
            assert config.mqtt_retain is True
            assert config.shelley_address == "AA:BB:CC:DD:EE:FF"
            assert config.sleep_interval_seconds == 5
            assert "current" in config.reading_types
            assert "apower" in config.reading_types

def test_valid_config_returns_true_for_valid_config_file():
    """Test that the is_valid_config function returns True for a valid config file."""
    valid_config_data = json.dumps({
        "station_id": "station_alpha",
        "building_id": "building_24",
        "mqtt_broker_address": "192.168.1.115",
        "mqtt_broker_port": 1883,
        "mqtt_qos": 1,
        "mqtt_retain": False,
        "shelley_address": "30:30:F9:EB:DC:EE",
        "reading_types": {"current": "amps", "apower": "watts"},
        "sleep_interval_seconds": 10,
        "CONFIG_VERSION": 1
    })
    
    with patch("builtins.open", mock_open(read_data=valid_config_data)):
        result = app_config.is_valid_config()
        assert result is True

def test_valid_config_returns_false_for_invalid_config_file():
    """Test that the is_valid_config function returns False for an invalid config file."""
    # Invalid because station_id doesn't start with 'station_'
    invalid_config_data = json.dumps({
        "station_id": "invalid_id",
        "building_id": "building_24",
        "mqtt_broker_address": "192.168.1.115",
        "mqtt_broker_port": 1883,
        "mqtt_qos": 1,
        "mqtt_retain": False,
        "shelley_address": "30:30:F9:EB:DC:EE",
        "reading_types": {"current": "amps"},
        "sleep_interval_seconds": 10,
        "CONFIG_VERSION": 1
    })
    
    with patch("builtins.open", mock_open(read_data=invalid_config_data)):
        result = app_config.is_valid_config()
        assert result is False

def test_valid_config_returns_false_for_missing_config_file():
    """Test that the is_valid_config function returns False when the config file is missing."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = app_config.is_valid_config()
        assert result is False

def test_validation_support_functions_behave_as_expected():
    """Test that the validation support functions (all of the ones beginning with is_valid_)
    behave as expected when given valid and invalid input."""
    assert app_config.is_valid_station_id("station_alpha") is True
    assert app_config.is_valid_station_id("invalid station id") is False
    assert app_config.is_valid_building_id("building_24") is True
    assert app_config.is_valid_building_id("invalid building id") is False
    assert app_config.is_valid_mqtt_broker_address("192.168.1.115") is True
    assert app_config.is_valid_mqtt_broker_address("invalid broker address") is False
    assert app_config.is_valid_mqtt_broker_port("1883") is True
    assert app_config.is_valid_mqtt_broker_port("f") is False
    assert app_config.is_valid_mqtt_qos("1") is True
    assert app_config.is_valid_mqtt_qos("3") is False
    assert app_config.is_valid_mqtt_retain("true") is True
    assert app_config.is_valid_mqtt_retain("false") is True
    assert app_config.is_valid_mqtt_retain("invalid retain") is False
    assert app_config.is_valid_shelley_address("30:30:F9:EB:DC:EE") is True
    assert app_config.is_valid_shelley_address("invalid shelley address") is False
    assert app_config.is_valid_reading_types(app_config.VALID_READING_TYPES) is True
    assert app_config.is_valid_reading_types({"invalid reading type": "invalid unit"}) is False
    assert app_config.is_valid_sleep_interval("10") is True
    assert app_config.is_valid_sleep_interval("-1") is False
    assert app_config.is_valid_config_version(str(app_config.CURRENT_CONFIG_VERSION)) is True
    assert app_config.is_valid_config_version("invalid config version") is False

def test_get_config_returns_config_from_file():
    """Test that the get_config function retrieves a Config object from a file 
    when a valid config file is present."""
    valid_config_data = json.dumps({
        "station_id": "station_test",
        "building_id": "building_1",
        "mqtt_broker_address": "192.168.1.100",
        "mqtt_broker_port": 1883,
        "mqtt_qos": 1,
        "mqtt_retain": False,
        "shelley_address": "AA:BB:CC:DD:EE:FF",
        "reading_types": {"current": "amps", "voltage": "volts"},
        "sleep_interval_seconds": 15,
        "CONFIG_VERSION": 1
    })
    
    with patch("builtins.open", mock_open(read_data=valid_config_data)):
        with patch("app.configuration.config.is_valid_config", return_value=True):
            config = app_config.get_config()
            assert isinstance(config, Config)
            for key, value in json.loads(valid_config_data).items():
                assert getattr(config, key) == value

def test_get_config_calls_create_config_if_config_file_is_invalid():
    """Test that the get_config function calls create_config if the config file is invalid."""
    mock_config = Config(station_id="station_created")
    
    with patch("app.configuration.config.is_valid_config", return_value=False):
        with patch("app.configuration.config.create_config", return_value=mock_config) as mock_create:
            config = app_config.get_config()
            mock_create.assert_called_once()
            assert config.station_id == "station_created"