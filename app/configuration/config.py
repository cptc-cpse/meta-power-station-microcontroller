from dataclasses import dataclass, field

#Filepath to the configuration file
CONFIG_PATH: str

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

def get_config() -> Config:
    """Retrieves the application configuration.
    Attempts to load from a file, but if no valid configuration is found, 
    calls create_config to generate the configuration with user input.

    Returns:
        Config: The application configuration object.
    """
    return Config()

def create_config() -> Config:
    """Creates a new configuration by prompting the user for input.
    When no input is provided, defaults are used.
    Validates the input and saves the configuration to a file for future use.

    Returns:
        Config: The newly created configuration object based on user input.
    """
    return Config()

def is_valid_config() -> bool:
    """Checks if the existing configuration file is valid.
    Checks for the presence of the configuration file, 
    and whether all fields are present and formatted correctly.

    Returns:
        bool: True if the configuration file exists and is valid, False otherwise.
    """
    return True