import time
import json
import redis
from redis_client import get_client


_redis = get_client()
VALUE_PREFIX = "memx:value:"


def _redis_key(key: str) -> str:
    return f"{VALUE_PREFIX}{key}"


def get_value(key):
    raw = _redis.get(_redis_key(key))
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def set_value(key, value):
    """Last-write-wins based on timestamp, stored in Redis."""
    redis_key = _redis_key(key)
    now = time.time()
    payload = {"value": value, "ts": now}

    with _redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(redis_key)
                prev_raw = pipe.get(redis_key)
                if prev_raw:
                    prev = json.loads(prev_raw)
                    if now <= prev.get("ts", 0):
                        pipe.unwatch()
                        return False
                pipe.multi()
                pipe.set(redis_key, json.dumps(payload))
                pipe.execute()
                return True
            except redis.WatchError:
                # Retry if the key was modified between watch and execute
                continue
            finally:
                pipe.reset()
