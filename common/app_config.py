"""Configuration loader with plugin support"""
import configparser
import os
from pathlib import Path
import yaml

class AppConfig:
    """Load and manage application configuration with plugin support"""

    def __init__(self, config_file='appconfig.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.plugins = {}
        self.load()

    def load(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        self.config.read(self.config_file)

    def load_plugin_config(self, plugin_name, config_path):
        """Load plugin configuration from YAML"""
        try:
            with open(config_path, 'r') as f:
                plugin_config = yaml.safe_load(f)
                self.plugins[plugin_name] = plugin_config
                return plugin_config
        except Exception as e:
            print(f"Error loading plugin config: {e}")
            return None

    def get(self, section, key, fallback=None):
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=None):
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=None):
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)

    def get_plugin_config(self, plugin_name):
        """Get plugin configuration"""
        return self.plugins.get(plugin_name)

    def sections(self):
        """Get all configuration sections"""
        return self.config.sections()

    def items(self, section):
        """Get all items in a section"""
        return self.config.items(section)

# Global config instance
_config = None

def get_config(config_file='appconfig.ini'):
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = AppConfig(config_file)
    return _config
