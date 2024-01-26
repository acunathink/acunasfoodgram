pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir -q

python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

cp -r /app/collected_static/. /backend/static

gunicorn foodgram_backend.wsgi --bind 0.0.0.0:8000
