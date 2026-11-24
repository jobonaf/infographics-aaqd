#!/usr/bin/env python3
"""Infografica 03 – Fitness-for-purpose (v3, archetipo G «hub»; documento tecnico CE, §1.5, §3.3, §3.4.5).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non previsto
Testi in strings/<lingua>.yaml; geometrie qui. Nessun dato numerico: la figura è concettuale."""
import sys, math, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
OCHRE_D = "#8A5F0C"

HUB_C, HUB_R = (960, 450), 215
CARD_W, CARD_H = 560, 150
LEFT_X, RIGHT_X = 36, 1324
ICONS = ["grid", "gear", "source", "wave", "check", "doc"]
ROW_ICONS = ["pin", "area", "road", "flag", "wave"]

def node(gid, x, cy, kind, label, gloss=None):
    y = cy - CARD_H / 2
    out = [f'<g id="{gid}">', card(x, y, CARD_W, CARD_H, rx=28), circ_icon(kind, x + 60, cy, r=36)]
    tx, maxw = x + 118, CARD_W - 118 - 24
    g_ls = wrap([gloss], 21, maxw) if gloss else []
    total = 34 + (8 + len(g_ls) * 26 if g_ls else 0)
    top = cy - total / 2
    out.append(lines(tx, top + 28, [label], 31, maxw, w=700, fill=TEAL_D))
    if g_ls:
        out.append(lines(tx, top + 34 + 8 + 20, g_ls, 21, maxw, fill=SLATE, lh=1.24))
    out.append("</g>")
    return "".join(out)

def build(lang):
    s = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    cx0, cy0 = HUB_C
    body = [f'<rect width="{W}" height="{H}" fill="{BEIGE}"/>', header(s["title"], s["subtitle"])]
    WARN_BEFORE = len(WARN)

    cys = [250, 450, 650]
    slots = [(LEFT_X, cys[0]), (LEFT_X, cys[1]), (LEFT_X, cys[2]), (RIGHT_X, cys[0]), (RIGHT_X, cys[1]), (RIGHT_X, cys[2])]
    # raggi (sotto cerchio e riquadri)
    body.append('<g id="spokes">')
    for x, cy in slots:
        sx = x + CARD_W if x == LEFT_X else x
        vx, vy = sx - cx0, cy - cy0
        d = math.hypot(vx, vy)
        ex, ey = cx0 + vx / d * HUB_R, cy0 + vy / d * HUB_R
        body.append(f'<path d="M{sx},{cy} L{ex:.1f},{ey:.1f}" stroke="{TEAL_D}" stroke-width="5" stroke-linecap="round"/>')
        body.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="8" fill="{TEAL_D}"/>')
    body.append("</g>")

    # centro
    body.append('<g id="hub">')
    body.append(f'<circle cx="{cx0}" cy="{cy0}" r="{HUB_R}" fill="#fff" stroke="{TEAL_D}" stroke-width="7"/>')
    body.append(lines(cx0, cy0 - 100, s["hub"], 46, 2 * HUB_R - 80, w=700, fill=TEAL_D, anchor="middle", lh=1.15))
    # cerchio piccolo: MQO
    mc = (cx0, cy0 + 96); mr = 98
    body.append(f'<circle cx="{mc[0]}" cy="{mc[1]}" r="{mr}" fill="{OCHRE}" fill-opacity=".16" stroke="{OCHRE}" stroke-width="5"/>')
    body.append(lines(mc[0], mc[1] - 24, s["mqo_circle"], 24, 2 * mr - 28, w=700, fill=OCHRE_D, anchor="middle", lh=1.3))
    body.append("</g>")

    # sei criteri
    body.append('<g id="criteria">')
    for i, ((x, cy), kind, label) in enumerate(zip(slots, ICONS, s["crit"])):
        body.append(node(f"criterion-{i+1}", x, cy, kind, label, s["gloss"][i] or None))
    body.append("</g>")

    # riga degli ambiti
    ry, rh = 762, 136
    body.append('<g id="domains">' + card(36, ry, 1848, rh, rx=28))
    body.append(lines(76, ry + 52, s["row_label"], 28, 470, w=700, fill=TEAL_D, lh=1.2))
    body.append(f'<path d="M600,{ry+22} V{ry+rh-22}" stroke="{GREY}" stroke-width="2.6" stroke-linecap="round"/>')
    n = len(s["row_items"]); x0, x1 = 640, 1860; step = (x1 - x0) / n
    for i, (kind, lab) in enumerate(zip(ROW_ICONS, s["row_items"])):
        cx = x0 + step * (i + .5)
        body.append(circ_icon(kind, cx, ry + 40, r=32))
        base = ry + 96 if len(lab) == 2 else ry + 108
        body.append(lines(cx, base, lab, 23, step - 14, w=700, fill=SLATE, anchor="middle", lh=1.15))
    body.append("</g>")

    # fascia input
    by, bh = 916, 104
    body.append(f'<g id="inputs"><rect x="36" y="{by}" width="1848" height="{bh}" rx="28" fill="{TEAL_D}"/>')
    body.append(f'<g transform="translate(110,{by+bh/2}) scale(1.35)">{icon("check", 0, 0, "#fff")}</g>')
    full = s["band_pre"] + s["band_bold"] + s["band_post"]
    if width(full, 40, True) > 1848 - 200:
        WARN.append("fascia in basso troppo larga")
    body.append(f'<text x="170" y="{by+bh/2+14}" font-size="40" fill="#fff"><tspan>{esc(s["band_pre"])}</tspan>'
                f'<tspan font-weight="700" text-decoration="underline">{esc(s["band_bold"])}</tspan><tspan>{esc(s["band_post"])}</tspan></text></g>')

    svg = svg_wrap("\n".join(body), s["alt_title"], " ".join(s["alt_desc"].split()), lang)
    render(svg, OUT / f"fitness_for_purpose_{lang}")

if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["it", "en"]):
        build(lang)
    for m in WARN:
        print("ATTENZIONE:", m)
