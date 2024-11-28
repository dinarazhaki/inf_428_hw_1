import numpy as np
import unittest
import os
import pandas as pd

from hw1ofanother.aggregatedUserThreatScore import generate_department_data


def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def save_department_data_to_csv(department_name, data, case_name):
    os.makedirs("csvs", exist_ok=True)
    file_path = os.path.join("csvs", f"{case_name}_{department_name}.csv")

    df = pd.DataFrame(data, columns=["Threat_Score"])
    df.to_csv(file_path, index=False)
    print(f"Data for {department_name} saved to {file_path}")

def calculate_aggregated_threat_score(department_data):
    total_users = sum(len(scores) for scores in department_data.values())
    total_sum = sum(np.sum(scores) for scores in department_data.values())

    aggregated_score = total_sum / total_users if total_users > 0 else 0
    return min(max(aggregated_score, 0), 90)




def generate_test_case_csv(departments=['Engineering', 'Marketing', 'Finance', 'HR', 'Science']):
    np.random.seed(0)

    for dept in departments:
        data = generate_random_data(mean=40, variance=10, num_samples=50)
        save_department_data_to_csv(dept, data, "case_1")

        # one department has high threat scores
    for dept in departments[:-1]:  # Exclude the last department (Dept5)
        data = generate_random_data(mean=20, variance=5, num_samples=50)
        save_department_data_to_csv(dept, data, "case_2")
    high_data = generate_random_data(mean=80, variance=5, num_samples=50)  # High threat scores for Dept5
    save_department_data_to_csv(departments[-1], high_data, "case_2")

    # high outliers in one department
    for dept in departments[:-1]:  # Exclude the last department (Dept5)
        data = generate_random_data(mean=20, variance=5, num_samples=50)
        save_department_data_to_csv(dept, data, "case_3")

    outlier_data = np.concatenate([generate_random_data(mean=20, variance=5, num_samples=45),
                                   np.random.randint(80, 91, 5)])
    save_department_data_to_csv(departments[-1], outlier_data, "case_3")

    # different number of users across departments
    save_department_data_to_csv(departments[0], generate_random_data(mean=30, variance=5, num_samples=20), "case_4")
    save_department_data_to_csv(departments[1], generate_random_data(mean=50, variance=10, num_samples=80), "case_4")
    save_department_data_to_csv(departments[2], generate_random_data(mean=40, variance=5, num_samples=100), "case_4")
    save_department_data_to_csv(departments[3], generate_random_data(mean=35, variance=10, num_samples=50), "case_4")
    save_department_data_to_csv(departments[4], generate_random_data(mean=45, variance=15, num_samples=30), "case_4")


generate_test_case_csv()


def read_data_from_csv(filename):
    try:
        file_path = f"csvs/{filename}"
        df = pd.read_csv(file_path)
        return df["Threat_Score"].tolist()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []


class TestAggregatedThreatScore(unittest.TestCase):

    def setUp(self):
        np.random.seed(0)

    def populate_data_from_csv(self, case_name):
        department_data = {f"Dept{i}": [] for i in range(1, 6)}

        for dept_num in range(1, 6):
            csv_file = f"{case_name}_Dept{dept_num}.csv"
            department_name = f"Dept{dept_num}"
            threat_scores = read_data_from_csv(csv_file)
            department_data[department_name] = threat_scores

        return department_data

    def test_aggregated_threat_case_1(self):
        department_data = self.populate_data_from_csv("case_1")
        result = calculate_aggregated_threat_score(department_data)
        print(f"Calculated Aggregated Threat Score: {result}")
        self.assertTrue(35 <= result <= 45)

    def test_aggregated_threat_case_2(self):
        department_data = self.populate_data_from_csv("case_2")
        result = calculate_aggregated_threat_score(department_data)
        print(f"Calculated Aggregated Threat Score: {result}")
        for dept, scores in department_data.items():
            print(f"{dept}: {scores[:5]}...")
        self.assertTrue(30 <= result <= 45)

    def test_aggregated_threat_case_3(self):
        department_data = self.populate_data_from_csv("case_3")
        result = calculate_aggregated_threat_score(department_data)
        print(f"Calculated Aggregated Threat Score: {result}")
        for dept, scores in department_data.items():
            print(f"{dept}: {scores[:5]}...")
        self.assertTrue(20 <= result <= 40)

    def test_aggregated_threat_case_4(self):
        department_data = self.populate_data_from_csv("case_4")
        result = calculate_aggregated_threat_score(department_data)
        print(f"Calculated Aggregated Threat Score: {result}")
        self.assertTrue(30 <= result <= 60)


if __name__ == "__main__":
    department_data = generate_department_data()
    unittest.main()
