
import requests

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

if __name__ == '__main__':
    main()