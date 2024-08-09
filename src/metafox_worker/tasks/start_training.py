import pandas as pd

from metafox_worker.main import app
from metafox_shared.constants.tpot_constants import *
from metafox_shared.constants.string_constants import *

@app.task
def start_automl_train(config: object) -> dict:
    
    details = config[DETAILS]
    job_id = config[ID]
    
    # Load the data
    data = pd.read_csv(details[DATA_SOURCE])
    X_train = data.drop(details[TARGET_VARIABLE], axis=1)
    y_train = data[details[TARGET_VARIABLE]]
    
    if details[AUTOML_LIBRARY] == TPOT:
        if details[PROBLEM_TYPE] == REGRESSION:
            from metafox_worker.automl.tpot_regressor import TPOTRegressorWrapper
            
            try:
                model = TPOTRegressorWrapper(
                    n_jobs=N_JOBS_TPOT,
                    memory=MEMORY_TPOT,
                    use_dask=USE_DASK_TPOT,
                    verbosity=VERBOSITY_TPOT,
                    warm_start=WARM_START_TPOT,
                    generations=details[GENERATIONS],
                    population_size=details[POPULATION_SIZE],
                    offspring_size=details[OFFSPRING_SIZE],
                    mutation_rate=details[MUTATION_RATE],
                    crossover_rate=details[CROSSOVER_RATE],
                    scoring=details[SCORING],
                    cv=details[CV],
                    subsample=details[SUBSAMPLE],
                    max_time_mins=details[MAX_TIME_MINS],
                    max_eval_time_mins=details[MAX_EVAL_TIME_MINS],
                    random_state=details[RANDOM_STATE],
                    config_dict=details[CONFIG_DICT],
                    template=details[TEMPLATE],
                    early_stop=details[EARLY_STOP],
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
                    generations=details[GENERATIONS],
                    population_size=details[POPULATION_SIZE],
                    offspring_size=details[OFFSPRING_SIZE],
                    mutation_rate=details[MUTATION_RATE],
                    crossover_rate=details[CROSSOVER_RATE],
                    scoring=details[SCORING],
                    cv=details[CV],
                    subsample=details[SUBSAMPLE],
                    max_time_mins=details[MAX_TIME_MINS],
                    max_eval_time_mins=details[MAX_EVAL_TIME_MINS],
                    random_state=details[RANDOM_STATE],
                    config_dict=details[CONFIG_DICT],
                    template=details[TEMPLATE],
                    early_stop=details[EARLY_STOP],
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