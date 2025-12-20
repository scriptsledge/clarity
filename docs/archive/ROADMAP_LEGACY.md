# 📜 Legacy Roadmap (Original Plan)

> "This document represents the initial vision and step-by-step plan for Clarity before its evolution into the current production system."

**⚠️ Note:** This is an archived file. Links to other documents (like `projects.md`) may be broken. Please refer to the **[New Journey](../../JOURNEY.md)** for current information.

---

### 🎯 Project Goal (MVP)
To build a web-based tool with a simple interface where a user can:
1.  Paste a buggy Python code snippet.
2.  Click a button to submit the code to a backend API.
3.  Receive an AI-corrected version of the code from the API.
4.  View the corrected code in the interface.

---

### 💻 Recommended Technology Stack

| Component | Technology | Recommendation & Justification |
| :--- | :--- | :--- |
| **Backend** | **Python with FastAPI** | FastAPI is modern, fast, and has automatic interactive documentation (Swagger UI), which is excellent for API development and testing. |
| **AI Model** | **Qwen 2.5 0.5B (Original Plan)** | We initially planned to use `Qwen/Qwen2.5-Coder-0.5B-Instruct` via the standard Hugging Face `transformers` library for lightweight CPU inference. |
| **Frontend** | **HTML, CSS, JavaScript** | For an MVP, vanilla web technologies are perfect. They are simple, have no build steps, and are easy to deploy. |

---

## **Project Phases: Step-by-Step Implementation Plan**

### **Phase 1: The Backend Skeleton**

**Goal:** Create a basic, non-AI backend that can receive a request and send a fixed response. This allows the frontend team to start working in parallel.

**Key Tasks:**
1.  **Project Structure:**
    *   Initialize the `git` repository.
    *   Create the folder structure: `/clarity`, `/backend`, `/frontend`.
    *   Add a `.gitignore` file.
2.  **Create the API:**
    *   In `backend/main.py`, set up a FastAPI app.
    *   Create a single endpoint: `POST /api/correct`.
    *   Implement CORS middleware to allow requests from the frontend.
3.  **Mock the AI:**
    *   In `backend/model_service.py`, create a function `correct_code_with_ai`.
    *   **Crucially, do not add the real AI model yet.** Just make the function return a hardcoded string, like: `return "# This is a corrected code snippet."`
4.  **Dependencies:**
    *   Create `backend/requirements.txt` with `fastapi` and `uvicorn`.

**Outcome of Phase 1:** A developer can run the backend, send it code, and get a predictable, fake response.

### **Phase 2: The Frontend User Interface**

**Goal:** Build the user-facing part of the application that can talk to the "fake" backend from Phase 1.

**Key Tasks:**
1.  **HTML Structure:**
    *   In `frontend/index.html`, create the main page with a title, a text area for input, a "Correct Code" button, and a display area for the output.
2.  **JavaScript Logic:**
    *   In `frontend/script.js`, write the code to:
        *   Listen for a click on the button.
        *   Get the text from the input area.
        *   Use `fetch` to `POST` the text to your local backend (`http://127.0.0.1:8000/api/correct`).
        *   Display the response from the backend in the output area.
3.  **Basic Styling:**
    *   In `frontend/style.css`, add some simple CSS to make the page usable and clean. Don't worry about making it perfect yet.

**Outcome of Phase 2:** You have a working web page where a user can type code, click a button, and see the fake response from the backend. The full loop is complete, just without the "smart" part.

### **Phase 3: The AI Brain (Original Implementation)**

**Goal:** Replace the "fake" backend logic with the real AI model using the standard `transformers` pipeline.

**Key Tasks:**
1.  **Update Dependencies:**
    *   Add `transformers`, `torch`, and `accelerate` to `backend/requirements.txt`.
2.  **Integrate the Model:**
    *   In `backend/model_service.py`, modify the `correct_code_with_ai` function.
    *   Load the `Qwen/Qwen2.5-Coder-0.5B-Instruct` model pipeline.
    *   Pass the user's code to the model and get the real, AI-generated output.
    *   Handle potential errors during model inference.
3.  **Test the Endpoint:**
    *   Thoroughly test the `/api/correct` endpoint directly (using FastAPI's automatic docs) to ensure it's working as expected.

**Outcome of Phase 3:** The backend is now "smart." When you send it buggy code, it sends back a real, AI-generated correction.

**Running the Backend (Phase 3):**
```bash
cd backend
uvicorn main:app --reload
```

**File: `backend/requirements.txt` (Original)**
```
fastapi
uvicorn
transformers
torch
accelerate
```

**File: `backend/model_service.py` (Original)**
```python
from transformers import pipeline
import torch

# Original Plan: Use 0.5B model with standard pipeline
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-Coder-0.5B-Instruct", device_map="auto")

def correct_code_with_ai(code: str) -> str:
    messages = [
        {"role": "system", "content": "You are a coding assistant. Fix the bugs in the code below. Return ONLY the code."},
        {"role": "user", "content": code}
    ]
    outputs = pipe(messages, max_new_tokens=512)
    return outputs[0]["generated_text"][-1]["content"]
```

### **Phase 4: Integration and Polish**

**Goal:** Connect the final frontend and backend, and improve the user experience.

**Key Tasks:**
1.  **Full-Stack Test:**
    *   Run the frontend and backend together to ensure they work perfectly with the real AI.
2.  **Add a Loading State:**
    *   The AI model takes a few seconds to run. In `script.js`, add a loading message (e.g., "Correcting...") that displays after the user clicks the button and before the response arrives.
3.  **Error Handling:**
    *   What if the backend is down or returns an error? Update the `fetch` call in `script.js` to handle errors gracefully and show a user-friendly message.
4.  **Improve CSS:**
    *   Now that everything works, spend time making the UI look professional and polished.

**Outcome of Phase 4:** A complete, functional, and good-looking application running on your local machine.

---

### **Deployment and Hosting (Free Options)**

Yes, you can absolutely host this entire project for free. Here’s a recommended strategy:

### **1. Hosting the Frontend**

Your frontend is a simple "static site" (HTML, CSS, JS). The best free options are:

*   **GitHub Pages:** If your code is already on GitHub, this is the easiest option.
*   **Vercel & Netlify:** Both have excellent free tiers, are incredibly fast, and make deployment from a Git repository trivial.

**Recommendation:** Use **Vercel**. It's extremely user-friendly.

### **2. Hosting the Backend (FastAPI App + AI Model)**

This is the most critical part because of the AI model's size. You don't "upload" the model with your code; instead, you host your app on a platform that can download and run the model from the Hugging Face Hub.

**Primary Recommendation: Hugging Face Spaces**

*   **Why it's perfect:** Hugging Face Spaces is a free service *designed* for hosting ML applications. It provides you with a containerized environment where your FastAPI app can run.
*   **How it works:** When your app starts in a Space, it will download the `Qwen/Qwen2.5-Coder-7B-Instruct` model from the Hub into the container's storage. The model will stay there, so it doesn't need to be re-downloaded on every request.
*   **Size Limits:** The free "Community" tier provides enough CPU, RAM, and storage for an MVP with a small model like ours. There are no hard project limits that would affect this MVP.