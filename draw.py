#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday 26 November 2026.

Deterministic: no timestamps, no randomness. Writes entry.png next to this
file (or to the path given as argv[1]). Run: python3 draw.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RULE = (40, 40, 40)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline_block(draw, x, y, max_w, headline, head_size, body, body_size,
                   head_leading=None, body_leading=None, kicker=None):
    """A story block: optional kicker, bold headline, body text. Returns y."""
    if kicker:
        kf = font(SERIF_B, 15)
        draw.text((x, y), kicker.upper(), font=kf, fill=GREY)
        y += 22
    hf = font(SERIF_B, head_size)
    y = draw_wrapped(draw, x, y, headline, hf, max_w,
                     head_leading or int(head_size * 1.08))
    y += 4
    bf = font(SERIF, body_size)
    y = draw_wrapped(draw, x, y, body, bf, max_w,
                     body_leading or int(body_size * 1.30))
    return y


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin
    CW = W - 2 * M  # content width

    # --- top double rule ---
    d.line([(M, 26), (W - M, 26)], fill=RULE, width=3)
    d.line([(M, 32), (W - M, 32)], fill=RULE, width=1)

    # --- masthead ---
    mast = font(SERIF_B, 86)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 44), title, font=mast, fill=INK)

    # --- date / edition line ---
    d.line([(M, 152), (W - M, 152)], fill=RULE, width=2)
    df = font(SERIF, 24)
    date = "Thursday 26 November 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 162), date, font=df, fill=INK)
    sf = font(SERIF_I, 17)
    left = "WORLD EDITION"
    right = "No. 330"
    d.text((M, 166), left, font=sf, fill=GREY)
    rw = d.textlength(right, font=sf)
    d.text((W - M - rw, 166), right, font=sf, fill=GREY)
    d.line([(M, 198), (W - M, 198)], fill=RULE, width=3)
    d.line([(M, 204), (W - M, 204)], fill=RULE, width=1)

    y = 222
    # --- lead story ---
    y = headline_block(
        d, M, y, CW,
        "US proposes 25% tariffs on India",
        56,
        "Washington proposes tariffs of up to 25% on Indian goods — falling to "
        "17% if a trade deal is clinched — and prepares a wider plan for new "
        "tariffs on trading partners around the world.",
        21, head_leading=60, body_leading=27, kicker="Trade • Lead story")
    y += 6
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10

    # --- two-column middle: stories 2-3 left, 4-5 right ---
    col_w = (CW - 24) // 2
    left_x, right_x = M, M + col_w + 24
    ly = headline_block(
        d, left_x, y, col_w,
        "China probes Shanghai party chief",
        30,
        "Beijing investigates Politburo member Chen Jining in a graft probe "
        "that upends the traditional path to power.",
        19, head_leading=33, body_leading=24, kicker="China")
    ly += 12
    d.line([(left_x, ly), (left_x + col_w, ly)], fill=GREY, width=1)
    ly += 12
    ly = headline_block(
        d, left_x, ly, col_w,
        "Russia's war toll nears 500,000",
        30,
        "Russia's own figures show it has lost nearly 500,000 people in the "
        "Ukraine war.",
        19, head_leading=33, body_leading=24, kicker="Ukraine war")
    ry = headline_block(
        d, right_x, y, col_w,
        "Record migrant arrival in Canary Islands",
        30,
        "Nearly 2,000 migrants reach Spain's Canary Islands in a record "
        "single-day arrival.",
        19, head_leading=33, body_leading=24, kicker="Migration")
    ry += 12
    d.line([(right_x, ry), (right_x + col_w, ry)], fill=GREY, width=1)
    ry += 12
    ry = headline_block(
        d, right_x, ry, col_w,
        "Colombia supermarket siege ends",
        30,
        "Colombian police storm a supermarket and free 20 hostages held for "
        "17 hours.",
        19, head_leading=33, body_leading=24, kicker="Colombia")
    y = max(ly, ry) + 10
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10

    # --- bottom row: three columns, stories 6-8 ---
    col3 = (CW - 48) // 3
    xs = [M, M + col3 + 24, M + 2 * (col3 + 24)]
    stories = [
        ("North Korea expels Swiss envoy",
         "Pyongyang orders Switzerland to close its newly opened diplomatic "
         "office and expels its head over sanctions."),
        ("Bangladesh garment workers win 36% pay rise",
         "Bangladesh raises the minimum wage for garment workers by 36%."),
        ("First Pakistani astronaut heads to Tiangong",
         "Muhammad Zeeshan Ali becomes the first foreign astronaut to join "
         "China's Shenzhou-24 mission to the Tiangong space station."),
    ]
    bottom = y
    for x, (h, b) in zip(xs, stories):
        e = headline_block(d, x, y, col3, h, 24, b, 17,
                           head_leading=27, body_leading=22)
        bottom = max(bottom, e)
    y = bottom + 10

    # --- also in brief strip ---
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 10
    bf = font(SERIF_B, 16)
    d.text((M, y), "ALSO IN BRIEF", font=bf, fill=INK)
    y += 22
    brief = font(SERIF, 16)
    items = [
        "Houthis threaten retaliation after a port city is hit.",
        "India marks Constitution Day; IITs to add 6,000 seats.",
        "India and China hold high-level border talks in the Arunachal sector.",
        "Sheikh Hasina plans a return to Bangladesh on 16 December.",
        "US attorney general dodges questions about an Nvidia investigation.",
        "India–Nepal joint military exercise begins in Rupandehi.",
    ]
    for it in items:
        d.text((M + 14, y), "•", font=brief, fill=INK)
        y = draw_wrapped(d, M + 34, y, it, brief, CW - 34, 20)
        y += 1

    # --- footer ---
    d.line([(M, H - 44), (W - M, H - 44)], fill=RULE, width=2)
    ff = font(SERIF_I, 16)
    foot = "THE WORLD TODAY  •  Thursday 26 November 2026  •  All the world's news, in one page"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, H - 36), foot, font=ff, fill=GREY)

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {W}x{H}")


if __name__ == "__main__":
    main()
