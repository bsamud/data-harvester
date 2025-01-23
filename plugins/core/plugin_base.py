class Plugin:
    """Base class for plugins"""

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def initialize(self):
        raise NotImplementedError

    def process(self, data):
        raise NotImplementedError
