# repository: https://github.com/omlahore/RemoveMacAI
cask "removemacai" do
  version "1.1.0"
  sha256 "6119e9b5e6ec2517a30778e2cc34090e29ff872878d94ec53cd69485b9aab7e2"

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
