import redis
import sys

def check_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("Redis is running and accessible.")
        return True
    except redis.ConnectionError:
        print("Error: Redis is NOT running or not accessible at localhost:6379.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    if check_redis():
        sys.exit(0)
    else:
        sys.exit(1)
