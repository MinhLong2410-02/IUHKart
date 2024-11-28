Vì tách ra 2 file docker-compose nên dùng network extenal.

Tạo trước network trên máy:
```bash
docker network create iuhkart-network
```

# Các database bao gồm:
`docker-compose.yml`

Khởi động các database chính:
```bash
docker compose -f docker-compose.yml up -d
```

Thông tin kết nối:
**server**
- host server: **crawl.serveftp.com**
- host clouflare: **iuhkart.systems**

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
    - database: `demo`
    - collection: `items`
```python
connection_string = "mongodb://crawl.serveftp.com:27017/?replicaSet=rs0"
```

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
