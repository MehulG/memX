import os
import redis


def get_client():
    """
    Return a Redis client configured via REDIS_URL (default localhost).
    decode_responses=True to handle JSON strings easily.
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(redis_url, decode_responses=True)
