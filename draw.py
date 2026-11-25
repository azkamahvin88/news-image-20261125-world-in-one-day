#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

Fresh build, 25 Nov 2026. Generates a 1024x1024 newspaper front page
summarising Wednesday 25 November 2026 world news: 36 stories, 7 regions.
Run: python3 draw.py  -> writes entry.png (deterministic, no network,
no wall-clock, no unseeded randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 22                      # side margin
CW = W - 2 * M              # content width = 980

PAPER = (246, 241, 229)
INK = (20, 18, 16)
RED = (142, 31, 31)
NAVY = (31, 58, 95)
GREY = (107, 100, 85)
RULE = (201, 191, 165)
LIGHT = (238, 231, 214)
GOLD = (176, 132, 40)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, leading, fill=INK, max_lines=None):
    lines = wrap(d, text, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=font, fill=fill)
    return y + len(lines) * leading


def center(d, y, text, font, fill=INK, x0=M, x1=W - M):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------- stories
# (num, region, label, headline, body, source)
LEADS = [
    (1, "Europe", "UKRAINE'S LONG ARM",
     "Kyiv's sea drones sink Russian warship off Libya",
     "President Zelenskyy confirmed Ukraine struck two Russian vessels at "
     "Benghazi, sinking the corvette Merkury, and a cargo ship in the Gulf "
     "of Finland. Norway, a staunch ally, urged caution.",
     "Reuters"),
    (2, "Middle East", "RIYADH ATTACK",
     "Houthis hit Riyadh's tallest tower; 11 wounded",
     "A Houthi strike hit the capital's tallest tower, wounding 11, Saudi "
     "civil defence said. The rebels pushed to within 60 km of Aden, and "
     "Britain sanctioned the Houthis and four officials.",
     "Reuters"),
    (3, "Asia", "HUAWEI GUILTY",
     "Huawei convicted on 10 of 12 US criminal counts",
     "A Brooklyn jury found Huawei guilty of bank fraud, wire fraud and "
     "stealing trade secrets over its Iran business, after an 11-week "
     "trial. Sentencing is set for 14 September 2027.",
     "Reuters"),
]

SMALL = [
    (4, "Europe", "NATO / POLAND",
     "NATO sends early-warning jets to Poland",
     "AWACS jets will deploy after Russian missiles and a drone entered "
     "Polish airspace.", "Reuters"),
    (5, "Europe", "PUTIN / RETALIATION",
     "Putin vows retaliation over refinery strikes",
     "Putin called retaliation \u201cinevitable\u201d; Lukashenko offered a "
     "Moscow flight.", "Kremlin / X"),
    (6, "Europe", "WAR TOLL",
     "700,000+ Russian soldiers killed, leak finds",
     "Leaked Russian documents point to over 700,000 Russian dead in the "
     "Ukraine war.", "RFE/RL"),
    (7, "Europe", "KYIV REGION",
     "Russian strike on Kyiv-region flats kills 11",
     "Rescuers pulled bodies from a Kyiv-region block hit by drones; toll "
     "reached 11.", "RFE/RL"),
    (8, "Europe", "PATRIOT DELAY",
     "Zelenskyy: US \u201caligning with Russia\u201d",
     "48 Patriot interceptors await US approval; Ukraine needs \u20ac115bn "
     "for 2027.", "Bloomberg"),
    (9, "Americas", "THANKSGIVING",
     "Trump pardons turkeys Freedom and Feathers",
     "The president spared two turkeys, and gave Rudy Giuliani the Medal "
     "of Freedom.", "AP"),
    (10, "Americas", "FORT HOOD",
     "Fort Hood gunman seeks stay of execution",
     "Nidal Hasan, who killed 13 in 2009, asked a US court to halt his "
     "execution next week.", "Reuters"),
    (11, "Europe", "SARKOZY",
     "Sarkozy and Bruni ordered to stand trial",
     "French judges sent the ex-president and his wife to trial; first "
     "hearing 1 April 2027.", "Reuters"),
    (12, "Asia", "INDONESIA",
     "Indonesia's vice-president resigns",
     "The vice-president stepped down amid political strain in Jakarta.",
     "Wire reports"),
    (13, "Africa", "SENEGAL",
     "Senegal get AFCON title back after CAS ruling",
     "The Court of Arbitration for Sport restored Senegal's 2025 Africa "
     "Cup of Nations title.", "AFP"),
]

