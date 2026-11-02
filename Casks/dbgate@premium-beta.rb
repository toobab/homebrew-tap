cask "dbgate@premium-beta" do
  arch arm: "arm64", intel: "x64"

  version "7.3.4-premium-beta.2"
  sha256 arm:   "54ce6dbaa5c76d8fc80158c1b34e6adeaa8759c4010d067edf2c9769ec038bf7",
         intel: "95faa525a228fe3fe4f77c867da323ad03b6a81a3829e35db39abb9c0a71d089"

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
