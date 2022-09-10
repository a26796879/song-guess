""" 猜歌遊戲主程式 """
from pickletools import read_uint1
from tkinter.tix import Tree
import requests
from bs4 import BeautifulSoup
import random
import os
import settings
from lyrics import MusixMatch


class SongGuess:
    """ 猜歌遊戲 """
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    OAUTH_URL = 'https://openapi-docs-proxy.azurewebsites.net/oauth2/token'

    @classmethod
    def get_token_headers(cls):
        """ 取得token """
        payload = {
            'redirect_uri': 'https://docs-zhtw.kkbox.codes/oauth-receiver.html',
            'grant_type': 'client_credentials',
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET
        }

        res = requests.post(url=cls.OAUTH_URL, data=payload)
        headers = {
            'accept': "application/json",
            'authorization': f"Bearer {res.json()['access_token']}"
        }
        return headers

    @classmethod
    def search_singer(cls, keyword):
        """ 搜尋關鍵字取得歌手ID """
        url = f"https://api.kkbox.com/v1.1/search?q={keyword}&type=artist&territory=TW&offset=0&limit=50"
        res = requests.get(url=url, headers=cls.get_token_headers())
        return res.json()['artists']['data'][0]['id']

    @classmethod
    def get_top_tracks(cls, singer_id):
        """ 根據歌手ID取得熱門歌曲 """
        top_tracks_url = f"https://api.kkbox.com/v1.1/artists/{singer_id}/top-tracks?territory=TW&offset=0&limit=500"
        res = requests.get(url=top_tracks_url, headers=cls.get_token_headers())
        return res.json()['data']

    @classmethod
    def get_playlist(cls, playlist_id):
        """ 根據 歌單ID取得 歌曲 """
        playlist_url = f"https://api.kkbox.com/v1.1/session-playlists/{playlist_id}?territory=TW&offset=0&limit=500"
        res = requests.get(url=playlist_url, headers=cls.get_token_headers())
        return res.json()  # ['tracks']['data']

    @staticmethod
    def get_preview(song_id):
        """ 取得試聽連結 """
        song_url = f'https://www.kkbox.com/tw/tc/song/{song_id}'
        res = requests.get(song_url)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup.find_all('meta')[10].get('content')

    @staticmethod
    def run(type, data):
        """ 執行遊戲
            type:
                by_singer、by_playlist
            data:
                by_singer: singer
                by_playlist: playlist
        """
        if type == 'by_singer':
            singer_id = SongGuess.search_singer(data)
            quiz = SongGuess.get_top_tracks(singer_id)

        if type == 'by_playlist':
            quiz = SongGuess.get_playlist(data)

        nubmer = random.randrange(len(quiz))
        singer = quiz[nubmer]['album']['artist']['name'].split(' (')[0]
        track_name = quiz[nubmer]['name'].split(' (')[0]
        track = MusixMatch.get_track(
            singer=singer, track_name=track_name)

        # print(quiz[nubmer]['name'], quiz[nubmer]['album']['artist']['name'],
        preview_url = SongGuess.get_preview(quiz[nubmer]['id'])
        print(preview_url)

        lyrics = MusixMatch.get_lyrics(track).replace(
            '******* This Lyrics is NOT for Commercial use *******', ''
        ).replace(
            '(1409622762958)', ''
        ).replace(
            '男: ', ''
        ).replace(
            '女: ', ''
        ).replace(
            '男女: ', ''
        )

        # print(lyrics)
        if lyrics != 'Something error':
            MusixMatch.speech_lyric(lyrics)
            return preview_url
        return False


if __name__ == '__main__':
    # while SongGuess.run(type='by_singer', data='周杰倫') is not True:
    #     SongGuess.run(type='by_singer', data='周杰倫')

    #SongGuess.run(type='by_singer', data='李聖傑')
    SongGuess.run(type='by_playlist', data='OqvcU7OhhreaHHFltp')
