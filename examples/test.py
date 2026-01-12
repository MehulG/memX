"""
Basic smoke test against the memX API.
- Uses a single schema and reuses one key to avoid clutter in Redis.
- Respects MEMX_BASE_URL and MEMX_API_KEY if provided; otherwise defaults to local dev.
"""

import os
import sys
from memx_sdk import memxContext


BASE_URL = os.getenv("MEMX_BASE_URL")  # memxContext already defaults to http://127.0.0.1:8000
API_KEY = os.getenv("MEMX_API_KEY", "local_dev_key")
KEY_WITH_SCHEMA = os.getenv("MEMX_TEST_KEY_WITH_SCHEMA", "agent:goal:with-schema")
KEY_NO_SCHEMA = os.getenv("MEMX_TEST_KEY_NO_SCHEMA", "agent:goal:no-schema")

SCHEMA = {
    "type": "object",
    "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"}
    },
    "required": ["x", "y"]
}

WITH_SCHEMA_PAYLOAD = {"x": 1, "y": 7}
WITHOUT_SCHEMA_PAYLOAD = {"note": "no schema applied here"}
READ_AFTER_WRITES = int(os.getenv("MEMX_READ_TIMES", "1"))  # set >1 to intentionally repeat reads


def main():
    ctx = memxContext(api_key=API_KEY, base_url=BASE_URL)

    def set_and_get(key: str, payload: dict, set_schema: bool = False):
        try:
            if set_schema:
                print(f"[schema] setting schema for {key}")
                ctx.set_schema(key, SCHEMA)
            print(f"[set] writing {key}: {payload}")
            ctx.set(key, payload)
            got = ctx.get(key)
            print(f"[get] from {key} received:", got)
        except Exception as exc:
            print(f"Set/get failed for {key}:", exc)
            sys.exit(1)

    # Subscribe to value events for both keys
    def sub_callback(msg):
        print("[sub:value] received:", msg)

    ctx.subscribe(KEY_WITH_SCHEMA, sub_callback)
    ctx.subscribe(KEY_NO_SCHEMA, sub_callback)

    # One key with schema (validated), one key without schema (freeform)
    set_and_get(KEY_WITH_SCHEMA, WITH_SCHEMA_PAYLOAD, set_schema=True)
    set_and_get(KEY_NO_SCHEMA, WITHOUT_SCHEMA_PAYLOAD, set_schema=False)

    # Multiple reads of each key to verify persistence
    for key in (KEY_WITH_SCHEMA, KEY_NO_SCHEMA):
        for j in range(1, READ_AFTER_WRITES + 1):
            try:
                got = ctx.get(key)
                print(f"[read] {key} repeat #{j} received:", got)
            except Exception as exc:
                print(f"Repeated read failed for {key} at iteration {j}:", exc)
                sys.exit(1)

    # Keep the process alive briefly to allow subscription callbacks to fire
    import time
    time.sleep(2)

    print("✅ smoke test succeeded")


if __name__ == "__main__":
    main()
