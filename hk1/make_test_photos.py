"""Makes three test photos to send to a box: what the wallpaper and the screensaver show."""
import os

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "fotos-teste")
W, H = 1920, 1080


def gradient(top, bottom, path):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        ))
    img.save(path, quality=92)
    print("wrote", path)


def main():
    os.makedirs(OUT, exist_ok=True)
    # A deep blue night, the way the app's own background looks.
    gradient((8, 12, 38), (26, 52, 104), os.path.join(OUT, "noite.jpg"))
    # A warm dusk.
    gradient((92, 34, 62), (222, 122, 74), os.path.join(OUT, "entardecer.jpg"))
    # A cold morning.
    gradient((18, 48, 72), (108, 156, 186), os.path.join(OUT, "manha.jpg"))


if __name__ == "__main__":
    main()
