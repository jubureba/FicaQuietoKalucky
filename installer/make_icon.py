#!/usr/bin/env python3
"""Gera installer/icon.ico (ícone do instalador). Rode uma vez: python installer/make_icon.py"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SIZE = 256
ACCENT = (88, 101, 242)   # Discord blurple
FG = (242, 243, 245)


def build() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Fundo com cantos arredondados
    radius = 56
    d.rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=radius, fill=ACCENT)

    # Letra "F" centralizada
    text = "F"
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 170)
    except OSError:
        font = ImageFont.load_default()

    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text(
        ((SIZE - tw) / 2 - box[0], (SIZE - th) / 2 - box[1]),
        text, font=font, fill=FG,
    )
    return img


def main():
    img = build()
    ico = HERE / "icon.ico"
    img.save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Ícone gerado: {ico}")


if __name__ == "__main__":
    main()
