web: gunicorn afrivent.wsgi --log-file -
worker: celery -A afrivent worker -l info
release: python manage.py migrate