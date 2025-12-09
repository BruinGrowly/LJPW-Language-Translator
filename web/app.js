const API_BASE = "/";
let radarChart = null;

// DOM Elements
const els = {
    status: document.getElementById('apiStatus'),
    input: document.getElementById('searchInput'),
    searchBtn: document.getElementById('searchBtn'),
    dashboard: document.getElementById('conceptDashboard'),
    name: document.getElementById('conceptName'),
    domain: document.getElementById('conceptDomain'),
    def: document.getElementById('conceptDef'),
    neighbors: document.getElementById('neighborsList'),
    coords: {
        l: document.getElementById('valL'),
        j: document.getElementById('valJ'),
        p: document.getElementById('valP'),
        w: document.getElementById('valW')
    }
};

// Init
async function init() {
    try {
        const res = await fetch('/api/root');
        const data = await res.json();
        els.status.innerText = `Online: ${data.concepts_loaded} Concepts`;
        els.status.classList.add('online');
        initChart();

        // Load default concept
        loadConcept('Love');
    } catch (e) {
        els.status.innerText = "System Offline";
        console.error(e);
    }
}

function initChart() {
    const ctx = document.getElementById('radarChart').getContext('2d');
    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Love', 'Justice', 'Wisdom', 'Power'], // Order matters for visual shape
            datasets: [{
                label: 'Soul Signature',
                data: [0, 0, 0, 0],
                backgroundColor: 'rgba(0, 204, 255, 0.2)',
                borderColor: '#00ccff',
                pointBackgroundColor: ['#ff0055', '#00ccff', '#aa00ff', '#ffaa00'], // Colored corners
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                r: {
                    min: 0,
                    max: 1,
                    ticks: { display: false, stepSize: 0.2 },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                    pointLabels: {
                        font: { size: 14, family: 'Outfit' },
                        color: '#888'
                    }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

async function loadConcept(query) {
    if (!query) return;

    // Normalize query (API handles case, but UI clean)
    query = query.trim();

    try {
        // 1. Get Concept
        const res = await fetch(`/concepts/${query}`);
        if (!res.ok) throw new Error("Concept not found");
        const c = await res.json();

        renderConcept(c);

        // 2. Get Neighbors
        const resN = await fetch(`/neighbors/${query}?n=12`);
        if (resN.ok) {
            const neighbors = await resN.json();
            renderNeighbors(neighbors);
        }

        els.dashboard.classList.remove('hidden');

    } catch (e) {
        alert("Concept not found within the semantic void.");
    }
}

function renderConcept(c) {
    els.name.innerText = c.name;
    els.domain.innerText = c.domain;
    els.def.innerText = c.definition;

    const [l, j, p, w] = c.coordinates;

    // Update Text
    els.coords.l.innerText = l.toFixed(2);
    els.coords.j.innerText = j.toFixed(2);
    els.coords.p.innerText = p.toFixed(2);
    els.coords.w.innerText = w.toFixed(2);

    // Update Chart (L, J, W, P order to match labels)
    radarChart.data.datasets[0].data = [l, j, w, p];
    radarChart.update();
}

function renderNeighbors(list) {
    els.neighbors.innerHTML = '';
    list.forEach(n => {
        const li = document.createElement('li');
        li.className = 'neighbor-tag';
        li.innerText = n.name;
        li.onclick = () => {
            els.input.value = n.name;
            loadConcept(n.name);
        };
        els.neighbors.appendChild(li);
    });
}

// Events
els.searchBtn.onclick = () => loadConcept(els.input.value);
els.input.onkeypress = (e) => {
    if (e.key === 'Enter') loadConcept(els.input.value);
};

// Analysis Logic
const analyzeBtn = document.getElementById('analyzeBtn');
const analyzeText = document.getElementById('analyzeText');
const analysisResult = document.getElementById('analysisResult');

analyzeBtn.onclick = async () => {
    const text = analyzeText.value.trim();
    if (!text) return;

    analyzeBtn.innerText = "Processing...";

    try {
        const res = await fetch('/analyze/text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        if (!res.ok) throw new Error("Analysis failed");

        const data = await res.json();
        // Render Result (Profile)
        const [l, j, p, w] = data.coordinates;
        analysisResult.innerHTML = `
            <div style="margin-top:10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 8px;">
                <strong>Soul Signature:</strong><br>
                <span style="color:var(--color-love)">L: ${l.toFixed(2)}</span> | 
                <span style="color:var(--color-justice)">J: ${j.toFixed(2)}</span> | 
                <span style="color:var(--color-power)">P: ${p.toFixed(2)}</span> | 
                <span style="color:var(--color-wisdom)">W: ${w.toFixed(2)}</span>
            </div>
        `;

        // Update Chart to show this profile
        radarChart.data.datasets[0].data = [l, j, w, p];
        radarChart.update();
        els.name.innerText = "Text Analysis";
        els.def.innerText = `"${text}"`;
        els.domain.innerText = "Composite";

    } catch (e) {
        analysisResult.innerText = "Error analyzing text.";
        console.error(e);
    } finally {
        analyzeBtn.innerText = "ANALYZE";
    }
};

init();
