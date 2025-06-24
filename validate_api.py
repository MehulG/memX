import fnmatch
from fastapi import Request, HTTPException, WebSocket
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

def _check_scope(scopes: dict, action: str, key: str, user_id: str):
    namespaced_key = f"{user_id[:8]}:{key}"
    return any(fnmatch.fnmatch(namespaced_key, pattern) for pattern in scopes.get(action, []))

async def validate_api_key(request: Request, key: str, action: str = "write"):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    res = supabase.from_("api_keys").select("*").eq("key", api_key).eq("active", True).single().execute()
    if res.get("error") or not res.get("data"):
        raise HTTPException(status_code=403, detail="Invalid API key")

    record = res["data"]
    scopes = record.get("scopes", {})
    user_id = record.get("user_id", "")

    if not _check_scope(scopes, action, key, user_id):
        raise HTTPException(status_code=403, detail=f"{action.upper()} not permitted for key '{key}'")

    request.state.api_key = record

async def validate_websocket(websocket: WebSocket, key: str) -> bool:
    api_key = websocket.headers.get("x-api-key")
    if not api_key:
        await websocket.close(code=4401, reason="Missing API key")
        return False

    res = supabase.table("api_keys").select("*").eq("key", api_key).eq("active", True).execute()
    if not res.data:
        await websocket.close(code=4403, reason="Invalid API key")
        return False

    record = res.data[0]
    scopes = record.get("scopes", {})
    user_id = record.get("user_id", "")

    if not _check_scope(scopes, "read", key, user_id):
        await websocket.close(code=4403, reason="Unauthorized to subscribe to this key")
        return False

    return True
