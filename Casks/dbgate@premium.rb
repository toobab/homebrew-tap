cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.0"
  sha256 arm:   "3874d675ea7ab0c4d45811b2eeb423b15302ad89d565aa9bf66504985458c1be",
         intel: "b5c1a42b2ca5dcd48d3d4be13670e664cf6518100f2389645248e39496c77710"

  url "https://github.com/dbgate/dbgate/releases/download/v#{version}/dbgate-premium-#{version}-mac_#{arch}.dmg"
  name "DbGate Premium"
  desc "Database manager for MySQL, PostgreSQL, SQL Server, MongoDB, SQLite and others"
  homepage "https://dbgate.org/"

  livecheck do
    url :url
    strategy :github_releases
  end

  app "DbGate Premium.app"

  zap trash: [
    "~/Library/Caches/org.dbgate.premium",
    "~/Library/Caches/org.dbgate.premium.ShipIt",
    "~/Library/HTTPStorages/org.dbgate.premium",
    "~/Library/Preferences/ByHost/org.dbgate.premium.ShipIt.*.plist",
    "~/Library/Preferences/org.dbgate.premium.plist",
  ]
end
