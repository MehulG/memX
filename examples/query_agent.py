from context_sdk import AgentContext
import time

ctx = AgentContext(api_key="agent_key_1")

ctx.set("memx:query", "Impacts of open-source LLMs on enterprise adoption")
ctx.set("memx:context", "Customer is preparing a tech brief for internal stakeholders")

print("🧠 QueryAgent initialized research context.")
