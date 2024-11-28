import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def calculate_aggregated_threat_score(department_data):
    total_weighted_score = 0
    total_importance = 0

    for users_count, threat_scores, importance in department_data:
        avg_score = np.mean(threat_scores)

        weighted_score = avg_score * importance
        total_weighted_score += weighted_score
        total_importance += importance

    if total_importance == 0:
        return 0
    aggregated_score = total_weighted_score / total_importance

    return np.clip(aggregated_score, 0, 90)


def generate_department_data():
    department_data = []
    departments = ['Engineering', 'Marketing', 'Finance', 'HR', 'Science']

    for i in range(5):
        num_users = np.random.randint(10, 201)
        threat_scores = generate_random_data(mean=50, variance=20, num_samples=num_users)
        importance = np.random.randint(1, 6)
        department_data.append((num_users, threat_scores, importance))

    return department_data


if __name__ == "__main__":
    department_data = generate_department_data()

    aggregated_score = calculate_aggregated_threat_score(department_data)

    print(f"Aggregated Cybersecurity Threat Score: {aggregated_score}")


class TestAggregatedThreatScore(unittest.TestCase):

    def test_generate_random_data(self):
        mean = 50
        variance = 20
        num_samples = 100
        data = generate_random_data(mean, variance, num_samples)
        self.assertTrue(np.all(data >= 0) and np.all(data <= 90))

    def test_calculate_aggregated_threat_score(self):
        department_data = [
            (100, np.random.randint(0, 90, 100), 2),
            (150, np.random.randint(0, 90, 150), 3),
            (200, np.random.randint(0, 90, 200), 1),
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_calculate_aggregated_threat_score_empty(self):
        department_data = []
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertEqual(aggregated_score, 0)

    def test_calculate_aggregated_threat_score_single_department(self):
        department_data = [
            (100, np.random.randint(0, 90, 100), 3)
        ]
        aggregated_score = calculate_aggregated_threat_score(department_data)
        self.assertTrue(0 <= aggregated_score <= 90)


if __name__ == "__main__":
    unittest.main()