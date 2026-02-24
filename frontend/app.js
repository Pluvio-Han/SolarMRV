const API_BASE = '/api';

// DOM Elements
const elSlgBalance = document.getElementById('slgBalance');
const elMusdBalance = document.getElementById('musdBalance');
const elWalletAddress = document.getElementById('walletAddress');
const elStatusDot = document.getElementById('statusDot');
const elLivePower = document.getElementById('livePower');
const elTotalEnergy = document.getElementById('totalEnergy');
const elChainTxNum = document.getElementById('chainTxNum');

let powerChartInstance = null;

// Initialize Chart.js
function initChart() {
    const ctx = document.getElementById('powerChart').getContext('2d');

    // Create gradient
    let gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(52, 211, 153, 0.4)'); // Emerald 400
    gradient.addColorStop(1, 'rgba(52, 211, 153, 0.0)');

    powerChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Generation (W)',
                data: [],
                borderColor: '#10B981', // Emerald 500
                backgroundColor: gradient,
                borderWidth: 2,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#10B981',
                pointHoverBackgroundColor: '#10B981',
                pointHoverBorderColor: '#fff',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#111827',
                    bodyColor: '#4B5563',
                    borderColor: '#E5E7EB',
                    borderWidth: 1,
                    padding: 10,
                    boxPadding: 4
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: { display: false, drawBorder: false },
                    ticks: { maxTicksLimit: 6, color: '#9CA3AF' }
                },
                y: {
                    display: true,
                    grid: { color: '#F3F4F6', drawBorder: false, borderDash: [5, 5] },
                    ticks: { color: '#9CA3AF' },
                    beginAtZero: true
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Update Chart Data
function updateChart(powerValue) {
    const now = new Date();
    const timeLabel = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;

    if (powerChartInstance.data.labels.length > 20) {
        powerChartInstance.data.labels.shift();
        powerChartInstance.data.datasets[0].data.shift();
    }

    powerChartInstance.data.labels.push(timeLabel);
    powerChartInstance.data.datasets[0].data.push(powerValue);
    powerChartInstance.update('none'); // Update without full animation for performance
}

// API Calls
async function handleAuth(actionType) {
    const passwordInput = document.getElementById('authPassword').value;
    const btn = document.getElementById(actionType === 'login' ? 'loginBtn' : 'createBtn');
    const otherBtn = document.getElementById(actionType === 'login' ? 'createBtn' : 'loginBtn');
    const errorEl = document.getElementById('authError');
    const originalText = btn.innerHTML;

    if (!passwordInput || passwordInput.length < 6) {
        errorEl.textContent = 'Password must be at least 6 characters.';
        errorEl.classList.remove('hidden');
        return;
    }

    // UI Loading state
    btn.innerHTML = `
        <svg class="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    `;
    btn.disabled = true;
    otherBtn.disabled = true;
    errorEl.classList.add('hidden');

    const endpoint = actionType === 'login' ? '/wallet/connect' : '/wallet/create';

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: passwordInput })
        });
        const data = await res.json();

        if (data.success) {
            // Setup Dashboard Data
            const addr = data.primary_address;
            document.getElementById('walletAddress').setAttribute('data-full-address', addr);
            elWalletAddress.textContent = addr;
            elStatusDot.classList.remove('bg-gray-300');
            elStatusDot.classList.add('bg-green-500');
            fetchBalances(addr);

            // Animate Overlay Away & Reveal Dashboard
            document.getElementById('authOverlay').classList.add('opacity-0', 'pointer-events-none');
            setTimeout(() => {
                document.getElementById('authOverlay').style.display = 'none';
            }, 500);

            const dashboard = document.getElementById('dashboardApp');
            dashboard.classList.remove('opacity-0', 'blur-sm', 'pointer-events-none');
            dashboard.classList.add('opacity-100', 'blur-none');

            // Start Polling Telemetry Data
            fetchDashboardSummary();
            setInterval(fetchDashboardSummary, 5000);

        } else {
            throw new Error(data.error || 'Authentication Failed');
        }
    } catch (err) {
        console.error('Wallet auth error:', err);
        errorEl.textContent = err.message || 'Server Offline or Authentication Failed.';
        errorEl.classList.remove('hidden');
        btn.innerHTML = originalText;
        btn.disabled = false;
        otherBtn.disabled = false;
    }
}

async function fetchBalances(address) {
    try {
        const res = await fetch(`${API_BASE}/wallet/balances?address=${address}`);
        const data = await res.json();
        if (data.success) {
            elSlgBalance.textContent = Number(data.data.slg).toFixed(2);
            elMusdBalance.textContent = Number(data.data.musd).toFixed(2);
        }
    } catch (err) {
        console.error('Balance fetch error:', err);
    }
}

async function fetchDashboardSummary() {
    try {
        const res = await fetch(`${API_BASE}/dashboard/summary`);
        const data = await res.json();

        if (data.success) {
            const metrics = data.data;

            // Update Metric Cards
            elLivePower.textContent = metrics.power_w;
            elTotalEnergy.textContent = metrics.energy_kwh;
            elChainTxNum.textContent = metrics.blockchain_tx_count === 'N/A' ? '--' : metrics.blockchain_tx_count;

            // Update Chart
            updateChart(metrics.power_w);

            // Animate power number slightly to show activity
            elLivePower.classList.remove('text-emerald-600');
            void elLivePower.offsetWidth; // trigger reflow
            elLivePower.classList.add('text-emerald-600');
            setTimeout(() => { elLivePower.classList.remove('text-emerald-600'); }, 500);
        }
    } catch (err) {
        console.error('Summary fetch error:', err);
    }
}

