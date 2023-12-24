import whisper_timestamped as whisper
import json

model = whisper.load_model("base", device="cpu")


def _recognize(name, lang):
    return whisper.transcribe(model, whisper.load_audio(f'uploads/{name}.wav'), language=lang)


def get_phrases(name, lang):
    result = _recognize(name, lang)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    phrases, no_speach_prob = [], 0
    if 'segments' in result.keys():
        for segment in result['segments']:
            if segment['no_speech_prob'] > 0.5:
                continue
            for d in segment['words']:
                phrases.append([d['start'], d['end'], d['text'], d['confidence'], 0])
    return phrases


if __name__ == '__main__':
    print(get_phrases('test', 'uk'))
