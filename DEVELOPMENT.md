# Developer Manual 🛠️

This guide covers the architecture, setup, and contribution workflows for Clarity.

## 🏗️ Architecture

Clarity uses a decoupled architecture with a **Hybrid AI Engine**:

*   **Frontend:** Vanilla HTML/JS/CSS (No framework bloat). Hosted on Vercel or locally.
*   **Backend:** FastAPI (Python). Hosted on Hugging Face Spaces or Docker.
*   **AI Models:**
    *   **Local:** Qwen 2.5 Coder 0.5B (via `transformers` + `torch`).
    *   **Cloud:** Google Gemini (via `google-generativeai`) with **Dynamic Model Discovery**.

### Hybrid Inference Flow
1.  **User Selects Model:** "Google" (with Version Selector) or "Local" in the UI.
2.  **Request:** Frontend sends JSON payload to Backend (`/api/correct`).
3.  **Routing:**
    *   If `provider="google"`: Backend calls Google Gemini API using the selected version (e.g., `gemini-flash-latest`).
    *   If `provider="local"`: Backend runs Qwen model locally.
4.  **Security:** Google API Key is read from `os.environ` (Server) or `payload` (BYOK from Client).

## 🚀 Local Setup

### Prerequisites
*   Docker & Docker Compose
*   Python 3.10+
*   (Optional) Google API Key

### Quick Start
```bash
# 1. Clone
git clone https://github.com/your-repo/clarity.git
cd clarity

# 2. Setup Secrets (Optional, for Google Default)
echo "GOOGLE_API_KEY=your_key_here" > .env

# 3. Run
docker compose up --build
```

Access:
*   Frontend: `http://localhost:80`
*   Backend Docs: `http://localhost:7860/docs`

## ☁️ Deployment

### 1. Backend (Hugging Face Spaces)
The backend is designed to run on a **CPU Basic** Space (free).
1.  Create a new Space (SDK: Docker).
2.  Upload the `backend/` folder contents.
3.  **Settings > Variables and secrets:** Add `GOOGLE_API_KEY`.

### 2. Frontend (Vercel/Netlify)
1.  Deploy the `frontend/` folder.
2.  The `script.js` automatically detects production and points to the HF Backend.

## 🧪 Testing
Run the backend unit tests:
```bash
cd backend
python -m pytest
```
