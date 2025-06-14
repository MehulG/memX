import asyncio
import websockets
import json

async def executor():
    uri = "ws://localhost:8000/subscribe/agent:goal"
    try:
        async with websockets.connect(uri) as websocket:
            print("[Executor] Connected. Waiting for goals...")
            while True:
                try:
                    msg = await websocket.recv()
                    data = json.loads(msg)
                    print(f"[Executor] Received goal: {data['value']}")
                    # Simulate doing something
                    await asyncio.sleep(1)
                except websockets.exceptions.ConnectionClosed as e:
                    print("[Executor] WebSocket closed:", e)
                    break
                except Exception as e:
                    print("[Executor] Error while receiving:", e)
    except Exception as e:
        print("[Executor] Could not connect to server:", e)

if __name__ == "__main__":
    asyncio.run(executor())
