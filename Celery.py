from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')  # Configurar o broker

# ... (resto do seu código)