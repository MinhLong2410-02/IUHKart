FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]