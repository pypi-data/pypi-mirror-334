import unittest
from digitalbrainsdk.api.analyze.analyze_api import AnalyzeApi

class TestDigitalBrain(unittest.TestCase):
    def setUp(self):
        self.analyze_api=AnalyzeApi()
    
    def test_nrrd_download(self):
        nrrd_path = self.analyze_api.download_nrrd()
        self.assertIsNotNone(nrrd_path)
    


if __name__ == '__main__':
    unittest.main()