cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.3"
  sha256 arm:   "ea925486049d8ed4d5a1c64798c1b23d06ae4c579e75aea6b8e137f0ff6de1a7",
         intel: "db00d4afba716867a3eea422f73e2001621092900b3d1a1e4180a6af9d2357a6"

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
