import uuid
from telethon import events
from config import client
import os
from utilities import convert_to_mp3
SAVE_DIR = 'saved_media'
user_audio_state = {}
os.makedirs(SAVE_DIR, exist_ok=True)
@client.on(events.NewMessage())
async def outgoing_handler(event):
    # if event.chat and event.chat.is_self:
    if not event.is_private:
        return
    msg = event.message
    user_id = event.sender_id
    file_path = None
    text = msg.raw_text or ""
    print(event.raw_text)
    # if msg.message:
    #     print("📝 پیام متنی:")
    #     print(msg.message)
    #     with open(os.path.join(SAVE_DIR, 'texts.txt'), 'a', encoding='utf-8') as f:
    #         f.write(msg.message + '\n' + '-'*40 + '\n')
    #     await event.reply("📝 پیام متنی ذخیره شد.")

    # elif msg.photo:
    #     file_path = await msg.download_media(file=SAVE_DIR)
    #     print("🖼 عکس ذخیره شد:", file_path)
    #     await event.reply(f"🖼 عکس ذخیره شد:\n{file_path}")

    # elif msg.video:
    #     file_path = await msg.download_media(file=SAVE_DIR)
    #     print("🎥 ویدیو ذخیره شد:", file_path)
    #     await event.reply(f"🎥 ویدیو ذخیره شد:\n{file_path}")

    # 🎵 صدا (voice note یا موزیک)
    if msg.voice:
        file_path = await msg.download_media(file=SAVE_DIR)
        voiceArtist = msg.sender.username if msg.sender.username else str(event.sender_id)
        user_audio_state[user_id] = {
        'audio': file_path,
        'artist': voiceArtist,
        'cover': None
        }
        await event.reply(f"ویس ذخیره شد:\n برای تبدیل به فایل لطفا عکس کاور مورد نظر برای آن را بفرستید\n درصورت عدم تمایل به قرار دادن کاور `/skip_cover` را ارسال نمایید")
        # mp3_path = convert_to_mp3(file_path,'mp3' ,voiceArtist)
        # await event.reply(f"🎧 ویس به MP3 تبدیل شد:\n{mp3_path}")
        # await event.reply(file=mp3_path)
        # try:
        #     os.remove(file_path)
        #     os.remove(mp3_path)
        # except Exception as e:
        #     print(f"⚠️ خطا هنگام حذف فایل‌ها: {e}")
    elif msg.photo:
        # اگر قبلاً فایل صوتی برای این کاربر داریم
        if user_id not in user_audio_state or 'audio' not in user_audio_state[user_id]:
            await event.reply("📷 عکس دریافت شد، ولی هنوز فایل صوتی نفرستادی. اول آهنگ رو بفرست.")
            return

        # ذخیره عکس
        unique_name = str(uuid.uuid4()) + '.jpg'
        cover_path = os.path.join(SAVE_DIR, unique_name)
        await msg.download_media(file=cover_path)

        # حالا تبدیل کن
        state = user_audio_state[user_id]
        audio_path = state['audio']
        artist = state['artist']
        
        await event.reply("🖼 عکس دریافت شد. در حال تبدیل فایل صوتی با کاور جدید...")

        try:
            output_path = convert_to_mp3(audio_path, output_format='mp3', artist=artist, audio_cover_path=cover_path)

            await event.reply("✅ آماده‌ست! فایل نهایی:", file=output_path)

        except Exception as e:
            await event.reply(f"❌ خطا در تبدیل فایل: {e}")
            print(f"Error: {e}")

        finally:
            for p in [audio_path, cover_path, output_path]:
                if p and os.path.exists(p):
                    try:
                        os.remove(p)
                    except:
                        pass
            user_audio_state.pop(user_id, None)
    elif msg.audio:
        # file_path = await msg.download_media(file=SAVE_DIR)
        await event.reply(f"چه قشنگهههه")
    elif msg.message:
        if text == '/skip_cover':
            if user_id in user_audio_state and 'audio' in user_audio_state[user_id]:
                audio_path = user_audio_state[user_id]['audio']
                artist = user_audio_state[user_id]['artist']
                output_path = convert_to_mp3(audio_path, output_format='mp3', artist=artist)
                await event.reply("✅ آماده‌ست! فایل نهایی:", file=output_path)
                for p in [audio_path, output_path]:
                    if p and os.path.exists(p):
                        try:
                            os.remove(p)
                        except:
                            pass
                user_audio_state.pop(user_id, None)
            else:
                await event.reply("❌ هنوز فایل صوتی نفرستادی.")

    # elif msg.document:
    #     file_path = await msg.download_media(file=SAVE_DIR)
    #     print("📎 فایل ذخیره شد:", file_path)
    #     await event.reply(f"📎 فایل ذخیره شد:\n{file_path}")

    # elif msg.sticker:
    #     file_path = await msg.download_media(file=SAVE_DIR)
    #     print("🧲 استیکر ذخیره شد:", file_path)
    #     await event.reply(f"🧲 استیکر ذخیره شد:\n{file_path}")

    # elif msg.web_preview:
    #     print("🌐 پیام با پیش‌نمایش لینک:", msg.message)
    #     await event.reply("🌐 پیام با لینک دریافت شد.")

    # # ❓ ناشناخته
    # else:
    #     print("❓ پیام ناشناخته یا بدون محتوا.")
    #     await event.reply("⛔ نوع پیام پشتیبانی نمی‌شود.")
    #     await event.reply('This is a reply to your message!')

# @client.on(events.MessageDeleted())
# async def deleted_handler(event):