#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Draw one editorial image that sums up the world's news of Tuesday 24 November 2026.

Everything is drawn here from Pillow primitives -- no downloaded or copied artwork --
so the file a reader sees on make.fun is generated in this session.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
W = H = 1024

# ---------------------------------------------------------------- typography


def pick(paths):
    for candidate in paths:
        if os.path.isfile(candidate):
            return candidate
    raise SystemExit("no font found among: " + ", ".join(paths))


REG = pick([
    "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
])
BOLD = pick([
    "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
])
BLACK = pick([
    "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
])


def face(size, weight="reg"):
    path = BLACK if weight == "black" else (BOLD if weight == "bold" else REG)
    return ImageFont.truetype(path, size)


def sized(text, ceiling, width, weight="reg"):
    """Largest size at or below `ceiling` whose text still fits `width`."""
    size = ceiling
    while size > 11:
        if face(size, weight).getlength(text) <= width:
            break
        size -= 1
    return face(size, weight)


# ---------------------------------------------------------------- palette
INK = (9, 18, 31)
INK_2 = (15, 31, 50)
PANEL = (21, 41, 64)
EDGE = (47, 74, 104)
RULE = (58, 90, 124)
AMBER = (246, 178, 49)
TEAL = (84, 199, 196)
CORAL = (232, 96, 88)
PAPER = (240, 244, 249)
MUTE = (158, 181, 206)

img = Image.new("RGB", (W, H), INK)
px = img.load()

# A slow vertical wash gives the flat colour some depth without any texture asset.
for y in range(H):
    t = y / H
    tone = tuple(int(INK[c] + (INK_2[c] - INK[c]) * t) for c in range(3))
    for x in range(W):
        px[x, y] = tone

d = ImageDraw.Draw(img)


def centred(text, y, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text(((W - (box[2] - box[0])) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 7], fill=AMBER)
d.rectangle([0, H - 7, W, H], fill=AMBER)

centred("THE DAY IN PICTURES", 24, face(21, "bold"), AMBER)
centred("TUESDAY 24 NOVEMBER 2026", 58, face(60, "black"), PAPER)
centred("Six stories the wires carried through the day", 138, face(22), MUTE)
d.line([(72, 170), (W - 72, 170)], fill=RULE, width=2)

# ---------------------------------------------------------------- icons


def plate(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(12, 27, 44), outline=EDGE, width=2)


def orbit(cx, cy, rx, ry, tilt=0):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=TEAL, width=2)


def rocket(cx, cy):
    plate(cx, cy, 44)
    # a blunt nose cone and two fins, pointing up-right
    d.polygon([(cx - 2, cy - 26), (cx + 14, cy + 8), (cx - 18, cy + 8)], fill=PAPER)
    d.rectangle([cx - 2, cy + 8, cx + 14, cy + 20], fill=(176, 196, 214))
    d.polygon([(cx - 20, cy + 10), (cx - 26, cy + 26), (cx - 8, cy + 18)], fill=CORAL)
    d.polygon([(cx + 16, cy + 10), (cx + 22, cy + 26), (cx + 10, cy + 18)], fill=CORAL)
    d.ellipse([cx + 4, cy - 4, cx + 16, cy + 8], outline=AMBER, width=2)
    for k in range(3):
        d.line([(cx - 4 + k * 7, cy + 24), (cx - 8 + k * 7, cy + 34)], fill=MUTE, width=2)
    # the station it is bound for
    d.arc([cx - 22, cy - 20, cx - 6, cy - 4], 200, 340, fill=TEAL, width=2)


def ballot(cx, cy):
    plate(cx, cy, 44)
    d.rounded_rectangle([cx - 24, cy - 20, cx + 16, cy + 22], 4, outline=PAPER, width=3)
    d.line([(cx - 24, cy - 6), (cx + 16, cy - 6)], fill=PAPER, width=2)
    d.line([(cx - 16, cy + 4), (cx + 8, cy + 4)], fill=MUTE, width=2)
    d.line([(cx - 16, cy + 12), (cx + 4, cy + 12)], fill=MUTE, width=2)
    # a marked slip going in
    d.polygon([(cx + 2, cy - 30), (cx + 18, cy - 30), (cx + 26, cy - 18), (cx + 10, cy - 18)], fill=AMBER)
    d.line([(cx + 6, cy - 26), (cx + 14, cy - 20)], fill=INK, width=2)


def chip(cx, cy):
    plate(cx, cy, 44)
    d.rounded_rectangle([cx - 16, cy - 16, cx + 16, cy + 16], 5, outline=TEAL, width=3)
    d.rounded_rectangle([cx - 7, cy - 7, cx + 7, cy + 7], 2, outline=TEAL, width=2)
    for off in (-14, 0, 14):
        d.line([(cx + off, cy - 24), (cx + off, cy - 16)], fill=TEAL, width=2)
        d.line([(cx + off, cy + 16), (cx + off, cy + 24)], fill=TEAL, width=2)
        d.line([(cx - 24, cy + off), (cx - 16, cy + off)], fill=TEAL, width=2)
        d.line([(cx + 16, cy + off), (cx + 24, cy + off)], fill=TEAL, width=2)
    d.arc([cx + 12, cy - 22, cx + 34, cy], 290, 60, fill=AMBER, width=3)


