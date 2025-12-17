import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# --- Configuration ---
REPO_ID = "unsloth/rnj-1-instruct-GGUF"
FILENAME = "rnj-1-instruct-BF16.gguf"

print(f"Initializing Clarity AI Engine...")
print(f"Target Model: {REPO_ID} ({FILENAME})")

llm = None

try:
    # 1. Download the model file efficiently (caches automatically)
    print("Ensuring model file is downloaded...")
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        local_files_only=False  # Allow downloading if not cached
    )
    print(f"Model path: {model_path}")

    # 2. Load the model into memory
    # n_ctx=4096: Sets the context window (code can be long).
    # n_threads=2: Optimizes for the 2 vCPU cores on HF Spaces.
    print("Loading model into RAM (this may take a moment)...")
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=2,
        verbose=False
    )
    print("Success: Clarity AI Model loaded.")

except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model. {e}")
    llm = None

def detect_language(code: str) -> dict:
    """
    Simple heuristic to detect programming language.
    """
    code = code.strip()
    if "#include" in code or "std::" in code or "int main()" in code:
        return {"name": "C++", "ext": "cpp"}
    if "public class" in code or "System.out.println" in code:
        return {"name": "Java", "ext": "java"}
    if "const " in code or "let " in code or "console.log" in code or "function" in code:
        return {"name": "JavaScript", "ext": "js"}
    if "def " in code or "import " in code or "print(" in code:
        return {"name": "Python", "ext": "py"}
    return {"name": "Text", "ext": "txt"}

def correct_code_with_ai(code: str) -> dict:
    """
    Takes a buggy code snippet and returns a corrected version using the RNJ-1 model.
    """
    detected_lang = detect_language(code)
    
    if not llm:
        return {
            "code": "# Model failed to load. Check server logs.",
            "language": detected_lang
        }

    # Prompt Engineering for RNJ-1 / Llama-3 style models
    # We ask for a strict code-only response.
    system_prompt = (
        f"You are Clarity, an expert coding assistant created by Team Clarity. "
        f"Your task is to fix bugs in {detected_lang['name']} code. "
        f"Return ONLY the corrected code. Do not add explanations or markdown backticks."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": code}
    ]
    
    try:
        # Generate response using the Chat Completion API of llama-cpp
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=1024,  # Allow for decent sized code blocks
            temperature=0.2,  # Low temperature for precision
            stop=["```"]      # Stop if it tries to close a block we didn't ask for
        )
        
        # Extract text
        raw_response = response["choices"][0]["message"]["content"]
        
        # Clean up commonly occurring artifacts
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```"):
            # Remove first line (```language)
            cleaned_response = "\n".join(cleaned_response.split("\n")[1:])
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        return {
            "code": cleaned_response.strip(),
            "language": detected_lang
        }

    except Exception as e:
        print(f"Inference Error: {e}")
        return {
            "code": f"# An error occurred during processing: {str(e)}",
            "language": detected_lang
        }