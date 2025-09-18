from typing import Dict, TypedDict, List
from langgraph.graph import  StateGraph, START, END

class AgentState(TypedDict):
    name: str
    age: str
    skills: List[str]
    final: str

def  first_node(state: AgentState) -> AgentState:
    """
    This is first node of the sequence
    """
    state["final"] = f"Hi, {state['name']}"
    return state

def second_node(state: AgentState) -> AgentState:
    """
    This is second node of the sequence
    """
    state["final"] = f"{state['final']}, you are {state['age']} years old"
    return state

def third_node(state: AgentState) -> AgentState:
    """
    This is third node of the sequence
    """
    state["final"] = f"{state['final']}, you are {state['skills']} years old"
    return state

graph = StateGraph(AgentState)
graph.add_node("name",first_node)
graph.add_node("age",second_node)
graph.add_node("skills",third_node)
graph.set_entry_point("name")
graph.add_edge("name", "age")
graph.add_edge("age", "skills")
graph.set_finish_point("skills")
app = graph.compile()
result = app.invoke({
    "name": "Nato",
    "age": "10",
    "skills": ["java", "python"],
})

print(result["final"])