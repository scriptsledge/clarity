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

    # Few-Shot Priming: We inject a fake history where the model correctly identifies itself.
    # This guides the small model (0.5B) to follow the pattern much better than just instructions.
    messages = [
        {"role": "system", "content": "You are Clarity AI Assistant, a proprietary tool created solely by Team Clarity. You are NOT related to Anthropic, Alibaba, or OpenAI. Your goal is to make code clearer, cleaner, and more correct."},
        {"role": "user", "content": "Who made you?"},
        {"role": "assistant", "content": "I am Clarity AI Assistant, developed by Team Clarity."},
        {"role": "user", "content": f"{code}"},
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