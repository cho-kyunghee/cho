import requests
import json
import os

kakao_account = '581f10694dca3785189ca3d1ae87c17f'

if kakao_account in [None, '']:
    raise Exception('Kakao account invalid')

stt_url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
stt_headers = {
    'Content-Type': 'application/octet-stliream',
    'Authorization': 'KakaoAK ' + kakao_account
}

os.system('arecord -D plughw:1,0 -c2 -r 16000 -f S32_LE -d 5 -t wav -q -vv -V streo stream.raw; sox stream.raw -c 1 -b 16 stream.wav')

with open('stream.wav', 'rb') as f:
    stt_data = f.read()

stt_res = requests.post(stt_url, headers=stt_headers, data=stt_data)
# print(stt_res.text)

result_json_string = stt_res.text[stt_res.text.index('{"type":"finalResult"'):stt_res.text.rindex('}')+1]

# print(result_json_string)
result = json.loads(result_json_string)
# print(result)
print(result['value'])

say_word=result['value']

tts_filename = '/home/pi/tts.mp3'
volume = -500

if kakao_account in [None, '']:
    raise Exception('Kakao account invalid')

tts_url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
tts_headers = {
    'Content-Type': 'application/xml',
    'Authorization': 'KakaoAK ' + kakao_account
}
tts_string = '<speak><voice name="WOMAN_READ_CALM">  {} </voice></speak>'.format(say_word)

print(tts_string)
tts_res = requests.post(tts_url, headers=tts_headers, data=tts_string.encode('utf-8'))

with open(tts_filename, 'wb') as f:
    f.write(tts_res.content)

os.system(f'omxplayer -o local --vol {volume} {tts_filename}')