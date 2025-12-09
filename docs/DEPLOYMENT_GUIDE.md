# Clarity Deployment Guide & Post-Mortem

This document details the step-by-step process used to deploy the Clarity application (Phase 5 of the Roadmap), including specific technical decisions, workarounds for free-tier limitations, and explanations of cloud platform concepts.

## 1. Backend Deployment (Hugging Face Spaces)

**Goal:** Host the FastAPI backend and the Qwen-0.5B AI model on a public server.

### 1.1 Docker Configuration
We utilized **Docker** to containerize the application, ensuring it runs consistently regardless of the host environment.

**`backend/Dockerfile` Breakdown:**
*   `FROM python:3.10-slim`: Uses a lightweight Linux + Python 3.10 base image.
*   `WORKDIR /app`: Sets the internal directory.
*   `COPY requirements.txt .` & `RUN pip install ...`: Installs Python dependencies (FastAPI, Uvicorn, Torch, Transformers).
*   `RUN useradd ...`: Creates a non-root user (Security best practice & Requirement for Hugging Face).
*   `EXPOSE 7860`: Exposes the default Hugging Face port.
*   `CMD ["uvicorn", "main:app", ...]`: Starts the web server.

### 1.2 Deployment Steps (Hugging Face)
We used **Hugging Face Spaces** for its free access to CPU compute.

1.  **Created Space:**
    *   **SDK:** Docker
    *   **Template:** Empty
    *   **Hardware:** CPU Basic (2 vCPU, 16GB RAM) - *Selected because it is free and sufficient for the 0.5B model.*
2.  **File Upload (The "Free Tier" Workaround):**
    *   *Challenge:* The standard `git push` or SSH cloning requires a PRO account for "Dev Mode".
    *   *Solution:* We manually uploaded the `backend/` files via the Hugging Face web interface ("Files and versions" tab).
    *   *Process:* Files (Dockerfile, main.py, model_service.py, requirements.txt) were placed in the **root** of the Space.
3.  **Build & Launch:**
    *   Hugging Face automatically detected the `Dockerfile` and built the image.
    *   **Success Indicator:** Status changed to "Running", and logs showed `Uvicorn running on http://0.0.0.0:7860`.

### 1.3 Identifying the API URL
*   **Web URL:** `https://huggingface.co/spaces/scriptsledge/clarity-backend` (The UI wrapper).
*   **Direct API URL:** `https://scriptsledge-clarity-backend.hf.space` (The actual endpoint for code).
*   **Endpoint:** `https://scriptsledge-clarity-backend.hf.space/api/correct`

---

## 2. Frontend Deployment (Vercel)

**Goal:** Host the static HTML/CSS/JS frontend.

### 2.1 Configuration
1.  **API Connection:**
    *   Modified `frontend/script.js` to replace `localhost:8000` with the live Hugging Face API URL.
2.  **Project Settings:**
    *   **Root Directory:** Set to `frontend/` so Vercel serves the UI, not the backend Python files.

### 2.2 Vercel Concepts & Hierarchy
During deployment, we encountered various URLs. Here is how Vercel organizes them:

*   **Account (Team):** `scriptsledge` (The top-level owner).
*   **Project:** `clarity` (The specific application repository).
*   **Deployment:** An immutable instance of your app. Every time you push code, a *new* deployment is created.

### 2.3 Understanding Vercel URLs
Vercel generates three types of URLs for every project:

1.  **Production Domain:** `https://logiclensclarity.vercel.app`
    *   *Note:* We chose the name `logiclensclarity` to ensure a clear, unique URL.
    *   *Customization:* You can rename the project in Vercel Settings to try for a different URL (e.g., `scriptsledge-clarity.vercel.app`).
2.  **Deployment URL:** `https://logiclensclarity-git-main-scriptsledge.vercel.app`
    *   Linked to a specific Git branch (e.g., `main`). Useful for testing changes before they go live.
3.  **Immutable Deployment URL:** `https://logiclensclarity-3mycgn3cu-scriptsledge.vercel.app`
    *   Contains a unique hash (`3mycgn3cu`). This points to *that specific build* forever. Even if you update the site, this URL will show the old version.

---

## 3. Architecture Summary

Now that deployment is complete, the application flow is:

1.  **User** visits `https://logiclensclarity.vercel.app` (Frontend on Vercel).
2.  User enters code and clicks "Correct".
3.  **Frontend** sends a POST request to `https://scriptsledge-clarity-backend.hf.space/api/correct`.
4.  **Backend (Hugging Face)** receives the code, runs it through the Qwen model, and returns the fix.
5.  **Frontend** displays the result.
