import requests
import json
import os

kakao_account = '581f10694dca3785189ca3d1ae87c17f'
tts_filename = '/home/pi/tts.mp3'
volume = -500

if kakao_account in [None, '']:
    raise Exception('Kakao account invalid')

tts_url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
tts_headers = {
    'Content-Type': 'application/xml',
    'Authorization': 'KakaoAK ' + kakao_account
}

say_word = '안녕하세요. 열공중이시군요~!!! 오늘은 여기까지!!!ㅠㅠ!!!'

tts_string = '<speak><voice name="WOMAN_READ_CALM">  {} </voice></speak>'.format(say_word)

print(tts_string)
tts_res = requests.post(tts_url, headers=tts_headers, data=tts_string.encode('utf-8'))

with open(tts_filename, 'wb') as f:
    f.write(tts_res.content)

os.system(f'omxplayer -o local --vol {volume} {tts_filename}')