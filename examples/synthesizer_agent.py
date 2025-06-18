from context_sdk import AgentContext
import time
import requests
import hashlib

ctx = AgentContext(api_key="agent_key_1")
last_summary_hash = None
final_summary = ''
count = 0
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def call_mistral(prompt: str) -> str:
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        })
        res.raise_for_status()
        return res.json()["response"].strip()
    except Exception as e:
        print("❌ Mistral error:", e)
        return "LLM error."

def summarize():
    global last_summary_hash
    global final_summary
    global count
    try:
        query = ctx.get("memx:query")["value"]
        results = ctx.get("memx:search_results:0")["value"]
        thoughts = [ctx.get("memx:thoughts:0")["value"]]
        try:
            thoughts.append(ctx.get("memx:thoughts:1")["value"])
        except:
            pass  # optional follow-up thought
    except:
        print("⏳ Waiting for all inputs...")
        return

    prompt = f"""You are a summarizer agent.

Based on the following:
- Query: {query}
- Search Result: {results}
- Thoughts:
{"".join(f"- {t}\n" for t in thoughts)}

Write a final 2-sentence summary suitable for a leadership audience.
"""

    print("🧠 SynthesizerAgent: summarizing via Mistral...")
    summary = call_mistral(prompt)
    summary_hash = hash_text(summary)

    if summary_hash != last_summary_hash:
        ctx.set("memx:summary", summary)
        last_summary_hash = summary_hash
        final_summary = summary
        count += 1
        if count > 1:
            print("✅ Final summary written:\n", final_summary, "\n")
    else:
        print("⚠️ Summary unchanged — skipping write.")

def on_data(_):
    summarize()

# ctx.subscribe("memx:search_results:0", on_data)
ctx.subscribe("memx:thoughts:0", on_data)
ctx.subscribe("memx:thoughts:1", on_data)



while True:
    time.sleep(1)
