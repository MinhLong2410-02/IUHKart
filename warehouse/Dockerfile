FROM python:latest
COPY . /app

RUN apt-get update && apt-get install cron -y -qq
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN chmod +x /app/run.sh
RUN echo "0 0 * * * root /app/run.sh > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab

ENTRYPOINT ["cron", "-f"]