import jsonschema

schemas = {}

def validate(key, value):
    schema = schemas.get(key)
    if not schema:
        return True  # No schema
    jsonschema.validate(instance=value, schema=schema)
    return True
