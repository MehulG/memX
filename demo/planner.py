import httpx

def planner_set_goal(goal):
    res = httpx.post(
        "http://localhost:8000/set",
        headers={"x-api-key": "agent_key_1"},
        json={"key": "agent:goal", "value": goal}
    )
    print("Planner set goal:", res.json())

if __name__ == "__main__":
    planner_set_goal("navigate hallway")
