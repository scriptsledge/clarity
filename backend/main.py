from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from model_service import correct_code_with_ai
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

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/correct")
def correct_code_endpoint(snippet: CodeSnippet):
    result = correct_code_with_ai(snippet.code)
    # result is now a dict: {"code": "...", "language": {"name": "...", "ext": "..."}}
    return {
        "corrected_code": result["code"],
        "language": result["language"]
    }

