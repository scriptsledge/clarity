# 🏗️ Architecture & Design Patterns

This project employs a **Microservices-lite** architecture orchestrated via Docker Compose, designed for flexibility across Local, Docker, and Cloud environments.

## 🔄 The Routing Logic (Smart Backend Discovery)

The frontend uses a **Smart Discovery** mechanism to automatically determine the correct API endpoint based on the environment.

### 1. Production / Docker Container (`http://localhost`)
When running inside the Nginx container, the app is served on standard HTTP ports (80/443).
*   **Logic:** `window.location.port` is empty or '80'.
*   **Result:** Uses relative path `''`.
*   **Flow:** Requests go to `/api/...`, which Nginx intercepts and proxies to `http://backend:7860`.

### 2. Local Preview (`http://127.0.0.1:5500`)
When developing locally (e.g., VS Code Live Server), the app runs on a non-standard port.
*   **Logic:** `window.location.port` is '5500' (or similar).
*   **Result:** Uses explicit URL `http://127.0.0.1:7860`.
*   **Flow:** Requests bypass Nginx and hit the exposed Docker port directly.

## 🌍 System Modes

The application supports three distinct backend modes, togglable via the UI:

| Mode | Target URL | Use Case |
| :--- | :--- | :--- |
| **Cloud** (Default) | `https://...hf.space` | No setup required. Uses the public demo backend. |
| **Docker** | `http://127.0.0.1:7860` | Running via `docker-compose up`. |
| **Local** | `http://127.0.0.1:8000` | Running via `python backend/main.py` (Manual dev). |

## 🧠 Intelligence Features

### 1. Heuristic Language Detection
The backend analyzes code snippets to automatically detect the programming language before processing.
*   **C/C++**: Checks for `#include`, `std::`, `int main()`.
*   **Java**: Checks for `public class`, `System.out`.
*   **JavaScript**: Checks for `const`, `let`, `console.log`.
*   **Python**: Checks for `def`, `import`, `print`.

### 2. Identity Guardrails
A post-processing layer ensures the model maintains the "Clarity" persona. It sanitizes outputs to remove references to the underlying base model (e.g., Qwen, Alibaba) and enforces the team's credit (Team Clarity).
