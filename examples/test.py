from memx_sdk import memxContext


# Use the local dev key defined in config/acl.json when running against the local server.
ctx = memxContext(api_key="local_dev_key")

ctx.set_schema("agent:goal", {
    "type": "object",
    "properties": {
      "x": { "type": "number" },
      "y": { "type": "number" }
    },
    "required": ["x", "y"]
  })

get1 = ctx.get("agent:goal")

print(get1)

ctx.set("agent:goal", {"x":1, "y":7})

get2 = ctx.get("agent:goal")

print(get2)

for i in range(0,10):
    ctx.set_schema("agent:goal:"+str(i), {
    "type": "object",
    "properties": {
      "x": { "type": "number" },
      "y": { "type": "number" }
    },
    "required": ["x", "y"]
    })
    ctx.set("agent:goal"+str(i), {"x":i, "y":i*2})
    get1 = ctx.get("agent:goal"+str(i))

    print(get1)


