import json
import jsonschema
import redis
from redis_client import get_client


_redis = get_client()
SCHEMA_PREFIX = "memx:schema:"


def _redis_key(key: str) -> str:
    return f"{SCHEMA_PREFIX}{key}"


def register_schema(key, schema_dict):
    jsonschema.Draft7Validator.check_schema(schema_dict)
    _redis.set(_redis_key(key), json.dumps(schema_dict))


def validate_schema(key, value):
    schema = get_schema(key)
    if schema:
        jsonschema.validate(instance=value, schema=schema)


def get_schema(key):
    raw = _redis.get(_redis_key(key))
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def delete_schema(key):
    return _redis.delete(_redis_key(key)) == 1
