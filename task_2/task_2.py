import numpy as np

def generate_random_data(mean, variance, num_samples):
    if variance == 0:
        return np.full(num_samples, mean)
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def calculate_aggregated_threat(department_data, importance_weights):

    weighted_sum = 0
    total_importance = sum(importance_weights)

    for scores, weight in zip(department_data, importance_weights):
        department_average = np.mean(scores)
        weighted_sum += department_average * weight

    aggregated_score = weighted_sum / total_importance
    return min(max(aggregated_score, 0), 90)


