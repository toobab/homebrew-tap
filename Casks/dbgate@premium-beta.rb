cask "dbgate@premium-beta" do
  arch arm: "arm64", intel: "x64"

  version "7.3.2-premium-beta.4"
  sha256 arm:   "15e03c6641dcd1e3eaac25c7729e81da2770da93839403edcfa10f3e534b0012",
         intel: "da3c584911539500120ab66bdbcb38ff65ed72b54d7be0fcb8aff86ee267bf80"

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
    "~/Library/Caches/org.dbgate.premium",
    "~/Library/Caches/org.dbgate.premium.ShipIt",
    "~/Library/HTTPStorages/org.dbgate.premium",
    "~/Library/Preferences/ByHost/org.dbgate.premium.ShipIt.*.plist",
    "~/Library/Preferences/org.dbgate.premium.plist",
  ]
end
