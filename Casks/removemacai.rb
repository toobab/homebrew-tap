# repository: https://github.com/omlahore/RemoveMacAI
cask "removemacai" do
  version "1.1.2"
  sha256 "9b487013d566c2dc052060588bb97813f1401ac4c0ee483c55382dbe44e89af5"

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
