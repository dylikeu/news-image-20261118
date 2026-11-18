#!/usr/bin/env python3
"""Render the news-summary infographic for make.fun news-image-20261118.

One page, 1024x1024 PNG: the world's news of Wednesday 18 November 2026.
Stories verified against live reporting on 18 Nov 2026 (Just Security Early
Edition, Open Chronicle, Horizon, OneTurn, Zark News).
Deterministic output: same bytes every run (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = (250, 246, 238)
NAVY = (15, 36, 64)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
INK = (20, 33, 61)
MUTED = (91, 100, 114)
TILE = (255, 255, 255)
BORDER = (227, 220, 203)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
f_title = font(F_SERIF_B, 62)
d.text((W // 2, 30), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255), anchor="ma")
f_date = font(F_SANS_B, 27)
d.text((W // 2, 102), "WEDNESDAY,  18  NOVEMBER  2026", font=f_date, fill=GOLD, anchor="ma")

# ---- lead story ----
f_kick = font(F_SANS_B, 21)
d.text((24, 168), "LEAD STORY  ·  THE GULF", font=f_kick, fill=RED, anchor="la")
f_head = font(F_SERIF_B, 56)
d.text((24, 196), "U.S. STRIKES IRAN,", font=f_head, fill=INK, anchor="la")
d.text((24, 258), "TEHRAN HITS BACK", font=f_head, fill=INK, anchor="la")
f_sub = font(F_SANS, 26)
sub = ("U.S. jets hit a Revolutionary Guard missile site on Qeshm Island. "
       "Iran answered with strikes on U.S. bases in Bahrain and Kuwait.")
for i, line in enumerate(wrap(d, sub, f_sub, W - 48)):
    d.text((24, 326 + i * 34), line, font=f_sub, fill=MUTED, anchor="la")
d.line([24, 442, W - 24, 442], fill=BORDER, width=2)

# ---- story tiles: 2 cols x 3 rows ----
stories = [
    ("SUMMIT · SHENZHEN", "Xi hosts Putin in Shenzhen",
     "Trilateral talks with Trump set for Thursday at APEC."),
    ("UKRAINE", "Kerch Bridge hit again",
     "Part of the road span collapses into the strait."),
    ("UNITED STATES", "Peltola flips Alaska",
     "Democrats take a 56–44 Senate majority."),
    ("HEALTH", "U.S. loses measles-free status",
     "5,412 cases in 2026, the most since 1991."),
    ("AFRICA", "Ebola passes 11,000 cases",
     "Congo outbreak is the second-largest on record."),
    ("SPACE", "Voyager 1, one light-day out",
     "First human-made object 16 billion miles from Earth."),
]
f_tile_kick = font(F_SANS_B, 19)
f_tile_head = font(F_SERIF_B, 27)
f_tile_body = font(F_SANS, 21)
cols, rows = 2, 3
gx, gy = 20, 458
cw, ch = 482, 152
gapx, gapy = 20, 12
for idx, (kick, head, body) in enumerate(stories):
    r, c = divmod(idx, cols)
    x0 = gx + c * (cw + gapx)
    y0 = gy + r * (ch + gapy)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=TILE, outline=BORDER, width=2)
    d.text((x0 + 16, y0 + 12), kick, font=f_tile_kick, fill=RED, anchor="la")
    hl = wrap(d, head, f_tile_head, cw - 32)
    for i, line in enumerate(hl[:2]):
        d.text((x0 + 16, y0 + 40 + i * 33), line, font=f_tile_head, fill=INK, anchor="la")
    bl = wrap(d, body, f_tile_body, cw - 32)
    for i, line in enumerate(bl[:2]):
        d.text((x0 + 16, y0 + 98 + i * 26), line, font=f_tile_body, fill=MUTED, anchor="la")

# ---- footer ----
d.rectangle([0, 962, W, H], fill=NAVY)
f_foot = font(F_SANS_B, 21)
d.text((W // 2, 978), "S&P 500  −1.03%   ·   GOLD $3,775   ·   BRENT $91.55",
       font=f_foot, fill=(255, 255, 255), anchor="ma")

img.save(os.path.join(HERE, "news.png"), "PNG", optimize=True)
print("saved news.png")
