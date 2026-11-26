#!/usr/bin/env python3
"""Infografica 04 – MQI e MQO (Dir. 2024/2881, Allegato V; documento tecnico CE, §3.4). Archetipo D: il target plot è l'elemento principale.

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non previsto
Testi in strings/<lingua>.yaml; geometrie e numeri qui. I 12 punti del target plot sono SINTETICI (esempio inventato, dichiarato)."""
import sys, pathlib
import numpy as np, yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
DOCH = "#8A5F0C"          # ocra scuro per il testo (contrasto)

# ------------------------------------------------------------------ valori normativi (PM10, media annua; vedi sources.md)
LV = 20.0                 # valore limite annuo, µg/m³
U_LV = 4.0                # incertezza max misure fisse al VL (= U_Ø per la media annua), µg/m³ (20 %)
BETA = 1.3                # rapporto max modello / misure fisse, PM10 lungo termine
XMAX, YMAX = 70.0, 20.0   # intervallo della figura 3-2 del documento tecnico

def u_fix(o):
    o = np.asarray(o, float)
    return np.where(o <= LV, U_LV, o * U_LV / LV)

UO_LV, UM_LV = float(u_fix(LV)), BETA * float(u_fix(LV))
DEN_LV = float(np.hypot(UO_LV, UM_LV))      # √(U_O² + U_M²) al VL

# ------------------------------------------------------------------ dati sintetici: (CRMSE normalizzato, bias normalizzato)
STATIONS = np.array([(-0.30, -0.15), (-0.18, -0.42), (0.25, -0.30), (-0.45, 0.20), (0.32, -0.46), (-0.52, -0.38),
                     (0.48, 0.30), (0.62, -0.52), (-0.70, 0.45), (0.55, 0.78), (-0.38, -0.85), (0.85, 0.72)])
MQI_ST = np.hypot(STATIONS[:, 0], STATIONS[:, 1])
P90 = float(np.percentile(MQI_ST, 90))
N_IN, N_ALL = int((MQI_ST <= 1).sum()), len(MQI_ST)
assert P90 <= 1.0 and N_IN / N_ALL >= 0.9, "esempio sintetico incoerente: l'MQO deve risultare soddisfatto"

def rich(txt):
    """'U_O' -> U con pedice O; il carattere dopo '_' diventa pedice."""
    parts, i = [], 0
    while i < len(txt):
        if txt[i] == "_" and i + 1 < len(txt):
            parts.append(("sub", txt[i + 1])); i += 2
        else:
            if parts and not isinstance(parts[-1], tuple): parts[-1] += txt[i]
            else: parts.append(txt[i])
            i += 1
    return parts

def tw(parts, size, w=400):
    tot = 0
    for p in parts:
        k, tx = p if isinstance(p, tuple) else ("n", p)
        tot += width(tx.replace(" ", "\u00a0"), size if k == "n" else size * 0.68, w == 700)
    return tot

def rtext(x, y, txt, size, w=400, fill=SLATE, anchor="start", maxw=None):
    parts = rich(txt)
    if maxw and tw(parts, size, w) > maxw: WARN.append(f"riga troppo larga ({tw(parts, size, w):.0f}>{maxw:.0f}): {txt}")
    return tsub(x, y, parts, size, w, fill, anchor)

def halo(x, y, s, size, w, fill, anchor="start"):
    return (T(x, y, s, size, w, "#fff", anchor, extra='stroke="#fff" stroke-width="6" stroke-linejoin="round"')
            + T(x, y, s, size, w, fill, anchor))

