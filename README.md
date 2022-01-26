# Commands

## install Redis

```bash
sudo apt install redis-server -y
sudo systemctl restart redis.service
sudo systemctl start redis
sudo systemctl status redis
```

## commands Redis

```bash
redis-cli
27.0.0.1:6379> SET color RED
27.0.0.1:6379> SET color WHITE
27.0.0.1:6379> GET color
```