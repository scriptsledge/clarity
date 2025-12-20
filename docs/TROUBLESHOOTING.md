# 🔧 Troubleshooting & Post-Mortem Log

> "Mistakes are the portals of discovery." — *James Joyce*

This document serves as a **Knowledge Base** for the specific technical challenges encountered during the development of Clarity, and the architectural decisions made to resolve them.

---

## 🛑 Critical System Errors

### 1. The `GGML_ASSERT` Crash
**Symptom:** The backend server would crash silently or with a segmentation fault when processing code.
```text
ggml-cpu/ops.cpp:5399: GGML_ASSERT(i1 >= 0 && i1 < ne1) failed
```
**Root Cause:**
Two distinct issues were colliding:
1.  **Context Overflow:** The prompt + generation exceeded the `n_ctx` (Context Window) of the model.
2.  **Race Condition:** The Frontend's "Health Check" was aggressively re-enabling the "Optimize" button while a request was still processing. If the user double-clicked, `llama.cpp` (running single-threaded per slot) would corrupt its memory state.

**Solution:**
*   **Backend:** Increased `n_ctx` to `4096` (and `8192` where RAM permits).
*   **Frontend:** Implemented a **Mutex Lock (`isProcessing`)**. The UI now strictly disables interaction until the current transaction completes, regardless of Health Check status.

### 2. High Latency on CPU
**Symptom:** Inference took 30+ seconds on local hardware.
**Solution:**
*   Switched from `transformers` (PyTorch) to **`llama.cpp`** (GGUF).
*   Utilized **4-bit Quantization** (`Q4_K_M`) to reduce memory bandwidth pressure.
*   Result: Inference dropped to <5 seconds on standard CPUs.

---

## 🎨 UI & Theming Challenges

### 1. The "Brown Box" Syntax Highlighting
**Symptom:** Code blocks appeared with an ugly, opaque background color that clashed with the Glassmorphism UI.
**Cause:** `Highlight.js` themes apply their own `background-color` to the `<code>` block.
**Solution:**
We forced a transparent background in our global CSS to let the Catppuccin surface shine through:
```css
code.hljs {
    background: transparent !important;
}
```

### 2. Light Mode "Washed Out" Sidebar
**Symptom:** In "Latte" (Light) mode, the sidebar was indistinguishable from the main background.
**Solution:**
We implemented theme-specific transparency overrides.
*   **Dark Modes:** High opacity (0.85) for contrast against deep backgrounds.
*   **Light Mode:** Lower opacity (0.60) to keep the sidebar feeling "airy" and distinct.

---

## 🧠 AI Behavior

### 1. "I am an AI developed by..." (Hallucinations)
**Symptom:** The 7B model would waste tokens introducing itself as generic AI.
**Solution:**
We implemented a **Strict Persona System Prompt** combined with **One-Shot Prompting**. By providing a single "ideal" dialogue example (Input -> Code Only), the model latches onto the pattern and skips the pleasantries.

### 2. Language Detection Failures
**Symptom:** Small snippets (e.g., `val x = 1`) were misidentified as Text or C++.
**Solution:**
We moved detection from **Input** to **Output**. Since the AI *corrects* and *completes* the code (e.g., adding `class Main` or `#include`), the output is significantly easier to classify than the messy input.

---

## 📚 See Also
*   [Architecture Guide](ARCHITECTURE.md) - How the pieces fit together.
*   [AI Manifesto](AI_MANIFESTO.md) - The "Soul" of the AI.
*   [Deployment Guide](DEPLOYMENT_GUIDE.md) - Shipping to production.
