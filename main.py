import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

KAGGLE_URL = os.getenv("KAGGLE_URL", "")

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rectuna — JSON Extractor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        surface: {
                            900: '#0a0a0f',
                            800: '#12121a',
                            700: '#1a1a24',
                            600: '#252533',
                        },
                        accent: {
                            DEFAULT: '#6366f1',
                            hover: '#818cf8',
                        },
                    },
                },
            },
        };
    </script>
    <style>
        * { box-sizing: border-box; }
        body {
            background: #0a0a0f;
            background-image:
                radial-gradient(ellipse 80% 60% at 50% -20%, rgba(99, 102, 241, 0.15), transparent),
                radial-gradient(ellipse 60% 50% at 80% 100%, rgba(168, 85, 247, 0.08), transparent);
            min-height: 100vh;
        }
        .code-scroll::-webkit-scrollbar { width: 8px; height: 8px; }
        .code-scroll::-webkit-scrollbar-track { background: transparent; }
        .code-scroll::-webkit-scrollbar-thumb { background: #252533; border-radius: 4px; }
        .code-scroll::-webkit-scrollbar-thumb:hover { background: #3a3a4a; }
        textarea { resize: vertical; }
        .spinner {
            border: 2px solid rgba(255,255,255,0.1);
            border-top-color: #818cf8;
            border-radius: 50%;
            width: 16px;
            height: 16px;
            animation: spin 0.7s linear infinite;
            display: inline-block;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body class="font-sans text-gray-100 antialiased">
    <div class="max-w-5xl mx-auto px-6 py-10 md:py-16">

        <!-- Header -->
        <header class="mb-10 md:mb-14">
            <div class="flex items-center gap-3 mb-3">
                <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                </div>
                <h1 class="text-2xl md:text-3xl font-bold tracking-tight">Rectuna</h1>
            </div>
            <p class="text-gray-400 text-sm md:text-base max-w-xl">
                Turn unstructured text into structured JSON. Fine-tuned Qwen2.5-1.5B across four extraction schemas.
            </p>
        </header>

        <!-- Main grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

            <!-- Left: Input -->
            <section class="bg-surface-800 border border-surface-600 rounded-2xl p-6">
                <div class="flex items-center justify-between mb-5">
                    <h2 class="text-sm font-semibold text-gray-300 uppercase tracking-wider">Input</h2>
                    <span class="text-xs text-gray-500 font-mono" id="charCount">0 chars</span>
                </div>

                <!-- Mode selector -->
                <label class="block text-xs font-medium text-gray-400 mb-2 uppercase tracking-wider">Schema</label>
                <div class="grid grid-cols-4 gap-2 mb-5" id="modeGroup">
                    <button type="button" data-mode="invoice" class="mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-indigo-500 text-white transition-all duration-150">Invoice</button>
                    <button type="button" data-mode="product" class="mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-surface-700 text-gray-300 hover:bg-surface-600 transition-all duration-150">Product</button>
                    <button type="button" data-mode="receipt" class="mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-surface-700 text-gray-300 hover:bg-surface-600 transition-all duration-150">Receipt</button>
                    <button type="button" data-mode="contact" class="mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-surface-700 text-gray-300 hover:bg-surface-600 transition-all duration-150">Contact</button>
                </div>

                <!-- Text input -->
                <label class="block text-xs font-medium text-gray-400 mb-2 uppercase tracking-wider">Paste your text</label>
                <textarea id="inputText" rows="12"
                    class="w-full bg-surface-900 border border-surface-600 rounded-lg px-4 py-3 text-sm font-mono text-gray-200 placeholder-gray-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all duration-150 code-scroll"
                    placeholder="Invoice #INV-9001&#10;Vendor: Delta Supplies Co.&#10;Date: 2024-07-15&#10;&#10;Items:&#10;- 3x Widget @ $25.00&#10;- 2x Gizmo @ $75.00&#10;&#10;Total: $225.00"></textarea>

                <!-- Submit button -->
                <button id="submitBtn"
                    class="w-full mt-5 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-medium py-3 rounded-lg transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="btnText">Extract JSON</span>
                    <span id="btnSpinner" class="spinner hidden"></span>
                </button>

                <!-- Sample fill -->
                <button id="sampleBtn" class="w-full mt-2 text-xs text-gray-500 hover:text-gray-300 transition-colors py-2">
                    Load a sample
                </button>
            </section>

            <!-- Right: Output -->
            <section class="bg-surface-800 border border-surface-600 rounded-2xl p-6 flex flex-col">
                <div class="flex items-center justify-between mb-5">
                    <h2 class="text-sm font-semibold text-gray-300 uppercase tracking-wider">Output</h2>
                    <button id="copyBtn" class="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1.5 opacity-0 pointer-events-none" disabled>
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                        </svg>
                        Copy
                    </button>
                </div>

                <div id="outputWrap" class="flex-1 bg-surface-900 border border-surface-600 rounded-lg p-4 font-mono text-sm overflow-auto code-scroll min-h-[400px]">
                    <div id="emptyState" class="h-full flex flex-col items-center justify-center text-gray-600 text-center">
                        <svg class="w-12 h-12 mb-3 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
                        </svg>
                        <p class="text-xs">Extracted JSON will appear here</p>
                    </div>
                    <pre id="outputPre" class="hidden text-gray-200 whitespace-pre-wrap break-words"></pre>
                </div>

                <div id="metaRow" class="hidden mt-3 flex items-center justify-between text-xs text-gray-500 font-mono">
                    <span id="metaLatency"></span>
                    <span id="metaStatus"></span>
                </div>
            </section>

        </div>

        <!-- Footer -->
        <footer class="mt-10 md:mt-14 pt-6 border-t border-surface-700 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-gray-600">
            <p>Rectuna — a fine-tuned Qwen2.5-1.5B LoRA adapter</p>
            <div class="flex items-center gap-4">
                <a href="https://huggingface.co/heydothan/rectuna-qwen2.5-1.5b" target="_blank" rel="noopener" class="hover:text-gray-400 transition-colors">HuggingFace</a>
                <a href="https://github.com/heydothan/rectuna" target="_blank" rel="noopener" class="hover:text-gray-400 transition-colors">GitHub</a>
            </div>
        </footer>

    </div>

    <script>
        const modeBtns = document.querySelectorAll('.mode-btn');
        const inputText = document.getElementById('inputText');
        const submitBtn = document.getElementById('submitBtn');
        const btnText = document.getElementById('btnText');
        const btnSpinner = document.getElementById('btnSpinner');
        const outputPre = document.getElementById('outputPre');
        const emptyState = document.getElementById('emptyState');
        const copyBtn = document.getElementById('copyBtn');
        const metaRow = document.getElementById('metaRow');
        const metaLatency = document.getElementById('metaLatency');
        const metaStatus = document.getElementById('metaStatus');
        const charCount = document.getElementById('charCount');
        const sampleBtn = document.getElementById('sampleBtn');

        let currentMode = 'invoice';

        const SAMPLES = {
            invoice: `Invoice #INV-9001
Vendor: Delta Supplies Co.
Date: 2024-07-15

Items:
- 3x Widget @ $25.00
- 2x Gizmo @ $75.00

Total: $225.00`,
            product: `Product: Sony WH-1000XM5
Brand: Sony
Price: $398.00
Category: Audio
Rating: 4.7 stars`,
            receipt: `Target
2024-06-15

Bread $3.50
Milk $4.20
Eggs $5.00

TOTAL: $12.70`,
            contact: `Michael Chen
VP of Engineering
DataFlow Systems
michael.chen@dataflow.com
+1 (415) 555-0199
San Francisco, CA`,
        };

        // Mode switching
        modeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                if (btn.dataset.mode === currentMode) return;
                currentMode = btn.dataset.mode;
                modeBtns.forEach(b => {
                    if (b === btn) {
                        b.className = 'mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-indigo-500 text-white transition-all duration-150';
                    } else {
                        b.className = 'mode-btn px-3 py-2.5 text-sm font-medium rounded-lg bg-surface-700 text-gray-300 hover:bg-surface-600 transition-all duration-150';
                    }
                });

                // Clear input and output on mode switch
                inputText.value = '';
                charCount.textContent = '0 chars';
                outputPre.textContent = '';
                outputPre.classList.add('hidden');
                emptyState.classList.remove('hidden');
                metaRow.classList.add('hidden');
                copyBtn.classList.add('opacity-0', 'pointer-events-none');
                copyBtn.disabled = true;
            });
        });

        // Char count
        inputText.addEventListener('input', () => {
            charCount.textContent = inputText.value.length + ' chars';
        });

        // Sample
        sampleBtn.addEventListener('click', () => {
            inputText.value = SAMPLES[currentMode];
            charCount.textContent = inputText.value.length + ' chars';
            inputText.focus();
        });

        // Submit
        submitBtn.addEventListener('click', async () => {
            const text = inputText.value.trim();
            if (!text) {
                inputText.focus();
                return;
            }

            submitBtn.disabled = true;
            btnText.textContent = 'Extracting...';
            btnSpinner.classList.remove('hidden');
            emptyState.classList.add('hidden');
            outputPre.classList.remove('hidden');
            outputPre.textContent = '';
            metaRow.classList.add('hidden');
            copyBtn.classList.add('opacity-0', 'pointer-events-none');
            copyBtn.disabled = true;

            const start = performance.now();

            try {
                const formData = new FormData();
                formData.append('mode', currentMode);
                formData.append('text', text);

                const resp = await fetch('/api/extract', {
                    method: 'POST',
                    body: formData,
                });

                if (!resp.ok) {
                    throw new Error('Server returned ' + resp.status);
                }

                const data = await resp.json();
                const elapsed = ((performance.now() - start) / 1000).toFixed(2);

                if (data.valid) {
                    outputPre.textContent = JSON.stringify(data.output, null, 2);
                    metaStatus.textContent = '✓ valid JSON';
                    metaStatus.className = 'text-emerald-400';
                } else {
                    outputPre.textContent = data.output;
                    metaStatus.textContent = '⚠ raw output (invalid JSON)';
                    metaStatus.className = 'text-amber-400';
                }

                metaLatency.textContent = elapsed + 's';
                metaRow.classList.remove('hidden');
                copyBtn.classList.remove('opacity-0', 'pointer-events-none');
                copyBtn.disabled = false;
            } catch (err) {
                outputPre.textContent = 'Error: ' + err.message;
                metaStatus.textContent = '✗ request failed';
                metaStatus.className = 'text-red-400';
                metaRow.classList.remove('hidden');
            } finally {
                submitBtn.disabled = false;
                btnText.textContent = 'Extract JSON';
                btnSpinner.classList.add('hidden');
            }
        });

        // Copy
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(outputPre.textContent);
                const original = copyBtn.innerHTML;
                copyBtn.innerHTML = '✓ Copied';
                setTimeout(() => { copyBtn.innerHTML = original; }, 1500);
            } catch (e) {
                /* noop */
            }
        });

        // Cmd/Ctrl + Enter to submit
        inputText.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
                submitBtn.click();
            }
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.post("/api/extract")
async def extract(mode: str = Form(...), text: str = Form(...)):
    if not KAGGLE_URL:
        return JSONResponse(
            status_code=500,
            content={"valid": False, "output": "KAGGLE_URL not configured on server"},
        )

    try:
        resp = requests.post(
            f"{KAGGLE_URL}/extract",
            data={"mode": mode, "text": text},
            headers={"ngrok-skip-browser-warning": "true"},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        return JSONResponse(
            status_code=504,
            content={"valid": False, "output": "Model server timed out"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={"valid": False, "output": f"Upstream error: {str(e)[:200]}"},
        )