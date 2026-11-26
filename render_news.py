"""Render the 25 November 2026 front page as a 1024x1024 PNG.

Everything on the page is drawn from scratch with Pillow: the masthead,
the lead story with a small hand-drawn harbour illustration, four mid-page
stories in two rows, and a three-column strip along the bottom. The eight
stories are the verified headlines of 25 November 2026; the wording below
is the copy that goes on the page.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
EDGE = 44                      # side margin
INNER_W = PAGE_W - 2 * EDGE    # 936
HALF_W = 452                   # width of one of the two mid-page columns
HALF_X2 = EDGE + HALF_W + 32   # x of the right-hand column (528)

PAPER = (250, 246, 238)
INK = (22, 22, 22)
SOFT_INK = (60, 58, 52)
RULE = (22, 22, 22)
CRIMSON = (172, 32, 32)
RUST = (196, 90, 20)
NAVY = (28, 64, 110)
TEAL = (14, 120, 110)
PLUM = (110, 52, 130)
OCHRE = (176, 128, 20)
SEA = (38, 74, 110)
SKY = (198, 164, 110)
SUN = (233, 196, 90)

DEJAVU = "/usr/share/fonts/truetype/dejavu"


def pick_font(filename, size):
    """Load a DejaVu face; fall back to Pillow's built-in bitmap font."""
    path = os.path.join(DEJAVU, filename)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


def serif_bold(size):
    return pick_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return pick_font("DejaVuSerif.ttf", size)


def sans(size):
    return pick_font("DejaVuSans.ttf", size)


def sans_bold(size):
    return pick_font("DejaVuSans-Bold.ttf", size)


def fit_serif_bold(text, size, max_width):
    """Shrink the masthead face until the line fits the page width."""
    face = serif_bold(size)
    while face.getlength(text) > max_width and size > 20:
        size -= 2
        face = serif_bold(size)
    return face


