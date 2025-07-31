from mutagen.easyid3 import EasyID3
import os
import ffmpeg

# def convert_ogg_to_mp3(input_path):
#     output_path = os.path.splitext(input_path)[0] + '.mp3'
#     sound = AudioSegment.from_file(input_path, format='ogg')
#     sound.export(output_path, format='mp3')
#     return output_path


def convert_to_mp3(input_path: str,output_format:str = "mp3" ,artist: str = None) -> str:
    allowed_formats = ['mp3', 'flac', 'ogg', 'm4a', 'mp4', 'wav']
    if output_format not in allowed_formats:
        print(f"⚠️ فرمت خروجی '{output_format}' پشتیبانی نمی‌شود. تبدیل به 'mp3' انجام خواهد شد.")
        output_format = 'mp3'
    output_path = os.path.splitext(input_path)[0] + f'.{output_format}'

    # اجرای ffmpeg برای تبدیل فرمت
    ffmpeg.input(input_path).output(output_path).run(quiet=True, overwrite_output=True)
    if artist and output_format == 'mp3':
        try:
            audio = EasyID3(output_path)

        except Exception:
            from mutagen.mp3 import MP3
            audio = MP3(output_path, ID3=EasyID3)
            audio.add_tags()
            audio = EasyID3(output_path)
        audio['artist'] = artist
        audio.save()
    return output_path