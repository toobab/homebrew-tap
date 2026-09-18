import os, json, requests

TOKEN = os.environ.get('TRAFFIC_TOKEN')
REPO = "toobab/homebrew-tap"
URL = f"https://api.github.com/repos/{REPO}/traffic/clones"

if not TOKEN:
    print("Error: TRAFFIC_TOKEN environment variable not set.")
    exit(1)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch data: {response.status_code} - {response.text}")
    exit(1)

data = response.json()
stats_file = "stats/clones.json"
os.makedirs("stats", exist_ok=True)

# Načtení stávající historie
history = {}
if os.path.exists(stats_file):
    with open(stats_file, 'r') as f:
        history = json.load(f)

# Sloučení nových dat (přepíše posledních 14 dní, zachová starší)
for item in data.get('clones', []):
    date_str = item['timestamp'][:10]
    history[date_str] = {
        "count": item['count'],
        "uniques": item['uniques']
    }

# Uložení seřazené historie
with open(stats_file, 'w') as f:
    json.dump(history, f, indent=2, sort_keys=True)
