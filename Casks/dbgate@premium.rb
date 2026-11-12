cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.6"
  sha256 arm:   "0a0e32c3e9288fa14fa2bcf4c62bba94d77c682c64845915d6c2ca426ff9012a",
         intel: "ea1e68f660acc1610db350f6239ed7d29b65d9f78f5a133f0a2e6f061ef8ab0d"

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
