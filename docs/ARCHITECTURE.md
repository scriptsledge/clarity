# 🏗️ Architecture & Design Patterns

This project employs a **Microservices-lite** architecture orchestrated via Docker Compose for local development, mirroring a modern cloud deployment strategy.

## 🔄 The Routing Logic (Reverse Proxy)

We use **Nginx** as a unified gateway to solve the CORS (Cross-Origin Resource Sharing) and Environment Parity problems.

### The Problem
*   **Local Dev:** Frontend runs on `localhost:80`, Backend on `localhost:7860`. The browser blocks requests due to CORS.
*   **Cloud:** Frontend might be on Vercel, Backend on Hugging Face. Hardcoding URLs breaks local dev.

### The Solution: Gateway Pattern
We treat the application as a single entity exposed on **Port 80**.

```mermaid
graph LR
    User[User / Browser] -->|http://localhost| Nginx[Nginx Gateway (Frontend Container)]
    
    subgraph Docker Network
        Nginx -->|/ (Root)| Static[Static Files (HTML/JS)]
        Nginx -->|/api/*| Backend[Python FastAPI (Backend Container)]
    end
```

1.  **Frontend (`/`)**: Nginx serves the static assets directly.
2.  **Backend (`/api`)**: Nginx transparently proxies traffic to the internal `backend:7860` address.

## ⚡ Environment Parity

**Key Code Decision:** `script.js` uses a **relative path**:
```javascript
fetch('/api/correct', ...) // No hardcoded https://...
```

*   **Locally:** Nginx catches `/api` and routes it to the backend container.
*   **In Cloud:** Your load balancer (or Cloudflare/Netlify/Vercel rewrites) handles the `/api` route.

This ensures **Zero Config Changes** between Local and Production.
