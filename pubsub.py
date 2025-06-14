from collections import defaultdict

subscriptions = defaultdict(list)

def subscribe(key, websocket):
    subscriptions[key].append(websocket)

async def publish(key, value):
    disconnected = []
    for ws in subscriptions.get(key, []):
        try:
            await ws.send_json({"key": key, "value": value})
        except Exception as e:
            print(f"[WARN] Failed to send to WebSocket: {e}")
            disconnected.append(ws)

    # Remove dead sockets
    for ws in disconnected:
        subscriptions[key].remove(ws)
