#!/usr/bin/env python3
"""Infografica 04 – ESI: quanto è esteso un superamento? (documento tecnico CE, §3.5).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non ancora previsto
Testi in strings/<lingua>.yaml; geometrie qui. Le forme della mappa e dei casi SRA/superamento sono SCHEMATICHE."""
import sys, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
INK = "#22343A"
WARN = []

_FONTS = {}
def _width(txt, size, bold=False):
    try:
        from PIL import ImageFont
        if bold not in _FONTS:
            for d in (pathlib.Path.home() / ".fonts", pathlib.Path("/usr/share/fonts")):
                f = next(iter(d.rglob("SourceSans3-Bold.otf" if bold else "SourceSans3-Regular.otf")), None) if d.exists() else None
                if f: _FONTS[bold] = ImageFont.truetype(str(f), 100); break
            else: _FONTS[bold] = None
        if _FONTS[bold]: return _FONTS[bold].getlength(txt) * size / 100
    except ImportError:
        pass
    return len(txt) * size * 0.40

def wrap(ls, size, maxw, w=400):
    words = " ".join(ls).split(); out, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if cur and _width(trial, size, w == 700) > maxw: out.append(cur); cur = wd
        else: cur = trial
    return out + [cur]

def lines(x, y, ls, size, maxw, w=400, fill=SLATE, it=False, lh=1.22, anchor="start"):
    for l in ls:
        if _width(l, size, w == 700) > maxw: WARN.append(f"riga troppo larga ({_width(l, size, w == 700):.0f}>{maxw:.0f}): {l}")
    return T(x, y, ls, size, w, fill, anchor, it=it, lh=lh)

def para(x, y, ls, size, maxw, **kw):
    """Paragrafo ri-spezzato; restituisce (svg, numero di righe)."""
    out = wrap(ls, size, maxw, kw.get("w", 400))
    return lines(x, y, out, size, maxw, **kw), len(out)

def small_arrow(cx, cy):
    return f'<path d="M{cx-12},{cy-9} h10 v-9 l16,18 l-16,18 v-9 h-10 z" fill="{TEAL_D}"/>'

ST = f'fill="none" stroke="{TEAL_D}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
def icon(kind, cx, cy):
    g = [f'<g transform="translate({cx},{cy})" {ST}>']
    if kind == "area":
        g.append('<path d="M-20,-4 L-8,-20 L14,-14 L20,6 L4,20 L-16,14 Z"/>')
    elif kind == "people":
        g.append('<circle cx="-9" cy="-10" r="6"/><path d="M-20,16 v-6 a11,9 0 0 1 22,0 v6"/><circle cx="12" cy="-6" r="5"/><path d="M6,16 v-4 a9,8 0 0 1 16,0 v4"/>')
    elif kind == "road":
        g.append('<path d="M-9,22 L-4,-22 M9,22 L4,-22"/><path d="M0,-18 v8 M0,-2 v8 M0,12 v8" stroke-width="2.6"/>')
    elif kind == "leaf":
        g.append('<path d="M-18,16 C-20,-8 0,-22 20,-20 C22,0 6,18 -18,16 Z M-18,16 L8,-8"/>')
    elif kind == "grid":
        for i in (-14, 0, 14): g.append(f'<path d="M-21,{i} H21 M{i},-21 V21"/>')
    elif kind == "check":
        g.append('<circle r="21"/><path d="M-10,1 L-3,9 L11,-9"/>')
    elif kind == "wave":
        g.append('<path d="M-22,6 C-14,-18 -6,-18 0,0 C6,18 14,18 22,-6"/><path d="M-22,20 H22" stroke-width="2.6"/>')
    elif kind == "canyon":
        g.append('<path d="M-22,22 V-14 H-8 V22 M8,22 V-18 H22 V22 M-26,22 H26"/>')
    elif kind == "doc":
        g.append('<path d="M-14,-22 H6 L16,-12 V22 H-14 Z M6,-22 V-12 H16 M-7,-2 H9 M-7,7 H9 M-7,15 H3"/>')
    g.append("</g>")
    return "".join(g)

def pts(poly, x, y, w, h):
    return " ".join(f"{x+px*w:.1f},{y+py*h:.1f}" for px, py in poly)

