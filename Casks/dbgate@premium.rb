cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.4"
  sha256 arm:   "7beafbb96f3360a177e8a4ad716956d6664d70e40945228fe4330481ef1355ce",
         intel: "3aa71b2b6daeb2583a4f9b18b144b0d20accb07407b6ba0a9aa1312203ad9b85"

  url "https://github.com/dbgate/dbgate/releases/download/v#{version}/dbgate-premium-#{version}-mac_#{arch}.dmg"
  name "DbGate Premium"
  desc "Database manager for SQL and NoSQL databases"
  homepage "https://dbgate.org/"

  livecheck do
    skip "Updated automatically by GitHub Actions"
  end

  conflicts_with cask: "dbgate@premium-beta"

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
