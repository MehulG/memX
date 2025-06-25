from fastapi import FastAPI, WebSocket, Request, HTTPException
from store import get_value, set_value
from pubsub import subscribe, publish
from schema import register_schema, validate_schema, get_schema, delete_schema
import asyncio
import jsonschema
import validate_api

app = FastAPI()

@app.get("/get")
async def get(key: str, request: Request):
    await validate_api.validate_api_key(request, key, action="read")
    return get_value(key)

@app.post("/set")
async def set(request: Request):
    body = await request.json()
    value = body["value"]
    key = body["key"]

    await validate_api.validate_api_key(request, key, action="write")

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
    if not await validate_api.validate_websocket(websocket, key):
        return
    print(f"[WebSocket] Subscribed to {key}")
    subscribe(key, websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        print(f"[WebSocket] closed: {key}")

@app.post("/schema")
async def set_schema(request: Request):
    body = await request.json()
    key = body["key"]
    schema = body["schema"]

    await validate_api.validate_api_key(request, key, action="write")

    try:
        register_schema(key, schema)
    except jsonschema.exceptions.SchemaError as e:
        raise HTTPException(400, detail=f"Invalid schema: {e}")
    return {"ok": True}

@app.get("/schema")
async def fetch_schema(key: str, request: Request):
    await validate_api.validate_api_key(request, key, action="read")
    schema = get_schema(key)
    if not schema:
        raise HTTPException(404, detail="Schema not found")
    return {"key": key, "schema": schema}

@app.delete("/schema")
async def remove_schema(key: str, request: Request):
    await validate_api.validate_api_key(request, key, action="write")
    deleted = delete_schema(key)
    if not deleted:
        raise HTTPException(404, detail="Schema not found")
    return {"ok": True}
