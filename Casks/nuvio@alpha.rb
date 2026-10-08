cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.28-alpha"
  sha256 arm:   "78f935a68b78203ab93588391eaa70f1233522b41fa64e7508ffc226dea732dd",
         intel: "4da06bb14e1185458f5d3756dda0902564d1ecfd47d617f648769a37027a5dce"

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
