web: gunicorn parking.wsgi --log-file -
release: python manage.py migrate
worker: python manage.py celery worker --loglevel=info
beat: python manage.py celery beat --loglevel=info
