#!/usr/bin/env python3
"""Infografica 06 – Progettazione della rete di monitoraggio (documento tecnico CE, §2.3).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide)
Testi in strings/<lingua>.yaml; geometrie qui. Mappa, fasce di concentrazione e gruppi MoNET sono SCHEMATICI (inventati)."""
import sys, pathlib, random
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *
from layout import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
LEV = ("#FBE6E1", "#F4BDB4", "#E6867C")      # tre fasce di concentrazione modellata (bassa -> alta)
ZONE_FILL = "#EEF3F1"
CX = 0.67                                     # frazione della larghezza della mappa occupata dalla città
MX, MY, MW, MH = 50, 164, 1102, 712           # mappa dentro la card (36,150,1130,740)


def station_dot(x, y):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{RED}" stroke="#fff" stroke-width="3.2"/>'


def tag(x, y, label, col=TEAL_D, size=22):
    w = width(label, size, True) + 24; h = size + 14
    return (f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="#fff" stroke="{col}" stroke-width="2.4"/>'
            + T(f"{x:.1f}", f"{y+size*0.35:.1f}", label, size, 700, col, "middle"))


def draw_map(t):
    mx, my, mw, mh = MX, MY, MW, MH
    F = lambda pts: [(mx + px * CX * mw, my + py * mh) for px, py in pts]   # coordinate nella città
    A = lambda pts: [(mx + px * mw, my + py * mh) for px, py in pts]        # coordinate assolute nella mappa
    c = lambda px, py: (mx + px * CX * mw, my + py * mh)
    zone = F([(0.02, 0.34), (0.10, 0.12), (0.26, 0.18), (0.40, 0.03), (0.62, 0.08), (0.74, 0.02), (0.93, 0.16), (0.99, 0.40), (0.90, 0.58), (0.97, 0.80), (0.76, 0.97), (0.54, 0.90), (0.36, 0.99), (0.14, 0.88), (0.04, 0.66)])
    main = F([(0.0, 0.62), (0.14, 0.56), (0.30, 0.60), (0.46, 0.52), (0.62, 0.58), (0.78, 0.50), (1.0, 0.44)])
    ns = F([(0.44, 0.0), (0.47, 0.18), (0.45, 0.34), (0.50, 0.52), (0.55, 0.72), (0.52, 1.0)])
    east = F([(0.70, 0.04), (0.74, 0.28), (0.79, 0.50), (0.88, 0.74), (0.92, 1.0)])
    diag = F([(0.04, 0.20), (0.22, 0.30), (0.36, 0.40), (0.47, 0.52)])
    loc1 = F([(0.36, 0.585), (0.35, 0.46), (0.31, 0.34)])
    loc2 = F([(0.62, 0.575), (0.65, 0.68), (0.63, 0.80)])
    loc3 = F([(0.30, 0.60), (0.27, 0.72), (0.31, 0.84)])
    loc4 = F([(0.55, 0.555), (0.58, 0.40), (0.62, 0.26)])
    ext = [c(0.88, 0.47)] + A([(0.80, 0.43), (1.0, 0.41)])
    river = A([(0.0, 0.88), (0.14, 0.82), (0.28, 0.90), (0.45, 0.86), (0.60, 0.96), (0.75, 0.90), (1.0, 0.94)])
    veg1 = F([(0.07, 0.62), (0.14, 0.50), (0.27, 0.54), (0.30, 0.70), (0.20, 0.78), (0.09, 0.74)])
    veg2 = F([(0.80, 0.14), (0.90, 0.20), (0.92, 0.34), (0.82, 0.38), (0.74, 0.26)])
    vegr = A([(0.74, 0.03), (0.90, 0.02), (0.985, 0.09), (0.93, 0.18), (0.78, 0.15)])
    s = ['<g id="map">', card(36, 150, 1130, 740),
         f'<defs><clipPath id="map-clip"><rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="20"/></clipPath>'
         f'<clipPath id="zone-clip"><path d="{smooth(zone, True)}"/></clipPath></defs>',
         '<g clip-path="url(#map-clip)">',
         f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="#F5F3E8"/>',
         f'<path d="{smooth(vegr, True)}" fill="#9CC48C" fill-opacity=".6"/>',
         f'<path d="{smooth(river)}" fill="none" stroke="#BCD6E3" stroke-width="9" stroke-linecap="round"/>',
         f'<path d="{smooth(zone, True)}" fill="{ZONE_FILL}"/>', '<g clip-path="url(#zone-clip)">']
    for v in (veg1, veg2):
        s.append(f'<path d="{smooth(v, True)}" fill="#9CC48C" fill-opacity=".75"/>')
    # fasce di concentrazione: seguono le due strade principali, con rigonfiamenti agli incroci
    cor = [(smooth(main[2:6]), 36), (smooth(ns[1:5]), 26)]
    blobs = [(c(0.48, 0.53), 38, 34), (c(0.79, 0.50), 24, 20), (c(0.31, 0.60), 22, 18)]
    for extra, col in ((64, LEV[0]), (32, LEV[1]), (0, LEV[2])):
        for d, wd in cor:
            s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd+extra}" stroke-linecap="round" stroke-linejoin="round"/>')
        for (bx, by), rx, ry in blobs:
            s.append(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx+extra/2}" ry="{ry+extra/2}" fill="{col}"/>')
    for P, wd in ((loc1, 3), (loc2, 3), (loc3, 3), (loc4, 3), (east, 4), (diag, 4), (ns, 6), (main, 8)):
        s.append(f'<path d="{smooth(P)}" fill="none" stroke="#fff" stroke-width="{wd+3}" stroke-linecap="round" stroke-linejoin="round"/>')
        s.append(f'<path d="{smooth(P)}" fill="none" stroke="#9AA6AB" stroke-width="{wd}" stroke-linecap="round" stroke-linejoin="round"/>')
    rnd = random.Random(7)
    cpts = sample(main[2:6], 8) + sample(ns[1:5], 8)
    for P in (main, ns, east, diag, loc1, loc2, loc3, loc4):
        for (x, y, dx, dy) in sample(P, 12):
            for sgn in (-1, 1):
                if rnd.random() < 0.18: continue
                off = 11 + rnd.random() * 14
                bx, by = x - dy * off * sgn, y + dx * off * sgn
                sz = 4.5 + rnd.random() * 4.5
                near = any((bx - cx) ** 2 + (by - cy) ** 2 < 24 ** 2 for cx, cy, _, _ in cpts)
                s.append(f'<rect x="{bx-sz/2:.1f}" y="{by-sz/2:.1f}" width="{sz:.1f}" height="{sz:.1f}" rx="1.5" fill="{SLATE if near else "#B4BFC3"}" fill-opacity="{.8 if near else .9}"/>')
    s.append("</g>")
    s.append(f'<path d="{smooth(zone, True)}" fill="none" stroke="{SLATE}" stroke-width="2.6" stroke-linejoin="round"/>')
    s.append(f'<path d="{smooth(ext)}" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>')
    s.append(f'<path d="{smooth(ext)}" fill="none" stroke="#9AA6AB" stroke-width="6" stroke-linecap="round"/>')
    # stazioni ed etichette
    hx, hy = c(0.48, 0.525); ux, uy = c(0.20, 0.43); rx_, ry_ = mx + 0.86 * mw, my + 0.045 * mh
    s.append(f'<path d="M{hx:.1f},{hy-13:.1f} V{hy-62:.1f}" stroke="{RED_T}" stroke-width="2.4"/>')
    s.append(f'<path d="M{ux:.1f},{uy-13:.1f} V{uy-40:.1f}" stroke="{TEAL_D}" stroke-width="2.4"/>')
    s.append(f'<path d="M{rx_:.1f},{ry_+13:.1f} V{ry_+28:.1f}" stroke="{TEAL_D}" stroke-width="2.4"/>')
    for x, y in ((hx, hy), (ux, uy), (rx_, ry_)):
        s.append(station_dot(x, y))
    s.append(tag(hx, hy - 76, t["lab_hot"], RED_T))
    s.append(tag(ux, uy - 54, t["lab_urban"]))
    s.append(tag(rx_, ry_ + 42, t["lab_rural"]))
    s.append("</g>")
    # didascalia
    s.append(f'<rect x="{mx+8}" y="{my+mh-40}" width="{width(t["map_note"], 19)+22:.1f}" height="30" rx="15" fill="#fff" fill-opacity=".9"/>')
    s.append(T(mx + 19, my + mh - 19, t["map_note"], 19, 400, SLATE, it=True))
    s.append("</g>")
    return "".join(s)


