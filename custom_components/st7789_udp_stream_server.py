from PIL import Image
import socket
import time
import image_to_rgb565

UDP_IP = "192.168.0.107"   # ESP32 IP
UDP_PORT = 9998

WIDTH = 240
HEIGHT = 240

BLOCK_LINES = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


image_to_rgb565.gen_rgb565_array("SHARE_20260528_1057020.jpeg")

# 分块发送
for y in range(0, HEIGHT, BLOCK_LINES):

    start = y * WIDTH * 2

    end = start + WIDTH * BLOCK_LINES * 2
    #
    sock.sendto(
        xxx,
        (UDP_IP, UDP_PORT)
    )

    time.sleep(0.002)