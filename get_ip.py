from ssd1306_oled import *
from PIL import ImageFont, Image, ImageDraw
import socket
import fcntl
import struct
import time

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915, 
            struct.pack("256s", str.encode(ifname[:15])),
        )[20:24]
    )

spi = busio.SPI(11, 10, 9)
rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
oled = ssd1306.SSD1306_SPI(128,64, spi, dc_pin, rst_pin, cs_pin)
font = ImageFont.truetype(font_path, 15)

time.sleep(30)
text = get_ip_address("wlan0")
print(text)

image = Image.new("1", (128,64))
draw = ImageDraw.Draw(image)
draw.text((5,5), text, font=font, fill=255)

oled.image(image)
oled.show()