from fastapi import FastAPI

from metafox.tasks.start_training import start_automl_train
from metafox.schemas.start_automl_request import StartAutoMLRequest

app = FastAPI()

@app.post("/automl/start")
async def start_automl_task(body: StartAutoMLRequest):
    result = start_automl_train.delay(body.link_to_data, body.target)
    return {"task_id": result.id, "message": "AutoML task started."}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = start_automl_train.AsyncResult(task_id)
    return {"task_id": task.id, "status": task.status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)