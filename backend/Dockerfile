FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram_backend.wsgi"]
