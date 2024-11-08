import unittest
import numpy as np
from task_2 import generate_random_data, calculate_aggregated_threat


class TestAggregatedThreatScore(unittest.TestCase):

    def setUp(self):
        np.random.seed(0)

    def test_aggregated_threat_basic_case(self):
        department_data = [
            generate_random_data(mean=40, variance=10, num_samples=50),
            generate_random_data(mean=40, variance=10, num_samples=50),
            generate_random_data(mean=40, variance=10, num_samples=50),
            generate_random_data(mean=40, variance=10, num_samples=50),
            generate_random_data(mean=40, variance=10, num_samples=50)
        ]
        importance_weights = [1, 1, 1, 1, 1]
        result = calculate_aggregated_threat(department_data, importance_weights)

        self.assertAlmostEqual(result, 40, delta=5)

    def test_aggregated_threat_different_importance(self):
        department_data = [
            generate_random_data(mean=30, variance=10, num_samples=100),
            generate_random_data(mean=60, variance=10, num_samples=150),
            generate_random_data(mean=20, variance=5, num_samples=75),
            generate_random_data(mean=70, variance=15, num_samples=120),
            generate_random_data(mean=50, variance=10, num_samples=90)
        ]
        importance_weights = [1, 5, 1, 3, 2]
        result = calculate_aggregated_threat(department_data, importance_weights)

        self.assertTrue(50 <= result <= 70)

    def test_aggregated_threat_outliers(self):
        department_data = [
            generate_random_data(mean=20, variance=5, num_samples=50),
            generate_random_data(mean=90, variance=0, num_samples=10),
            generate_random_data(mean=30, variance=5, num_samples=60),
            generate_random_data(mean=40, variance=10, num_samples=100),
            generate_random_data(mean=25, variance=5, num_samples=80)
        ]
        importance_weights = [1, 1, 1, 1, 1]
        result = calculate_aggregated_threat(department_data, importance_weights)

        self.assertTrue(30 <= result <= 60)

    def test_aggregated_threat_all_low_scores(self):
        department_data = [
            generate_random_data(mean=5, variance=2, num_samples=60),
            generate_random_data(mean=10, variance=3, num_samples=40),
            generate_random_data(mean=7, variance=2, num_samples=50),
            generate_random_data(mean=8, variance=1, num_samples=55),
            generate_random_data(mean=6, variance=2, num_samples=45)
        ]
        importance_weights = [2, 2, 2, 2, 2]
        result = calculate_aggregated_threat(department_data, importance_weights)

        self.assertTrue(5 <= result <= 10)

    def test_aggregated_threat_high_importance_on_low_score(self):
        department_data = [
            generate_random_data(mean=5, variance=1, num_samples=50),  # Low score
            generate_random_data(mean=40, variance=10, num_samples=70),
            generate_random_data(mean=50, variance=10, num_samples=80),
            generate_random_data(mean=60, variance=10, num_samples=60),
            generate_random_data(mean=70, variance=10, num_samples=90)
        ]
        importance_weights = [5, 1, 1, 1, 1]
        result = calculate_aggregated_threat(department_data, importance_weights)

        self.assertTrue(10 <= result <= 30)


if __name__ == "__main__":
    unittest.main()

