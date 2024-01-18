import whisper_timestamped as whisper
from text_functions import evaluate, load_words
from dataclasses import dataclass

model = whisper.load_model("base", device="cpu")


@dataclass
class Phrase:
    start: float
    end: float
    text: str
    confidence: float
    tone: float


def _recognize(name, lang):
    return whisper.transcribe(model, whisper.load_audio(f'uploads/{name}.wav'), language=lang)


def get_phrases(name, lang):
    result = _recognize(name, lang)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    arr, no_speach_prob = [], 0
    if 'segments' in result.keys():
        for segment in result['segments']:
            if segment['no_speech_prob'] > 0.6:
                continue
            for d in segment['words']:
                text = ''.join(a for a in d['text'] if a.isalpha())
                arr.append(Phrase(d['start'], d['end'], text, d['confidence'], evaluate(text, lang)))
    return arr


if __name__ == '__main__':
    print(get_phrases('test', 'uk'))
