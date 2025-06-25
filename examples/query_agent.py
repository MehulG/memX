from context_sdk import memxContext

ctx = memxContext(api_key="agent_key_1")

ctx.set("memx:query", "Impacts of open-source LLMs on enterprise adoption")
ctx.set("memx:context", "Customer is preparing a technical brief for leadership")

print("🧠 QueryAgent: seeded query + context")
