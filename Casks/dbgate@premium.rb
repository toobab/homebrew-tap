cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.2-premium-beta.3"
  sha256 arm:   "7f9bac97fa54891e8eea12655d0418b2c0cac014a5eac620593963bd84ecb34c",
         intel: "5369a56bd3fd6b2e1f4e9a291df21c0d5dcbe857fa73dc3d4cb36f594b82c988"

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