def hull(cx, cy):
    plate(cx, cy, 44)
    d.polygon([(cx - 30, cy + 8), (cx + 30, cy + 8), (cx + 20, cy + 22), (cx - 22, cy + 22)], fill=(168, 190, 210))
    d.rectangle([cx - 12, cy - 6, cx + 8, cy + 8], fill=(196, 214, 228))
    d.rectangle([cx - 4, cy - 18, cx + 3, cy - 6], fill=(214, 226, 236))
    for i in range(4):
        y = cy - 22 + i * 6
        d.line([(cx + 14, y), (cx + 20, y)], fill=CORAL, width=2)
    # a drone skimming the water beside it
    d.polygon([(cx + 12, cy + 20), (cx + 30, cy + 20), (cx + 27, cy + 25), (cx + 15, cy + 25)], fill=PAPER)
    d.line([(cx + 21, cy + 20), (cx + 21, cy + 13)], fill=TEAL, width=2)
    for k in range(-2, 3):
        d.line([(cx - 26 + k * 4, cy + 30), (cx - 30 + k * 4, cy + 34)], fill=EDGE, width=2)


def scales(cx, cy):
    plate(cx, cy, 44)
    d.line([(cx, cy - 24), (cx, cy + 22)], fill=PAPER, width=3)
    d.line([(cx - 26, cy - 14), (cx + 26, cy - 14)], fill=PAPER, width=3)
    for sign in (-1, 1):
        x = cx + sign * 24
        d.line([(x, cy - 14), (x - 9, cy + 6)], fill=MUTE, width=2)
        d.line([(x, cy - 14), (x + 9, cy + 6)], fill=MUTE, width=2)
        d.arc([x - 13, cy - 2, x + 13, cy + 18], 0, 180, fill=TEAL if sign < 0 else CORAL, width=3)
    d.polygon([(cx - 8, cy + 26), (cx + 8, cy + 26), (cx, cy + 16)], fill=AMBER)


def flame(cx, cy):
    plate(cx, cy, 44)
    d.rounded_rectangle([cx - 18, cy - 6, cx + 18, cy + 24], 4, outline=AMBER, width=3)
    d.line([(cx - 18, cy + 8), (cx + 18, cy + 8)], fill=AMBER, width=2)
    d.polygon([(cx - 6, cy - 8), (cx + 8, cy - 8), (cx + 2, cy - 28), (cx - 12, cy - 18)], fill=CORAL)
    d.arc([cx - 26, cy - 30, cx - 14, cy - 18], 90, 200, fill=TEAL, width=2)
    d.arc([cx + 14, cy - 30, cx + 26, cy - 18], -20, 90, fill=TEAL, width=2)


ICONS = [rocket, ballot, chip, hull, scales, flame]

# ---------------------------------------------------------------- cards
STORIES = [
    ("SPACE", "SHENZHOU-24 LIFTOFF",
     "China lifts off with the first foreign astronaut",
     "a Pakistani specialist heads to the station"),
    ("US POLITICS", "DEMOCRATS TAKE CONGRESS",
     "Both chambers fall in the 2026 midterms, a House",
     "majority not seen since 1992"),
    ("BUSINESS", "NVIDIA CEO REINSTATED",
     "Jensen Huang returns as chief executive after",
     "the White House pressed the board"),
    ("UKRAINE WAR", "LIBYA PROTESTS KIEV",
     "Tripoli demands an account of the drone strikes",
     "that sank Russian ships at Benghazi"),
    ("MIDDLE EAST", "IRAN VOWS TO END BLOCKADE",
     "Tehran vows every means as Washington cuts its",
     "last financial lifeline"),
    ("CLIMATE", "COP31 CLOSES WITH NO DEAL",
     "Antalya ends two weeks with no pact on fossil",
     "fuels; the UN sees no ambiguity"),
]

MARGIN = 44
GUTTER = 14
CARD_W = (W - 2 * MARGIN - GUTTER) // 2
CARD_H = 228
TOP = 186

for index, (kicker, head, detail_a, detail_b) in enumerate(STORIES):
    col, row = index % 2, index // 2
    x = MARGIN + col * (CARD_W + GUTTER)
    y = TOP + row * (CARD_H + GUTTER)
    d.rounded_rectangle([x, y, x + CARD_W, y + CARD_H], 16, fill=PANEL, outline=EDGE, width=2)
    d.rounded_rectangle([x, y, x + 7, y + CARD_H], 4, fill=AMBER if index % 2 == 0 else TEAL)

    cx, cy = x + 60, y + CARD_H // 2
    ICONS[index](cx, cy)

    text_x = x + 118
    d.text((text_x, y + 20), kicker, font=face(17, "bold"), fill=AMBER)
    d.text((text_x, y + 50), head, font=sized(head, 24, CARD_W - 142, "bold"), fill=PAPER)
    d.text((text_x, y + 98), detail_a, font=sized(detail_a, 15, CARD_W - 142), fill=MUTE)
    d.text((text_x, y + 123), detail_b, font=sized(detail_b, 15, CARD_W - 142), fill=MUTE)

    d.line([(text_x, y + CARD_H - 28), (x + CARD_W - 20, y + CARD_H - 28)], fill=EDGE, width=1)
    d.text((text_x, y + CARD_H - 23), "%02d / 06" % (index + 1), font=face(13, "bold"), fill=(104, 132, 162))

# ---------------------------------------------------------------- ticker
ticker_y = TOP + 3 * (CARD_H + GUTTER) + 6
d.rounded_rectangle([MARGIN, ticker_y, W - MARGIN, ticker_y + 54], 12, fill=(12, 27, 44), outline=EDGE, width=1)
d.text((MARGIN + 18, ticker_y + 8), "ALSO CARRIED", font=face(15, "bold"), fill=AMBER)
also = ("Gukesh opens his title defence against Sindarov  ·  South Sudan raids kill 24 civilians  "
        " ·  Delta outage delays more than 1,600 flights")
d.text((MARGIN + 18, ticker_y + 30), also, font=sized(also, 15, W - 2 * MARGIN - 36), fill=MUTE)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
