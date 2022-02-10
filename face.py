import cv2
import numpy as np
import openpibo_face_models

face_detector = cv2.CascadeClassifier(openpibo_face_models.filepath("haarcascade_frontalface_default.xml"))

cap = cv2.VideoCapture(0)
_, img = cap.read()

if not type(img) is np.ndarray:
    raise Exception('img must be image data from opencv')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_detector.detectMultiScale(gray, 1.1, 5)

print(faces[0])
x, y, w, h = faces[0]

# img, 왼쪽 상단 좌표, 오른쪽 하단 좌표, 색(bgr순서), 사각형 두께
rec_img = cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,255), 5)
cv2.imwrite('image2.jpg', rec_img)

# re_img = cv2.resize(img, (128,64))
# cv2.imwrite('image3.jpg', re_img)

# from ssd1306_oled import *
# from PIL import ImageFont, Image, ImageDraw

# spi = busio.SPI(11, 10, 9)
# rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
# cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
# dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!

# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# oled = ssd1306.SSD1306_SPI(128,64, spi, dc_pin, rst_pin, cs_pin)
# font = ImageFont.truetype(font_path, 15)

# image = Image.new("1", (128,64))
# draw = ImageDraw.Draw(image)

# image = Image.open("/home/pi/camera/image3.jpg").convert("1")
# oled.image(image)
# oled.show()