#!/usr/bin/env python3
"""Infografica 03 – Fitness-for-purpose: quando un modello è adatto allo scopo (documento tecnico CE, §1.5 e §3.3).

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non ancora previsto
Testi in strings/<lingua>.yaml; geometrie qui. Nessun dato numerico: la figura è concettuale."""
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

def lines(x, y, ls, size, maxw, w=400, fill=SLATE, it=False, lh=1.22, anchor="start"):
    """Righe di testo con controllo della larghezza massima (avvisa se una riga esce dal riquadro)."""
    for l in ls:
        if _width(l, size, w == 700) > maxw: WARN.append(f"riga troppo larga ({_width(l, size, w == 700):.0f}>{maxw}): {l}")
    return T(x, y, ls, size, w, fill, anchor, it=it, lh=lh)

def wrap(ls, size, maxw, w=400):
    """Ri-spezza un paragrafo (lista di righe) in righe che stanno entro maxw px, con le metriche del font."""
    words = " ".join(ls).split(); out, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if cur and _width(trial, size, w == 700) > maxw: out.append(cur); cur = wd
        else: cur = trial
    return out + [cur]

def small_arrow(cx, cy):
    return f'<path d="M{cx-12},{cy-9} h10 v-9 l16,18 l-16,18 v-9 h-10 z" fill="{TEAL_D}"/>'

# ---------------------------------------------------------------- icone (stile tratto, ~44 px)
ST = f'fill="none" stroke="{TEAL_D}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
def icon(kind, cx, cy):
    g = [f'<g transform="translate({cx},{cy})" {ST}>']
    if kind == "grid":
        for i in (-14, 0, 14):
            g.append(f'<path d="M-21,{i} H21 M{i},-21 V21"/>')
    elif kind == "process":
        g.append('<circle cx="-14" cy="12" r="6"/><circle cx="14" cy="14" r="6"/><circle cx="0" cy="-14" r="6"/>'
                 '<path d="M-10,-9 L-13,6 M4,-9 L12,8 M-8,13 H8"/>')
    elif kind == "source":
        g.append('<path d="M-20,20 V-2 H-6 V20 M-6,20 V-22 H8 V20 M8,20 H22 M-24,20 H24"/>'
                 '<path d="M17,-10 q4,-5 8,0 M14,-20 q4,-5 8,0" stroke-width="2.6"/>')
    elif kind == "weather":
        g.append('<path d="M-16,12 a9,9 0 0 1 2,-17 a12,12 0 0 1 23,-3 a9,9 0 0 1 3,20 z"/>')
    elif kind == "check":
        g.append('<circle r="21"/><path d="M-10,1 L-3,9 L11,-9"/>')
    elif kind == "doc":
        g.append('<path d="M-14,-22 H6 L16,-12 V22 H-14 Z M6,-22 V-12 H16 M-7,-2 H9 M-7,7 H9 M-7,15 H3"/>')
    g.append("</g>")
    return "".join(g)

# ================================================================== pannello 1: criteri e input
def panel1(t, x0, y0, w):
    s = ['<g id="panel1">', panel(x0, y0, w, 710, 1, t["h1"])]
    kinds = ("grid", "process", "source", "weather", "check", "doc")
    for i, (k, ls) in enumerate(zip(kinds, t["crit"])):
        cy = y0 + 112 + i * 66
        s.append(f'<circle cx="{x0+54}" cy="{cy}" r="29" fill="{TEAL}" fill-opacity=".10"/>')
        s.append(icon(k, x0 + 54, cy))
        s.append(lines(x0 + 104, cy - 4, ls, 21, w - 104 - 14))
    s.append(T(x0 + 24, y0 + 494, t["crit_src"], 19, 400, SLATE, it=True))
    s.append(f'<path d="M{x0+24},{y0+512} H{x0+w-24}" stroke="{GREY}" stroke-width="2"/>')
    s.append(T(x0 + 24, y0 + 548, t["p1_sub"], 24, 700, TEAL_D))
    pt = wrap(t["p1_text"], 21, w - 48)
    if len(pt) > 4: WARN.append(f"p1_text: {len(pt)} righe")
    s.append(lines(x0 + 24, y0 + 582, pt, 21, w - 48))
    return "".join(s) + "</g>"

# ================================================================== pannello 2: cinque ambiti
GREEN, ORANGE, GREYC = "#7DB46C", "#EBA04A", "#C3CACD"

def chip(x, y, h, d, w=160):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{TEAL_D}"/>']
    n = len(d["name"]); blockh = n * 25 + 20
    base = y + (h - blockh) / 2 + 19
    out.append(T(x + w / 2, base, d["name"], 22, 700, "#fff", "middle", lh=1.14))
    out.append(T(x + w / 2, base + n * 25 + 3, d["sec"], 19, 400, "#fff", "middle"))
    return "".join(out)

