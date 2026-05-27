from machine import Pin, PWM
import time

# SG90 PWM
servo = PWM(Pin(13), freq=50)

# 角度区间就是25-135
for d in range(25, 135, 5):

    print(d)

    servo.duty(d)

    time.sleep(0.5)
