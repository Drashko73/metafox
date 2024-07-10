import requests

from time import sleep

def main() -> None:
    
    config = {
        "job_name": "Boston Housing",
        "data_source": "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
        "target_variable": "medv",
        "problem_type": "regression",
        "metrics": [],
        "random_state": 42,
        "model": "",
        "max_iterations": 1000,
        "timeout": 1,
        "automl_library": "tpot"
    }
    
    # Create an AutoML job
    url = "http://localhost:8000/metafox/api/v1/automl/job/create"
    response = requests.post(url, json = config)
    
    job_id = response.json()["job_id"]
    if job_id == None:
        print("Job creation failed")
        return
    
    # Start the AutoML job
    body = {
        "job_id": job_id
    }
    url = "http://localhost:8000/metafox/api/v1/automl/job/start"
    response1 = requests.post(url, json = body)
    
    celery_job_id = response1.json()["job_id"]
    if celery_job_id == None:
        print("Job start failed")
        return
    
    # Retrieve the status of the AutoML job until it is finished or failed
    url = f"http://localhost:8000/metafox/api/v1/automl/job/{celery_job_id}/status"
    response2 = requests.get(url)
    
    while response2.json()["status"] != "SUCCESS":
        if response2.json()["status"] == "FAILURE":
            print("Task failed.")
            return
        
        print("Task is still running. Current status: " + response2.json()["status"])
        sleep(10)
        response2 = requests.get(url)
    
    # Retrieve the result of the AutoML job
    url = f"http://localhost:8000/metafox/api/v1/automl/job/{celery_job_id}/result"
    response3 = requests.get(url)
    
    print(response3.json())
    
if __name__ == "__main__":
    main()