# Custom Agents with Ollama 3.1 and LangGraph

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
ollama --help
ollama pull llama3.1
```
