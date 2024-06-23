from celery import Celery
import pandas as pd

from sklearn.neighbors import KNeighborsRegressor

from time import sleep

app = Celery()
app.config_from_object('celeryconfig')

@app.task
def start_automl(link_to_data: str, target: str) -> dict:
    print("Starting AutoML")
    
    df = pd.read_csv(link_to_data)
    
    X_train = df.drop(target, axis=1)
    y_train = df[target]
    
    model = KNeighborsRegressor()
    model.fit(X_train, y_train)
    
    return model.get_params()