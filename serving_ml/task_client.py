import asyncio
from typing import Any, Dict
import requests
from models import TrainingData
from app import train

import pandas as pd
TRAIN_FILEPATH = "C:\\Users\\Ceramo\\Desktop\\MetaFOX\\MetaFOX-Demo\\serving_ml\\assets\\Churn_Modelling_Train_data.csv"

# Function to read data from CSV file and format it as TrainingData
def read_and_format_csv(csv_filepath: str) -> TrainingData:
    df = pd.read_csv(csv_filepath)
    data = df.to_dict(orient='records')
    exited = df['Exited'].tolist()
    return TrainingData(data=data, Exited=exited)


def train_task(data):
    base_uri = r'http://127.0.0.1:8000'
    train_task_uri = base_uri + '/churn/train'
    # print(data)
    task = requests.post(train_task_uri, json=data)
    # print(task)

    task_id = task.json()['task_id']
    print(f'Training task created with ID: {task_id}')
    # task = train_model.delay(data, 'Exited')
    
    # task_id = task.task_id
    return task_id

async def main():
    formatted_data = read_and_format_csv(TRAIN_FILEPATH)
    task = await train(formatted_data)  # Await the coroutine
    print(f'Training task created with ID: {task["task_id"]}')

if __name__ == '__main__':
    asyncio.run(main())  # Run the async function using asyncio.run()