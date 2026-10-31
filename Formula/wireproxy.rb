# repository: https://github.com/windtf/wireproxy
class Wireproxy < Formula
  desc "WireGuard client that exposes itself as a SOCKS5 proxy"
  homepage "https://github.com/windtf/wireproxy"
  url "https://github.com/windtf/wireproxy/releases/download/v1.1.3/wireproxy_darwin_all.tar.gz"
  sha256 "7d55581d0310afe6b882717e6e6d5abf86cad05b9f5de63d0bb5133ba9da0cee"
  license "ISC"

  def install
    bin.install "wireproxy"
  end

  def caveats
    <<~EOS
      Run with a WireGuard-style config file:
        wireproxy -c /path/to/config
      Example configuration: https://github.com/windtf/wireproxy#configuration
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/wireproxy -v")
  end
end
