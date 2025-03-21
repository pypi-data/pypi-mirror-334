import re
import warnings
from pathlib import Path

import pyfiglet
from PIL import Image

from archerdfu.glyphs.glyphs import batched

FONT_PATH = Path(__file__).resolve().parent / "fonts" / "default.flf"


class CustomFigletFont(pyfiglet.FigletFont):
    @classmethod
    def preloadFont(cls, font):
        try:
            return super().preloadFont(font)
        except pyfiglet.FontNotFound:
            try:
                with open(font, "rb") as f:
                    return f.read().decode("UTF-8", "replace")
            except (OSError, IOError):
                raise pyfiglet.FontNotFound(font)


class CustomFiglet(pyfiglet.Figlet):
    def setFont(self, **kwargs):
        if "font" in kwargs:
            self.font = kwargs["font"]
        self.Font = CustomFigletFont(font=self.font)

    def render_centered(self, text: str, width: int, height: int):
        # Генеруємо текст у форматі ASCII
        figlet_text = self.renderText(text)

        figlet_lines = figlet_text.splitlines()

        # Обрізаємо або заповнюємо рядки до потрібної ширини
        formatted_lines = [line[:width].center(width) for line in figlet_lines]

        # Розраховуємо, скільки порожніх рядків треба додати для вирівнювання по висоті
        total_lines = len(formatted_lines)
        if total_lines < height:
            top_padding = (height - total_lines) // 2
            bottom_padding = height - total_lines - top_padding
            formatted_lines = [" " * width] * top_padding + formatted_lines + [" " * width] * bottom_padding
        else:
            formatted_lines = formatted_lines[:height]  # Обрізаємо зайві рядки

        return "\n".join(formatted_lines)


ICON_SIZE = 32
WHITE = b"\x00"
BLACK = b"\xC0"


def _warn_unsupported_size(size: int):
    if size != ICON_SIZE:
        warnings.warn(
            f"Using a size different from {ICON_SIZE} may cause unexpected behavior.",
            UserWarning,
            stacklevel=2,
        )


def _trunc_caliber(caliber: str) -> str:
    caliber = re.sub(r"\s", "", caliber)
    caliber = "".join(
        [ch if ch.isupper() or ch.isdigit() or ch in ".,/| " else "" for ch in caliber]
    )
    return caliber


def _stringify_weight(weight: [int, float]) -> str:
    rnd_weight = round(weight, 1)
    if rnd_weight % 1 == 0:
        rnd_weight = int(rnd_weight)
    return f"{rnd_weight}grn"


def mkicon(caliber_txt: str,
           weight: [int, float],
           *,
           size: int = ICON_SIZE,
           font=FONT_PATH):
    _warn_unsupported_size(size)
    figlet = CustomFiglet(font=font)

    line_white = ' ' * size
    line_black = '#' * size
    caliber_txt = figlet.render_centered(_trunc_caliber(caliber_txt), width=size, height=size // 2 - 2)
    weight_txt = figlet.render_centered(_stringify_weight(weight), width=size, height=size // 2 - 2)
    string = line_white + caliber_txt + line_black + line_black + line_white + weight_txt
    string = string.replace('\n', '')
    buffer = bytearray()
    for line in batched(string, size):
        buffer += b"".join(WHITE if char == " " else BLACK for char in line) * 2
    return buffer


def join_icons(*icons: [bytes, bytearray]):
    return b"".join(icons)


def split_icons(b: [bytes, bytearray], *, size: int = ICON_SIZE) -> tuple[bytes, ...]:
    _warn_unsupported_size(size)
    chunk = size ** 2 * 2
    count = len(b) // chunk
    icons = (b[i * chunk: (i + 1) * chunk] for i in range(count))
    return tuple(icons)


def decode(b, *, size: int = ICON_SIZE):
    _warn_unsupported_size(size)

    if len(b) != size ** 2 * 2:
        raise ValueError("Unexpected icon size")

    img = Image.new("L", size=(size, size), color="white")
    px = img.load()

    for x in range(size):
        # skip each second line
        for y in range(0, size * 2, 2):
            px[x, y // 2] = 0 if b[size * y + x] > 127 else 255
    img = img.convert("RGB")
    return img


def encode(img, *, size: int = ICON_SIZE):
    _warn_unsupported_size(size)
    if img.size != (size, size):
        raise ValueError("Unexpected Image size")

    img = img.convert("L")
    px = img.load()
    buf = bytearray()

    for y in range(size):
        row = b"".join(WHITE if px[x, y] > 127 else BLACK for x in range(size))
        buf += row * 2  # repeat row twice
    return buf


def decode_all(*icons, size: int = ICON_SIZE):
    _warn_unsupported_size(size)
    b = join_icons(*icons)
    length = size ** 2 * 2
    if len(b) % length:
        raise ValueError("Unexpected icon size")
    count = len(b) // length

    img = Image.new("L", size=(size, size * count), color="white")
    px = img.load()

    for x in range(size):
        # skip each second line
        for y in range(0, size * 2 * count, 2):
            px[x, y // 2] = 0 if b[size * y + x] > 127 else 255
    img = img.convert("RGB")
    return img


def encode_all(*imgs: Image.Image, size: int = ICON_SIZE):
    _warn_unsupported_size(size)
    buf = bytearray()
    for img in imgs:
        w, h = img.size
        if w != size or h % size:
            raise ValueError("Unexpected Image size")
        count = h // size

        img = img.convert("L")
        px = img.load()

        for y in range(size * count):
            row = b"".join(WHITE if px[x, y] > 127 else BLACK for x in range(size))
            buf += row * 2  # repeat row twice
    return buf


if __name__ == "__main__":
    ic = mkicon("308WIN", 175)
    im = decode(ic)
    im.show()
    ic2 = encode(im)
    assert ic == ic2

    icons = tuple(mkicon("308WIN", 10.5 * i) for i in range(20))
    b_icons = join_icons(*icons)
    icons2 = split_icons(b_icons)
    assert icons == icons2

    icons_im = decode_all(b_icons)
    icons_im.show()
    icons3 = encode_all(icons_im)
    assert b_icons == icons3

    icons_im2 = decode_all(b_icons, b_icons)
    icons4 = encode_all(icons_im2)
    assert icons4 == b_icons + b_icons

    icons5 = decode_all(icons3, icons3)
    b_icons5 = encode_all(icons5)
    assert b_icons5 == b_icons + b_icons

    ic64 = mkicon("308WIN", 100.5, size=64)
    decode(ic64, size=64).show()
