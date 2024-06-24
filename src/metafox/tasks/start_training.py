import pandas as pd

from metafox.celery import app
from metafox.ml_models.knn import KNNRegressor

from time import sleep

@app.task
def start_automl_train(link_to_data: str, target: str):
    print(f"Starting AutoML task with data: {link_to_data} and target: {target}")
    
    # Load the data
    data = pd.read_csv(link_to_data)
    X_train = data.drop(target, axis=1)
    y_train = data[target]
    
    # Train the model
    model = KNNRegressor()
    model.fit(X_train, y_train)
    
    sleep(10)   # Simulate a long-running task (10 seconds
    
    return {"message": "AutoML task completed.", "model_params": model.get_params()}