# Plugin Development Guide

## Creating a Plugin

1. Create plugin directory under `plugins/examples/`
2. Add `plugin.yaml` configuration
3. Implement plugin class extending `Plugin`
4. Add to plugin configuration

## Example
```python
from plugins.core.plugin_base import Plugin

class MyPlugin(Plugin):
    def initialize(self):
        pass

    def process(self, data):
        return data
```
