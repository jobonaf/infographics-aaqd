#!/usr/bin/env python3
"""Infografica 01 – Rappresentatività spaziale di un punto di campionamento (Dir. 2024/2881, Dec. es. 2026/1208).

Uso:  python build.py                  # IT + EN, layout "wide" (16:9, slide) e "mobile" (verticale, smartphone)
      python build.py en mobile        # solo inglese, solo layout verticale
Tutti i testi stanno in strings/<lingua>.yaml; geometrie e numeri sono calcolati qui, quindi lingue e layout
non possono divergere. I dati della mappa sono SINTETICI."""
import sys, pathlib
import numpy as np, yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ mappa sintetica (celle, coordinate in unità-cella)
N = 20
ZONE_POLY = [(1.0, 3.0), (4.0, 0.5), (9.5, 0.3), (13.0, 1.2), (15.6, 2.4), (18.2, 0.8), (19.4, 5.5), (19.0, 10.5),
             (19.2, 15.0), (14.0, 17.5), (9.5, 19.2), (3.5, 18.0), (0.8, 12.0), (2.8, 8.0)]
ROAD = [(8.2, -0.6), (7.6, 3.0), (6.5, 6.0), (7.0, 9.0), (7.8, 12.0), (7.0, 15.5), (6.0, 19.8)]
PATCH = [(13.5, 8.5), (16.5, 8.5), (16.5, 11.5), (14.5, 11.5), (14.5, 10.5), (13.5, 10.5)]   # bordi a metà cella: non tagliano mai un punto
STA, STB = (4, 6), (13, 13)

def components(mask, seeds):
    """Componenti connesse (8 vicini) che contengono almeno un seme: l'area è ancorata alla stazione
    o a isole dichiarate (area non contigua); i residui isolati vengono scartati."""
    keep, h, w = np.zeros_like(mask), *mask.shape
    for sx, sy in seeds:
        if not mask[sy, sx] or keep[sy, sx]: continue
        stack = [(sx, sy)]; keep[sy, sx] = True
        while stack:
            x, y = stack.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    a, b = x + dx, y + dy
                    if 0 <= a < w and 0 <= b < h and mask[b, a] and not keep[b, a]:
                        keep[b, a] = True; stack.append((a, b))
    return keep

def build_map():
    c, r = np.meshgrid(np.arange(N), np.arange(N))
    sg = lambda cx, cy, sd, p=5: np.exp(-(np.hypot(c - cx, r - cy) / sd) ** p)      # picco a "cappello"
    F = (12 + 17 * sg(5.8, 6.4, 4.6) + 8 * sg(13, 13, 5.0) + 2.5 * sg(15.8, 9.4, 3.0)
         + 17 * sg(3.0, 14.2, 1.5) + 8 * sg(11.2, 4.2, 1.7) + 0.5 * np.sin(c / 2.3) * np.cos(r / 2.9))
    CA, CB = F[STA[1], STA[0]], F[STB[1], STB[0]]
    tol = lambda C: max(0.15 * C, 2.0)                                   # PM10: minimo di Allegato I = 2 µg/m³
    inA, inB = abs(F - CA) <= tol(CA), abs(F - CB) <= tol(CB)
    toA = np.where(inA & inB, abs(F - CA) <= abs(F - CB), inA)           # cella in entrambi gli intervalli: valore più vicino
    areaA = components(inA & toA, [STA, (3, 14)])
    areaB = components(inB & ~toA, [STB, (11, 4)])
    dense, _ = catmull(ROAD)
    dr = np.array([[min(np.hypot(ci - x, ri - y) for x, y in dense[::3]) for ci in range(N)] for ri in range(N)])
    near_road = dr <= 1.05                                               # fascia di esclusione attorno alla strada (in celle)
    in_patch = np.array([[point_in_poly(ci, ri, PATCH) for ci in range(N)] for ri in range(N)])
    inzone = np.array([[point_in_poly(ci, ri, ZONE_POLY) for ci in range(N)] for ri in range(N)])
    excl = (areaA | areaB) & (near_road | in_patch) & inzone
    for s_ in (STA, STB): excl[s_[1], s_[0]] = False
    return dict(CA=CA, CB=CB, areaA=areaA & inzone & ~excl, areaB=areaB & inzone & ~excl, excl=excl, inzone=inzone)

