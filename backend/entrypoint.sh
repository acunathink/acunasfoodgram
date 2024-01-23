python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

cp -r /app/collected_static /backend/backend/static
gunicorn foodgram_backend.wsgi --bind 0.0.0.0:8000
