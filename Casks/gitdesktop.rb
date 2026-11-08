# repository: https://github.com/theBGuy/GitDesktop
cask "gitdesktop" do
  version "0.14.0"
  sha256 "6404c0219e8a21be1495cd36f9c29a50f5f74daac5c682b6ae726fd0f8268fb9"

  url "https://github.com/theBGuy/GitDesktop/releases/download/v#{version}/GitDesktop_#{version}_universal.dmg"
  name "GitDesktop"
  desc "AI-native, keyboard-first Git desktop client"
  homepage "https://gitdesktop.app/"

  livecheck do
    skip "Updated automatically by GitHub Actions"
  end

  app "GitDesktop.app"

  zap trash: [
    "~/Library/Application Support/com.thebguy.gitdesktop",
    "~/Library/Caches/com.thebguy.gitdesktop",
    "~/Library/WebKit/com.thebguy.gitdesktop",
  ]
end
