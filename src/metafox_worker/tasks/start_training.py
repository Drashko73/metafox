import pandas as pd

from metafox_worker.main import app
from metafox_worker.constants import *

@app.task
def start_automl_train(config: object) -> dict:
    
    details = config["details"]
    job_id = config["id"]
    
    # Load the data
    data = pd.read_csv(details["data_source"])
    X_train = data.drop(details["target_variable"], axis=1)
    y_train = data[details["target_variable"]]
    
    if details["automl_library"] == TPOT:
        if details["problem_type"] == "regression":
            from metafox_worker.automl.tpot_regressor import TPOTRegressorWrapper
            
            try:
                model = TPOTRegressorWrapper(
                    n_jobs=N_JOBS_TPOT,
                    memory=MEMORY_TPOT,
                    use_dask=USE_DASK_TPOT,
                    verbosity=VERBOSITY_TPOT,
                    warm_start=WARM_START_TPOT,
                    generations=details["generations"],
                    population_size=details["population_size"],
                    offspring_size=details["offspring_size"],
                    mutation_rate=details["mutation_rate"],
                    crossover_rate=details["crossover_rate"],
                    scoring=details["scoring"],
                    cv=details["cv"],
                    subsample=details["subsample"],
                    max_time_mins=details["max_time_mins"],
                    max_eval_time_mins=details["max_eval_time_mins"],
                    random_state=details["random_state"],
                    config_dict=details["config_dict"],
                    template=details["template"],
                    early_stop=details["early_stop"],
                    periodic_checkpoint_folder="metafox_worker/checkpoints/" + job_id,
                    log_file="metafox_worker/logs/" + job_id + ".log"
                )
            except Exception as e:
                return {"message": "Error occurred during TPOT initialization.", "error": str(e)}
            
            model.fit(X_train, y_train)
            result = model.get_model_params()
            
            model.export_model("metafox_worker/exported_models/" + job_id + ".py")
        else:
            from metafox_worker.automl.tpot_classifier import TPOTClassifierWrapper
            
            try:
                model = TPOTClassifierWrapper(
                    n_jobs=N_JOBS_TPOT,
                    memory=MEMORY_TPOT,
                    use_dask=USE_DASK_TPOT,
                    verbosity=VERBOSITY_TPOT,
                    warm_start=WARM_START_TPOT,
                    generations=details["generations"],
                    population_size=details["population_size"],
                    offspring_size=details["offspring_size"],
                    mutation_rate=details["mutation_rate"],
                    crossover_rate=details["crossover_rate"],
                    scoring=details["scoring"],
                    cv=details["cv"],
                    subsample=details["subsample"],
                    max_time_mins=details["max_time_mins"],
                    max_eval_time_mins=details["max_eval_time_mins"],
                    random_state=details["random_state"],
                    config_dict=details["config_dict"],
                    template=details["template"],
                    early_stop=details["early_stop"],
                    periodic_checkpoint_folder="metafox_worker/checkpoints/" + job_id,
                    log_file="metafox_worker/logs/" + job_id + ".log"
                )
            except Exception as e:
                return {"message": "Error occurred during TPOT initialization.", "error": str(e)}
            
            model.fit(X_train, y_train)
            result = model.get_model_params()
            
            model.export_model("metafox_worker/exported_models/" + job_id + ".py")
    else:
        raise ValueError("Invalid AutoML library specified.")
    
    return {"message": "AutoML task completed.", "model": result}