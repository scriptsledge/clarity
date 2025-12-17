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
Open **[http://localhost](http://localhost)** in your browser.
*   The Frontend is served instantly.
*   API calls are routed to the backend container seamlessly.

---

## 🐍 Option B: The Manual Way (Legacy)
If you cannot use Docker, you must run services independently and handle networking manually.

### 1. Start Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 7860
```

### 2. Start Frontend
You cannot simply open `index.html`. You must serve it to avoid CORS issues, **BUT** you also need to modify the code.

**⚠️ Code Change Required:**
Since you don't have the Nginx proxy, you must edit `frontend/script.js`:
```javascript
// Change this:
fetch('/api/correct', ...)

// To this (hardcoded local URL):
fetch('http://localhost:7860/api/correct', ...)
```

Then serve the file:
```bash
cd frontend
python3 -m http.server 8000
```
Access at `http://localhost:8000`.