def draw_map(M, px, py, S):
    """Zona, celle, strada, riquadro esperti, confine e stazioni; px/py convertono celle → pixel."""
    rr, rs, rx = 0.365 * S, 0.18 * S, 0.35 * S
    poly = " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in ZONE_POLY)
    s = [f'<defs><clipPath id="zoneclip"><polygon points="{poly}"/></clipPath></defs>',
         f'<polygon id="zone" points="{poly}" fill="{ZONE}"/>']
    dots = []
    for r in range(N):
        for c in range(N):
            if not M["inzone"][r, c]: continue
            x, y = px(c), py(r)
            if M["areaA"][r, c]: dots.append(dot(x, y, rr, TEAL))
            elif M["areaB"][r, c]: dots.append(dot(x, y, rr, OCHRE))
            elif M["excl"][r, c]: dots.append(excluded(x, y, rx))
            else: dots.append(dot(x, y, rs, GREY, 'fill-opacity=".85"'))
    s.append('<g id="cells">' + "".join(dots) + "</g>")
    _, road_d = catmull([(px(a), py(b)) for a, b in ROAD])
    s.append(f'<g clip-path="url(#zoneclip)"><path id="road" d="{road_d}" fill="none" stroke="{SLATE}" stroke-width="{S*0.155:.1f}" stroke-linecap="round" stroke-linejoin="round"/></g>')
    pp = " ".join(f"{px(a):.1f},{py(b):.1f}" for a, b in PATCH)
    s.append(f'<polygon id="expert-patch" points="{pp}" fill="none" stroke="{SLATE}" stroke-width="2.4" stroke-dasharray="8 6" stroke-linejoin="round"/>')
    s.append(f'<polygon id="zone-boundary" points="{poly}" fill="none" stroke="{SLATE}" stroke-width="2.8" stroke-dasharray="11 7" stroke-linejoin="round"/>')
    s.append(station(px(STA[0]), py(STA[1]), "A") + station(px(STB[0]), py(STB[1]), "B"))
    return "".join(s)

def draw_legend(t, lx, ty, step, size, S, oneline=False):
    rr, rs, rx = 0.365 * S, 0.18 * S, 0.35 * S
    s = []
    for k, (kind, key) in enumerate([("A", "leg_A"), ("B", "leg_B"), ("x", "leg_excl"), ("s", "leg_not"), ("z", "leg_zone"), ("r", "leg_station")]):
        y = ty + k * step
        if kind == "A": s.append(dot(lx, y, rr, TEAL))
        elif kind == "B": s.append(dot(lx, y, rr, OCHRE))
        elif kind == "x": s.append(excluded(lx, y, rx))
        elif kind == "s": s.append(dot(lx, y, rs, GREY))
        elif kind == "z": s.append(f'<path d="M{lx-14},{y} h28" stroke="{SLATE}" stroke-width="2.8" stroke-dasharray="8 5"/>')
        else: s.append(dot(lx, y, 11.5, RED, 'stroke="#fff" stroke-width="2.5"'))
        ln = [" ".join(t[key])] if oneline else t[key]
        s.append(T(lx + 26 + (size - 20) * 0.5, y + (size * 0.35 if len(ln) == 1 else -size * 0.15), ln, size, 400, SLATE, lh=1.15))
    return "".join(s)

def icon_instrument(cx, iy, k=1.0):
    return (f'<g fill="none" stroke="{TEAL_D}" stroke-width="{3.2*k:.1f}" stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="{cx-13*k:.1f}" y="{iy-4*k:.1f}" width="{26*k:.1f}" height="{44*k:.1f}" rx="{3*k:.1f}"/>'
            + "".join(f'<path d="M{cx-13*k:.1f},{iy+(6+n*9)*k:.1f} h{9*k:.1f}"/>' for n in range(4)) +
            f'<circle cx="{cx+9*k:.1f}" cy="{iy-14*k:.1f}" r="{7*k:.1f}"/><path d="M{cx+9*k:.1f},{iy-7*k:.1f} v{3*k:.1f}"/></g>')

