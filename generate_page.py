import os, re, json, glob, html

REPO = os.environ.get("GITHUB_REPOSITORY", "toobab/homebrew-tap")
TAP = REPO.replace("homebrew-", "")
OWNER, REPO_NAME = REPO.split("/")
BASE = f"https://{OWNER}.github.io/{REPO_NAME}/"
SITE_NAME = f"{TAP} - Homebrew tap for macOS apps"

# --- Parsování balíčků ---
def parse_package(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    name_match = re.search(r'name\s+[\'"]([^\'"]+)[\'"]', content)
    desc_match = re.search(r'desc\s+[\'"]([^\'"]+)[\'"]', content)
    version_match = re.search(r'version\s+[\'"]([^\'"]+)[\'"]', content)
    homepage_match = re.search(r'homepage\s+[\'"]([^\'"]+)[\'"]', content)

    version_str = "unknown"
    if version_match:
        version_str = version_match.group(1)
    else:
        url_match = re.search(r'url\s+[\'"]([^\'"]+)[\'"]', content)
        if url_match:
            ver_search = (re.search(r'/v?(\d+\.\d+\.\d+[a-zA-Z0-9.\-]*)/', url_match.group(1))
                          or re.search(r'-(\d+\.\d+\.\d+[a-zA-Z0-9\-]*)', url_match.group(1)))
            if ver_search:
                version_str = ver_search.group(1)

    file_ext = "unknown"
    url_match = re.search(r'url\s+[\'"]([^\'"]+)[\'"]', content)
    if url_match:
        url_str = url_match.group(1)
        ext_search = re.search(r'(\.[a-zA-Z0-9]+)(?:[\'"]|$)', url_str.split('?')[0])
        if ext_search:
            file_ext = ext_search.group(1)

        repo_match = re.search(r'https?://github\.com/([^/]+/[^/]+)', url_str)
        if repo_match:
            github_repo_url = f"https://github.com/{repo_match.group(1)}"
        else:
            github_repo_url = None
    else:
        github_repo_url = None

    shas = {}
    multi_sha = re.search(r'sha256\s+arm:\s*[\'"]([^\'"]+)[\'"],\s*intel:\s*[\'"]([^\'"]+)[\'"]', content)
    if multi_sha:
        shas['Apple Silicon (arm64)'] = multi_sha.group(1)
        shas['Intel (x86_64)'] = multi_sha.group(2)
    else:
        top_level = re.findall(r'^ {2,4}sha256\s+[\'"]([0-9a-f]{64})[\'"]', content, re.MULTILINE)
        if len(top_level) == 2 and 'Hardware::CPU.arm?' in content:
            shas['Apple Silicon (arm64)'] = top_level[0]
            shas['Intel (x86_64)'] = top_level[1]
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

    repo_comment = re.search(r'^#\s*repository:\s*(\S+)', content, re.MULTILINE | re.IGNORECASE)
    if repo_comment:
        github_repo_url = repo_comment.group(1)

    pkg_id = os.path.basename(filepath).replace('.rb', '')
    return {
        "id": pkg_id,
        "name": name_match.group(1) if name_match else pkg_id,
        "description": desc_match.group(1) if desc_match else "macOS package",
        "version": version_str,
        "homepage": homepage_match.group(1) if homepage_match else None,
        "github_repo": github_repo_url,
        "file_ext": file_ext,
        "shas": shas,
        "deps": deps,
        "caveats": caveats,
        "slug": os.path.basename(filepath)[:-3].replace("@", "-"),
        "kind": "cask" if "Casks" in filepath else "formula",
        "install_cmd": f"brew install --cask {TAP}/{pkg_id}" if "Casks" in filepath else f"brew install {TAP}/{pkg_id}"
    }

packages = [parse_package(f) for f in sorted(glob.glob("Casks/*.rb") + glob.glob("Formula/*.rb"))]
esc = html.escape
total_packages = len(packages)

packages_html = ""
for p in packages:
    details_html = f"<ul style='margin-bottom: 0;'>"

    if p['homepage']:
        details_html += f"<li><strong>Official Website:</strong> <a href='{esc(p['homepage'])}' target='_blank' rel='noopener'>{esc(p['homepage'])}</a></li>"
    if p['github_repo'] and p['github_repo'] != p['homepage']:
        details_html += f"<li><strong>Repository:</strong> <a href='{esc(p['github_repo'])}' target='_blank' rel='noopener'>{esc(p['github_repo'])}</a></li>"

    details_html += f"<li><strong>Format:</strong> <code style='display:inline; padding: 0.2rem; margin: 0;'>{esc(p['file_ext'])}</code></li>"

    if p['shas']:
        details_html += "<li><strong>Hashes (SHA256):</strong><ul style='margin-top: 0.25rem;'>"
        for arch, sha in p['shas'].items():
            details_html += f"<li>{esc(arch)}: <code style='display:inline; padding: 0.2rem; margin: 0;'>{esc(sha)}</code></li>"
        details_html += "</ul></li>"

    if p['deps']:
        details_html += f"<li><strong>Dependencies:</strong> <code>{esc(', '.join(p['deps']))}</code></li>"
    details_html += "</ul>"

    caveats_html = ""
    if p['caveats']:
        caveats_html = f"""
        <details class="caveats-box">
            <summary><strong>Caveats & Instructions</strong></summary>
            <pre>{esc(p['caveats'])}</pre>
        </details>
        """

    p['_details'], p['_caveats'] = details_html, caveats_html

    packages_html += f"""
    <article class="package" id="{p['slug']}">
        <div class="pkg-header">
            <h3 class="pkg-name"><a href="{p['slug']}/">{esc(p['name'])}</a></h3>
            <span class="pkg-version">v{esc(p['version'])}</span>
        </div>
        <p>{esc(p['description'])}</p>
        <strong>Install:</strong>
        <code>{esc(p['install_cmd'])}</code>
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

history_list = [{"date": d, "count": clones_history[d]["count"]} for d in sorted(clones_history.keys())]

names = [p["name"] for p in packages]
PAGE_TITLE = f"Homebrew Tap for macOS apps: {', '.join(names[:4])} | {TAP}"
PAGE_DESC = (f"Homebrew tap {TAP} with {total_packages} macOS packages ({', '.join(names)}). "
             f"Run brew tap {TAP}, then brew install. Versions and SHA256 hashes are updated automatically.")


def software_ld(p):
    same_as = [u for u in (p["homepage"], p["github_repo"]) if u]
    return {
        "@type": "SoftwareApplication", "@id": f"{BASE}{p['slug']}/#app", "name": p["name"],
        "url": f"{BASE}{p['slug']}/", "softwareVersion": p["version"], "description": p["description"],
        "applicationCategory": "DeveloperApplication", "operatingSystem": "macOS",
        "installUrl": f"{BASE}{p['slug']}/", "sameAs": same_as, "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }


json_ld = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": BASE + "#website", "name": SITE_NAME, "url": BASE,
         "description": PAGE_DESC, "inLanguage": "en"},
        {"@type": "CollectionPage", "@id": BASE + "#page", "url": BASE, "name": PAGE_TITLE,
         "description": PAGE_DESC, "isPartOf": {"@id": BASE + "#website"},
         "mainEntity": {"@type": "ItemList", "numberOfItems": total_packages, "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "item": software_ld(p)} for i, p in enumerate(packages)]}},
    ],
}

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8D%BA%3C/text%3E%3C/svg%3E"


def seo_head(title, desc, canonical, og_type="website"):
    return f"""<title>{esc(title)}</title>
    <meta name="description" content="{esc(desc, quote=True)}">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" href="{FAVICON}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="{esc(SITE_NAME, quote=True)}">
    <meta property="og:title" content="{esc(title, quote=True)}">
    <meta property="og:description" content="{esc(desc, quote=True)}">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{esc(title, quote=True)}">
    <meta name="twitter:description" content="{esc(desc, quote=True)}">"""


def ld_script(data):
    return '<script type="application/ld+json">' + json.dumps(data, indent=2).replace("</", "<\\/") + '</script>'


html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {seo_head(PAGE_TITLE, PAGE_DESC, BASE)}

    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
    <script async defer src="https://buttons.github.io/buttons.js"></script>

    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; }}
        .header-container {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }}
        h1 {{ margin: 0; }}
        .header-right {{ display: flex; align-items: center; gap: 15px; }}
        .package-badge {{ background: #eff1f3; padding: 0.3rem 0.8rem; border-radius: 2em; font-size: 0.85rem; font-weight: 600; color: #57606a; border: 1px solid #d0d7de; }}
        .gh-buttons {{ display: flex; gap: 10px; align-items: center; }}

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
        .range-btn.active {{ color: #24292f; border-bottom-color: #0969da; }}

        .search-box {{ width: 100%; padding: 0.8rem; margin: 2rem 0 1.5rem 0; border: 1px solid #d0d7de; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }}
        .package {{ background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
        .pkg-header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
        .pkg-name a {{ color: inherit; text-decoration: none; }}
        .pkg-name a:hover {{ text-decoration: underline; }}
        .pkg-name {{ font-size: 1.25rem; font-weight: bold; margin: 0; }}
        .pkg-version {{ background: #0969da; color: white; padding: 0.2em 0.6em; border-radius: 2em; font-size: 0.85em; font-weight: bold; }}
        code {{ background: #eff1f3; padding: 0.5rem; border-radius: 4px; display: block; margin-top: 1rem; font-family: monospace; font-size: 0.95em; word-break: break-all; }}

        .details-accordion {{ margin-top: 1.25rem; border-top: 1px dashed #d0d7de; padding-top: 0.75rem; }}
        .details-accordion > summary {{ cursor: pointer; color: #0969da; font-weight: 600; list-style-type: none; }}
        .details-accordion > summary::-webkit-details-marker {{ display: none; }}
        .details-accordion > summary::before {{ content: '▶ '; font-size: 0.8em; color: #57606a; }}
        .details-accordion[open] > summary::before {{ content: '▼ '; }}
        .details-content {{ margin-top: 0.75rem; font-size: 0.9em; color: #57606a; }}
        .caveats-box {{ margin-top: 1rem; background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 1rem; color: #24292f; }}
        .caveats-box summary {{ cursor: pointer; font-weight: 600; }}
        .caveats-box pre {{ margin-top: 0.5rem; margin-bottom: 0; white-space: pre-wrap; font-family: monospace; font-size: 0.9em; }}
    </style>

    {ld_script(json_ld)}
</head>
<body>
    <main>
        <div class="header-container">
            <h1>TOOBAB.net Homebrew Tap</h1>
            <div class="header-right">
                <span class="package-badge">{total_packages} packages</span>
                <div class="gh-buttons">
                    <a class="github-button" href="https://github.com/{REPO}" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star {REPO} on GitHub">Star</a>
                    <a class="github-button" href="https://github.com/{REPO}/subscription" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch {REPO} on GitHub">Watch</a>
                </div>
            </div>
        </div>

        <p>{TAP} is a Homebrew tap with {total_packages} macOS apps and CLI tools ({esc(", ".join(names))}). Versions are checked automatically against upstream releases. To add this tap, run:</p>
        <code>brew tap {TAP}</code>

        <!-- Statistiky v NPM stylu s modrým grafem -->
        <div class="npm-stats-wrapper">
            <div class="npm-stats-container">
                <div class="npm-stats-text">
                    <h3 class="npm-stats-title">
                        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-8.5C1 2.784 1.784 2 2.75 2h10.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 13.25 14ZM2.75 3.5c-.138 0-.25.112-.25.25v8.5c0 .138.112.25.25.25h10.5c.138 0 .25-.112.25-.25v-8.5c0-.138-.112-.25-.25-.25Zm8 4a.75.75 0 0 1 .75.75v2a.75.75 0 0 1-1.5 0v-2a.75.75 0 0 1 .75-.75Zm-5 1.5a.75.75 0 0 1 .75.75v.5a.75.75 0 0 1-1.5 0v-.5a.75.75 0 0 1 .75-.75Zm2.5-2.5a.75.75 0 0 1 .75.75v3a.75.75 0 0 1-1.5 0v-3a.75.75 0 0 1 .75-.75Z"></path></svg>
                        <span id="statTitle">Clones</span>
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
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.package').forEach(pkg => {{
                const name = pkg.querySelector('.pkg-name').textContent.toLowerCase();
                pkg.style.display = name.includes(term) ? 'block' : 'none';
            }});
        }});

        const historyData = {json.dumps(history_list)};
        let chartInstance = null;
        const ctx = document.getElementById('cloneChart').getContext('2d');

        function renderStats(days, titleSuffix) {{
            let filtered = historyData;

            if (days !== 'all' && historyData.length > 0) {{
                filtered = historyData.slice(-Math.max(parseInt(days), 2));
            }}

            const total = filtered.reduce((sum, item) => sum + item.count, 0);

            document.getElementById('statNumber').innerText = total.toLocaleString('en-US');
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
                        borderColor: '#0969da',
                        backgroundColor: 'rgba(9, 105, 218, 0.15)',
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

        renderStats('all', '');

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

# --- Stránky jednotlivých balíčků ---
CSS = re.search(r"<style>(.*?)</style>", html_content, re.S).group(1)
import datetime
TODAY = datetime.date.today().isoformat()


def package_page(p):
    url = f"{BASE}{p['slug']}/"
    cask_flag = "--cask " if p["kind"] == "cask" else ""
    title = f"{p['name']} {p['version']} - brew install {cask_flag}{TAP}/{p['id']}"
    desc = (f"{p['description'].rstrip('.')}. Install {p['name']} {p['version']} on macOS with Homebrew: "
            f"brew install {cask_flag}{TAP}/{p['id']}.")
    ld = {"@context": "https://schema.org", "@graph": [
        software_ld(p),
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": BASE},
            {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]}]}
    steps = (f"brew tap {TAP}\n{p['install_cmd']}\n\n# upgrade / uninstall\n"
             f"brew upgrade {cask_flag}{p['id']}\nbrew uninstall {cask_flag}{p['id']}")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {seo_head(title, desc, url, "article")}
    {ld_script(ld)}
    <style>{CSS}</style>
</head>
<body>
    <main>
        <nav aria-label="Breadcrumb"><a href="../">{esc(SITE_NAME)}</a> &rsaquo; {esc(p['name'])}</nav>
        <div class="header-container"><h1>{esc(p['name'])}</h1><span class="pkg-version">v{esc(p['version'])}</span></div>
        <p>{esc(p['description'])}. Available as a Homebrew {p['kind']} in the {esc(TAP)} tap for macOS.</p>
        <h2>Install with Homebrew</h2>
        <pre><code>{esc(steps)}</code></pre>
        <h2>Details</h2>
        <div class="details-content">{p['_details']}{p['_caveats']}</div>
        <p><a href="../">&larr; All packages in {esc(TAP)}</a></p>
    </main>
</body>
</html>"""


for p in packages:
    os.makedirs(f"public/{p['slug']}", exist_ok=True)
    with open(f"public/{p['slug']}/index.html", "w") as f:
        f.write(package_page(p))

# --- sitemap.xml, robots.txt, llms.txt ---
urls = [BASE] + [f"{BASE}{p['slug']}/" for p in packages]
with open("public/sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n")
    f.write("</urlset>\n")

with open("public/robots.txt", "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

lines = [f"# {TAP}", "", f"> {PAGE_DESC}", "",
         f"Add the tap with `brew tap {TAP}`. Casks install with `brew install --cask {TAP}/<name>`, formulae with `brew install {TAP}/<name>`.", "",
         "## Packages", ""]
for p in packages:
    lines.append(f"- [{p['name']}]({BASE}{p['slug']}/): {p['description']} (v{p['version']}). Install: `{p['install_cmd']}`")
lines += ["", "## Source", "", f"- [GitHub repository](https://github.com/{REPO}): cask and formula definitions, update scripts",
          f"- [Sitemap]({BASE}sitemap.xml)", ""]
with open("public/llms.txt", "w") as f:
    f.write("\n".join(lines))
