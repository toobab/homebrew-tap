# repository: https://github.com/sunecz/Media-Downloader
class MediaDownloader < Formula
  desc "Download media from various websites"
  homepage "https://projects.suneweb.net/media-downloader/"
  url "https://github.com/sunecz/Media-Downloader/archive/refs/tags/0.2.9-dev.27.alpha.3.tar.gz"
  version "0.2.9-dev.27.alpha.3"
  sha256 "317e7f3d12c97ff7067b7f2d6e5d147d1727fe18492be1a9592bd3326a23312b"
  license "MIT"

  depends_on "ant" => :build
  depends_on "openjdk@21"

  resource "javafx" do
    on_arm do
      url "https://download2.gluonhq.com/openjfx/21.0.9/openjfx-21.0.9_osx-aarch64_bin-sdk.zip"
      sha256 "91de1aa04d46f717ec9bc4d421caece3a25a547519f6fcd190095311dd4ff222"
    end
    on_intel do
      url "https://download2.gluonhq.com/openjfx/21.0.9/openjfx-21.0.9_osx-x64_bin-sdk.zip"
      sha256 "956cef897a1efde9fad387432807c9918b52795c7dc65f1b83dee4ec68ae0318"
    end
  end

  def install
    resource("javafx").stage { (libexec/"javafx").install Dir["*"] }

    ENV["JAVA_HOME"] = formula_opt_libexec("openjdk@21")/"openjdk.jdk/Contents/Home"
    system "ant", "-Dpath.javafx=#{libexec}/javafx", "build"
    libexec.install "build/media-downloader.jar"

    (bin/"media-downloader").write <<~SH
      #!/bin/bash
      # Replaces the official launcher: the application downloads and updates its own
      # JRE, plugins and ffmpeg into a writable directory, then expects a restart.
      HOME_DIR="${MEDIA_DOWNLOADER_HOME:-$HOME/Library/Application Support/MediaDownloader}"
      mkdir -p "$HOME_DIR" && cd "$HOME_DIR" || exit 1

      # Seed or refresh the bootstrap jar when the Homebrew version changes.
      if [ ! -f media-downloader.jar ] || [ "$(cat .brew-version 2>/dev/null)" != "#{version}" ]; then
        cp "#{libexec}/media-downloader.jar" media-downloader.jar
        echo "#{version}" > .brew-version
      fi

      for _ in 1 2 3 4 5; do
        [ -d jre-new ] && rm -rf jre && mv jre-new jre
        [ -f media-downloader-new.jar ] && mv -f media-downloader-new.jar media-downloader.jar
        if [ -x jre/bin/java ]; then
          jre/bin/java -jar media-downloader.jar "$@"
        else
          "#{formula_opt_bin("openjdk@21")}/java" --module-path "#{libexec}/javafx/lib" \\
            --add-modules javafx.controls,javafx.web,javafx.media,javafx.base,javafx.graphics \\
            -jar media-downloader.jar "$@"
        fi
        # The application exits after downloading an update; start it again.
        [ -d jre-new ] || [ -f media-downloader-new.jar ] || break
      done
    SH
  end

  def caveats
    <<~EOS
      Run: media-downloader
      On first launch the application downloads its own JRE, ffmpeg and plugins
      into ~/Library/Application Support/MediaDownloader and then keeps itself updated.
      To remove that data: rm -rf "$HOME/Library/Application Support/MediaDownloader"
    EOS
  end

  test do
    assert_path_exists libexec/"media-downloader.jar"
    assert_match "MediaDownloader", shell_output("unzip -l #{libexec}/media-downloader.jar")
  end
end
