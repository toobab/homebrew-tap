import os, re, json, glob

def parse_package(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    name_match = re.search(r'name\s+"([^"]+)"', content)
    desc_match = re.search(r'desc\s+"([^"]+)"', content)
    version_match = re.search(r'version\s+"([^"]+)"', content)

    pkg_id = os.path.basename(filepath).replace('.rb', '')

    return {
        "id": pkg_id,
        "name": name_match.group(1) if name_match else pkg_id,
        "description": desc_match.group(1) if desc_match else "macOS package",
        "version": version_match.group(1) if version_match else "unknown",
        "install_cmd": f"brew install --cask toobab/tap/{pkg_id}" if "Casks" in filepath else f"brew install toobab/tap/{pkg_id}"
    }

packages = [parse_package(f) for f in glob.glob("Casks/*.rb") + glob.glob("Formula/*.rb")]

# JSON-LD pro GEO (Generative Engine Optimization) - AI agenti toto milují
json_ld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": [
        {
            "@type": "SoftwareApplication",
            "name": p["name"],
            "softwareVersion": p["version"],
            "description": p["description"],
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "macOS"
        } for p in packages
    ]
}

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- SEO & OpenGraph -->
    <title>Toobab Homebrew Tap</title>
    <meta name="description" content="Custom Homebrew tap for macOS applications including Nuvio and DbGate Premium.">
    <meta property="og:title" content="Toobab Homebrew Tap">
    <meta property="og:description" content="Automated Homebrew repository for custom macOS packages.">
    <meta property="og:type" content="website">

    <!-- Styl pro čistý, čitelný vzhled -->
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; color: #333; }}
        h1 {{ border-bottom: 2px solid #eaeaea; padding-bottom: 0.5rem; }}
        .package {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 1.5rem; margin-bottom: 1.5rem; }}
        .pkg-header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #eaeaea; padding-bottom: 0.5rem; margin-bottom: 1rem; }}
        .pkg-name {{ font-size: 1.25rem; font-weight: bold; margin: 0; }}
        .pkg-version {{ background: #0969da; color: white; padding: 0.2em 0.6em; border-radius: 2em; font-size: 0.85em; font-weight: bold; }}
        code {{ background: #eff1f3; padding: 0.5rem; border-radius: 4px; display: block; margin-top: 1rem; font-family: monospace; font-size: 0.95em; }}
    </style>

    <!-- GEO Structured Data -->
    <script type="application/ld+json">
    {json.dumps(json_ld, indent=4)}
    </script>
</head>
<body>
    <main>
        <h1>Toobab Homebrew Tap</h1>
        <p>This is a custom Homebrew tap for macOS packages. To add this tap, run:</p>
        <code>brew tap toobab/tap</code>

        <h2>Available Packages</h2>
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
    </main>
</body>
</html>"""

os.makedirs('public', exist_ok=True)
with open('public/index.html', 'w') as f:
    f.write(html_content)
