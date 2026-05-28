from PIL import Image


def gen_rgb565_array(img_path):
    img = Image.open(img_path)
    img = img.resize((240, 240))
    img = img.convert("RGB")

    rgb565_array = bytearray()

    for y in range(240):
        for x in range(240):
            r, g, b = img.getpixel((x, y))

            rgb565 = (
                    ((r & 0xF8) << 8) |
                    ((g & 0xFC) << 3) |
                    (b >> 3)
            )

            rgb565_array.append(rgb565 >> 8)
            rgb565_array.append(rgb565 & 0xFF)

    return rgb565_array


def save_rgb565_file(rgb565_array, output_path="cat.rgb565"):
    with open(output_path, "wb") as f:
        f.write(rgb565_array)

if __name__ == '__main__':
    save_rgb565_file(gen_rgb565_array('./20260109-163317.bmp'))