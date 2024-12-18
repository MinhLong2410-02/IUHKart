# Mô tả tổng quan 
1. `docker-compose.yml` chạy các công cụ `CDC` và `Kafka`.
2. `docker-compose-etl.yml` khởi tạo quá trình ETL vào DWH.
3. `docker-compose-gendata.yml` Airflow quản lí việc sinh data (product, order, review).
4. `docker-compose-recsys.yml` gồm mô hình embedding và hệ thống tìm kiếm + khuyến nghị.
5. `docker-compose-superset.yml` công cụ Visualization.

# Chi tiết các dịch vụ
## API embedding
Đã build sẵn image `qxnam/embedding-api`
- localhost: localhost:8000
- domain: [https://embed.iuhkart.systems/](https://embed.iuhkart.systems/)

## Superset (Dashboard)
Cần thực hiện các lệnh trong `pipeline/configs/superset/init.sh` để khởi tạo user đăng nhập.

- localhost: localhost:8088
- domain: [https://superset.iuhkart.systems/](https://superset.iuhkart.systems/)

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

