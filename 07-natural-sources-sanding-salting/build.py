#!/usr/bin/env python3
"""Infografica 07 – Sorgenti naturali, sale e sabbia (documento tecnico CE, §3.7 e §5.3.4).
Archetipo F (albero decisionale). Nessun valore numerico: le altezze delle barre del riquadro «proiezioni» sono solo schematiche.

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide)
Testi in strings/<lingua>.yaml; geometrie qui."""
import sys, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
OCHRE_D = "#8A5F0C"

# ------------------------------------------------------------------ icone aggiuntive (stesso stile di layout.icon)
def cicon(kind, cx, cy, col=TEAL_D):
    st = f'fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
    P = {
        "fire": ('<path d="M2,-22 C4,-10 16,-6 16,6 A16,16 0 0 1 -16,6 C-16,-2 -10,-8 -6,-14 C-4,-8 0,-10 2,-22 Z"/>'
                 '<path d="M0,21 C-6,21 -8,16 -6,12 C-4,9 0,7 0,3 C4,7 7,11 5,16 C4,19 2,21 0,21 Z"/>'),
        "dust": ('<path d="M-22,-10 H6 A6,6 0 1 0 0,-16"/><path d="M-22,2 H14 A6,6 0 1 1 8,8"/><path d="M-22,14 H-2"/>'
                 f'<circle cx="14" cy="18" r="1.8" fill="{col}"/><circle cx="21" cy="12" r="1.8" fill="{col}"/>'),
        "volcano": '<path d="M-23,20 L-9,-6 H9 L23,20 Z"/><path d="M-4,-12 L-7,-21 M0,-14 V-24 M4,-12 L7,-21"/>',
        "salt": ('<path d="M-22,20 Q-8,-6 0,-6 Q8,-6 22,20 Z"/>'
                 f'<circle cx="-6" cy="-16" r="1.8" fill="{col}"/><circle cx="4" cy="-20" r="1.8" fill="{col}"/><circle cx="11" cy="-12" r="1.8" fill="{col}"/>'),
    }
    return f'<g transform="translate({cx},{cy})" {st}>{P[kind]}</g>'

def ico(kind, cx, cy, col=TEAL_D):
    return cicon(kind, cx, cy, col) if kind in ("fire", "dust", "volcano", "salt") else icon(kind, cx, cy, col)

# ------------------------------------------------------------------ primitive locali
def rbox(x, y, w, h, fill="#fff", fo=1, stroke=TEAL_D, sw=3, rx=24):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{fo}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')

def ctext(cx, cy, txt, size, maxw, w=400, fill=SLATE, lh=1.22):
    ls = wrap([txt], size, maxw, w); n = len(ls)
    return lines(cx, cy - (n - 1) * size * lh / 2 + size * 0.34, ls, size, maxw, w, fill, False, lh, "middle")

def ltext(x, cy, txt, size, maxw, w=400, fill=SLATE, lh=1.22):
    ls = wrap([txt], size, maxw, w); n = len(ls)
    return lines(x, cy - (n - 1) * size * lh / 2 + size * 0.34, ls, size, maxw, w, fill, False, lh, "start")

def seg(x1, y1, x2, y2, col=TEAL_D, sw=4):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>'

