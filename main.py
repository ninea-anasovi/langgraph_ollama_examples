from typing import Dict, TypedDict, List
import random
from langgraph.graph import  StateGraph, START, END
from parso.python.tokenize import group


class AgentState(TypedDict):
    name: str
    number: list[int]
    counter: int

def greeting(state: AgentState) -> AgentState:
    """Greeting node which says hi to the person"""
    state["name"] = f"Hello, {state['name']}"
    state["counter"] = 0
    return state

def random_node(state: AgentState) -> AgentState:
    """Random node which gives random numbers"""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1
    return state

def should_continue(state: AgentState) -> AgentState:
    """function decides if it Should continue"""
    if state["counter"] < 5:
        print("entering loop", state["counter"])
        return "loop"
    else:
        return "exit"


graph = StateGraph(AgentState)
graph.add_node("greeting", greeting)
graph.add_node("random", random_node)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "random")
graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END,
    }
)
app = graph.compile()
res = app.invoke({
    "name": "Joe",
    "number": [],
    "counter": -11
})
print(res)