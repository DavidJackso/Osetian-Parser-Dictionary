from pydub import AudioSegment
from pydub import S

def split_audio_ru_os(target_audio_path,os_audio_path, ru_audio_path):
    sound = AudioSegment.from_file(target_audio_path)

