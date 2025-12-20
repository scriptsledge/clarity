// CONFIGURATION
const isDev = window.location.port !== '' && window.location.port !== '80' && window.location.port !== '443';
const ENDPOINTS = {
    LOCAL: 'http://127.0.0.1:8000',  // python backend/main.py
    DOCKER: isDev ? 'http://127.0.0.1:7860' : '', // Smart switching: Dev -> Direct, Prod -> Nginx
    CLOUD: 'https://scriptsledge-clarity-backend.hf.space'
};

// State: 'LOCAL' | 'DOCKER' | 'CLOUD'
let CURRENT_MODE = 'CLOUD'; 
let API_BASE = ENDPOINTS[CURRENT_MODE];

// DOM Elements
const correctBtn = document.getElementById('correctBtn');
const codeInput = document.getElementById('codeInput');
const codeOutput = document.getElementById('codeOutput');
const copyOutputBtn = document.getElementById('copyOutputBtn');
const latencyStat = document.getElementById('latency');
const statusDot = document.querySelector('.status-dot');
const statusText = document.querySelector('.status-text');
const backendToggle = document.getElementById('backendToggle');

// Language UI Elements
const inputTab = document.getElementById('inputTab');
const outputTab = document.getElementById('outputTab');
const langStat = document.getElementById('langStat');

// Settings Elements
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');
const themeToggle = document.getElementById('themeToggle');

// 1. Initialization
async function initializeSystem() {
    console.log('[Clarity] Initializing...');
    updateToggleUI(); 
    
    // Initial check
    await performHealthCheck();
}

// Re-usable check function
async function performHealthCheck() {
    try {
        await checkHealth(API_BASE);
        // If checkHealth resolves, we are good
        setSystemStatus('online', "System Online");
    } catch (e) {
        console.warn("Health check failed:", e);
        setSystemStatus('offline', "Offline / Connecting...");
    }
}

async function checkHealth(baseUrl) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); 
    let url = baseUrl === '' ? '/api/health' : `${baseUrl}/api/health`;
    
    try {
        const response = await fetch(url, { signal: controller.signal });
        clearTimeout(timeoutId);
        
        // INTELLIGENT STATUS CHECK
        // 1. If 200 OK -> Always Good.
        if (response.ok) return true;

        // 2. Cloud Exception: HF Spaces often return 404/405 on root or specific paths
        // but the connection is actually alive.
        if (CURRENT_MODE === 'CLOUD' && (response.status === 404 || response.status === 405)) {
            return true; 
        }

        // 3. Otherwise (e.g., Docker/Local): 404/405 are actual failures for the health check endpoint.
        // So for Docker/Local, 404 is a FAILURE.
        
        throw new Error(`HTTP Status ${response.status}`);

    } catch (e) {
        throw e; // Network errors will throw here
    }
}

function setSystemStatus(state, msg) {
    if(!statusDot || !statusText) return;

    statusText.textContent = msg;
    
    // CRITICAL: Disable button if offline, enable otherwise
    if (state === 'offline') {
        correctBtn.disabled = true; 
    } else {
        correctBtn.disabled = false;
    }

    if (state === 'online') {
        statusDot.style.backgroundColor = 'var(--green)';
        statusDot.style.boxShadow = '0 0 8px var(--green)';
        statusText.style.color = 'var(--green)';
    } else { // State is 'offline'
        statusDot.style.backgroundColor = 'var(--red)';
        statusDot.style.boxShadow = 'none';
        statusText.style.color = 'var(--red)';
    }
}

function updateToggleUI() {
    if (!backendToggle) return;
    const modeText = backendToggle.querySelector('.mode-text');
    const modeIcon = backendToggle.querySelector('span.mode-icon');
    
    switch (CURRENT_MODE) {
        case 'LOCAL':
            modeText.textContent = 'Local';
            if(modeIcon) modeIcon.textContent = '💻';
            break;
        case 'DOCKER':
            modeText.textContent = 'Docker';
            if(modeIcon) modeIcon.textContent = '🐳';
            break;
        case 'CLOUD':
            modeText.textContent = 'Cloud';
            if(modeIcon) modeIcon.textContent = '☁️';
            break;
    }
}

