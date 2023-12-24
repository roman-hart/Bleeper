from flask import Flask, render_template, jsonify, request, send_from_directory
from edit_audio import edit, convert
from recognize_speech import get_phrases
from evaluate_wors import evaluate, re
import os


app = Flask(__name__)
app.config["UPLOAD_DIR"] = "uploads"


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_DIR']), filename)


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        lang = request.values.get('lang')
        if 'file' in request.files:
            file = request.files['file']  # for file in request.files.getlist('file'):
            name = file.filename.split('.')[0]
            file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
            if not convert(file.filename):
                return render_template("index.html", msg='Unknown file format. Only mp3, wav, ogg are valid.')
            phrases = get_phrases(name, lang)
            if not phrases:
                return render_template("index.html", msg='Failed to recognize any word.')
            for ph in phrases:
                ph[-1] = evaluate(ph[2], lang)
            print('Phrases:', phrases)
            return render_template("index.html", name=name, lang=lang, phrases=phrases,
                                   phrases_string=';'.join('-'.join(str(p) for p in ph) for ph in phrases))
        if timestamps := request.values.get('timestamps_string'):
            effect, name, phrases_string = [request.values.get(i) for i in ['effect', 'name', 'phrases_string']]
            phrases = [ph.split('-') for ph in phrases_string.split(';')]
            timestamps = re.sub(r'\([^)]*\)', '', timestamps)
            timestamps = [tuple(float(j) for j in i.split('-')) for i in timestamps.split(';')[:-1]]
            edit(name, timestamps, True if effect == 'silence' else False)
            return render_template("index.html", name=name, timestamps=timestamps,
                                   lang=lang, phrases=phrases)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
