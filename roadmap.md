# Clarity Project Roadmap: A Detailed Guide

This document outlines the detailed, step-by-step plan for building the Minimum Viable Product (MVP) of Clarity, structured into distinct phases. The goal is to create a functional web application that can correct simple bugs in Python code using an AI model.

---

### 📚 Table of Contents
- [Navigation](#-navigation)
- [Project Goal (MVP)](#-project-goal-mvp)
- [Recommended Technology Stack](#-recommended-technology-stack)
- [Phase 1: The Backend Skeleton](#phase-1-the-backend-skeleton)
- [Phase 2: The Frontend User Interface](#phase-2-the-frontend-user-interface)
- [Phase 3: The AI Brain](#phase-3-the-ai-brain)
- [Phase 4: Integration and Polish](#phase-4-integration-and-polish)
- [Phase 5: Deployment](#phase-5-deployment)
- [Deployment and Hosting (Free Options)](#deployment-and-hosting-free-options)

---

### 🧭 Navigation
- **[Home](https://github.com/scriptsledge/clarity/blob/main/README.md)**
- **[Other Projects](https://github.com/scriptsledge/clarity/blob/main/projects.md)**

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
| **AI Model** | **Hugging Face Transformers** | We use `Qwen/Qwen2.5-0.5B-Instruct`, a small and fast model that works well for code instruction tasks. |
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

**Running the Backend (Phase 1):**
```bash
# Navigate to the backend directory first to avoid import errors
cd backend

# Start the server
uvicorn main:app --reload
```
*Note: If you see `ModuleNotFoundError`, ensure you are inside the `backend` folder before running `uvicorn`.*

**File: `backend/requirements.txt`**
```
fastapi
uvicorn
```

**File: `backend/main.py`**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from model_service import correct_code_with_ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from our frontend (running on a different port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For simplicity, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSnippet(BaseModel):
    code: str

@app.post("/api/correct")
def correct_code_endpoint(snippet: CodeSnippet):
    corrected_code = correct_code_with_ai(snippet.code)
    return {"corrected_code": corrected_code}
```

**File: `backend/model_service.py`**
```python
def correct_code_with_ai(code: str) -> str:
    # This is a mock function for Phase 1
    return "# This is a corrected code snippet (mock response from Phase 1)."
```

---

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

**File: `frontend/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Clarity - AI Code Corrector</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Clarity ✨</h1>
        <p>Paste your buggy Python code below and let AI fix it.</p>
        
        <textarea id="codeInput" placeholder="def find_evens(numbers): ..."></textarea>
        <button id="correctBtn">Correct My Code</button>
        
        <h2>Corrected Code:</h2>
        <pre id="codeOutput"><code># Your corrected code will appear here...</code></pre>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

**File: `frontend/script.js`**
```javascript
document.getElementById('correctBtn').addEventListener('click', () => {
    const codeInput = document.getElementById('codeInput').value;
    const codeOutput = document.getElementById('codeOutput');
    
    codeOutput.textContent = 'Correcting...';

    fetch('http://127.0.0.1:8000/api/correct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: codeInput }),
    })
    .then(response => response.json())
    .then(data => {
        codeOutput.textContent = data.corrected_code;
    })
    .catch(error => {
        console.error('Error:', error);
        codeOutput.textContent = '# An error occurred while connecting to the API.';
    });
});
```

---

### **Phase 3: The AI Brain**

**Goal:** Replace the "fake" backend logic with the real AI model. This is the core technical challenge.

**Key Tasks:**
1.  **Update Dependencies:**
    *   Add `transformers` and `torch` to `backend/requirements.txt`.
2.  **Integrate the Model:**
    *   In `backend/model_service.py`, modify the `correct_code_with_ai` function.
    *   Load the `Qwen/Qwen2.5-0.5B-Instruct` model.
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
*Important: On the very first run, the application will download the AI model (approx. 1GB). This may take a few minutes. Wait until you see `Application startup complete` before testing.*

**File: `backend/requirements.txt` (Updated)**
```
fastapi
uvicorn
transformers
torch
```

**File: `backend/model_service.py` (Updated)**
```python
from transformers import pipeline

# Initialize the model pipeline using a standard Transformers model.
# We use 'Qwen/Qwen2.5-0.5B-Instruct' which is small, fast, and works natively with the installed libraries.
print("Loading AI model (Qwen/Qwen2.5-0.5B-Instruct)...")
try:
    code_fixer = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", trust_remote_code=True)
except Exception as e:
    print(f"Failed to load model: {e}")
    code_fixer = None

def correct_code_with_ai(code: str) -> str:
    """
    Takes a buggy code snippet and returns a corrected version using the Qwen AI model.
    """
    if not code_fixer:
        return "# Model failed to load. Check server logs."

    # Frame the input as a chat conversation
    messages = [
        {"role": "system", "content": "You are a helpful Python coding assistant. Your task is to fix bugs in the provided code. Return ONLY the corrected code, without explanation."},
        {"role": "user", "content": f"{code}"},
    ]
    
    try:
        # Generate the response
        # max_new_tokens controls how much new text is generated.
        outputs = code_fixer(messages, max_new_tokens=512)
        
        # The pipeline for chat-like input typically returns a list of dictionaries.
        # We need to parse the output to get just the assistant's response.
        # The structure is usually: [{'generated_text': [...conversation including response...]}]
        # or sometimes just the generated text depending on pipeline version.
        
        result = outputs[0]['generated_text']
        
        # If the result is the full conversation list (common in newer transformers for chat)
        if isinstance(result, list):
            # The last message should be the assistant's response
            return result[-1]['content']
        else:
            # Fallback if it returns a string
            return result

    except Exception as e:
        print(f"An error occurred during AI correction: {e}")
        return f"# Unable to correct the code. Error: {str(e)}"
```

---

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

### **Phase 5: Deployment**

**Goal:** Put your project on the internet so anyone can use it.

**Key Tasks:**
1.  **Deploy Backend:**
    *   Create a new **Space** on [Hugging Face](https://huggingface.co/spaces) and link it to your GitHub repository (specifically the `backend` directory).
2.  **Deploy Frontend:**
    *   Use a service like [Vercel](https://vercel.com/) or [GitHub Pages](https://pages.github.com/) to host your static `frontend` folder.
3.  **Connect Them:**
    *   Once your backend is live on Hugging Face Spaces, you will get a public URL (e.g., `https://your-username-your-space-name.hf.space`).
    *   Update the `fetch` URL in your `frontend/script.js` to this new public URL.
    *   Redeploy the frontend on Vercel/GitHub Pages.

**Outcome of Phase 5:** Your project is live on the web! You have a public URL you can share with anyone.

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
*   **How it works:** When your app starts in a Space, it will download the `Qwen/Qwen2.5-0.5B-Instruct` model from the Hub into the container's storage. The model will stay there, so it doesn't need to be re-downloaded on every request.
*   **Size Limits:** The free "Community" tier provides enough CPU, RAM, and storage for an MVP with a small model like ours. There are no hard project limits that would affect this MVP.

**Alternative (Not Recommended for this MVP): Heroku, Render, etc.**

*   **The Challenge:** Most general-purpose free hosting platforms (like Heroku's free tier) have a "slug size" limit (typically 500MB). Your application code *plus* all its dependencies must fit within this limit.
*   **The Problem:** The AI model itself (`torch`, `transformers`, etc.) will easily exceed this limit, making deployment impossible on these free tiers without complex workarounds.

### **Summary of Free Hosting Strategy**

1.  **Push your `frontend` and `backend` folders to a GitHub repository.**
2.  **Deploy the Backend:**
    *   Create a new **Space** on [Hugging Face](https://huggingface.co/spaces).
    *   Point it to your GitHub repository and specify the `backend` directory.
    *   Ensure your `requirements.txt` is correct. Hugging Face will automatically install the dependencies and run your FastAPI app.
3.  **Deploy the Frontend:**
    *   Sign up for [Vercel](https://vercel.com/) with your GitHub account.
    *   Create a new project and point it to the same GitHub repository, but specify the `frontend` directory.
4.  **Connect Them:**
    *   Once your backend is live on Hugging Face Spaces, you will get a public URL (e.g., `https://your-username-your-space-name.hf.space`).
    *   Update the `fetch` URL in your `frontend/script.js` to this new public URL.
    *   Redeploy the frontend on Vercel.

Your project will now be live on the internet for free!
