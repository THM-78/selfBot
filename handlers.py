from telethon import events
from config import client
import os
from utilities import convert_to_mp3
SAVE_DIR = 'saved_media'
os.makedirs(SAVE_DIR, exist_ok=True)
@client.on(events.NewMessage(incoming=True, ))
async def outgoing_handler(event):
    print(event.raw_text)
    # if event.chat and event.chat.is_self:
    msg = event.message
    file_path = None
    if event.is_private:
        # 📝 پیام متنی
        if msg.message:
            print("📝 پیام متنی:")
            print(msg.message)
            with open(os.path.join(SAVE_DIR, 'texts.txt'), 'a', encoding='utf-8') as f:
                f.write(msg.message + '\n' + '-'*40 + '\n')
            await event.reply("📝 پیام متنی ذخیره شد.")

        # 🖼 عکس (photo)
        elif msg.photo:
            file_path = await msg.download_media(file=SAVE_DIR)
            print("🖼 عکس ذخیره شد:", file_path)
            await event.reply(f"🖼 عکس ذخیره شد:\n{file_path}")

        # 🎥 ویدیو
        elif msg.video:
            file_path = await msg.download_media(file=SAVE_DIR)
            print("🎥 ویدیو ذخیره شد:", file_path)
            await event.reply(f"🎥 ویدیو ذخیره شد:\n{file_path}")

        # 🎵 صدا (voice note یا موزیک)
        elif msg.voice:
            file_path = await msg.download_media(file=SAVE_DIR)
            await event.reply(f"🎵 صدا ذخیره شد:\n{file_path}")
            mp3_path = convert_to_mp3(file_path,'mp3' ,msg.sender.username if msg.sender.username else event.sender_id)
            await event.reply(f"🎧 ویس به MP3 تبدیل شد:\n{mp3_path}")
            await event.reply(file=mp3_path)

        elif msg.audio:
            # file_path = await msg.download_media(file=SAVE_DIR)
            await event.reply(f"چه قشنگهههه")

        # 📎 فایل (document)
        elif msg.document:
            file_path = await msg.download_media(file=SAVE_DIR)
            print("📎 فایل ذخیره شد:", file_path)
            await event.reply(f"📎 فایل ذخیره شد:\n{file_path}")

        # 🧲 استیکر
        elif msg.sticker:
            file_path = await msg.download_media(file=SAVE_DIR)
            print("🧲 استیکر ذخیره شد:", file_path)
            await event.reply(f"🧲 استیکر ذخیره شد:\n{file_path}")

        # 🌐 پیام دارای لینک یا webpage
        elif msg.web_preview:
            print("🌐 پیام با پیش‌نمایش لینک:", msg.message)
            await event.reply("🌐 پیام با لینک دریافت شد.")

        # ❓ ناشناخته
        else:
            print("❓ پیام ناشناخته یا بدون محتوا.")
            await event.reply("⛔ نوع پیام پشتیبانی نمی‌شود.")
            await event.reply('This is a reply to your message!')
