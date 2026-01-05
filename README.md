<div align="center">
  <img src="frontend/assets/logo.png" width="120" alt="Clarity Logo">
  
  <h1>Clarity</h1>
  
  <p>
    <strong>Intelligent Code Correction & Refactoring Engine</strong>
  </p>

  <!-- Badges: Catppuccin Mocha Themed -->
  <p>
    <img src="https://img.shields.io/badge/FastAPI-Backend-b4befe?style=for-the-badge&logo=fastapi&logoColor=1e1e2e" alt="FastAPI">
    <img src="https://img.shields.io/badge/HuggingFace-Transformers-fab387?style=for-the-badge&logo=huggingface&logoColor=1e1e2e" alt="Transformers">
    <img src="https://img.shields.io/badge/Docker-Containerized-a6e3a1?style=for-the-badge&logo=docker&logoColor=1e1e2e" alt="Docker">
    <img src="https://img.shields.io/badge/License-MIT-f38ba8?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🔮 Overview

## 📚 Documentation

**For Team & Evaluators:**
*   **[📖 The Journey (Start Here)](JOURNEY.md):** The comprehensive story, team roster, timeline, and troubleshooting war stories.
*   **[🎓 College Artifacts](docs/college/README.md):** Synopsis and Presentation slides.

**For Students / Beginners:**
*   **[🧠 Zero-to-Hero Concepts](docs/archive/LEARNING_RESOURCES.md):** What is Docker? What is an API? The core concepts explained simply.

**For Developers:**
*   **[🛠️ Developer Manual](DEVELOPMENT.md):** Architecture, Local Setup, and Deployment Guide.
*   **[AI Manifesto](docs/AI_MANIFESTO.md):** Our core philosophy, identity, and operating rules.

## Features

**Clarity** is an AI-powered code assistant designed to automatically detect bugs, suggest refactoring improvements, and enforce industry-standard naming conventions.

### ✨ Key Features
*   **Multi-Language Support (20+):** Auto-detects and corrects major languages:
    <p>
      <!-- Row 1: The Giants -->
      <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
      <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++">
      <img src="https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=java&logoColor=white" alt="Java">
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS">
      <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TS">
    </p>
    <p>
      <!-- Row 2: Systems & Modern -->
      <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go">
      <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust">
      <img src="https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white" alt="C#">
      <img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black" alt="C">
      <img src="https://img.shields.io/badge/Swift-F05138?style=for-the-badge&logo=swift&logoColor=white" alt="Swift">
    </p>
    <p>
      <!-- Row 3: Web & Scripting -->
      <img src="https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white" alt="PHP">
      <img src="https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white" alt="Ruby">
      <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin">
      <img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white" alt="Dart">
      <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white" alt="SQL">
    </p>
    <p>
      <!-- Row 4: Functional & Others -->
      <img src="https://img.shields.io/badge/Scala-DC322F?style=for-the-badge&logo=scala&logoColor=white" alt="Scala">
      <img src="https://img.shields.io/badge/Elixir-4B275F?style=for-the-badge&logo=elixir&logoColor=white" alt="Elixir">
      <img src="https://img.shields.io/badge/Erlang-A90533?style=for-the-badge&logo=erlang&logoColor=white" alt="Erlang">
      <img src="https://img.shields.io/badge/Racket-3C5280?style=for-the-badge&logo=racket&logoColor=white" alt="Racket">
    </p>

*   **Instant Feedback:** Optimized inference using **Hugging Face Transformers** and **PyTorch**.
*   **Adaptive Theming:** Full **Catppuccin** support with 4 flavors:
    *   🌻 **Latte** (Light)
    *   🪴 **Frappé** (Soft Dark)
    *   🌺 **Macchiato** (Medium Dark)
    *   🌿 **Mocha** (Deep Dark)
    *   🖥️ **Auto-Switching** based on system preference.
*   **Hybrid AI Engine:**
    *   **Local:** Qwen 2.5 Coder (Privacy-focused).
    *   **Cloud:** Google Gemini 1.5/2.0 (High Performance) with **Dynamic Model Discovery**.
*   **Professional UI:** Glassmorphism design with real-time Syntax Highlighting (Highlight.js).
*   **Mobile Ready:** Fully responsive design with touch-optimized controls and mobile-specific branding.
*   **Hybrid Deployment:** Run entirely locally (Docker) or connect to the Cloud backend out-of-the-box.

## 🏗️ Architecture

The system is containerized and composed of a decoupled frontend and inference engine.

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'darkMode': true, 'primaryColor': '#1e1e2e', 'edgeLabelBackground':'#181825', 'tertiaryColor': '#181825', 'mainBkg': '#1e1e2e', 'nodeBorder': '#b4befe', 'lineColor': '#cdd6f4'}}}%%
graph LR
    User(User) -->|Code Snippet| FE["Frontend (Nginx/HTML)"]
    FE -->|REST API| API["FastAPI Gateway"]
    API -->|Inference Request| Engine["Transformers Engine"]
    Engine -->|Corrected Code| API
    API -->|JSON Response| FE
    FE -->|Display| User
    
    style User fill:#fab387,stroke:#fab387,color:#1e1e2e
    style FE fill:#94e2d5,stroke:#94e2d5,color:#1e1e2e
    style API fill:#b4befe,stroke:#b4befe,color:#1e1e2e
    style Engine fill:#45475a,stroke:#cdd6f4,color:#cdd6f4
```

## 🚀 Quick Start

### 1. Instant Demo (Cloud Mode)
You don't need to install anything! The app defaults to **Cloud Mode**.
1.  Clone the repo: `git clone ...`
2.  Serve `frontend/` (e.g., `python -m http.server 3000`)
3.  Open `http://localhost:3000` in your browser.
4.  Start coding immediately.

### 2. Docker Compose (Local Privacy)
Run the entire stack locally for zero-latency, private inference.

```bash
docker compose up --build
```
*   **Frontend:** `http://localhost:80`
*   **API Docs:** `http://localhost:7860/docs`

*Switch the toggle in the footer to **Docker** to connect.*

### 3. Manual Development

**Backend:**
```bash
cd backend
# Install dependencies (using uv for speed)
pip install uv
uv pip install --system -r requirements.txt

# Run Server
uvicorn main:app --reload --port 7860
```

**Frontend:**
Serve the `frontend/` directory:
```bash
cd frontend
python -m http.server 3000
```
Open `http://localhost:3000`.
*Switch the toggle in the footer to **Local**.*

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 / JS | **Catppuccin** Themed UI with **Highlight.js** |
| **API Gateway** | FastAPI | High-performance async Python framework |
| **Inference** | Transformers | Native PyTorch Inference Pipeline |
| **Model** | Qwen 2.5 Coder 0.5B | State-of-the-art Coding LLM |
| **Serving** | Uvicorn / Nginx | Production-grade web servers |
| **DevOps** | Docker Compose | Multi-container orchestration |

## 📂 Repository Structure

```text
.
├── backend/                # FastAPI application & Model logic
│   ├── main.py             # API Entrypoint
│   └── model_service.py    # Inference logic & Language Detection
├── frontend/               # Static web assets
│   ├── index.html          # Main UI
│   ├── style.css           # Catppuccin Theme System
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