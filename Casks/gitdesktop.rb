# repository: https://github.com/theBGuy/GitDesktop
cask "gitdesktop" do
  version "0.13.7"
  sha256 "aeb3827ea1c865cc86d21440f000bb7b03225268b1649e48c734d42d1ffd8ea7"

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
