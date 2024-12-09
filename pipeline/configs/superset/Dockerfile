FROM apache/superset:latest

USER root
RUN pip install --no-cache-dir SQLAlchemy clickhouse-connect>=0.6.8
COPY --chmod=777 superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/usr/bin/run-server.sh" ]