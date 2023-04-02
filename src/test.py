""" 取得試聽連結 """
from kkbox_developer_sdk.auth_flow import KKBOXOAuth
import requests
from bs4 import BeautifulSoup
import os
import json

""" 猜歌遊戲 """
OAUTH_URL = 'https://account.kkbox.com/oauth2/token'

CLIENT_ID = '661b0c84f123f2a78f95ad7455f74aa7'
CLIENT_SECRET = '636b995af81f46efd03cebd90dff9cbc'
API_KEY = 'c9df216200de4ce300804d89ba2e790a'


url = 'https://widget.kkbox.com/v1/?id=DY1OT1_7ri5YSYF4zZ&type=song&terr=TW'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
mydivs = soup.find_all("div", {"class": "___iso-state___"})
access_token = json.loads(mydivs[0]['data-state'])['feed']['accessToken']

song_url = 'https://api-web.kkbox.com.tw/v2/track-previews'
data_ = {
    'track_id': 'DY1OT1_7ri5YSYF4zZ',
    'access_token': access_token,
    'territory': 'TW'
}
res = requests.post(song_url, data=data_)
soup = BeautifulSoup(res.text, 'lxml')
print(res.json()['preview_url'])
