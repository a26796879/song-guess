""" SongGuess Backend """
from flask import Flask, render_template
from main import SongGuess
app = Flask(__name__)


@app.route('/')
def index():
    """ homepage """
    return render_template('index.html')


@app.route('/get_quiz/<playlist_id>')
def get_quiz(playlist_id):
    """ 取得歌單 """
    return SongGuess.get_playlist(playlist_id)


@app.route('/get_preview/<song_id>')
def get_preview(song_id):
    """ 取得試聽連結 """
    return {"preview_url": SongGuess.get_preview(song_id)}


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