# ================================================================== sinistra: target plot (elemento principale)
def target(t, lang, x0, y0, w, h):
    s = ['<g id="target-plot">', card(x0, y0, w, h)]
    S = 640; L, Tp = x0 + 96, y0 + 22
    R1 = S / 2.6                                  # raggio del cerchio MQI = 1 (dominio ±1,3)
    cx, cy = L + S / 2, Tp + S / 2; Rt, B = L + S, Tp + S
    s.append(f'<rect x="{L}" y="{Tp}" width="{S}" height="{S}" fill="#fff" stroke="{GREY}" stroke-width="2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R1:.1f}" fill="{TEAL}" fill-opacity=".10"/>')
    s.append(f'<path d="M{L},{cy} H{Rt} M{cx},{Tp} V{B}" stroke="{SLATE}" stroke-width="1.8"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R1/2:.1f}" fill="none" stroke="{TEAL_D}" stroke-width="2.4" stroke-dasharray="7 6"/>')
    s.append(f'<circle id="mqo-circle" cx="{cx}" cy="{cy}" r="{R1:.1f}" fill="none" stroke="{TEAL_D}" stroke-width="4.4"/>')
    for v in (-1, -0.5, 0, 0.5, 1):
        lab = "0" if v == 0 else ("−" if v < 0 else "") + fmt(abs(v), 1 if abs(v) % 1 else 0, lang)
        xx, yy = cx + v * R1, cy - v * R1
        s.append(f'<path d="M{xx:.1f},{B} v-8 M{L},{yy:.1f} h8" stroke="{SLATE}" stroke-width="2"/>')
        s.append(T(xx, B + 24, lab, 19, 400, SLATE, "middle"))
        s.append(T(L - 10, yy + 7, lab, 19, 400, SLATE, "end"))
    s.append(T(cx, B + 56, t["axis_x3"], 21, 400, SLATE, "middle"))
    s.append(T(x0 + 36, cy, t["axis_y3"], 21, 400, SLATE, "middle", extra=f'transform="rotate(-90 {x0+36} {cy:.1f})"'))
    s.append(halo(cx + 8, cy - R1 - 9, t["circ1"], 22, 700, TEAL_D))
    s.append(halo(cx + 8, cy - R1 / 2 - 9, t["circ05"].replace("0,5", fmt(0.5, 1, lang)), 20, 400, TEAL_D))
    s.append(T(cx + 8, Tp + 24, t["bias_pos"], 20, 400, SLATE)); s.append(T(cx + 8, B - 10, t["bias_neg"], 20, 400, SLATE))
    s.append(T(L + 10, cy - 8, "R", 22, 700, SLATE)); s.append(T(Rt - 10, cy - 8, "SD", 22, 700, SLATE, "end"))
    for (xn, yn), m in zip(STATIONS, MQI_ST):
        s.append(dot(cx + xn * R1, cy - yn * R1, 10.5, OCHRE if m > 1 else TEAL, 'stroke="#fff" stroke-width="2.4"'))
    # colonna destra del riquadro
    rx = x0 + 764; av = w - 764 - 20
    s.append(T(rx, y0 + 46, t["tp_title"], 28, 700, TEAL_D))
    s.append(lines(rx, y0 + 74, [t["tp_sub"]], 21, av))
    svg, n = para(rx, y0 + 114, t["tp_desc"], 21, av); s.append(svg)
    s.append(lines(rx, y0 + 270, [t["count"].format(n=N_IN, N=N_ALL)], 25, av, w=700, fill=TEAL_D))
    s.append(dot(rx + 10, y0 + 306, 9, TEAL, 'stroke="#fff" stroke-width="2"')); s.append(T(rx + 30, y0 + 313, t["leg_in"], 21))
    s.append(dot(rx + 10, y0 + 340, 9, OCHRE, 'stroke="#fff" stroke-width="2"')); s.append(T(rx + 30, y0 + 347, t["leg_out"], 21))
    s.append(tsub(rx, y0 + 422, ["MQI", ("sub", "90"), " = " + fmt(P90, 2, lang)], 30, 700, TEAL_D))
    s.append(T(rx, y0 + 452, t["ex"], 20, 400, SLATE, it=True))
    s.append(f'<path d="M{rx},{y0+586} H{rx+av}" stroke="{GREY}" stroke-width="2"/>')
    s.append(dot(rx + 6, y0 + 621, 5.5, TEAL_D))
    svg, n = para(rx + 20, y0 + 628, [t["min_st"]], 20, av - 20, w=700, fill=TEAL_D); s.append(svg)
    if y0 + 628 + (n - 1) * 24.4 > y0 + h - 14: WARN.append("nota sulle 10 stazioni troppo lunga")
    return "".join(s) + "</g>"

# ================================================================== destra in alto: formula con simboli
def formula(t, x0, y0, w, h):
    s = ['<g id="formula">', card(x0, y0, w, h)]
    s.append(T(x0 + 30, y0 + 36, t["formula_cap"], 21, 400, SLATE))
    segs = [("MQI = ", TEAL_D), ("RMSE", RED_T), (" / ", SLATE), ("√(U_O² + U_M²)", DOCH)]
    x = x0 + 30
    for txt, col in segs:
        parts = rich(txt)
        s.append(tsub(x, y0 + 94, parts, 46, 700, col)); x += tw(parts, 46, 700)
    if x > x0 + w - 20: WARN.append(f"formula troppo larga: {x - x0:.0f}")
    for i, k in enumerate(("leg1", "leg2", "leg3")):
        s.append(rtext(x0 + 30, y0 + 134 + i * 27, t[k], 21, 400, SLATE, maxw=w - 60))
    return "".join(s) + "</g>"

