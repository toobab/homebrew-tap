cask "dbgate@premium" do
  arch arm: "arm64", intel: "x64"

  version "7.3.2-premium-beta.2"
  sha256 arm:   "d239b2629f128c50f6d4fa13aa4116080ed30827015aec87af1de5abea9c7955",
         intel: "c45262233511b5634456b06d4ee33d02d2c3ceb73723ffdbde9df44b178f8b2e"

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
