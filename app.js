// ==========================================
// AUTHENTICATION GUARD
// ==========================================
(function checkAuth() {
    const user = sessionStorage.getItem('marketmind_user');
    if (!user) {
        // Redirect to login if not authenticated
        window.location.href = 'login.html';
        return;
    }
})();

document.addEventListener('DOMContentLoaded', () => {

    // Update user info from session
    try {
        const userData = JSON.parse(sessionStorage.getItem('marketmind_user'));
        const userName = userData.name || 'User';
        const userNameElement = document.querySelector('.user-info .name');
        if (userNameElement) {
            userNameElement.textContent = userName.charAt(0).toUpperCase() + userName.slice(1);
        }

        // Update avatar with first letter
        const avatarElement = document.querySelector('.avatar');
        if (avatarElement) {
            avatarElement.textContent = userName.charAt(0).toUpperCase();
        }
    } catch (e) {
        console.error('Error parsing user data:', e);
    }

    // --- Character Counter & Input Validation ---
    function setupCharacterCounter(textareaId, minChars = 20) {
        const textarea = document.getElementById(textareaId);
        if (!textarea) return;

        // Create counter container
        const counterDiv = document.createElement('div');
        counterDiv.className = 'char-counter';
        counterDiv.style.cssText = `
            font-size: 0.8rem;
            margin-top: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        `;

        const countSpan = document.createElement('span');
        countSpan.className = 'char-count';

        const warningSpan = document.createElement('span');
        warningSpan.className = 'char-warning';
        warningSpan.style.cssText = `
            color: #f59e0b;
            font-style: italic;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        counterDiv.appendChild(countSpan);
        counterDiv.appendChild(warningSpan);

        // Insert after textarea
        textarea.parentNode.insertBefore(counterDiv, textarea.nextSibling);

        // Update counter on input
        const updateCounter = () => {
            const length = textarea.value.length;
            countSpan.textContent = `${length} characters`;
            countSpan.style.color = length < 10 ? '#ef4444' : length < minChars ? '#f59e0b' : '#4ade80';

            if (length > 0 && length < 10) {
                warningSpan.textContent = '⚠️ Very short - may reduce AI quality';
                warningSpan.style.opacity = '1';
            } else if (length >= 10 && length < minChars) {
                warningSpan.textContent = `💡 ${minChars}+ characters recommended`;
                warningSpan.style.opacity = '1';
            } else {
                warningSpan.style.opacity = '0';
            }
        };

        textarea.addEventListener('input', updateCounter);
        updateCounter(); // Initial update
    }

    // Setup character counters for all textareas
    setTimeout(() => {
        setupCharacterCounter('mkt-desc', 50);
        setupCharacterCounter('sales-desc', 50);
        setupCharacterCounter('lead-data', 30);
    }, 100);

    // Helper: Simple Markdown-to-HTML parser (Frontend)
    // We expect the backend to return Markdown.
    function formatOutput(text) {
        if (!text) return "";
        let html = text
            // Headers
            .replace(/^### (.*$)/gim, '<h4>$1</h4>')
            .replace(/^## (.*$)/gim, '<h3>$1</h3>')
            // Bold
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            // Lists
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            // Double newlines to paragraphs (or breaks)
            .replace(/\n\n/g, '<br><br>')
            // Single newlines
            .replace(/\n/g, '<br>');

        // Fix list wrapping logic: Group adjacent LIs into a UL
        // This is a simplistic approach for demo purposes
        html = html.replace(/<\/li><br><li>/g, '</li><li>');
        html = html.replace(/<\/li><br><br><li>/g, '</li><li>');

        // Wrap any sequence of LIs in UL
        if (html.includes('<li>')) {
            html = html.replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>');
            html = html.replace(/<\/ul><ul>/g, ''); // cleanup
        }

        return html;
    }

    // --- Navigation Logic ---
    const navBtns = document.querySelectorAll('.nav-btn');
    const modules = document.querySelectorAll('.module');
    const pageTitle = document.getElementById('page-title');

    // Mobile Menu Toggle Logic
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('main-sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (mobileMenuToggle && sidebar && overlay) {
        mobileMenuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : '';
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    const titles = {
        'marketing-module': 'Marketing Campaign Generator',
        'sales-module': 'Sales Pitch Generator',
        'lead-module': 'Lead Qualification & Scoring'
    };

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            modules.forEach(m => m.classList.remove('active'));
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
            pageTitle.textContent = titles[targetId];

            // Close sidebar when clicking a nav button on mobile
            if (window.innerWidth <= 1024 && sidebar && overlay) {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // --- Logo Navigation ---
    const logo = document.getElementById('logo-home');
    if (logo) {
        logo.addEventListener('click', () => {
            // Reset to first module (Marketing)
            navBtns.forEach(b => b.classList.remove('active'));
            modules.forEach(m => m.classList.remove('active'));
            navBtns[0].classList.add('active');
            document.getElementById('marketing-module').classList.add('active');
            pageTitle.textContent = titles['marketing-module'];
        });
    }

    // --- Profile Dropdown Menu ---
    const profileTrigger = document.getElementById('profile-menu-trigger');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileTrigger && profileDropdown) {
        profileTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', () => {
            profileDropdown.classList.remove('active');
        });

        // Prevent dropdown from closing when clicking inside it
        profileDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Logout functionality
    const logoutItem = document.querySelector('.dropdown-item.logout');
    if (logoutItem) {
        logoutItem.addEventListener('click', () => {
            sessionStorage.removeItem('marketmind_user');
            window.location.href = 'login.html';
        });
    }


    // --- Action Buttons (Copy & PDF Export) ---
    function addActionButtons(outputElementId, moduleTitle) {
        const outputContainer = document.getElementById(outputElementId);
        if (!outputContainer) return;

        // Remove existing action bar if any
        const existingBar = outputContainer.querySelector('.action-button-bar');
        if (existingBar) existingBar.remove();

        // Create action button bar
        const actionBar = document.createElement('div');
        actionBar.className = 'action-button-bar';
        actionBar.style.cssText = `
            position: absolute;
            top: 16px;
            right: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 10;
        `;

        // Create Copy button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'action-btn copy-btn';
        copyBtn.innerHTML = '<i class="fa-solid fa-copy"></i> Copy';
        copyBtn.style.cssText = `
            background: #ffffff;
            border: 1.5px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 8px 16px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 8px rgba(66, 133, 244, 0.1);
        `;

        copyBtn.addEventListener('click', async () => {
            const textContent = outputContainer.innerText
                .replace('Copy', '')
                .replace('Download PDF', '')
                .replace('Copied!', '')
                .replace('Downloaded!', '')
                .trim();

            try {
                await navigator.clipboard.writeText(textContent);

                // Visual feedback
                copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
                copyBtn.style.background = 'var(--accent-green)';
                copyBtn.style.borderColor = 'var(--accent-green)';
                copyBtn.style.color = '#ffffff';

                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fa-solid fa-copy"></i> Copy';
                    copyBtn.style.background = '#ffffff';
                    copyBtn.style.borderColor = 'var(--accent-blue)';
                    copyBtn.style.color = 'var(--accent-blue)';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });

        // Create PDF button
        const pdfBtn = document.createElement('button');
        pdfBtn.className = 'action-btn pdf-btn';
        pdfBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> PDF';
        pdfBtn.style.cssText = `
            background: #ffffff;
            border: 1.5px solid var(--accent-red);
            color: var(--accent-red);
            padding: 8px 16px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 8px rgba(234, 67, 53, 0.1);
        `;

        pdfBtn.addEventListener('click', () => {
            const textContent = outputContainer.innerText
                .replace('Copy', '')
                .replace('Download PDF', '')
                .replace('PDF', '')
                .replace('Copied!', '')
                .replace('Downloaded!', '')
                .trim();
            const timestamp = new Date().toLocaleString();

            const pdfContent = `
MarketMind - ${moduleTitle}
Generated: ${timestamp}

${textContent}

---
Powered by MarketMind AI
            `.trim();

            // Create blob and download
            const blob = new Blob([pdfContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `MarketMind_${moduleTitle.replace(/\s+/g, '_')}_${Date.now()}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            // Visual feedback
            pdfBtn.innerHTML = '<i class="fa-solid fa-check"></i> Done!';
            pdfBtn.style.background = 'var(--accent-green)';
            pdfBtn.style.borderColor = 'var(--accent-green)';
            pdfBtn.style.color = '#ffffff';

            setTimeout(() => {
                pdfBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i> PDF';
                pdfBtn.style.background = '#ffffff';
                pdfBtn.style.borderColor = 'var(--accent-red)';
                pdfBtn.style.color = 'var(--accent-red)';
            }, 2000);
        });

        // Add buttons to action bar
        actionBar.appendChild(copyBtn);
        actionBar.appendChild(pdfBtn);

        // Add action bar to output container
        outputContainer.style.position = 'relative';
        outputContainer.appendChild(actionBar);
    }

    // --- Output History Management ---
    function saveToHistory(moduleId, content) {
        const historyKey = `marketmind_history_${moduleId}`;
        let history = JSON.parse(sessionStorage.getItem(historyKey) || '[]');

        // Add new entry with timestamp
        history.unshift({
            content: content,
            timestamp: new Date().toISOString(),
            preview: content.substring(0, 100) + '...'
        });

        // Keep only last 5
        history = history.slice(0, 5);

        sessionStorage.setItem(historyKey, JSON.stringify(history));
    }

    function getHistory(moduleId) {
        const historyKey = `marketmind_history_${moduleId}`;
        return JSON.parse(sessionStorage.getItem(historyKey) || '[]');
    }

    // --- Form Reset Function (Global) ---
    window.resetForm = function (formId) {
        if (confirm('Clear all form fields?')) {
            const form = document.getElementById(formId);
            if (form) {
                form.reset();
            }
        }
    };

    // --- Helper Functions ---

    function setLoading(elementId, isLoading, buttonElement) {
        const outputContainer = document.getElementById(elementId);
        outputContainer.style.position = 'relative';
        if (isLoading) {
            // Clear previous output immediately
            outputContainer.innerHTML = `
                <div class="loading-overlay">
                    <div class="loader"></div>
                    <p id="loading-step-text">Step 1/3: Analyzing inputs...</p>
                </div>
            `;

            // Step-based progress messaging
            const stepText = document.getElementById('loading-step-text');
            if (stepText) {
                setTimeout(() => {
                    stepText.textContent = 'Step 2/3: Generating insights...';
                }, 1000);
                setTimeout(() => {
                    stepText.textContent = 'Step 3/3: Formatting results...';
                }, 2000);
            }

            // Disable button
            if (buttonElement) {
                buttonElement.disabled = true;
            }
        } else {
            // Re-enable button
            if (buttonElement) {
                buttonElement.disabled = false;
            }
        }
    }

    function displayResult(elementId, content) {
        const outputDiv = document.getElementById(elementId);
        outputDiv.classList.remove('placeholder-text');
        outputDiv.innerHTML = formatOutput(content);

        // Determine module title for PDF
        let moduleTitle = 'Output';
        if (elementId === 'mkt-output') moduleTitle = 'Marketing_Campaign';
        else if (elementId === 'sales-output') moduleTitle = 'Sales_Pitch';
        else if (elementId === 'lead-output') moduleTitle = 'Lead_Scoring';

        // Add action buttons (Copy + PDF) in grouped bar
        addActionButtons(elementId, moduleTitle);

        // Save to history
        saveToHistory(elementId, content);
    }

    // --- API Configuration ---
    // Robust detection: If on file protocol or wrong port, default to the Flask backend port
    const API_BASE = (window.location.protocol === 'file:' || (window.location.port !== '5001' && window.location.hostname === '127.0.0.1'))
        ? 'http://127.0.0.1:5001'
        : window.location.origin;

    console.log(`[MarketMind] API Base set to: ${API_BASE}`);

    async function callApi(endpoint, payload, outputId, buttonElement) {
        setLoading(outputId, true, buttonElement);
        try {
            const apiUrl = `${API_BASE}${endpoint}`;
            console.log(`[MarketMind] Calling: ${apiUrl}`);

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error(`[MarketMind] Server Error (${response.status}):`, errorText);
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            displayResult(outputId, data.result);

        } catch (error) {
            console.error("[MarketMind] API Fetch Failure:", error);
            const failureMsg = `### ⚠️ Connection Error\n\n**Note:**\nUnable to connect to the AI backend. \n\n**Troubleshooting:**\n1. Ensure your terminal is running \`python app.py\`\n2. Check if the backend is active at [http://127.0.0.1:5001](http://127.0.0.1:5001)\n3. Check browser console for detailed CORS or Network errors.`;
            displayResult(outputId, failureMsg);
        } finally {
            // Re-enable button after completion
            setLoading(outputId, false, buttonElement);
        }
    }

    // --- Module 1: Marketing Campaign Generator ---

    const marketingForm = document.getElementById('marketing-form');
    marketingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const payload = {
            product: document.getElementById('mkt-product').value,
            description: document.getElementById('mkt-desc').value,
            audience: document.getElementById('mkt-audience').value,
            platform: document.getElementById('mkt-platform').value
        };
        await callApi('/api/marketing', payload, 'mkt-output', submitBtn);
    });


    // --- Module 2: Sales Pitch Generator ---

    const salesForm = document.getElementById('sales-form');
    salesForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const payload = {
            product: document.getElementById('sales-product').value,
            persona: document.getElementById('sales-persona').value,
            industry: document.getElementById('sales-industry').value,
            size: document.getElementById('sales-size').value,
            budget: document.getElementById('sales-budget').value
        };
        await callApi('/api/sales', payload, 'sales-output', submitBtn);
    });


    // --- Module 3: Lead Qualification & Scoring ---

    const leadForm = document.getElementById('lead-form');
    leadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const payload = {
            product: document.getElementById('lead-product').value,
            icp: document.getElementById('lead-icp').value,
            valueProp: document.getElementById('lead-value').value,
            leadData: document.getElementById('lead-data').value
        };
        await callApi('/api/lead-scoring', payload, 'lead-output', submitBtn);
    });

    // Soft Launch Welcome
    setTimeout(() => {
        const welcome = document.createElement('div');
        welcome.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            transform: translateY(100px);
            transition: transform 0.5s ease;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        welcome.innerHTML = '<i class="fa-solid fa-rocket"></i> <div><strong>Soft Launch Live</strong><br><span style="font-size:0.8em">Welcome to MarketMind Beta v1.0</span></div>';
        document.body.appendChild(welcome);
        setTimeout(() => welcome.style.transform = 'translateY(0)', 100);
        setTimeout(() => welcome.style.transform = 'translateY(100px)', 5000);
    }, 1000);

});
