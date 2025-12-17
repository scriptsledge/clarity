<div align="center">
  <img src="frontend/assets/logo.png" width="120" alt="Clarity Logo">
  
  <h1>Clarity</h1>
  
  <p>
    <strong>Intelligent Code Correction & Refactoring Engine</strong>
  </p>

  <!-- Badges: Catppuccin Mocha Themed -->
  <p>
    <img src="https://img.shields.io/badge/FastAPI-Backend-b4befe?style=for-the-badge&logo=fastapi&logoColor=1e1e2e" alt="FastAPI">
    <img src="https://img.shields.io/badge/PyTorch-AI-94e2d5?style=for-the-badge&logo=pytorch&logoColor=1e1e2e" alt="PyTorch">
    <img src="https://img.shields.io/badge/Docker-Containerized-a6e3a1?style=for-the-badge&logo=docker&logoColor=1e1e2e" alt="Docker">
    <img src="https://img.shields.io/badge/License-MIT-f38ba8?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🔮 Overview

**Clarity** is an AI-powered code assistant designed to automatically detect bugs, suggest refactoring improvements, and enforce industry-standard naming conventions across multiple languages (Python, C++, Java, JS).

Built on a robust **Microservices Architecture**, it leverages state-of-the-art LLMs (via Hugging Face Transformers) to understand code semantics and intent.

## 🏗️ Architecture

The system is containerized and composed of a decoupled frontend and inference engine.

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'darkMode': true, 'primaryColor': '#1e1e2e', 'edgeLabelBackground':'#181825', 'tertiaryColor': '#181825', 'mainBkg': '#1e1e2e', 'nodeBorder': '#b4befe', 'lineColor': '#cdd6f4'}}}%%
graph LR
    User[User] -->|Code Snippet| FE[Frontend (Nginx/HTML)];
    FE -->|REST API| API[FastAPI Gateway];
    API -->|Inference Request| Model[Transformer Model];
    Model -->|Corrected Code| API;
    API -->|JSON Response| FE;
    FE -->|Display| User;
    
    style User fill:#fab387,stroke:#fab387,color:#1e1e2e
    style FE fill:#94e2d5,stroke:#94e2d5,color:#1e1e2e
    style API fill:#b4befe,stroke:#b4befe,color:#1e1e2e
    style Model fill:#45475a,stroke:#cdd6f4,color:#cdd6f4
```

## 🚀 Quick Start

### 1. Docker Compose (Recommended)
Launch the entire stack with a single command.

```bash
git clone https://github.com/your-username/clarity.git
cd clarity
docker compose up --build
```
*   **Frontend:** `http://localhost:80`
*   **API Docs:** `http://localhost:8000/docs`

### 2. Manual Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
Simply serve the `frontend/` directory using any static file server (e.g., `python -m http.server 3000`).

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 / JS | Lightweight, vanilla implementation with **Mocha** styling |
| **API Gateway** | FastAPI | High-performance async Python framework |
| **Inference** | PyTorch / Transformers | Hugging Face LLM integration |
| **Serving** | Uvicorn / Nginx | Production-grade web servers |
| **DevOps** | Docker Compose | Multi-container orchestration |

## 📂 Repository Structure

```text
.
├── backend/                # FastAPI application & Model logic
│   ├── main.py             # API Entrypoint
│   └── model_service.py    # Inference logic
├── frontend/               # Static web assets
│   ├── index.html          # Main UI
│   ├── style.css           # Catppuccin Mocha Theme
│   └── assets/             # Generated logos
├── generate_assets.py      # Procedural asset generator script
└── docker-compose.yml      # Orchestration config
```

## 🎨 Asset Generation

This project includes a procedural asset generator to ensure brand consistency.
```bash
python generate_assets.py
```
*Generates `frontend/assets/logo.png`.*

## 📜 License

Distributed under the MIT License.

---
<div align="center">
  <small>Designed with 💜 and ☕ (Catppuccin Mocha)</small>
</div>