def draw_legend(t, x, y, w):
    s = [f'<g id="legend" transform="translate({x:.1f},{y:.1f})">',
         f'<rect width="{w}" height="138" rx="16" fill="#fff" fill-opacity=".94" stroke="{GREY}" stroke-width="2"/>',
         T(16, 30, t["leg_conc"], 20, 700, SLATE)]
    cols = (ZONE_FILL, LEV[0], LEV[1], LEV[2])
    for i, col in enumerate(cols):
        s.append(f'<rect x="{16+i*38}" y="42" width="34" height="22" rx="4" fill="{col}" stroke="{GREY}" stroke-width="1.4"/>')
    s.append(T(16, 88, t["leg_low"], 19))
    s.append(T(16 + 4 * 38 - 4, 88, t["leg_high"], 19, 400, SLATE, "end"))
    s.append(station_dot(30, 112))
    s.append(T(52, 119, t["leg_station"], 20))
    return "".join(s) + "</g>"


def draw_monet(t, x, y, w):
    CA, CB, CC = TEAL, OCHRE, "#6F8FAF"
    pad = 16
    s = []
    s.append(T(pad, 34, t["mon_head"], 25, 700, TEAL_D))
    p1, n1 = para(pad, 62, [t["mon_text"]], 20, w - 2 * pad)
    s.append(p1)
    gy = 62 + (n1 - 1) * 24 + 20
    cell = 28; gx = (w - 6 * cell) / 2
    G = ["AAABBB", "AABBBC", "AABCCC", "AACCCC"]
    colr = {"A": CA, "B": CB, "C": CC}
    for r, row in enumerate(G):
        for k, ch in enumerate(row):
            s.append(f'<rect x="{gx+k*cell+1:.1f}" y="{gy+r*cell+1}" width="{cell-2}" height="{cell-2}" rx="4" fill="{colr[ch]}"/>')
    for r, k in ((0, 1), (2, 0), (1, 3)):    # stazioni: due nel gruppo A, una nel gruppo B, nessuna nel gruppo C
        s.append(f'<circle cx="{gx+k*cell+cell/2:.1f}" cy="{gy+r*cell+cell/2}" r="8" fill="{RED}" stroke="#fff" stroke-width="2.4"/>')
    y1 = gy + 4 * cell + 34
    s.append(f'<rect x="{pad}" y="{y1-20}" width="46" height="26" rx="13" fill="{CA}"/>')
    s.append(f'<circle cx="{pad+14}" cy="{y1-7}" r="7" fill="{RED}" stroke="#fff" stroke-width="2"/><circle cx="{pad+32}" cy="{y1-7}" r="7" fill="{RED}" stroke="#fff" stroke-width="2"/>')
    p2, n2 = para(pad + 58, y1, [t["mon_same"]], 20, w - pad - 58 - 12); s.append(p2)
    y2 = y1 + (n2 - 1) * 24 + 40
    s.append(f'<rect x="{pad}" y="{y2-20}" width="46" height="26" rx="13" fill="{CC}"/>')
    p3, n3 = para(pad + 58, y2, [t["mon_gap"]], 20, w - pad - 58 - 12); s.append(p3)
    h = y2 + (n3 - 1) * 24 + 22
    bg = f'<rect width="{w}" height="{h:.1f}" rx="16" fill="#fff" stroke="{TEAL_D}" stroke-opacity=".5" stroke-width="2"/>'
    return f'<g id="monet" transform="translate({x:.1f},{y:.1f})">{bg}{"".join(s)}</g>', h


