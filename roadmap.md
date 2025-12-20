# 🗺️ Project Roadmap: The Journey

> "A plan is a bridge to your dreams."

This document outlines the strategic evolution of Clarity from concept to production-grade AI application.

---

### 📚 Table of Contents
- [Navigation](#-navigation)
- [Mission Objective](#-mission-objective)
- [Strategic Phases](#-strategic-phases)
- [Deployment Strategy](#-deployment-strategy)

---

### 🧭 Navigation
- **[⬅️ Back to Home](README.md)**
- **[👥 Team Roster](projects.md)**

---

## 🎯 Mission Objective
**To democratize code quality.**
We aim to build a zero-friction, intelligent code refactoring tool that helps students and juniors write industry-standard code instantly.

---

## 🛤️ Strategic Phases

### ✅ Phase 1: The Foundation (Backend Skeleton)
*Status: Completed*
- [x] Initialize Git repository structure.
- [x] Build FastAPI scaffolding (`POST /api/correct`).
- [x] Create mock Inference logic for frontend integration testing.

### ✅ Phase 2: The Interface (Frontend UI)
*Status: Completed*
- [x] Develop glassmorphism UI with HTML5/CSS3.
- [x] Implement **Catppuccin** Theme Engine (Latte/Mocha/Frappé/Macchiato).
- [x] Add real-time syntax highlighting with **Highlight.js**.
- [x] Build responsive layout and font controls.

### ✅ Phase 3: The Intelligence (AI Integration)
*Status: Completed*
- [x] Integrate `llama.cpp` for CPU-optimized inference.
- [x] Deploy **Qwen 2.5 Coder 7B (GGUF)** model.
- [x] Implement heuristic Language Detection (20+ languages).
- [x] Engineer system prompts for "Student Mentor" persona.

### ✅ Phase 4: Reliability & Polish
*Status: Completed*
- [x] Fix Race Conditions in API calls.
- [x] Implement independent Font Size controls.
- [x] Add detailed error handling and "Troubleshooting" docs.
- [x] Optimize context window (`n_ctx=8192`) for large files.

### 🔄 Phase 5: Production Deployment
*Status: In Progress / Continuous*
- [x] Containerize Backend (Docker).
- [x] Deploy to **Hugging Face Spaces**.
- [x] Deploy Frontend to Vercel/Pages.
- [ ] Implement user accounts (Future).
- [ ] Add history tracking (Future).

---

## 🚀 Deployment Strategy

### The "Free Tier" Architecture
We utilize a hybrid cloud strategy to keep operating costs at $0.

| Component | Host | Reason |
| :--- | :--- | :--- |
| **Frontend** | **Vercel** / **GitHub Pages** | Fast CDN, automatic SSL, zero config. |
| **Backend** | **Hugging Face Spaces** | Free container hosting with enough RAM (16GB) to run 7B models. |
| **Model** | **Hugging Face Hub** | Models are streamed directly to the container, no storage cost. |

---

> *Updated December 2025*
