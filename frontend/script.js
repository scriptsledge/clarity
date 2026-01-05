// CONFIGURATION
const isVercel = window.location.hostname.includes('vercel.app');
const isDev = !isVercel && window.location.port !== '' && window.location.port !== '80' && window.location.port !== '443';
const ENDPOINTS = {
    LOCAL: `${window.location.protocol}//${window.location.hostname}:7860`,
    DOCKER: '', // Relative path for Docker/Nginx (same origin)
    CLOUD: 'https://scriptsledge-clarity-backend.hf.space'
};

// State
let CURRENT_MODE = 'GOOGLE'; // Default
let API_BASE = (isDev) ? ENDPOINTS.LOCAL : (isVercel ? ENDPOINTS.CLOUD : ENDPOINTS.DOCKER);
let isProcessing = false;

// UI Elements
const correctBtn = document.getElementById('correctBtn');
const codeInput = document.getElementById('codeInput');
const codeOutput = document.getElementById('codeOutput');
const copyOutputBtn = document.getElementById('copyOutputBtn');
const latencyStat = document.getElementById('latency');
const statusDot = document.querySelector('.status-dot');
const statusText = document.querySelector('.status-text');

// Advanced Model Controls
const providerToggle = document.getElementById('providerToggle');
const providerLabel = document.getElementById('providerLabel');
const googleVersionWrapper = document.getElementById('googleVersionWrapper');
// const googleVersionSelect = document.getElementById('googleVersionSelect'); // Removed

// Settings
const apiSettingsBtn = document.getElementById('apiSettingsBtn');
const apiModal = document.getElementById('apiModal');
const closeApiSettings = document.getElementById('closeApiSettings');
const googleApiKeyInput = document.getElementById('googleApiKey');
const saveApiBtn = document.getElementById('saveApiBtn');

const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');

// Language UI Elements
const inputTab = document.getElementById('inputTab');
const outputTab = document.getElementById('outputTab');
const langStat = document.getElementById('langStat');

// Mobile Buttons
const mobileApiBtn = document.getElementById('mobileApiBtn');
const mobileSettingsBtn = document.getElementById('mobileSettingsBtn');

if (mobileApiBtn && apiModal) {
    mobileApiBtn.addEventListener('click', () => {
        apiModal.classList.remove('hidden');
        loadSettings();
    });
}

if (mobileSettingsBtn && settingsModal) {
    mobileSettingsBtn.addEventListener('click', () => {
        settingsModal.classList.remove('hidden');
        // Load settings values... (logic shared/duplicated or handled by existing)
        const savedIn = localStorage.getItem('clarity-fs-in') || '14';
        const savedOut = localStorage.getItem('clarity-fs-out') || '14';
        if (inputFS) inputFS.value = savedIn;
        if (outputFS) outputFS.value = savedOut;
        if (inSizeVal) inSizeVal.textContent = savedIn + 'px';
        if (outSizeVal) outSizeVal.textContent = savedOut + 'px';
    });
}

function loadSettings() {
    const savedKey = localStorage.getItem('clarity-google-api-key');
    if (savedKey && googleApiKeyInput) googleApiKeyInput.value = savedKey;
}

// Toast Notification
const toastContainer = document.getElementById('toastContainer');

