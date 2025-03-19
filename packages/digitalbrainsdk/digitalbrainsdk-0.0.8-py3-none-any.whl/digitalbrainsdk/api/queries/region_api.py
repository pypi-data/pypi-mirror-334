import requests
from digitalbrainsdk.api.api.core import Core
from digitalbrainsdk.config import ConfigManager
import os
from treelib import Tree
from IPython.display import display, Markdown
import json


class RegionApi:
    def __init__(self, environment="PRODUCTION", species="mouse"):
        self.core = Core(environment)
        self.region_data = None
        self.region_type = None
        self.species = species
        cache_dir_name = ConfigManager().get("CACHE", "CacheDir")
        self.cache_dir = None
        if not self.cache_dir:
            self.cache_dir = os.path.join(os.getcwd(), cache_dir_name, "region")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_region(self, id=None, file=None):
        if not self.region_data:
            self._download_region_data()
        target_region = None
        if self.region_data:
            if id:
                target_region = self._get_region_by_id(id)
            elif file:
                target_region = self._get_region_by_file(file)
        if target_region:
            content = self._download_region(target_region)
            file_path = f"{self.cache_dir}/{target_region['file']}"
            with open(file_path, "wb") as f:
                f.write(content)
            return file_path
        return None

    def _download_region_data(self):
        # Check if species and project are valid
        if self.species:
            # Define the cache file path
            cache_file_path = (
                f"{self.cache_dir}/{self.species}_region.json"
            )

            # Check if the cache file exists
            if os.path.exists(cache_file_path):
                print(f"Loading cached data from {cache_file_path}")
                # Load the cached data
                with open(cache_file_path, "r") as cache_file:
                    cached_data = json.load(cache_file)
                    self.region_data = cached_data["region_data"]
                    self.region_type = cached_data["region_type"]
            else:
                # Fetch the data from the URL
                url = f"{self.core.base_url}/info/{self.species}/{self.species}.region.info.json"
                response = requests.get(url)
                self.region_data = response.json()["region_data"]
                self.region_type = response.json()["region_type"]

                # Cache the data to a JSON file
                with open(cache_file_path, "w") as cache_file:
                    json.dump(
                        {
                            "region_data": self.region_data,
                            "region_type": self.region_type,
                        },
                        cache_file,
                    )

    def _get_region_by_id(self, id):
        if self.region_data and id in self.region_data:
            return self.region_data[id]
        return None

    def _get_region_by_file(self, file):
        if self.region_data:
            for _, region in self.region_data.items():
                if region["file"] == file:
                    return region

    def _download_region(self, region):
        # TODO
        return f"test {region['file']}".encode()

    def _recover_tree(self, json_data, uid, tree, added_nodes):
        if uid in added_nodes:
            return tree.get_node(uid)

        item = json_data[str(uid)]
        parent_node = None
        parent_uid = item["parent_uid"]
        if parent_uid is not None:
            parent_node = self._recover_tree(
                json_data, str(parent_uid), tree, added_nodes
            )

        tree.create_node(
            identifier=str(item["uid"]),
            data={"acronym": item["acronym"], "name": item["name"]},
            parent=parent_node.identifier if parent_node else None,
        )
        added_nodes.add(uid)

        node = tree.get_node(uid)
        return node

    def region_tree(self):
        if not self.region_data:
            self._download_region_data()

        tree = Tree()
        added_nodes = set()
        for key in self.region_data.keys():
            self._recover_tree(self.region_data, str(key), tree, added_nodes)
        return tree

    def show_tree(self, tree):
        tree_structure = tree.show(stdout=False)
        display(Markdown(f"```\n{tree_structure}\n```"))
