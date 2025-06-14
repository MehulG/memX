import jsonschema

schemas = {}

def register_schema(key, schema_dict):
    jsonschema.Draft7Validator.check_schema(schema_dict)
    schemas[key] = schema_dict

def validate_schema(key, value):
    schema = schemas.get(key)
    if schema:
        jsonschema.validate(instance=value, schema=schema)

def get_schema(key):
    return schemas.get(key)

def delete_schema(key):
    return schemas.pop(key, None)
