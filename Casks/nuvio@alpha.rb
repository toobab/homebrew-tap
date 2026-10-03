cask "nuvio@alpha" do
  arch arm: "arm64", intel: "x86_64"

  version "0.1.27-alpha"
  sha256 arm:   "6f3b57bda493bc39cf8666affa0d6c8fcfc07686958a741938a7210e532780a6",
         intel: "701e3376b4e947371c5085917635327a34e2d768d56747f9209c965e5acd0b9d"

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
