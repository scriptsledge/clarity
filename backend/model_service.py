from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Initialize the model pipeline.
# We use 'Qwen/Qwen2.5-0.5B-Instruct' which is small, fast, and works natively.
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
print(f"Loading AI model ({model_id})...")

code_fixer = None
try:
    # 1. Try loading from local cache first (offline mode)
    print("Attempting to load from local cache...")
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, local_files_only=True)
    code_fixer = pipeline("text-generation", model=model, tokenizer=tokenizer)
    print("Success: Loaded model from local cache.")
except Exception as local_err:
    print(f"Local cache not found or incomplete: {local_err}")
    print("Attempting to download model from Hugging Face (requires internet)...")
    try:
        # 2. Fallback to downloading (online mode)
        code_fixer = pipeline("text-generation", model=model_id, trust_remote_code=True)
        print("Success: Model downloaded and loaded.")
    except Exception as remote_err:
        print(f"CRITICAL: Failed to load model. Error: {remote_err}")
        print("To run locally, ensure you have internet access for the first run to download the model.")
        code_fixer = None

def detect_language(code: str) -> dict:
    """
    Simple heuristic to detect programming language.
    Returns a dict with 'name' and 'extension'.
    """
    code = code.strip()
    
    # C/C++ Heuristics
    if "#include" in code or "std::" in code or "int main()" in code:
        return {"name": "C++", "ext": "cpp"}
    
    # Java Heuristics
    if "public class" in code or "System.out.println" in code:
        return {"name": "Java", "ext": "java"}
    
    # JavaScript Heuristics
    if "const " in code or "let " in code or "console.log" in code or "function" in code:
        return {"name": "JavaScript", "ext": "js"}
    
    # Python Heuristics (Default)
    # Checks for def, import, print without parens (py2) or with (py3)
    if "def " in code or "import " in code or "print(" in code:
        return {"name": "Python", "ext": "py"}

    # Default fallback
    return {"name": "Text", "ext": "txt"}

def correct_code_with_ai(code: str) -> dict:
    """
    Takes a buggy code snippet and returns a corrected version using the Qwen model,
    along with detected language information.
    """
    detected_lang = detect_language(code)
    
    if not code_fixer:
        return {
            "code": "# Model failed to load. Check server logs.",
            "language": detected_lang
        }

    # Few-Shot Priming: We inject a history to teach the small model (0.5B) its role.
    # It learns to be:
    # 1. Concise (Code only).
    # 2. Multi-language (Supports C++, Java, JS, Python).
    # 3. A "Style Guide" (Improves naming).
    # 4. Aware of its creators.
    messages = [
        {
            "role": "system", 
            "content": f"You are Clarity, a concise coding assistant created by Team Clarity. You are an expert in {detected_lang['name']}. Provide only the corrected code."
        },
        # Example 1: Identity & Credit
        {
            "role": "user", 
            "content": "Who created you?"
        },
        {
            "role": "assistant", 
            "content": "I am Clarity, a minor project created by Team Clarity: Nipun Lakhera, Sahil Raikwar, Mo Zaid Sheikh, and Shivansh Nigam. Our Guide is Vipin Verma and our Co-guide is Swati Patel."
        },
        # Example 4: Simple Syntax Fix (C++) - Demonstrates multi-lang support
        {
            "role": "user", 
            "content": "int main() { std::cout << \"Hello World\" return 0; }"
        },
        {
            "role": "assistant", 
            "content": "int main() { std::cout << \"Hello World\"; return 0; }"
        },
        # The actual user input
        {
            "role": "user", 
            "content": f"{code}"
        },
    ]
    
    try:
        # Generate the response
        outputs = code_fixer(messages, max_new_tokens=512)
        
        result = outputs[0]['generated_text']
        
        if isinstance(result, list):
            raw_response = result[-1]['content']
        else:
            raw_response = result

        # --- IDENTITY GUARDRAIL (Post-Processing) ---
        # Small models often hallucinate their training origin (e.g., "I am Qwen...").
        # We strictly sanitize this to ensure the user always sees the correct identity.
        forbidden_terms = ["Anthropic", "OpenAI", "Google", "Alibaba", "Qwen", "Claude", "Meta"]
        cleaned_response = raw_response
        
        # Simple text replacement if the model slips up
        for term in forbidden_terms:
            if term in cleaned_response:
                cleaned_response = cleaned_response.replace(term, "Team Clarity")
        
        # Specific fix for "I am [Wrong Name]" patterns
        if "I am" in cleaned_response and "Clarity" not in cleaned_response:
             # If it says "I am chatgpt", just force it.
             import re
             cleaned_response = re.sub(r"I am .+?(\.|$)", "I am Clarity AI Assistant, developed by Team Clarity.", cleaned_response)

        return {
            "code": cleaned_response,
            "language": detected_lang
        }

    except Exception as e:
        print(f"An error occurred during AI correction: {e}")
        return {
            "code": f"# Unable to correct the code. Error: {str(e)}",
            "language": detected_lang
        }