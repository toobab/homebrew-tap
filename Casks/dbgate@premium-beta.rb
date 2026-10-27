cask "dbgate@premium-beta" do
  arch arm: "arm64", intel: "x64"

  version "7.3.3-premium-beta.15"
  sha256 arm:   "014d5485be680ff412a60173cb6021949d0e815c7cc9d992abb486f29355b8fe",
         intel: "2226fbd696624dabf3cc8acb8c18e5a294e363b85bd25f833bdd498ece658824"

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
