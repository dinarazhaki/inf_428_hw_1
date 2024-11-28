import numpy as np
from task_2 import generate_random_data, save_department_data_to_csv


def generate_test_case_csv():
    np.random.seed(0)

    #all departments have similar threat scores
    for i in range(1, 6):
        data = generate_random_data(mean=40, variance=10, num_samples=50)
        save_department_data_to_csv(f"Dept{i}", data, "case_1")

    #one department has high threat scores
    for i in range(1, 5):
        data = generate_random_data(mean=20, variance=5, num_samples=50)
        save_department_data_to_csv(f"Dept{i}", data, "case_2")
    high_data = generate_random_data(mean=80, variance=5, num_samples=50)
    save_department_data_to_csv("Dept5", high_data, "case_2")

    #high outliers in one department
    for i in range(1, 5):
        data = generate_random_data(mean=20, variance=5, num_samples=50)
        save_department_data_to_csv(f"Dept{i}", data, "case_3")

    outlier_data = np.concatenate([generate_random_data(mean=20, variance=5, num_samples=45),
                                   np.random.randint(80, 91, 5)])
    save_department_data_to_csv("Dept5", outlier_data, "case_3")

    #different number of users across departments
    save_department_data_to_csv("Dept1", generate_random_data(mean=30, variance=5, num_samples=20), "case_4")
    save_department_data_to_csv("Dept2", generate_random_data(mean=50, variance=10, num_samples=80), "case_4")
    save_department_data_to_csv("Dept3", generate_random_data(mean=40, variance=5, num_samples=100), "case_4")
    save_department_data_to_csv("Dept4", generate_random_data(mean=35, variance=10, num_samples=50), "case_4")
    save_department_data_to_csv("Dept5", generate_random_data(mean=45, variance=15, num_samples=30), "case_4")


generate_test_case_csv()
