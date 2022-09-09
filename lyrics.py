""" Lyrics """
from opencc import OpenCC
import requests
import pyttsx3
import os
import settings

API_KEY = os.getenv('API_KEY')
URL = 'https://api.musixmatch.com/ws/1.1/'
HEADERS = {
    'apikey': API_KEY
}


class MusixMatch:
    """ 歌詞API """
    TO_SAMPLE = OpenCC('t2s')

    @classmethod
    def get_track(cls, singer, track_name):
        """ 根據歌手&歌名 取得歌詞ID """
        track_url = f'{URL}matcher.track.get?apikey={API_KEY}&q_artist={cls.TO_SAMPLE.convert(singer)}&q_track={track_name}'
        print(track_url)
        res = requests.get(url=track_url, headers=HEADERS)
        res_status_code = res.json()['message']['header']['status_code']
        if res_status_code != 200:
            return 'Something error'
        return res.json()['message']['body']['track']['track_id']

    @classmethod
    def get_lyrics(cls, track_id):
        """ 根據歌詞ID 取得歌詞 """
        lyric = f'track.lyrics.get?apikey={API_KEY}&track_id={track_id}'
        lyric_res = requests.get(url=URL+lyric, headers=HEADERS)
        lyric_res_status_code = lyric_res.json(
        )['message']['header']['status_code']
        if lyric_res_status_code != 200:
            return 'Something error'
        return lyric_res.json()['message']['body']['lyrics']['lyrics_body']

    @staticmethod
    def speech_lyric(lyric):
        """ 念出歌詞 """
        text_speech = pyttsx3.init()
        # text_speech.say(lyric)
        text_speech.save_to_file(lyric, 'question.mp3')
        text_speech.runAndWait()
        return True


if __name__ == '__main__':
    track = 1  # MusixMatch.get_track(singer=SINGER, track_name=TRACK)
    print(track)
# lyrics = MusixMatch.get_lyrics(track).replace(
#     '******* This Lyrics is NOT for Commercial use *******', '').replace('(1409622762958)', '')
# print(lyrics)
