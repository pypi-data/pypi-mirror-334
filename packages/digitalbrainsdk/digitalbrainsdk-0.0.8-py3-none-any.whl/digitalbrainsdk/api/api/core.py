from digitalbrainsdk.config import ConfigManager


class Core:
    def __init__(self, environment="PRODUCTION"):
        self.environment = environment
        self.base_url = self._get_base_url()

    def _get_base_url(self):
        return ConfigManager().get(self.environment, "AppSRV")
     
    def get_environment(self):
        return self.environment

