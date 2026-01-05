// CONFIGURATION
const isDev = window.location.port !== '' && window.location.port !== '80' && window.location.port !== '443';
const ENDPOINTS = {
    LOCAL: 'http://127.0.0.1:7860',  // Docker default port
    DOCKER: isDev ? 'http://127.0.0.1:7860' : '', 
    CLOUD: 'https://scriptsledge-clarity-backend.hf.space'
};

// State
let CURRENT_MODE = 'GOOGLE'; // Default
let API_BASE = isDev ? ENDPOINTS.LOCAL : ENDPOINTS.CLOUD; 

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
const googleVersionSelect = document.getElementById('googleVersionSelect');

// Settings
const apiSettingsBtn = document.getElementById('apiSettingsBtn');
const apiModal = document.getElementById('apiModal');
const closeApiSettings = document.getElementById('closeApiSettings');
const googleApiKeyInput = document.getElementById('googleApiKey');

const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');

// Language UI
const inputTab = document.getElementById('inputTab');
const outputTab = document.getElementById('outputTab');
const langStat = document.getElementById('langStat');

// 1. Initialization
async function initializeSystem() {
    console.log('[Clarity] Initializing...');
    loadSettings();
    updateModelUI(); // Set initial UI state
    await performHealthCheck();
}

function loadSettings() {
    const savedKey = localStorage.getItem('clarity-google-api-key');
    if (savedKey && googleApiKeyInput) googleApiKeyInput.value = savedKey;
    if (googleApiKeyInput) {
        googleApiKeyInput.addEventListener('input', (e) => {
            const key = e.target.value.trim();
            localStorage.setItem('clarity-google-api-key', key);
            
            // Clear cache and re-fetch if we are in Google mode
            cachedGoogleModels = null;
            if (CURRENT_MODE === 'GOOGLE') {
                fetchGoogleModels();
                performHealthCheck();
            }
        });
    }
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
            API_BASE = isDev ? ENDPOINTS.LOCAL : ENDPOINTS.CLOUD;
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
            // Trigger fetch (it has internal caching)
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
        console.warn("Health check failed:", e);
        setSystemStatus('offline', "Offline / Connecting...");
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
    if(!statusDot || !statusText) return;
    statusText.textContent = msg;
    if (state === 'offline') correctBtn.disabled = true; 
    else if (!isProcessing) correctBtn.disabled = false;

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
                if (googleVersionSelect) {
                    payload.google_model_name = googleVersionSelect.value;
                }
            }
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            
            if (!response.ok) {
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

        } catch (error) {
            console.error('[Clarity] API Error:', error);
            codeOutput.textContent = `# Error: ${error.message}`;
            codeOutput.style.color = 'var(--red)';
            setSystemStatus('offline', "Connection Failed");
        } finally {
            isProcessing = false;
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
if (codeInput) { codeInput.addEventListener('keydown', function(e) { if (e.key == 'Tab') { e.preventDefault(); this.value = this.value.substring(0, this.selectionStart) + "    " + this.value.substring(this.selectionEnd); this.selectionStart = this.selectionEnd = this.selectionStart + 4; }}); }

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

// --- Dynamic Model Fetching ---
let cachedGoogleModels = null;

async function fetchGoogleModels() {
    // Prevent re-fetching if we already have the list
    if (cachedGoogleModels) {
        populateModelDropdown(cachedGoogleModels);
        return;
    }

    if (!googleVersionSelect) return;
    
    // Show Loading State
    googleVersionSelect.innerHTML = '<option>Loading models...</option>';
    googleVersionSelect.disabled = true;

    try {
        const url = API_BASE === '' ? '/api/models' : `${API_BASE}/api/models`;
        
        // Prepare Payload (Send API Key if user provided one)
        const payload = {};
        const key = localStorage.getItem('clarity-google-api-key');
        if (key) payload.api_key = key;

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to fetch models");
        
        const data = await response.json();
        
        if (data.models && data.models.length > 0 && !data.models[0].includes("Error")) {
            cachedGoogleModels = data.models; // Cache it
            populateModelDropdown(data.models);
        } else {
            // Fallback to defaults if API fails or returns error
            fallbackToDefaultModels();
        }

    } catch (e) {
        console.warn("Model fetch failed, using defaults", e);
        fallbackToDefaultModels();
    } finally {
        googleVersionSelect.disabled = false;
    }
}

function populateModelDropdown(models) {
    if (!googleVersionSelect) return;
    googleVersionSelect.innerHTML = ''; // Clear
    
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = model;
        // Format name nicely (e.g. gemini-1.5-flash -> Gemini 1.5 Flash)
        option.textContent = model;
        
        // Auto-select the best one (Flash Latest)
        if (model === 'gemini-flash-latest') option.selected = true;
        
        googleVersionSelect.appendChild(option);
    });
}

function fallbackToDefaultModels() {
    if (!googleVersionSelect) return;
    googleVersionSelect.innerHTML = `
        <option value="gemini-flash-latest" selected>Flash Latest</option>
        <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
        <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
    `;
}