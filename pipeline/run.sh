docker compose -f docker-compose.yml up -d
docker compose -f docker-compose-etl.yml up -d
docker compose -f docker-compose-recsys.yml up -d
docker compose -f docker-compose-gendata.yml up -d