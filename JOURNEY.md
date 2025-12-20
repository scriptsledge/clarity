# 🛤️ The Clarity Journey: From Concept to Cloud

> "A chronicle of the Minor Project 2025 development lifecycle."

This document serves as the **comprehensive history** of Clarity. It details the struggles, decisions, learning curves, and evolution of the project.

---

## 👥 The Team
**Clarity (Project #18)** was brought to life by:
*   **Nipun Lakhera**
*   **Sahil Raikwar**
*   **Mo Zaid Sheikh**
*   **Shivansh Nigam**

---

## 📅 The Evolution Timeline

### Phase 1: The Vision & First Steps (Backend Skeleton)
**Initial Goal:** To create a simple API that could "correct" code.
**The Plan:** We started with a basic `FastAPI` wrapper. We didn't even have an AI yet; we just mocked the response to ensure our frontend could talk to our backend.

**Technical Challenges:**
*   **Challenge:** Understanding how to structure a Python project for the web.
*   **Learning:** We learned about `uvicorn` (the server) and `fastapi` (the framework). We realized we needed `CORS` middleware immediately because our frontend (port 5500) couldn't talk to our backend (port 8000) due to browser security.

---

### Phase 2: Building the Interface (Frontend UI)
**Initial Goal:** A simple HTML page to accept text.
**Evolution:** We didn't want a boring bootstrap look. We aimed for **Glassmorphism**.

**The "Theme" Struggle:**
*   **Challenge:** Implementing Dark Mode was harder than expected. We started with a simple toggle, but the colors felt off.
*   **Breakthrough:** We discovered **Catppuccin**. We decided to go all-in on this palette.
*   **The "Opacity" Bug:** When we implemented the "Latte" (Light) theme, the sidebar disappeared because our transparency values were tuned for Dark mode. We had to implement a complex CSS variable system where `body.theme-latte` overrides specific RGBA alpha channels to ensure the sidebar remained visible against the light background.

---

### Phase 3: The AI Brain (The Pivot)
**Initial Goal:** Use `transformers` and PyTorch with a small model.
**The Crisis:** When we tried to run a 3B parameter model on our local laptops, it crashed or took 30+ seconds to respond. Our 16GB RAM was barely enough for the model + OS + Browser.

**The "llama.cpp" Solution:**
*   **Research:** We found the `llama.cpp` project, which allows LLMs to run on CPUs efficiently using "Quantization".
*   **Implementation:** We switched from the standard Hugging Face pipeline to `llama-cpp-python`.
*   **Result:** We could run a **7B Parameter Model (Qwen 2.5)** with only 6GB of RAM usage and response times under 5 seconds. This was a massive win for the project's viability.

---

## 🛑 The Troubleshooting Log (War Stories)

> "Mistakes are the portals of discovery."

### 1. The `GGML_ASSERT` Crash
**Symptom:** The backend server would crash silently or with a segmentation fault when processing code.
```text
ggml-cpu/ops.cpp:5399: GGML_ASSERT(i1 >= 0 && i1 < ne1) failed
```
**Root Cause:**
Two distinct issues were colliding:
1.  **Context Overflow:** The prompt + generation exceeded the `n_ctx` (Context Window) of the model.
2.  **Race Condition:** The Frontend's "Health Check" was aggressively re-enabling the "Optimize" button while a request was still processing. If the user double-clicked, `llama.cpp` (running single-threaded per slot) would corrupt its memory state.

**Solution:**
*   **Backend:** Increased `n_ctx` to `4096` (and `8192` where RAM permits).
*   **Frontend:** Implemented a **Mutex Lock (`isProcessing`)**. The UI now strictly disables interaction until the current transaction completes.

### 2. The "Brown Box" Syntax Highlighting
**Symptom:** Code blocks appeared with an ugly, opaque background color that clashed with the Glassmorphism UI.
**Solution:**
We forced a transparent background in our global CSS to let the Catppuccin surface shine through:
```css
code.hljs { background: transparent !important; }
```

---

## 🏗️ The "Free Tier" Architecture Strategy

One of our primary constraints was **zero cost**. Hosting AI models usually costs money (GPUs). We engineered a solution using specific free-tier offerings:

### 🐳 Understanding the Dockerfile
We utilize **Docker** to "freeze" our environment. This ensures that if it runs on our laptop, it runs on the cloud.

**Key Concepts:**
*   **`FROM python:3.10-slim`**: We start with a minimal Linux OS.
*   **`RUN useradd ...`**: Security. By default, Docker runs as `root`. Hugging Face rejects root containers for security. We created a user named `user` (ID 1000).
*   **`EXPOSE 7860`**: Docker containers are isolated. We must explicitly "open a hole" (port 7860) to let traffic in.

### 📚 Vercel Concepts
Vercel is not just a server; it's a deployment platform.
*   **Deployment:** Every time we `git push`, Vercel builds a *new, immutable* version of our site. This allows us to "roll back" instantly if we break something.

---

## 🔮 The Future
*   **User Accounts:** Storing history in a database.
*   **Diff View:** Showing the "Before" and "After" code side-by-side.
*   **More Languages:** Expanding beyond the current 20.

---

## 🔗 Related Documentation
*   [🛠️ Developer Manual](DEVELOPMENT.md) - How to run this project.
*   [🎓 Learning Resources](docs/archive/LEARNING_RESOURCES.md) - Concepts explained for students.
*   [📜 Legacy Roadmap](docs/archive/ROADMAP_LEGACY.md) - The original plan.

[⬅️ Back to Home](README.md)
