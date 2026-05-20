from app.configuration import config as app_config
from app.configuration.config import Config

def test_config_has_expected_defaults():
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
        "power": "watts",
        "voltage": "volts",
    }
    assert config.sleep_interval_seconds == 10
    assert config.CONFIG_VERSION == 1

def test_get_config_returns_config_object():
    config = app_config.get_config()
    assert isinstance(config, Config)

def test_create_config_returns_config_object():
    config = app_config.create_config()
    assert isinstance(config, Config)

def test_is_valid_config_returns_boolean():
    valid = app_config.is_valid_config()
    assert isinstance(valid, bool)