# ================================================================== destra al centro: schema dell'incertezza ammessa (senza numeri)
def curve(t, lang, x0, y0, w, h):
    s = ['<g id="uncertainty-curve">', card(x0, y0, w, h)]
    s.append(T(x0 + 30, y0 + 42, t["c_title"], 25, 700, TEAL_D))
    px0, px1 = x0 + 56, x0 + w - 30; pyb, pyt = y0 + h - 84, y0 + 96
    X = lambda c: px0 + (px1 - px0) * c / XMAX
    Y = lambda u: pyb - (pyb - pyt) * u / YMAX
    s.append(f'<path d="M{px0},{pyt - 8} V{pyb} H{px1}" stroke="{SLATE}" stroke-width="2.4" fill="none"/>')
    s.append(T((px0 + px1) / 2, pyb + 34, t["c_x"], 21, 400, SLATE, "middle"))
    s.append(T(x0 + 28, (pyt + pyb) / 2, t["c_y"], 21, 400, SLATE, "middle", extra=f'transform="rotate(-90 {x0+28} {(pyt+pyb)/2:.1f})"'))
    cs = [0, LV, XMAX]
    pm = " ".join(f"{X(c):.1f},{Y(float(u_fix(c))):.1f}" for c in cs)
    pM = " ".join(f"{X(c):.1f},{Y(BETA * float(u_fix(c))):.1f}" for c in cs)   # schema: andamento, nessun valore numerico in figura
    s.append(f'<path d="M{X(LV):.1f},{pyt - 8} V{pyb}" stroke="{SLATE}" stroke-width="3" stroke-dasharray="9 6"/>')
    s.append(T(X(LV) - 8, pyt - 2, t["c_lv"], 20, 700, SLATE, "end"))
    s.append(f'<polyline points="{pm}" fill="none" stroke="{TEAL_D}" stroke-width="5.4" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(f'<polyline points="{pM}" fill="none" stroke="{OCHRE}" stroke-width="5.4" stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(rtext(px1, Y(float(u_fix(XMAX))) + 62, t["c_uo"], 22, 700, TEAL_D, "end"))
    s.append(rtext(px1, Y(BETA * float(u_fix(XMAX))) - 14, t["c_um"], 22, 700, DOCH, "end"))
    nx = X(LV) + 16; ny = pyt + 8
    s.append(T(nx, ny, t["c_note"], 21, 400, SLATE))
    return "".join(s) + "</g>"

# ================================================================== destra in basso: data fusion
def fusion(t, x0, y0, w, h):
    s = ['<g id="data-fusion">', card(x0, y0, w, h), circ_icon("grid", x0 + 64, y0 + h / 2, 36)]
    tx = x0 + 126; av = w - 126 - 24
    s.append(lines(tx, y0 + 52, [t["df1"]], 26, av, w=700, fill=TEAL_D))
    svg, n = para(tx, y0 + 90, [t["df2"]], 23, av); s.append(svg)
    return "".join(s) + "</g>"

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    if lang == "en": assert set(t) == set(yaml.safe_load((HERE / "strings" / "it.yaml").read_text(encoding="utf-8"))), "chiavi IT/EN diverse"
    LX, LW, TOP, HH = 36, 1020, 150, 740
    RX = LX + LW + 24; RW = 1884 - RX
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>', header(t["title"], t["subtitle"]),
            target(t, lang, LX, TOP, LW, HH),
            formula(t, RX, TOP, RW, 200),
            curve(t, lang, RX, TOP + 220, RW, 370),
            fusion(t, RX, TOP + 610, RW, 130)]
    if width(t["def_l1"], 27) + width(t["def_bold"], 27, True) > 1848 - 76: WARN.append("fascia, riga 1 troppo lunga")
    if width(t["def_l2"], 27) > 1848 - 76: WARN.append("fascia, riga 2 troppo lunga")
    body.append(f'<g id="definition">{band(36, 910, 1848, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>')
    desc = " ".join(t["alt_desc"].split()).format(p90=fmt(P90, 2, lang))
    svg = svg_wrap("\n".join(body), t["alt_title"], desc, lang, W, H)
    return render(svg, OUT / f"mqi_mqo_{lang}")

if __name__ == "__main__":
    for lang in [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]:
        print("scritto", build(lang).name)
    print("U_O(LV)=%.1f U_M(LV)=%.1f denominatore=%.2f | MQI90=%.3f | dentro: %d/%d" % (UO_LV, UM_LV, DEN_LV, P90, N_IN, N_ALL))
    for m in WARN: print("ATTENZIONE:", m)