def draw_cards(t):
    RX, RW = 1206, 678
    tx = RX + 100; av = RW - 100 - 26
    s = ['<g id="messages">']
    # 1 hotspot
    y, h = 150, 172
    s += [card(RX, y, RW, h), circ_icon("pin", RX + 52, y + 56, r=30)]
    svg, n = para(tx, y + 50, [t["h_hot"]], 27, av, w=700, fill=TEAL_D, lh=1.2); s.append(svg)
    yb = y + 50 + (n - 1) * 33 + 38
    s.append(para(tx, yb, [t["sub_hot"]], 21, av)[0])
    if yb + 14 > y + h: WARN.append("card hotspot: contenuto oltre il riquadro")
    # 2 fondo
    y, h = 338, 126
    s += [card(RX, y, RW, h), circ_icon("leaf", RX + 52, y + 56, r=30)]
    svg, n = para(tx, y + 50, [t["h_bg"]], 27, av, w=700, fill=TEAL_D, lh=1.2); s.append(svg)
    if y + 50 + (n - 1) * 33 + 16 > y + h: WARN.append("card fondo: contenuto oltre il riquadro")
    # 3 riduzione
    y, h = 480, 410
    s += [card(RX, y, RW, h), circ_icon("check", RX + 52, y + 80, r=30)]
    pw = width(t["pill_red"], 20) + 28
    s.append(f'<rect x="{tx}" y="{y+22}" width="{pw:.1f}" height="34" rx="17" fill="#FBF3DF" stroke="{OCHRE}" stroke-width="2.4"/>')
    s.append(T(tx + 14, y + 46, t["pill_red"], 20, 400, SLATE))
    svg, n = para(tx, y + 94, [t["h_red"]], 27, av, w=700, fill=TEAL_D, lh=1.2); s.append(svg)
    yy = y + 94 + (n - 1) * 33 + 62
    for i, k in enumerate(("c1", "c2", "c3")):
        s.append(badge(RX + 52, yy - 7, i + 1))
        svg, m = para(tx, yy, [t[k]], 24, av, lh=1.2); s.append(svg)
        yy += (m - 1) * 29 + 74
    if yy - 74 + 20 > y + h: WARN.append(f"card riduzione: contenuto fino a {yy-y:.0f} su {h}")
    return "".join(s) + "</g>"


