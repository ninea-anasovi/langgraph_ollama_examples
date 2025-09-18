from typing import TypedDict, List, Union
from langgraph.graph import START, END, StateGraph
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage

llm = OllamaLLM(model="llama3.1")


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def process(state: AgentState) -> AgentState:
    """This node will solve request from input"""
    response = llm.invoke(state["messages"])   # returns string
    state["messages"].append(AIMessage(content=response))
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []
user_input = input("Enter: ")

while user_input != "end":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    print(result["messages"])
    user_input = input("Enter: ")