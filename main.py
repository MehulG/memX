from fastapi import FastAPI, WebSocket, Request, HTTPException
from store import get_value, set_value
from schema import validate
from auth import is_authorized
from pubsub import subscribe, publish
import asyncio

app = FastAPI()

@app.get("/get")
def get(key: str):
    return get_value(key)

@app.post("/set")
async def set(request: Request):
    body = await request.json()
    key = body["key"]
    value = body["value"]
    api_key = request.headers.get("x-api-key")

    if not is_authorized(api_key, key):
        raise HTTPException(403)

    validate(key, value)

    updated = set_value(key, value)
    if updated:
        await publish(key, value)

    return {"ok": True, "updated": updated}

@app.websocket("/subscribe/{key}")
async def websocket_endpoint(websocket: WebSocket, key: str):
    await websocket.accept()
    print("connection open")
    subscribe(key, websocket)

    try:
        while True:
            # Keep it alive by pinging, even if we don't expect client input
            await asyncio.sleep(1)
    except Exception as e:
        print(f"[Server] WebSocket error: {e}")