def icon_models(cx, iy, k=1.0):
    return "".join(f'<rect x="{cx-21*k+a*15*k:.1f}" y="{iy-10*k+b*15*k:.1f}" width="{12*k:.1f}" height="{12*k:.1f}" rx="{2*k:.1f}" fill="{TEAL if (a+b)%2 else TEAL_D}"/>'
                   for a in range(3) for b in range(3))

def scale_bars(s, t, X, top, C, lo, hi, cap_a, cap_b, cx, fs):
    """Una scala 0–30 µg/m³ con intervallo [lo, hi] e marker in C; fs = dimensioni font."""
    ay = top + 15
    s.append(f'<path d="M{X(0)},{ay} H{X(30)}" stroke="{SLATE}" stroke-width="2.4"/>')
    for v in (0, 10, 20, 30):
        s.append(f'<path d="M{X(v)},{top} V{top+30}" stroke="{SLATE}" stroke-width="2.4"/>')
        s.append(T(X(v), top + fs["tick_dy"], str(v), fs["tick"], 400, SLATE, "middle"))
    s.append(f'<rect x="{X(lo)}" y="{top}" width="{X(hi)-X(lo)}" height="30" fill="{TEAL}" fill-opacity=".92"/>')
    s.append(f'<path d="M{X(lo)},{ay} H{X(hi)}" stroke="{SLATE}" stroke-width="2.4"/>')
    s.append(f'<rect x="{X(C)-2.5}" y="{top-9}" width="5" height="48" fill="{RED}"/>')
    s.append(T(X(C), top - fs["c_dy"], f"C = {C}", fs["c"], 700, RED_T, "middle"))
    s.append(T(cx, top + fs["a_dy"], cap_a, fs["cap"], 400, SLATE, "middle"))
    s.append(T(cx, top + fs["b_dy"], cap_b, fs["capb"], 700, TEAL_D, "middle"))

# ================================================================== layout "wide" (1920×1080, slide)
def panel1(t, x0=48, y0=170):
    s = [f'<g id="panel1">', panel(x0, y0, 440, 710, 1, t["h1"])]
    s.append(T(x0 + 220, y0 + 130, t["central_value"], 32, 700, RED_T, "middle"))
    gx, gy, step = 84, 336, 34
    for i in range(7):
        for j in range(7):
            if (i, j) != (4, 3): s.append(dot(gx + i * step, gy + j * step, 10, GREY))
    sx, sy = gx + 4 * step, gy + 3 * step
    s.append(f'<path d="M{sx+9},{sy-7} L{sx+84},{sy-36}" stroke="{SLATE}" stroke-width="2" fill="none"/>')
    s.append(dot(sx, sy, 12, RED, 'stroke="#fff" stroke-width="2.5"'))
    s.append(T(sx + 90, sy - 40, t["sampling_point"], 22))
    cx1, cx2, iy = 163, 373, 596
    s.append(icon_instrument(cx1, iy) + icon_models(cx2, iy))
    s.append(T(cx1, iy + 74, t["meas_head"], 23, 700, SLATE, "middle") + T(cx1, iy + 102, t["meas_body"], 22, 400, SLATE, "middle"))
    s.append(T(cx2, iy + 74, t["model_head"], 23, 700, SLATE, "middle") + T(cx2, iy + 102, t["model_body"], 22, 400, SLATE, "middle"))
    s.append(T(x0 + 220, y0 + 640, t["other_metrics"], 22, 400, SLATE, "middle", it=True))
    s.append(T(x0 + 220, y0 + 680, t["via"], 26, 700, SLATE, "middle"))
    return "".join(s) + "</g>"

def panel2(t, x0=558, y0=170):
    s = [f'<g id="panel2">', panel(x0, y0, 480, 710, 2, t["h2"])]
    cx = x0 + 240
    s.append(T(cx, y0 + 122, t["formula"], 28, 700, SLATE, "middle"))
    s.append(T(cx, y0 + 208, t["example"], 22, 400, SLATE, "middle", it=True))
    X = lambda v: 618 + 12.0 * v                                          # 0–30 µg/m³ → 360 px (proporzioni esatte)
    fs = dict(tick=22, tick_dy=64, c=27, c_dy=22, cap=24, capb=26, a_dy=108, b_dy=142)
    scale_bars(s, t, X, y0 + 292, 20, 17, 23, t["cap1a"], t["cap1b"], cx, fs)
    scale_bars(s, t, X, y0 + 514, 10, 8, 12, t["cap2a"], t["cap2b"], cx, fs)
    return "".join(s) + "</g>"

