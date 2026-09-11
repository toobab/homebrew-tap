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
      Spuštění klienta:
        vpsfreectl

      ---
      Tipy pro autentizaci s 2FA (TOTP):
      Získání tokenu čistě přes CLI příkaz (vpsfreectl token request) často selhává
      kvůli dvoufázovému ověření. Spolehlivý workaround je vygenerovat token přes cURL:

      1. Získání pending tokenu:
         PENDING_TOKEN=$(curl -s -X POST https://api.vpsfree.cz/_auth/token/tokens \\
         -H "Content-Type: application/json" -d '{"user":"tvuj-login","password":"heslo"}')

      2. Potvrzení tokenu pomocí TOTP z authenticatoru:
         curl -X POST https://api.vpsfree.cz/_auth/token/tokens/totp \\
         -H "Content-Type: application/json" -d "{\\"token\\":\\"$PENDING_TOKEN\\",\\"code\\":\\"123456\\"}"

      Následně ulož aktivní token do lokální konfigurace pro automatické přihlašování:
        vpsfreectl --auth token --save tvuj-login
    EOS
  end
end

