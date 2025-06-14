import time

store = {}

def get_value(key):
    return store.get(key)

def set_value(key, value):
    now = time.time()
    prev = store.get(key)
    if not prev or now > prev['ts']:
        store[key] = {'value': value, 'ts': now}
        return True
    return False
