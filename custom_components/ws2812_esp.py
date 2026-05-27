from machine import Pin
import neopixel
import time

LED_NUM = 16
MAX_RPM = 8000

np = neopixel.NeoPixel(Pin(33), LED_NUM)


# brightness 亮度 0-1范围
def set_pixel(i, r, g, b, brightness=0.3):
    np[i] = (int(r * brightness),
             int(g * brightness),
             int(b * brightness))


def test(num: int):
    # 根据转速计算亮灯数量
    led_count = max(num % 17,0)

    for i in range(LED_NUM):

        if i < led_count:

            # 低转速 绿色
            if i < LED_NUM * 0.5:
                set_pixel(i, 0, 255, 0)

            # 中转速 黄色
            elif i < LED_NUM * 0.8:
                set_pixel(i, 255, 120, 0)

            # 高转速 红色
            else:
                set_pixel(i, 255, 0, 0)

        else:
            set_pixel(i, 0, 0, 0)

    np.write()

if __name__ == '__main__':
    test(15)
