#!/usr/bin/env python3
"""Infografica 01 – Il ruolo della modellistica nella AAQD: cinque ambiti, un percorso (documento tecnico CE, §1.3, p. 14-16, fig. 1-1).

Uso:  python build.py [it|en]      # senza argomenti: it ed en; layout "wide" (16:9, slide)
Archetipo G (hub). Testi in strings/<lingua>.yaml; geometrie qui. Nessun dato numerico: la figura è concettuale.
Le tinte AMBITI (colore + icona per ambito) sono l'«indice» della serie: riusarle identiche nelle altre slide."""
import sys, math, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
STEM = "role_of_modelling"

# ---- indice della serie: colore e icona per ambito (tinte neutre, diverse da rosso/ocra che hanno significato fisso)
AMBITI = {
    "rete": ("pin",    "#3B78B0"),
    "val":  ("area",   "#2E9A78"),
    "sa":   ("source", "#8A62A8"),
    "pia":  ("doc",    "#C45A86"),
    "pre":  ("warn",   "#7C8B3A"),
}

CX, CY, RX, RY = 960, 515, 520, 268      # ellisse dei nodi
R_HUB, R_NODE = 104, 50
ANG = {"rete": -90, "val": -18, "sa": 54, "pia": 126, "pre": 198}   # senso orario, in gradi SVG

def pos(k, off=0):
    a = math.radians(ANG[k] + off)
    return CX + RX * math.cos(a), CY + RY * math.sin(a)

def head(x, y, dx, dy, col, L=26, wd=0.42):
    n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
    bx, by = x - dx * L, y - dy * L
    return f'<polygon points="{x:.1f},{y:.1f} {bx - dy * L * wd:.1f},{by + dx * L * wd:.1f} {bx + dy * L * wd:.1f},{by - dx * L * wd:.1f}" fill="{col}"/>'

def ellipse_arrow(k0, k1, col=TEAL_D, sw=7, gap0=64, gap1=62):
    """Freccia lungo l'ellisse dal nodo k0 al nodo k1 (taglia i tratti dentro i nodi)."""
    p0, p1 = pos(k0), pos(k1); a0, a1 = ANG[k0], ANG[k1]
    pts = []
    for i in range(0, 401):
        x, y = pos_t(a0 + (a1 - a0) * i / 400)
        if math.hypot(x - p0[0], y - p0[1]) >= gap0 and math.hypot(x - p1[0], y - p1[1]) >= gap1:
            pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-8])
    (xa, ya), (xb, yb) = pts[-9], pts[-1]
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
            + head(xb, yb, xb - xa, yb - ya, col))

def pos_t(a):
    r = math.radians(a)
    return CX + RX * math.cos(r), CY + RY * math.sin(r)

