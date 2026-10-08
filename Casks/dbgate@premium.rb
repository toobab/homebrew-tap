cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.2"
  sha256 arm:   "0fa5f7e042d3085e408c38989bcfa91979599cb09d6f60d054e91869d9ea00c3",
         intel: "0eb699d044fa360bd12ec3687e54933a2e4afa7580c94b6aa0d3025111cb6f19"

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
    "~/Library/Caches/org.dbgate.premium",
    "~/Library/Caches/org.dbgate.premium.ShipIt",
    "~/Library/HTTPStorages/org.dbgate.premium",
    "~/Library/Preferences/ByHost/org.dbgate.premium.ShipIt.*.plist",
    "~/Library/Preferences/org.dbgate.premium.plist",
  ]
end
