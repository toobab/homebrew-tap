cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.26-alpha"
  sha256 arm:   "bd8b91ecd7230d11e076212adda514b39150941c192dfd7b77706d0d2d7558d9",
         intel: "78cb4e8a1e9572658dfb4d9fb49425d745e95b6517078b3a8d909e0a3003b9f5"

  url "https://github.com/NuvioMedia/NuvioDesktop/releases/download/#{version}/Nuvio-macOS-#{arch}-#{version}.dmg"
  name "Nuvio Alpha"
  desc "Nuvio Desktop Media Player (Alpha Channel)"
  homepage "https://github.com/NuvioMedia/NuvioDesktop"

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
