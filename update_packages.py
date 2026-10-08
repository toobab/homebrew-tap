#!/usr/bin/env python3
"""Aktualizuje casky a formule v tapu na nejnovější dostupné verze.

Pravidla:
  * nová verze se použije až ve chvíli, kdy jsou k dispozici všechny potřebné
    soubory (DMG ještě nemusí být nahraný) - jinak se balíček tiše přeskočí
    a zkusí se to při dalším běhu,
  * SHA256 se bere z GitHub API (`digest`) nebo se spočítá ze staženého souboru;
    chybná odpověď (404 apod.) nikdy nevyústí v zapsání hashe,
  * selhání jednoho balíčku neovlivní ostatní.
"""
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def http(url, accept=None):
    headers = {"User-Agent": "homebrew-tap-updater"}
    if accept:
        headers["Accept"] = accept
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {TOKEN}"
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60)


def get_json(url):
    with http(url, "application/vnd.github+json") as r:
        return json.load(r)


def sha256_of_url(url):
    h, size = hashlib.sha256(), 0
    with http(url) as r:  # urllib vyhodí výjimku při 4xx/5xx
        for chunk in iter(lambda: r.read(1 << 20), b""):
            h.update(chunk)
            size += len(chunk)
    if size < 1_000_000:
        raise RuntimeError(f"{url}: podezřele malý soubor ({size} B)")
    return h.hexdigest()


def asset_sha256(asset):
    digest = asset.get("digest") or ""
    if digest.startswith("sha256:"):
        return digest[7:]
    return sha256_of_url(asset["browser_download_url"])


def github_releases(repo):
    return get_json(f"https://api.github.com/repos/{repo}/releases?per_page=50")


def first_complete(releases, accept, wanted):
    """Vrátí (release, {klíč: asset}) pro první release, který vyhovuje a má všechny assety."""
    for rel in releases:
        if rel.get("draft") or not accept(rel):
            continue
        names = {a["name"]: a for a in rel["assets"] if a.get("state", "uploaded") == "uploaded"}
        files = wanted(rel)
        if all(f in names for f in files.values()):
            return rel, {k: names[f] for k, f in files.items()}
    return None, None


# --- definice balíčků --------------------------------------------------------

def dbgate(stable):
    def latest():
        def accept(rel):
            tag = rel["tag_name"]
            if stable:
                return not rel["prerelease"] and re.fullmatch(r"v\d+\.\d+\.\d+", tag)
            return "premium-beta" in tag

        def wanted(rel):
            v = rel["tag_name"].lstrip("v")
            return {a: f"dbgate-premium-{v}-mac_{a}.dmg" for a in ("arm64", "x64")}

        rel, assets = first_complete(github_releases("dbgate/dbgate"), accept, wanted)
        if not rel:
            return None
        return rel["tag_name"].lstrip("v"), {"arm": asset_sha256(assets["arm64"]),
                                              "intel": asset_sha256(assets["x64"])}
    return latest


def nuvio():
    def wanted(rel):
        t = rel["tag_name"]
        return {a: f"Nuvio-macOS-{a}-{t}.dmg" for a in ("arm64", "x86_64")}

    rel, assets = first_complete(github_releases("NuvioMedia/NuvioDesktop"),
                                 lambda r: True, wanted)
    if not rel:
        return None
    return rel["tag_name"], {"arm": asset_sha256(assets["arm64"]),
                             "intel": asset_sha256(assets["x86_64"])}


def vpsfree_client():
    with http("https://rubygems.org/api/v1/gems/vpsfree-client.json") as r:
        info = json.load(r)
    if not re.fullmatch(r"[0-9a-f]{64}", info["sha"]):
        raise RuntimeError("rubygems nevrátil platný sha256")
    return info["version"], info["sha"]


def apply_cask(text, version, shas):
    new = re.sub(r'(?m)^(\s*version\s+")[^"]+(")', rf'\g<1>{version}\g<2>', text, count=1)
    new = re.sub(r'(sha256\s+arm:\s*")[0-9a-f]+(",\s*intel:\s*")[0-9a-f]+(")',
                 rf'\g<1>{shas["arm"]}\g<2>{shas["intel"]}\g<3>', new, count=1)
    return new


def apply_formula(text, version, sha):
    new = re.sub(r'(vpsfree-client-)[0-9][^"/]*?(\.gem")', rf'\g<1>{version}\g<2>', text, count=1)
    new = re.sub(r'(?m)^(\s*sha256\s+")[0-9a-f]+(")', rf'\g<1>{sha}\g<2>', new, count=1)
    return new


PACKAGES = [
    ("Casks/dbgate@premium.rb", dbgate(True), apply_cask),
    ("Casks/dbgate@premium-beta.rb", dbgate(False), apply_cask),
    ("Casks/nuvio@alpha.rb", nuvio, apply_cask),
    ("Formula/vpsfree-client.rb", vpsfree_client, apply_formula),
]


def current_version(text):
    m = re.search(r'(?m)^\s*version\s+"([^"]+)"', text)
    if m:
        return m.group(1)
    m = re.search(r'vpsfree-client-([0-9][^"/]*?)\.gem"', text)
    return m.group(1) if m else None


def main():
    changed, errors = [], []
    for path, fetch, apply in PACKAGES:
        full = os.path.join(ROOT, path)
        name = os.path.basename(path)[:-3]
        try:
            result = fetch()
            if not result:
                print(f"[{name}] žádný kompletní release, přeskakuji")
                continue
            version, shas = result
            text = open(full).read()
            if current_version(text) == version:
                print(f"[{name}] aktuální ({version})")
                continue
            new = apply(text, version, shas)
            if new == text:
                raise RuntimeError("úprava souboru nic nezměnila")
            open(full, "w").write(new)
            print(f"[{name}] {current_version(text)} -> {version}")
            changed.append(f"{name} {version}")
        except Exception as e:  # noqa: BLE001 - chceme pokračovat s dalšími balíčky
            print(f"::warning::[{name}] {type(e).__name__}: {e}")
            errors.append(name)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"message={', '.join(changed)}\n")
    if errors and not changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
