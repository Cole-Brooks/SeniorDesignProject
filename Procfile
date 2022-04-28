web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: celery worker --parking=tasks.app --l info
beat: celery beat --parking=tasks.app --loglevel=info
