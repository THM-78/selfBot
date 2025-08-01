#!/bin/sh
set -e
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Downloading ffmpeg..."
  wget -qO /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  tar -xJf /tmp/ffmpeg.tar.xz -C /tmp
  mv /tmp/ffmpeg-*/ffmpeg /usr/local/bin/ffmpeg
  chmod +x /usr/local/bin/ffmpeg
  rm -rf /tmp/ffmpeg-*
else
  echo "ffmpeg is already installed."
fi