def panel3(t, M, x0=1108, y0=170):
    S, gx0, gy0 = 26, 1150, 262
    px, py = (lambda c: gx0 + c * S), (lambda r: gy0 + r * S)
    s = [f'<g id="panel3">', panel(x0, y0, 764, 710, 3, t["h3"]), draw_map(M, px, py, S)]
    s.append(T(1396, y0 + 62, t["road"], 22, 400, SLATE))
    s.append(f'<path d="M1390,{y0+56} L{px(8.0)+2},{py(0.5)-2}" stroke="{SLATE}" stroke-width="1.8" fill="none"/>')
    s.append(T(1692, y0 + 170, t["expert"], 21, 400, SLATE))
    s.append(f'<path d="M1700,{y0+232} L{px(16.5)+4},{py(9.5)-4}" stroke="{SLATE}" stroke-width="1.8" fill="none"/>')
    lx = 1690
    s.append(draw_legend(t, lx, y0 + 290, 54, 20, S))
    ry = y0 + 618
    s.append(arc_arrow(lx, ry, 13, 200, 340, TEAL_D) + arc_arrow(lx, ry, 13, 20, 160, TEAL_D))
    s.append(T(lx + 26, ry - 2, t["review"], 22, 700, SLATE, lh=1.15))
    s.append(T(x0 + 30, y0 + 668, t["synthetic"], 20, 400, SLATE, it=True))
    s.append(T(x0 + 764 - 30, y0 + 668, t["refinement"], 21, 400, SLATE, "end"))
    return "".join(s) + "</g>"

def layout_wide(t, M):
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 86, t["title"], 58, 700, TEAL_D), T(48, 134, t["subtitle"], 30, 400, SLATE),
            panel1(t), block_arrow(523, 525), panel2(t), block_arrow(1073, 525), panel3(t, M),
            f'<g id="definition">{band(48, 910, 1824, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    return "\n".join(body), W, H

# ================================================================== layout "mobile" (1200×1960, schermo verticale)
# Testo minimo 29 px su 1200 (≥ 2,4 % della larghezza): leggibile anche su uno schermo di 390 px.
def panel1_m(t, x0, y0, w=550, h=720):
    s = [f'<g id="panel1">', panel(x0, y0, w, h, 1, t["h1"], hs=40)]
    s.append(T(x0 + w / 2, y0 + 128, t["central_value"], 38, 700, RED_T, "middle"))
    gx, gy, step = x0 + 40, y0 + 168, 34
    for i in range(7):
        for j in range(7):
            if (i, j) != (4, 3): s.append(dot(gx + i * step, gy + j * step, 10, GREY))
    sx, sy = gx + 4 * step, gy + 3 * step
    s.append(f'<path d="M{sx+10},{sy-8} L{sx+86},{sy-40}" stroke="{SLATE}" stroke-width="2.4" fill="none"/>')
    s.append(dot(sx, sy, 12.5, RED, 'stroke="#fff" stroke-width="2.5"'))
    s.append(T(sx + 92, sy - 38, t["sampling_point"], 32))
    cx1, cx2, iy = x0 + w * 0.27, x0 + w * 0.73, y0 + 425
    s.append(icon_instrument(cx1, iy, 1.25) + icon_models(cx2, iy, 1.25))
    s.append(T(cx1, iy + 92, t["meas_head"], 32, 700, SLATE, "middle") + T(cx1, iy + 130, t["meas_body"], 30, 400, SLATE, "middle"))
    s.append(T(cx2, iy + 92, t["model_head"], 32, 700, SLATE, "middle") + T(cx2, iy + 130, t["model_body"], 30, 400, SLATE, "middle"))
    s.append(T(x0 + w / 2, y0 + 680, t["other_metrics"], 30, 400, SLATE, "middle", it=True))
    return "".join(s) + "</g>"

