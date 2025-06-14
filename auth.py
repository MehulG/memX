acl = {
    "agent_key_1": ["agent:*"],
    "planner_key": ["agent:planner:*"],
}

def is_authorized(api_key, key):
    scopes = acl.get(api_key, [])
    return any(key.startswith(scope.rstrip("*")) for scope in scopes)
