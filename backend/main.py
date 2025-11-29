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

@app.post("/api/correct")
def correct_code_endpoint(snippet: CodeSnippet):
    corrected_code = correct_code_with_ai(snippet.code)
    return {"corrected_code": corrected_code}

