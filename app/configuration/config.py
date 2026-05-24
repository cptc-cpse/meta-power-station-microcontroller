from dataclasses import dataclass, field
import json
import logging

#Filepath to the configuration file
CONFIG_PATH: str = "app/configuration/config.json"

"""
There are other things we could pull from the status, 
but I'm not entirely sure how to handle them.
There is output and source, which is a boolean and string respectively,
there's aenergy, ret_aenergy, and temperature, which are nested dictionaries for some reason,
so we'd have to treat them special cases if we wanted to extract them.
"""
#Valid reading types that can be polled from the Shelly status response, mapped to their expected units
VALID_READING_TYPES = { 
    "current": "amps",
    "apower": "watts",
    "voltage": "volts",
    "frequency": "hertz"
}

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
    reading_types: dict[str, str] =  field(default_factory=lambda: {"current": "amps", "apower": "watts", "voltage": "volts"})
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
    print("Please enter the following configuration values. Press Enter to use the default value shown in parentheses, when applicable.")

    prompt = "Station ID (no default, format: 'station_<name>'): "
    config.station_id = get_valid_user_input(prompt, is_valid_station_id)
        
    prompt = f"Building ID (default: {config.building_id}): "
    config.building_id = get_valid_user_input(prompt, is_valid_building_id, default=config.building_id)

    prompt = f"MQTT Broker Address (default: {config.mqtt_broker_address}): "
    config.mqtt_broker_address = get_valid_user_input(prompt, is_valid_mqtt_broker_address, default=config.mqtt_broker_address)

    prompt = f"MQTT Broker Port (default: {config.mqtt_broker_port}): "
    config.mqtt_broker_port = int(get_valid_user_input(prompt, is_valid_mqtt_broker_port, default=str(config.mqtt_broker_port)))

    prompt = f"MQTT QoS Level (0, 1, or 2; default: {config.mqtt_qos}): "
    config.mqtt_qos = int(get_valid_user_input(prompt, is_valid_mqtt_qos, default=str(config.mqtt_qos)))

    prompt = f"MQTT Retain Flag (true or false; default: {config.mqtt_retain}): "
    config.mqtt_retain = get_valid_user_input(prompt, is_valid_mqtt_retain, default=str(config.mqtt_retain)).lower() == "true"

    prompt = f"Shelley Device Address (no default, Bluetooth MAC Address, example: {config.shelley_address}): "
    config.shelley_address = get_valid_user_input(prompt, is_valid_shelley_address)

    prompt = f"Sleep Interval Seconds (default: {config.sleep_interval_seconds}): "
    config.sleep_interval_seconds = int(get_valid_user_input(prompt, is_valid_sleep_interval, default=str(config.sleep_interval_seconds)))

    user_input = -1
    print("For reading types, you will select which of the following readings types you want to use. If you select a reading type that is already selected, it will be removed. Press Enter without typing anything to finish selecting.")
    while user_input or not config.reading_types: 
        prompt = f"Currently selected reading types: {list(config.reading_types.keys())}. \nEnter a reading type to add or remove (options: {list(VALID_READING_TYPES.keys())}): "
        user_input = input(prompt).strip()
        if user_input in VALID_READING_TYPES.keys():
            if user_input in config.reading_types:
                del config.reading_types[user_input]
            else:
                config.reading_types[user_input] = VALID_READING_TYPES[user_input]
        elif user_input: 
            print("Invalid reading type. Please enter one of the valid options, or press Enter to finish selecting.")
        elif not config.reading_types:
            print("You must select at least one reading type. Please enter one of the valid options.")

    #config version is not set by the user

    #Save the configuration to a file
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

            if not is_valid_station_id(config.station_id):
                return False
            if not is_valid_building_id(config.building_id):
                return False
            if not is_valid_mqtt_broker_address(config.mqtt_broker_address):
                return False
            if not is_valid_mqtt_broker_port(str(config.mqtt_broker_port)):
                return False
            if not is_valid_mqtt_qos(str(config.mqtt_qos)):
                return False
            if not is_valid_mqtt_retain(str(config.mqtt_retain)):
                return False
            if not is_valid_shelley_address(config.shelley_address):
                return False
            if not is_valid_reading_types(config.reading_types):
                return False
            if not is_valid_sleep_interval(str(config.sleep_interval_seconds)):
                return False
            if not is_valid_config_version(str(config.CONFIG_VERSION)):
                return False

            return True
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.error(f"Configuration file error: {e}")
        return False
    
