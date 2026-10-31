# homebrew-tap

```bash
brew tap toobab/tap
brew install --cask toobab/tap/dbgate@premium        # stable
brew install --cask toobab/tap/dbgate@premium-beta   # beta
brew install --cask toobab/tap/nuvio@alpha
brew install --cask toobab/tap/gitdesktop
brew install --cask toobab/tap/removemacai
brew install toobab/tap/vpsfree-client
brew install toobab/tap/wireproxy
brew install toobab/tap/n-m3u8dl-re
```

Verze se aktualizují automaticky (`update_packages.py`, workflow *Update Packages* každé 3 h).
Nová verze se zapíše až ve chvíli, kdy jsou nahrané všechny soubory (DMG), jinak se počká na další běh.
Po každé změně se přegeneruje web na GitHub Pages (`generate_page.py`).
Web generuje také `sitemap.xml`, `robots.txt`, `llms.txt` a samostatnou stránku pro každý balíček (SEO).
