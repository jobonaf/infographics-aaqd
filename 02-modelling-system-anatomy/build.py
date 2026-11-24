#!/usr/bin/env python3
"""Infografica 02 - Anatomia di un sistema modellistico (documento tecnico CE, §1.4).
Archetipo H (anatomia con callout) + matrioska delle scale. Solo layout wide (16:9).
Uso:  python build.py [it|en]      Testi in strings/<lingua>.yaml; geometrie qui.
Nessun valore numerico inventato: scale e dimensioni delle celle sono quelle del documento (Tab. 1-1, §1.4.7).
La griglia di punti di «Concentrazioni» e' uno schema illustrativo (campo liscio calcolato, senza unita')."""
import sys, math, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
STEM = "modelling_system_anatomy"

def big_arrow(cx, cy, k=1.5):
    return f'<g transform="translate({cx},{cy}) scale({k}) translate({-cx},{-cy})">{small_arrow(cx, cy)}</g>'

def build(lang):
    S = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    b = [f'<rect width="{W}" height="{H}" fill="{BEIGE}"/>', header(S["title"], S["subtitle"])]

    # ---------------- 2 · ingressi (gruppo)
    b.append('<g id="inputs">')
    b.append(f'<rect x="26" y="150" width="390" height="520" rx="36" fill="{TEAL}" fill-opacity=".10"/>')
    cards = [(160, 100, "source", S["emissions"], None), (300, 100, "wave", S["meteo"], None),
             (440, 220, "area", S["boundary"], S["boundary_sub"])]
    for y, h, kind, title, sub in cards:
        b.append(card(36, y, 370, h))
        if sub is None:
            b.append(circ_icon(kind, 88, y + h // 2, r=30))
            b.append(lines(136, y + h // 2 + 10, [title], 29, 255, w=700, fill=TEAL_D))
        else:
            b.append(circ_icon(kind, 88, y + 52, r=30))
            t, n = para(136, y + 48, [title], 29, 255, w=700, fill=TEAL_D, lh=1.15)
            b.append(t)
            s2, _ = para(136, y + 48 + 34 * n + 18, [sub], 22, 255)
            b.append(s2)
    b.append('</g>')
    for cy in (210, 350, 550):
        b.append(big_arrow(453, cy))

    # ---------------- 1 · modello
    b.append('<g id="model">')
    b.append(card(500, 160, 380, 500))
    b.append(T(524, 205, S["model"], 32, 700, TEAL_D))
    for y, kind, key in ((222, "gear", "det"), (438, "grid", "data")):
        b.append(f'<rect x="520" y="{y}" width="340" height="200" rx="22" fill="{TEAL}" fill-opacity=".10"/>')
        b.append(circ_icon(kind, 576, y + 58, r=32))
        b.append(lines(624, y + 68, [S[key]], 29, 225, w=700, fill=SLATE))
        t, _ = para(540, y + 132, [S[key + "_sub"]], 23, 300)
        b.append(t)
    b.append('</g>')
    b.append(big_arrow(930, 410))

    # ---------------- uscita: concentrazioni (schema: campo liscio calcolato)
    b.append('<g id="output">')
    b.append(card(980, 160, 260, 500))
    b.append(lines(1110, 205, [S["out"]], 29, 230, w=700, fill=TEAL_D, anchor="middle"))
    for j in range(8):
        for i in range(5):
            v = (0.9 * math.exp(-((i - 1.2) ** 2 + (j - 3.0) ** 2) / 2.2)
                 + 0.5 * math.exp(-((i - 3.5) ** 2 + (j - 5.5) ** 2) / 3.0) + 0.12)
            r = 5 + 13 * min(v, 1.0)
            col = RED if v > 0.75 else TEAL
            op = 0.35 + 0.6 * min(v, 1.0)
            b.append(f'<circle cx="{1110 + (i - 2) * 46}" cy="{255 + j * 46}" r="{r:.1f}" fill="{col}" fill-opacity="{op:.2f}"/>')
    b.append(lines(1110, 640, [S["out_note"]], 19, 230, it=True, fill=SLATE, anchor="middle"))
    b.append('</g>')

    # ---------------- 4 · misure e ritorno
    b.append('<g id="measurements">')
    b.append(arrow(690, 740, 690, 668, TEAL_D, 7))
    b.append(arrow(1110, 740, 1110, 668, TEAL_D, 7))
    b.append(card(36, 740, 1204, 150))
    b.append(circ_icon("pin", 106, 815, r=36))
    b.append(lines(160, 827, [S["meas"]], 34, 300, w=700, fill=TEAL_D))
    for x in (490, 950):
        b.append(f'<path d="M{x},760 V870" stroke="#B7C6C4" stroke-width="2.4"/>')
    for cx, key, mw in ((690, "assim", 360), (1095, "fusion", 250)):
        b.append(lines(cx, 786, [S[key]], 28, mw, w=700, fill=SLATE, anchor="middle"))
        t, _ = para(cx, 820, [S[key + "_sub"]], 22, mw, anchor="middle")
        b.append(t)
    b.append('</g>')

    # ---------------- 3 · matrioska delle scale
    b.append('<g id="scales">')
    fills = ["#FFFFFF", "#E3F1EF", "#C9E5E2", "#AFD9D5"]
    for i in range(4):
        x, y, w, h = 1290 + 30 * i, 160 + 62 * i, 594 - 60 * i, 440 - 92 * i
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{28 - 4 * i}" fill="{fills[i]}" stroke="{TEAL_D}" stroke-width="2.6"/>')
        b.append(lines(x + 24, y + 38, [S["scales"][i]], 26, w - 110, w=700, fill=SLATE))
        b.append(circ_icon(["area", "people", "road", "canyon"][i], x + w - 44, y + 29, r=24))
    b.append(lines(1290, 636, wrap([S["chain"]], 26, 594, 700), 26, 594, w=700, fill=TEAL_D))
    b.append('</g>')

    # ---------------- dimensione delle celle (NO2 vs PM2,5)
    b.append('<g id="resolution">')
    b.append(card(1290, 690, 594, 200))
    b.append(lines(1320, 734, [S["res_title"]], 28, 540, w=700, fill=TEAL_D))
    rows = [("road", [("n", "NO"), ("sub", "2"), ("n", S["res_no2"])], S["res_no2_val"], 795),
            ("grid", [("n", "PM"), ("sub", S["res_pm_sub"]), ("n", S["res_pm"])], S["res_pm_val"], 855)]
    for kind, parts, val, cy in rows:
        b.append(circ_icon(kind, 1342, cy - 6, r=26))
        b.append(tsub(1388, cy + 2, parts, 23))
        sym, num = val.split(" ", 1)          # "≤" a parte (font DejaVu): con anchor=end il tspan si sovrapponeva
        b.append(f'<text x="1676" y="{cy + 2}" font-size="30" font-weight="700" fill="{SLATE}" font-family="\'DejaVu Sans\',sans-serif">{sym}</text>')
        b.append(lines(1716, cy + 2, [num], 30, 140, w=700, fill=SLATE))
    b.append('</g>')

    # ---------------- fascia di definizione
    b.append(f'<rect x="36" y="910" width="1848" height="120" rx="28" fill="{TEAL_D}"/>')
    bw = width(S["band_bold"], 30, True)
    b.append(f'<text x="76" y="965" font-size="30" fill="#fff"><tspan font-weight="700">{esc(S["band_bold"])}</tspan> {esc(S["band_text"])}</text>')
    b.append(f'<text x="76" y="1007" font-size="30" fill="#fff">{esc(S["band_line2"])}</text>')
    for wd in (bw + width(" " + S["band_text"], 30), width(S["band_line2"], 30)):
        if wd > 1848 - 80:
            WARN.append(f"fascia troppo larga ({wd:.0f})")

    svg = svg_wrap("\n".join(b), S["alt_title"], " ".join(S["alt_desc"].split()), lang)
    render(svg, OUT / f"{STEM}_{lang}")

if __name__ == "__main__":
    for lg in (sys.argv[1:] or ["it", "en"]):
        build(lg)
    for m in WARN:
        print("ATTENZIONE:", m)
