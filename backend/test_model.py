import sys

print("Testing model service...")

try:
    from model_service import correct_code_with_ai
except ImportError as e:
    print(f"\nCRITICAL: Missing dependencies. Please run 'pip install -r requirements.txt' in the backend directory.\nError: {e}")
    sys.exit(1)

buggy_code = "def add(a, b): return a - b # Bug: should be +"

print(f"\nInput Code:\n{buggy_code}")

try:
    result = correct_code_with_ai(buggy_code)
    print("\n--- Result ---")
    print(result)
    print("--- End Result ---")
except Exception as e:
    print(f"\nError during inference: {e}")