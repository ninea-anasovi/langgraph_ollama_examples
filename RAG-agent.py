import os
from typing import Annotated, Sequence, TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma

llm = ChatOllama(model="llama3.1", temperature=0)

embeddings = OllamaEmbeddings(
    model="llama3.1",
)

pdf_path = "Guide.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"File {pdf_path} not found")

pdf_loader = PyPDFLoader(pdf_path)
try:
    pages = pdf_loader.load()
    print(f"PDF succcessfully loaded with {len(pages)}")
except Exception as e:
    print(f"PDF could not be loaded: {e}")
    raise

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

page_split = text_splitter.split_documents(pages[100:120])

persist_directory = r'/Users/nineaanasovi/Documents/Coding/RAG-agents'
collection_name = "guide"

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

try:
    vectorestore = Chroma.from_documents(
        documents=page_split,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_directory,
    )
    print(f"Chroma restored to {vectorestore}")
except Exception as e:
    print(f"Chroma could not be restored to {e}")
    raise

retriever = vectorestore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k": 5}
)

@tool
def retriever_tool(query: str) -> str:
    """
    this tool searches and returns the information for a query in a Guide.
    """
    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Guide file"

    results = []
    for index, doc in enumerate(docs):
        results.append(f"Document {index+1}:\n{doc.page_content}")
    return "\n\n".join(results)

tools = [retriever_tool]

llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState) -> bool:
    "checks if last message contains tool calls"
    result = state["messages"][-1]
    return hasattr(result, "tool_calls") and len(result.tool_calls) > 0


system_prompt = """
You are an intelligent AI assistant who answers questions about Guide book based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""

tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary of our tools

def call_llm(state: AgentState) -> AgentState:
    """Function to call LLM with the current state."""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {"messages": [message]}


def take_action(state: AgentState) -> AgentState:
    """Execute tools from llm's respopnse"""
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

        if not t['name'] in tools_dict:  # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."

        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)
graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent",
        False: END
    }
)
graph.add_edge("retriever_agent", "llm")
graph.add_edge(START, "llm")
rag_agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")

    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages = [HumanMessage(content=user_input)]  # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})

        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()
