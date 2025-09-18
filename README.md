# Custom ReAct Agent with Ollama 3.1 and LangGraph

This project demonstrates how to build a **custom ReAct agent** using Ollama 3.1 LLaMA model and LangGraph for tool-calling and multi-step reasoning.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Download Ollama 3.1 Model](#download-ollama-31-model)
- [Python Environment Setup](#python-environment-setup)
- [Project Structure](#project-structure)
- [Running the Agent](#running-the-agent)
- [Adding Custom Tools](#adding-custom-tools)
- [Notes](#notes)

---

## Requirements

- Python 3.10+
- Ollama CLI
- macOS or Linux (Windows supported via WSL)
- `pip` for Python dependencies

---

## Installation

### 1. Install Ollama CLI

#### macOS

```bash
brew install ollama
```

#### Linux

Follow instructions from the [Ollama GitHub repository](https://github.com/ollama/ollama).

#### Verify installation

```bash
ollama --help
```

---

## Download Ollama 3.1 Model

```bash
ollama pull llama3.1
```

This downloads the LLaMA 3.1 model locally.

---

## Python Environment Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows
```

Upgrade pip:

```bash
pip install --upgrade pip
```

---

## Install Dependencies

Create `requirements.txt`:

```txt
langchain-core>=0.2.0
langchain-ollama>=0.3.0
langgraph>=0.1.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

Example project layout:

```
project/
├─ .venv/
├─ reAct_agent.py
├─ requirements.txt
└─ README.md
```

---

## Using the Custom ReAct Agent

Follow the instructions in `reAct_agent.py` to define your tools, bind them to the Ollama Chat model, build the StateGraph, and run queries.

---

## Adding Custom Tools

- Define your Python function.
- Decorate with `@tool`.
- Add it to the `tools` list.
- Ollama will automatically be aware of it via `.bind_tools(tools)`.

---

## Notes

- Ollama 3.1 must be installed locally via the CLI (`ollama pull llama3.1`).  
- Use `ChatOllama(model="llama3.1")` to access the model in Python.  
- `.bind_tools()` allows the model to call your Python tools automatically.  
- LangGraph handles multi-step reasoning and tool execution.  
- You can extend the StateGraph with additional nodes for logging, validation, or persistence.
