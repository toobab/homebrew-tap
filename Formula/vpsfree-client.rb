class VpsfreeClient < Formula
  desc "Ruby CLI and client library for vpsFree.cz API"
  homepage "https://github.com/vpsfreecz/vpsfree-client"
  url "https://rubygems.org/downloads/vpsfree-client-0.20.1.gem"
  sha256 "ef0dfadd1a5b7ba6183045fa8950a168d0913747f61ab9599c85642536026fcd"

  depends_on "ruby"

  def install
    ENV["GEM_HOME"] = libexec
    system "gem", "install", "vpsfree-client-0.20.1.gem", "--no-document"
    
    bin.install libexec/"bin/vpsfreectl"
    bin.env_script_all_files(libexec/"bin", GEM_HOME: ENV["GEM_HOME"])
  end

  def caveats
    <<~EOS
      Running the client:
        vpsfreectl

      ---
      Authentication with 2FA (TOTP) workaround:
      Generating a token purely via the CLI (vpsfreectl token request) often fails
      due to two-factor authentication. A reliable workaround is to generate the token via cURL:

      1. Request a pending token:
         PENDING_TOKEN=$(curl -s -X POST https://api.vpsfree.cz/_auth/token/tokens \\
         -H "Content-Type: application/json" -d '{"user":"your-username","password":"your-password"}')

      2. Confirm the token with your TOTP code:
         curl -X POST https://api.vpsfree.cz/_auth/token/tokens/totp \\
         -H "Content-Type: application/json" -d "{\\"token\\":\\"$PENDING_TOKEN\\",\\"code\\":\\"123456\\"}"

      Finally, save the active token to your local configuration for automatic login:
        vpsfreectl --auth token --save your-username
    EOS
  end
end

