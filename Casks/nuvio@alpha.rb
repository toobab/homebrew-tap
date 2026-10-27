# repository: https://github.com/NuvioMedia/NuvioDesktop
cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.33-alpha"
  sha256 arm:   "2dcab2bf5cb84274b6b677ff92348951696d526470b80b59f6d9077eb298724a",
         intel: "a89237c978efb593258ba3b32c38d2a99e101e5242fd4e8975e76efafd61b6e0"

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