def get_valid_user_input(prompt: str, validation_func, default: str | None = None) -> str:
    """Helper function to get valid user input based on a validation function.

    Args:
        prompt: The input prompt to display to the user.
        validation_func: A function that takes a string input and returns True if it's valid, False otherwise.
        default: The default value to return if the user doesn't provide any input.

    Returns:
        A valid user input string that passes the validation function.
    """
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        elif default is not None and user_input == "":
            return default
        print("Invalid input. Please try again.")
    
def is_valid_station_id(station_id: str) -> bool:
    """Validates the station ID input by the user. 
    A valid station ID is a non-empty string that does not contain spaces and starts with 'station_'.
    Args:
        station_id: The station ID string to validate.

    Returns:
        bool: True if the station ID is valid, False otherwise.
    """
    if " " not in station_id and station_id.startswith("station_") and len(station_id) > len("station_"):
        return True
    return False

def is_valid_building_id(building_id: str) -> bool:
    """Validates the building ID input by the user. 
    A valid building ID is a non-empty string that does not contain spaces and starts with 'building_'.
    Args:
        building_id: The building ID string to validate.

    Returns:
        bool: True if the building ID is valid, False otherwise.
    """
    if " " not in building_id and building_id.startswith("building_"):
        return True
    return False

def is_valid_mqtt_broker_address(address: str) -> bool:
    """Validates the MQTT broker address input by the user. 
    A valid address is a non-empty string that is either a valid IP address or hostname.

    Args:
        address: The MQTT broker address string to validate.
    
    Returns:
        bool: True if the MQTT broker address is valid, False otherwise.
    """
    # Basic validation for hostname format
    if 0 < len(address) < 253 and " " not in address:
        return True
    # Basic validation for IP address format
    parts = address.split(".")
    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return True
    return False

def is_valid_mqtt_broker_port(port: str) -> bool:
    """Validates the MQTT broker port input by the user. 
    A valid port is an integer between 1 and 65565.

    Args:
        port_str: The MQTT broker port string to validate.
    
    Returns:
        bool: True if the MQTT broker port is valid, False otherwise.
    """
    if port.isdigit() and 1 <= int(port) <= 65565:
        return True
    return False

def is_valid_mqtt_qos(qos: str) -> bool:
    """Validates the MQTT QoS level input by the user. 
    A valid QoS level is an integer value of 0, 1, or 2.

    Args:
        qos_str: The MQTT QoS level string to validate.
    
    Returns:
        bool: True if the MQTT QoS level is valid, False otherwise.
    """
    if qos.isdigit() and int(qos) in [0, 1, 2]:
        return True
    return False

def is_valid_mqtt_retain(retain: str) -> bool:
    """Validates the MQTT retain flag input by the user. 
    A valid retain flag is a string value of "true" or "false" (case insensitive).

    Args:
        retain_str: The MQTT retain flag string to validate.
    
    Returns:
        bool: True if the MQTT retain flag is valid, False otherwise.
    """
    if retain.lower() in ["true", "false"]:
        return True
    return False

def is_valid_shelley_address(address: str) -> bool:
    """Validates the Shelley device address input by the user. 
    A valid address is a non-empty string that matches the format of a Bluetooth MAC address.

    Args:
        address: The Shelley device address string to validate.
    
    Returns:
        bool: True if the Shelley device address is valid, False otherwise.
    """
    if not address:
        return False
    parts = address.split(":")
    if len(parts) != 6:
        return False
    for part in parts:
        if len(part) != 2 or not all(c in "0123456789ABCDEFabcdef" for c in part):
            return False
    return True

def is_valid_reading_types(reading_types: dict) -> bool:
    """Validates the reading types input by the user. 
    Valid reading types is a dictionary where keys are keys that can be polled from the 
    Shelly status response (like "current", "power", "voltage") 
    and values are their corresponding units (like "amps", "watts", "volts").

    Args:
        reading_types: The reading types dictionary to validate.
    
    Returns:
        bool: True if the reading types are valid, False otherwise.
    """
    if not reading_types:
        return False
    for key, value in reading_types.items():
        if key not in VALID_READING_TYPES or value != VALID_READING_TYPES[key]:
            return False
    return True

def is_valid_sleep_interval(interval: str) -> bool:
    """Validates the sleep interval input by the user. 
    A valid sleep interval is an integer value greater than or equal to 1.

    Args:
        interval_str: The sleep interval string to validate.
    
    Returns:
        bool: True if the sleep interval is valid, False otherwise.
    """
    if interval.isdigit() and int(interval) >= 1:
        return True
    return False

def is_valid_config_version(version: str) -> bool:
    """Validates the configuration version input by the user. 
    A valid configuration version is an integer value greater than or equal to 1.

    Args:
        version: The configuration version string to validate.
    
    Returns:
        bool: True if the configuration version is valid, False otherwise.
    """
    if version.isdigit() and int(version) >= 1:
        return True
    return False