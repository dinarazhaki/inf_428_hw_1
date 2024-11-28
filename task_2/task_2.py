import numpy as np
import pandas as pd
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import matplotlib.pyplot as plt

def generate_random_data(mean, variance, num_samples):
    if variance == 0:
        return np.full(num_samples, mean)
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def save_department_data_to_csv(department_name, data, case_name):
    os.makedirs("task_2", exist_ok=True)
    file_path = os.path.join("task_2", f"{case_name}_{department_name}.csv")

    df = pd.DataFrame(data, columns=["Threat_Score"])
    df.to_csv(file_path, index=False)
    print(f"Data for {department_name} saved to {file_path}")


es = Elasticsearch("http://localhost:9200")

def create_index():
    index_name = "threat_scores"
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    mappings = {
        "mappings": {
            "properties": {
                "case_name": {"type": "keyword"},
                "department_name": {"type": "keyword"},
                "threat_score": {"type": "integer"}
            }
        }
    }
    es.indices.create(index=index_name, body=mappings)
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mappings)
        print(f"Index {index_name} created successfully.")
    else:
        print(f"Index {index_name} already exists.")
def populate_index_from_csv(case_name):
    index_name = "threat_scores"
    actions = []
    for dept_num in range(1, 6):
        csv_file = f"task_2/{case_name}_Dept{dept_num}.csv"
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            for score in df["Threat_Score"]:
                actions.append({
                    "_index": index_name,
                    "_source": {
                        "case_name": case_name,
                        "department_name": f"Dept{dept_num}",
                        "threat_score": score
                    }
                })
    if actions:
        bulk(es, actions)
        print(f"Data for case '{case_name}' populated into index '{index_name}'.")

def calculate_aggregated_threat_from_es(case_name):
    index_name = "threat_scores"

    query = {
        "size": 0,
        "query": {"term": {"case_name": case_name}},
        "aggs": {
            "avg_threat_score": {
                "avg": {"field": "threat_score"}
            }
        }
    }

    response = es.search(index=index_name, body=query)
    avg_score = response["aggregations"]["avg_threat_score"]["value"]
    return min(max(avg_score, 0), 90) if avg_score is not None else 0

def calculate_aggregated_threat(department_data):
    total_users = sum(len(scores) for scores in department_data.values())
    total_sum = sum(np.sum(scores) for scores in department_data.values())

    aggregated_score = total_sum / total_users if total_users > 0 else 0
    return min(max(aggregated_score, 0), 90)



