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