from collections import defaultdict

# subscriptions[event][key] -> list of websockets
subscriptions = defaultdict(lambda: defaultdict(list))

def subscribe(key, websocket, event: str = "value"):
    subscriptions[event][key].append(websocket)

async def publish(key, payload, event: str = "value"):
    disconnected = []
    for ws in subscriptions.get(event, {}).get(key, []):
        try:
            await ws.send_json(payload)
        except Exception as e:
            print(f"[WARN] Failed to send to WebSocket: {e}")
            disconnected.append(ws)

    # Remove dead sockets
    for ws in disconnected:
        subscriptions[event][key].remove(ws)
