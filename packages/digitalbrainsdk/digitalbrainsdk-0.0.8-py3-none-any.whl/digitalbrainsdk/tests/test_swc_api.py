import unittest
from digitalbrainsdk.api.queries.swc_api import SWCApi

class TestSWCApi(unittest.TestCase):
    
    def setUp(self):
        self.swc_api = SWCApi(species='mouse')

    def test_species(self):
        self.swc_api = SWCApi(species='mouse')
        self.assertEqual(self.swc_api.species, "mouse")
    
    def test_download_neuron_data(self):
        self.swc_api._download_neuron_data()
        self.assertIsNotNone(self.swc_api.neuron_data)
        self.assertIsNotNone(self.swc_api.neuron_type)
    
    def test_get_swc_by_id(self):
        self.swc_api._download_neuron_data()
        self.assertIsNotNone(self.swc_api._get_swc_by_id("1"))

    def test_get_swc_by_file(self):
        self.swc_api._download_neuron_data()
        self.assertIsNotNone(self.swc_api._get_swc_by_file("17099_002.swc"))

    def test_download_swc(self):
        self.swc_api._download_neuron_data()
        neuron = self.swc_api._get_swc_by_id("1")
        self.assertIsNotNone(self.swc_api.download_swc(neuron))
    
    def test_get_swc(self):
        result = self.swc_api.get_swc(id="1")
        self.assertIsNotNone(result)
    
    def test_project(self):
        self.swc_api = SWCApi(species='mouse', project='hipp')
        neuron = self.swc_api.get_swc(id="1")
        self.assertIsNotNone(neuron)
    
    def test_get_projects(self):
        projects = self.swc_api.get_projects(species='mouse')
        self.assertEqual(projects, ["pfc", "hy", "hipp", "pvh_oxt", "cea"])

    def test_swc_project_download(self):
        self.swc_api.set_project("hy")
        swcs_path = self.swc_api.download_swc_by_project()
        self.assertIsNotNone(swcs_path)   

if __name__ == '__main__':
    unittest.main()