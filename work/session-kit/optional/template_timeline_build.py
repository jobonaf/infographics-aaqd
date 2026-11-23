#!/usr/bin/env python3
"""Infografica 07 – Dalla valutazione al piano: tempi e passi (documento tecnico CE, §5.1 e §5.2).
Versione 2, archetipo «linea dei tempi»: elemento grafico principale in alto, tre blocchi sintetici in basso.

Uso:  python build.py [it|en]      # layout "wide" (16:9, slide); layout mobile non ancora previsto
Testi in strings/<lingua>.yaml; geometrie qui. Gli anni 2027, 2029, 2031 della linea dei tempi sono un ESEMPIO.
La versione 1 (più testuale) è conservata in v1-testuale/."""
import sys, math, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
INK = "#22343A"; OCHRE_D = "#8A5F0C"
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

def card(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="#fff" stroke="#B7C6C4" stroke-width="2.6"/>'

# ---------------------------------------------------------------- icone a tratto (~44 px)
def icon(kind, cx, cy, col=TEAL_D):
    st = f'fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
    g = [f'<g transform="translate({cx},{cy})" {st}>']
    if kind == "warn":
        g.append(f'<path d="M0,-21 L21,17 H-21 Z"/><path d="M0,-8 V5"/><circle cy="11" r="1.4" fill="{col}"/>')
    elif kind == "doc":
        g.append('<path d="M-14,-22 H6 L16,-12 V22 H-14 Z M6,-22 V-12 H16 M-7,-2 H9 M-7,7 H9 M-7,15 H3"/>')
    elif kind == "flag":
        g.append('<path d="M-14,22 V-22"/><path d="M-14,-22 H16 L8,-12 L16,-2 H-14"/>')
    elif kind == "pin":
        g.append('<path d="M0,22 C-14,6 -17,0 -17,-8 a17,17 0 0 1 34,0 c0,8 -3,14 -17,30z"/><circle cy="-8" r="5"/>')
    elif kind == "area":
        g.append('<path d="M-20,-4 L-8,-20 L14,-14 L20,6 L4,20 L-16,14 Z"/>')
    elif kind == "source":
        g.append('<path d="M-20,20 V-2 H-6 V20 M-6,20 V-22 H8 V20 M8,20 H22 M-24,20 H24"/>')
    elif kind == "gear":
        teeth = "".join(f'<path d="M{15*math.cos(a):.1f},{15*math.sin(a):.1f} L{22*math.cos(a):.1f},{22*math.sin(a):.1f}"/>' for a in [i * math.pi / 4 for i in range(8)])
        g.append(f'<circle r="11"/><circle r="4"/>{teeth}')
    elif kind == "baseline":
        g.append('<path d="M-20,-20 V20 H20"/><path d="M-14,2 H16" stroke-dasharray="5 5"/>')
    elif kind == "question":
        g.append('<path d="M-9,-10 a9,9 0 1 1 13,8 c-3,2 -4,4 -4,8"/><circle cy="17" r="1.6" fill="%s"/>' % col)
    g.append("</g>")
    return "".join(g)

def circ_icon(kind, cx, cy, r=26):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL}" fill-opacity=".12"/>' + icon(kind, cx, cy)

# ================================================================== blocco alto: linea dei tempi
def timeline(t):
    s = [card(36, 150, 1848, 470)]
    A, B = 250, 520
    XY, XE = 420, 1500; XP = (XY + XE) / 2
    # --- binario del piano
    s.append(T(64, A + 10, t["plan_lbl"], 32, 700, TEAL_D))
    s.append(f'<path d="M300,{A} H1790" stroke="{TEAL_D}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<path d="M1772,{A-11} l18,11 l-18,11" fill="none" stroke="{TEAL_D}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<rect x="{XY}" y="{A-7}" width="{XE-XY}" height="14" fill="{RED}" fill-opacity=".4"/>')
    s.append(f'<path d="M{XY},{A-52} V{A-60} H{XE} V{A-52}" fill="none" stroke="{RED_T}" stroke-width="2.6"/>')
    s.append(T((XY + XE) / 2, A - 70, t["period"], 22, 400, RED_T, "middle", it=True))
    kinds = ("warn", "doc", "flag")
    for i, (lab, desc, ex) in enumerate(t["markers"]):
        X = (XY, XP, XE)[i]
        s.append(f'<circle cx="{X}" cy="{A}" r="14" fill="{TEAL_D}" stroke="#fff" stroke-width="3.4"/>')
        s.append(T(X, A - 22, lab, 34, 700, TEAL_D, "middle"))
        s.append(circ_icon(kinds[i], X, A + 62))
        s.append(lines(X, A + 124, desc, 22, 290, 400, SLATE, "middle" == "middle" and False, 1.1, "middle"))
        s.append(T(X, A + 124 + len(desc) * 25 + 6, ex, 20, 400, SLATE, "middle", it=True))
        if i == 1:
            s.append(T(X, A + 124 + len(desc) * 25 + 34, t["report"], 20, 700, TEAL_D, "middle"))
    # piano aggiornato (cerchio di ritorno)
    s.append(arc_arrow(1692, A + 62, 24, 30, 330, OCHRE_D, 4.2))
    s.append(lines(1726, A + 58, t["loop"], 19, 150, 700, OCHRE_D, False, 1.12))
    s.append(f'<path d="M64,{A+216} H1860" stroke="#B7C6C4" stroke-width="2"/>')
    # --- binario della roadmap
    s.append(T(64, B + 10, t["road_lbl"], 32, 700, TEAL_D))
    s.append(f'<path d="M300,{B} H1790" stroke="{TEAL_D}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<path d="M1772,{B-11} l18,11 l-18,11" fill="none" stroke="{TEAL_D}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<rect x="{XY}" y="{B-7}" width="{XE-XY}" height="14" fill="{RED}" fill-opacity=".4"/>')
    for k, yr in enumerate(range(2026, 2031)):
        x = XY + 270 * k
        s.append(f'<path d="M{x},{B-12} V{B+12}" stroke="{TEAL_D}" stroke-width="3.4"/>')
        s.append(T(x, B + 40, str(yr), 24, 700 if yr == 2030 else 400, TEAL_D if yr == 2030 else SLATE, "middle"))
    s.append(T(XY + 10, B - 26, t["road_bar"], 22, 400, SLATE, it=True))
    xf = XY + 270 * 3                                     # 31 dicembre 2028 = inizio del 2029
    s.append(f'<path d="M{xf},{B} V{B-52}" stroke="{OCHRE_D}" stroke-width="3.4"/>')
    s.append(f'<path d="M{xf},{B-52} H{xf+34} L{xf+24},{B-42} L{xf+34},{B-32} H{xf}" fill="{OCHRE}" stroke="{OCHRE_D}" stroke-width="2.4" stroke-linejoin="round"/>')
    s.append(lines(xf, B + 72, t["flag"], 20, 260, 700, OCHRE_D, False, 1.15, "middle"))
    s.append(f'<circle cx="{XE}" cy="{B}" r="13" fill="{TEAL_D}" stroke="#fff" stroke-width="3.4"/>')
    s.append(lines(XE, B + 72, t["road_end"], 20, 150, 700, TEAL_D, False, 1.15, "middle"))
    s.append(lines(XY, B + 72, t["road_rule"], 20, 230, 400, SLATE, True, 1.15))
    return "".join(s)

