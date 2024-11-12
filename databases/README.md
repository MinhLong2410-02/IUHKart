Vì tách ra 2 file docker-compose nên dùng network extenal.

Tạo trước network trên máy:
```bash
docker network create iuhkart-network
```

# Các database bao gồm:
`docker-compose-databases.yml`

Khởi động các database chính:
```bash
docker compose -f docker-compose-databases.yml up -d
```

Thông tin kết nối:
**server**
- host [sub domain]: **crawl.serveftp.com**

**local**
- postgres-database:
    - host: `localhost`
    - port: `5432`
    - user: `iuhkart`
    - password: `iuhkartpassword`
    - database: `postgres`

- mongo:
    - host: `localhost`
    - port: `27017`
    - user: `iuhkart`
    - password: `iuhkartpassword`
    - database: `e-commerce`

- clickhouse:
    - host: `localhost`
    - port: `8123`
    - user: `iuhkart`
    - password: `iuhkartpassword`
    - database: `default`

- qdrant:
    - host: `localhost`
    - port: `6334`

UI: [qdrant.iuhkart.systems/dashboard](https://qdrant.iuhkart.systems/dashboard)

- minio:
    user: `$MINIO_ROOT_USER`
    password: `$MINIO_ROOT_PASSWORD`

UI: [minio.iuhkart.systems](https://minio.iuhkart.systems)
