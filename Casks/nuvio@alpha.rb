# repository: https://github.com/NuvioMedia/NuvioDesktop
cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.38-alpha"
  sha256 arm:   "a456810871b957104164315cf30806b59fa61b220428f26afabea552f9d113d8",
         intel: "ee28136d68cdc27f796e16b1251d830eb847008f4a8622ea0fc833e794a29baa"

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
