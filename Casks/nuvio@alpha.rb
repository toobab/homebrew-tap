cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.29-alpha"
  sha256 arm:   "0d8992627cf9779f1d5f1ffab573b4a73cb89d8741b9eeea3095560acb8d86a5",
         intel: "f5f7b3df7d448adbb3c0b35481d2e7e21928643c951088aede7aabd9ffb03c8a"

  url "https://github.com/NuvioMedia/NuvioDesktop/releases/download/#{version}/Nuvio-macOS-#{arch}-#{version}.dmg"
  name "Nuvio Alpha"
  desc "Nuvio Desktop Media Player (Alpha Channel)"
  homepage "https://github.com/NuvioMedia/NuvioDesktop"

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
