"""Draws the "Free memory" icon: a broom sweeping, as the Material Symbols' "cleaning_services" does.

The Material font isn't on this machine (tools/make_symbols.py needs it), so the shape is drawn here,
in the same style as the other symbols: white, with the transparency the app expects.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

SIZE = 172
OUT = os.path.join(os.path.dirname(__file__), "..", "app", "assets", "symbols", "memory.png")


def main():
    # A supersampled canvas, so the edges come out smooth.
    s = 4
    w = SIZE * s
    img = Image.new("RGBA", (w, w), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    # The handle: a diagonal stick, from the top right to the middle.
    x0, y0 = int(w * 0.72), int(w * 0.16)
    x1, y1 = int(w * 0.46), int(w * 0.52)
    d.line([(x0, y0), (x1, y1)], fill=(255, 255, 255, 255), width=int(w * 0.075))

    # The brush: the head of the broom, a fan of bristles below the handle.
    bx, by = int(w * 0.44), int(w * 0.54)
    d.polygon(
        [
            (bx - int(w * 0.02), by - int(w * 0.02)),
            (bx + int(w * 0.06), by - int(w * 0.05)),
            (bx + int(w * 0.19), by + int(w * 0.30)),
            (bx - int(w * 0.13), by + int(w * 0.30)),
        ],
        fill=(255, 255, 255, 255),
    )
    # The bristles: the gaps between them.
    for i in range(3):
        t = (i + 1) / 4
        xa = bx - int(w * 0.11) + int(w * 0.30 * t)
        d.line(
            [(xa, by + int(w * 0.06)), (xa + int(w * 0.03), by + int(w * 0.30))],
            fill=(255, 255, 255, 0),
            width=int(w * 0.018),
        )

    # The swept line: the dust the broom takes away.
    d.line(
        [(int(w * 0.14), int(w * 0.86)), (int(w * 0.62), int(w * 0.86))],
        fill=(255, 255, 255, 160),
        width=int(w * 0.035),
    )

    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    # The app reads the alpha as the shape (Symbols.get), so the colour must be white.
    alpha = img.split()[3]
    img = Image.merge("RGBA", (Image.new("L", (SIZE, SIZE), 255),) * 3 + (alpha,))
    img.save(OUT)
    print("wrote", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
