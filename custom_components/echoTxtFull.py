import math

from PIL import Image, ImageDraw, ImageFont
import os
import time


def wrap_list(text, limit=7):
    return [
        text[i:i + limit]
        for i in range(0, len(text), limit)
    ]


WIDTH = 1920
HEIGHT = 1080

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    # "/System/Library/Fonts/NewYork.ttf",
    260
)

LINE = 3


def print_str(source_text: str):
    w = wrap_list(source_text)
    if len(w) <= 0:
        return
    elif len(w) <= LINE:
        full_text = source_text
        source_text = None
    else:
        full_text = ''.join(w[:LINE])
        source_text = ''.join(w[LINE:])
    full_list = wrap_list(full_text)
    start = 0
    while True:
        img = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            "black"
        )

        draw = ImageDraw.Draw(img)
        start = 1 + start
        text = '\n'.join(full_list[0:start])
        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = 0
        y = 0
        if len(full_list) == 1:
            x = max((WIDTH - text_width) // 2, 0)
            y = max((HEIGHT - text_height) // 2, 0) - text_height // 2
        draw.text(
            (x, y),
            text,
            font=font,
            fill="white"
        )

        img.save("/tmp/hud.tmp.bmp")

        os.replace(
            "/tmp/hud.tmp.bmp",
            "/tmp/hud.bmp"
        )
        time.sleep(1.5)
        start = start % LINE
        if len(full_list) == start:
            start = 0
        if start != 0:
            continue

        time.sleep(1)
        if source_text is not None:
            print_str(source_text)
        break


# feh -F --reload 0.2 /tmp/hud.bmp
if __name__ == '__main__':
    print_str("测试一行”")
    print_str(
        "在《极限竞速：地平线5》里，手动挡（尤其是“手动+离合”）确实能比自动挡更快，但核心不是“疯狂换挡”，而是把发动机一直维持在最有动力的转速区间。")
    print_str("完成！是“疯狂换挡”")
