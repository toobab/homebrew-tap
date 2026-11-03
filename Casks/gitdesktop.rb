# repository: https://github.com/theBGuy/GitDesktop
cask "gitdesktop" do
  version "0.13.8"
  sha256 "25f48fee4e088bcb8d4b9dc2e8a416b66eb9a002564e46ea43b9eda2fe7ed376"

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
