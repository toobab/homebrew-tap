# repository: https://github.com/omlahore/RemoveMacAI
cask "removemacai" do
  version "1.1.4"
  sha256 "2063d4dc7e0b41b15cebcd9e1b9807b04615b96e3e23db35cbd1196be3c96bee"

  url "https://github.com/omlahore/RemoveMacAI/releases/download/v#{version}/RemoveMacAI.zip"
  name "RemoveMacAI"
  desc "Turn off Apple Intelligence, analytics, ads and pop-ups"
  homepage "https://omlahore.github.io/RemoveMacAI/"

  livecheck do
    skip "Updated automatically by GitHub Actions"
  end

  depends_on arch: :arm64
  depends_on macos: :tahoe

  app "RemoveMacAI.app"

  zap trash: [
    "~/Library/Caches/io.github.omlahore.removemacai.app",
    "~/Library/Preferences/io.github.omlahore.removemacai.app.plist",
  ]

  caveats <<~EOS
    The app is only ad-hoc signed (not notarized). If macOS refuses to open it, run:
      xattr -dr com.apple.quarantine /Applications/RemoveMacAI.app
  EOS
end
