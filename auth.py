# API key → allowed key prefixes
acl = {
    "agent_key_1": ["agent:goal", "agent:state"],
    "planner_only": ["agent:goal"],
}

def is_authorized(api_key, key):
    scopes = acl.get(api_key, [])
    return any(key.startswith(scope.rstrip("*")) for scope in scopes)
