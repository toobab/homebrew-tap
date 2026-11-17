# repository: https://github.com/NuvioMedia/NuvioDesktop
cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.37-alpha"
  sha256 arm:   "9835d5a800672ffeb7be759f358d1a190bcaf56545ccdaed502016da243c87de",
         intel: "1ded3b9c87d167806889f290dd471f66c73049465cb36e900be6b90a529f3bb8"

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
