import unittest
import numpy as np
from task_3 import time_to_cyclic

class TestTimeToCyclic(unittest.TestCase):

    def test_midnight(self):
        sin_time, cos_time = time_to_cyclic(0)
        self.assertAlmostEqual(sin_time, 0, places=5)
        self.assertAlmostEqual(cos_time, 1, places=5)

    def test_noon(self):
        sin_time, cos_time = time_to_cyclic(12)
        self.assertAlmostEqual(sin_time, 0, places=5)
        self.assertAlmostEqual(cos_time, -1, places=5)

    def test_six_am(self):
        sin_time, cos_time = time_to_cyclic(6)
        self.assertAlmostEqual(sin_time, 1, places=5)
        self.assertAlmostEqual(cos_time, 0, places=5)

    def test_six_pm(self):
        sin_time, cos_time = time_to_cyclic(18)
        self.assertAlmostEqual(sin_time, -1, places=5)
        self.assertAlmostEqual(cos_time, 0, places=5)

    def test_near_midnight_circularity(self):
        sin_time_23, cos_time_23 = time_to_cyclic(23)
        sin_time_1, cos_time_1 = time_to_cyclic(1)
        distance = np.sqrt((sin_time_23 - sin_time_1) ** 2 + (cos_time_23 - cos_time_1) ** 2)
        self.assertAlmostEqual(distance, 0, delta=0.6)

if __name__ == "__main__":
    unittest.main()
