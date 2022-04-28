web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: celery -A parking worker
beat: celery -A parking beat
worker-beat: celery -A parking worker & celery -A parking beat & wait -n