from model_service import correct_code_with_ai
import sys

print("Testing model service...")
buggy_code = "def add(a, b): return a - b # Bug: should be +"
result = correct_code_with_ai(buggy_code)
print("\n--- Result ---")
print(result)
print("--- End Result ---")
