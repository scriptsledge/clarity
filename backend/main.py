from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from model_service import correct_code_with_ai, correct_code_with_gemini, get_gemini_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for simplicity.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSnippet(BaseModel):
    code: str
    model_provider: str = "local" # "local" or "google"
    api_key: Optional[str] = None
    google_model_name: Optional[str] = None

class ModelRequest(BaseModel):
    api_key: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/models")
def list_models_endpoint(req: ModelRequest):
    """
    Fetches available Google models using the provided (or env) API key.
    """
    models = get_gemini_models(req.api_key)
    return {"models": models}

@app.post("/api/correct")
def correct_code_endpoint(snippet: CodeSnippet):
    if snippet.model_provider == "google":
        result = correct_code_with_gemini(snippet.code, snippet.api_key, snippet.google_model_name)
    else:
        # Default to local
        result = correct_code_with_ai(snippet.code)

    # result is now a dict: {"code": "...", "language": {"name": "...", "ext": "..."}}
    return {
        "corrected_code": result["code"],
        "language": result["language"]
    }