// -------------------------------------------------------------
// UI Utilities: Address Copy
// -------------------------------------------------------------
function copyAddress() {
    const el = document.getElementById('walletAddress');
    const fullAddr = el.getAttribute('data-full-address');
    if (!fullAddr) return;

    const showTooltip = () => {
        const tooltip = document.getElementById('copyTooltip');
        tooltip.classList.remove('opacity-0');
        setTimeout(() => {
            tooltip.classList.add('opacity-0');
        }, 1500);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(fullAddr).then(showTooltip);
    } else {
        // Fallback for non-HTTPS connections
        const textArea = document.createElement("textarea");
        textArea.value = fullAddr;
        textArea.style.position = "fixed";  // Avoid scrolling
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showTooltip();
        } catch (err) {
            console.error('Copy failed', err);
        }
        document.body.removeChild(textArea);
    }
}

// -------------------------------------------------------------
// Transaction History
// -------------------------------------------------------------

function addTxToHistory(type, amountIn, amountOut, txHash) {
    const container = document.getElementById('txHistoryContainer');
    if (!container) return;

    // Remove empty state if present
    if (container.children.length === 1 && container.children[0].classList.contains('text-center')) {
        container.innerHTML = '';
    }

    const shortHash = txHash ? `${txHash.substring(0, 10)}...${txHash.substring(txHash.length - 8)}` : 'Pending...';
    const explorerUrl = `https://fisco-bcos.example.com/tx/${txHash}`; // Placeholder explorer link

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    const txItem = document.createElement('div');
    txItem.className = 'py-3 border-b border-gray-100 last:border-0 flex justify-between items-center text-sm';
    txItem.innerHTML = `
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center text-blue-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path></svg>
            </div>
            <div>
                <p class="font-bold text-gray-800">Swap <span class="text-emerald-500">${amountIn} SLG</span> for <span class="text-blue-500">${amountOut} mUSD</span></p>
                <div class="flex items-center gap-2 mt-0.5">
                    <span class="text-xs text-gray-400">${timeStr}</span>
                    <a href="${explorerUrl}" target="_blank" class="text-xs text-blue-400 font-mono hover:underline inline-flex items-center gap-1">
                        ${shortHash}
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                    </a>
                </div>
            </div>
        </div>
        <div class="text-right">
            <span class="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-bold rounded">Success</span>
        </div>
    `;

    container.insertBefore(txItem, container.firstChild);
}

// User Actions
async function executeTrade() {
    const btn = document.getElementById('btnTrade');
    const amount = document.getElementById('tradeAmount').value;

    if (amount <= 0) return;

    const originalText = btn.textContent;
    btn.textContent = 'Processing Dex Tx...';
    btn.disabled = true;
    btn.classList.add('opacity-75', 'cursor-not-allowed');

    try {
        const res = await fetch(`${API_BASE}/dex/buy`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: parseFloat(amount) })
        });
        const data = await res.json();

        if (data.success) {
            // Fake animation delay for "blockchain confirmation"
            setTimeout(() => {
                btn.textContent = 'Success - Tx Confirmed!';
                btn.classList.remove('from-blue-500', 'to-indigo-500');
                btn.classList.add('from-green-500', 'to-emerald-500');

                // Update local balance mock
                const currentSlg = parseFloat(elSlgBalance.textContent);
                const currentMusd = parseFloat(elMusdBalance.textContent);
                const receivedAmount = (parseFloat(amount) * 0.15).toFixed(2);

                elSlgBalance.textContent = (currentSlg - parseFloat(amount)).toFixed(2);
                elMusdBalance.textContent = (currentMusd + parseFloat(receivedAmount)).toFixed(2);

                // Log Transaction History
                addTxToHistory('Swap', amount, receivedAmount, data.tx_hash);

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.disabled = false;
                    btn.classList.remove('opacity-75', 'cursor-not-allowed');
                    btn.classList.remove('from-green-500', 'to-emerald-500');
                    btn.classList.add('from-blue-500', 'to-indigo-500');
                    document.getElementById('tradeAmount').value = ''; // Reset Form
                    document.getElementById('receiveEst').textContent = '0.00';
                }, 3000);
            }, 1000);
        }
    } catch (err) {
        console.error('Trade error:', err);
        btn.textContent = 'Transaction Failed';
        btn.classList.remove('from-blue-500', 'to-indigo-500');
        btn.classList.add('from-red-500', 'to-red-600');
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
            btn.classList.remove('opacity-75', 'cursor-not-allowed');
            btn.classList.remove('from-red-500', 'to-red-600');
            btn.classList.add('from-blue-500', 'to-indigo-500');
        }, 3000);
    }
}

// Calculate estimated amount
document.getElementById('tradeAmount').addEventListener('input', (e) => {
    const val = parseFloat(e.target.value) || 0;
    // Mock exchange rate 1 SLG = 0.15 mUSD
    document.getElementById('receiveEst').textContent = (val * 0.15).toFixed(2);
});

// Boot Sequence
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    // The app now waits in blurred state until the user enters their Keystore password via handleAuth()
});
