# First stage: build the wheel file and dependencies
FROM python:3.9-slim-buster AS builder

RUN apt-get update && apt-get install -y curl && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir=/app/wheels -r requirements.txt


# Second stage: copy the wheel file and install dependencies
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY main.py .
COPY requirements.txt .

# Install the sentence-transformers library and download the model
RUN apt-get update && apt-get install -y curl
RUN pip install --no-cache /wheels/* && python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2');"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]