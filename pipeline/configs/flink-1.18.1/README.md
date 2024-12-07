## Build image:
```bash
docker build -t flink-etl .
```

```bash
docker tag flink-etl qxnam/flink-etl
```

Vì đã build sẵn nên chỉ cần gọi image tự pull về dùng luôn.

Job `etl` chỉ là mẫu để kiểm tra có nhận được data từ kafka khi database `OLTP` có sự thay đổi.

## Submit job
```bash
docker compose exec flink-jobmanager flink run -py ./jobs/etl.py -d
```