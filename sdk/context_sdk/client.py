import httpx
import asyncio
import websockets
import threading
import json

class memxContext:
    def __init__(self, api_key, base_url="https://memx-production.up.railway.app"):
        self.api_key = api_key
        self.base_url = base_url

    def set(self, key, value):
        res = httpx.post(
            f"{self.base_url}/set",
            headers={"x-api-key": self.api_key},
            json={"key": key, "value": value}
        )
        res.raise_for_status()
        return res.json()

    def get(self, key):
        res = httpx.get(
            f"{self.base_url}/get",
            headers={"x-api-key": self.api_key},
            params={"key": key}
        )
        res.raise_for_status()
        return res.json()

    def subscribe(self, key, callback):
        def _listen():
            uri = f"{self.base_url.replace('http', 'ws')}/subscribe/{key}"
            async def _inner():
                async with websockets.connect(uri, additional_headers={"x-api-key": self.api_key}) as ws:
                    while True:
                        try:
                            msg = await ws.recv()
                            data = json.loads(msg)
                            callback(data)
                        except Exception as e:
                            print("[WebSocket error]", e)
                            break
            asyncio.run(_inner())

        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()

    def set_schema(self, key, schema):
        res = httpx.post(
            f"{self.base_url}/schema",
            headers={"x-api-key": self.api_key},
            json={"key": key, "schema": schema}
        )
        res.raise_for_status()
        return res.json()

    def get_schema(self, key):
        res = httpx.get(
            f"{self.base_url}/schema",
            headers={"x-api-key": self.api_key},
            params={"key": key}
        )
        res.raise_for_status()
        return res.json()

    def delete_schema(self, key):
        res = httpx.delete(
            f"{self.base_url}/schema",
            headers={"x-api-key": self.api_key},
            params={"key": key}
        )
        res.raise_for_status()
        return res.json()

