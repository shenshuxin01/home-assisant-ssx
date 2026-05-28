from machine import Pin, SPI, PWM
import st7789py
import time


#
# =========================
# SPI## 一、硬件接线
#
# | ST7789 屏幕 | ESP32 |
#
# |---|---|
#
# | GND | GND |
#
# | VCC | 3.3V |
#
# | SCL / CLK | GPIO15 |
#
# | SDA / MOSI | GPIO14 |
#
# | RES / RST | GPIO12 |
#
# | DC | GPIO25 |
#
# | CS | GPIO26 |
#
# | BLK | 3.3V | 屏幕背光 GPIO27
# =========================

def set_screen_background_light(light: int = 0):
    bl = PWM(Pin(27))
    bl.freq(1000)
    # 亮度 0~1023
    bl.duty(light % 1000)


spi = SPI(
    2,
    baudrate=20000000,
    polarity=1,
    phase=1,
    sck=Pin(15),
    mosi=Pin(14)
)
# =========================
# ST7789
# =========================
tft = st7789py.ST7789(
    spi,
    240,
    240,
    reset=Pin(12, Pin.OUT),
    cs=Pin(26, Pin.OUT),
    dc=Pin(25, Pin.OUT)
)
# 初始化
tft.init()


def test_default():
    width = 240
    height = 240

    block_lines = 20

    buf = bytearray(width * block_lines * 2)
    with open("cat.rgb565", "rb") as f:

        for y in range(0, height, block_lines):

            h = min(block_lines, height - y)
            size = width * h * 2
            f.readinto(buf)
            tft.blit_buffer(
                memoryview(buf)[:size],
                0,
                y,
                width,
                h
            )


if __name__ == '__main__':
    set_screen_background_light(300)
    time.sleep(3)
    test_default()