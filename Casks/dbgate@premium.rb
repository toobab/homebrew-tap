cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.1"
  sha256 arm:   "4662a09ab325d4586fc6b344e2ebd10566d71a66d23298688562d3aaf511f3ca",
         intel: "d60dc050c9b733a43e56dffd369b6d0f49777e816bed5248a87d208210c76970"

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
