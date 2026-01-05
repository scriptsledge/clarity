# 🐛 Bug Tracker & Known Issues

This document tracks resolved bugs and current known issues for the Clarity project.

## ✅ Resolved Bugs

### 1. Port Mismatch
- **Issue:** Backend was running on 7860 but docs/frontend expected 8000.
- **Fix:** Standardized on port `7860` for the backend to match Hugging Face Spaces default.

### 2. Network Logic
- **Issue:** Frontend had hardcoded `localhost` URLs, breaking Docker/Cloud deployments.
- **Fix:** Implemented dynamic `API_BASE` resolution in `script.js` to handle Local, Docker, and Cloud environments automatically.

### 3. Model Blocking (Lazy Loading)
- **Issue:** Backend server startup was slow because it loaded the heavy AI model immediately.
- **Fix:** Implemented "Lazy Loading". The model now only loads upon the first request or health check, making startup instant.

### 4. "Weird Stroke" on Dropdown
- **Issue:** The model selection menu had an ugly native border.
- **Fix:** Replaced the native `<select>` with a custom-built CSS dropdown matching the Glassmorphism theme.

### 5. Mobile Responsiveness / Branding
- **Issue:** Mobile view lacked branding and access to Settings/API Configuration.
- **Fix:** Added a mobile-specific header with the "Clarity" logo and moved Settings/API buttons to the top bar for mobile users.

## ⚠️ Known Issues / Limitations

### 1. File Protocol Restrictions
- **Description:** Opening `index.html` directly (double-click) may block API requests due to CORS/Browser security.
- **Workaround:** Always serve the frontend using a local server (e.g., `python -m http.server`).

### 2. Mobile Keyboard
- **Description:** On very small screens, the code editor might be hard to scroll when the virtual keyboard is open.
- **Status:** Mitigation planned (Editor Resizing).

### 3. "Refactor Engine" Title Visibility
- **Description:** On Desktop, "Refactor Engine" is the main title. On mobile, it is hidden in favor of "Clarity" to save space.
- **Status:** Intentional Design.
