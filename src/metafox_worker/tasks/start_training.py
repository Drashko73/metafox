import pandas as pd

from metafox_worker.main import app

@app.task
def start_automl_train(config: object) -> dict:
    
    # Load the data
    data = pd.read_csv(config["data_source"])
    X_train = data.drop(config["target_variable"], axis=1)
    y_train = data[config["target_variable"]]
    
    if config["automl_library"] == "tpot":
        from metafox_worker.automl.tpot_regressor import TPOTRegressorWrapper
        
        model = TPOTRegressorWrapper(
            random_state=config["random_state"],
            max_time_mins=config["timeout"]
        )
        
        model.fit(X_train, y_train)
        result = model.get_model_params()
        
    else:
        raise ValueError("Invalid AutoML library specified.")
    
    return {"message": "AutoML task completed.", "model": result}