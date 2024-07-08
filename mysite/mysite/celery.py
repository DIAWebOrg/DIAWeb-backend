import os
from celery import Celery
from celery.signals import worker_process_init
from myapp.stream_consumer import main as stream_consumer_main
from filelock import FileLock
from celery.signals import worker_process_init
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

lock_path = "/tmp/stream_consumer.lock"

@worker_process_init.connect
def start_stream_consumer(*args, **kwargs):
    # Use a file lock to ensure only one stream consumer starts across all workers
    lock = FileLock(lock_path)
    # This will run the stream_consumer_main function in a separate thread
    # when a new worker process is initialized.
    try:
        # Try to acquire the lock, but do not block if it's already locked
        with lock.acquire(timeout=1):
            thread = Thread(target=stream_consumer_main)
            thread.daemon = True  # This ensures the thread exits when the main process does
            thread.start()
    except TimeoutError:
        # If the lock is already held by another worker, do nothing
        pass
