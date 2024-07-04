import requests

from time import sleep

def main() -> None:
    
    config = {
        "name" : "Boston Housing",
        "data_source" : "https://raw.githubusercontent.com/Drashko73/datasets/master/boston_housing/housing.csv",
        "target_variable" : "medv",
        "model_type" : "regression",
        "random_state" : 42,
        "model" : "LinearRegression",
        "max_iter" : 1000,
        "timeout" : 1,
        "automl_library" : "tpot"
    }
    
    # Start the AutoML task
    url = "http://localhost:8000/metafox/v1/automl/start"
    response = requests.post(url, json = config)   # Send a POST request to the server in order to start the AutoML task
    
    # Check task status
    task_id = response.json()["task_id"]
    url = f"http://localhost:8000/metafox/v1/automl/task/{task_id}/status"
    response = requests.get(url)   # Send a GET request to the server to get the status of the AutoML task
    
    while response.json()["status"] != "SUCCESS":
        if response.json()["status"] == "FAILURE":
            print("Task failed.")
            return
        
        print("Task is still running. Current status: " + response.json()["status"])
        sleep(10)   # Wait for 10 seconds before checking the status again
        response = requests.get(url)
        
    # Get the result
    url = f"http://localhost:8000/metafox/v1/automl/task/{task_id}/result"
    response = requests.get(url)   # Send a GET request to the server to get the result of the AutoML task
    print(response.json())
    
if __name__ == "__main__":
    main()