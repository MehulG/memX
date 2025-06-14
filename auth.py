import json

with open("config/acl.json") as f:
    acl = json.load(f)

def is_authorized(api_key, key):
    scopes = acl.get(api_key, [])
    return any(key.startswith(scope.rstrip("*")) for scope in scopes)
