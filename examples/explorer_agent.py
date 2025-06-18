from context_sdk import AgentContext
import time
import requests

ctx = AgentContext(api_key="agent_key_1")

query_handled = False
summary_handled = False

def call_mistral(prompt: str) -> str:
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return res.json()["response"].strip() if res.status_code == 200 else "LLM error."

def on_memory(data):
    global query_handled, summary_handled

    key, value = data["key"], data["value"]

    if key == "memx:query" and not query_handled:
        context = ctx.get("memx:context")["value"]
        prompt = f"""You are a research assistant.
Given the query: "{value}" and context: "{context}", list one relevant source and one key observation."""
        print("🔍 ExplorerAgent: generating initial info with Mistral...")
        output = call_mistral(prompt)
        ctx.set("memx:search_results:0", output)
        ctx.set("memx:thoughts:0", f"Initial observation: {output}")
        query_handled = True

    elif key == "memx:summary" and not summary_handled:
        prompt = f"""You are a second-pass reviewer.
Based on this summary: "{value}", what additional consideration should be mentioned?"""
        print("🔄 ExplorerAgent: reacting to summary via Mistral...")
        thought = call_mistral(prompt)
        ctx.set("memx:thoughts:1", f"Follow-up observation: {thought}")
        summary_handled = True

ctx.subscribe("memx:query", on_memory)
ctx.subscribe("memx:summary", on_memory)

while True:
    time.sleep(1)