# ================================================================== blocchi in basso
Y0B = 640
def steps_block(t):
    s = [card(36, Y0B, 880, 250), T(64, Y0B + 42, t["steps_h"], 27, 700, TEAL_D)]
    w, h, step = 164, 62, 154
    for i, (name, q) in enumerate(t["steps"]):
        x = 64 + i * step; y = Y0B + 62
        pts = [(x, y), (x + w - 20, y), (x + w, y + h / 2), (x + w - 20, y + h), (x, y + h)]
        if i: pts.append((x + 20, y + h / 2))
        s.append(f'<polygon points="{" ".join(f"{px:.1f},{py:.1f}" for px, py in pts)}" fill="{TEAL_D}" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>')
        cx = x + w / 2 + (8 if i else -2)
        if _width(name, 22, True) > w - 44: WARN.append(f"nome tappa troppo largo: {name}")
        s.append(T(cx, y + h / 2 + 8, name, 22, 700, "#fff", "middle"))
        ql = wrap([q], 21, 140)
        s.append(lines(x + w / 2 - 6, y + h + 32, ql, 21, 150, 400, SLATE, False, 1.15, "middle"))
    return "".join(s)

def say_block(t):
    s = [card(936, Y0B, 640, 250), T(964, Y0B + 42, t["say_h"], 27, 700, TEAL_D)]
    for i, (name, sub, kind) in enumerate(t["say"]):
        col, row = i % 2, i // 2
        x = 964 + col * 300; y = Y0B + 70 + row * 56
        s.append(circ_icon(kind, x + 22, y + 18, 22))
        s.append(T(x + 56, y + 18, name, 22, 700, SLATE))
        if _width(sub, 19) > 236: WARN.append(f"sottotitolo troppo largo: {sub}")
        s.append(T(x + 56, y + 42, sub, 19, 400, SLATE))
    return "".join(s)

def coop_block(t):
    s = [card(1596, Y0B, 288, 250), T(1620, Y0B + 42, t["coop_h"], 27, 700, TEAL_D)]
    cy = Y0B + 94
    s.append(f'<path d="M1636,{cy-30} q-14,10 -10,30 q4,22 28,24 q22,0 28,-22 q4,-24 -14,-34 q-18,-6 -32,2 z" fill="{TEAL}" fill-opacity=".25" stroke="{TEAL_D}" stroke-width="3"/>')
    s.append(f'<path d="M1800,{cy-26} q18,-8 34,4 q12,16 4,36 q-12,22 -36,16 q-22,-8 -20,-34 q2,-14 18,-22 z" fill="{OCHRE}" fill-opacity=".3" stroke="{OCHRE_D}" stroke-width="3"/>')
    s.append(f'<path d="M1706,{cy} H1776" stroke="{TEAL_D}" stroke-width="4" stroke-linecap="round"/><path d="M1764,{cy-9} l12,9 l-12,9" fill="none" stroke="{TEAL_D}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="M1710,{cy-14} q6,-8 12,0 t12,0 t12,0" fill="none" stroke="{TEAL_D}" stroke-width="2.4" stroke-linecap="round"/>')
    s.append(lines(1620, Y0B + 158, t["coop"], 20, 256, 400, SLATE, False, 1.18))
    return "".join(s)

# ================================================================== layout "wide" (1920×1080)
def build(lang):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 76, t["title"], 58, 700, TEAL_D), T(48, 122, t["subtitle"], 30, 400, SLATE),
            f'<g id="timeline">{timeline(t)}</g>', f'<g id="steps">{steps_block(t)}</g>',
            f'<g id="say">{say_block(t)}</g>', f'<g id="coop">{coop_block(t)}</g>',
            f'<g id="definition">{band(36, 910, 1848, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    svg = svg_wrap("\n".join(body), t["alt_title"], " ".join(t["alt_desc"].split()), lang, W, H)
    stem = OUT / f"piano_{lang}"
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
