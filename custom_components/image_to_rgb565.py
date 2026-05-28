from PIL import Image

img = Image.open("./IMG_3384.jpeg")
img = img.resize((240, 240))
img = img.convert("RGB")

with open("cat.rgb565", "wb") as f:
    for y in range(240):
        for x in range(240):
            r, g, b = img.getpixel((x, y))

            rgb565 = (
                    ((r & 0xF8) << 8) |
                    ((g & 0xFC) << 3) |
                    (b >> 3)
            )

            f.write(bytes([
                rgb565 >> 8,
                rgb565 & 0xFF
            ]))
