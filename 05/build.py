#!/usr/bin/env python3
"""Infografica 05 – Gli scenari emissivi di un piano per la qualità dell'aria (documento tecnico CE, §5.2.4).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non ancora previsto
Testi in strings/<lingua>.yaml; geometrie qui. I valori del grafico a barre (pannello 2) sono INVENTATI e dichiarati."""
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

# ================================================================== pannello 1: sette scenari
def panel1(t, x0, y0, w):
    s = ['<g id="panel1">', panel(x0, y0, w, 710, 1, t["h1"])]
    y = y0 + 96
    tx = x0 + 24 + 50; avail = w - (tx - x0) - 20
    for i, d in enumerate(t["scen"]):
        s.append(f'<circle cx="{x0+24+19}" cy="{y+11}" r="19" fill="{TEAL_D}"/>')
        s.append(T(x0 + 24 + 19, y + 19, str(i + 1), 23, 700, "#fff", "middle"))
        s.append(T(tx, y + 18, d["name"], 24, 700, TEAL_D))
        px = tx + _width(d["name"], 24, True) + 14; pw = _width(d["tag"], 18, d["req"]) + 22
        if px + pw > x0 + w - 16: WARN.append(f"pillola troppo larga: {d['tag']}")
        if d["req"]:
            s.append(f'<rect x="{px:.1f}" y="{y-3}" width="{pw:.1f}" height="29" rx="14.5" fill="{TEAL_D}"/>')
            s.append(T(px + 11, y + 17, d["tag"], 18, 700, "#fff"))
        else:
            s.append(f'<rect x="{px:.1f}" y="{y-3}" width="{pw:.1f}" height="29" rx="14.5" fill="#fff" stroke="{GREY}" stroke-width="2.2"/>')
            s.append(T(px + 11, y + 17, d["tag"], 18, 400, SLATE))
        svg, n = para(tx, y + 44, d["text"], 21, avail, lh=1.18); s.append(svg)
        y += 44 + (n - 1) * 25 + 11
    if y > y0 + 712: WARN.append(f"pannello 1: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 2: che cosa cambia (grafico a barre)
def panel2(t, x0, y0, w):
    s = ['<g id="panel2">', panel(x0, y0, w, 710, 2, t["h2"])]
    cap, nc = para(x0 + 24, y0 + 96, [t["chart_title"]], 19, w - 48, it=True); s.append(cap)
    lx = x0 + 24; labw = 150
    bx0 = lx + labw + 6; bx1 = x0 + w - 30
    VMAX = 150.0
    X = lambda v: bx0 + (bx1 - bx0) * v / VMAX
    top = y0 + 146; rowh = 58; n = len(t["chart_rows"])
    bottom = top + rowh * n
    for tick in (0, 50, 100, 150):
        s.append(f'<path d="M{X(tick):.1f},{top-6} V{bottom}" stroke="{GREY}" stroke-opacity=".5" stroke-width="1.6"/>')
        s.append(T(X(tick), bottom + 28, str(tick), 20, 400, SLATE, "middle"))
    for i, (lab, val, rng) in enumerate(t["chart_rows"]):
        cy = top + rowh * i + rowh / 2
        ls = wrap([lab], 21, labw)
        s.append(T(lx, cy - (len(ls) - 1) * 12 + 7, ls, 21, 400, SLATE, lh=1.1))
        over = val > 100 if not rng else rng[0] > 100 or val > 100
        col = RED if val > 100 else TEAL
        s.append(f'<rect x="{bx0:.1f}" y="{cy-15:.1f}" width="{X(val)-bx0:.1f}" height="30" rx="5" fill="{col}"/>')
        s.append(T(bx0 + 10, cy + 7, str(val), 20, 700, "#fff"))
        if rng:
            a, b = X(rng[0]), X(rng[1])
            s.append(f'<path d="M{a:.1f},{cy:.1f} H{b:.1f} M{a:.1f},{cy-9:.1f} v18 M{b:.1f},{cy-9:.1f} v18" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"/>')
    s.append(f'<path d="M{X(100):.1f},{top-14} V{bottom}" stroke="{SLATE}" stroke-width="3.4" stroke-dasharray="9 6"/>')
    s.append(T(X(100) + 8, top - 18, t["limit_label"], 20, 700, SLATE))
    s.append(T((bx0 + bx1) / 2, bottom + 58, t["chart_axis"], 20, 400, SLATE, "middle"))
    y = bottom + 88
    s.append(f'<path d="M{lx+2},{y-6} h40 M{lx+2},{y-14} v16 M{lx+42},{y-14} v16" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"/>')
    s.append(lines(lx + 54, y, [t["chart_legend"]], 20, w - 48 - 54))
    y += 36
    svg, n1 = para(lx, y, t["chart_note"], 21, w - 48, w=700, fill=TEAL_D); s.append(svg); y += n1 * 26 + 8
    svg, n2 = para(lx, y, t["chart_note2"], 21, w - 48); s.append(svg); y += n2 * 26
    if y > y0 + 706: WARN.append(f"pannello 2: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== pannello 3: incertezza e numero di calcoli
def panel3(t, x0, y0, w):
    s = ['<g id="panel3">', panel(x0, y0, w, 710, 3, t["h3"])]
    y = y0 + 100; avail = w - 48
    s.append(T(x0 + 24, y, t["p3_a_title"], 25, 700, TEAL_D)); y += 14
    svg, n = para(x0 + 24, y + 26, t["p3_a"], 21, avail); s.append(svg); y += 26 + n * 26 + 26
    s.append(T(x0 + 24, y, t["p3_b_title"], 25, 700, TEAL_D)); y += 14
    svg, n = para(x0 + 24, y + 26, t["p3_b"], 21, avail); s.append(svg); y += 26 + n * 26 + 18
    # mini schema: due scenari + uno tratteggiato (etichette anche su più righe)
    labs = [x if isinstance(x, list) else [x] for x in t["boxes"]]
    bx = x0 + 24; rowh = 0
    for i, ls in enumerate(labs):
        wd = max(_width(l, 21, True) for l in ls) + 28; hh = 38 + (len(ls) - 1) * 25
        if bx + wd > x0 + w - 20:
            bx = x0 + 24; y += rowh + 14; rowh = 0
        if i < 2:
            s.append(f'<rect x="{bx:.1f}" y="{y}" width="{wd:.1f}" height="{hh}" rx="10" fill="{TEAL_D}"/>')
            s.append(T(bx + wd / 2, y + 26, ls, 21, 700, "#fff", "middle", lh=1.15))
        else:
            s.append(f'<rect x="{bx:.1f}" y="{y}" width="{wd:.1f}" height="{hh}" rx="10" fill="#fff" stroke="{TEAL_D}" stroke-width="2.6" stroke-dasharray="7 5"/>')
            s.append(T(bx + wd / 2, y + 26, ls, 21, 700, TEAL_D, "middle", lh=1.15))
        bx += wd + 12; rowh = max(rowh, hh)
    y += rowh
    if y > y0 + 706: WARN.append(f"pannello 3: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== layout "wide" (1920×1080)
def layout_wide(t):
    y0, gap = 170, 40
    ws = [820, 500, 448]
    xs = [36]
    for wd in ws[:-1]: xs.append(xs[-1] + wd + gap)
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 86, t["title"], 58, 700, TEAL_D), T(48, 134, t["subtitle"], 30, 400, SLATE),
            panel1(t, xs[0], y0, ws[0]), small_arrow(xs[0] + ws[0] + gap / 2, y0 + 355),
            panel2(t, xs[1], y0, ws[1]), small_arrow(xs[1] + ws[1] + gap / 2, y0 + 355),
            panel3(t, xs[2], y0, ws[2]),
            f'<g id="definition">{band(36, 910, 1848, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    return "\n".join(body), W, H

def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    for k, wd in zip(("h1", "h2", "h3"), (820, 500, 448)):
        if _width(t[k], 36, True) > wd - 84: WARN.append(f"titolo {k} troppo largo: {_width(t[k], 36, True):.0f}>{wd-84}")
    body, w, h = layout_wide(t)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"scenari_{lang}"
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
