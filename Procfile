web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: celery -A parking worker --pool=solo -l info
beat: celery -A parking beat -l INFO
worker-beat: celery -A parking worker & celery -A parking beat & wait -n
