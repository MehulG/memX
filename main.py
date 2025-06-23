from fastapi import FastAPI, WebSocket, Request, HTTPException
from store import get_value, set_value
from schema import validate_schema
from auth import is_authorized
from pubsub import subscribe, publish
from schema import register_schema, validate_schema, get_schema, delete_schema
import asyncio
import jsonschema
import validate_api_key

app = FastAPI()

@app.get("/get")
def get(key: str):
    return get_value(key)

@app.post("/set")
async def set(request: Request):
    await validate_api_key(request)
    body = await request.json()
    key = body["key"]
    value = body["value"]
    # api_key = request.headers.get("x-api-key")

    # if not api_key or not is_authorized(api_key, key):
    #     raise HTTPException(403, detail="Forbidden: key not allowed")

    try:
        validate_schema(key, value)
    except jsonschema.exceptions.ValidationError as e:
        raise HTTPException(400, detail=str(e))

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

@app.post("/schema")
async def set_schema(request: Request):
    body = await request.json()
    key = body["key"]
    schema = body["schema"]
    api_key = request.headers.get("x-api-key")

    if not api_key or not is_authorized(api_key, key):
        raise HTTPException(403)
    try:
        register_schema(key, schema)
    except jsonschema.exceptions.SchemaError as e:
        raise HTTPException(400, detail=f"Invalid schema: {e}")
    return {"ok": True}

@app.get("/schema")
def fetch_schema(key: str, request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or not is_authorized(api_key, key):
        raise HTTPException(403)
    schema = get_schema(key)
    if not schema:
        raise HTTPException(404, detail="Schema not found")
    return {"key": key, "schema": schema}

@app.delete("/schema")
def remove_schema(key: str, request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or not is_authorized(api_key, key):
        raise HTTPException(403)
    deleted = delete_schema(key)
    if not deleted:
        raise HTTPException(404, detail="Schema not found")
    return {"ok": True}
