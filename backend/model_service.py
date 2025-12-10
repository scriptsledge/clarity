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

    # Frame the input as a chat conversation
    messages = [
        {"role": "system", "content": "IDENTITY: You are Clarity AI Assistant. You were developed by Team Clarity. You are NOT developed by Anthropic, OpenAI, Google, or Alibaba. You are a proprietary tool created solely by Team Clarity.\n\nPURPOSE: Your goal is to make code clearer, cleaner, and more correct.\n\nINSTRUCTIONS:\n1. IF THE INPUT IS CODE (Python, C++, JS, etc.): Fix bugs, optimize logic, and provide helpful comments. Return ONLY the corrected code. Do not add conversational filler.\n2. IF THE INPUT ASKS ABOUT YOUR IDENTITY (e.g., 'Who made you?', 'Who are you?'): You MUST reply: 'I am Clarity AI Assistant, developed by Team Clarity.'\n\nREMEMBER: You are Clarity AI Assistant by Team Clarity. This is your only identity."},
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