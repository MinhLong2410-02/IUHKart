docker exec -it superset superset db upgrade
docker exec -it superset superset init
docker exec -it superset superset fab create-admin --username admin --firstname Admin --lastname User --email Admin --password admin 
docker exec -it superset superset load_examples