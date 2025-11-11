from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# TODO (Team Task): Import the 'correct_code_with_ai' function from model_service.py
# from model_service import correct_code_with_ai

app = FastAPI()

# This middleware allows the frontend (running on a different address) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for simplicity.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This Pydantic model defines the expected structure of the request body.
class CodeSnippet(BaseModel):
    code: str

@app.post("/api/correct")
def correct_code_endpoint(snippet: CodeSnippet):
    # --- Team Task ---
    # TODO: Call the 'correct_code_with_ai' function, passing it the user's code (snippet.code).
    # TODO: Store the result in a variable called 'corrected_code'.
    # Example: corrected_code = correct_code_with_ai(snippet.code)
    
    # For now, we are returning a placeholder. Replace this with the real result.
    corrected_code = "# The corrected code from the AI will appear here."
    
    return {"corrected_code": corrected_code}

# To run this server:
# 1. Navigate to the 'backend' directory in your terminal.
# 2. Run the command: uvicorn main:app --reload
# 3. Open your browser to http://127.0.0.1:8000/docs to see the API documentation.
