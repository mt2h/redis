import sys
import redis

r = redis.StrictRedis('localhost', 6379, decode_responses=True)

header = ['firstname', 'lastname', 'fullname', 'address']

def get_values(key):
    key = str(key)
    print(key)
    try:
        value = r.get(key)
    except:
        sys.exit("Error in execution...")
    return value

print(get_values(sys.argv[1]))
