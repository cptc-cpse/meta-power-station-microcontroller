from dataclasses import dataclass

CONFIG_PATH: str

@dataclass
class Config:
    station_id: str = "station_alpha"
    building_id: str = "building_24"
    mqtt_broker_address: str = "192.168.1.115"
    mqtt_broker_port: int = 1883
    mqtt_qos: int = 1
    mqtt_retain: bool = False
    shelley_address: str = "30:30:F9:EB:DC:EE"
    reading_types: dict[str, str] = {"current": "amps", "power": "watts", "voltage": "volts"}
    sleep_interval_seconds: int = 10
    config_version: int = 1

def get_config() -> Config:
    return Config()

def create_config() -> Config:
    return Config()

def is_valid_config() -> bool:
    return True