from machine import Pin, PWM
from time import sleep

MAX_BRIGHTNESS = 500
# =========================
# PWM 亮度
# duty:
# 0     最暗
# 1023  最亮
# =========================

brightness = 20

# =========================
# PWM GPIO
# 引脚号	段/功能	ESP32 GPIO 引脚
# 1	e	GPIO 19
# 2	d	GPIO 18
# 3	共阴极	GND
# 4	c	GPIO 5
# 5	dp	GPIO 23
# 6	b	GPIO 4
# 7	a	GPIO 2
# 8	共阴极	GND
# 9	f	GPIO 21
# 10	g	GPIO 22

# =========================
# https://img-blog.csdnimg.cn/img_convert/c0a9e76cabfb25eb2108e1414b79629b.png
# https://i-blog.csdnimg.cn/blog_migrate/dfa16b39922851d9b47c9a70d7b20fc6.png
# https://juejin.cn/post/7377439806136418356

seg_a = PWM(Pin(2), freq=MAX_BRIGHTNESS)
seg_b = PWM(Pin(4), freq=MAX_BRIGHTNESS)
seg_c = PWM(Pin(5), freq=MAX_BRIGHTNESS)
seg_d = PWM(Pin(18), freq=MAX_BRIGHTNESS)
seg_e = PWM(Pin(19), freq=MAX_BRIGHTNESS)
seg_f = PWM(Pin(21), freq=MAX_BRIGHTNESS)
seg_g = PWM(Pin(22), freq=MAX_BRIGHTNESS)
seg_dp = PWM(Pin(23), freq=MAX_BRIGHTNESS)

segments = [
    seg_a,
    seg_b,
    seg_c,
    seg_d,
    seg_e,
    seg_f,
    seg_g
]

digits = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1]
}


def set_seg(seg, on):
    if on:
        seg.duty(brightness)
    else:
        seg.duty(0)


def set_dp(hold: bool = True):
    if hold:
        seg_dp.duty(brightness)
    else:
        seg_dp.duty(0)


def show_digit(num):
    pattern = digits[num]

    for i in range(7):
        set_seg(segments[i], pattern[i])


def close_all():
    set_dp(False)
    for segment in segments:
        set_seg(segment, False)


def pwm_dp():
    # 亮度范围
    # 渐亮
    for duty in range(0, MAX_BRIGHTNESS, 5):
        seg_dp.duty(duty)
        sleep(0.005)

    # 渐暗
    for duty in range(MAX_BRIGHTNESS, 0, -5):
        seg_dp.duty(duty)
        sleep(0.005)
    seg_dp.duty(0)


def test(n: int):
    n = n % 10
    # close_all()
    show_digit(n)
    # pwm_dp()


if __name__ == '__main__':
    test(1)
