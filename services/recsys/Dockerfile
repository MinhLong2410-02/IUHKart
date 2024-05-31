FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/rs.py

CMD ["python", "rs.py"]