from itertools import islice
from PIL import Image
import warnings

TRASHOLD = 127
GLYPH_SIZE = 16
ICON_SIZE = 32


def _warn_unsupported_size(size: int):
    if size not in {GLYPH_SIZE, ICON_SIZE}:
        warnings.warn(
            f"Using a size different from {GLYPH_SIZE} for a font or {ICON_SIZE} for an icon may cause unexpected behavior.",
            UserWarning,
            stacklevel=2,
        )


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def encode_glyphs(*imgs: Image.Image, size: int) -> bytearray:
    _warn_unsupported_size(size)
    buffer = bytearray()
    gw, gh = size, size * 2
    for img in imgs:
        img = img.convert("L")
        w, h = img.size
        if w != gw or h % gw:
            raise Exception(
                "Image width must be 16 pixels and height a quant of 16 pixels"
            )
        px = img.load()
        for y in range(h):
            line = bytearray()
            for x in range(w):
                line += b"\xc0" if px[x, y] > TRASHOLD else b"\x00"
            buffer += line * 2  # double icon line
            if y % gw == 0:  # mark icon start
                buffer[y * gh] += 1
    return buffer


def decode_glyphs(*glyphs: [bytes, bytearray], size: int) -> Image.Image:
    _warn_unsupported_size(size)
    buffer = b"".join(glyphs)
    gw, gh = size, size * 2
    count = len(buffer) // (gw * gh)
    if count < 1:
        raise Exception("glyphs count must be at least 1")

    img = Image.new("L", (gw, count * gw))
    px = img.load()

    x, y = 0, 0
    icons = batched(buffer, gw * gh)
    for ic in icons:
        lines = [line[:gw] for line in batched(ic, gh)]
        for l in lines:
            for b in l:
                px[x, y] = 255 if b > TRASHOLD else 0
                x += 1
            x = 0
            y += 1
    img = img.convert("RGB")
    return img


if __name__ == "__main__":
    with open(r"fonts/cyrillic.bin", "rb") as fp:
        d = fp.read()
        im = decode_glyphs(d, size=GLYPH_SIZE)
        im.save("assets/cyrillic.bmp")
        gl = encode_glyphs(im, size=GLYPH_SIZE)
        assert gl == d

    with open(r"fonts/latin.bin", "rb") as fp:
        d = fp.read()
        im = decode_glyphs(d, size=GLYPH_SIZE)
        im.save("assets/latin.bmp")
        gl = encode_glyphs(im, size=GLYPH_SIZE)
        # assert gl == d
        for i, j in enumerate(d):
            if gl[i] != j:
                print(i, i // (32 * 16), gl[i], j)

