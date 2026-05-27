from machine import Pin, SPI
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
# | SCL / CLK | GPIO18 |
#
# | SDA / MOSI | GPIO23 |
#
# | RES / RST | GPIO4 |
#
# | DC | GPIO2 |
#
# | CS | GPIO5 |
#
# | BLK | 3.3V |
# =========================
spi = SPI(
    2,
    baudrate=20000000,
    polarity=1,
    phase=1,
    sck=Pin(18),
    mosi=Pin(23)
)
# =========================
# ST7789
# =========================
tft = st7789py.ST7789(
    spi,
    240,
    240,
    reset=Pin(4, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(2, Pin.OUT)
)
# 初始化
tft.init()
# =========================
# 测试颜色
# =========================
tft.fill(st7789py.RED)
time.sleep(1)
tft.fill(st7789py.GREEN)
time.sleep(1)
tft.fill(st7789py.BLUE)
time.sleep(1)
tft.fill(st7789py.BLACK)
time.sleep(1)
tft.pixel(120, 120, st7789py.YELLOW)
# =========================
# 显示 RGB565 图片
# =========================
width = 240
height = 240
with open("cat.rgb565", "rb") as f:
    for y in range(height):
        # 每行:
        # 240 像素 × 2字节
        line = f.read(width * 2)
        tft.blit_buffer(
            line,
            0,
            y,
            width,
            1
        )
print('Done')