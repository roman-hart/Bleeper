from pydub import AudioSegment
from pathlib import Path
import os


def manage_capacity(capacity, max_file_size):
    available = capacity - sum(f.stat().st_size for f in Path('uploads').glob('**/*') if f.is_file()) // 1000000
    if available < max_file_size:
        path_to_oldest = sorted(Path('uploads').iterdir(), key=os.path.getmtime)[0]
        os.remove(path_to_oldest)


def edit(name, timestamps, silence=False, wider=0.15, during_len=None):
    audio = AudioSegment.from_file(f'uploads/{name}.wav')
    for start, end in timestamps:
        start_index, end_index = int(start * 1000), int((end + wider) * 1000)
        d = end_index - start_index if during_len is None else during_len
        audio_before = audio[:start_index]
        audio_during = AudioSegment.silent(duration=d) if silence else AudioSegment.from_file('bleep.mp3')[:d]
        audio_after = audio[end_index:]
        audio = audio_before + audio_during + audio_after
    audio.export(f'uploads/{name}-bleeper_ai.wav', format="wav")


def convert(filename):
    name, typ = filename.split('.')
    if typ == 'mp3':
        sound = AudioSegment.from_mp3(f'uploads/{filename}')
        sound.export(f'uploads/{name}.wav', format="wav")
        return True
    elif typ == 'ogg':
        sound = AudioSegment.from_ogg(f'uploads/{filename}')
        sound.export(f'uploads/{name}.wav', format="wav")
        return True
    elif typ == 'wav':
        return True
    return