function showToast(message, type = 'info') {
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'info';
    if (type === 'success') icon = 'check-circle';
    if (type === 'error') icon = 'warning-circle';
    if (type === 'warning') icon = 'warning';

    toast.innerHTML = `<i class="ph ph-${icon}"></i> <span>${message}</span>`;

    toastContainer.appendChild(toast);

    // Auto remove
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// File Protocol Warning
if (window.location.protocol === 'file:') {
    setTimeout(() => {
        showToast("Browsers block 'file://' requests. Usage may be limited.", 'warning');
    }, 1000);
}

if (saveApiBtn) {
    saveApiBtn.addEventListener('click', async () => {
        const key = googleApiKeyInput.value.trim();
        localStorage.setItem('clarity-google-api-key', key);

        // Visual Feedback
        const originalHtml = saveApiBtn.innerHTML;
        saveApiBtn.innerHTML = '<i class="ph ph-circle-notch ph-spin"></i> Verifying...';
        saveApiBtn.disabled = true;

        // Reset Cache & Trigger Re-Discovery
        cachedGoogleModels = null;
        if (CURRENT_MODE === 'GOOGLE') {
            await fetchGoogleModels();
            await performHealthCheck();
        }

        setTimeout(() => {
            saveApiBtn.innerHTML = '<i class="ph ph-check-circle"></i> Applied Successfully';
            saveApiBtn.style.background = 'var(--green)';
            saveApiBtn.style.color = 'var(--base)';

            setTimeout(() => {
                saveApiBtn.innerHTML = originalHtml;
                saveApiBtn.style.background = '';
                saveApiBtn.style.color = '';
                saveApiBtn.disabled = false;
                // Close modal after short delay
                apiModal.classList.add('hidden');
            }, 1500);
        }, 800);
    });
}

// 2. Mode Switching Logic (Toggle Cycle)
const MODES = ['GOOGLE', 'LOCAL', 'CLOUD'];

function cycleMode() {
    const currentIndex = MODES.indexOf(CURRENT_MODE);
    const nextIndex = (currentIndex + 1) % MODES.length;
    CURRENT_MODE = MODES[nextIndex];

    // Update Endpoint Logic
    switch (CURRENT_MODE) {
        case 'GOOGLE':
            // 1. Dev -> Local Backend
            // 2. Vercel -> Cloud Backend (Cross-Origin to HF Spaces)
            // 3. Docker/Nginx -> Relative Path (Same Origin)
            if (isDev) {
                API_BASE = ENDPOINTS.LOCAL;
            } else if (isVercel) {
                API_BASE = ENDPOINTS.CLOUD;
            } else {
                API_BASE = ENDPOINTS.DOCKER;
            }
            break;
        case 'LOCAL':
            API_BASE = ENDPOINTS.LOCAL;
            break;
        case 'CLOUD':
            API_BASE = ENDPOINTS.CLOUD;
            break;
    }

    updateModelUI();
    setSystemStatus('offline', "Checking...");
    performHealthCheck();

    // Initial Fetch for Google Models if active
    if (CURRENT_MODE === 'GOOGLE') {
        fetchGoogleModels();
    }
}

function updateModelUI() {
    if (!providerLabel || !providerToggle) return;

    // Update Label
    if (CURRENT_MODE === 'GOOGLE') {
        providerLabel.textContent = 'Google';
        providerToggle.innerHTML = '<i class="ph ph-google-logo"></i> <span>Google</span>';

        // Show Sub-Menu
        if (googleVersionWrapper) {
            googleVersionWrapper.classList.remove('hidden');
            fetchGoogleModels();
        }
    } else if (CURRENT_MODE === 'LOCAL') {
        providerLabel.textContent = 'Local (Qwen)';
        providerToggle.innerHTML = '<i class="ph ph-hard-drives"></i> <span>Local</span>';

        if (googleVersionWrapper) googleVersionWrapper.classList.add('hidden');
    } else {
        providerLabel.textContent = 'Cloud (Qwen)';
        providerToggle.innerHTML = '<i class="ph ph-cloud"></i> <span>Cloud</span>';

        if (googleVersionWrapper) googleVersionWrapper.classList.add('hidden');
    }
}

if (providerToggle) {
    providerToggle.addEventListener('click', cycleMode);
}

// 3. Health Check
async function performHealthCheck() {
    try {
        await checkHealth(API_BASE);
        setSystemStatus('online', "System Online");
    } catch (e) {
        // Fix Race Condition: If we recently had a success (e.g. user manually triggered optimize), ignore this background failure
        if (Date.now() - lastSuccessTime < 60000) {
            console.log("Ignoring health check failure due to recent success.");
            return;
        }

        console.warn("Health check failed:", e);
        let msg = "Offline";
        if (e.name === 'AbortError') msg = "Timeout (Waking up...)";
        else if (e.message.includes('Failed to fetch')) msg = "Connection Refused (CORS?)";

        setSystemStatus('offline', msg);
        if (statusDot) statusDot.title = `Error: ${e.message}. If using file://, CORS blocks requests.`;
    }
}

async function checkHealth(baseUrl) {
    const controller = new AbortController();
    // Increase timeout to 15s to allow for HF Cold Start
    const timeoutId = setTimeout(() => controller.abort(), 15000);
    let url = baseUrl === '' ? '/api/health' : `${baseUrl}/api/health`;

    try {
        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
        if (response.ok) return true;

        // Cloud Exception
        if ((CURRENT_MODE === 'CLOUD' || (CURRENT_MODE === 'GOOGLE' && !isDev)) && (response.status === 404 || response.status === 405)) {
            return true;
        }

        throw new Error(`HTTP Status ${response.status}`);
    } catch (e) {
        console.error("Health Check Details:", { mode: CURRENT_MODE, url: url, error: e });
        throw e;
    }
}

function setSystemStatus(state, msg) {
    if (!statusDot || !statusText) return;
    statusText.textContent = msg;
    if (state === 'offline') correctBtn.disabled = true;
    else if (typeof isProcessing !== 'undefined' && !isProcessing) correctBtn.disabled = false;

    if (state === 'online') {
        statusDot.style.backgroundColor = 'var(--green)';
        statusDot.style.boxShadow = '0 0 8px var(--green)';
        statusText.style.color = 'var(--green)';
    } else {
        statusDot.style.backgroundColor = 'var(--red)';
        statusDot.style.boxShadow = 'none';
        statusText.style.color = 'var(--red)';
    }
}

// 4. Optimization Logic
if (correctBtn) {
    correctBtn.addEventListener('click', async () => {
        const code = codeInput.value;
        if (!code.trim()) return;

        isProcessing = true;
        const originalHtml = correctBtn.innerHTML;
        correctBtn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Processing...';
        correctBtn.disabled = true;
        codeOutput.style.opacity = '0.5';

        const startTime = performance.now();
        codeOutput.parentElement.classList.add('processing'); // Add shimmer effort

        try {
            const url = API_BASE === '' ? '/api/correct' : `${API_BASE}/api/correct`;

            const payload = {
                code: code,
                model_provider: CURRENT_MODE === 'GOOGLE' ? 'google' : 'local'
            };

            if (CURRENT_MODE === 'GOOGLE') {
                const key = localStorage.getItem('clarity-google-api-key');
                if (key) payload.api_key = key;

                // Add Google Model Selection
                payload.google_model_name = currentGoogleModelValue;
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                // Handle 429 Quota Exceeded Gracefully
                if (response.status === 429 || response.status === 503) {
                    const errText = await response.text();
                    if (errText.includes('quota') || errText.includes('exhausted') || errText.includes('429')) {
                        throw new Error("QUOTA_EXHAUSTED");
                    }
                }
                const errText = await response.text();
                throw new Error(`API Error: ${response.status} - ${errText}`);
            }

            const data = await response.json();
            codeOutput.style.opacity = '1';
            codeOutput.textContent = data.corrected_code;

            if (data.language) {
                const { name, ext } = data.language;
                if (langStat) langStat.textContent = name;
                if (inputTab) inputTab.innerHTML = `<i class="ph ph-file-code"></i> source.${ext}`;
                if (outputTab) outputTab.innerHTML = `<i class="ph ph-sparkle"></i> optimized.${ext}`;

                codeOutput.className = '';
                codeOutput.removeAttribute('data-highlighted');
                const hljsClass = getHljsClass(ext);
                codeOutput.classList.add(`language-${hljsClass}`);
                if (window.hljs) hljs.highlightElement(codeOutput);
            }

            const endTime = performance.now();
            const lat = Math.round(endTime - startTime);
            if (latencyStat) latencyStat.textContent = `Latency: ${lat}ms`;

            setSystemStatus('online', "System Online");
            lastSuccessTime = Date.now();

        } catch (error) {
            console.error('[Clarity] API Error:', error);

            if (error.message === 'QUOTA_EXHAUSTED') {
                codeOutput.innerHTML = `
                 <div style="padding: 1rem; color: var(--text);">
                    <h3 style="color: var(--peach); margin-bottom: 0.5rem;"><i class="ph ph-warning"></i> High Traffic / Quota Exceeded</h3>
                    <p style="margin-bottom: 1rem;">The system is experiencing high traffic or the shared quota is exhausted.</p>
                    <p style="margin-bottom: 1rem;"><b>Solution:</b> Use your own <span style="color: var(--green);">FREE</span> Google API Key to continue without limits.</p>
                    <button onclick="document.getElementById('apiModal').classList.remove('hidden')" class="secondary-btn" style="width: fit-content;">
                        <i class="ph ph-key"></i> Add Your API Key
                    </button>
                 </div>`;
                codeOutput.textContent = ''; // Clear text content to let HTML render, but checking if innerHTML overrides (it does in JS)
                // actually codeOutput is a <code> tag inside a <pre>. InnerHTML on code tag works.
                setSystemStatus('offline', "Quota Exceeded");
            } else {
                codeOutput.textContent = `# Error: ${error.message}`;
                codeOutput.style.color = 'var(--red)';
                setSystemStatus('offline', "Connection Failed");
            }
        } finally {
            isProcessing = false;
            codeOutput.parentElement.classList.remove('processing');
            correctBtn.innerHTML = originalHtml;
            if (statusDot.style.backgroundColor !== 'var(--red)') correctBtn.disabled = false;
        }
    });
}

// 5. Utilities (Copy, Tab, Theme, Fonts) - Minimized for brevity
function getHljsClass(ext) {
    const map = { 'py': 'python', 'js': 'javascript', 'ts': 'typescript', 'cs': 'csharp', 'cpp': 'cpp', 'c': 'c', 'java': 'java', 'go': 'go', 'rs': 'rust', 'rb': 'ruby', 'php': 'php', 'swift': 'swift', 'kt': 'kotlin', 'dart': 'dart', 'scala': 'scala', 'ex': 'elixir', 'erl': 'erlang', 'rkt': 'scheme', 'html': 'xml', 'css': 'css', 'sql': 'sql', 'sh': 'bash' };
    return map[ext] || ext;
}
// Copy
const copyInputBtn = document.getElementById('copyInputBtn');
async function handleCopy(text, btnElement) {
    if (!text) return;
    const icon = btnElement.querySelector('i');
    const showStatus = (type) => {
        if (!icon) return;
        const originalClass = 'ph ph-copy';
        if (type === 'success') icon.className = 'ph ph-check'; else if (type === 'error') icon.className = 'ph ph-warning';
        setTimeout(() => icon.className = originalClass, 2000);
    };
    try { await navigator.clipboard.writeText(text); showStatus('success'); } catch (err) { showStatus('error'); }
}
if (copyOutputBtn) copyOutputBtn.addEventListener('click', () => handleCopy(codeOutput.textContent, copyOutputBtn));
if (copyInputBtn) copyInputBtn.addEventListener('click', () => handleCopy(codeInput.value, copyInputBtn));

// Tab
if (codeInput) { codeInput.addEventListener('keydown', function (e) { if (e.key == 'Tab') { e.preventDefault(); this.value = this.value.substring(0, this.selectionStart) + "    " + this.value.substring(this.selectionEnd); this.selectionStart = this.selectionEnd = this.selectionStart + 4; } }); }

// Modal Logic
if (settingsBtn && settingsModal && closeSettings) {
    settingsBtn.addEventListener('click', (e) => { e.preventDefault(); settingsModal.classList.remove('hidden'); });
    closeSettings.addEventListener('click', () => settingsModal.classList.add('hidden'));
    settingsModal.addEventListener('click', (e) => { if (e.target === settingsModal) settingsModal.classList.add('hidden'); });
}
if (apiSettingsBtn && apiModal && closeApiSettings) {
    apiSettingsBtn.addEventListener('click', (e) => { e.preventDefault(); apiModal.classList.remove('hidden'); });
    closeApiSettings.addEventListener('click', () => apiModal.classList.add('hidden'));
    apiModal.addEventListener('click', (e) => { if (e.target === apiModal) apiModal.classList.add('hidden'); });
}

// Theme
const themeGrid = document.getElementById('themeGrid');
const body = document.body;
function updateActiveThemeButton(activeTheme) {
    if (!themeGrid) return;
    const buttons = themeGrid.querySelectorAll('.theme-option');
    buttons.forEach(btn => { if (btn.dataset.value === activeTheme) btn.classList.add('active'); else btn.classList.remove('active'); });
}
function applyTheme(theme) {
    body.classList.remove('theme-latte', 'theme-frappe', 'theme-macchiato', 'theme-mocha');
    if (theme === 'system') {
        if (!window.matchMedia('(prefers-color-scheme: dark)').matches) body.classList.add('theme-latte');
    } else {
        body.classList.add(`theme-${theme}`);
    }
    localStorage.setItem('clarity-theme', theme);
    updateActiveThemeButton(theme);
}
const savedTheme = localStorage.getItem('clarity-theme') || 'system';
applyTheme(savedTheme);
if (themeGrid) { themeGrid.addEventListener('click', (e) => { const btn = e.target.closest('.theme-option'); if (btn) applyTheme(btn.dataset.value); }); }

// Fonts
const inputFS = document.getElementById('inputFontSize'); const outputFS = document.getElementById('outputFontSize');
const inVal = document.getElementById('inSizeVal'); const outVal = document.getElementById('outSizeVal');
function updateFont(target, size, labelEl, storageKey) { if (!target) return; target.style.fontSize = `${size}px`; target.style.lineHeight = '1.6'; if (labelEl) labelEl.textContent = `${size}px`; localStorage.setItem(storageKey, size); }
if (inputFS && codeInput) { const savedIn = localStorage.getItem('clarity-fs-in') || '14'; inputFS.value = savedIn; updateFont(codeInput, savedIn, inVal, 'clarity-fs-in'); inputFS.addEventListener('input', (e) => updateFont(codeInput, e.target.value, inVal, 'clarity-fs-in')); }
if (outputFS && codeOutput) { const savedOut = localStorage.getItem('clarity-fs-out') || '14'; outputFS.value = savedOut; updateFont(codeOutput, savedOut, outVal, 'clarity-fs-out'); outputFS.addEventListener('input', (e) => updateFont(codeOutput, e.target.value, outVal, 'clarity-fs-out')); }

// --- Custom Dynamic Dropdown ---
let cachedGoogleModels = null;
let currentGoogleModelValue = 'gemini-flash-latest'; // Default

// UI References
const modelDropdownTrigger = document.getElementById('modelDropdownTrigger');
const modelDropdownMenu = document.getElementById('modelDropdownMenu');
const selectedModelText = document.getElementById('selectedModelText');

// Toggle Menu
if (modelDropdownTrigger) {
    modelDropdownTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        modelDropdownMenu.classList.toggle('show');
        modelDropdownTrigger.classList.toggle('active');
    });
}

