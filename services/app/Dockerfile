FROM python:3.10-slim
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]