class VpsfreeClient < Formula
  desc "Ruby CLI and client library for vpsFree.cz API"
  homepage "https://github.com/vpsfreecz/vpsfree-client"
  url "https://github.com/vpsfreecz/vpsfree-client/archive/refs/tags/v0.20.1.tar.gz"
  sha256 "ea1d614a5c1d9a64b22c894f43cffd131bfbc2cedf616b3474bd256d085a82ab"

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    system "gem", "build", "vpsfree-client.gemspec"
    system "gem", "install", "vpsfree-client-0.20.1.gem"
    
    bin.install libexec/"bin/vpsfreectl"
    bin.env_script_all_files(libexec/"bin", GEM_HOME: ENV["GEM_HOME"])
  end
end
