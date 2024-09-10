# tasks.py
from celery_config import app

@app.task
def add_numbers(x, y):
    return x + y
