#!/usr/bin/env python3
"""Infografica 06 – Proiezioni: come stimare le concentrazioni future (documento tecnico CE, §5.3 e §5.4.3).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non ancora previsto
Testi in strings/<lingua>.yaml; geometrie qui. I valori dell'esempio sul bias (pannello 3) e la mappa del pannello 1
sono INVENTATI e dichiarati nella figura. Layout mobile non previsto."""
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
    out = wrap(ls, size, maxw, kw.get("w", 400))
    return lines(x, y, out, size, maxw, **kw), len(out)

def small_arrow(cx, cy):
    return f'<path d="M{cx-12},{cy-9} h10 v-9 l16,18 l-16,18 v-9 h-10 z" fill="{TEAL_D}"/>'

def smooth(P, closed=False):
    n = len(P); d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in (range(n) if closed else range(n - 1)):
        p0 = P[(i - 1) % n] if closed or i > 0 else P[0]
        p1, p2 = P[i], P[(i + 1) % n]
        p3 = P[(i + 2) % n] if closed or i + 2 < n else P[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")

def fmt(x, nd, lang):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "it" else s

# ---- esempio inventato sul bias (µg/m³): fondo + una fonte locale; il modello sottostima di 5 (25 %) ------------
BG0, LOC0, OBS = 8.0, 7.0, 20.0           # valutazione: modello = fondo + fonte locale; misure
BG_T, LOC_T = 0.90, 0.60                  # a fine scenario il fondo scende del 10 %, la fonte locale del 40 %
MOD0 = BG0 + LOC0
BIAS = OBS - MOD0                         # 5 µg/m³ = 25 % delle misure
RATIO = OBS / MOD0
BG1, LOC1 = BG0 * BG_T, LOC0 * LOC_T      # proiezione senza correzione
SPLIT_BG, SPLIT_LOC = 3.0, 2.0            # nel metodo combinato: 3 al fondo (assoluta), 2 alla fonte locale (relativa)
assert abs(SPLIT_BG + SPLIT_LOC - BIAS) < 1e-9
LOC_COMB = LOC1 * (LOC0 + SPLIT_LOC) / LOC0
BARS = [  # (segmenti [(valore, tipo)], totale)
    [(BG0, "bg"), (LOC0, "loc")],
    [(OBS, "obs")],
    [(BG1, "bg"), (LOC1, "loc")],
    [(BG1, "bg"), (LOC1, "loc"), (BIAS, "cor")],
    [(BG1, "bg"), (LOC1, "loc"), (MOD0 and (BG1 + LOC1) * (RATIO - 1), "cor")],
    [(BG1, "bg"), (SPLIT_BG, "cor"), (LOC1, "loc"), (LOC_COMB - LOC1, "cor")],
]

# ================================================================== pannello 1: emissioni e fondo
def panel1(t, x0, y0, w):
    s = ['<g id="panel1">', panel(x0, y0, w, 710, 1, t["h1"])]
    y = y0 + 100; avail = w - 48
    s.append(T(x0 + 24, y, t["p1_intro"], 22, 700, SLATE)); y += 44
    for key in ("e", "b", "n"):
        s.append(T(x0 + 24, y, t[key + "_title"], 25, 700, TEAL_D))
        svg, n = para(x0 + 24, y + 30, t[key + "_text"], 21, avail, lh=1.2); s.append(svg)
        y += 30 + (n - 1) * 25 + 34
    if y - 34 > y0 + 690: WARN.append(f"pannello 1: contenuto fino a {y-34-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 2: meteorologia
def panel2(t, x0, y0, w):
    s = ['<g id="panel2">', panel(x0, y0, w, 710, 2, t["h2"])]
    y = y0 + 98
    svg, n = para(x0 + 24, y, t["m_intro"], 21, w - 48, w=700, fill=SLATE); s.append(svg); y += n * 26 + 14
    tx = x0 + 24 + 50; avail = w - (tx - x0) - 20
    for i, d in enumerate(t["opts"]):
        s.append(f'<circle cx="{x0+24+19}" cy="{y+11}" r="19" fill="{TEAL_D}"/>')
        s.append(T(x0 + 24 + 19, y + 19, str(i + 1), 23, 700, "#fff", "middle"))
        s.append(T(tx, y + 18, d["name"], 24, 700, TEAL_D))
        if d["tag"]:
            px = tx + _width(d["name"], 24, True) + 14; pw = _width(d["tag"], 18, d["filled"]) + 22
            if px + pw > x0 + w - 16: WARN.append(f"pillola troppo larga: {d['tag']}")
            if d["filled"]:
                s.append(f'<rect x="{px:.1f}" y="{y-3}" width="{pw:.1f}" height="29" rx="14.5" fill="{TEAL_D}"/>')
                s.append(T(px + 11, y + 17, d["tag"], 18, 700, "#fff"))
            else:
                s.append(f'<rect x="{px:.1f}" y="{y-3}" width="{pw:.1f}" height="29" rx="14.5" fill="#fff" stroke="{GREY}" stroke-width="2.2"/>')
                s.append(T(px + 11, y + 17, d["tag"], 18, 400, SLATE))
        svg, n = para(tx, y + 44, d["text"], 21, avail, lh=1.18); s.append(svg)
        y += 44 + (n - 1) * 25 + 18
    s.append(f'<path d="M{x0+24},{y-6} H{x0+w-24}" stroke="{GREY}" stroke-width="2"/>')
    y += 24
    s.append(T(x0 + 24, y, t["aei_title"], 24, 700, TEAL_D))
    svg, n = para(x0 + 24, y + 30, t["aei_text"], 21, w - 48, lh=1.18); s.append(svg); y += 30 + (n - 1) * 25
    if y > y0 + 700: WARN.append(f"pannello 2: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 3: correzione del bias
def panel3(t, x0, y0, w, lang):
    s = ['<g id="panel3">', panel(x0, y0, w, 710, 3, t["h3"])]
    y = y0 + 98
    svg, n = para(x0 + 24, y, t["p3_intro"], 21, w - 48, lh=1.18); s.append(svg); y += (n - 1) * 25 + 28
    title = t["chart_title"].format(bias=fmt(BIAS, 0, lang))
    s.append(T(x0 + 24, y, title, 19, 400, SLATE, it=True)); y += 14
    lx = x0 + 24; labw = 172; bx0 = lx + labw + 8; bx1 = lx + 384; VMAX = 24.0
    X = lambda v: bx0 + (bx1 - bx0) * v / VMAX
    top = y + 6; rowh = 34; n_rows = len(BARS); bottom = top + rowh * n_rows
    for tick in (0, 5, 10, 15, 20):
        s.append(f'<path d="M{X(tick):.1f},{top-4} V{bottom}" stroke="{GREY}" stroke-opacity=".5" stroke-width="1.6"/>')
        s.append(T(X(tick), bottom + 24, str(tick), 19, 400, SLATE, "middle"))
    COL = {"bg": "#B4BFC3", "loc": TEAL, "cor": OCHRE, "obs": INK}
    for i, (segs, lab) in enumerate(zip(BARS, t["rows"])):
        cy = top + rowh * i + rowh / 2
        s.append(T(lx, cy + 6, lab, 18, 400, SLATE))
        if _width(lab, 18) > labw: WARN.append(f"etichetta riga troppo larga: {lab}")
        v = 0.0
        for val, kind in segs:
            s.append(f'<rect x="{X(v):.1f}" y="{cy-14:.1f}" width="{X(v+val)-X(v):.1f}" height="28" fill="{COL[kind]}"/>')
            v += val
        s.append(T(X(v) + 8, cy + 7, fmt(v, 1, lang), 19, 700, INK))
    y = bottom + 56
    xx = lx
    for lab, col in zip(t["leg"], (COL["bg"], COL["loc"], COL["cor"])):
        s.append(f'<rect x="{xx:.1f}" y="{y-14}" width="20" height="18" rx="3" fill="{col}"/>')
        s.append(T(xx + 28, y, lab, 19, 400, SLATE)); xx += 28 + _width(lab, 19) + 26
    # colonna dei metodi, a destra del grafico
    mx = lx + 414; mw = w - (mx - x0) - 24; my = top + 6
    for d in t["methods"]:
        s.append(T(mx, my + 14, d["name"].format(bias=fmt(BIAS, 0, lang), ratio=fmt(RATIO, 2, lang)), 23, 700, TEAL_D))
        svg, n = para(mx, my + 42, d["text"], 21, mw, lh=1.18); s.append(svg)
        my += 42 + (n - 1) * 25 + 20
    yb = max(y, my) + 6
    s.append(f'<path d="M{x0+24},{yb-2} H{x0+w-24}" stroke="{GREY}" stroke-width="2"/>')
    yb += 30
    colw = (w - 48 - 36) / 2
    yend = yb
    for k, key in enumerate(("test", "dyn")):
        cx = x0 + 24 + k * (colw + 36)
        tl = wrap([t[key + "_title"]], 24, colw, 700)
        s.append(lines(cx, yb, tl, 24, colw, 700, TEAL_D, lh=1.15))
        svg, n = para(cx, yb + len(tl) * 28 + 4, t[key + "_text"], 21, colw, lh=1.18); s.append(svg)
        yend = max(yend, yb + len(tl) * 28 + 4 + (n - 1) * 25)
    yb = yend
    if yb > y0 + 700: WARN.append(f"pannello 3: contenuto fino a {yb-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== layout "wide" (1920×1080)
WS = [430, 520, 778]
def layout_wide(t, lang):
    y0, gap = 170, 40
    xs = [36]
    for wd in WS[:-1]: xs.append(xs[-1] + wd + gap)
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 86, t["title"], 58, 700, TEAL_D), T(48, 134, t["subtitle"], 30, 400, SLATE),
            panel1(t, xs[0], y0, WS[0]), small_arrow(xs[0] + WS[0] + gap / 2, y0 + 355),
            panel2(t, xs[1], y0, WS[1]), small_arrow(xs[1] + WS[1] + gap / 2, y0 + 355),
            panel3(t, xs[2], y0, WS[2], lang),
            f'<g id="definition">{band(36, 910, 1848, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    return "\n".join(body), W, H

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    for k, wd in zip(("h1", "h2", "h3"), WS):
        if _width(t[k], 36, True) > wd - 84: WARN.append(f"titolo {k} troppo largo: {_width(t[k], 36, True):.0f}>{wd-84}")
    body, w, h = layout_wide(t, lang)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"projections_{lang}"
    stem.with_suffix(".svg").write_text(svg, encoding="utf-8")
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(stem.with_suffix(".png")), output_width=3840)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(stem.with_suffix(".pdf")))
    except ImportError:
        print("cairosvg non installato: generato solo l'SVG")
    return stem

if __name__ == "__main__":
    print("bias = %.1f (%.0f %% delle misure) | rapporto = %.3f | proiezione senza correzione = %.1f | assoluta %.1f | relativa %.1f | combinata %.1f"
          % (BIAS, 100 * BIAS / OBS, RATIO, BG1 + LOC1, BG1 + LOC1 + BIAS, (BG1 + LOC1) * RATIO, BG1 + SPLIT_BG + LOC_COMB))
    for lang in [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]:
        print("scritto", build(lang).name)
    for m in WARN: print("ATTENZIONE:", m)
