import json
import redis
from controllers.config import Config

_redis_client = None

def redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(Config.REDIS_URL, decode_responses=True)

    return _redis_client

def cache_get(key):
    try:
        value = redis_client().get(key)
    except redis.RedisError:
        return None

    if not value:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None

def cache_set(key, value, timeout=None):
    try:
        redis_client().setex(
            key,
            timeout or Config.CACHE_DEFAULT_TIMEOUT,
            json.dumps(value)
        )
    except (TypeError, redis.RedisError):
        return

def cache_delete_pattern(pattern):
    try:
        client = redis_client()
        keys = list(client.scan_iter(pattern))

        if keys:
            client.delete(*keys)
    except redis.RedisError:
        return

def clear_api_cache():
    cache_delete_pattern("api:*")