// Close on Outside Click
document.addEventListener('click', (e) => {
    if (modelDropdownMenu && modelDropdownMenu.classList.contains('show')) {
        if (!modelDropdownTrigger.contains(e.target) && !modelDropdownMenu.contains(e.target)) {
            modelDropdownMenu.classList.remove('show');
            modelDropdownTrigger.classList.remove('active');
        }
    }
});

async function fetchGoogleModels() {
    // 1. Check Cache
    if (cachedGoogleModels) {
        renderCustomOptions(cachedGoogleModels);
        return;
    }

    if (!selectedModelText) return;

    // Show Loading
    const prevText = selectedModelText.textContent;
    selectedModelText.textContent = "Loading...";
    modelDropdownTrigger.disabled = true;

    try {
        const url = API_BASE === '' ? '/api/models' : `${API_BASE}/api/models`;

        const payload = {};
        const key = localStorage.getItem('clarity-google-api-key');
        if (key) payload.api_key = key;

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Fetch failed");

        const data = await response.json();

        if (data.models && data.models.length > 0) {
            cachedGoogleModels = data.models;
            renderCustomOptions(data.models);
        } else {
            fallbackToDefaultModels();
        }

    } catch (e) {
        console.warn("Model fetch failed, using defaults", e);
        fallbackToDefaultModels();
    } finally {
        // Restore Text if failed, or update if success (handled by render)
        if (!cachedGoogleModels) selectedModelText.textContent = "Flash Latest";
        modelDropdownTrigger.disabled = false;
    }
}

