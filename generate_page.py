import os, re, json, glob

# --- Parsování balíčků ---
def parse_package(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    name_match = re.search(r'name\s+[\'"]([^\'"]+)[\'"]', content)
    desc_match = re.search(r'desc\s+[\'"]([^\'"]+)[\'"]', content)
    version_match = re.search(r'version\s+[\'"]([^\'"]+)[\'"]', content)

    version_str = "unknown"
    if version_match:
        version_str = version_match.group(1)
    else:
        url_match = re.search(r'url\s+[\'"]([^\'"]+)[\'"]', content)
        if url_match:
            ver_search = re.search(r'-(\d+\.\d+\.\d+[a-zA-Z0-9\-]*)', url_match.group(1))
            if ver_search:
                version_str = ver_search.group(1)

    file_ext = "unknown"
    url_match = re.search(r'url\s+[\'"]([^\'"]+)[\'"]', content)
    if url_match:
        ext_search = re.search(r'(\.[a-zA-Z0-9]+)(?:[\'"]|$)', url_match.group(1).split('?')[0])
        if ext_search:
            file_ext = ext_search.group(1)

    shas = {}
    multi_sha = re.search(r'sha256\s+arm:\s*[\'"]([^\'"]+)[\'"],\s*intel:\s*[\'"]([^\'"]+)[\'"]', content)
    if multi_sha:
        shas['Apple Silicon (arm64)'] = multi_sha.group(1)
        shas['Intel (x86_64)'] = multi_sha.group(2)
    else:
        single_sha = re.search(r'sha256\s+[\'"]([^\'"]+)[\'"]', content)
        if single_sha:
            shas['Universal'] = single_sha.group(1)

    deps = []
    for line in content.split('\n'):
        if line.strip().startswith('depends_on'):
            deps.append(line.replace('depends_on', '').strip())

    caveats = None
    caveats_match = re.search(r'caveats\s+do\s*(.*?)\s*end', content, re.DOTALL | re.IGNORECASE)
    if caveats_match:
        caveats = caveats_match.group(1).strip()
    else:
        caveats_eos = re.search(r'caveats\s+<<~EOS\s*(.*?)\s*EOS', content, re.DOTALL | re.IGNORECASE)
        if caveats_eos:
            caveats = caveats_eos.group(1).strip()

    pkg_id = os.path.basename(filepath).replace('.rb', '')
    return {
        "id": pkg_id,
        "name": name_match.group(1) if name_match else pkg_id,
        "description": desc_match.group(1) if desc_match else "macOS package",
        "version": version_str,
        "file_ext": file_ext,
        "shas": shas,
        "deps": deps,
        "caveats": caveats,
        "install_cmd": f"brew install --cask toobab/tap/{pkg_id}" if "Casks" in filepath else f"brew install toobab/tap/{pkg_id}"
    }

packages = [parse_package(f) for f in glob.glob("Casks/*.rb") + glob.glob("Formula/*.rb")]

packages_html = ""
for p in packages:
    details_html = f"<ul style='margin-bottom: 0;'>"
    details_html += f"<li><strong>Format:</strong> <code>{p['file_ext']}</code></li>"
    if p['shas']:
        details_html += "<li><strong>Hashes (SHA256):</strong><ul style='margin-top: 0.25rem;'>"
        for arch, sha in p['shas'].items():
            details_html += f"<li>{arch}: <code style='display:inline; padding: 0.2rem; margin: 0;'>{sha}</code></li>"
        details_html += "</ul></li>"
    if p['deps']:
        details_html += f"<li><strong>Dependencies:</strong> <code>{', '.join(p['deps'])}</code></li>"
    details_html += "</ul>"

    caveats_html = ""
    if p['caveats']:
        caveats_html = f"""
        <details class="caveats-box">
            <summary><strong>Caveats & Instructions</strong></summary>
            <pre>{p['caveats']}</pre>
        </details>
        """

    packages_html += f"""
    <article class="package">
        <div class="pkg-header">
            <h3 class="pkg-name">{p['name']}</h3>
            <span class="pkg-version">v{p['version']}</span>
        </div>
        <p>{p['description']}</p>
        <strong>Install:</strong>
        <code>{p['install_cmd']}</code>
        <details class="details-accordion">
            <summary>Package Details & Metadata</summary>
            <div class="details-content">
                {details_html}
                {caveats_html}
            </div>
        </details>
    </article>
    """

# --- Zpracování statistik pro JS ---
clones_history = {}
if os.path.exists('stats/clones.json'):
    with open('stats/clones.json', 'r') as f:
        clones_history = json.load(f)

# Převedeme historii na list slovníků pro snadnou manipulaci v JavaScriptu
history_list = [{"date": d, "count": clones_history[d]["count"]} for d in sorted(clones_history.keys())]

json_ld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        {"@type": "SoftwareApplication", "name": p["name"], "softwareVersion": p["version"], "description": p["description"], "applicationCategory": "DeveloperApplication", "operatingSystem": "macOS"} for p in packages
    ]
}

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOOBAB.net Homebrew Tap</title>
    <meta name="description" content="Custom Homebrew tap for macOS applications.">

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script async defer src="https://buttons.github.io/buttons.js"></script>

    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; }}
        .header-container {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }}
        h1 {{ margin: 0; }}
        .gh-buttons {{ display: flex; gap: 10px; }}

        /* NPM.js styl grafu a statistik */
        .npm-stats-wrapper {{ margin: 2rem 0; }}
        .npm-stats-container {{ display: flex; align-items: flex-end; border-bottom: 1px solid #eaeaea; padding-bottom: 0; }}
        .npm-stats-text {{ flex: 0 0 auto; padding-right: 2rem; padding-bottom: 0.5rem; }}
        .npm-stats-title {{ font-size: 0.85rem; color: #57606a; font-weight: 600; margin: 0 0 0.5rem 0; display: flex; align-items: center; gap: 0.5rem; }}
        .npm-stats-number {{ font-size: 2.5rem; font-weight: 600; line-height: 1; color: #24292f; margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
        .npm-chart-wrapper {{ flex: 1 1 auto; height: 70px; position: relative; }}

        /* Tlačítka filtru */
        .range-selectors {{ display: flex; gap: 1rem; font-size: 0.85rem; margin-top: 0.8rem; font-weight: 500; }}
        .range-btn {{ cursor: pointer; color: #57606a; border: none; background: none; padding: 0; border-bottom: 2px solid transparent; transition: all 0.2s; }}
        .range-btn:hover {{ color: #24292f; }}
        .range-btn.active {{ color: #24292f; border-bottom-color: #8956ff; }}

        .search-box {{ width: 100%; padding: 0.8rem; margin: 2rem 0 1.5rem 0; border: 1px solid #d0d7de; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }}
        .package {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
        .pkg-header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
        .pkg-name {{ font-size: 1.25rem; font-weight: bold; margin: 0; }}
        .pkg-version {{ background: #0969da; color: white; padding: 0.2em 0.6em; border-radius: 2em; font-size: 0.85em; font-weight: bold; }}
        code {{ background: #eff1f3; padding: 0.5rem; border-radius: 4px; display: block; margin-top: 1rem; font-family: monospace; font-size: 0.95em; word-break: break-all; }}

        .details-accordion {{ margin-top: 1.25rem; border-top: 1px dashed #d0d7de; padding-top: 0.75rem; }}
        .details-accordion > summary {{ cursor: pointer; color: #0969da; font-weight: 600; list-style-type: none; }}
        .details-accordion > summary::-webkit-details-marker {{ display: none; }}
        .details-accordion > summary::before {{ content: '▶ '; font-size: 0.8em; color: #57606a; }}
        .details-accordion[open] > summary::before {{ content: '▼ '; }}
        .details-content {{ margin-top: 0.75rem; font-size: 0.9em; color: #57606a; }}
        .caveats-box {{ margin-top: 1rem; background: #fff8c5; border: 1px solid #e1b400; border-radius: 6px; padding: 1rem; color: #24292f; }}
        .caveats-box summary {{ cursor: pointer; font-weight: 600; }}
        .caveats-box pre {{ margin-top: 0.5rem; margin-bottom: 0; white-space: pre-wrap; font-family: monospace; font-size: 0.9em; }}
    </style>

    <script type="application/ld+json">
    {json.dumps(json_ld, indent=4)}
    </script>
</head>
<body>
    <main>
        <div class="header-container">
            <h1>TOOBAB.net Homebrew Tap</h1>
            <div class="gh-buttons">
                <a class="github-button" href="https://github.com/toobab/homebrew-tap" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star toobab/homebrew-tap on GitHub">Star</a>
                <a class="github-button" href="https://github.com/toobab/homebrew-tap/subscription" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch toobab/homebrew-tap on GitHub">Watch</a>
            </div>
        </div>

        <p>This is a custom Homebrew tap for macOS packages. To add this tap, run:</p>
        <code>brew tap toobab/tap</code>

        <!-- NPM.js styl statistik -->
        <div class="npm-stats-wrapper">
            <div class="npm-stats-container">
                <div class="npm-stats-text">
                    <h3 class="npm-stats-title">
                        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-8.5C1 2.784 1.784 2 2.75 2h10.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 13.25 14ZM2.75 3.5c-.138 0-.25.112-.25.25v8.5c0 .138.112.25.25.25h10.5c.138 0 .25-.112.25-.25v-8.5c0-.138-.112-.25-.25-.25Zm8 4a.75.75 0 0 1 .75.75v2a.75.75 0 0 1-1.5 0v-2a.75.75 0 0 1 .75-.75Zm-5 1.5a.75.75 0 0 1 .75.75v.5a.75.75 0 0 1-1.5 0v-.5a.75.75 0 0 1 .75-.75Zm2.5-2.5a.75.75 0 0 1 .75.75v3a.75.75 0 0 1-1.5 0v-3a.75.75 0 0 1 .75-.75Z"></path></svg>
                        <span id="statTitle">Downloads</span>
                    </h3>
                    <div class="npm-stats-number" id="statNumber">0</div>
                </div>
                <div class="npm-chart-wrapper">
                    <canvas id="cloneChart"></canvas>
                </div>
            </div>

            <div class="range-selectors">
                <button class="range-btn active" data-days="all">All time</button>
                <button class="range-btn" data-days="365">1 Year</button>
                <button class="range-btn" data-days="30">1 Month</button>
                <button class="range-btn" data-days="7">1 Week</button>
                <button class="range-btn" data-days="1">1 Day</button>
            </div>
        </div>

        <h2>Available Packages</h2>
        <input type="text" id="searchInput" class="search-box" placeholder="Search for a package (e.g., nuvio)...">

        <div id="packageList">
            {packages_html}
        </div>
    </main>

    <script>
        // Filtrace balíčků
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.package').forEach(pkg => {{
                const name = pkg.querySelector('.pkg-name').textContent.toLowerCase();
                pkg.style.display = name.includes(term) ? 'block' : 'none';
            }});
        }});

        // Data statistik vložená z Pythonu
        const historyData = {json.dumps(history_list)};
        let chartInstance = null;
        const ctx = document.getElementById('cloneChart').getContext('2d');

        function renderStats(days, titleSuffix) {{
            let filtered = historyData;

            if (days !== 'all' && historyData.length > 0) {{
                const targetDate = new Date();
                targetDate.setDate(targetDate.getDate() - parseInt(days));
                filtered = historyData.filter(d => new Date(d.date) >= targetDate);
            }}

            const total = filtered.reduce((sum, item) => sum + item.count, 0);

            // Formatování čísla s mezerami po tisících
            document.getElementById('statNumber').innerText = total.toLocaleString('cs-CZ').replace(/,/g, ' ');

            // Oprava sčítání textových řetězců (bez kolize s Python f-stringem)
            document.getElementById('statTitle').innerText = 'Clones ' + (titleSuffix ? '(' + titleSuffix + ')' : '');

            const labels = filtered.map(d => d.date);
            const data = filtered.map(d => d.count);

            if (chartInstance) chartInstance.destroy();

            chartInstance = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: labels,
                    datasets: [{{
                        data: data,
                        borderColor: '#8956ff',
                        backgroundColor: 'rgba(137, 86, 255, 0.15)',
                        borderWidth: 2.5,
                        fill: true,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            mode: 'index',
                            intersect: false,
                            displayColors: false,
                            callbacks: {{ label: (ctx) => ctx.raw + ' clones' }}
                        }}
                    }},
                    scales: {{
                        x: {{ display: false }},
                        y: {{ display: false, min: 0 }}
                    }},
                    layout: {{ padding: 0 }},
                    interaction: {{ mode: 'nearest', axis: 'x', intersect: false }}
                }}
            }});
        }}

        // Inicializace s All-time
        renderStats('all', '');

        // Interakce tlačítek
        document.querySelectorAll('.range-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');

                const days = e.target.getAttribute('data-days');
                const title = e.target.innerText;
                renderStats(days, days === 'all' ? '' : title.toLowerCase());
            }});
        }});
    </script>
</body>
</html>"""

os.makedirs('public', exist_ok=True)
with open('public/index.html', 'w') as f:
    f.write(html_content)
