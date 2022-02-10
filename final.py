import os
import requests, json, csv
from bs4 import BeautifulSoup as bs
import time, datetime, random
import RPi.GPIO as GPIO
import cv2
from PIL import Image
import openpibo_models
from ssd1306_oled import *

cap = cv2.VideoCapture(0)

dialog_path = openpibo_models.filepath('dialog.csv')
dialog_db = []
with open(dialog_path, 'r', encoding='utf-8') as f:
    rdr = csv.reader(f)
    dialog_db = [[line[0].split(' '), line[1], line[2]] for line in rdr]

spi = busio.SPI(11, 10, 9)
rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!
oled = ssd1306.SSD1306_SPI(128,64, spi, dc_pin, rst_pin, cs_pin)

BUTTON = 2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

kakao_account = '3ad5aa16a0dcfd7e59ea407d388ba0da'
tts_filename = '/home/pi/tts.mp3'
stt_filename = '/home/pi/stream.wav'
volume = -500

if kakao_account in [None, '']:
    raise Exception('Kakao account invalid')

stt_url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
stt_headers = {
    'Content-Type': 'application/octet-stliream',
    'Authorization': 'KakaoAK ' + kakao_account
}

tts_url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
tts_headers = {
    'Content-Type': 'application/xml',
    'Authorization': 'KakaoAK ' + kakao_account
}

def make_video():
    t = time.time()
    timeout = 20

    while True:
        _, img = cap.read()
        cv2.imwrite('image.jpg', img)
        img = Image.fromarray(cv2.resize(img,(128,64))).convert('1')
        oled.image(img)
        oled.show()

        if time.time() - t > timeout:
            break

def get_distance(aT, bT):
    cnt = 0
    for i in aT:
        for j in bT:
            if i == j:
                cnt += 1
    return cnt / len(aT)
   

def make_chat(q):
    max_acc = 0
    max_ans = []

    for line in dialog_db:
        acc = get_distance(line[0], q.split(' '))

        if acc == max_acc:
            max_ans.append(line)

        if acc > max_acc:
            max_acc = acc
            max_ans = [line]

    ans = random.choice(max_ans)[1]
    print('answer is : ' + ans)
    return ans

def stt():
    timeout = 5
    os.system(f'arecord -D plughw:1,0 -c 2 -r 16000 -f S32_LE -d {timeout} -t wav -q -vv -V stereo stream.raw;sox stream.raw -c 1 -b 16 {stt_filename}')

    with open(stt_filename, 'rb') as f:
        stt_data = f.read()

    stt_res = requests.post(stt_url, headers=stt_headers, data=stt_data)
    try:
        result_json_string = stt_res.text[stt_res.text.index('{"type":"finalResult"'):stt_res.text.rindex('}')+1]
    except Exception as ex:
        result_json_string = stt_res.text[stt_res.text.index('{"type":"errorCalled"'):stt_res.text.rindex('}')+1]

    result = json.loads(result_json_string)
    print(f'make text : {result["value"]}')
    return result

def tts(tts_string):
    tts_res = requests.post(tts_url, headers=tts_headers, data=tts_string.encode('utf-8'))

    with open(tts_filename, 'wb') as f:
        f.write(tts_res.content)
        print('Success make tts.mp3')

def play_audio():
    os.system(f'omxplayer -o local --vol {volume} {tts_filename}')

def check_keyword(keyword):
    if '날씨' in keyword:
        url = 'https://www.weather.go.kr/w/weather/forecast/short-term.do?stnId=109'
        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        forecast = soup.find('div', {'class':'cmp-view-content'}).text.split('\n')[1].split('○')
        print('weather  : '+ forecast[0])
        today_weather = forecast[0].split('\n')[0]

        print(today_weather)
        make_txt = '<speak><voice name="MAN_READ_CALM"> {}, 이상입니다. <break time="150ms"/></voice></speak>'.format(today_weather)
    elif '시간' in keyword:
        now = str(datetime.datetime.now())
        clock = now.split(' ')[1].split('.')[0]

        make_txt = '<speak><voice name="MAN_READ_CALM"> <say-as interpret-as="time" format="hms12"> {} </say-as> 입니다. <break time="150ms"/></voice></speak>'.format(clock)
    elif '동영상' in keyword:
        make_txt = '<speak><voice name="MAN_READ_CALM"> 20초 동안 촬영하였습니다. <break time="150ms"/></voice></speak>'    
        make_video()
    else:
        ans = make_chat(keyword)
        make_txt = '<speak><voice name="MAN_READ_CALM"> {} <break time="150ms"/></voice></speak>'.format(ans)
    
    return make_txt
    
if __name__ == "__main__":
    logo = Image.open("/home/pi/pibo_logo.png").convert("1")
    oled.image(logo)
    oled.show()

    while True:
        check = GPIO.input(BUTTON)
        print(check)

        if check == 0:
            result = stt()

            if result['type'] == 'errorCalled':
                make_txt = '<speak><voice name="MAN_READ_CALM">잘 못 이해했어요.<break time="150ms"/></voice></speak>'
            else:
                make_txt = check_keyword(result['value'])
            tts(make_txt)
            play_audio()
            
            oled.image(logo)
            oled.show()
        
        time.sleep(1)