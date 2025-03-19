import configparser
import pkg_resources
"""
ConfigManager is a class to manage configuration files using configparser.
Attributes:
    config_file (str): The path to the configuration file.
    config (ConfigParser): An instance of ConfigParser to handle the configuration.
Methods:
    __init__(config_file='config.ini'):
        Initializes the ConfigManager with the specified configuration file.
    load_config():
        Loads the configuration from the config file.
    get(section, option, fallback=None):
        Retrieves the value for the given section and option from the configuration.
        If the section or option does not exist, returns the fallback value.
    set(section, option, value):
        Sets the value for the given section and option in the configuration.
        If the section does not exist, it is created.
        Saves the updated configuration to the file.
    save_config():
        Writes the current configuration to the config file.
"""

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        config_path = pkg_resources.resource_filename("digitalbrainsdk", "config.ini")
        self.config.read(config_path)

    def get(self, section, option, fallback=None):
        return self.config.get(section, option, fallback=fallback)

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)