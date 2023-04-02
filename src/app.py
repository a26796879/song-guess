""" SongGuess Backend """
from flask import Flask, render_template
from main import SongGuess
from lyrics import MusixMatch
app = Flask(__name__)


@app.route('/')
def index():
    """ homepage """
    return render_template('index.html')


@app.route('/lyric')
def lyric():
    """ lyric page """
    return render_template('lyric.html')


@app.route('/get_quiz/<playlist_id>')
def get_quiz(playlist_id):
    """ 取得歌單 """
    return SongGuess.get_playlist(playlist_id)


@app.route('/get_preview/<song_id>')
def get_preview(song_id):
    """ 取得試聽連結 """
    return {"preview_url": SongGuess.get_preview(song_id)}


@app.route('/search_playlist/<keyword>')
def search_playlist(keyword):
    """ 取得 KKBOX 歌單查詢結果 """
    return SongGuess.search_playlist(keyword)


@app.route('/get_lyric/<singer>/<song>')
def get_lyric(singer, song):
    """ 取得 KKBOX 歌單查詢結果 """
    track_id = MusixMatch.get_track(singer=singer, track_name=song)
    return MusixMatch.get_lyrics(track_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
