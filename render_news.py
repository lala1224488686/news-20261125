#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page (1024x1024 PNG).

A broadsheet front page for Wednesday 25 November 2026: masthead, a hero
story on the Strait of Hormuz tanker attacks with a drawn illustration,
a two-by-two grid of the day's other big stories, and a bottom band of
three short items. Pure Pillow, no network, fully deterministic.

Stories (all reported on 25 November 2026):
- IRGC: two oil tankers struck naval mines in the Strait of Hormuz,
  exploded and caught fire (Just Security / AP).
- Houthis attack Saudi Arabia's Ras Tanura refinery; a Riyadh skyscraper
  is hit again, 11 people injured (SCMP / AP).
- Israeli strike in Gaza kills Hamas security chief Mohammad Abuelouf,
  his wife and two children (SCMP).
- US federal court finds Huawei guilty of conspiracy to steal trade
  secrets and bank fraud (Just Security).
- China's Shenzhou-24 launches with a Pakistani national, the first
  foreign astronaut bound for the Tiangong station (Reuters).
- Solomon Islands and Australia sign a treaty barring any foreign
  military base (AFP).
- An unclassified CIA system is breached (SCMP).
- COP31 climate talks end without agreement; Pope Leo XIV voices
  concern (AP).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (18, 18, 18)
MUTED = (96, 92, 82)
RED = (168, 32, 28)
NAVY = (28, 52, 96)
TEAL = (12, 110, 108)
GOLD = (186, 140, 24)
ORANGE = (208, 104, 16)
PURPLE = (92, 60, 134)
SEA = (24, 68, 104)
SEA_DARK = (16, 48, 76)
FLAME = (232, 122, 24)
FLAME_Y = (244, 190, 60)
RULE = (18, 18, 18)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, spacing=5):
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x0, x1, y, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, color):
    draw.text((x, y), text, font=SANS_B(15), fill=color)
    return y + 22


