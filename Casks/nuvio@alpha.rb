# repository: https://github.com/NuvioMedia/NuvioDesktop
cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.36-alpha"
  sha256 arm:   "8da41505125e1c164024aa57a89186318a2a8ca6af725983bd023c805fcf2a31",
         intel: "16f6a5a6fb7377778cd703cc7de955aa4ee7ba653448f4b4d1483b45a1af803f"

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
    "~/Library/HTTPStorages/com.nuvio.media.desktop",
    "~/Library/Preferences/com.nuvio.media.desktop.plist",
    "~/Library/WebKit/com.nuvio.media.desktop",
  ]
end
