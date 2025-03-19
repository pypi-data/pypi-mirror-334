import unittest
from digitalbrainsdk.api.queries.region_api import RegionApi

class TestDigitalBrain(unittest.TestCase):
    def setUp(self):
        self.region_api=RegionApi(environment="DEBUG")
    
    def test_region_info_download(self):
        self.region_api._download_region_data()
        self.assertIsNotNone(self.region_api.region_data)
        self.assertIsNotNone(self.region_api.region_type)
    
    def test_get_region_by_id(self):
        region = self.region_api.get_region(id = "997")
        self.assertIsNotNone(region)
    
    def test_get_region_by_file(self):
        region = self.region_api.get_region(file="1.stl")
        self.assertIsNotNone(region)
    
    def test_region_tree(self):
        tree = self.region_api.region_tree()
        self.assertGreater(tree.depth(),0)


if __name__ == '__main__':
    unittest.main()