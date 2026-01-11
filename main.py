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
    namespaced_key = getattr(request.state, "namespaced_key", key)
    return get_value(namespaced_key)

@app.post("/set")
async def set(request: Request):
    body = await request.json()
    value = body["value"]
    key = body["key"]

    await validate_api.validate_api_key(request, key, action="write")
    namespaced_key = getattr(request.state, "namespaced_key", key)

    try:
        validate_schema(namespaced_key, value)
    except jsonschema.exceptions.ValidationError as e:
        raise HTTPException(400, detail=str(e))

    updated = set_value(namespaced_key, value)
    if updated:
        await publish(namespaced_key, value)

    return {"ok": True, "updated": updated}

@app.websocket("/subscribe/{key}")
async def websocket_endpoint(websocket: WebSocket, key: str):
    await websocket.accept()
    namespaced_key = await validate_api.validate_websocket(websocket, key)
    if not namespaced_key:
        return
    print(f"[WebSocket] Subscribed to {namespaced_key}")
    subscribe(namespaced_key, websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        print(f"[WebSocket] closed: {namespaced_key}")

@app.post("/schema")
async def set_schema(request: Request):
    body = await request.json()
    key = body["key"]
    schema = body["schema"]

    await validate_api.validate_api_key(request, key, action="write")
    namespaced_key = getattr(request.state, "namespaced_key", key)

    try:
        register_schema(namespaced_key, schema)
    except jsonschema.exceptions.SchemaError as e:
        raise HTTPException(400, detail=f"Invalid schema: {e}")
    return {"ok": True}

@app.get("/schema")
async def fetch_schema(key: str, request: Request):
    await validate_api.validate_api_key(request, key, action="read")
    namespaced_key = getattr(request.state, "namespaced_key", key)
    schema = get_schema(namespaced_key)
    if not schema:
        raise HTTPException(404, detail="Schema not found")
    return {"key": key, "schema": schema}

@app.delete("/schema")
async def remove_schema(key: str, request: Request):
    await validate_api.validate_api_key(request, key, action="write")
    namespaced_key = getattr(request.state, "namespaced_key", key)
    deleted = delete_schema(namespaced_key)
    if not deleted:
        raise HTTPException(404, detail="Schema not found")
    return {"ok": True}
