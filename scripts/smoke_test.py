import os
import sys
import httpx


BASE_URL = os.getenv("MEMX_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("MEMX_SMOKE_API_KEY", "local_dev_key")
SMOKE_KEY = os.getenv("MEMX_SMOKE_KEY", "agent:smoke")

schema = {
    "type": "object",
    "properties": {"message": {"type": "string"}},
    "required": ["message"],
}
value = {"message": "hello from smoke test"}


def main():
    headers = {"x-api-key": API_KEY}
    with httpx.Client(base_url=BASE_URL, headers=headers, timeout=5) as client:
        print(f"[schema] setting schema for {SMOKE_KEY}")
        res = client.post("/schema", json={"key": SMOKE_KEY, "schema": schema})
        res.raise_for_status()

        print(f"[set] writing value to {SMOKE_KEY}")
        res = client.post("/set", json={"key": SMOKE_KEY, "value": value})
        res.raise_for_status()

        print(f"[get] reading value from {SMOKE_KEY}")
        res = client.get("/get", params={"key": SMOKE_KEY})
        res.raise_for_status()

        print("Result:", res.json())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("Smoke test failed:", exc, file=sys.stderr)
        sys.exit(1)
