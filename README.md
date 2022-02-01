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

## Performance (redis-benchmark)

```bash
redis-cli -p 6379
127.0.0.1:6379> keys *
127.0.0.1:6379> exit

redis-cli
127.0.0.1:6379> redis-benchmark -h 127.0.0.1 -q -n 1000000

free -h

redis-cli
127.0.0.1:6379> redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 #10 bytes per records

127.0.0.1:6379> redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 -t get,set
127.0.0.1:6379> redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 -t get,set -c 5 #-c number of clients

127.0.0.1:6379> dbsize
127.0.0.1:6379> flushall
```