# ================================================================== mappa schematica ma realistica
import random
def smooth(P, closed=False):
    """Curva liscia (Catmull-Rom → Bézier) per punti già in pixel."""
    n = len(P); d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in (range(n) if closed else range(n - 1)):
        p0 = P[(i - 1) % n] if closed or i > 0 else P[0]
        p1, p2 = P[i], P[(i + 1) % n]
        p3 = P[(i + 2) % n] if closed or i + 2 < n else P[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")

def sample(P, step):
    """Punti equispaziati lungo la poligonale (approssima la curva) con direzione locale."""
    out = []
    for (x1, y1), (x2, y2) in zip(P[:-1], P[1:]):
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5
        k = max(1, int(L // step))
        for j in range(k):
            out.append((x1 + (x2 - x1) * j / k, y1 + (y2 - y1) * j / k, (x2 - x1) / L, (y2 - y1) / L))
    return out

def draw_map(mx, my, mw, mh):
    F = lambda pts: [(mx + px * mw, my + py * mh) for px, py in pts]
    zone = F([(0.02, 0.34), (0.10, 0.12), (0.26, 0.18), (0.40, 0.03), (0.62, 0.08), (0.74, 0.02), (0.93, 0.16), (0.99, 0.40), (0.90, 0.58), (0.97, 0.80), (0.76, 0.97), (0.54, 0.90), (0.36, 0.99), (0.14, 0.88), (0.04, 0.66)])
    main = F([(0.0, 0.62), (0.14, 0.56), (0.30, 0.60), (0.46, 0.52), (0.62, 0.58), (0.78, 0.50), (1.0, 0.44)])
    ns = F([(0.44, 0.0), (0.47, 0.18), (0.45, 0.34), (0.50, 0.52), (0.55, 0.72), (0.52, 1.0)])
    east = F([(0.70, 0.04), (0.74, 0.28), (0.79, 0.50), (0.88, 0.74), (0.92, 1.0)])
    diag = F([(0.04, 0.20), (0.22, 0.30), (0.36, 0.40), (0.47, 0.52)])
    loc1 = F([(0.36, 0.585), (0.35, 0.46), (0.31, 0.34)])
    loc2 = F([(0.62, 0.575), (0.65, 0.68), (0.63, 0.80)])
    loc3 = F([(0.30, 0.60), (0.27, 0.72), (0.31, 0.84)])
    loc4 = F([(0.55, 0.555), (0.58, 0.40), (0.62, 0.26)])
    river = F([(0.0, 0.88), (0.20, 0.82), (0.40, 0.90), (0.65, 0.86), (0.85, 0.96), (1.0, 0.92)])
    veg1 = F([(0.07, 0.62), (0.14, 0.50), (0.27, 0.54), (0.30, 0.70), (0.20, 0.78), (0.09, 0.74)])
    veg2 = F([(0.80, 0.14), (0.90, 0.20), (0.92, 0.34), (0.82, 0.38), (0.74, 0.26)])
    s = [f'<defs><clipPath id="zone-clip"><path d="{smooth(zone, True)}"/></clipPath></defs>',
         f'<path d="{smooth(zone, True)}" fill="#EEF3F1"/>', '<g clip-path="url(#zone-clip)">']
    for v in (veg1, veg2):
        s.append(f'<path d="{smooth(v, True)}" fill="#9CC48C" fill-opacity=".75"/>')
    s.append(f'<path d="{smooth(river)}" fill="none" stroke="#BCD6E3" stroke-width="9" stroke-linecap="round"/>')
    # area di superamento: segue la strada principale e quella nord-sud, con rigonfiamenti agli incroci
    cor = [(smooth(main[2:6]), 40), (smooth(ns[1:5]), 30)]
    blobs = [((mx + 0.48 * mw, my + 0.53 * mh), 36, 38), ((mx + 0.79 * mw, my + 0.50 * mh), 27, 22), ((mx + 0.31 * mw, my + 0.60 * mh), 24, 20)]
    for extra, col in ((5, RED_T), (0, "#F4C2BA")):
        for d, wd in cor:
            s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd+extra}" stroke-linecap="round" stroke-linejoin="round"/>')
        for (cx, cy), rx, ry in blobs:
            s.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx+extra/2}" ry="{ry+extra/2}" fill="{col}"/>')
    # strade (bordo bianco + asfalto)
    for P, wd in ((loc1, 3), (loc2, 3), (loc3, 3), (loc4, 3), (east, 4), (diag, 4), (ns, 6), (main, 8)):
        s.append(f'<path d="{smooth(P)}" fill="none" stroke="#fff" stroke-width="{wd+3}" stroke-linecap="round" stroke-linejoin="round"/>')
        s.append(f'<path d="{smooth(P)}" fill="none" stroke="#9AA6AB" stroke-width="{wd}" stroke-linecap="round" stroke-linejoin="round"/>')
    # edifici lungo le strade (più scuri dentro l'area di superamento)
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
    return "".join(s)

# ================================================================== pannello 1: che cosa si calcola
def panel1(t, x0, y0, w):
    s = ['<g id="panel1">', panel(x0, y0, w, 710, 1, t["h1"])]
    mx, my, mw, mh = x0 + 24, y0 + 90, w - 48, 184
    s.append(draw_map(mx, my, mw, mh))
    cap, nc = para(mx, my + mh + 24, t["map_cap"], 19, w - 48, it=True, lh=1.2); s.append(cap)
    y = my + mh + 24 + nc * 24 + 18
    for k, d in zip(("area", "people", "road", "leaf"), t["ind"]):
        s.append(f'<circle cx="{x0+24+27}" cy="{y+8}" r="25" fill="{TEAL}" fill-opacity=".10"/>')
        s.append(icon(k, x0 + 24 + 27, y + 8))
        s.append(T(x0 + 24 + 66, y + 6, d["name"], 23, 700, TEAL_D))
        missing = d["value"].startswith(("non", "not"))
        s.append(T(x0 + w - 24, y + 6, d["value"], 20 if missing else 24, 400 if missing else 700, SLATE if missing else INK, "end", it=missing))
        svg, n = para(x0 + 24 + 66, y + 32, d["text"], 21, w - 24 - 66 - 14)
        s.append(svg)
        y += 30 + n * 26 + 14
    if y > y0 + 726: WARN.append(f"pannello 1: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 2: i passi del calcolo
def panel2(t, x0, y0, w):
    s = ['<g id="panel2">', panel(x0, y0, w, 710, 2, t["h2"])]
    y = y0 + 98
    tx = x0 + 24 + 50; avail = w - (tx - x0) - 18
    items = [(d["name"], d["tag"], wrap(d["text"], 21, avail)) for d in t["steps"]]
    for i, (name, tag, ls) in enumerate(items):
        s.append(f'<circle cx="{x0+24+19}" cy="{y+11}" r="19" fill="{TEAL_D}"/>')
        s.append(T(x0 + 24 + 19, y + 19, str(i + 1), 23, 700, "#fff", "middle"))
        s.append(T(tx, y + 18, name, 24, 700, TEAL_D))
        px = tx + _width(name, 24, True) + 14; pw = _width(tag, 18, True) + 20
        if px + pw > x0 + w - 14: WARN.append(f"pillola troppo larga: {tag}")
        s.append(f'<rect x="{px:.1f}" y="{y-2}" width="{pw:.1f}" height="28" rx="14" fill="{TEAL}" fill-opacity=".14"/>')
        s.append(T(px + 10, y + 18, tag, 18, 700, TEAL_D))
        s.append(lines(tx, y + 46, ls, 21, avail))
        h = 46 + (len(ls) - 1) * 26 + 10
        if i < len(items) - 1:
            s.append(f'<path d="M{x0+24+19},{y+32} V{y+h+6}" stroke="{GREY}" stroke-width="3" stroke-linecap="round"/>')
        y += h + 7
    if y > y0 + 716: WARN.append(f"pannello 2: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 3: fonti di incertezza
def panel3(t, x0, y0, w):
    s = ['<g id="panel3">', panel(x0, y0, w, 710, 3, t["h3"])]
    y = y0 + 98
    tx = x0 + 24 + 54; avail = w - (tx - x0) - 14
    for d in t["rows3"]:
        s.append(f'<circle cx="{x0+24+22}" cy="{y+7}" r="22" fill="{TEAL}" fill-opacity=".10"/>')
        s.append(icon(d["icon"], x0 + 24 + 22, y + 7))
        nm = wrap([d["name"]], 22, avail, 700)
        s.append(lines(tx, y + 8, nm, 22, avail, 700, TEAL_D))
        svg, n = para(tx, y + 8 + len(nm) * 26, d["text"], 21, avail)
        s.append(svg)
        y += 8 + len(nm) * 26 + n * 26 + 12
    L = w - 48; by = y + 4
    for i, (lab, frac) in enumerate(zip(t["bars"], (0.42, 1.0))):
        yy = by + i * 38
        wb = L * frac
        s.append(f'<rect x="{x0+24}" y="{yy}" width="{wb:.1f}" height="32" rx="8" fill="{TEAL if i == 0 else TEAL_D}"/>')
        tw = _width(lab, 20, True)
        if tw + 24 <= wb: s.append(T(x0 + 24 + 12, yy + 23, lab, 20, 700, "#fff"))
        else: s.append(T(x0 + 24 + wb + 10, yy + 23, lab, 20, 700, TEAL_D))
    cap, nc = para(x0 + 24, by + 76 + 22, [t["bars_cap"]], 19, w - 48, it=True)
    s.append(cap)
    if by + 76 + 22 + (nc - 1) * 24 > y0 + 704: WARN.append(f"pannello 3: contenuto fino a {by+98+(nc-1)*24-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 4: quale modello
def panel4(t, x0, y0, w):
    s = ['<g id="panel4">', panel(x0, y0, w, 710, 4, t["h4"])]
    y = y0 + 98
    tx = x0 + 24 + 54; avail = w - (tx - x0) - 14
    for d in t["rows4"]:
        s.append(f'<circle cx="{x0+24+22}" cy="{y+7}" r="22" fill="{TEAL}" fill-opacity=".10"/>')
        s.append(icon(d["icon"], x0 + 24 + 22, y + 7))
        nm = wrap([d["name"]], 22, avail, 700)
        s.append(lines(tx, y + 8, nm, 22, avail, 700, TEAL_D))
        svg, n = para(tx, y + 8 + len(nm) * 26, d["text"], 21, avail)
        s.append(svg)
        y += 8 + len(nm) * 26 + n * 26 + 22
    if y > y0 + 706: WARN.append(f"pannello 4: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== layout "wide" (1920×1080)
def layout_wide(t):
    y0, gap = 170, 40
    ws = [396, 510, 444, 378]
    xs = [36]
    for wd in ws[:-1]: xs.append(xs[-1] + wd + gap)
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 86, t["title"], 58, 700, TEAL_D), T(48, 134, t["subtitle"], 30, 400, SLATE),
            panel1(t, xs[0], y0, ws[0]), small_arrow(xs[0] + ws[0] + gap / 2, y0 + 355),
            panel2(t, xs[1], y0, ws[1]), small_arrow(xs[1] + ws[1] + gap / 2, y0 + 355),
            panel3(t, xs[2], y0, ws[2]), small_arrow(xs[2] + ws[2] + gap / 2, y0 + 355),
            panel4(t, xs[3], y0, ws[3]),
            f'<g id="definition">{band(36, 910, 1848, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    return "\n".join(body), W, H

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    for k, wd in zip(("h1", "h2", "h3", "h4"), (396, 510, 444, 378)):
        if _width(t[k], 36, True) > wd - 84: WARN.append(f"titolo {k} troppo largo: {_width(t[k], 36, True):.0f}>{wd-84}")
    body, w, h = layout_wide(t)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"esi_{lang}"
    stem.with_suffix(".svg").write_text(svg, encoding="utf-8")
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(stem.with_suffix(".png")), output_width=3840)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(stem.with_suffix(".pdf")))
    except ImportError:
        print("cairosvg non installato: generato solo l'SVG")
    return stem

if __name__ == "__main__":
    for lang in [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]:
        print("scritto", build(lang).name)
    for m in WARN: print("ATTENZIONE:", m)
