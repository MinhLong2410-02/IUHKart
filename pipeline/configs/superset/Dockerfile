FROM apache/superset:3.0.2
USER root
RUN pip install --no-cache-dir clickhouse-connect>=0.6.8 sqlalchemy psycopg2-binary
COPY --chmod=777 superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
USER superset
ENTRYPOINT [ "/usr/bin/run-server.sh" ]