# (num, headline, source) -- one line each
ALSO = [
    (14, "Iran braces for winter gas shortages; power rationing bites", "DW"),
    (15, "Iraq orders federal forces to seize Kurdish oilfields", "Reuters"),
    (16, "Israeli strike kills Hamas security chief in Gaza", "BBC"),
    (17, "Israel: Iran building chemical weapons, plotted to kill Trump", "Israel says"),
    (18, "Iran says three oil tankers hit by mines in Hormuz strait", "IRGC claim"),
    (19, "EU unveils 22nd sanctions package against Russia", "EU"),
    (20, "Denmark's top court upholds \u201cghetto\u201d evictions", "Reuters"),
    (21, "Cameroon separatist leader faces war-crimes trial in Norway", "Reuters"),
    (22, "RFE/RL returns to shortwave radio for Afghan girls", "RFE/RL"),
    (23, "Xiamen Airlines orders 50 Boeing 737-8 jets", "Reuters"),
    (24, "Nvidia gives back $240bn after Monday's 31.5% surge", "Motley Fool"),
    (25, "Bitcoin slips towards $60,000 as crypto pressure grows", "Share-Talk"),
    (26, "England beat Australia by 8 wickets in 2nd T20I, chasing 185", "AP"),
    (27, "Australia's ASX jumps 1.82%; layoffs hit post-Covid high", "FNN"),
    (28, "Car bomb in Colombia wounds 23; gunmen hold 25 hostage", "Reuters"),
    (29, "FBI crime database hit by suspected breach", "Reuters"),
    (30, "Radar fault delays flights at Chicago O'Hare, FAA says", "Reuters"),
    (31, "US envoy \u201cnot certain\u201d military aid to Israel ends this year", "Reuters"),
    (32, "NATO vows to defend vs space threats", "Reuters"),
    (33, "Asteroid eclipse imaged; Vera Rubin's first pictures released", "NASA"),
    (34, "Landmine victims hit five-year high", "Landmine Monitor"),
    (35, "Nigerian emir suspended after sexual-assault allegation", "Reuters"),
    (36, "DR Congo rebels pull back from areas after clashes", "Reuters"),
]

# region name -> (count, colour)
REGIONS = [
    ("Europe", 10, (31, 58, 95)),
    ("Asia", 5, (176, 132, 40)),
    ("Middle East", 7, (142, 31, 31)),
    ("Africa", 4, (46, 110, 70)),
    ("Americas", 5, (90, 60, 110)),
    ("Oceania", 2, (20, 120, 130)),
    ("Global", 3, (90, 90, 90)),
]

STATS = [
    ("700,000+", "Russian soldiers killed (reported)"),
    ("11", "wounded in Riyadh tower strike"),
    ("60 km", "Houthis from Aden"),
    ("10 of 12", "Huawei counts guilty"),
    ("\u20ac115bn", "Ukraine needs for 2027"),
    ("31.5%", "Nvidia's Monday surge"),
]

# (lon, lat) pins for featured stories 1-13
PINS = {
    1: (20.1, 32.1), 2: (46.7, 24.7), 3: (-68.0, 44.0), 4: (14.0, 56.0),
    5: (44.0, 60.0), 6: (42.0, 47.0), 7: (24.0, 45.0), 8: (32.0, 54.0),
    9: (-78.0, 37.0), 10: (-97.8, 31.1), 11: (0.0, 50.0),
    12: (106.8, -6.2), 13: (-17.4, 14.7),
}


