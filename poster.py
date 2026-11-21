#!/usr/bin/env python3
"""Render the round-3 front page for news-image-20261120 (build time only).

Draws a 1024x1024 newspaper front page with PIL: a dominant lead on the
Russian missiles that landed in Poland on 20 November 2026, with a
schematic situation map of the impact zone, a Wall Street rout feature
with a plunging chart, and briefs. Output is deterministic: same input,
same bytes.

Run:  python3 poster.py            # writes entry.png next to this file
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (246, 241, 230)
INK = (27, 27, 27)
NAVY = (22, 40, 62)
GOLD = (232, 182, 76)
RED = (179, 38, 30)
BLUE = (46, 95, 122)
TEAL = (15, 107, 92)
GREY = (109, 99, 80)
RULE = (185, 173, 147)
SEA = (198, 214, 226)
LAND = (233, 226, 208)
POLAND_FILL = (250, 238, 205)
FOE_FILL = (224, 205, 198)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: font(f"{FD}/DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font(f"{FD}/DejaVuSerif.ttf", s)            # noqa: E731
SANS = lambda s: font(f"{FL}/LiberationSans-Regular.ttf", s)  # noqa: E731
SANS_B = lambda s: font(f"{FL}/LiberationSans-Bold.ttf", s)   # noqa: E731


def tracked(d, xy, text, fnt, fill, tracking=2):
    """Draw text with extra space between letters (kickers)."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking
    return x


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(d, cx, cy, r, fill):
    """Eight-point impact star."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8 - math.pi / 2
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=(255, 255, 255))


def dashed_line(d, pts, fill, width=2, dash=9, gap=6):
    """Dashed polyline through pts (list of xy tuples)."""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg == 0:
            continue
        nx, ny = (x2 - x1) / seg, (y2 - y1) / seg
        s = 0.0
        while s < seg:
            e = min(s + dash, seg)
            d.line([(x1 + nx * s, y1 + ny * s), (x1 + nx * e, y1 + ny * e)],
                   fill=fill, width=width)
            s = e + gap


def arrowhead(d, tip, angle, fill, size=11):
    """Filled arrowhead at tip pointing along angle (radians)."""
    x, y = tip
    p1 = (x - size * math.cos(angle - 0.45), y - size * math.sin(angle - 0.45))
    p2 = (x - size * math.cos(angle + 0.45), y - size * math.sin(angle + 0.45))
    d.polygon([(x, y), p1, p2], fill=fill)


def bezier(p0, p1, p2, steps=24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 38                      # page margin
    CW = W - 2 * MX              # content width

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 82], fill=NAVY)
    d.text((MX, 17), "THE WORLD", font=SERIF_B(48), fill=PAPER)
    tw = d.textlength("THE WORLD ", font=SERIF_B(48))
    d.text((MX + tw, 17), "TODAY", font=SERIF_B(48), fill=GOLD)
    date_f = SANS_B(18)
    d.text((W - MX - d.textlength("FRIDAY 20 NOVEMBER 2026", font=date_f), 21),
           "FRIDAY 20 NOVEMBER 2026", font=date_f, fill=GOLD)
    ed_f = SANS(10)
    ed = "ONE DAY  ·  ONE PAGE  ·  EVENING EDITION"
    d.text((W - MX - d.textlength(ed, font=ed_f), 49), ed, font=ed_f, fill=(201, 212, 226))
    d.rectangle([0, 82, W, 86], fill=GOLD)

    y = 96
    # ---------- lead ----------
    tracked(d, (MX, y), "POLAND  ·  NATO  ·  UKRAINE", SANS_B(13), RED, tracking=3)
    y += 25
    head_f = SERIF_B(58)
    d.text((MX, y), "RUSSIAN MISSILES LAND", font=head_f, fill=INK)
    y += 62
    d.text((MX, y), "ON NATO SOIL", font=head_f, fill=INK)
    y += 68
    stand_f = SANS(19)
    stand = ("Poland calls it an \u201cintentional provocation\u201d as NATO jets scramble "
             "\u2014 two cruise missiles and a drone crash in the south-east during "
             "Moscow\u2019s biggest strike of the month on Ukraine.")
    y = para(d, MX, y, wrap(d, stand, stand_f, CW), stand_f, (43, 43, 43), 25)
    y += 10

    # ---------- situation map panel ----------
    # Correct-aspect strip map: lon 12-36.4, lat 48.8-55.5 (1 deg lon ~ 0.63 deg lat
    # in pixels at 51N, so the shapes read true).
    panel_y0, panel_y1 = y, y + 268
    d.rectangle([MX, panel_y0, W - MX, panel_y1], fill=(252, 249, 240),
                outline=NAVY, width=2)
    map_x0, map_y0 = MX + 14, panel_y0 + 12
    map_w, map_h = 620, panel_y1 - panel_y0 - 24
    rail_x = map_x0 + map_w + 16
    rail_w = W - MX - 14 - rail_x
    LON0, LON1, LAT0, LAT1 = 12.0, 36.4, 48.8, 55.5

    def px(lon):
        return map_x0 + (lon - LON0) / (LON1 - LON0) * map_w

    def py(lat):
        return map_y0 + (LAT1 - lat) / (LAT1 - LAT0) * map_h

    def poly(coords, **kw):
        d.polygon([(px(lo), py(la)) for lo, la in coords], **kw)

    # Baltic Sea (band along the top, north of the Polish coast)
    poly([(12, 55.5), (36.4, 55.5), (36.4, 54.6), (26, 54.9), (24.0, 54.4),
          (22.6, 54.15), (20.9, 54.35), (19.4, 54.2), (18.9, 54.5),
          (17.5, 54.6), (15.5, 54.2), (14.2, 54.0), (12, 54.2)], fill=SEA)
    # Germany (west edge strip)
    poly([(12, 54.2), (14.2, 54.0), (14.2, 53.0), (14.1, 51.9), (14.3, 51.0),
          (15.0, 50.5), (14.6, 49.6), (12, 49.6)], fill=LAND, outline=RULE)
    # Belarus (north-east, tinted)
    poly([(23.9, 53.9), (24.5, 54.5), (26, 54.9), (36.4, 54.9), (36.4, 51.9),
          (32, 51.9), (30, 51.8), (28, 51.5), (26, 51.3), (24.5, 51.5),
          (23.9, 51.9)], fill=FOE_FILL, outline=RULE)
    # Ukraine (east, cut off at the bottom of the strip)
    poly([(22.5, 49.5), (22.9, 50.1), (23.5, 50.9), (23.9, 51.9),
          (24.5, 51.5), (26, 51.3), (28, 51.5), (30, 51.8), (32, 51.9),
          (36.4, 51.9), (36.4, 48.8), (22.4, 48.8), (22.2, 48.9)],
         fill=LAND, outline=RULE)
    # Poland, highlighted
    poland = [(14.2, 54.0), (15.5, 54.2), (17.5, 54.6), (18.9, 54.5),
              (19.4, 54.2), (20.9, 54.35), (22.6, 54.15), (23.9, 53.9),
              (24.0, 53.0), (23.9, 51.9), (23.5, 50.9), (22.9, 50.1),
              (22.5, 49.5), (21.0, 49.4), (19.2, 49.5), (18.2, 49.8),
              (17.2, 50.2), (15.5, 50.8), (14.3, 51.0), (14.1, 51.9),
              (14.2, 53.0)]
    poly(poland, fill=POLAND_FILL, outline=NAVY)
    d.line([(px(lo), py(la)) for lo, la in poland] + [(px(14.2), py(54.0))],
           fill=NAVY, width=2)
    # labels
    d.text((px(30.0), py(55.2)), "BALTIC SEA", font=SANS_B(10), fill=BLUE)
    d.text((px(12.6), py(52.6)), "GERMANY", font=SANS_B(10), fill=GREY)
    d.text((px(27.5), py(54.35)), "BELARUS", font=SANS_B(10), fill=GREY)
    d.text((px(31.2), py(51.4)), "UKRAINE", font=SANS_B(11), fill=GREY)
    d.text((px(16.8), py(51.7)), "POLAND", font=SERIF_B(15), fill=NAVY)
    # cities
    for lon, lat, name, dx, dy in [(21.01, 52.23, "WARSAW", 8, -6),
                                   (30.52, 50.45, "KYIV", 8, -6)]:
        d.ellipse([px(lon) - 3, py(lat) - 3, px(lon) + 3, py(lat) + 3],
                  fill=INK)
        d.text((px(lon) + dx, py(lat) + dy), name, font=SANS_B(11), fill=INK)
    # missile tracks (dashed red, from the east into SE Poland)
    for p0, p1, p2 in [((29.6, 49.6), (26.4, 50.7), (23.15, 50.55)),
                       ((28.8, 51.3), (25.5, 51.0), (22.30, 50.44)),
                       ((29.4, 48.9), (26.2, 49.5), (23.00, 50.02))]:
        pts = bezier((px(p0[0]), py(p0[1])), (px(p1[0]), py(p1[1])),
                     (px(p2[0]), py(p2[1])))
        dashed_line(d, pts, RED, width=2)
        ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        arrowhead(d, pts[-1], ang, RED)
    # impact stars + staggered labels with leader lines
    lab_f = SANS_B(10)
    nl = (px(23.10), py(50.55))
    star(d, *nl, 9, RED)
    d.line([(nl[0] + 5, nl[1] - 7), (nl[0] + 12, nl[1] - 24)], fill=RED, width=1)
    d.text((nl[0] + 14, nl[1] - 34), "NOWY LIPOWIEC", font=lab_f, fill=RED)
    rn = (px(22.24), py(50.44))
    star(d, *rn, 9, RED)
    rt = "RUDNIK NAD SANEM"
    d.line([(rn[0] - 12, rn[1] - 4),
            (rn[0] - 24 - d.textlength(rt, font=lab_f), rn[1] - 4)],
           fill=RED, width=1)
    d.text((rn[0] - 24 - d.textlength(rt, font=lab_f), rn[1] - 9), rt,
           font=lab_f, fill=RED)
    mo = (px(22.95), py(50.02))
    star(d, *mo, 9, RED)
    d.line([(mo[0] + 6, mo[1] + 7), (mo[0] + 12, mo[1] + 16)], fill=RED, width=1)
    d.text((mo[0] + 14, mo[1] + 12), "MO\u0141ODYCZ", font=lab_f, fill=RED)
    # callout + schematic note (exercise timing kept as a caption line)
    tag = "NATO JETS SCRAMBLED  ·  PATRIOTS ON ALERT"
    tf = SANS_B(11)
    twd = d.textlength(tag, font=tf)
    d.rectangle([map_x0 + 8, map_y0 + 8, map_x0 + 24 + twd, map_y0 + 30],
                fill=NAVY)
    d.text((map_x0 + 16, map_y0 + 14), tag, font=tf, fill=(255, 255, 255))
    d.text((map_x0, panel_y1 - 12),
           "SCHEMATIC MAP \u2014 NOT TO SCALE  ·  TIMED TO COINCIDE WITH THE "
           "COALITION EXERCISE AT NOWA D\u0118BA",
           font=SANS(9), fill=GREY)

    # right rail: the strike in numbers
    rx = rail_x
    d.text((rx, panel_y0 + 12), "THE STRIKE", font=SANS_B(13), fill=RED)
    d.line([(rx, panel_y0 + 34), (rx + rail_w, panel_y0 + 34)], fill=RULE, width=1)
    facts = [
        ("3", "Russian weapons down in Poland \u2014 two Kh-101 missiles and a drone"),
        ("400+", "drones and 110 missiles fired at Ukraine overnight"),
        ("8", "killed in the strikes on Ukraine, Kyiv says"),
        ("0", "hurt in Poland \u2014 jets scrambled, Patriots on alert"),
    ]
    fy = panel_y0 + 46
    for num, txt in facts:
        nf = SERIF_B(30)
        d.text((rx, fy), num, font=nf, fill=RED)
        nw = d.textlength(num, font=nf)
        tx = rx + nw + 12
        lines = wrap(d, txt, SANS(13.5), rail_w - (nw + 12))
        para(d, tx, fy + 2, lines, SANS(13.5), (43, 43, 43), 17)
        fy += 56
        if num != "0":
            d.line([(rx, fy - 7), (rx + rail_w, fy - 7)], fill=RULE, width=1)

    y = panel_y1 + 10
    d.line([(MX, y), (W - MX, y)], fill=NAVY, width=2)
    d.line([(MX, y + 4), (W - MX, y + 4)], fill=NAVY, width=1)
    y += 12

    # ---------- supporting row ----------
    col_gap = 26
    left_w = 500
    right_x = MX + left_w + col_gap
    right_w = W - MX - right_x
    top_y = y

    # left: markets + chart
    tracked(d, (MX, top_y), "MARKETS  ·  WALL STREET", SANS_B(13), BLUE, tracking=3)
    mh = para(d, MX, top_y + 24,
              ["AI rout wipes $4 trillion", "in a week"],
              SERIF_B(27), INK, 32)
    body = ("Nasdaq falls 5.3% and the S&P 500 3.7% as the AI sell-off deepens; "
            "Nvidia drops 14% as the SEC opens a probe into its accounting "
            "\u2014 its worst week since 2008.")
    by = para(d, MX, mh + 6, wrap(d, body, SANS(15.5), left_w), SANS(15.5),
              (43, 43, 43), 20)
    # plunging chart
    d.text((MX, by + 8), "NASDAQ COMPOSITE, THIS WEEK", font=SANS_B(10), fill=RED)
    ch_x, ch_y, ch_w, ch_h = MX, by + 26, left_w, 54
    d.rectangle([ch_x, ch_y, ch_x + ch_w, ch_y + ch_h], outline=RULE, width=1)
    vals = [100, 97.4, 95.2, 93.1, 89.7]      # Nasdaq index, Mon-Fri
    vmin, vmax = 88.0, 101.0
    pts = []
    for i, v in enumerate(vals):
        pts.append((ch_x + 14 + i * (ch_w - 28) / 4,
                    ch_y + 8 + (vmax - v) / (vmax - vmin) * (ch_h - 20)))
    area = pts + [(pts[-1][0], ch_y + ch_h - 4), (pts[0][0], ch_y + ch_h - 4)]
    d.polygon(area, fill=(244, 214, 210))
    d.line(pts, fill=RED, width=3, joint="curve")
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=RED)
    wk = "\u221210% IN A WEEK"
    d.text((ch_x + ch_w - 8 - d.textlength(wk, font=SANS_B(12)), ch_y + 6), wk,
           font=SANS_B(12), fill=RED)
    d.text((ch_x + 8, ch_y + ch_h - 16), "MON", font=SANS(9), fill=GREY)
    d.text((ch_x + ch_w - 26, ch_y + ch_h - 16), "FRI", font=SANS(9), fill=GREY)
    left_bottom = ch_y + ch_h

    # right: Iran, then Akvan
    tracked(d, (right_x, top_y), "WASHINGTON  ·  IRAN", SANS_B(13), RED, tracking=3)
    rh = para(d, right_x, top_y + 24,
              ["Senate backs Trump on Iran", "war, 51\u201348"],
              SERIF_B(27), INK, 32)
    body2 = ("Republicans block a war-powers curb in the first Iran vote since "
             "the midterms; Trump says he is in \u201cno rush\u201d and will "
             "decide after the new year.")
    ry = para(d, right_x, rh + 6, wrap(d, body2, SANS(15.5), right_w),
              SANS(15.5), (43, 43, 43), 20)
    ry += 10
    d.line([(right_x, ry), (right_x + right_w, ry)], fill=RULE, width=1)
    ry += 10
    tracked(d, (right_x, ry), "INDIA  ·  WEATHER", SANS_B(13), RED, tracking=3)
    rh2 = para(d, right_x, ry + 24, ["Cyclone Akvan hits India\u2019s coast"],
               SERIF_B(24), INK, 29)
    body3 = ("More than 300,000 evacuated as the storm makes landfall near "
             "Gopalpur; no deaths reported.")
    ry2 = para(d, right_x, rh2 + 5, wrap(d, body3, SANS(15.5), right_w),
               SANS(15.5), (43, 43, 43), 20)
    right_bottom = ry2

    y = max(left_bottom, right_bottom) + 10
    d.line([(MX, y), (W - MX, y)], fill=NAVY, width=2)
    y += 10

    # ---------- the day in brief ----------
    d.text((MX, y), "THE DAY IN BRIEF", font=SANS_B(12), fill=NAVY)
    y += 20
    briefs = [
        ("PERU  ·  QUAKE", RED, "6.7 quake shakes Andes",
         "Felt in Lima; no deaths reported."),
        ("CLIMATE  ·  COP31", TEAL, "Draft drops fossil fuels",
         "Antalya talks run past deadline."),
        ("CULTURE  ·  GAMES", RED, "GTA 6: $3.8bn day one",
         "32.5m copies, a record launch."),
        ("SPORT  ·  CRICKET", TEAL, "Phillips makes history",
         "A first in all three formats."),
    ]
    bw = (CW - 3 * 20) / 4
    for i, (kick, col, head, txt) in enumerate(briefs):
        bx = MX + i * (bw + 20)
        if i:
            d.line([(bx - 10, y), (bx - 10, y + 70)], fill=RULE, width=1)
        tracked(d, (bx, y), kick, SANS_B(11), col, tracking=2)
        byy = para(d, bx, y + 20, wrap(d, head, SERIF_B(16), bw),
                   SERIF_B(16), INK, 19)
        para(d, bx, byy + 3, wrap(d, txt, SANS(13), bw), SANS(13),
             (43, 43, 43), 16)
    y += 80

    # ---------- footer ----------
    d.line([(MX, y), (W - MX, y)], fill=NAVY, width=1)
    foot = ("HEADLINES AS REPORTED ON FRIDAY 20 NOVEMBER 2026  ·  COMPILED FROM "
            "WIRE AND PRESS REPORTS OF THE DAY")
    ff = SANS(11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y + 8), foot, font=ff,
           fill=GREY)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({W}x{H}); footer ends near y={y + 19}")


if __name__ == "__main__":
    main()
