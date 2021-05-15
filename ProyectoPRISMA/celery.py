from celery import Celery

app = Celery('ProyectoPRISMA',
             broker='amqp://localhost',
             backend='rpc://',
             include=['ProyectoPRISMA.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Argentina/Buenos_Aires',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()