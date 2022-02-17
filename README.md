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

#sets (members)
sadd users_ip 10.0.0.1
sadd users_ip 10.0.0.2 10.0.0.3 192.168.0.0
scard users_ip
smembers users_ip
sadd yesterday_ip 10.0.0.1 192.168.0.0 10.3.4.0 192.168.0.0.3
sdiff users_ip yesterday_ip
sdiff yesterday_ip users_ip
sismember yesterday_ip 192.168.0.0 #if exists as member
smove yesterday_ip previous_ip 192.168.0.0
smembers previous_ip
smembers yesterday_ip
sadd users john martin rahul vikas henry
spop users #remove
spop users 2
srem users "john" #remove
srem users "martin" "henry"
```

## Transactions

https://www.itpanther.com/redis-transactions/

```bash
set ticket_available 4
keys *
get ticket_available
decr ticket_available

multi
get ticket_available #QUEUED
decr ticket_available #QUEUED
exec

multi
decr ticket_available #QUEUED
discard #discard transaction

watch ticket_available
multi
get ticket_available
decr ticket_available
exec
```

## Redis Insertion

https://www.itpanther.com/what-is-the-fastest-way-to-insert-data-to-redis/

```bash
cd raw_data/
awk -F ',' '{print $1}' countries.csv #print firt column (separate by comma)
awk -F ',' '{print "SET " $2 " " $1}' countries.csv > countries_to_redis.csv
wc -l countries_to_redis.csv #count lines

#insert data
cat countries_to_redis.csv | redis-cli -h localhost -p 6379
cat countries_to_redis.csv | redis-cli -h localhost -p 6379 --pipe

dbsize
```

## Backup and Restore

```bash
vim /etc/redis/redis.conf
```

## Python

```bash
cd python
cat student.csv.redis_format | redis-cli --pipe
pip3 install redis
python3 load_students_info.py 1
```

## Commands

```bash
ps -ef | grep redis
sudo redis-server /etc/redis/redis.conf &
```

## History

```bash
less ~/.rediscli_history
```
