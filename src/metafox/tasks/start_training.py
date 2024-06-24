import pandas as pd

from metafox.celery import app
from metafox.ml_models.knn import KNNRegressor

@app.task
def start_automl_train(link_to_data: str, target: str):
    
    # Load the data
    data = pd.read_csv(link_to_data)
    X_train = data.drop(target, axis=1)
    y_train = data[target]
    
    # Train the model
    model = KNNRegressor()
    model.fit(X_train, y_train)
    
    result = model.get_params()
    
    return {"message": "AutoML task completed.", "model_params": result}