import os
import subprocess

def ensure_ffmpeg():
    if subprocess.call(['which', 'ffmpeg']) != 0:
        print("Downloading ffmpeg...")
        os.system('wget -qO /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz')
        os.system('tar -xJf /tmp/ffmpeg.tar.xz -C /tmp')
        os.system('mv /tmp/ffmpeg-*/ffmpeg /usr/local/bin/ffmpeg')
        os.system('chmod +x /usr/local/bin/ffmpeg')
        os.system('rm -rf /tmp/ffmpeg-*')
    else:
        print("ffmpeg found.")

ensure_ffmpeg()
