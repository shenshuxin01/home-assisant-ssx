from machine import Pin, I2C
from machine_i2c_lcd import I2cLcd
import time

# I2C
# 接线图
# 正负极
# SDA - GPIO21
# SCL - GPIO22


print("start")

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

devices = i2c.scan()

print("scan done")

print(devices)


# LCD 地址
I2C_ADDR = 0x27

# 行列
LCD_ROWS = 2
LCD_COLS = 16

# 初始化 LCD
lcd = I2cLcd(
    i2c,
    I2C_ADDR,
    LCD_ROWS,
    LCD_COLS
)

# 清屏
lcd.clear()

# 显示文字
# lcd.backlight_off()
# time.sleep(3)
# lcd.backlight_on()
lcd.putstr("Hello ESP32!")

# 第二行
lcd.move_to(0, 1)
lcd.putstr("LCD1602 IIC")

# 长文本

text = "Hello ESP32 LCD1602 scrolling text demo "


# 滑动窗口

for i in range(len(text) - 15):

    lcd.clear()

    lcd.putstr(text[i:i+16])

    time.sleep(0.3)


print("Done")