def panel2_m(t, x0, y0, w=550, h=720):
    s = [f'<g id="panel2">', panel(x0, y0, w, h, 2, t["h2"], hs=40)]
    cx = x0 + w / 2
    s.append(T(cx, y0 + 128, t["formula"], 34, 700, SLATE, "middle", lh=1.2))
    s.append(T(cx, y0 + 226, t["example"], 30, 400, SLATE, "middle", it=True))
    X = lambda v: x0 + 55 + 440 / 30 * v                                  # 0–30 µg/m³ → 440 px
    fs = dict(tick=30, tick_dy=62, c=36, c_dy=26, cap=30, capb=34, a_dy=110, b_dy=152)
    scale_bars(s, t, X, y0 + 304, 20, 17, 23, t["cap1a"], t["cap1b"], cx, fs)
    scale_bars(s, t, X, y0 + 534, 10, 8, 12, t["cap2a"], t["cap2b"], cx, fs)
    return "".join(s) + "</g>"

def panel3_m(t, M, x0, y0, w=1120, h=720):
    S, gx0, gy0 = 25, x0 + 70, y0 + 130
    px, py = (lambda c: gx0 + c * S), (lambda r: gy0 + r * S)
    s = [f'<g id="panel3">', panel(x0, y0, w, h, 3, t["h3"], hs=40), draw_map(M, px, py, S)]
    s.append(T(px(8.0) + 34, y0 + 62, t["road"], 30, 400, SLATE))
    s.append(f'<path d="M{px(8.0)+28},{y0+54} L{px(8.0)+2},{py(0.5)-2}" stroke="{SLATE}" stroke-width="2.2" fill="none"/>')
    s.append(T(x0 + 640, y0 + 165, t["expert"], 30, 400, SLATE))
    s.append(f'<path d="M{x0+650},{y0+250} L{px(16.5)+4},{py(9.5)-4}" stroke="{SLATE}" stroke-width="2.2" fill="none"/>')
    lx = x0 + 668
    s.append(draw_legend(t, lx, y0 + 330, 52, 30, S, oneline=True))
    ry = y0 + 330 + 6 * 52 + 6
    s.append(arc_arrow(lx, ry, 16, 200, 340, TEAL_D, 3.8) + arc_arrow(lx, ry, 16, 20, 160, TEAL_D, 3.8))
    s.append(T(lx + 36, ry + 11, " ".join(t["review"]), 32, 700, SLATE))
    s.append(T(gx0 - 30, y0 + 652, t["synthetic"], 28, 400, SLATE, it=True))
    s.append(T(gx0 - 30, y0 + 694, t["refinement"], 29, 400, SLATE))
    return "".join(s) + "</g>"

def layout_mobile(t, M):
    Wm, Hm = 1200, 1960
    d = t["def_bold"], " ".join([t["def_l1"], t["def_l2"]])
    body = [f'<rect id="background" width="{Wm}" height="{Hm}" fill="{BEIGE}"/>',
            T(40, 80, t["title_m"], 56, 700, TEAL_D, lh=1.14), T(40, 200, t["subtitle_m"], 30, 400, SLATE),
            panel1_m(t, 40, 265), panel2_m(t, 610, 265), panel3_m(t, M, 40, 1005),
            f'<g id="definition">{band_wrapped(40, 1745, 1120, 170, d[0], d[1], 29, 88)}</g>']
    return "\n".join(body), Wm, Hm

# ------------------------------------------------------------------ build
LAYOUTS = {"wide": (layout_wide, "", 3840), "mobile": (layout_mobile, "_mobile", 2400)}

def build(lang, M, layout):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    fn, suffix, png_w = LAYOUTS[layout]
    body, w, h = fn(t, M)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"spatrep_{lang}{suffix}"
    stem.with_suffix(".svg").write_text(svg, encoding="utf-8")
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(stem.with_suffix(".png")), output_width=png_w)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(stem.with_suffix(".pdf")))
    except ImportError:
        print("cairosvg non installato: generato solo l'SVG")
    return stem

if __name__ == "__main__":
    args = sys.argv[1:]
    langs = [a for a in args if a in ("it", "en")] or ["it", "en"]
    lays = [a for a in args if a in LAYOUTS] or list(LAYOUTS)
    M = build_map()
    print("C_A=%.1f C_B=%.1f | celle A=%d B=%d escluse=%d" % (M["CA"], M["CB"], M["areaA"].sum(), M["areaB"].sum(), M["excl"].sum()))
    for lang in langs:
        for lay in lays:
            print("scritto", build(lang, M, lay).name)
