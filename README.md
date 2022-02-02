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

redis-cli -p 6379

```bash
keys *
exit

#redis-cli
redis-benchmark -h 127.0.0.1 -q -n 1000000

#free -h

#redis-cli
redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 #10 bytes per records

redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 -t get,set
redis-benchmark -h 127.0.0.1 -p 6379 -q -n 1000000 -d 10 -t get,set -c 5 #-c number of clients

dbsize
flushall
```

## Data Types

redis-cli

```bash
#simple values
set chair 100
get chair
keys *
del chair
set seq_id 1
incr seq_id #increment counter
get seq_id
exists seq_id #if exists
dbsize #total records

#multiple values
mset soft 100 TV 200 Bed 300
mget soft TV Bed

#TTL (expires seconds)
set color red EX 60
expire Bed 60
flushall #all clear

#lists
lpush color Red Blue White #insert from left list
lrange color 0 -1 #get list
lpush color Black
rpush color Magenta #insert right to list
#lrange | rrange color 0 -(total - secuncuence)
llen color #lenght list

#remove elements of list
lpop color
rpop color
ltrim color 0 2 #delete from 2 index onwards

#hashes
hset product chair 100 table 200 TV 300
hget product chair
hmget product chair table #get multiple elements
```