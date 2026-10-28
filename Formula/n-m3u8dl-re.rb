# repository: https://github.com/nilaoda/N_m3u8DL-RE
class NM3u8dlRe < Formula
  desc "Cross-platform stream downloader for MPD, M3U8 and ISM"
  homepage "https://github.com/nilaoda/N_m3u8DL-RE"
  version "0.6.0-beta"
  license "MIT"

  depends_on "ffmpeg"

  if Hardware::CPU.arm?
    url "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-arm64_20260629.tar.gz"
    sha256 "ca181b7e8976564766c34e3cefe48fff409f58289ca970ade062668c01c53918"
  else
    url "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.6.0-beta/N_m3u8DL-RE_v0.6.0-beta_osx-x64_20260629.tar.gz"
    sha256 "4dab8d256ae3164557f48a3326c8fa60da99e37536ee1589ce6c841180fa8204"
  end

  def install
    bin.install "N_m3u8DL-RE"
  end

  test do
    assert_match version.to_s.split("-").first, shell_output("#{bin}/N_m3u8DL-RE --version 2>&1")
  end
end
