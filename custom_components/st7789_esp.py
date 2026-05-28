from machine import Pin, SPI, PWM
import st7789py
import time
import socket
import _thread


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


WIDTH = 240
HEIGHT = 240

BLOCK_LINES = 2

BLOCK_SIZE = WIDTH * BLOCK_LINES * 2
FRAME_START = b"\xAA\x55"

# 预分配 buffer
buf = bytearray(BLOCK_SIZE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 9998))

print("st7789 UDP listen 9998")


def rest():
    tft.reset()


def udp_video_stream():
    current_y = 0

    while True:

        data, addr = sock.recvfrom(BLOCK_SIZE + 16)

        # 帧同步头
        if data.startswith(FRAME_START):
            tft.fill(st7789py.BLACK) #清屏
            current_y = 0
            data = data[2:]

        data_len = len(data)

        if data_len == 0:
            continue

        mv = memoryview(buf)

        mv[:data_len] = data

        h = data_len // (WIDTH * 2)

        if h <= 0:
            continue

        # 显示当前块
        tft.blit_buffer(
            mv[:data_len],
            0,
            current_y,
            WIDTH,
            h
        )

        current_y += h

        # 超出屏幕重新同步
        if current_y >= HEIGHT:
            current_y = 0


def test_udp_stream():
    set_screen_background_light(300)
    # 启动 UDP 视频流线程
    _thread.start_new_thread(
        udp_video_stream,
        ()
    )
    print("udp stream thread started")


if __name__ == '__main__':
    set_screen_background_light(300)
    tft.fill(st7789py.YELLOW)
    time.sleep(1)
    test_default()
    test_udp_stream()
