from fastapi import Request, HTTPException
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

async def validate_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if not key:
        raise HTTPException(status_code=401, detail="Missing API key")

    res = supabase.from_("api_keys").select("*").eq("key", key).eq("active", True).single().execute()
    if res.get("error") or not res.get("data"):
        raise HTTPException(status_code=403, detail="Invalid API key")

    request.state.api_key = res["data"]
