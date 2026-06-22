#!/usr/bin/env python3
"""Genereert de PNG-assets voor het Luminosity Plymouth-thema ("Grote zonsopkomst").

Draait met Pillow. De output gaat naar het thema in airootfs zodat de ISO-build
ze meeneemt:
    iso/airootfs/usr/share/plymouth/themes/luminosity/

Assets:
    background.png   1920x1080  donker + warme horizon-gloed van onderaf
    sun.png          360x360    gouden zon met gezicht (zonder stralen)
    rays.png         360x360    losse stralenkrans (wordt door het script gedraaid)
    ring.png         420x420    dunne voortgangsring (gedraaid = activiteit)
    title.png                   "Luminosity OS" wordmark (OS in goud)
    tagline.png                 "je computer in gewone taal"
    label.png                   "OPSTARTEN…"
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HIER, "..", "airootfs", "usr", "share", "plymouth", "themes", "luminosity"))
os.makedirs(OUT, exist_ok=True)

BG = (10, 12, 18)            # #0a0c12
GOLD = (255, 209, 102)       # #ffd166
ORANGE = (255, 158, 74)      # #ff9e4a
INK = (36, 26, 6)            # #241a06
TEXT = (238, 240, 246)       # #eef0f6
MUTED = (207, 211, 224)      # #cfd3e0
SS = 4                       # supersampling voor gladde randen


def _font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
        "/usr/share/fonts/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def background(w=1920, h=1080):
    img = Image.new("RGB", (w, h), BG)
    # Warme horizon-gloed: radiale ellips die net onder het midden-onder zit.
    glow = Image.new("RGB", (w, h), BG)
    px = glow.load()
    cx, cy = w / 2, h * 1.06           # centrum laag (horizon onderaan)
    rx, ry = w * 0.62, h * 0.62
    for y in range(h):
        for x in range(0, w, 2):       # stap 2 voor snelheid; vul beide kolommen
            d = math.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
            t = max(0.0, 1.0 - d)
            t = t * t                  # zachtere afval
            r = int(BG[0] + (255 - BG[0]) * t * 0.9)
            g = int(BG[1] + (180 - BG[1]) * t * 0.75)
            b = int(BG[2] + (90 - BG[2]) * t * 0.45)
            px[x, y] = (r, g, b)
            if x + 1 < w:
                px[x + 1, y] = (r, g, b)
    img = glow
    # dunne lichtlijn als "horizon"
    d = ImageDraw.Draw(img, "RGBA")
    ly = int(h * 0.74)
    for i, a in ((0, 0), (1, 90), (2, 40)):
        d.line([(w * 0.12, ly + i), (w * 0.88, ly + i)], fill=(255, 209, 102, a), width=1)
    img.save(os.path.join(OUT, "background.png"))


def _supersampled(size):
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img), big


def sun(size=360):
    img, d, big = _supersampled(size)
    c = big / 2
    r = big * 0.30
    # zachte gloed-halo
    halo = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse([c - r * 1.5, c - r * 1.5, c + r * 1.5, c + r * 1.5], fill=GOLD + (60,))
    img = Image.alpha_composite(img, halo)
    d = ImageDraw.Draw(img)
    # schijf
    d.ellipse([c - r, c - r, c + r, c + r], fill=GOLD + (255,))
    # gezicht
    eye = r * 0.10
    ex = r * 0.36
    ey = r * 0.18
    d.ellipse([c - ex - eye, c - ey - eye, c - ex + eye, c - ey + eye], fill=INK + (255,))
    d.ellipse([c + ex - eye, c - ey - eye, c + ex + eye, c - ey + eye], fill=INK + (255,))
    # glimlach
    mw = r * 0.5
    d.arc([c - mw, c - r * 0.05, c + mw, c + r * 0.55], start=20, end=160,
          fill=INK + (255,), width=int(r * 0.10))
    img.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, "sun.png"))


def rays(size=360, n=12):
    img, d, big = _supersampled(size)
    c = big / 2
    r0 = big * 0.34
    r1 = big * 0.43
    wlw = int(big * 0.012)
    for i in range(n):
        a = math.radians(i * 360 / n)
        x0, y0 = c + math.cos(a) * r0, c + math.sin(a) * r0
        x1, y1 = c + math.cos(a) * r1, c + math.sin(a) * r1
        d.line([(x0, y0), (x1, y1)], fill=GOLD + (255,), width=wlw)
    img.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, "rays.png"))


def ring(size=420):
    img, d, big = _supersampled(size)
    c = big / 2
    r = big * 0.46
    lw = int(big * 0.010)
    # track (donker) volledige cirkel
    d.ellipse([c - r, c - r, c + r, c + r], outline=(32, 40, 58, 255), width=lw)
    # voortgangsboog (goud) ~ 100 graden
    d.arc([c - r, c - r, c + r, c + r], start=-90, end=10, fill=GOLD + (255,), width=lw)
    img.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, "ring.png"))


def text_img(name, text, size, color, bold=True, spacing=0):
    f = _font(size * SS, bold=bold)
    tmp = Image.new("RGBA", (10, 10))
    td = ImageDraw.Draw(tmp)
    bbox = td.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0] + spacing * (len(text) - 1) + 8 * SS
    h = bbox[3] - bbox[1] + 8 * SS
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if spacing:
        x = 4 * SS
        for ch in text:
            d.text((x, 4 * SS - bbox[1]), ch, font=f, fill=color + (255,))
            cb = d.textbbox((0, 0), ch, font=f)
            x += (cb[2] - cb[0]) + spacing
    else:
        d.text((4 * SS, 4 * SS - bbox[1]), text, font=f, fill=color + (255,))
    sw, sh = int(w / SS), int(h / SS)
    img.resize((sw, sh), Image.LANCZOS).save(os.path.join(OUT, name))


def title():
    # "Luminosity OS" — OS in goud. Twee delen naast elkaar samenstellen.
    f = _font(46 * SS, bold=True)
    a, b = "Luminosity", " OS"
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ba = tmp.textbbox((0, 0), a, font=f)
    bb = tmp.textbbox((0, 0), b, font=f)
    w = (ba[2] - ba[0]) + (bb[2] - bb[0]) + 8 * SS
    h = max(ba[3] - ba[1], bb[3] - bb[1]) + 8 * SS
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    top = 4 * SS - min(ba[1], bb[1])
    d.text((4 * SS, top), a, font=f, fill=TEXT + (255,))
    d.text((4 * SS + (ba[2] - ba[0]), top), b, font=f, fill=GOLD + (255,))
    img.resize((int(w / SS), int(h / SS)), Image.LANCZOS).save(os.path.join(OUT, "title.png"))


if __name__ == "__main__":
    print("genereren naar", OUT)
    background()
    sun()
    rays()
    ring()
    title()
    text_img("tagline.png", "je computer in gewone taal", 20, MUTED, bold=False)
    text_img("label.png", "OPSTARTEN", 16, MUTED, bold=True, spacing=int(5 * SS))
    print("klaar:", sorted(os.listdir(OUT)))
