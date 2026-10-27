"""App icons for installation (PNG 192 / 512, and 512 'maskable' with a safe zone): same drawing as preventif.ico."""
import math
import pathlib
import sys

from PIL import Image

BG = (15, 95, 110)
WHITE = (255, 255, 255)
AMBER = (240, 181, 61)


def sd_round_rect(x, y, x0, y0, x1, y1, r):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    qx, qy = abs(x - cx) - hx, abs(y - cy) - hy
    return math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - r


def sd_segment(x, y, ax, ay, bx, by):
    px, py, vx, vy = x - ax, y - ay, bx - ax, by - ay
    t = max(0, min(1, (px * vx + py * vy) / (vx * vx + vy * vy)))
    return math.hypot(px - vx * t, py - vy * t)


def cover(d):
    return max(0.0, min(1.0, 0.5 - d))


def draw(n, maskable):
    img = Image.new("RGBA", (n, n))
    k = n / 256  # drawing designed on a 256 grid
    g = 0.72 if maskable else 1.0  # maskable: glyph inside the 80 % safe circle, full-bleed background
    pix = img.load()
    for j in range(n):
        for i in range(n):
            x, y = (i + 0.5) / k, (j + 0.5) / k
            a = 1.0 if maskable else cover(sd_round_rect(x, y, 8, 8, 248, 248, 54) * k)
            gx, gy = 128 + (x - 128) / g, 128 + (y - 128) / g
            col = list(BG)
            d = abs(sd_round_rect(gx, gy, 58, 72, 198, 206, 22)) - 7
            d = min(d, sd_segment(gx, gy, 58, 114, 198, 114) - 7)
            d = min(d, sd_segment(gx, gy, 98, 50, 98, 88) - 7, sd_segment(gx, gy, 158, 50, 158, 88) - 7)
            w = cover(d * k * g)
            col = [c * (1 - w) + wc * w for c, wc in zip(col, WHITE)]
            dc = min(sd_segment(gx, gy, 98, 160, 122, 184), sd_segment(gx, gy, 122, 184, 164, 140)) - 9
            c2 = cover(dc * k * g)
            col = [c * (1 - c2) + kc * c2 for c, kc in zip(col, AMBER)]
            pix[i, j] = (round(col[0]), round(col[1]), round(col[2]), round(a * 255))
    return img


out = pathlib.Path(sys.argv[1])
big = draw(512, False)
big.save(out / "icon-512.png")
big.resize((192, 192), Image.LANCZOS).save(out / "icon-192.png")
draw(512, True).save(out / "icon-maskable-512.png")
print("icônes :", sorted(p.name for p in out.glob("icon-*.png")))
