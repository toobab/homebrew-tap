# repository: https://github.com/NuvioMedia/NuvioDesktop
cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.30-alpha"
  sha256 arm:   "11f469d7efbbaaeca65aee3d2f5e990f9ed1f8b4a1d0ce529722fc6ea7844bb9",
         intel: "4388e7d9c43f7c7d00c4d41389624be5f9dcfe5af94606bb0fdd0b9d20d949be"

  url "https://github.com/NuvioMedia/NuvioDesktop/releases/download/#{version}/Nuvio-macOS-#{arch}-#{version}.dmg"
  name "Nuvio Alpha"
  desc "Nuvio Desktop Media Player (Alpha Channel)"
  homepage "https://nuvio.tv/"

  livecheck do
    skip "Updated automatically by GitHub Actions"
  end

  app "Nuvio.app"

  zap trash: [
    "~/Library/Application Support/CrashReporter/Nuvio_*.plist",
    "~/Library/Application Support/Nuvio",
    "~/Library/Caches/com.nuvio.media.desktop",
    "~/Library/Caches/Nuvio",
    "~/Library/Preferences/com.nuvio.media.desktop.plist",
    "~/Library/WebKit/com.nuvio.media.desktop",
  ]
end
