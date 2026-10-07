#!/usr/bin/env python3
"""Rasterize the same geometry as web/favicon.svg into web/favicon.ico.

Coordinates are the 32x32 viewBox. Each size is drawn at 8x and downsampled.
Paths are relative to this file. Optional: --preview PATH writes a 256 PNG.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw

# x, y, w, h, rx, fill — matches favicon.svg
SHAPES = (
    (0, 0, 32, 32, 6, (0x2F, 0x6F, 0xB3, 255)),
    (5, 18, 4, 8, 1, (0xFF, 0xFF, 0xFF, 255)),
    (11, 14, 4, 12, 1, (0xFF, 0xFF, 0xFF, 255)),
    (17, 10, 4, 16, 1, (0xFF, 0xFF, 0xFF, 255)),
    (23, 6, 4, 20, 1, (0xFF, 0xFF, 0xFF, 255)),
)
SIZES = (16, 32, 48)
SUPERSAMPLE = 8

WEB = Path(__file__).resolve().parent.parent
ICO_PATH = WEB / "favicon.ico"


def render(size, supersample=SUPERSAMPLE):
    """Draw viewBox shapes scaled to size, supersampled, then downsampled."""
    scale = (size / 32) * supersample
    canvas = size * supersample
    image = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for x, y, w, h, rx, fill in SHAPES:
        # Pillow's box is inclusive, so the far edge is one pixel inside x+w.
        box = (x * scale, y * scale, (x + w) * scale - 1, (y + h) * scale - 1)
        draw.rounded_rectangle(box, radius=rx * scale, fill=fill)
    if supersample != 1:
        image = image.resize((size, size), Image.Resampling.LANCZOS)
    return image


def write_ico(path=ICO_PATH):
    frames = [render(size) for size in SIZES]
    # Primary image must be the largest; smaller sizes are matched exactly.
    frames[-1].save(
        path,
        format="ICO",
        sizes=[(size, size) for size in SIZES],
        append_images=frames[:-1],
    )
    return path


def main():
    parser = argparse.ArgumentParser(description="Write web/favicon.ico from favicon.svg geometry.")
    parser.add_argument("--preview", metavar="PATH", help="also write a 256x256 PNG to PATH")
    args = parser.parse_args()
    write_ico()
    if args.preview:
        render(256).save(args.preview, format="PNG")


if __name__ == "__main__":
    main()
