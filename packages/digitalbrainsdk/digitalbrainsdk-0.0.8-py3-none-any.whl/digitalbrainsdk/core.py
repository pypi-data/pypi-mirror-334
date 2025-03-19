from digitalbrainsdk.api.api.core import Core

class DigitalBrain:
    def __init__(self, environment='PRODUCTION'):
        self.core = Core(environment)

    def get_environment(self):
        return self.core.get_environment()