// 2. Toggle Logic
if (backendToggle) {
    backendToggle.addEventListener('click', async () => {
        if (CURRENT_MODE === 'LOCAL') {
            CURRENT_MODE = 'DOCKER';
        } else if (CURRENT_MODE === 'DOCKER') {
            CURRENT_MODE = 'CLOUD';
        } else {
            CURRENT_MODE = 'LOCAL';
        }
        
        API_BASE = ENDPOINTS[CURRENT_MODE];
        updateToggleUI();
        
        // Show checking state
        setSystemStatus('offline', "Checking..."); 
        await performHealthCheck();
    });
}

// 3. Optimization Logic
if (correctBtn) {
    correctBtn.addEventListener('click', async () => {
        const code = codeInput.value;
        if (!code.trim()) return;

        const originalHtml = correctBtn.innerHTML;
        correctBtn.innerHTML = '<i class="ph ph-spinner ph-spin"></i> Processing...';
        correctBtn.disabled = true; // Disable while processing
        codeOutput.style.opacity = '0.5';
        
        const startTime = performance.now();

        try {
            const url = API_BASE === '' ? '/api/correct' : `${API_BASE}/api/correct`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code }),
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();
            codeOutput.style.opacity = '1';
            codeOutput.textContent = data.corrected_code;
            
            // Auto-update Language UI if data exists
            if (data.language) {
                const { name, ext } = data.language;
                if (langStat) langStat.textContent = name;
                if (inputTab) inputTab.innerHTML = `<i class="ph ph-file-code"></i> source.${ext}`;
                if (outputTab) outputTab.innerHTML = `<i class="ph ph-sparkle"></i> optimized.${ext}`;
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
            correctBtn.innerHTML = originalHtml;
            // Only re-enable if current status is not offline (from health check)
            // If offline, keep disabled
            if (statusDot.style.backgroundColor !== 'var(--red)') {
                 correctBtn.disabled = false;
            }
        }
    });
}

// 4. Copy Logic
const copyInputBtn = document.getElementById('copyInputBtn');

async function handleCopy(text, btnElement) {
    if (!text) return;
    const icon = btnElement.querySelector('i');
    
    // Helper to show status without destroying DOM
    const showStatus = (type) => {
        if (!icon) return;
        const originalClass = 'ph ph-copy';
        
        if (type === 'success') icon.className = 'ph ph-check';
        else if (type === 'error') icon.className = 'ph ph-warning';
        
        setTimeout(() => icon.className = originalClass, 2000);
    };

    try {
        // Priority 1: Modern Clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(text);
            showStatus('success');
        } else {
            throw new Error('Clipboard API unavailable');
        }
    } catch (err) {
        // Priority 2: Fallback to execCommand
        try {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.left = '-9999px';
            textarea.style.top = '0';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            
            const successful = document.execCommand('copy');
            document.body.removeChild(textarea);
            
            if (successful) showStatus('success');
            else showStatus('error');
        } catch (fallbackErr) {
            console.error('Copy failed:', fallbackErr);
            showStatus('error');
        }
    }
}

if (copyOutputBtn) {
    copyOutputBtn.addEventListener('click', () => handleCopy(codeOutput.textContent, copyOutputBtn));
}

if (copyInputBtn) {
    copyInputBtn.addEventListener('click', () => handleCopy(codeInput.value, copyInputBtn));
}

// 5. Tab Support
if (codeInput) {
    codeInput.addEventListener('keydown', function(e) {
        if (e.key == 'Tab') {
            e.preventDefault();
            this.value = this.value.substring(0, this.selectionStart) + "    " + this.value.substring(this.selectionEnd);
            this.selectionStart = this.selectionEnd = this.selectionStart + 4;
        }
    });
}

// 6. Settings Logic
if (settingsBtn && settingsModal && closeSettings) {
    settingsBtn.addEventListener('click', (e) => {
        e.preventDefault();
        settingsModal.classList.remove('hidden');
    });

    closeSettings.addEventListener('click', () => {
        settingsModal.classList.add('hidden');
    });

    // Close on click outside
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.add('hidden');
        }
    });
}

// 7. Theme Toggle Logic
if (themeToggle) {
    let isLight = false;
    themeToggle.addEventListener('click', () => {
        isLight = !isLight;
        document.body.classList.toggle('light-theme');
        
        const icon = themeToggle.querySelector('i');
        const text = themeToggle.querySelector('span');
        
        if (isLight) {
            icon.className = 'ph ph-sun';
            text.textContent = 'Latte (Light)';
        } else {
            icon.className = 'ph ph-moon';
            text.textContent = 'Mocha (Dark)';
        }
    });
}

// Start
initializeSystem();
// Auto-Check every 30s
setInterval(performHealthCheck, 30000);