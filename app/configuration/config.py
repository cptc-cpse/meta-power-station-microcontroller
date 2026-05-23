from dataclasses import dataclass, field
import json
import logging

#Filepath to the configuration file
CONFIG_PATH: str = "app/configuration/config.json"

@dataclass
class Config:
    """App configuration data class."""
    """Default values are currently being set for all fields for convenience, 
    but in the future values like the shelley_address and station_id should require 
    user specification during configuration creation as they should differ between each station."""

    #The identifer for the power station, used in MQTT topic construction
    station_id: str = "station_alpha" 
    #The identifer for the building, used in MQTT topic construction
    building_id: str = "building_24" 
    #The address of the MQTT broker being published to
    mqtt_broker_address: str = "192.168.1.115"
    #The port of the MQTT broker being published to
    mqtt_broker_port: int = 1883
    #The Quality of Service level for MQTT messages (0, 1, or 2)
    mqtt_qos: int = 1
    #Whether to retain MQTT messages on the broker
    mqtt_retain: bool = False
    #The BLE address of the Shelley device
    shelley_address: str = "30:30:F9:EB:DC:EE"
    #The types of readings to extract from the Shelly status response, mapped to their units
    reading_types: dict[str, str] =  field(default_factory=lambda: {"current": "amps", "power": "watts", "voltage": "volts"})
    #The interval in seconds between each loop of polling the Shelly device and publishing to MQTT
    sleep_interval_seconds: int = 10
    #The version of the configuration schema, used for validating and migrating configurations
    #Not set by the user, we will increment this when we make breaking changes to the 
    #configuration structure to trigger re-creation of the config file
    CONFIG_VERSION: int = 1

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create a Config instance from a dictionary, ignoring any extra fields."""
        return cls(
            station_id=data["station_id"],
            building_id=data["building_id"],
            mqtt_broker_address=data["mqtt_broker_address"],
            mqtt_broker_port=data["mqtt_broker_port"],
            mqtt_qos=data["mqtt_qos"],
            mqtt_retain=data["mqtt_retain"],
            shelley_address=data["shelley_address"],
            reading_types=data["reading_types"],
            sleep_interval_seconds=data["sleep_interval_seconds"],
            CONFIG_VERSION=data.get("CONFIG_VERSION", 1)
        )

def get_config() -> Config:
    """Retrieves the application configuration.
    Attempts to load from a file, but if no valid configuration is found, 
    calls create_config to generate the configuration with user input.

    Returns:
        Config: The application configuration object.
    """
    config = None
    if is_valid_config():
        with open(CONFIG_PATH, "r") as f:
            config_data = json.load(f)
            config = Config.from_dict(config_data)
            #print(config_data)
    else:
        logging.warning("No valid configuration found. Creating new configuration.")
        config = create_config()
    return config

def create_config() -> Config:
    """Creates a new configuration by prompting the user for input.
    When no input is provided, defaults are used.
    Validates the input and saves the configuration to a file for future use.

    Returns:
        Config: The newly created configuration object based on user input.
    """
    config = Config()

    json_string = json.dumps(config.__dict__, indent=4)
    with open(CONFIG_PATH, "w") as f:
        f.write(json_string)

    return Config()

def is_valid_config() -> bool:
    """Checks if the existing configuration file is valid.
    Checks for the presence of the configuration file, 
    and whether all fields are present and formatted correctly.

    Returns:
        bool: True if the configuration file exists and is valid, False otherwise.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config_data = json.load(f)
            config = Config.from_dict(config_data)
            return True
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.error(f"Configuration file error: {e}")
        return False
    
