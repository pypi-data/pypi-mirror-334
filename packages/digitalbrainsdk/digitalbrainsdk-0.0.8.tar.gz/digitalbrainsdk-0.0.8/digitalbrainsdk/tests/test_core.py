import unittest
from digitalbrainsdk import DigitalBrain

class TestDigitalBrain(unittest.TestCase):

    def setUp(self):
        self.brain = DigitalBrain()
        print("setUp",self.brain.get_environment())

    def test_environment(self):
        self.brain = DigitalBrain(environment='DEBUG')
        self.assertEqual(self.brain.core.get_environment(), "DEBUG")

    # def test_process_data(self):
    #     data = "sample data"
    #     self.brain.initialize()
    #     result = self.brain.process_data(data)
    #     self.assertEqual(result, "processed sample data")

    # def test_get_results(self):
    #     self.brain.initialize()
    #     self.brain.process_data("sample data")
    #     results = self.brain.get_results()
    #     self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()