from telethon import TelegramClient, events
from telethon.tl.types import Chat
from config import client
import handlers
import install_ffmpeg
async def main():
    print('Starting client...')
    await client.get_me()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()