def split_lines(canvas, text, face, width):
    """Greedy word wrap; returns a list of lines that fit inside width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if canvas.textlength(trial, font=face) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(canvas, x, y, text, face, width, leading, colour=INK):
    """Draw wrapped text starting at (x, y); return the y below the block."""
    for line in split_lines(canvas, text, face, width):
        canvas.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def hline(canvas, y, weight=2, colour=RULE):
    canvas.line([(EDGE, y), (PAGE_W - EDGE, y)], fill=colour, width=weight)


def masthead_block(canvas):
    """Paper name, a heavy rule, and the date line."""
    face = fit_serif_bold("THE WORLD TODAY", 82, INNER_W)
    canvas.text((EDGE, 20), "THE WORLD TODAY", font=face, fill=INK)
    canvas.line([(EDGE, 116), (PAGE_W - EDGE, 116)], fill=RULE, width=4)
    left = sans_bold(20)
    right = sans_bold(20)
    canvas.text((EDGE, 128), "WEDNESDAY, 25 NOVEMBER 2026",
                font=left, fill=INK)
    tag = "ONE DAY \u00b7 ONE PAGE"
    canvas.text((PAGE_W - EDGE - canvas.textlength(tag, font=right), 128),
                tag, font=right, fill=CRIMSON)
    hline(canvas, 156, 2)


def flame(canvas, base_x, base_y, tall):
    """One little flame: an orange spike with a yellow core."""
    canvas.polygon([(base_x, base_y), (base_x + 13, base_y - tall),
                    (base_x + 26, base_y)], fill=(232, 110, 20))
    canvas.polygon([(base_x + 6, base_y), (base_x + 13, base_y - tall + 14),
                    (base_x + 20, base_y)], fill=(245, 196, 60))


def tanker(canvas, hull_x, hull_y, hull_w, deck, flame_tops):
    """A dark hull with two container blocks, flames and smoke puffs."""
    canvas.polygon([(hull_x, hull_y),
                    (hull_x + hull_w, hull_y),
                    (hull_x + hull_w - 16, hull_y + 28),
                    (hull_x + 14, hull_y + 28)], fill=(28, 28, 28))
    for (cx, cw, ch, colour) in deck:
        canvas.rectangle([cx, hull_y - ch, cx + cw, hull_y], fill=colour)
    for fx in flame_tops:
        flame(canvas, fx, hull_y - 22, 42)
    for (sx, sy, r) in [(hull_x + 40, hull_y - 78, 22),
                        (hull_x + 66, hull_y - 92, 26),
                        (hull_x + 96, hull_y - 76, 19)]:
        canvas.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(62, 62, 62))


def strait_picture(canvas, x, y, w, h):
    """The lead illustration: dusk sky, hills, burning tankers at sea."""
    sky_h = 78
    canvas.rectangle([x, y, x + w, y + sky_h], fill=SKY)
    canvas.ellipse([x + w - 108, y + 12, x + w - 52, y + 68], fill=SUN)
    canvas.polygon([(x, y + sky_h), (x + 130, y + 46),
                    (x + 250, y + sky_h)], fill=(122, 96, 58))
    canvas.polygon([(x + 240, y + sky_h), (x + 360, y + 52),
                    (x + w, y + sky_h)], fill=(104, 88, 56))
    canvas.rectangle([x, y + sky_h, x + w, y + h], fill=SEA)
    for wy in range(y + sky_h + 16, y + h - 8, 20):
        canvas.line([(x + 8, wy), (x + w - 8, wy)],
                    fill=(96, 140, 178), width=2)
    tanker(canvas, x + 22, y + 216, 168,
           [(x + 38, 40, 26, (198, 64, 48)), (x + 84, 38, 24, (232, 230, 224))],
           [x + 42, x + 86, x + 118])
    tanker(canvas, x + 236, y + 228, 150,
           [(x + 252, 34, 22, (232, 230, 224)), (x + 290, 40, 26, (198, 64, 48))],
           [x + 296, x + 322])
    canvas.rectangle([x, y + h - 32, x + w, y + h], fill=(18, 18, 18))
    cap = sans_bold(14)
    canvas.text((x + 12, y + h - 25),
                "TANKERS BURN IN THE STRAIT OF HORMUZ",
                font=cap, fill=(245, 244, 238))


def lead_block(canvas):
    """Lead story on the left, illustration on the right."""
    y0 = 172
    canvas.text((EDGE, y0), "THE STRAIT OF HORMUZ \u00b7 LEAD STORY",
                font=sans_bold(17), fill=CRIMSON)
    head_y = put_lines(canvas, EDGE, y0 + 26,
                       "Tankers ablaze after mine strikes",
                       serif_bold(42), HALF_W, 50)
    body_y = put_lines(canvas, EDGE, head_y + 10,
                       "Two oil tankers were struck by naval mines and "
                       "caught fire crossing the Strait of Hormuz, Iran's "
                       "Revolutionary Guard said, in the sharpest "
                       "escalation of the Iran war at sea.",
                       sans(18), HALF_W, 24, colour=SOFT_INK)
    canvas.text((EDGE, body_y + 10),
                "Full report \u2014 page one, continued inside.",
                font=serif(17), fill=INK)
    text_bottom = body_y + 10 + 20
    strait_picture(canvas, HALF_X2, y0, HALF_W, 280)
    return max(text_bottom, y0 + 280)


def mid_story(canvas, x, y, kicker, tint, headline, summary, credit):
    """One mid-page story: coloured kicker, headline, summary, source."""
    canvas.text((x, y), kicker, font=sans_bold(15), fill=tint)
    y = put_lines(canvas, x, y + 24, headline, serif_bold(30),
                  HALF_W, 36)
    y = put_lines(canvas, x, y + 8, summary, sans(17), HALF_W, 23,
                  colour=SOFT_INK)
    canvas.text((x, y + 8), credit, font=sans_bold(13), fill=INK)
    return y + 26


def bottom_note(canvas, x, y, w, kicker, tint, text):
    """One of the three short items along the bottom of the page."""
    canvas.text((x, y), kicker, font=sans_bold(14), fill=tint)
    return put_lines(canvas, x, y + 20, text, sans(14), w, 18,
                     colour=SOFT_INK)


def footer_line(canvas, y):
    hline(canvas, y, 2)
    note = ("Sources: Just Security \u00b7 SCMP \u00b7 AP \u00b7 AFP \u00b7 "
            "Reuters  \u2014  All events first reported on 25 November 2026")
    canvas.text((EDGE, y + 7), note, font=sans(12), fill=SOFT_INK)


def build_page():
    """Compose the whole front page and write entry.png beside this file."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    canvas = ImageDraw.Draw(page)

    masthead_block(canvas)

    # Every block below reports where it actually ends, and the next
    # rule or row starts from that measured bottom, so nothing can
    # ever print on top of the block above it.
    lead_bottom = lead_block(canvas)
    hline(canvas, lead_bottom + 12, 2)

    row_y = lead_bottom + 24
    row1_end = max(
        mid_story(canvas, EDGE, row_y, "SAUDI ARABIA \u00b7 YEMEN", RUST,
                  "Houthis hit Saudi refinery; Riyadh tower struck again",
                  "The Ras Tanura refinery was attacked and fires broke "
                  "out; a second strike on a Riyadh skyscraper injured "
                  "11 people.",
                  "AP  \u00b7  SCMP"),
        mid_story(canvas, HALF_X2, row_y, "GAZA \u00b7 ISRAEL", CRIMSON,
                  "Israeli strike kills Hamas security chief in Gaza",
                  "Mohammad Abuelouf, who headed the militants' interior "
                  "security service, was killed with his wife and two "
                  "children.",
                  "SCMP"))
    hline(canvas, row1_end + 10, 1)

    row2_y = row1_end + 22
    row2_end = max(
        mid_story(canvas, EDGE, row2_y, "UNITED STATES \u00b7 TECH", NAVY,
                  "Huawei convicted of trade-secret theft",
                  "A US federal court convicted the Chinese tech giant of "
                  "conspiracy to steal trade secrets and bank fraud.",
                  "JUST SECURITY"),
        mid_story(canvas, HALF_X2, row2_y, "SPACE \u00b7 CHINA", TEAL,
                  "Shenzhou-24 lifts off with first foreign astronaut",
                  "China's crew of three includes a Pakistani national, "
                  "the first foreign astronaut bound for the Tiangong "
                  "station.",
                  "REUTERS"))
    hline(canvas, row2_end + 10, 1)

    strip_y = row2_end + 22
    third_w = 296
    third_x = [EDGE, EDGE + third_w + 24, EDGE + 2 * (third_w + 24)]
    strip_end = max(
        bottom_note(canvas, third_x[0], strip_y, third_w, "PACIFIC", PLUM,
                    "Solomon Islands and Australia sign a treaty barring "
                    "any foreign military base."),
        bottom_note(canvas, third_x[1], strip_y, third_w, "WASHINGTON",
                    NAVY,
                    "An unclassified CIA system was breached in the "
                    "latest US cybersecurity incident."),
        bottom_note(canvas, third_x[2], strip_y, third_w, "CLIMATE",
                    OCHRE,
                    "COP31 talks end with no deal; Pope Leo XIV warns "
                    "extreme weather is striking ever more often."))
    for gx in third_x[1:]:
        canvas.line([(gx - 12, strip_y), (gx - 12, strip_y + 56)],
                    fill=(180, 174, 162), width=1)

    footer_line(canvas, strip_end + 8)
    print("page bottoms: lead", lead_bottom, "row1", row1_end,
          "row2", row2_end, "strip", strip_end)

    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    page.save(target, format="PNG")
    print("wrote", target)
    return target


if __name__ == "__main__":
    build_page()
