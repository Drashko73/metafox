import os
import celery
import pickle
import threading
import numpy as np
import pandas as pd
import celery.result
from time import sleep
from celery import Task

from metafox_worker.main import app
from metafox_shared.constants.worker_constants import *
from metafox_shared.constants.string_constants import *

stop_event = threading.Event()
logs_dictionary = {}

def observe_logs(task: Task, job_id: str, task_id: str) -> None:
    log_file = "metafox_worker/logs/" + job_id + ".log"
    
    while not stop_event.is_set():
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = f.readlines()
                
                celery.Task.update_state(
                    task,
                    state="PENDING",
                    task_id=task_id,
                    meta={"logs": logs}
                )
        
        sleep(OBSERVER_LOGS_SLEEP)
    
    # Read the logs one last time before stopping the observer thread and updating the task state
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = f.readlines()
            
            celery.Task.update_state(
                task,
                state="PENDING",
                task_id=task_id,
                meta={"logs": logs}
            )
            
            logs_dictionary[task_id] = logs

@app.task(bind = True)
def start_automl_train(self, config: object) -> dict:
    
    details = config[DETAILS]
    job_id = config[ID]
    
    # Load the data
    data = pd.read_csv(details[DATA_SOURCE])
    X_train = data.drop(details[TARGET_VARIABLE], axis=1)
    y_train = data[details[TARGET_VARIABLE]]
    
    if details[AUTOML_LIBRARY] == TPOT:
        if details[PROBLEM_TYPE] == REGRESSION:
            from metafox_worker.automl.tpot_regressor import TPOTRegressorWrapper
            
            if not os.path.exists("metafox_worker/logs/"):
                os.makedirs("metafox_worker/logs/") # Create logs directory if it doesn't exist
                
            if not os.path.exists("metafox_worker/checkpoints/"):
                os.makedirs("metafox_worker/checkpoints/")  # Create checkpoints directory if it doesn't exist
                
            if not os.path.exists("metafox_worker/exported_models/"):
                os.makedirs("metafox_worker/exported_models/")  # Create exported models directory if it doesn't exist
            
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
                    config_dict=details[CONFIG_DICT] if details[CONFIG_DICT] in AVAILABLE_CONFIG_DICTS else eval(details[CONFIG_DICT]),
                    template=details[TEMPLATE],
                    early_stop=details[EARLY_STOP],
                    periodic_checkpoint_folder="metafox_worker/checkpoints/" + job_id,
                    log_file="metafox_worker/logs/" + job_id + ".log"
                )
            except Exception as e:
                return {"message": "Error occurred during TPOT initialization.", "error": str(e)}
            
            observer_thread = threading.Thread(target=observe_logs, args=(self, job_id, self.request.id))
            observer_thread.start()
            
            errorFitting = False
            try:
                model.fit(X_train, y_train)
            except Exception as e:
                errorFitting = True
            
            stop_event.set()
            observer_thread.join()
            stop_event.clear()
            
            result = pickle.dumps(model.get_pipeline()) if not errorFitting else None
            
            if not errorFitting:
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
                    config_dict=details[CONFIG_DICT] if details[CONFIG_DICT] in AVAILABLE_CONFIG_DICTS else eval(details[CONFIG_DICT]),
                    template=details[TEMPLATE],
                    early_stop=details[EARLY_STOP],
                    periodic_checkpoint_folder="metafox_worker/checkpoints/" + job_id,
                    log_file="metafox_worker/logs/" + job_id + ".log"
                )
            except Exception as e:
                return {"message": "Error occurred during TPOT initialization.", "error": str(e)}
            
            observer_thread = threading.Thread(target=observe_logs, args=(self, job_id, self.request.id))
            observer_thread.start()
            
            errorFitting = False
            try:
                model.fit(X_train, y_train)
            except Exception as e:
                errorFitting = True
            
            stop_event.set()
            observer_thread.join()
            stop_event.clear()
            
            result = pickle.dumps(model.get_pipeline()) if not errorFitting else None
            
            if not errorFitting:
                model.export_model("metafox_worker/exported_models/" + job_id + ".py")
    else:
        raise ValueError("Invalid AutoML library specified.")
    
    return {"message": "AutoML task completed.", "model": result, "logs": logs_dictionary[self.request.id]}