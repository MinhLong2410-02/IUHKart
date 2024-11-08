Vì tách ra 2 file docker-compose nên dùng network extenal.

Tạo trước network trên máy:
```bash
docker network create iuhkart-network
```

# Databases
`docker-compose-databases.yml`

Khởi động các database chính:
```bash
docker compose -f docker-compose-databases.yml up -d
```

Thông tin kết nối các database:
**server**
- host: crawl.serveftp.com

**local**
- postgres-database:
    - host: localhost
    - port: 5432
    - user: iuhkart
    - password: iuhkartpassword
    - database: postgres

- mongo:
    - host: localhost
    - port: 27017
    - user: iuhkart
    - password: iuhkartpassword
    - database: e-commerce

- clickhouse:
    - host: localhost
    - port: 8123
    - user: iuhkart
    - password: iuhkartpassword
    - database: default

- qdrant [http://localhost:6334/dashboard](http://localhost:6334/dashboard):
    - host: localhost
    - port: 6333

# Services
`docker-compose-services.yml`

Khởi động các service chính:
```bash
docker compose -f docker-compose-services.yml up -d
```

## API embedding slug
Đã build sẵn image `qxnam/embedding-api`
- localhost: localhost:8000
- domain: [https://embed.iuhkart.systems/](https://embed.iuhkart.systems/)

## Superset data visualization
Cần thực hiện các lệnh trong `pipeline/configs/superset/init.sh` để khởi tạo user đăng nhập.

- localhost: localhost:8088
- domain: [https://viz.iuhkart.systems/](https://viz.iuhkart.systems/)

Thông tin đăng nhập:
- user: admin
- password: admin

