import cv2

#촬영할 카메라 할당
cap=cv2.VideoCapture(0)

#사진촬영
_, img=cap.read()

#img를 img.jpg 파일로 저장
cv2.imwrite('image.jpg', img)

#img를 128*64 크기로 변환한 후 image1.jpg 파일로 저장
re_img=cv2.resize(img, (128,64))
cv2.imwrite('image1.jpg', re_img)

from ssd1306_oled import *
from PIL import ImageFont, Image, ImageDraw

spi = busio.SPI(11, 10, 9)
rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!

font_path = "/home/pi/KDL.ttf"
# font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
oled = ssd1306.SSD1306_SPI(128,64, spi, dc_pin, rst_pin, cs_pin)
font = ImageFont.truetype(font_path, 15)

image = Image.new("1", (128,64))
draw = ImageDraw.Draw(image)
# draw.text((5,5), "안녕하세요", font=font, fill=255)
# draw.text((5,5), "Good morning", font=font, fill=255)

image=Image.open('/home/pi/image1.jpg').convert('1')
oled.image(image)
oled.show()