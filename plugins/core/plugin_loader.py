import importlib
import yaml
from pathlib import Path

class PluginLoader:
    def __init__(self):
        self.plugins = {}

    def load_plugin(self, plugin_dir):
        config_path = Path(plugin_dir) / 'plugin.yaml'
        with open(config_path) as f:
            config = yaml.safe_load(f)

        plugin_name = config['name']
        self.plugins[plugin_name] = config
        return config

    def get_plugin(self, name):
        return self.plugins.get(name)
