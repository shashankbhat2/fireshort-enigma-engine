from fastapi import FastAPI
from celery import Celery

app = FastAPI()

# Initialize Celery
celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def add_numbers(x, y):
    return x + y

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add")
async def add(x: int, y: int):
    task = add_numbers.delay(x, y)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = add_numbers.AsyncResult(task_id)
    if task.ready():
        return {"result": task.result}
    return {"status": "pending"}