def calendar(cx, cy):
    st = 'fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<g {st}><rect x="{cx-27}" y="{cy-22}" width="54" height="48" rx="8"/><path d="M{cx-27},{cy-8} H{cx+27}"/>'
            f'<path d="M{cx-13},{cy-30} V{cy-16} M{cx+13},{cy-30} V{cy-16}"/></g>'
            + T(cx, cy + 20, "5", 28, 700, "#fff", "middle"))


def draw_band(t):
    return (f'<g id="review"><rect x="36" y="910" width="1848" height="120" rx="28" fill="{TEAL_D}"/>' + calendar(112, 972)
            + lines(176, 962, [t["band_bold"]], 34, 1600, 700, "#fff") + lines(176, 1002, [t["band_l2"]], 27, 1600, 400, "#fff") + "</g>")


def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    cx0 = MX + 0.705 * MW; colw = MX + MW - 12 - cx0
    mon, mh = draw_monet(t, cx0, 0, colw)
    mon_y = MY + MH - 14 - mh
    mon, mh = draw_monet(t, cx0, mon_y, colw)
    leg = draw_legend(t, cx0, MY + 0.165 * MH, colw)
    if mon_y < MY + 0.165 * MH + 138 + 24 + 0: WARN.append(f"MoNET (y={mon_y:.0f}) troppo vicino alla legenda")
    body = "\n".join([f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
                      header(t["title"], t["subtitle"]), draw_map(t), leg, mon, draw_cards(t), draw_band(t)])
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, W, H)
    return render(svg, OUT / f"monitoring_network_design_{lang}")


if __name__ == "__main__":
    for lang in [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]:
        print("scritto", build(lang).name)
    for m in WARN: print("ATTENZIONE:", m)
