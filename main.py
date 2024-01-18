from flask import Flask, render_template, render_template_string, jsonify, request, send_from_directory
from file_functions import *
from recognize_speech import get_phrases
from text_functions import save_words, get_timestamps


app = Flask(__name__)
app.config["UPLOAD_DIR"] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = max_file_size * 1024 * 1024
delete_old()


class File:
    all = {}

    def __init__(self, name, lang):
        self.name = name
        self.lang = lang
        self.loaded = time.time()
        self.phrases = []
        self.all[name] = self
        self.extract_phrases()

    def extract_phrases(self):
        self.phrases = get_phrases(self.name, self.lang)

    def edit(self, timestamps, silence=False):
        edit(self.name, timestamps, silence)


@app.route('/uploads', methods=['POST'])
def upload():
    file = request.files['file']
    manage_capacity()
    filename, ext = file.filename.split('.')
    number = ''
    while os.path.exists('uploads/'+filename+number+'.'+ext):
        number = str(int('0'+number) + 1)
    filename = filename+number+'.'+ext
    file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
    return jsonify(filename=filename, status=200)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_DIR']), filename)


def load_step(num=None):
    src = f'templates/step{num}.html' if num else f'templates/error.html'
    with open(src, 'r') as f:
        return f.read()


@app.route("/", methods=["GET", "POST"])
def main():
    if request.is_json:
        if request.json.get('nextstep') == '2':
            filename, lang = request.json.get('filename'), request.json.get('lang')
            name = filename.split('.')[0]
            if not convert(filename):
                os.remove('uploads/' + filename)
                return jsonify(render_template_string(load_step(), msg='Only mp3, wav, ogg formats are valid.'))
            if not filename.endswith('.wav'):
                os.remove('uploads/' + filename)
            file = File(name, lang)
            if not file.phrases:
                return jsonify(render_template_string(load_step(), msg='Failed to recognize any word.'))
            return jsonify(render_template_string(load_step(2), name=name, lang=lang, phrases=file.phrases))
        elif request.json.get("nextstep") == '3':
            effect, name, timestamps_string = [request.json.get(i) for i in ['effect', 'name', 'timestamps_string']]
            file = File.all.get(name)
            if not file:
                return jsonify(render_template_string(load_step(), msg='File not found'))
            save_words(timestamps_string)
            file.edit(get_timestamps(timestamps_string), True if effect == 'silence' else False)
            return jsonify(render_template_string(load_step(3), name=name))
        return jsonify(render_template_string(load_step(), msg='Unknown request'))
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
