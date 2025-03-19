import requests
from digitalbrainsdk.api.api.core import Core
from digitalbrainsdk.config import ConfigManager
import os
import json

class SWCApi:
    def __init__(self, environment="PRODUCTION", species="mouse", project="pfc"):
        self.core = Core(environment)
        self.neuron_data = None
        self.neuron_type = None
        self.species = species
        self.project = project
        cache_dir_name = ConfigManager().get("CACHE", "CacheDir")
        self.cache_dir = None
        if not self.cache_dir:
            self.cache_dir = os.path.join(os.getcwd(), cache_dir_name, "swc")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def set_project(self, project):
        self.project = project

    def get_swc(self, id=None, file=None):
        if not self.neuron_data:
            self._download_neuron_data()
        target_neuron = None
        if self.neuron_data:
            if id:
                target_neuron = self._get_swc_by_id(id)
            elif file:
                target_neuron = self._get_swc_by_file(file)

        # cache file path
        file_path = f"{self.cache_dir}/{target_neuron['file']}"

        # if exists return file path
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return file_path

        # if not exists download and save
        if target_neuron:
            content = self.download_swc(target_neuron)
            with open(file_path, "wb") as f:
                f.write(content)
            return file_path
        return None

    def _download_neuron_data(self):
        # Check if species and project are valid
        if self.species and self.project:
            # Define the cache file path
            cache_file_path = (
                f"{self.cache_dir}/{self.species}_{self.project}_neuron.json"
            )

            # Check if the cache file exists
            if os.path.exists(cache_file_path):
                print(f"Loading cached data from {cache_file_path}")
                # Load the cached data
                with open(cache_file_path, "r") as cache_file:
                    cached_data = json.load(cache_file)
                    self.neuron_data = cached_data["neuron_data"]
                    self.neuron_type = cached_data["neuron_type"]
            else:
                # Fetch the data from the URL
                url = f"{self.core.base_url}/info/{self.species}/{self.project if self.project != 'pfc' else ''}/{self.species}.neuron.info.json"
                response = requests.get(url)
                self.neuron_data = response.json()["neuron_data"]
                self.neuron_type = response.json()["neuron_type"]

                # Cache the data to a JSON file
                with open(cache_file_path, "w") as cache_file:
                    json.dump(
                        {
                            "neuron_data": self.neuron_data,
                            "neuron_type": self.neuron_type,
                        },
                        cache_file,
                    )

    def _get_swc_by_id(self, id):
        # TODO
        # check if id is valid
        if self.neuron_data and id in self.neuron_data:
            return self.neuron_data[id]
        return None

    def _get_swc_by_file(self, file):
        # TODO
        # check if file is valid
        if self.neuron_data:
            for _, neuron in self.neuron_data.items():
                if neuron["file"] == file:
                    return neuron
        return None

    def download_swc(self, neuron):
        url = self._get_swc_download_url(neuron)
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
        return None

    def _get_swc_download_url(self, neuron):
        base_url = self.core.base_url + "/info/mouse"
        if self.project == "pfc":
            return f"{base_url}/pfc_neuron_download/{neuron['file'][:-4]}_reg.swc"
        elif self.project == "hy":
            return f"{base_url}/hy/hy_neuron_download/{neuron['file']}"
        elif self.project == "hipp":
            return f"{base_url}/hipp/hipp_neuron_download/{neuron['file']}"
        elif self.project == "pvh_oxt":
            return f"{base_url}/pvh_oxt/pvh_oxt_neuron_download/{neuron['file']}"
        elif self.project == "cea":
            return f"{base_url}/cea/pvh_oxt_neuron_download/{neuron['file']}"
        else:
            return None

    def get_projects(self, species):
        if species == "mouse":
            return ["pfc", "hy", "hipp", "pvh_oxt", "cea"]
        elif species == "fish":
            return ["ei"]
        else:
            return None

    def download_swc_by_project(self):        
        if not self.neuron_data:
            self._download_neuron_data()
        try:
            for _, neuron in self.neuron_data.items():
                    os.makedirs(f"{self.cache_dir}/{self.project}", exist_ok=True)
                    file_path = f"{self.cache_dir}/{self.project}/{neuron['file']}"
                    if os.path.exists(file_path):
                        print(f"File already exists: {file_path}")
                    else:    
                        content = self.download_swc(neuron)
                        with open(file_path, "wb") as f:
                            f.write(content)
            return f"{self.project} swc files downloaded in path: {self.cache_dir}/{self.project}"
        except Exception as e:
            print(f"Error downloading swc: {e}")
        return None    
