cask "dbgate@premium-beta" do
  arch arm: "arm64", intel: "x64"

  version "7.3.6-premium-beta.1"
  sha256 arm:   "5699817a619d8eb7cd35e032b62f8feee47497a448537f16f9acaced736540db",
         intel: "3e65aa3d7b64b905e3a8fa03b4e60842b02d76943ff97d3c0254cccdf13c68e2"

  url "https://github.com/dbgate/dbgate/releases/download/v#{version}/dbgate-premium-#{version}-mac_#{arch}.dmg"
  name "DbGate Premium Beta"
  desc "Database manager for SQL and NoSQL databases (beta channel)"
  homepage "https://dbgate.org/"

  livecheck do
    skip "Updated automatically by GitHub Actions"
  end

  conflicts_with cask: "dbgate@premium"

  app "DbGate Premium.app"

  zap trash: [
    "~/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments/org.dbgate.premium.sfl4",
    "~/Library/Caches/org.dbgate.premium",
    "~/Library/Caches/org.dbgate.premium.ShipIt",
    "~/Library/HTTPStorages/org.dbgate.premium",
    "~/Library/Preferences/ByHost/org.dbgate.premium.ShipIt.*.plist",
    "~/Library/Preferences/org.dbgate.premium.plist",
  ]
end
