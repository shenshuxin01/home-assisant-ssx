from machine import Pin
import neopixel
import time

LED_NUM = 16
MAX_RPM = 8000



np = neopixel.NeoPixel(Pin(18), LED_NUM)
def set_pixel(i, r, g, b, brightness=0.3):
    np[i] = (int(r*brightness),
             int(g*brightness),
             int(b*brightness))
rpm = 0
direction = 1

for qqq in range(9190):

    # 模拟转速变化
    rpm += direction * 200

    if rpm >= MAX_RPM:
        direction = -1

    if rpm <= 0:
        direction = 1

    # 根据转速计算亮灯数量
    led_count = int(rpm / MAX_RPM * LED_NUM)

    for i in range(LED_NUM):

        if i < led_count:

            # 低转速 绿色
            if i < LED_NUM * 0.5:
                set_pixel(i,0,255,0)

            # 中转速 黄色
            elif i < LED_NUM * 0.8:
                set_pixel(i,255,120,0)

            # 高转速 红色
            else:
                set_pixel(i,255,0,0)

        else:
            set_pixel(i,0,0,0)

    np.write()

    time.sleep(0.03)
