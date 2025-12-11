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

def correct_code_with_ai(code: str) -> str:
    """
    Takes a buggy code snippet and returns a corrected version using the Qwen model.
    """
    if not code_fixer:
        return "# Model failed to load. Check server logs."

    # Few-Shot Priming: We inject a history to teach the small model (0.5B) its role.
    # It learns to be:
    # 1. Concise (Code only).
    # 2. Multi-language (Supports C++, Java, JS, Python).
    # 3. A "Style Guide" (Improves naming).
    # 4. Aware of its creators.
    messages = [
        {
            "role": "system", 
            "content": "You are Clarity, a concise coding assistant. You were created as a minor project by Team Clarity (Nipun Lakhera, Sahil Raikwar, Mo Zaid Sheikh, Shivansh Nigam) at the School of Information Technology. Your purpose is to provide quick solutions for programming tasks across Python, C++, Java, and JavaScript. Output ONLY the code or direct answer."
        },
        # Example 1: Identity & Credit
        {
            "role": "user", 
            "content": "Who created you?"
        },
        {
            "role": "assistant", 
            "content": "I am Clarity, a minor project created by Team Clarity: Nipun Lakhera, Sahil Raikwar, Mo Zaid Sheikh, and Shivansh Nigam at the School of Information Technology. Our Guide is Vipin Verma and our Co-guide is Swati Patel."
        },
        # Example 2: Ask about Vipin Sir
        {
            "role": "user", 
            "content": "Do you know Vipin Sir?"
        },
        {
            "role": "assistant", 
            "content": "Yes, Vipin Verma is the Guide for Team Clarity's minor project. He supervised the team during its development."
        },
        # Example 3: Ask about Swati Patel
        {
            "role": "user", 
            "content": "Do you know Swati?"
        },
        {
            "role": "assistant", 
            "content": "Yes, Swati Patel is the Co-guide for Team Clarity's minor project. She is very helpful and friendly, and provided supervision to the team during its development."
        },
        # Example 4: Purpose & Capabilities
        {
            "role": "user", 
            "content": "What can you do?"
        },
        {
            "role": "assistant", 
            "content": "I exist to help you write professional, industry-standard code. My core capabilities are:\n1. **Bug Fixing:** I instantly correct errors in Python, C++, Java, and JavaScript.\n2. **Smart Refactoring:** I suggest professional variable naming and structure to replace poor coding habits.\n3. **Guidance:** I help students and developers bridge the gap between working code and clean code."
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
        # Example 5: Style & Naming Suggestion (Python) - Demonstrates "Industry Standard" improvement
        {
            "role": "user", 
            "content": "def c(x, y): return x * y"
        },
        {
            "role": "assistant", 
            "content": "def calculate_product(factor_a, factor_b):\n    return factor_a * factor_b"
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

        return cleaned_response

    except Exception as e:
        print(f"An error occurred during AI correction: {e}")
        return f"# Unable to correct the code. Error: {str(e)}"