# ---------------- hero illustration: tankers burning in the strait -------
def draw_strait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA_DARK)
    # hazy sky band
    d.rectangle([x, y, x + w, y + 78], fill=(214, 176, 120))
    d.ellipse([x + w - 96, y + 12, x + w - 36, y + 72], fill=(244, 196, 90))
    # distant shore
    d.polygon([(x, y + 78), (x + w // 3, y + 52), (x + 2 * w // 3, y + 80),
               (x + w, y + 58), (x + w, y + 78)], fill=(120, 96, 66))
    # sea
    d.rectangle([x, y + 78, x + w, y + h], fill=SEA)
    for i, yy in enumerate(range(y + 96, y + h - 8, 26)):
        d.line([(x + 14 + (i % 3) * 8, yy), (x + w - 20 - (i % 2) * 10, yy)],
               fill=(70, 130, 175), width=2)
    # tanker 1 (left, listing)
    tx, ty, tw = x + 26, y + h - 118, 190
    d.polygon([(tx, ty + 34), (tx + tw, ty + 34), (tx + tw - 18, ty + 62),
               (tx + 16, ty + 62)], fill=(30, 30, 32))
    d.rectangle([tx + 30, ty + 6, tx + 78, ty + 34], fill=(196, 58, 40))
    d.rectangle([tx + 96, ty + 12, tx + 150, ty + 34], fill=(232, 232, 228))
    d.line([(tx + 120, ty - 16), (tx + 120, ty + 12)], fill=(232, 232, 228), width=4)
    # flames over tanker 1
    for fx, fh in ((tx + 44, 66), (tx + 66, 84), (tx + 92, 60), (tx + 118, 72)):
        d.polygon([(fx - 16, ty + 8), (fx, ty + 8 - fh), (fx + 16, ty + 8)],
                  fill=FLAME)
        d.polygon([(fx - 8, ty + 8), (fx, ty + 8 - fh // 2), (fx + 8, ty + 8)],
                  fill=FLAME_Y)
    # smoke
    for sx, sy, sr in ((tx + 60, ty - 52, 20), (tx + 92, ty - 74, 26),
                       (tx + 128, ty - 58, 18)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(58, 58, 60))
    # tanker 2 (right, smaller, on fire at the bow)
    ux, uy, uw = x + w - 216, y + h - 96, 160
    d.polygon([(ux, uy + 28), (ux + uw, uy + 28), (ux + uw - 14, uy + 50),
               (ux + 12, uy + 50)], fill=(44, 44, 48))
    d.rectangle([ux + 24, uy + 6, ux + 66, uy + 28], fill=(232, 232, 228))
    d.rectangle([ux + 82, uy + 10, ux + 128, uy + 28], fill=(196, 58, 40))
    for fx, fh in ((ux + 130, 52), (ux + 148, 40)):
        d.polygon([(fx - 13, uy + 10), (fx, uy + 10 - fh), (fx + 13, uy + 10)],
                  fill=FLAME)
        d.polygon([(fx - 6, uy + 10), (fx, uy + 10 - fh // 2), (fx + 6, uy + 10)],
                  fill=FLAME_Y)
    d.ellipse([ux + 128, uy - 58, ux + 168, uy - 18], fill=(58, 58, 60))
    # caption strip
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 10, y + h - 22), "TANKERS BURN IN THE STRAIT OF HORMUZ",
           font=SANS_B(13), fill=(255, 255, 255))


def story_card(d, x, y, w, h, kicker_text, color, headline, body, tag):
    kicker(d, x, y, kicker_text, color)
    y2 = draw_wrapped(d, x, y + 26, headline, SERIF_B(25), w, INK, spacing=3)
    draw_wrapped(d, x, y2 + 6, body, SANS(16), w, MUTED, spacing=3)
    d.text((x, y + h - 22), tag, font=SANS_B(12), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44  # margin
    # ---- masthead ----
    d.text((m, 26), "THE WORLD TODAY", font=SERIF_B(64), fill=INK)
    rule(d, m, W - m, 108, 4)
    d.text((m, 118), "WEDNESDAY, 25 NOVEMBER 2026", font=SANS_B(19), fill=INK)
    d.text((W - m - 218, 118), "ONE DAY · ONE PAGE", font=SANS_B(16), fill=RED)
    rule(d, m, W - m, 148, 2)

    # ---- hero: text left, illustration right ----
    hy = 168
    hw_text = 470
    kicker(d, m, hy, "THE STRAIT OF HORMUZ  ·  LEAD STORY", RED)
    y = draw_wrapped(d, m, hy + 28,
                     "Tankers ablaze after\nmine strikes",
                     SERIF_B(44), hw_text, INK, spacing=2)
    y = draw_wrapped(d, m, y + 10,
                     "Two oil tankers were struck by naval mines and "
                     "caught fire as they tried to cross the Strait of "
                     "Hormuz, Iran's Revolutionary Guard said, in the "
                     "sharpest escalation of the Iran war at sea.",
                     SANS(17), hw_text, MUTED, spacing=4)
    d.text((m, y + 14), "Full report — page one, continued inside.",
           font=SERIF(15), fill=INK)
    draw_strait(d, m + hw_text + 16, hy, W - m - (m + hw_text + 16), 300)
    rule(d, m, W - m, hy + 322, 2)

    # ---- 2x2 grid ----
    gy = hy + 344
    col_w = (W - 2 * m - 28) // 2
    row_h = 168
    story_card(d, m, gy, col_w, row_h, "SAUDI ARABIA  ·  YEMEN", ORANGE,
               "Houthis hit Saudi refinery; Riyadh tower struck again",
               "The Ras Tanura refinery was attacked and fires broke out; "
               "a second strike on a Riyadh skyscraper injured 11 people.",
               "AP  ·  SCMP")
    story_card(d, m + col_w + 28, gy, col_w, row_h, "GAZA  ·  ISRAEL", RED,
               "Israeli strike kills Hamas security chief in Gaza",
               "Mohammad Abuelouf, who headed the militants' interior "
               "security service, was killed with his wife and two children.",
               "SCMP")
    rule(d, m, W - m, gy + row_h + 8, 1)
    gy2 = gy + row_h + 26
    story_card(d, m, gy2, col_w, row_h, "UNITED STATES  ·  TECH", NAVY,
               "Huawei found guilty of trade-secret theft conspiracy",
               "A US federal court convicted the Chinese tech giant of "
               "conspiracy to steal trade secrets and bank fraud.",
               "JUST SECURITY")
    story_card(d, m + col_w + 28, gy2, col_w, row_h, "SPACE  ·  CHINA", TEAL,
               "Shenzhou-24 lifts off with first foreign astronaut",
               "China's crew of three includes a Pakistani national, the "
               "first foreign astronaut bound for the Tiangong station.",
               "REUTERS")
    rule(d, m, W - m, gy2 + row_h + 8, 2)

    # ---- bottom band: three short items ----
    by = gy2 + row_h + 26
    bw = (W - 2 * m - 56) // 3
    items = [
        ("PACIFIC", PURPLE, "Solomon Islands and Australia sign a treaty "
         "barring any foreign military base."),
        ("WASHINGTON", NAVY, "An unclassified CIA system was breached in "
         "the latest US cybersecurity incident."),
        ("CLIMATE", GOLD, "COP31 talks end with no deal; Pope Leo XIV warns "
         "extreme weather is striking ever more often."),
    ]
    for i, (kick, color, text) in enumerate(items):
        x = m + i * (bw + 28)
        kicker(d, x, by, kick, color)
        draw_wrapped(d, x, by + 26, text, SANS(15), bw, INK, spacing=3)
        if i < 2:
            d.line([(x + bw + 14, by), (x + bw + 14, by + 92)],
                   fill=(180, 175, 162), width=1)

    # ---- footer ----
    rule(d, m, W - m, H - 28, 2)
    d.text((m, H - 22),
           "Sources: Just Security · SCMP · AP · AFP · Reuters  —  All events first reported on 25 November 2026",
           font=SANS(13), fill=MUTED)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
