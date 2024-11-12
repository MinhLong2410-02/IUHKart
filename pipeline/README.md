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

