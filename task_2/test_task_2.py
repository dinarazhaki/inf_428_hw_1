import unittest
import pandas as pd
import numpy as np
from task_2 import calculate_aggregated_threat, create_index, populate_index_from_csv, calculate_aggregated_threat_from_es

def read_data_from_csv(csv_file):
    try:
        file_path = f"task_2/{csv_file}"
        df = pd.read_csv(file_path)
        return df["Threat_Score"].tolist()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []


class TestElasticsearchAggregatedThreatScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_index()

    def populate_data_in_es(self, case_name):
        populate_index_from_csv(case_name)

    def test_aggregated_threat_es_case_1(self):
        case_name = "case_1"
        self.populate_data_in_es(case_name)
        result = calculate_aggregated_threat_from_es(case_name)
        self.assertTrue(35 <= result <= 45)

    def test_aggregated_threat_es_case_2(self):
        case_name = "case_2"
        self.populate_data_in_es(case_name)
        result = calculate_aggregated_threat_from_es(case_name)
        self.assertTrue(30 <= result <= 45)

    def test_aggregated_threat_es_case_3(self):
        case_name = "case_3"
        self.populate_data_in_es(case_name)
        result = calculate_aggregated_threat_from_es(case_name)
        self.assertTrue(20 <= result <= 40)

    def test_aggregated_threat_es_case_4(self):
        case_name = "case_4"
        self.populate_data_in_es(case_name)
        result = calculate_aggregated_threat_from_es(case_name)
        self.assertTrue(30 <= result <= 60)

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

    #all departments have similar threat scores
    def test_aggregated_threat_case_1(self):
        department_data = self.populate_data_from_csv("case_1")
        result = calculate_aggregated_threat(department_data)
        self.assertTrue(35 <= result <= 45)

    #one department has high threat scores
    def test_aggregated_threat_case_2(self):
        department_data = self.populate_data_from_csv("case_2")
        result = calculate_aggregated_threat(department_data)
        for dept, scores in department_data.items():
            print(f"{dept}: {scores[:5]}...")
        self.assertTrue(30 <= result <= 45)

    #high outliers in one department
    def test_aggregated_threat_case_3(self):
        department_data = self.populate_data_from_csv("case_3")
        result = calculate_aggregated_threat(department_data)
        for dept, scores in department_data.items():
            print(f"{dept}: {scores[:5]}...")
        self.assertTrue(20 <= result <= 40)

    #different number of users across departments
    def test_aggregated_threat_case_4(self):
        department_data = self.populate_data_from_csv("case_4")
        result = calculate_aggregated_threat(department_data)
        self.assertTrue(30 <= result <= 60)

if __name__ == "__main__":
    unittest.main()
