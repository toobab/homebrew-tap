cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.24-alpha"
  sha256 arm:   "e847768f5ccc30e51b5f9d6484c737c6017cf0ce1301ecf36a1605a9df422612",
         intel: "f68f88d7ce3976df97f8ccfbf1e581041339a894c3d8a1d0a5e576b70f008810"

  url "https://github.com/NuvioMedia/NuvioDesktop/releases/download/#{version}/Nuvio-macOS-#{arch}-#{version}.dmg"
  name "Nuvio Alpha"
  desc "Nuvio Desktop Media Player (Alpha Channel)"
  homepage "https://nuvio.tv/"

  livecheck do
    url :url
    strategy :github_releases
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
