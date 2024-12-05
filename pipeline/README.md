# Services
`docker-compose].yml`

Khởi động các service chính:
```bash
docker compose up -d
```

## API embedding
Đã build sẵn image `qxnam/embedding-api`
- localhost: localhost:8000
- domain: [https://embed.iuhkart.systems/](https://embed.iuhkart.systems/)

## Superset (Dashboard)
Cần thực hiện các lệnh trong `pipeline/configs/superset/init.sh` để khởi tạo user đăng nhập.

- localhost: localhost:8088
- domain: [https://viz.iuhkart.systems/](https://viz.iuhkart.systems/)

Thông tin đăng nhập:
- user: admin
- password: admin

## debezium-ui (Change Data Capture)
- localhost: localhost:8085
- domain: [https://debezium.iuhkart.systems/](https://debezium.iuhkart.systems/)

## kafka-ui (Event streaming)
- localhost: localhost:8081
- domain: [https://kafka.iuhkart.systems/](https://kafka.iuhkart.systems/)

## flink (ETL)
- localhost: localhost:28081
- domain: [https://flink.iuhkart.systems/](https://flink.iuhkart.systems/)

## airflow (Generate data)
- localhost: localhost:13005
- domain: [https://airflow.iuhkart.systems/](https://airflow.iuhkart.systems/)

## portainer (Manager container)
- localhost: localhost:29011
- domain: [https://dockerdb.iuhkart.systems/](https://dockerdb.iuhkart.systems/)