def panel2(t, x0, y0, w):
    s = ['<g id="panel2">', panel(x0, y0, w, 710, 2, t["h2"])]
    cx = x0 + 24; tx = cx + 160 + 18; avail = w - (tx - x0) - 26
    y = y0 + 96
    # --- A: rete di monitoraggio, con i quattro livelli (Tier) e MoNET
    n = t["net"]; hA = 150
    s.append(chip(cx, y, hA, n))
    s.append(lines(tx, y + 22, [n["head"]], 21, avail))
    bw, gp = (avail - 3 * 8) / 4, 8
    for i, lab in enumerate(n["tiers"]):
        bx = tx + i * (bw + gp); hi = i >= 2
        s.append(f'<rect x="{bx:.1f}" y="{y+34}" width="{bw:.1f}" height="54" rx="9" fill="{TEAL_D if hi else "#fff"}" stroke="{TEAL_D if hi else GREY}" stroke-width="2.5"/>')
        s.append(T(bx + bw / 2, y + 34 + 23, lab, 20, 700 if hi else 400, "#fff" if hi else SLATE, "middle", lh=1.1))
    mo = wrap(n["monet"], 21, avail)
    if len(mo) > 2: WARN.append(f"monet: {len(mo)} righe")
    s.append(lines(tx, y + 112, mo, 21, avail))
    y += hA + 14
    # --- B: valutazione
    d = t["ass"]; hB = 76
    tl = wrap(d["text"], 21, avail)
    if len(tl) > 2: WARN.append(f"ass: {len(tl)} righe")
    s.append(chip(cx, y, hB, d)); s.append(lines(tx, y + 24, tl, 21, avail)); y += hB + 14
    # --- C: source apportionment e codice colore
    d = t["sa"]; hC = 100; yC = y
    s.append(chip(cx, y, hC, d)); s.append(lines(tx, y + 22, [d["head"]], 21, avail))
    xx = tx
    for lab, col in zip(d["chips"], (GREEN, ORANGE, GREYC)):
        wd = _width(lab, 19, True) + 22
        s.append(f'<rect x="{xx:.1f}" y="{y+34}" width="{wd:.1f}" height="32" rx="9" fill="{col}"/>')
        s.append(T(xx + wd / 2, y + 34 + 23, lab, 19, 700, INK, "middle"))
        xx += wd + 10
    if xx - 10 > tx + avail: WARN.append(f"chip colore troppo larghi: {xx-10-tx:.0f}>{avail:.0f}")
    s.append(lines(tx, y + 92, [d["example"]], 21, avail)); y += hC + 14
    # --- D: piani
    d = t["plan"]; hD = 92
    tl = wrap(d["text"], 21, avail)
    if len(tl) > 3: WARN.append(f"plan: {len(tl)} righe")
    s.append(chip(cx, y, hD, d)); s.append(lines(tx, y + 24, tl, 21, avail)); yD_end = y + hD; y += hD + 14
    # barra ocra: condizioni più severe (C e D)
    s.append(f'<rect x="{x0+w-20}" y="{yC}" width="7" height="{yD_end-yC}" rx="3.5" fill="{OCHRE}"/>')
    # --- E: previsioni
    d = t["fc"]; hE = 92
    tl = wrap(d["text"], 21, avail)
    if len(tl) > 3: WARN.append(f"fc: {len(tl)} righe")
    s.append(chip(cx, y, hE, d)); s.append(lines(tx, y + 24, tl, 21, avail)); y += hE
    ly = y0 + 690
    s.append(f'<rect x="{cx}" y="{ly-20}" width="7" height="26" rx="3.5" fill="{OCHRE}"/>')
    s.append(lines(cx + 20, ly, [t["strict_note"]], 21, w - 24 - 20 - 14, 700, SLATE))
    return "".join(s) + "</g>"

# ================================================================== pannello 3: oltre l'MQO
def panel3(t, x0, y0, w):
    s = ['<g id="panel3">', panel(x0, y0, w, 710, 3, t["h3"])]
    cx, cy, R = x0 + 24 + 88, y0 + 196, 88
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{TEAL}" fill-opacity=".10" stroke="{TEAL_D}" stroke-width="3.4"/>')
    s.append(T(cx, cy - 40, t["venn_outer"], 19, 700, TEAL_D, "middle", lh=1.1))
    s.append(f'<circle cx="{cx}" cy="{cy+30}" r="34" fill="{TEAL_D}"/>')
    s.append(T(cx, cy + 38, t["venn_inner"], 22, 700, "#fff", "middle"))
    s.append(lines(x0 + 24 + 2 * R + 26, cy - 40, t["venn_cap"], 23, w - (2 * R + 24 + 26) - 14, 700, TEAL_D))
    y = y0 + 330
    for ls in t["tools"]:
        ls = wrap(ls, 21, w - 52 - 14)
        s.append(dot(x0 + 34, y - 6, 5.5, TEAL_D))
        s.append(lines(x0 + 52, y, ls, 21, w - 52 - 14))
        y += len(ls) * 26 + 32
    if y > y0 + 705: WARN.append(f"pannello 3: contenuto fino a {y-y0:.0f}")
    return "".join(s) + "</g>"

# ================================================================== layout "wide" (1920×1080)
def layout_wide(t):
    y0, gap = 170, 40
    ws = [450, 780, 538]
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
    body, w, h = layout_wide(t)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"fitness_for_purpose_{lang}"
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
