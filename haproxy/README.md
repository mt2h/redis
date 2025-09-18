# Redis Architecture

## Install with Helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm show values bitnami/redis --version 17.15.2 > redis.yaml
```

## Standalone

```yaml
architecture: standalone
replica:
  replicaCount: 1
sentinel:
  enabled: false
```

## Replication (master + replicas)

```yaml
architecture: replication
replica:
  replicaCount: 3
sentinel:
  enabled: false
```

Connect to the master (write), connect to a replica (read): you can run `redis-cli INFO replication` in each pod to see the roles.

### Master

```bash
kubectl port-forward svc/redis-master -n redis 6379:6379
redis-cli -h localhost -p 6379 INFO replication
redis-cli -h localhost -p 6379 ROLE
```

Output:

```bash
role:master
connected_slaves:3
master_failover_state:no-failover
```

### Replica

```bash
kubectl port-forward svc/redis-replicas -n redis 6379:6379
redis-cli -h localhost -p 6379 INFO replication
redis-cli -h localhost -p 6379 ROLE
```

Output:

```bash
role:slave
slave_read_only:1
connected_slaves:0
master_failover_state:no-failover
```

## Replication + Sentinel (high availability and automatic failover)

```yaml
architecture: replication
replica:
  replicaCount: 3
sentinel:
  enabled: true
  masterSet: mymaster
  quorum: 2
```

### Current Master by Redis Port On Service

```bash
kubectl -n redis port-forward svc/redis 6379:6379
redis-cli -h localhost -p 6379 INFO replication
redis-cli -h localhost -p 6379 ROLE
```

Output:

```bash
role:master
connected_slaves:2
master_failover_state:no-failover
```

### Sentinel Service

```bash
kubectl -n redis port-forward svc/redis 26379:2637979
redis-cli -h localhost -p 26379 SENTINEL get-master-addr-by-name mymaster
```

Output:

```bash
1) "redis-node-0.redis-headless.redis.svc.cluster.local"
2) "6379"
```

### Failover

```bash
kubectl -n redis port-forward svc/redis 6379:6379 26379:26379
kubectl -n redis delete pod redis-node-0
kubectl -n redis logs redis-node-1 -c sentinel -f
# connect again
kubectl -n redis port-forward svc/redis 6379:6379 26379:26379
redis-cli -h localhost -p 6379 INFO replication
```

## HAProxy

🔹 What HAProxy Provides

A single connection point (the HAProxy service in Kubernetes).

The application no longer needs to know which node is the master or which is the replica.

It always connects to `haproxy:6379`.

Read/write routing according to rules:

* HAProxy can direct writes only to the master.
* HAProxy can distribute reads among the replicas (round-robin, leastconn, etc.).
* It also supports fallback: if the master fails, Sentinel promotes a replica → HAProxy updates the routing → the application only needs to reconnect.

Flow

The app connects to `haproxy.redis.svc.cluster.local:6379`.

HAProxy listens to Sentinel to know which node is the current master.

HAProxy forwards:

* Write commands → to the master.
* Read commands → balanced among the replicas.

```yaml
service:
  type: ClusterIP
  ports:
    - name: redis
      protocol: TCP
      port: 6379
      targetPort: 6379
replicaCount: 1
configuration: |
  global
    log stdout format raw local0
    maxconn 1024
  defaults
    log global
    timeout client 60s
    timeout connect 60s
    timeout server 60s
  frontend redis_frontend
    bind *:6379
    mode tcp
    default_backend redis_backend
  backend redis_backend
    mode tcp
    balance roundrobin
    option tcp-check
    server redis-node-0 redis-node-0.redis-headless.redis.svc.cluster.local:6379 check
    server redis-node-1 redis-node-1.redis-headless.redis.svc.cluster.local:6379 check
    server redis-node-2 redis-node-2.redis-headless.redis.svc.cluster.local:6379 check
containerPorts:
  - name: redis
    containerPort: 6379
extraEnvVars:
  - name: REDIS_SENTINEL_HOST
    value: "redis.redis.svc.cluster.local"
  - name: REDIS_SENTINEL_PORT
    value: "26379"
```

`frontend redis_frontend` → listens for your app on port 6379.

`backend redis_backend` → lists all Redis pods and does round-robin among them.

`option tcp-check` → allows HAProxy to mark a pod as down and avoid using it.

### HAProxy with proper CL (Connection Logic)

Configure HAProxy to:

* Redirect writes to the master
* Redirect reads to the replicas
