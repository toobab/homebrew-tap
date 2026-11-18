# repository: https://github.com/theBGuy/GitDesktop
cask "gitdesktop" do
  version "0.15.0"
  sha256 "a796dff14ba97bf4f5f53447c88558bd3dac10b53223ce885bad3e838ab6af57"

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
