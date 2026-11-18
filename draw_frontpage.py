#!/usr/bin/env python3
"""Draw the v2 front page for 18 November 2026 with PIL only.

Deterministic: no network, no randomness, no wall clock. Writes
entry.png (1024x1024) next to this script and prints its size.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024
PAPER = "#f7f3ea"
INK = "#111111"
RED = "#b91c1c"
NAVY = "#1e3a5f"
TEAL = "#0f766e"
SKY = "#dbe7f3"
BROWN = "#8b5a2b"
ORANGE = "#f97316"
YELLOW = "#facc15"
GREY = "#777777"
PINK = "#ffb3c1"
DARKPINK = "#880e4f"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tsize(fnt, text):
    """Pixel (width, height) of text in font fnt (Pillow 10: no getsize)."""
    box = fnt.getbbox(text)
    return box[2] - box[0], box[3] - box[1]


def twidth(fnt, text):
    return tsize(fnt, text)[0]


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if twidth(fnt, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, outer, inner, points=12):
    """Star polygon points (12-point burst)."""
    pts = []
    for i in range(2 * points):
        r = outer if i % 2 == 0 else inner
        a = i * math.pi / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def kicker(d, x, y, text, fnt):
    """Red chip with white bold text; returns (chip_w, chip_h)."""
    w, h = tsize(fnt, text)
    pad_x, pad_y = 10, 6
    cw, ch = w + 2 * pad_x, h + 2 * pad_y
    d.rectangle([x, y, x + cw, y + ch], fill=RED)
    d.text((x + pad_x, y + pad_y), text, font=fnt, fill="white")
    return cw, ch


def drone(d, cx, cy, s=13, color=NAVY):
    """Tiny drone silhouette: long body, short tail, rotor line on top."""
    d.line([cx - s, cy, cx + s, cy], fill=color, width=3)
    d.line([cx, cy, cx, cy + 7], fill=color, width=2)
    d.line([cx - s + 2, cy - 8, cx + s - 2, cy - 8], fill=color, width=1)


def headline_block(d, x, y, max_w, text, size, gap=6):
    """Draw a wrapped serif-bold headline; returns y below the block."""
    fnt = font(SERIF, size)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=INK)
        y += tsize(fnt, line)[1] + gap
    return y


def body_block(d, x, y, max_w, text, size, gap=4):
    """Draw a wrapped sans body; returns y below the block."""
    fnt = font(SANS, size)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=INK)
        y += tsize(fnt, line)[1] + gap
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.line([0, 8, W, 8], fill=INK, width=2)
fk = font(SANSB, 20)
kw, _ = tsize(fk, "THE WORLD IN ONE PAGE")
d.text(((W - kw) // 2, 20), "THE WORLD IN ONE PAGE", font=fk, fill=INK)
ft = font(SERIF, 64)
tw, _ = tsize(ft, "THE WORLD")
d.text(((W - tw) // 2, 38), "THE WORLD", font=ft, fill=INK)
d.line([0, 112, W, 112], fill=INK, width=2)

fd = font(SANSB, 20)
d.text((32, 122), "WEDNESDAY 18 NOVEMBER 2026", font=fd, fill=INK)
rd = "EIGHT STORIES THAT DEFINED THE DAY"
rw, _ = tsize(fd, rd)
d.text((992 - rw, 122), rd, font=fd, fill=INK)
d.line([0, 150, W, 150], fill=INK, width=2)
d.line([0, 154, W, 154], fill=RED, width=2)

# ---------------------------------------------------------------- lead
LY0, LY1 = 164, 448
fks = font(SANSB, 20)
kicker(d, 32, 172, "GULF STRIKES", fks)
y = headline_block(d, 32, 210, 568, "U.S. HITS IRAN MISSILE SITE AS DRONES STRIKE GULF", 40)
y = body_block(d, 32, y + 8, 568,
               "Jets strike a Revolutionary Guard launch site on Qeshm Island; "
               "Iran fires drones at Bahrain and Kuwait.", 21)

# lead illustration: sky, sea, island, explosion, drones
IX0, IX1, IY0, IY1 = 624, 992, 164, 452
SEA = IY1 - 92
d.rectangle([IX0, IY0, IX1, SEA], fill=SKY)
d.rectangle([IX0, SEA, IX1, IY1], fill=NAVY)
d.line([IX0, SEA, IX1, SEA], fill="white", width=1)
# wave dashes
for wx in (660, 740, 830, 920):
    d.line([wx, SEA + 34, wx + 44, SEA + 34], fill="#7fa8c9", width=2)
    d.line([wx + 18, SEA + 62, wx + 62, SEA + 62], fill="#7fa8c9", width=2)
# island
d.ellipse([768, SEA - 16, 848, SEA + 16], fill=BROWN)
# smoke rings first (behind the burst), then the layered burst
ECX, ECY = 808, SEA - 62
for r in (24, 33, 42):
    d.ellipse([ECX - r, ECY - 8 - r, ECX + r, ECY - 8 + r], outline=GREY, width=2)
# explosion: big layered burst above the island
d.polygon(star(ECX, ECY, 52, 22), fill=ORANGE)
d.polygon(star(ECX, ECY, 34, 14), fill=RED)
d.polygon(star(ECX, ECY, 18, 8), fill=YELLOW)
# drones inside the panel
drone(d, 668, 208)
drone(d, 748, 188)
drone(d, 884, 206)
drone(d, 944, 186)

d.line([0, 448, W, 448], fill=INK, width=1)

# ---------------------------------------------------------------- second row
RY0, RY1 = 458, 726
d.line([512, RY0, 512, RY1], fill=INK, width=1)

# left panel: Kerch bridge
y = RY0 + 10
kicker(d, 32, y, "UKRAINE WAR", fks)
y = headline_block(d, 32, y + 38, 464, "BRIDGE TO CRIMEA FALLS", 30)
y = body_block(d, 32, y + 4, 464,
               "Ukrainian drones and missiles partly collapse the Kerch bridge; "
               "one arch drops into the strait.", 18)
# bridge illustration strip
BX0, BX1, BY0, BY1 = 32, 496, RY1 - 92, RY1 - 8
d.rectangle([BX0, BY0, BX1, BY1], fill=SKY)
d.rectangle([BX0, BY0 + 62, BX1, BY1], fill="#2563eb")
d.line([BX0, BY0 + 62, BX1, BY0 + 62], fill="white", width=1)
deck_y = BY0 + 28
# deck: solid on the left, broken off on the right
d.rectangle([BX0 + 16, deck_y, BX0 + 296, deck_y + 8], fill="#4b5563")
d.rectangle([BX0 + 384, deck_y, BX1 - 16, deck_y + 8], fill="#4b5563")
# left arch intact: tall cap under the deck, with two pillars into the water
d.arc([BX0 + 60, deck_y - 28, BX0 + 180, deck_y + 28], 180, 360, fill="#4b5563", width=6)
d.line([BX0 + 60, deck_y + 24, BX0 + 60, BY0 + 74], fill="#4b5563", width=5)
d.line([BX0 + 180, deck_y + 24, BX0 + 180, BY0 + 74], fill="#4b5563", width=5)
# fallen deck segment tilted into the water, plus a splash starburst
d.line([BX0 + 300, deck_y + 6, BX0 + 356, BY0 + 66], fill="#4b5563", width=7)
d.polygon(star(BX0 + 366, BY0 + 60, 16, 7), fill="white")

# right panel: Shenzhen summit
y = RY0 + 10
kicker(d, 528, y, "SHENZHEN SUMMIT", fks)
y = headline_block(d, 528, y + 38, 464, "XI HOSTS PUTIN AS TRUMP SUMMIT LOOMS", 30)
y = body_block(d, 528, y + 4, 464,
               "Xi and Putin meet in Shenzhen; the first Trump-Xi-Putin "
               "trilateral is set for Thursday.", 18)
# skyline illustration strip
SX0, SX1, SY0, SY1 = 528, 992, RY1 - 92, RY1 - 8
d.rectangle([SX0, SY0, SX1, SY1], fill=SKY)
# red sun first, in the gap between tower groups, towers in front of it
d.ellipse([SX0 + 118, SY0 + 12, SX0 + 166, SY0 + 60], fill=RED)
towers = [(SX0 + 12, 34), (SX0 + 52, 48), (SX0 + 186, 40), (SX0 + 226, 30)]
for tx, th in towers:
    d.rectangle([tx, SY1 - th, tx + 32, SY1], fill=NAVY)
# pointed roof on the tallest tower
d.polygon([(SX0 + 52, SY1 - 48), (SX0 + 68, SY1 - 62), (SX0 + 84, SY1 - 48)], fill=NAVY)
# three flagpoles with flags, in front of the skyline
for i, (fx, flag) in enumerate([(SX0 + 268, "china"), (SX0 + 322, "russia"), (SX0 + 376, "usa")]):
    d.line([fx, SY0 + 10, fx, SY1], fill=INK, width=2)
    if flag == "china":
        d.rectangle([fx, SY0 + 10, fx + 40, SY0 + 34], fill=RED)
        d.ellipse([fx + 6, SY0 + 16, fx + 10, SY0 + 20], fill=YELLOW)
    elif flag == "russia":
        d.rectangle([fx, SY0 + 10, fx + 40, SY0 + 18], fill="white")
        d.rectangle([fx, SY0 + 18, fx + 40, SY0 + 26], fill="#2563eb")
        d.rectangle([fx, SY0 + 26, fx + 40, SY0 + 34], fill=RED)
    else:
        for s in range(4):
            d.rectangle([fx, SY0 + 10 + s * 6, fx + 40, SY0 + 16 + s * 6],
                        fill=RED if s % 2 == 0 else "white")
        d.rectangle([fx, SY0 + 10, fx + 16, SY0 + 22], fill=NAVY)

d.line([0, RY1, W, RY1], fill=INK, width=1)

# ---------------------------------------------------------------- third row
TY0, TY1 = 736, 926
d.line([352, TY0, 352, TY1], fill=INK, width=1)
d.line([672, TY0, 672, TY1], fill=INK, width=1)


def small_icon_ballot(d, cx, cy):
    d.rectangle([cx - 24, cy - 14, cx + 24, cy + 20], fill=NAVY)
    d.rectangle([cx - 12, cy - 26, cx + 12, cy + 2], fill="white")
    d.line([cx - 8, cy - 2, cx - 2, cy + 6, cx + 12, cy - 12], fill=RED, width=3)


def small_icon_virus(d, cx, cy):
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=PINK)
    for k in range(8):
        a = k * math.pi / 4
        x2 = cx + 28 * math.cos(a)
        y2 = cy + 28 * math.sin(a)
        d.line([cx, cy, x2, y2], fill=DARKPINK, width=2)
        d.ellipse([x2 - 2, y2 - 2, x2 + 2, y2 + 2], fill=DARKPINK)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=DARKPINK)


def small_icon_cyclone(d, cx, cy):
    for r in (10, 18, 26):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=TEAL, width=3)
    d.ellipse([cx - 12, cy + 14, cx + 12, cy + 24], fill=BROWN)


def column(x0, x1, kicker_text, head, body, icon):
    y = TY0 + 8
    cw, ch = kicker(d, x0, y, kicker_text, fks)
    icon(d, x1 - 28, y + ch // 2)
    y = headline_block(d, x0, y + ch + 8, x1 - x0, head, 27)
    y = body_block(d, x0, y + 4, x1 - x0, body, 18)
    return y


column(32, 336, "ALASKA", "PELTOLA WINS ALASKA",
       "Democrat Mary Peltola takes the Senate seat; Democrats reach 56 seats.",
       small_icon_ballot)
column(368, 656, "EBOLA IN CONGO", "OUTBREAK PASSES 11,000",
       "More than 11,000 cases and 5,400 deaths in DR Congo; children hit hardest.",
       small_icon_virus)
column(688, 992, "CYCLONE XAVIER", "CYCLONE SLAMS COOK ISLANDS",
       "The season's fiercest Category 5 storm strikes the Northern Cook Islands.",
       small_icon_cyclone)

# ---------------------------------------------------------------- also today
d.line([0, 934, W, 934], fill=INK, width=1)
fb = font(SANSB, 18)
d.text((32, 942), "ALSO TODAY", font=fb, fill=RED)
fi = font(SANS, 18)
d.text((178, 942),
       "U.S. LOSES MEASLES-FREE STATUS — 5,400 cases, first time in 26 years.",
       font=fi, fill=INK)
d.text((32, 966),
       "RUSSIAN MILITARY PLANE CRASHES — 19 dead in Siberia.",
       font=fi, fill=INK)

# ---------------------------------------------------------------- footer
d.line([0, 992, W, 992], fill=INK, width=1)
ff = font(SANS, 16)
d.text((32, 996),
       "Wire reports from 18 November 2026 — U.S., Gulf, Ukraine, China, Alaska, DR Congo.",
       font=ff, fill=INK)
fr = font(SANSB, 16)
rw, _ = tsize(fr, "THE WORLD IN ONE PAGE")
d.text((992 - rw, 996), "THE WORLD IN ONE PAGE", font=fr, fill=RED)

img.save(OUT, format="PNG")
print("Saved %s (%d bytes, %dx%d)" % (OUT, OUT.stat().st_size, W, H))
