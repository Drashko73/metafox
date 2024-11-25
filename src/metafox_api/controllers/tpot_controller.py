import re
import os
import json
import pickle
import bentoml
from fastapi import Response
from celery import states
from metafox_shared.constants.api_constants import *
from metafox_shared.constants.string_constants import *
from metafox_shared.dal.idatastore import IDataStore
from metafox_shared.models.tpot_job import TPOTAutoMLJob
from metafox_api.controllers.base_controller import BaseController
from metafox_shared.models.celery_task import CeleryTaskInfo
from metafox_shared.utilis import get_current_date
class TPOTController(BaseController):
    """
    Controller for TPOT AutoML jobs.
    Args:
        BaseController (_type_): Base controller class.
    """
    
    def __init__(self, data_store: IDataStore) -> None:
        """
        Initialize the TpotController with the given data store.

        Args:
            data_store (IDataStore): The data store instance to be used by the controller.
        """
        super().__init__(data_store)
        
    def create_automl_job(self, body: TPOTAutoMLJob) -> Response:
        """
        Creates a new AutoML job and stores its details in the data store.
        Args:
            body (TPOTAutoMLJob): The details of the AutoML job to be created.
        Returns:
            Response: A response object indicating the result of the operation.
                - 200: If the AutoML job was successfully created.
                - 500: If there was an error saving the AutoML job details.
        """
        job_details = body.__str__()

        id = self.data_store.generate_unique_job_key()
        
        try:
            self.data_store.set(id, job_details)
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
                media_type="text/plain"
            )
        
        celery_task = CeleryTaskInfo(
            task_id=NOT_STARTED,
            timestamp_created=get_current_date(),
            timestamp_received="",
            timestamp_started="",
            timestamp_completed="",
            hostname='',
            finished_status=''
        )
        
        try:
            self.data_store.set(CELERY_KEY_PREFIX + id, celery_task.__str__())    # Set celery task id to NOT_STARTED
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
                media_type="text/plain"
            )
            
        return Response(
            status_code=200, 
            content=json.dumps({"message": "AutoML job created.", "automl_job_id": id}), 
            media_type="application/json"
        )
    
    def start_automl_job(self, automl_job_id: str) -> Response:
        """
        Starts an AutoML job with the given job ID.
        Args:
            automl_job_id (str): The ID of the AutoML job to start.
        Returns:
            Response: A Response object indicating the result of the operation.
                - 404: If the required data for the AutoML job or the job details are not found.
                - 400: If the AutoML job has already been started.
                - 500: If there is an error saving the AutoML job details.
                - 200: If the AutoML job is successfully started.
        """
        
        task_id = self._get_task_id(automl_job_id)
        
        if task_id is None:
            return Response(
                status_code=404, 
                content="Could not find required data for the AutoML job.", 
                media_type="text/plain"
            )
        
        if task_id != NOT_STARTED:
            return Response(
                status_code=400, 
                content="AutoML job already started.", 
                media_type="text/plain"
            )
        
        job_details = self._get_automl_job_details(automl_job_id)
        if job_details is None:
            return Response(
                status_code=404, 
                content="AutoML job not found.", 
                media_type="text/plain"
            )
        
        result = self.celery.send_task('metafox_worker.tasks.start_training.start_automl_train', [{DETAILS: job_details, ID: automl_job_id}])
        
        celery_task = eval(self.data_store.get(CELERY_KEY_PREFIX + automl_job_id))
        celery_task[TASK_ID] = result.id
        
        try:
            self.data_store.update(CELERY_KEY_PREFIX + automl_job_id, celery_task.__str__())  # Update celery task id status to the task id
        except Exception as e:
            return Response(
                status_code=500, 
                content="Error saving AutoML job details.", 
                media_type="text/plain"
            )
        
        return Response(
            status_code=200, 
            content="AutoML job started.", 
            media_type="text/plain"
        )
    
    def stop_automl_job(self, automl_job_id: str) -> Response:
        """
        Stops an AutoML job given its job ID.
        Args:
            automl_job_id (str): The ID of the AutoML job to stop.
        Returns:
            Response: A Response object indicating the result of the stop operation.
                - If the job details are not found, returns a 404 response with a message.
                - If the job has not started, returns a 200 response with a message.
                - If the job is successfully stopped, returns a 200 response with a message.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        self.celery.control.terminate(task_id=status[TASK_ID], signal="SIGQUIT")
        
        return Response(
            status_code=200,
            content="AutoML job stopped.",
            media_type="text/plain"
        )
        
    def save_model_to_bentoml(self, automl_job_id: str) -> Response:
        """
        Save the model from an AutoML job to BentoML.
        Args:
            automl_job_id (str): The ID of the AutoML job.
        Returns:
            Response: A FastAPI Response object indicating the result of the operation.
        Raises:
            Exception: If there is an error retrieving the AutoML job details from the data store.
        Responses:
            404: If the AutoML job details are not found.
            200: If the AutoML job has not started or is not completed.
            500: If there is a failure in the AutoML job or saving the model to BentoML.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": res.traceback}),
                    media_type="application/json"
                )
            
            pipeline_bytes = res.get()["model"]
            response = self._save_pipeline_to_bentoml(pipeline_bytes, automl_job_id)
            
            if response != OK:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": response}),
                    media_type="application/json"
                )
            
            return Response(
                status_code=200,
                content="Model saved.",
                media_type="text/plain"
            )
        
        return Response(
            status_code=200,
            content="AutoML job not completed.",
            media_type="text/plain"
        )
    
    def retrieve_job_details(self, automl_job_id: str) -> Response:
        """
        Retrieve the details of an AutoML job.
        Args:
            automl_job_id (str): The ID of the AutoML job to retrieve details for.
        Returns:
            Response: A Response object containing the status code and job details.
                - 400: If the job ID starts with an invalid prefix.
                - 404: If the job details are not found.
                - 200: If the job details are successfully retrieved.
        """
        
        if automl_job_id.startswith(CELERY_KEY_PREFIX) or automl_job_id.startswith(CELERY_METAS_KEY_PREFIX):
            return Response(
                status_code=400,
                content="Invalid AutoML job id.",
                media_type="text/plain"
            )
        
        job_details = self._get_automl_job_details(automl_job_id)
        
        if job_details is None:    
            return Response(
                status_code=404,
                content="AutoML job not found.",
                media_type="text/plain"
            )
        
        return Response(
            status_code=200,
            content=json.dumps({"automl_job_id": automl_job_id, "details": job_details}),
            media_type="application/json"
        )
    
    def retreive_job_status(self, automl_job_id: str, lines: int) -> Response:
        """
        Retrieve the status of an AutoML job.
        Args:
            automl_job_id (str): The unique identifier for the AutoML job.
            lines (int): The number of log lines to retrieve. Must be greater than or equal to 0.
        Returns:
            Response: A Response object containing the status of the AutoML job, fitness score, logs, 
                      and any traceback information if the job failed.
        Responses:
            400: If the number of lines is less than 0.
            404: If the AutoML job details are not found.
            200: If the job status is successfully retrieved, including:
                 - "AutoML job not started" if the job has not started.
                 - Job state, fitness score, logs, and traceback information if the job has failed.
                 - Job state, fitness score, and logs if the job is in progress or completed.
        """
        if lines < 0:
            return Response(
                status_code=400, 
                content="Number of lines must be greater than or equal to 0.", 
                media_type="text/plain"
            )
        
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        job = self.celery.AsyncResult(status[TASK_ID])
        
        if job.state == states.FAILURE:
            return Response(
                status_code=200,
                content=json.dumps({
                    "status": job.state,
                    "fitness": "",
                    "logs": "",
                    "traceback": job.traceback
                }),
                media_type="application/json"
            )
        
        if job.info and "logs" in job.info:
            fitness = self._extract_fitness_from_logs("".join(job.info["logs"]))
            logs = "".join(job.info["logs"][-lines:])
        else:
            fitness = ""
            logs = ""
        
        return Response(
            status_code=200,
            content=json.dumps({
                "status": job.state,
                "fitness": fitness,
                "logs": logs
            }),
            media_type="application/json"
        )
    
    def retrieve_job_result(self, automl_job_id: str) -> Response:
        """
        Retrieve the result of an AutoML job.
        Args:
            automl_job_id (str): The unique identifier for the AutoML job.
        Returns:
            Response: A Response object containing the status and result of the AutoML job.
                - 200: If the job is not started, not completed, or completed successfully.
                - 404: If the job details are not found.
                - 500: If the job failed with an error.
        Raises:
            Exception: If there is an error retrieving the job details from the data store.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404, 
                content="Required AutoML job details not found.", 
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200, 
                content="AutoML job not started.", 
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": res.traceback}),
                    media_type="application/json"
                )
            
            return Response(
                status_code=200, 
                content=json.dumps({"result": res.get()}),
                media_type="application/json"
            )
        
        return Response(
            status_code=200, 
            content="AutoML job not completed.", 
            media_type="text/plain"
        )
        
    def export_model_bentoml(self, automl_job_id: str) -> Response:
        """
        Export the trained AutoML model using BentoML.
        Args:
            automl_job_id (str): The ID of the AutoML job.
        Returns:
            Response: A FastAPI Response object containing the status and content of the export operation.
        Raises:
            Exception: If there is an error retrieving the AutoML job details from the data store.
        Responses:
            404: If the required AutoML job details are not found or if the optimization failed.
            200: If the AutoML job has not started or is not completed.
            500: If there is an error saving the pipeline to BentoML.
            200: If the model file is successfully retrieved and returned as an attachment.
        """
        try:
            status = self.data_store.get(CELERY_KEY_PREFIX + automl_job_id)
        except Exception as e:
            return Response(
                status_code=404,
                content="Required AutoML job details not found.",
                media_type="text/plain"
            )
        
        status = eval(status)
        if status[TASK_ID] == NOT_STARTED:
            return Response(
                status_code=200,
                content="AutoML job not started.",
                media_type="text/plain"
            )
        
        res = self.celery.AsyncResult(status[TASK_ID])
        if res.ready():
            if res.state == states.FAILURE:
                return Response(
                    status_code=404,
                    content=json.dumps({
                        "message": "Optimization failed. Model not found.",
                        "traceback": res.traceback
                    }),
                    media_type="application/json"
                )
            
            pipeline_bytes = res.get()["model"]
            response = self._save_pipeline_to_bentoml(pipeline_bytes, automl_job_id)
            
            if response != OK:
                return Response(
                    status_code=500,
                    content=json.dumps({"traceback": response}),
                    media_type="application/json"
                )
            
            # Return the saved model file saved in metafox_api/bento_models
            filepath = "metafox_api/bento_models/" + automl_job_id + ".bentomodel"
            
            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    return Response(
                        status_code=200,
                        content=file.read(),
                        media_type="application/octet-stream",
                        headers={"Content-Disposition": f"attachment; filename={automl_job_id}.bentomodel"}
                    )
            else:
                return Response(
                    status_code=404,
                    content="Model not found. Make sure to call the save_model_bentoml endpoint first.",
                    media_type="text/plain"
                )
        
        return Response(
            status_code=200,
            content="AutoML job not completed.",
            media_type="text/plain"
        ) 
        
    def _save_pipeline_to_bentoml(self, pipeline_bytes: bytes, job_id: int) -> str:
        """
        Save a scikit-learn pipeline to BentoML and export the model.
        Args:
            pipeline_bytes (bytes): The serialized scikit-learn pipeline.
            job_id (int): The job identifier used for naming the saved model.
        Returns:
            str: "OK" if the model is successfully saved and exported, or an error message if an exception occurs.
        """
        
        # Check if sklearn module is not imported and import it
        if "sklearn" not in globals():
            import sklearn
        
        pipeline = pickle.loads(pipeline_bytes)
        
        # Check if the directory exists, if not create it
        if not os.path.exists("metafox_api/bento_models/"):
            os.makedirs("metafox_api/bento_models/")
            
        bento_path = "metafox_api/bento_models/" + str(job_id)
        
        # Check if the file already exists. 
        # If it does, return OK (No need to save it to the bento store again)
        if os.path.exists(bento_path + ".bentomodel"):
            return OK
        
        bento_tag = bentoml.Tag(
            name=str(job_id),
            version="1.0.0"
        )
        
        try:
            bentoml.sklearn.save_model(
                name=bento_tag,
                model=pipeline
            )
        except Exception as e:
            return str(e)
        
        try:
            bentoml.models.export_model(
                tag=bento_tag,
                path=bento_path,
            )
        except Exception as e:
            return str(e)
        
        return OK
    
    def _extract_fitness_from_logs(self, logs: str) -> str:
        """
        Extracts fitness scores from the provided log string.
        This method searches the log string for lines that match the pattern
        "Generation <number> - Current best internal CV score: <score>". It returns
        these lines joined by newline characters.
        Args:
            logs (str): The log string to search for fitness scores.
        Returns:
            str: A string containing the matched lines, each on a new line. If no
                 matches are found, an empty string is returned.
        """
        pattern = r"Generation \d+ - Current best internal CV score: -?\d+\.\d+"
        
        matches = re.findall(pattern, logs)
        
        return "" if len(matches) == 0 else "\n".join(matches)