# ------------------------------------------------------------------ geometria
YA, YB, YC = 295, 570, 795          # centri delle tre righe dell'albero
X1, X2, X3 = 340, 750, 1100         # colonne: rami / nodo 2 e terminali / esiti del nodo 2

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    if width(t["subtitle"], 30) > 1830:
        WARN.append("sottotitolo troppo largo")
    g = []
    # --- nodo 1
    n1 = rbox(36, 470, 230, 200, TEAL_D, 1, TEAL_D) + ico("question", 151, 515, "#fff") + ctext(151, 600, t["n1"], 28, 200, 700, "#fff")
    g.append(f'<g id="node-1">{n1}</g>')
    # --- connettori dal nodo 1
    c = seg(266, YB, 303, YB) + seg(303, YA, 303, YC) + arrow(303, YA, X1 - 2, YA) + arrow(303, YC, X1 - 2, YC) + arrow(300, YB, X1 - 2, YB)
    g.append(f'<g id="branches">{c}</g>')
    # --- riga A: naturale
    a = card(X1, 160, 360, 270) + T(X1 + 26, 204, t["nat_h"], 27, 700, TEAL_D)
    kinds = ["fire", "wave", "dust", "volcano"]
    cells = [(X1 + 95, 248), (X1 + 265, 248), (X1 + 95, 346), (X1 + 265, 346)]
    for k, (cx, cy), lab in zip(kinds, cells, t["nat_ex"]):
        a += (f'<circle cx="{cx}" cy="{cy}" r="26" fill="{TEAL}" fill-opacity=".12"/>' + ico(k, cx, cy)
              + ctext(cx, cy + 50, lab, 20, 160))
    a += arrow(704, 245, X2 - 4, 245)
    a += rbox(X2, 190, 540, 110, TEAL, .18, TEAL_D) + ico("check", X2 + 56, 245) + lines(X2 + 110, 238, t["nat_term"], 28, 420, 700, TEAL_D, lh=1.15)
    a += rbox(X2, 320, 540, 90, OCHRE, .16, OCHRE) + T(X2 + 26, 354, t["nat_cond_b"], 22, 700, OCHRE_D)
    a += lines(X2 + 26, 384, [t["nat_cond"]], 22, 490, 400, SLATE)
    g.append(f'<g id="natural">{a}</g>')
    # --- riga B: sale e sabbia, nodo 2, esiti
    b = card(X1, 465, 360, 210) + ico("road", X1 + 50, 515) + ico("salt", X1 + 110, 517)
    b += lines(X1 + 26, 580, t["salt_h"], 28, 320, 700, TEAL_D, lh=1.15)
    b += lines(X1 + 26, 650, [t["salt_sub"]], 21, 320, 400, SLATE)
    b += arrow(704, YB, X2 - 4, YB)
    b += rbox(X2, 495, 260, 150, "#fff", 1, TEAL_D) + ctext(X2 + 130, YB, t["q2"], 23, 224, 700, TEAL_D)
    b += seg(1010, YB, 1050, YB) + seg(1050, YB, 1050, 520) + arrow(1050, 520, X3 - 2, 520)
    b += seg(1050, YB, 1050, 620, RED_T) + arrow(1050, 620, X3 - 2, 620, RED_T)
    b += T(1076, 506, t["y_lbl"], 22, 700, TEAL_D, "middle") + T(1076, 606, t["n_lbl"], 22, 700, RED_T, "middle")
    b += rbox(X3, 480, 190, 80, TEAL, .18, TEAL_D) + ctext(X3 + 95, 520, t["sub_term"], 24, 170, 700, TEAL_D)
    b += rbox(X3, 580, 190, 80, RED, .12, RED_T) + ctext(X3 + 95, 620, t["rem_term"], 22, 170, 700, RED_T)
    g.append(f'<g id="salt-sand">{b}</g>')
    # --- riga C: altra causa
    cc = card(X1, 735, 360, 120) + ico("source", X1 + 56, YC) + ltext(X1 + 110, YC, t["other_h"], 28, 230, 700, TEAL_D)
    cc += arrow(704, YC, X2 - 4, YC)
    cc += rbox(X2, 735, 540, 120, RED, .12, RED_T) + ico("warn", X2 + 56, YC, RED_T) + ltext(X2 + 110, YC, t["rem_term"], 28, 410, 700, RED_T)
    g.append(f'<g id="other">{cc}</g>')
    # --- riquadro «nelle proiezioni»
    p = card(1330, 160, 554, 705)
    p += f'<circle cx="1378" cy="214" r="26" fill="{TEAL}" fill-opacity=".12"/>' + icon("baseline", 1378, 214)
    p += T(1420, 226, t["proj_h"], 34, 700, TEAL_D)
    base = 540
    p += seg(1360, base, 1850, base, GREY, 3)
    for x, h, col, st in ((1380, 240, TEAL, TEAL_D), (1520, 240, TEAL, TEAL_D), (1700, 120, OCHRE, OCHRE_D)):
        p += f'<rect x="{x}" y="{base - h}" width="90" height="{h}" rx="8" fill="{col}" fill-opacity=".35" stroke="{st}" stroke-width="3"/>'
    p += arrow(1476, 420, 1514, 420, TEAL_D, 3)
    s1, _ = para(1495, 592, [t["cap_same"]], 21, 250, anchor="middle")
    s2, _ = para(1745, 592, [t["cap_cut"]], 21, 230, anchor="middle")
    p += s1 + s2
    p += rbox(1360, 735, 494, 100, OCHRE, .16, OCHRE) + ico("gear", 1404, 785, OCHRE_D) + ltext(1446, 785, t["note"], 21, 390)
    g.append(f'<g id="projections">{p}</g>')
    # --- fascia di definizione
    g.append(f'<g id="definition">{band_wrapped(36, 930, 1848, 90, t["def_bold"], t["def_text"], 27, 140)}</g>')
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>', header(t["title"], t["subtitle"])] + g
    svg = svg_wrap("\n".join(body), t["alt_title"], " ".join(t["alt_desc"].split()), lang, W, H)
    return render(svg, OUT / f"natural_sources_sanding_salting_{lang}")

if __name__ == "__main__":
    for lang in [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]:
        print("scritto", build(lang).name)
    for m in WARN:
        print("ATTENZIONE:", m)
