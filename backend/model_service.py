import os
from transformers import pipeline
import torch

# --- Configuration ---
# Using the standard Qwen 2.5 Coder 0.5B Instruct model (Native PyTorch)
REPO_ID = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

print(f"Initializing Clarity AI Engine (Transformers)...")
print(f"Target Model: {REPO_ID}")

pipe = None

try:
    print("Loading model...")
    # Initialize the pipeline
    # device_map="auto" will use GPU if available, otherwise CPU.
    # torch_dtype="auto" will use appropriate precision (fp16 on GPU, fp32 on CPU typically)
    pipe = pipeline(
        "text-generation",
        model=REPO_ID,
        torch_dtype="auto",
        device_map="auto"
    )
    print("Success: Clarity AI Model loaded.")
    
    # Warm-up inference
    print("Warming up model...")
    warmup_msg = [{"role": "user", "content": "print('hello')"}]
    pipe(warmup_msg, max_new_tokens=10)
    print("Model warmup complete.")

except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model. {e}")
    pipe = None

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
    
    if not pipe:
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
        # Transformers pipeline inference
        outputs = pipe(
            messages,
            max_new_tokens=1024, # Optimized for 1.5B speed
            temperature=0.1, # Lower temperature for stricter adherence
            do_sample=True, # Required for temperature usage
        )
        
        # Extract content
        # Pipeline with list of messages returns a list containing one dict, which contains 'generated_text'.
        # 'generated_text' is the list of messages (history + new response).
        response_content = outputs[0]["generated_text"][-1]["content"]

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
