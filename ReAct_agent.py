from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# ---- Define agent state ----
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# ---- Tools ----
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [add, subtract, multiply]

# ---- Model ----
model = ChatOllama(model="llama3.1").bind_tools(tools)

# ---- Reasoning node ----
def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are my AI assistant. Please answer my query with the best of your ability."
    )
    # Pass list of BaseMessages, not dict
    messages = [system_prompt] + list(state["messages"])
    response = model.invoke(messages)
    return {"messages": list(state["messages"]) + [response]}

# ---- Conditional edge ----
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    # check if model wants to call a tool
    if getattr(last_message, "tool_calls", None):
        return "continue"
    return "end"

# ---- Graph wiring ----
graph = StateGraph(AgentState)
graph.add_node("reason", model_call)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "reason")
graph.add_conditional_edges("reason", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "reason")

app = graph.compile()

# ---- Run & print ----
def print_stream(stream):
    for s in stream:
        msg = s["messages"][-1]
        msg.pretty_print()

# Inputs as a dict for the state
inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))