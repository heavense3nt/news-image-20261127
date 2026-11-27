#!/usr/bin/env python3
"""news-image-20261127 — Sum up 27 November 2026 world news in one image.

Draws a dense one-page newspaper front page (1024x1024 PNG) with PIL.
Everything is drawn with code: fixed fonts, fixed geometry, no randomness,
no network, no timestamps -> two runs produce byte-identical output.
Writes /output/entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (248, 244, 236)
INK = (22, 22, 22)
NAVY = (20, 33, 61)
RED = (180, 35, 24)
GREY = (90, 90, 90)
LIGHT_GREY = (220, 216, 206)
BLUE = (38, 84, 140)
GOLD = (176, 132, 30)
GREEN = (32, 110, 62)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, max_w, text, fnt, fill=INK, leading=None, max_lines=None):
    """Draw wrapped paragraph; returns y after last line."""
    if leading is None:
        leading = fnt.size + 4
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(d, x, y, max_w, text, size=26, leading=None, fill=INK):
    fnt = font(SERIF, size)
    if leading is None:
        leading = size + 5
    return block(d, x, y, max_w, text, fnt, fill=fill, leading=leading)


def kicker(d, x, y, text, color=RED):
    fnt = font(SANS_B, 13)
    d.text((x, y), text, font=fnt, fill=color)
    return y + 19


def rule(d, x0, y, x1, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(198, 222, 240),
              outline=NAVY, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=NAVY,
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360, fill=NAVY,
          width=2)
    d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 0, 180, fill=NAVY,
          width=2)
    for mx, my in [(cx - 28, cy - 18), (cx + 12, cy - 30), (cx + 30, cy + 8)]:
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED)


def draw_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 64, 84))
    for ex, ey, ew, eh in [(x + 18, y + 34, 90, 46), (x + 70, y + 20, 110, 52),
                           (x + 140, y + 36, 96, 44), (x + 96, y + 48, 90, 40)]:
        d.ellipse([ex, ey, ex + ew, ey + eh], fill=(200, 205, 212))
    d.polygon([(x + 118, y + 62), (x + 96, y + 104), (x + 112, y + 104),
               (x + 100, y + 138), (x + 134, y + 92), (x + 118, y + 92)],
              fill=(250, 204, 21))
    for rx in range(x + 24, x + w - 16, 22):
        d.line([(rx, y + h - 26), (rx - 6, y + h - 8)], fill=(140, 180, 220),
               width=2)
    d.text((x + 10, y + 6), "70 mph GUSTS", font=font(SANS_B, 12),
           fill=(255, 255, 255))


def draw_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 38))
    d.ellipse([x + 8, y + 8, x + w - 8, y + h - 8], outline=(90, 140, 200),
              width=2)
    for sx, sy in [(x + 30, y + 26), (x + w - 34, y + 40), (x + 44, y + h - 30),
                   (x + w - 46, y + h - 42), (x + w // 2, y + 16)]:
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(250, 204, 21))
    cx = x + w // 2
    d.polygon([(cx, y + 34), (cx - 16, y + 62), (cx + 16, y + 62)], fill=RED)
    d.rectangle([cx - 16, y + 62, cx + 16, y + 108], fill=(240, 240, 240))
    d.ellipse([cx - 6, y + 70, cx + 6, y + 84], fill=BLUE)
    d.polygon([(cx - 16, y + 96), (cx - 30, y + 116), (cx - 16, y + 108)],
              fill=RED)
    d.polygon([(cx + 16, y + 96), (cx + 30, y + 116), (cx + 16, y + 108)],
              fill=RED)
    d.polygon([(cx - 9, y + 108), (cx + 9, y + 108), (cx, y + 132)],
              fill=(250, 160, 32))
    d.text((x + 10, y + h - 20), "1,000,000 SATELLITES",
           font=font(SANS_B, 12), fill=(255, 255, 255))


def draw_chart(d, x, y, w, h):
    vals = [("GDP 4.3%", 0.55, GREEN), ("NASDAQ +2.5%", 0.42, BLUE),
            ("GOLD $3,600+", 0.88, GOLD), ("BRENT $96", 0.62, NAVY)]
    bw = (w - 20) // 4
    base = y + h - 28
    for i, (lab, frac, col) in enumerate(vals):
        bx = x + 10 + i * bw
        bh = int((h - 52) * frac)
        d.rectangle([bx, base - bh, bx + bw - 12, base], fill=col)
        d.text((bx, base - bh - 16), lab.split()[1], font=font(SANS_B, 11),
               fill=INK)
        d.text((bx, base + 4), lab.split()[0], font=font(SANS_B, 10),
               fill=GREY)
    d.line([x + 4, base, x + w - 4, base], fill=INK, width=2)


def draw_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    cols = [RED, BLUE, GREEN, GOLD]
    for i in range(4):
        d.rectangle([x + 16 + i * 52, y + 30, x + 16 + i * 52 + 46, y + 58],
                    fill=cols[i])
        d.rectangle([x + 30 + i * 52, y + 62, x + 30 + i * 52 + 46, y + 90],
                    fill=cols[(i + 2) % 4])
    d.polygon([(x + 8, y + 92), (x + w - 8, y + 92), (x + w - 30, y + 118),
               (x + 30, y + 118)], fill=NAVY)
    d.text((x + 12, y + 6), "14 PARTNERS  \u2022  UP TO 40%",
           font=font(SANS_B, 12), fill=RED)


def draw_derrick(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 30))
    cx = x + w // 2
    d.line([cx - 34, y + h - 8, cx - 8, y + 14], fill=(200, 200, 200), width=3)
    d.line([cx + 34, y + h - 8, cx + 8, y + 14], fill=(200, 200, 200), width=3)
    d.line([cx - 26, y + h - 34, cx + 26, y + h - 34], fill=(200, 200, 200),
           width=2)
    d.line([cx - 18, y + h - 62, cx + 18, y + h - 62], fill=(200, 200, 200),
           width=2)
    d.polygon([(cx - 8, y + 30), (cx, y + 8), (cx + 8, y + 30)],
              fill=(250, 160, 32))
    d.polygon([(cx - 4, y + 30), (cx, y + 18), (cx + 4, y + 30)],
              fill=(250, 220, 80))
    d.text((x + 10, y + h - 22), "JAZAN REFINERY HIT",
           font=font(SANS_B, 12), fill=(255, 255, 255))


def draw_baseball(d, x, y, r):
    cx, cy = x + r, y + r
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=(255, 255, 255),
              outline=RED, width=3)
    d.arc([x - r, y - 6, x + r + 6, y + 2 * r + 6], 300, 60, fill=RED, width=3)
    d.arc([x + r - 6, y - 6, x + 3 * r, y + 2 * r + 6], 120, 240, fill=RED,
          width=3)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    R = W - M  # right edge

    # ---------- MASTHEAD ----------
    d.rectangle([0, 0, W, 90], fill=NAVY)
    d.text((M, 14), "THE WORLD IN ONE PAGE",
           font=font(SERIF, 46), fill=(255, 255, 255))
    d.text((R - 218, 16), "FRIDAY", font=font(SANS_B, 15),
           fill=(250, 204, 21))
    d.text((R - 218, 36), "27 NOVEMBER 2026", font=font(SANS_B, 24),
           fill=(255, 255, 255))
    d.rectangle([0, 90, W, 95], fill=RED)
    # ticker
    d.text((M, 102),
           "BRENT $96  \u2022  GOLD $3,600+  \u2022  NASDAQ FUTURES +2.5%  \u2022  "
           "DOLLAR: 3RD MONTHLY GAIN  \u2022  BLACK FRIDAY TODAY",
           font=font(SANS_B, 13), fill=INK)
    rule(d, M, 126, R, 2)

    # ---------- ROW A: LEAD + STORM ----------
    y = 140
    lx, lw = M, 596
    y2 = kicker(d, lx, y, "MIDDLE EAST  \u2022  UKRAINE  \u2014  LEAD STORY")
    y2 = headline(d, lx, y2, lw,
                  "TRUMP: \u2018VICTORY AT HAND\u2019 IN IRAN WAR; "
                  "PUTIN \u2018WANTS A DEAL\u2019 ON UKRAINE", size=29)
    y2 = block(d, lx, y2 + 4, lw,
               "Trump told troops victory over Iran is near and offered "
               "Tehran a chance to deal, after meeting NATO chief Rutte "
               "at Mar-a-Lago. Zelensky warned the US not to drift "
               "from Ukraine.",
               font(SANS, 15), leading=20)
    draw_globe(d, lx + 84, y2 + 52, 44)
    d.text((lx + 190, y2 + 14),
           "Hormuz tanker traffic rises\ndespite attacks on cargo ships.\n"
           "Iran rations power as US\npressure bites; oil near $96.",
           font=font(SANS, 14), fill=INK)
    # Storm (right, 356 wide)
    sx, sw = 644, 356
    rule(d, sx - 16, y, sx - 16, 268, fill=LIGHT_GREY)
    y2 = kicker(d, sx, y, "UNITED STATES  \u2022  WEATHER")
    y2 = headline(d, sx, y2, sw,
                  "THANKSGIVING STORM BATTERS EAST COAST", size=25)
    draw_storm(d, sx, y2 + 2, sw, 136)
    y2 = block(d, sx, y2 + 146, sw,
               "More than 724,000 without power as 70 mph gusts topple "
               "trees. The 100th Macy\u2019s Thanksgiving Day Parade is "
               "postponed for the first time ever; 1,000+ flights hit.",
               font(SANS, 14), leading=18)
    rule(d, M, 428, R, 2)

    # ---------- ROW B: SPACEX / MARKETS / TARIFFS ----------
    y = 444
    col_w = 312
    gap = 20
    cols = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    # SpaceX
    y2 = kicker(d, cols[0], y, "TECH  \u2022  SPACE")
    y2 = headline(d, cols[0], y2, col_w,
                  "SPACEX CLEARED FOR 1 MILLION SATELLITES", size=22)
    draw_rocket(d, cols[0], y2 + 2, col_w, 132)
    block(d, cols[0], y2 + 142, col_w,
          "FCC approves orbital AI data centres. Musk pledges 2 SpaceX "
          "shares to every US child \u2014 an $18bn giveaway.",
          font(SANS, 13), leading=18)
    # Markets
    rule(d, cols[1] - 10, y, cols[1] - 10, 268, fill=LIGHT_GREY)
    y2 = kicker(d, cols[1], y, "MARKETS  \u2022  ECONOMY")
    y2 = headline(d, cols[1], y2, col_w,
                  "GDP REVISED UP TO 4.3%; GOLD TOPS $3,600", size=22)
    draw_chart(d, cols[1], y2 + 2, col_w, 132)
    block(d, cols[1], y2 + 142, col_w,
          "US Q3 growth revised up from 3.4%. Trump demands a probe "
          "into the figures. Fed hike bets rise; Tokyo core inflation "
          "hits a 16-month high at 2.9%.",
          font(SANS, 13), leading=18)
    # Tariffs
    rule(d, cols[2] - 10, y, cols[2] - 10, 268, fill=LIGHT_GREY)
    y2 = kicker(d, cols[2], y, "TRADE  \u2022  TARIFFS")
    y2 = headline(d, cols[2], y2, col_w,
                  "NEW US TARIFFS: UP TO 40% ON CHINA", size=22)
    draw_ship(d, cols[2], y2 + 2, col_w, 132)
    block(d, cols[2], y2 + 142, col_w,
          "Washington proposes duties on 14 partners \u2014 40% China, "
          "35% Vietnam, 10% on Brazilian aircraft. Beijing and "
          "Brasilia vow retaliation.",
          font(SANS, 13), leading=18)
    rule(d, M, 716, R, 2)

    # ---------- ROW C: GULF / SPORT / BRIEFS ----------
    y = 732
    # Gulf
    y2 = kicker(d, cols[0], y, "GULF  \u2022  ENERGY")
    y2 = headline(d, cols[0], y2, col_w,
                  "HOUTHI STRIKE HITS SAUDI ARAMCO REFINERY", size=22)
    draw_derrick(d, cols[0], y2 + 2, col_w, 120)
    block(d, cols[0], y2 + 128, col_w,
          "Attack on Jazan refinery kills a worker and halts some "
          "operations. Two Italian technicians die in a drone strike "
          "on a Kuwaiti facility.",
          font(SANS, 13), leading=18)
    # Sport
    rule(d, cols[1] - 10, y, cols[1] - 10, 264, fill=LIGHT_GREY)
    y2 = kicker(d, cols[1], y, "SPORT")
    y2 = headline(d, cols[1], y2, col_w,
                  "SKUBAL\u2019S $450M METS DEAL SETS RECORD",
                  size=22)
    draw_baseball(d, cols[1] + 104, y2 + 4, 44)
    block(d, cols[1], y2 + 100, col_w,
          "Tarik Skubal signs a 9-year, $450m deal with the New York "
          "Mets \u2014 the richest contract ever for a pitcher. LeBron "
          "James posts his first triple-double for the 76ers.",
          font(SANS, 13), leading=18)
    # World briefs
    rule(d, cols[2] - 10, y, cols[2] - 10, 264, fill=LIGHT_GREY)
    y2 = kicker(d, cols[2], y, "WORLD IN BRIEF")
    briefs = [
        "NZ coalition falls one seat short of a majority.",
        "UK net migration drops to near a 30-year low.",
        "Cloudflare outage hits hours before Black Friday.",
        "FIFA hit by cyberattack; data stolen.",
        "Olympic trailblazer Anita DeFrantz dies at 74.",
        "Kim Jong Un vows to expand nuclear arsenal.",
    ]
    bf = font(SANS, 13)
    for b in briefs:
        d.ellipse([cols[2], y2 + 5, cols[2] + 7, y2 + 12], fill=RED)
        y2 = block(d, cols[2] + 14, y2, col_w - 14, b, bf, leading=18,
                   max_lines=2)
        y2 += 7

    # ---------- FOOTER ----------
    rule(d, M, 996, R, 2)
    d.text((M, 1004), "ALL STORIES FROM FRIDAY 27 NOVEMBER 2026  \u2022  "
           "SOURCES: REUTERS, AP, BBC, AFP, NYT",
           font=font(SANS_B, 11), fill=GREY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
