from app import app, db
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def gerar_feed_rss():
    # ... lógica para gerar o feed RSS