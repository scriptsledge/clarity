import os
import torch
from transformers import pipeline

# --- Configuration ---
# Switching to 3B model for faster download and inference as requested
MODEL_ID = "Qwen/Qwen2.5-Coder-3B-Instruct"

print(f"Initializing Clarity AI Engine (Transformers Pipeline)...")
print(f"Target Model: {MODEL_ID}")

# Optimize for speed: use float16 if GPU is available
dtype = torch.float16 if torch.cuda.is_available() else "auto"

pipe = None

try:
    print("Loading model pipeline...")
    # Using the exact pattern you provided
    pipe = pipeline(
        "text-generation",
        model=MODEL_ID,
        device_map="auto",
        torch_dtype=dtype
    )
    print("Success: Clarity AI Model loaded.")

except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model. {e}")
    pipe = None

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
    Takes a buggy code snippet and returns a corrected version using the Qwen model pipeline.
    """
    detected_lang = detect_language(code)
    
    if not pipe:
        return {
            "code": "# Model failed to load. Check server logs.",
            "language": detected_lang
        }

    system_prompt = (
        "You are 'Clarity', an intelligent code correction and refactoring engine. "
        f"Your goal is to take buggy or suboptimal {detected_lang['name']} code and provide a clean, "
        "production-ready version. \n\n"
        "Tasks:\n"
        "1. Fix all syntax and logical bugs.\n"
        "2. Improve code structure and readability (refactoring).\n"
        "3. Enforce industry-standard naming conventions.\n"
        "4. Maintain the original intent and logic of the code.\n\n"
        "Constraint: Return ONLY the corrected code. No explanations, no markdown backticks, no comments unless necessary for clarity."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": code}
    ]
    
    try:
        # Standard pipeline call
        outputs = pipe(
            messages,
            max_new_tokens=1024,
            return_full_text=False
        )
        
        # Extract content
        generated_msg = outputs[0]["generated_text"]
        
        if isinstance(generated_msg, list):
             response_content = generated_msg[-1]["content"]
        else:
             response_content = str(generated_msg)

        # Clean up
        cleaned_response = response_content.strip()
        if "```" in cleaned_response:
             lines = cleaned_response.split("\n")
             if lines[0].startswith("```"): lines = lines[1:]
             if lines and lines[-1].strip().startswith("```"): lines = lines[:-1]
             cleaned_response = "\n".join(lines).strip()

        return {
            "code": cleaned_response,
            "language": detected_lang
        }

    except Exception as e:
        print(f"Inference Error: {e}")
        return {
            "code": f"# An error occurred during processing: {str(e)}",
            "language": detected_lang
        }
