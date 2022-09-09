""" SongGuess Backend """
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('learn.html')


@app.route('/question')
def download_file():
    return send_from_directory(r'music/', 'question.wav')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
