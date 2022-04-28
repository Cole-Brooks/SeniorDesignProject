web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: celery worker --app=tasks.app --l info
beat: celery beat --app=tasks.app --loglevel=info
