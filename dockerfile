FROM python:3.13.5-slim

RUN apt-get update && apt-get install -y wget ca-certificates xz-utils && \
    wget -O /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
    tar -xJf /tmp/ffmpeg.tar.xz -C /tmp && \
    mv /tmp/ffmpeg-*/ffmpeg /usr/local/bin/ && \
    mv /tmp/ffmpeg-*/ffprobe /usr/local/bin/ && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf /tmp/* && \
    apt-get remove -y wget ca-certificates xz-utils && apt-get autoremove -y && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]