# ---------------------------------------------------------------- illustrations
def illus(d, num, x, y, w, h):
    """Flat original vector-style scene per story, drawn with PIL shapes."""
    sky = [(52, 84, 130), (196, 120, 60), (58, 90, 120), (70, 110, 140),
           (150, 90, 70), (90, 110, 90), (120, 90, 120), (70, 90, 120),
           (180, 160, 90), (60, 70, 90), (140, 120, 90), (70, 120, 110),
           (60, 130, 80)][num - 1]
    d.rectangle([x, y, x + w, y + h], fill=sky)
    # sun / moon
    d.ellipse([x + w - 26, y + 8, x + w - 8, y + 26], fill=(246, 230, 170))
    if num == 1:  # sea, ship, drone
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(28, 52, 84))
        d.polygon([(x + w * 0.15, y + h * 0.62), (x + w * 0.85, y + h * 0.62),
                   (x + w * 0.78, y + h * 0.85), (x + w * 0.22, y + h * 0.85)],
                  fill=(40, 40, 44))
        d.rectangle([x + w * 0.42, y + h * 0.42, x + w * 0.58, y + h * 0.62],
                    fill=(40, 40, 44))
        d.line([x + w * 0.5, y + h * 0.42, x + w * 0.5, y + h * 0.28],
               fill=(40, 40, 44), width=3)
        d.ellipse([x + w * 0.68, y + h * 0.12, x + w * 0.78, y + h * 0.22],
                  fill=(20, 20, 20))
        d.line([x + w * 0.62, y + h * 0.17, x + w * 0.84, y + h * 0.17],
               fill=(20, 20, 20), width=2)
        for k in range(5):
            d.line([x + w * 0.80, y + h * 0.30 + k * 6,
                    x + w * 0.88, y + h * 0.30 + k * 6], fill=(230, 80, 40), width=2)
    elif num == 2:  # tall tower + burst
        d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(60, 55, 50))
        d.polygon([(x + w * 0.42, y + h * 0.78), (x + w * 0.58, y + h * 0.78),
                   (x + w * 0.55, y + h * 0.08), (x + w * 0.45, y + h * 0.08)],
                  fill=(30, 30, 34))
        d.polygon([(x + w * 0.45, y + h * 0.08), (x + w * 0.55, y + h * 0.08),
                   (x + w * 0.52, y + h * 0.02), (x + w * 0.48, y + h * 0.02)],
                  fill=(30, 30, 34))
        for k in range(6):
            d.rectangle([x + w * 0.46, y + h * (0.15 + k * 0.10),
                         x + w * 0.54, y + h * (0.19 + k * 0.10)],
                        fill=(246, 220, 120))
        cx, cy = x + w * 0.72, y + h * 0.30
        for ang in range(0, 360, 45):
            import math
            ex = cx + 16 * math.cos(math.radians(ang))
            ey = cy + 16 * math.sin(math.radians(ang))
            d.line([cx, cy, ex, ey], fill=(240, 120, 30), width=3)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(240, 120, 30))
    elif num == 3:  # courthouse + scales
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(90, 85, 75))
        d.polygon([(x + w * 0.1, y + h * 0.35), (x + w * 0.5, y + h * 0.12),
                   (x + w * 0.9, y + h * 0.35)], fill=(240, 235, 220))
        for k in range(4):
            cx0 = x + w * (0.18 + k * 0.21)
            d.rectangle([cx0, y + h * 0.38, cx0 + 8, y + h * 0.75],
                        fill=(240, 235, 220))
        d.rectangle([x + w * 0.08, y + h * 0.75, x + w * 0.92, y + h * 0.82],
                    fill=(240, 235, 220))
        d.ellipse([x + w * 0.68, y + h * 0.55, x + w * 0.80, y + h * 0.67],
                  outline=(20, 20, 20), width=3)
        d.line([x + w * 0.74, y + h * 0.55, x + w * 0.74, y + h * 0.45],
               fill=(20, 20, 20), width=3)
    elif num == 4:  # AWACS plane
        d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(70, 90, 70))
        d.ellipse([x + w * 0.30, y + h * 0.28, x + w * 0.62, y + h * 0.50],
                  fill=(235, 235, 230))
        d.polygon([(x + w * 0.05, y + h * 0.45), (x + w * 0.38, y + h * 0.38),
                   (x + w * 0.38, y + h * 0.50)], fill=(235, 235, 230))
        d.polygon([(x + w * 0.60, y + h * 0.42), (x + w * 0.95, y + h * 0.38),
                   (x + w * 0.60, y + h * 0.50)], fill=(200, 200, 195))
        d.line([x + w * 0.46, y + h * 0.28, x + w * 0.46, y + h * 0.20],
               fill=(40, 40, 40), width=3)
        d.ellipse([x + w * 0.40, y + h * 0.14, x + w * 0.52, y + h * 0.26],
                  fill=(40, 40, 40))
        for k in range(3):
            d.line([x + w * 0.08, y + h * (0.60 + k * 0.08),
                    x + w * 0.92, y + h * (0.60 + k * 0.08)],
                   fill=(255, 255, 255), width=1)
    elif num == 5:  # refinery flames
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(50, 45, 40))
        for k, hh in enumerate([0.45, 0.60, 0.38]):
            bx = x + w * (0.15 + k * 0.28)
            d.rectangle([bx, y + h * (0.72 - hh), bx + 14, y + h * 0.72],
                        fill=(180, 180, 175))
            d.polygon([(bx + 2, y + h * (0.72 - hh)), (bx + 7, y + h * (0.60 - hh)),
                       (bx + 12, y + h * (0.72 - hh))], fill=(240, 120, 30))
        d.polygon([(x + w * 0.55, y + h * 0.72), (x + w * 0.75, y + h * 0.30),
                   (x + w * 0.95, y + h * 0.72)], fill=(230, 90, 40))
        d.polygon([(x + w * 0.65, y + h * 0.72), (x + w * 0.75, y + h * 0.48),
                   (x + w * 0.85, y + h * 0.72)], fill=(246, 200, 60))
    elif num == 6:  # field of crosses
        d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(70, 95, 60))
        for r in range(3):
            for c in range(6):
                cx = x + w * (0.10 + c * 0.16)
                cy = y + h * (0.30 + r * 0.18)
                d.line([cx, cy - 6, cx, cy + 6], fill=(235, 235, 225), width=3)
                d.line([cx - 5, cy - 2, cx + 5, cy - 2], fill=(235, 235, 225), width=3)
        d.rectangle([x, y + h * 0.68, x + w, y + h * 0.72], fill=(60, 80, 55))
    elif num == 7:  # damaged apartment block
        d.rectangle([x, y + h * 0.25, x + w * 0.75, y + h], fill=(150, 140, 125))
        d.polygon([(x + w * 0.75, y + h * 0.25), (x + w, y + h * 0.45),
                   (x + w, y + h), (x + w * 0.75, y + h)], fill=(110, 100, 88))
        for r in range(3):
            for c in range(3):
                wx = x + w * (0.10 + c * 0.20)
                wy = y + h * (0.35 + r * 0.20)
                d.rectangle([wx, wy, wx + 12, wy + 10], fill=(246, 220, 130))
        d.ellipse([x + w * 0.78, y + h * 0.10, x + w * 0.98, y + h * 0.30],
                  fill=(120, 115, 105))
        d.ellipse([x + w * 0.85, y + h * 0.02, x + w, y + h * 0.18],
                  fill=(140, 135, 125))
    elif num == 8:  # missile launcher
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(60, 70, 55))
        d.rectangle([x + w * 0.15, y + h * 0.62, x + w * 0.85, y + h * 0.75],
                    fill=(50, 55, 45))
        d.polygon([(x + w * 0.30, y + h * 0.62), (x + w * 0.45, y + h * 0.30),
                   (x + w * 0.55, y + h * 0.30), (x + w * 0.42, y + h * 0.62)],
                  fill=(200, 200, 190))
        d.polygon([(x + w * 0.45, y + h * 0.30), (x + w * 0.50, y + h * 0.18),
                   (x + w * 0.55, y + h * 0.30)], fill=(200, 60, 40))
        for k in range(3):
            d.ellipse([x + w * (0.70 + k * 0.10), y + h * 0.15,
                       x + w * (0.74 + k * 0.10), y + h * 0.19],
                      fill=(255, 255, 255))
    elif num == 9:  # turkey + White House
        d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(90, 110, 70))
        d.rectangle([x + w * 0.10, y + h * 0.45, x + w * 0.90, y + h * 0.70],
                    fill=(240, 235, 220))
        d.polygon([(x + w * 0.10, y + h * 0.45), (x + w * 0.5, y + h * 0.28),
                   (x + w * 0.90, y + h * 0.45)], fill=(240, 235, 220))
        cx, cy = x + w * 0.50, y + h * 0.55
        d.ellipse([cx - 14, cy - 10, cx + 14, cy + 12], fill=(120, 75, 35))
        d.ellipse([cx - 5, cy - 18, cx + 5, cy - 8], fill=(120, 75, 35))
        d.polygon([(cx - 3, cy - 14), (cx + 3, cy - 14), (cx, cy - 6)],
                  fill=(230, 120, 40))
        for k in range(3):
            d.ellipse([cx - 18 + k * 12, cy - 16, cx - 6 + k * 12, cy - 2],
                      outline=(150, 90, 40), width=2)
    elif num == 10:  # gavel + bars
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(80, 70, 60))
        for k in range(5):
            bx = x + w * (0.08 + k * 0.18)
            d.rectangle([bx, y + h * 0.15, bx + 6, y + h * 0.75],
                        fill=(60, 60, 64))
        d.rectangle([x + w * 0.55, y + h * 0.45, x + w * 0.95, y + h * 0.58],
                    fill=(120, 80, 40))
        d.line([x + w * 0.75, y + h * 0.58, x + w * 0.75, y + h * 0.72],
               fill=(120, 80, 40), width=4)
    elif num == 11:  # Paris tower + court
        d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(90, 85, 75))
        d.polygon([(x + w * 0.30, y + h * 0.78), (x + w * 0.50, y + h * 0.05),
                   (x + w * 0.70, y + h * 0.78)], fill=(40, 40, 44))
        d.polygon([(x + w * 0.38, y + h * 0.78), (x + w * 0.50, y + h * 0.35),
                   (x + w * 0.62, y + h * 0.78)], fill=(246, 241, 229))
        d.rectangle([x + w * 0.20, y + h * 0.60, x + w * 0.80, y + h * 0.64],
                    fill=(40, 40, 44))
        d.rectangle([x + w * 0.82, y + h * 0.55, x + w * 0.95, y + h * 0.78],
                    fill=(200, 190, 170))
    elif num == 12:  # Monas obelisk + flag
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(70, 100, 70))
        d.polygon([(x + w * 0.46, y + h * 0.75), (x + w * 0.54, y + h * 0.75),
                   (x + w * 0.52, y + h * 0.15), (x + w * 0.48, y + h * 0.15)],
                  fill=(240, 235, 220))
        d.polygon([(x + w * 0.44, y + h * 0.15), (x + w * 0.56, y + h * 0.15),
                   (x + w * 0.50, y + h * 0.05)], fill=(230, 180, 40))
        d.rectangle([x + w * 0.40, y + h * 0.72, x + w * 0.60, y + h * 0.78],
                    fill=(240, 235, 220))
        d.line([x + w * 0.70, y + h * 0.10, x + w * 0.70, y + h * 0.60],
               fill=(40, 40, 40), width=2)
        d.rectangle([x + w * 0.70, y + h * 0.10, x + w * 0.92, y + h * 0.20],
                    fill=(200, 40, 40))
        d.rectangle([x + w * 0.70, y + h * 0.20, x + w * 0.92, y + h * 0.30],
                    fill=(255, 255, 255))
    else:  # 13 trophy
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(46, 110, 70))
        cx = x + w * 0.5
        d.ellipse([cx - 26, y + h * 0.18, cx + 26, y + h * 0.55],
                  fill=(230, 180, 40))
        d.rectangle([cx - 26, y + h * 0.18, cx + 26, y + h * 0.32],
                    fill=(230, 180, 40))
        d.arc([cx - 38, y + h * 0.20, cx - 18, y + h * 0.48], 90, 270,
              fill=(230, 180, 40), width=4)
        d.arc([cx + 18, y + h * 0.20, cx + 38, y + h * 0.48], 270, 90,
              fill=(230, 180, 40), width=4)
        d.rectangle([cx - 4, y + h * 0.55, cx + 4, y + h * 0.68],
                    fill=(230, 180, 40))
        d.rectangle([cx - 14, y + h * 0.68, cx + 14, y + h * 0.75],
                    fill=(230, 180, 40))
        for k in range(5):
            d.ellipse([x + w * (0.08 + k * 0.18), y + h * 0.08,
                       x + w * (0.12 + k * 0.18), y + h * 0.12],
                      fill=(255, 255, 255))


# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 73),
     (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
     (-70, -52), (-73, -45), (-73, -30), (-70, -18), (-77, -12), (-80, -5),
     (-80, 2)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (2, 51), (5, 53),
     (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (12, 65), (18, 69),
     (25, 71), (30, 70), (35, 68), (40, 68), (45, 66), (40, 60), (35, 55),
     (30, 50), (28, 45), (23, 40), (20, 40), (15, 44), (10, 44), (5, 43),
     (0, 40), (-5, 36)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (40, 15), (43, 11), (48, 11), (51, 10), (46, 5),
     (42, 0), (40, -5), (38, -12), (35, -18), (32, -25), (28, -32),
     (20, -35), (16, -30), (12, -18), (9, -5), (9, 0), (4, 6), (-8, 5),
     (-13, 8), (-17, 15), (-17, 20), (-15, 25), (-10, 30)],
    [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 76),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45),
     (142, 40), (140, 35), (135, 33), (130, 31), (127, 35), (122, 38),
     (120, 32), (115, 25), (110, 20), (108, 12), (105, 8), (100, 8),
     (97, 15), (92, 20), (88, 22), (85, 20), (80, 15), (77, 8), (75, 10),
     (70, 20), (66, 25), (60, 25), (57, 26), (52, 28), (50, 30), (48, 30),
     (44, 29), (40, 32), (38, 36), (36, 36), (30, 36), (27, 37), (23, 36),
     (20, 40)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (114, -22)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    for lon in range(-150, 181, 30):
        mx = x + (lon + 170) / 360 * w
        d.line([mx, y, mx, y + h], fill=(235, 240, 244), width=1)
    for lat in range(-60, 76, 30):
        my = y + (75 - lat) / 130 * h
        d.line([x, my, x + w, my], fill=(235, 240, 244), width=1)

    def proj(lon, lat):
        return (x + (lon + 170) / 360 * w, y + (75 - lat) / 130 * h)

    for poly in CONTINENTS:
        d.polygon([proj(lo, la) for lo, la in poly], fill=(196, 188, 160),
                  outline=(120, 110, 90))
    fnum = F(SANS_B, 8)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(n), font=fnum)
        d.text((px - tw / 2, py - 4), str(n), font=fnum, fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- kicker bar
    fkick = F(SANS_B, 12)
    d.text((M, 12), "THE WORLD IN ONE DAY", font=fkick, fill=RED)
    rk = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - M - d.textlength(rk, font=fkick), 12), rk, font=fkick, fill=INK)
    d.line([M, 32, W - M, 32], fill=RED, width=2)
    d.line([M, 35, W - M, 35], fill=INK, width=1)

    # --- masthead
    fmast = F(SERIF_B, 56)
    center(d, 42, "Wednesday 25 November 2026", fmast)
    d.line([M, 106, W - M, 106], fill=INK, width=1)

    # --- sub-headline (italic, 2 lines, centred)
    fsub = F(SERIF_I, 15)
    sub = ("Kyiv's sea drones sink a Russian warship off Libya \u00b7 Houthis strike "
           "Riyadh's tallest tower \u00b7 Huawei convicted on 10 counts in New York")
    slines = wrap(d, sub, fsub, CW)
    y = 112
    for ln in slines:
        center(d, y, ln, fsub)
        y += 19
    d.line([M, 152, W - M, 152], fill=RULE, width=1)

    # --- stat strip: 6 boxes
    y0, y1 = 158, 206
    bw = (CW - 5 * 4) // 6
    fnum = F(SERIF_B, 25)
    flab = F(SANS, 9)
    for i, (num, lab) in enumerate(STATS):
        bx = M + i * (bw + 4)
        d.rectangle([bx, y0, bx + bw, y1], outline=RULE, width=1, fill=LIGHT)
        nw = d.textlength(num, font=fnum)
        d.text((bx + (bw - nw) / 2, y0 + 4), num, font=fnum, fill=RED)
        lw = d.textlength(lab, font=flab)
        d.text((bx + (bw - lw) / 2, y0 + 33), lab, font=flab, fill=GREY)

    # --- region bar
    y0, y1 = 212, 232
    total = sum(c for _, c, _ in REGIONS)
    rx = M
    flab2 = F(SANS_B, 9)
    for name, cnt, col in REGIONS:
        seg = int(round(cnt / total * CW))
        if rx + seg > W - M:
            seg = W - M - rx
        d.rectangle([rx, y0, rx + seg, y1], fill=col)
        short = {"Europe": "EUROPE", "Asia": "ASIA", "Middle East": "M. EAST",
                 "Africa": "AFRICA", "Americas": "AMERICAS", "Oceania": "OCEANIA",
                 "Global": "GLOBAL"}[name]
        t = "%s %d" % (short, cnt)
        tw = d.textlength(t, font=flab2)
        d.text((rx + (seg - tw) / 2, y0 + 5), t, font=flab2, fill=(255, 255, 255))
        rx += seg

    # --- 3 lead stories
    lw3 = (CW - 2 * 10) // 3
    flab3 = F(SANS_B, 11)
    fhead3 = F(SERIF_B, 16)
    fbody3 = F(SERIF, 12)
    fsrc = F(SANS, 10)
    for i, (num, region, label, head, body, src) in enumerate(LEADS):
        x = M + i * (lw3 + 10)
        illus(d, num, x, 240, lw3, 128)
        d.text((x, 372), "%d  %s" % (num, label), font=flab3, fill=RED)
        para(d, x, 388, head, fhead3, lw3, 19, max_lines=2)
        para(d, x, 428, body, fbody3, lw3, 15, max_lines=3)
        d.text((x, 472), "Source: " + src, font=fsrc, fill=GREY)

    d.line([M, 488, W - M, 488], fill=RULE, width=1)

    # --- 10 small stories, 5 x 2
    sw = (CW - 4 * 10) // 5
    flab4 = F(SANS_B, 9)
    fhead4 = F(SERIF_B, 12)
    fbody4 = F(SERIF, 10)
    fsrc4 = F(SANS, 9)
    for i, (num, region, label, head, body, src) in enumerate(SMALL):
        row, col = divmod(i, 5)
        x = M + col * (sw + 10)
        y = 496 + row * 110
        illus(d, num, x, y, sw, 34)
        d.text((x, y + 37), "%d  %s" % (num, label), font=flab4, fill=RED)
        para(d, x, y + 48, head, fhead4, sw, 13, max_lines=2)
        para(d, x, y + 74, body, fbody4, sw, 11, max_lines=2)
        d.text((x, y + 98), "Source: " + src, font=fsrc4, fill=GREY)

    d.line([M, 716, W - M, 716], fill=INK, width=1)

    # --- bottom: map (left) + ALSO ON (right)
    ftitle = F(SANS_B, 12)
    d.text((M, 724), "WHERE IT HAPPENED", font=ftitle, fill=INK)
    draw_map(d, M, 742, 330, 150)
    fnote = F(SANS, 9)
    para(d, M, 896, "Pins 1\u201313 mark the featured stories above. "
         "Numbers match the story numbers.", fnote, 330, 11, fill=GREY,
         max_lines=2)

    ax = M + 340
    aw = W - M - ax
    d.text((ax, 724), "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 23 MORE STORIES",
           font=ftitle, fill=INK)
    fitem = F(SANS, 9)
    fnum2 = F(SANS_B, 9)
    colw = (aw - 12) // 2
    for i, (num, head, src) in enumerate(ALSO):
        col, row = divmod(i, 12)
        x = ax + col * (colw + 12)
        y = 744 + row * 14
        d.text((x, y), "%d." % num, font=fnum2, fill=RED)
        nw = d.textlength("%d. " % num, font=fnum2)
        line = "%s (%s)" % (head, src)
        # trim if it would overflow the column
        while d.textlength(line, font=fitem) > colw - nw - 2 and len(line) > 20:
            line = line[:-5].rstrip() + "\u2026"
        d.text((x + nw, y), line, font=fitem, fill=INK)

    # --- DATE CHECK box
    d.rectangle([M, 926, W - M, 988], outline=RED, width=2)
    d.text((M + 10, 931), "DATE CHECK \u2014 WHAT WE LEFT OUT ON PURPOSE",
           font=F(SANS_B, 11), fill=RED)
    fdc = F(SERIF, 11)
    dc = ("Tue 24 Nov Champions League results (Real Madrid 5-1 PSV; Man City "
          "2-2 Napoli) are Tuesday's news, not today's. The Huawei verdict came "
          "down late Tuesday in New York. Wed night's ties (Liverpool at Club "
          "Brugge; PSG v Roma) were still to be played at press time; Nvidia's "
          "31.5% surge was Monday.")
    para(d, M + 10, 948, dc, fdc, CW - 20, 14, max_lines=3)

    # --- footer
    ffoot = F(SANS, 10)
    center(d, 996,
           "Every story here happened, or was first reported, on Wednesday "
           "25 November 2026  \u00b7  Sources named beside each story  \u00b7  "
           "Original drawings", ffoot, fill=GREY)
    return img


def main():
    img = build()
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
