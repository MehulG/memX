import fnmatch
import json
from fastapi import Request, HTTPException, WebSocket
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_URL and SUPABASE_SERVICE_KEY else None

# Fallback ACL for local/dev when Supabase is not configured or unreachable.
try:
    with open("config/acl.json") as f:
        LOCAL_ACL = json.load(f)
except Exception:
    LOCAL_ACL = {}

def _check_scope(scopes: dict, action: str, key: str, user_id: str):
    namespaced_key = key if not user_id else f"{user_id[:8]}:{key}"
    return any(fnmatch.fnmatch(namespaced_key, pattern) for pattern in scopes.get(action, []))

def _apply_namespace(key: str, record: dict) -> str:
    user_id = record.get("user_id", "")
    return key if not user_id else f"{user_id[:8]}:{key}"

async def validate_api_key(request: Request, key: str, action: str = "write"):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    record = None
    if supabase:
        try:
            res = supabase.from_("api_keys").select("*").eq("key", api_key).eq("active", True).execute()
            if res.data:
                record = res.data[0]
        except Exception as e:
            print("[validate_api] Supabase lookup failed, falling back to local ACL:", e)

    if not record:
        local_patterns = LOCAL_ACL.get(api_key, [])
        if not local_patterns:
            raise HTTPException(status_code=403, detail="Invalid or inactive API key")
        record = {"user_id": "", "scopes": {"read": local_patterns, "write": local_patterns}}

    scopes = record.get("scopes", {})
    user_id = record.get("user_id", "")

    if not _check_scope(scopes, action, key, user_id):
        raise HTTPException(status_code=403, detail=f"{action.upper()} not permitted for key '{key}'")

    request.state.api_key = record
    request.state.namespaced_key = _apply_namespace(key, record)

async def validate_websocket(websocket: WebSocket, key: str):
    api_key = websocket.headers.get("x-api-key")
    if not api_key:
        await websocket.close(code=4401, reason="Missing API key")
        return False

    record = None
    if supabase:
        try:
            res = supabase.table("api_keys").select("*").eq("key", api_key).eq("active", True).execute()
            if res.data:
                record = res.data[0]
        except Exception as e:
            print("[validate_api] Supabase lookup failed for websocket, falling back to local ACL:", e)

    if not record:
        local_patterns = LOCAL_ACL.get(api_key, [])
        if not local_patterns:
            await websocket.close(code=4403, reason="Invalid API key")
            return False
        record = {"user_id": "", "scopes": {"read": local_patterns, "write": local_patterns}}

    scopes = record.get("scopes", {})
    user_id = record.get("user_id", "")

    if not _check_scope(scopes, "read", key, user_id):
        await websocket.close(code=4403, reason="Unauthorized to subscribe to this key")
        return False

    return _apply_namespace(key, record)