def node(k, n=None):
    kind, col = AMBITI[k]; x, y = pos(k)
    s = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R_NODE}" fill="{col}" fill-opacity=".15" stroke="{col}" stroke-width="4.5"/>',
         f'<g transform="translate({x:.1f},{y:.1f}) scale(1.25)">{icon(kind, 0, 0, col)}</g>']
    if n:
        s.append(badge(round(x - 40), round(y - 40), n, 19))
    return "".join(s)

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    if width(t["title"], 58, True) > 1824: WARN.append(f"titolo troppo largo ({lang})")
    if width(t["subtitle"], 30) > 1824: WARN.append(f"sottotitolo troppo largo ({lang})")
    b = [f'<rect width="{W}" height="{H}" fill="{BEIGE}"/>', header(t["title"], t["subtitle"])]

    # raggi dall'hub ai nodi
    sp = ['<g id="spokes">']
    for k in ANG:
        x, y = pos(k); n = math.hypot(x - CX, y - CY); ux, uy = (x - CX) / n, (y - CY) / n
        sp.append(f'<path d="M{CX + ux * (R_HUB + 6):.1f},{CY + uy * (R_HUB + 6):.1f} L{x - ux * (R_NODE + 6):.1f},{y - uy * (R_NODE + 6):.1f}" '
                  f'stroke="{AMBITI[k][1]}" stroke-opacity=".55" stroke-width="4" stroke-linecap="round"/>')
    b.append("".join(sp) + "</g>")

    # percorso di un superamento: valutazione -> source apportionment -> piani
    b.append('<g id="path">' + ellipse_arrow("val", "sa") + ellipse_arrow("sa", "pia") + "</g>")
    pw = pill_w(t["path_label"], True, 24)
    px, py = pos_t(90)
    b.append(pill(px - pw / 2, py - 17, t["path_label"], True, 24))

    # freccia di ritorno: source apportionment -> valutazione
    sx, sy = pos("sa"); vx, vy = pos("val")
    P0 = (sx + R_NODE + 4, sy + 2); C1 = (1560, 765); C2 = (1650, 575)
    P3 = (vx + R_NODE * math.cos(math.radians(72)) + 3, vy + R_NODE * math.sin(math.radians(72)) + 3)
    b.append('<g id="feedback">'
             f'<path d="M{P0[0]:.1f},{P0[1]:.1f} C{C1[0]},{C1[1]} {C2[0]},{C2[1]} {P3[0]:.1f},{P3[1]:.1f}" fill="none" stroke="{SLATE}" stroke-width="4" stroke-dasharray="3 10" stroke-linecap="round"/>'
             + head(P3[0], P3[1], P3[0] - C2[0], P3[1] - C2[1], SLATE, 22))
    s, _ = para(1604, 626, [t["back_label"]], 22, 270, fill=SLATE)
    b.append(s + "</g>")

    # hub
    b.append(f'<g id="hub"><circle cx="{CX}" cy="{CY}" r="{R_HUB}" fill="{TEAL_D}"/>'
             + T(CX, CY + 11, t["hub"], 32, 700, "#fff", "middle") + "</g>")

    # nodi
    for k, n in (("rete", None), ("val", 1), ("sa", 2), ("pia", 3), ("pre", None)):
        b.append(f'<g id="node_{k}">' + node(k, n) + "</g>")

    # etichette
    lab = ['<g id="labels">']
    x, y = pos("rete")
    lab.append(lines(x + R_NODE + 22, y - 6, [t["rete_name"]], 30, 300, 700, SLATE))
    lab.append(lines(x + R_NODE + 22, y + 28, [t["rete_q"]], 26, 380, 400, SLATE))
    lab.append(lines(x + R_NODE + 22, y + 60, [t["rete_tag"]], 21, 330, 400, SLATE, it=True))
    for k in ("val", "pre"):
        x, y = pos(k)
        lab.append(lines(x, y - R_NODE - 52, [t[f"{k}_name"]], 30, 360, 700, SLATE, anchor="middle"))
        lab.append(lines(x, y - R_NODE - 20, [t[f"{k}_q"]], 26, 520, 400, SLATE, anchor="middle"))
    x, y = pos("pre")
    lab.append(lines(x, y + R_NODE + 32, [t["pre_tag"]], 21, 360, 400, SLATE, it=True, anchor="middle"))
    x, y = pos("sa")
    lab.append(lines(x, y + R_NODE + 38, [t["sa_name"]], 30, 360, 700, SLATE, anchor="middle"))
    lab.append(lines(x, y + R_NODE + 68, [t["sa_gloss"]], 21, 380, 400, SLATE, it=True, anchor="middle"))
    lab.append(lines(x, y + R_NODE + 100, [t["sa_q"]], 26, 360, 400, SLATE, anchor="middle"))
    x, y = pos("pia")
    lab.append(lines(x, y + R_NODE + 38, [t["pia_name"]], 30, 360, 700, SLATE, anchor="middle"))
    lab.append(lines(x, y + R_NODE + 70, [t["pia_q"]], 26, 360, 400, SLATE, anchor="middle"))
    b.append("".join(lab) + "</g>")

    # spunta sul nodo Piani e riquadro di verifica
    x, y = pos("pia")
    bx, by, bw, bh = 50, 640, 480, 140
    ck = [f'<g id="check"><circle cx="{x + 40:.1f}" cy="{y - 40:.1f}" r="23" fill="#fff"/>' + icon("check", round(x + 40), round(y - 40), TEAL_D),
          f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="#fff" stroke="{TEAL_D}" stroke-width="2.6"/>',
          circ_icon("check", bx + 56, by + bh // 2, 32, TEAL_D),
          lines(bx + 108, by + 50, [t["check_head"]], 26, 340, 700, TEAL_D)]
    body = wrap([t["check_text"]], 24, 350)
    if len(body) > 3: WARN.append(f"check_text: {len(body)} righe ({lang})")
    ck.append(lines(bx + 108, by + 84, body, 24, 350))
    ck.append(arrow(bx + bw + 6, y, x - R_NODE - 10, y, TEAL_D, 4))
    b.append("".join(ck) + "</g>")

    svg = svg_wrap("\n".join(b), t["alt_title"], t["alt_desc"], t["lang"])
    render(svg, OUT / f"{STEM}_{lang}")

if __name__ == "__main__":
    for lg in (sys.argv[1:] or ["it", "en"]):
        build(lg)
    for m in WARN:
        print("ATTENZIONE:", m)
