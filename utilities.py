import subprocess
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error as ID3Error
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggvorbis import OggVorbis
from PIL import Image
import imageio_ffmpeg as ffmpeg

# def convert_ogg_to_mp3(input_path):
#     output_path = os.path.splitext(input_path)[0] + '.mp3'
#     sound = AudioSegment.from_file(input_path, format='ogg')
#     sound.export(output_path, format='mp3')
#     return output_path


def embed_cover(output_path: str, cover_path: str):
    ext = os.path.splitext(output_path)[1].lower()
    with open(cover_path, 'rb') as imgf:
        img_data = imgf.read()

    if ext == '.mp3':
        try:
            audio = ID3(output_path)
        except ID3Error:
            audio = MP3(output_path, ID3=ID3)
            audio.add_tags()
        audio.delall('APIC')
        audio.add(APIC(
            encoding=3,             # UTF-8
            mime='image/jpeg' if cover_path.lower().endswith('.jpg') else 'image/png',
            type=3,                 # cover(front)
            desc='Cover',
            data=img_data
        ))
        audio.save(v2_version=3)
    
    elif ext == '.flac':
        audio = FLAC(output_path)
        audio.clear_pictures()
        pic = Picture()
        pic.data = img_data
        pic.mime = 'image/jpeg' if cover_path.endswith('.jpg') else 'image/png'
        pic.type = 3  # front cover
        pic.desc = 'Cover'
        audio.add_picture(pic)
        audio.save()

    elif ext in ('.m4a', '.mp4'):
        audio = MP4(output_path)
        fmt = MP4Cover.FORMAT_JPEG if cover_path.endswith('.jpg') else MP4Cover.FORMAT_PNG
        audio.tags['covr'] = [MP4Cover(img_data, imageformat=fmt)]
        audio.save()

    elif ext == '.ogg':
        pass

def convert_to_mp3(input_path: str,output_format:str = "mp3" ,artist: str = None, audio_cover_path: str = None) -> str:
    """
    این تابع فایل صوتی رو به فرمت دلخواه تبدیل می‌کنه،
    اگر اسم خواننده یا کاور بدی، اون‌ها رو هم اضافه می‌کنه، و در نهایت مسیر فایل خروجی رو بهت می‌ده.
    """
    allowed_formats = ['mp3', 'flac', 'ogg', 'm4a', 'mp4', 'wav']
    if output_format not in allowed_formats:
        print(f"⚠️ فرمت خروجی '{output_format}' پشتیبانی نمی‌شود. تبدیل به 'mp3' انجام خواهد شد.")
        output_format = 'mp3'

    output_path = os.path.splitext(input_path)[0] + f'.{output_format}'

    ffmpeg_path = ffmpeg.get_ffmpeg_exe()

    subprocess.run([
        ffmpeg_path,
        '-y',  # برای overwrite
        '-i', input_path,
        output_path
    ], check=True)

    if artist and output_format == 'mp3':
        try:
            audio = EasyID3(output_path)
        except Exception:
            audio = MP3(output_path, ID3=EasyID3)
            audio.add_tags()
            audio = EasyID3(output_path)

        audio['artist'] = artist
        audio.save(v2_version=3) 
        if audio_cover_path:
            try:
                crop_center_square(audio_cover_path)
                embed_cover(output_path, cover_path = audio_cover_path)
            except Exception as e:
                print(f"⚠️ خطا در embed کردن کاور: {e}")
        else:
            audio.save()

    return output_path




def crop_center_square(image_path: str) -> str:
    """
    تصویر رو باز می‌کنه، وسطشو به صورت 1:1 کراپ می‌کنه، و روی خودش overwrite می‌کنه.
    """
    img = Image.open(image_path)
    width, height = img.size
    min_dim = min(width, height)

    # محاسبه مختصات کراپ
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(image_path)  # روی فایل اصلی ذخیره کنه (یا می‌تونی مسیر جدید بدی)

    return image_path