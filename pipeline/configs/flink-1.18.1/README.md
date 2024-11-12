Build image:
```bash
docker build -t pyflink:1.18.1 .
```

```bash
docker tag pyflink:1.18.1 qxnam/pyflink:1.18.1
```

Vì đã build sẵn nên chỉ cần gọi image tự pull về dùng luôn.

Job `etl` chỉ là mẫu để kiểm tra có nhận được data từ kafka khi database `OLTP` có sự thay đổi.