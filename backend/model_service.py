import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

# --- Configuration ---
# Using the 4-bit quantized version of Qwen 2.5 Coder 7B
# This fits comfortably in 16GB RAM (~5-6GB usage) and is much faster on CPU
REPO_ID = "Qwen/Qwen2.5-Coder-7B-Instruct-GGUF"
FILENAME = "qwen2.5-coder-7b-instruct-q4_k_m.gguf"

print(f"Initializing Clarity AI Engine (llama.cpp)...")
print(f"Target Model: {REPO_ID} [{FILENAME}]")

llm = None

try:
    print("Downloading/Loading model...")
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        # This caches the model in ~/.cache/huggingface/hub
    )
    
    # Initialize Llama
    # Use environment variable to toggle context size (8192 for HF Spaces, 4096 for local)
    ctx_size = int(os.getenv("MODEL_CTX_SIZE", "4096"))
    llm = Llama(
        model_path=model_path,
        n_ctx=ctx_size, 
        n_batch=512,
        n_threads=os.cpu_count(),
        verbose=False 
    )
    print("Success: Clarity AI Model loaded.")

except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model. {e}")
    llm = None

def detect_language(code: str) -> dict:
    """
    Heuristic detection for LeetCode-supported languages.
    """
    code = code.strip()
    
    # C / C++
    if "#include" in code or "using namespace std" in code or "std::" in code:
        return {"name": "C++", "ext": "cpp"}
    if "printf" in code and "#include <stdio.h>" in code:
        return {"name": "C", "ext": "c"}
        
    # Java / C#
    if "public class" in code:
        if "System.out.println" in code or "public static void main" in code:
            return {"name": "Java", "ext": "java"}
        if "Console.WriteLine" in code or "namespace " in code or "using System" in code:
            return {"name": "C#", "ext": "cs"}
            
    # Python
    if "def " in code and ":" in code:
        return {"name": "Python", "ext": "py"}
        
    # JS / TS
    if "console.log" in code or "const " in code or "let " in code or "function" in code:
        if ": number" in code or ": string" in code or "interface " in code:
            return {"name": "TypeScript", "ext": "ts"}
        return {"name": "JavaScript", "ext": "js"}

    # Go
    if "package main" in code or "func main" in code or "fmt.Print" in code:
        return {"name": "Go", "ext": "go"}

    # Rust
    if "fn " in code and ("let mut" in code or "println!" in code or "Vec<" in code):
        return {"name": "Rust", "ext": "rs"}

    # PHP
    if "<?php" in code or "$" in code and "echo" in code:
        return {"name": "PHP", "ext": "php"}

    # Ruby
    if "def " in code and "end" in code and "puts" in code:
        return {"name": "Ruby", "ext": "rb"}
        
    # Swift
    if "func " in code and ("var " in code or "let " in code) and "print(" in code:
        if "->" in code: # Swift return type arrow
            return {"name": "Swift", "ext": "swift"}
            
    # Kotlin
    if "fun " in code and ("val " in code or "var " in code) and "println(" in code:
        return {"name": "Kotlin", "ext": "kt"}
        
    # Dart
    if "void main()" in code and "print(" in code and ";" in code:
        return {"name": "Dart", "ext": "dart"}

    # Scala
    if "object " in code or "def main" in code or "val " in code and "println" in code:
        return {"name": "Scala", "ext": "scala"}

    # Elixir
    if "defmodule" in code or "defp" in code or "IO.puts" in code or ":ok" in code:
        return {"name": "Elixir", "ext": "ex"}

    # Erlang
    if "-module" in code or "-export" in code or "io:format" in code:
        return {"name": "Erlang", "ext": "erl"}

    # Racket / Lisp
    if "(define" in code or "(lambda" in code or "#lang racket" in code:
        return {"name": "Racket", "ext": "rkt"}

    # Fallback
    return {"name": "Text", "ext": "txt"}

def correct_code_with_ai(code: str) -> dict:
    """
    Takes a buggy code snippet and returns a corrected version using the Qwen model.
    """
    detected_lang = detect_language(code)
    
    if not llm:
        return {
            "code": "# Model failed to load. Check server logs.",
            "language": detected_lang
        }

    # Stricter System Prompt with Educational Persona
    system_prompt = (
        "You are Clarity, an intelligent coding assistant designed for students and junior developers. "
        "You were created by a team of college students (see projects.md) for a minor project to help peers write better code.\n\n"
        "Your Mission:\n"
        "1.  **Review & Fix:** Correct syntax and logical errors.\n"
        "2.  **Educate:** Improve variable naming (use industry standards like Google Style Guide), readability, and structure.\n"
        "3.  **Optimize:** Remove redundancy and improve logic.\n"
        "4.  **Be Concise:** Provide objective, short, and high-value feedback. Avoid long lectures.\n\n"
        "Guidelines:\n"
        "-   **Style:** Follow the Google Style Guide for the respective language.\n"
        "-   **Comments:** Add comments ONLY for complex logic or educational 'aha!' moments.\n"
        "-   **Tone:** Concise, Objective, and Mentor-like.\n"
        "-   **Identity:** You are 'Clarity'. If asked about your version, refer users to the GitHub repo. If asked non-code questions, answer only if factual and harmless; otherwise, politely decline.\n\n"
        "Constraint: Return ONLY the corrected code with necessary educational comments inline. Do not output a separate explanation block unless absolutely necessary for a critical concept."
    )

    # One-shot example to force the pattern (Input -> Code Only)
    example_input = "def sum(a,b): return a+b" if detected_lang["name"] == "Python" else "int sum(int a, int b) { return a+b; }"
    example_output = (
        "def sum(operand_a, operand_b):\n"
        "    # Descriptive names improve readability\n"
        "    return operand_a + operand_b"
    ) if detected_lang["name"] == "Python" else (
        "int sum(int operand_a, int operand_b) {\n"
        "    // Descriptive names improve readability\n"
        "    return operand_a + operand_b;\n"
        "}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": example_input},
        {"role": "assistant", "content": example_output},
        {"role": "user", "content": code}
    ]
    
    try:
        # llama-cpp-python chat completion
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=2048,
            temperature=0.1, # Lower temperature for stricter adherence
        )
        
        # Extract content
        response_content = response["choices"][0]["message"]["content"]

        # Clean up (double check for markdown or chatty intros)
        cleaned_response = response_content.strip()
        
        # Aggressive stripping of "Here is the code..." or markdown
        if "```" in cleaned_response:
             lines = cleaned_response.split("\n")
             # Remove starting markdown
             if lines[0].strip().startswith("```"): lines = lines[1:]
             # Remove ending markdown
             if lines and lines[-1].strip().startswith("```"): lines = lines[:-1]
             # Remove common chatty prefixes if they slipped through
             if lines and (lines[0].lower().startswith("here is") or lines[0].lower().startswith("sure")):
                 lines = lines[1:]
             cleaned_response = "\n".join(lines).strip()

        # Run detection on the CLEAN, CORRECTED code for maximum accuracy
        detected_lang = detect_language(cleaned_response)

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