# 🧠 Agentic App Builder (LLM-Driven)

An **Agentic App Builder** that converts **natural language instructions into a working application** using an **LLM-first planner, agent orchestration, context memory, and dynamic UI generation**.

This project demonstrates how modern **agentic AI systems** reason, plan, execute, and iterate over user intent.

---

## 🚀 What This Project Does

- Takes a **natural language description** of an app
- Uses an **LLM-based Planner Agent** to understand intent
- Orchestrates multiple agents to build the app
- Generates **working application logic**
- Renders a **dynamic Streamlit UI**
- Supports **incremental updates using context memory**

Example:
Design a todo app.
Add, list and delete tasks.
Rename add button to ranit.
Disable delete button.


➡️ The UI updates automatically — no code changes required.

---

## 🧩 Core Features

### ✅ Agentic Orchestration
- **Planner Agent (LLM-based)** – understands user intent
- **Architect Agent** – defines app structure
- **Coder Agent** – generates executable logic
- **Reviewer Agent** – validates and refines output

### ✅ LLM-First Reasoning
- Uses **local open-source LLM (Mistral via Ollama)**
- Converts unstructured text → structured JSON plan
- Safe execution with validation + fallbacks

### ✅ Context Memory (Last 3 Prompts)
- Remembers previous instructions
- Supports **continuation prompts**
- Enables true incremental updates

Example:
Now enable delete and rename it to remove_task


### ✅ Dynamic UI Generation
- Buttons are **not hardcoded**
- UI is generated from an **action registry**
- Buttons can be:
  - Renamed
  - Disabled
  - Added dynamically
  - Removed safely

### ✅ Robust & Safe
- Timeout handling for LLM calls
- Retry + fallback logic
- Validation before UI execution
- No Streamlit crashes from bad LLM output

---

## 🏗️ Architecture Overview

User Prompt
↓
LLM Planner Agent (with context memory)
↓
Validated Action Registry
↓
Orchestrator
↓
Architect → Coder → Reviewer
↓
Dynamic Streamlit UI


---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – frontend
- **Ollama** – local LLM runtime
- **Mistral** – open-source LLM
- **Agentic Design Pattern**

---
## 📂 Project Structure

├── app.py # Streamlit frontend
├── orchestrator.py # Agent orchestration logic
├── agents/
│ ├── planner.py # LLM-based planner with memory
│ ├── architect.py # App structure design
│ ├── coder.py # Code generation
│ └── reviewer.py # Validation & refinement
├── README.md


---
## ▶️ How to Run Locally

### 1️⃣ Install Ollama
Download and install from:
https://ollama.com

Pull the model:
```bash
ollama pull mistral

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install streamlit

4️⃣ Run the App
streamlit run app.py

🧪 Demo Prompts (Recommended)
Initial Build
Design a minimal todo app.
Add, list and delete tasks.
Rename add button to ranit.
Disable delete button.

Iteration
Now enable delete and rename it to remove_task.

Extension
Add a clear all button to remove all tasks.

👤 Author
Ranit Pal
📧 Email: ranitpal57@gmail.com

🐙 GitHub: https://github.com/ranit57