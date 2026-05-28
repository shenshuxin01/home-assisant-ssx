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


FRAME_START = b"\xAA\x55"

def sendto_esp32(pic_path):
    # bytes_data = image_to_rgb565.gen_rgb565_array("IMG_3384.jpeg")
    bytes_data = image_to_rgb565.gen_rgb565_array(pic_path)
    # bytes_data = image_to_rgb565.gen_rgb565_array("20260109-163317.bmp")

    # 分块发送
    for y in range(0, HEIGHT, BLOCK_LINES):

        start = y * WIDTH * 2

        end = start + WIDTH * BLOCK_LINES * 2

        # 从 rgb565 数组中读取当前块
        block_data = bytes_data[start:end]

        # 第一块增加帧同步头
        if y == 0:
            block_data = FRAME_START + block_data

        sock.sendto(
            block_data,
            (UDP_IP, UDP_PORT)
        )

        time.sleep(0.04)

if __name__ == '__main__':
    sendto_esp32('20260109-163317.bmp')