function renderCustomOptions(models) {
    if (!modelDropdownMenu) return;
    modelDropdownMenu.innerHTML = ''; // Clear

    models.forEach(model => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        if (model === currentGoogleModelValue) item.classList.add('selected');

        // Format Name (e.g. gemini-1.5-flash -> Gemini 1.5 Flash)
        // Simple heuristic: Capitalize and replace hyphens
        const displayName = model
            .replace('gemini-', 'Gemini ')
            .replace('flash', 'Flash')
            .replace('pro', 'Pro')
            .replace('latest', 'Latest')
            .replace(/-/g, ' ');

        item.innerHTML = `<span>${displayName}</span> <i class="ph ph-check"></i>`;

        item.addEventListener('click', () => {
            selectModel(model, displayName);
        });

        modelDropdownMenu.appendChild(item);
    });

    // Ensure trigger text matches current if possible
    if (models.includes(currentGoogleModelValue)) {
        // trigger text update is redundant if we assume user usage, but good for data sync
    }
}

function selectModel(value, displayName) {
    currentGoogleModelValue = value;
    if (selectedModelText) selectedModelText.textContent = displayName;

    // Close Menu
    modelDropdownMenu.classList.remove('show');
    modelDropdownTrigger.classList.remove('active');

    // Update Visual Selection class
    const options = modelDropdownMenu.querySelectorAll('.dropdown-item');
    options.forEach(opt => {
        if (opt.textContent.includes(displayName)) opt.classList.add('selected');
        else opt.classList.remove('selected');
    });
}

function fallbackToDefaultModels() {
    const defaults = ['gemini-flash-latest', 'gemini-1.5-flash', 'gemini-2.0-flash'];
    cachedGoogleModels = defaults;
    renderCustomOptions(defaults);
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    updateModelUI();

    // Initial System Check
    setSystemStatus('offline', "Initializing...");
    performHealthCheck();

    // Initial Fetch for Google Models if active
    if (CURRENT_MODE === 'GOOGLE') {
        fetchGoogleModels();
    }
});