# 💻 Local Development Guide

## 🐳 Option A: The Docker Way (Recommended)
This approach guarantees an identical environment to production and solves all networking issues automatically.

### Prerequisites
*   Docker & Docker Compose

### Quick Start
Run the entire stack with one command:
```bash
docker compose up --build
```

### Access
*   **Full App:** Open **[http://localhost](http://localhost)**.
*   **Local Preview:** Open `frontend/index.html` in your editor (Live Server).
    *   *Note:* Ensure the toggle is set to **Docker** (Port 7860).

---

## 🐍 Option B: The Manual Way (Legacy)
If you cannot use Docker, you must run services independently.

### 1. Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Run on port 8000
uvicorn main:app --reload --port 8000
```

### 2. Start Frontend
Simply open `frontend/index.html` in your browser or use a simple server:
```bash
cd frontend
python3 -m http.server 3000
```

### 3. Connect
In the UI Footer, click the toggle button until it says **Local**. This connects to `http://127.0.0.1:8000`.

---

## 🎛️ Modes & Troubleshooting

The application has a built-in switch to connect to different backends.

| Mode | Indicator | Description | Port |
| :--- | :--- | :--- | :--- |
| **Cloud** | ☁️ | **Default.** Connects to the public Hugging Face demo. No local backend needed. | Remote |
| **Docker** | 🐳 | Connects to your local Docker container. Use this if you ran `docker-compose up`. | `7860` |
| **Local** | 💻 | Connects to a manually started Python server. Use this if you ran `uvicorn ...`. | `8000` |

### Status Indicators
*   **🟢 Green (System Online):** Successfully connected to the selected backend.
*   **🔴 Red (Offline):** Cannot reach the backend.
    *   *Check:* Is your Docker container running?
    *   *Check:* Did you select the correct mode? (e.g., Don't use "Local" if you are running Docker).

## See Also
*   [Architecture Guide](ARCHITECTURE.md) for system design.
*   [AI Manifesto](AI_MANIFESTO.md) for understanding the model's behavior.
