
import requests
import time

def main():

    url = "http://localhost:8000/automl/start"
    payload = {
        "link_to_data": "data/Boston_dataset_Train_data.csv",
        "target": "medv"
    }

    response = requests.post(url, json = payload)
    
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        print(f"AutoML task started with task ID: {task_id}")
    else:
        print(f"Failed to start AutoML task. Status code: {response.status_code}")
        print(response.text)

    url_result = f"http://localhost:8000/automl/result/{task_id}"
    while True:
        response_result = requests.get(url_result)
        if response_result.status_code == 200:
            result_json = response_result.json()
            status = result_json["status"]
            if status == "SUCCESS":
                model = result_json["result"]
                print("AutoML task completed successfully.")
                print("Fitted Model:", model)
                break
            elif status == "PENDING" or status == "PROCESSING":
                print("AutoML task still processing...")
            else:
                print(f"AutoML task failed with status: {status}")
                break
        else:
            print(f"Failed to fetch AutoML task result. Status code: {response_result.status_code}")
            print(response_result.text)
            break
        time.sleep(5)  # Polling interval

if __name__ == '__main__':
    main()