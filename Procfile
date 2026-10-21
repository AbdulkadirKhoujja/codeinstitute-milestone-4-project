release: python manage.py migrate --noinput
web: gunicorn config.wsgi:application --config config/gunicorn.py --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 30 --access-logfile - --error-logfile -
