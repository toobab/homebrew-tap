import os, re, json, glob
from datetime import datetime, timedelta

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

    pkg_id = os.path.basename(filepath).replace('.rb', '')
    return {
        "id": pkg_id,
        "name": name_match.group(1) if name_match else pkg_id,
        "description": desc_match.group(1) if desc_match else "macOS package",
        "version": version_str,
        "install_cmd": f"brew install --cask toobab/tap/{pkg_id}" if "Casks" in filepath else f"brew install toobab/tap/{pkg_id}"
    }

packages = [parse_package(f) for f in glob.glob("Casks/*.rb") + glob.glob("Formula/*.rb")]

# --- Zpracování statistik z gitu ---
clones_history = {}
if os.path.exists('stats/clones.json'):
    with open('stats/clones.json', 'r') as f:
        clones_history = json.load(f)

# Výpočet základních metrik
all_time_clones = sum(day['count'] for day in clones_history.values())

# Příprava dat pro Chart.js (posledních 30 dní v historii)
sorted_dates = sorted(clones_history.keys())[-30:]
chart_labels = sorted_dates
chart_data = [clones_history[date]['count'] for date in sorted_dates]

# --- Generování HTML ---
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
    <meta property="og:title" content="TOOBAB.net Homebrew Tap">
    <meta property="og:description" content="Automated Homebrew repository for custom macOS packages.">

    <!-- Chart.js pro grafy -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- GitHub Buttons -->
    <script async defer src="https://buttons.github.io/buttons.js"></script>

    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; }}
        .header-container {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }}
        h1 {{ margin: 0; }}
        .gh-buttons {{ display: flex; gap: 10px; }}
        .stats-card {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 1.5rem; margin-bottom: 2rem; text-align: center; }}
        .stats-number {{ font-size: 2rem; font-weight: bold; color: #0969da; margin: 0.5rem 0; }}
        .chart-container {{ position: relative; height: 200px; width: 100%; margin-top: 1rem; }}
        .search-box {{ width: 100%; padding: 0.8rem; margin: 1.5rem 0; border: 1px solid #d0d7de; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }}
        .package {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
        .pkg-header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
        .pkg-name {{ font-size: 1.25rem; font-weight: bold; margin: 0; }}
        .pkg-version {{ background: #0969da; color: white; padding: 0.2em 0.6em; border-radius: 2em; font-size: 0.85em; font-weight: bold; }}
        code {{ background: #eff1f3; padding: 0.5rem; border-radius: 4px; display: block; margin-top: 1rem; font-family: monospace; font-size: 0.95em; }}
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
                <!-- Tlačítka pro Stars a Watchers -->
                <a class="github-button" href="https://github.com/toobab/homebrew-tap" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star toobab/homebrew-tap on GitHub">Star</a>
                <a class="github-button" href="https://github.com/toobab/homebrew-tap/subscription" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch toobab/homebrew-tap on GitHub">Watch</a>
            </div>
        </div>

        <p>This is a custom Homebrew tap for macOS packages. To add this tap, run:</p>
        <code>brew tap toobab/tap</code>

        <!-- Sekce se statistikami -->
        <div class="stats-card">
            <h3>Repository Clones (All-time)</h3>
            <div class="stats-number">{all_time_clones}</div>
            <p style="font-size: 0.85em; color: #57606a;">Number of times this tap was installed or updated by users.</p>
            <div class="chart-container">
                <canvas id="cloneChart"></canvas>
            </div>
        </div>

        <h2>Available Packages</h2>

        <input type="text" id="searchInput" class="search-box" placeholder="Search for a package (e.g., nuvio)...">

        <div id="packageList">
        {''.join(f'''
            <article class="package">
                <div class="pkg-header">
                    <h3 class="pkg-name">{p['name']}</h3>
                    <span class="pkg-version">v{p['version']}</span>
                </div>
                <p>{p['description']}</p>
                <strong>Install:</strong>
                <code>{p['install_cmd']}</code>
            </article>
        ''' for p in packages)}
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

        // Vykreslení grafu klonování přes Chart.js
        const ctx = document.getElementById('cloneChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(chart_labels)},
                datasets: [{{
                    label: 'Daily Clones',
                    data: {json.dumps(chart_data)},
                    backgroundColor: '#0969da',
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ y: {{ beginAtZero: true, ticks: {{ precision: 0 }} }} }}
            }}
        }});
    </script>
</body>
</html>"""

os.makedirs('public', exist_ok=True)
with open('public/index.html', 'w') as f:
    f.write(html_content)
