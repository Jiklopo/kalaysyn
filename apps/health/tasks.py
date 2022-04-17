import time
from configuration.celery import app


@app.task(bind=True)
def test_task(self):
    time.sleep(5)
    print(f'Request: {self.request!r}')
