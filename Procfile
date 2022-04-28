web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: celery -A parking worker --l info
beat: celery -A parking beat --loglevel=info
