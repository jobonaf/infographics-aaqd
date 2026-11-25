"""common/layout.py - helper condivisi di layout per le infografiche della serie AAQD (slide 1920x1080).

Uso in NN-slug/build.py:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
    from svgkit import *
    from layout import *
"""
import math
import pathlib

from svgkit import T, SLATE, TEAL, TEAL_D, GREY, RED, RED_T, OCHRE, esc, W, H

WARN = []

# ------------------------------------------------------------------ misura del testo
_FONTS = {}
_FONT_MISSING = [False]
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
_FONT_DIR = _REPO_ROOT / "assets" / "fonts"


def _font(bold):
    """Carica Source Sans 3 dal repository, poi dai font di sistema."""
    if bold in _FONTS:
        return _FONTS[bold]

    f = None
    try:
        from PIL import ImageFont

        repo_names = (
            ("SourceSans3-Bold.ttf", "SourceSans3-Bold.otf", "SourceSans3-SemiBold.ttf", "SourceSans3-SemiBold.otf")
            if bold
            else ("SourceSans3-Regular.ttf", "SourceSans3-Regular.otf")
        )
        candidates = [_FONT_DIR / name for name in repo_names]

        system_dirs = (
            pathlib.Path.home() / ".fonts",
            pathlib.Path("/usr/share/fonts"),
            pathlib.Path("/usr/local/share/fonts"),
            pathlib.Path("C:/Windows/Fonts"),
        )
        for directory in system_dirs:
            if not directory.exists():
                continue
            for name in repo_names:
                match = next(iter(directory.rglob(name)), None)
                if match is not None:
                    candidates.append(match)

        for path in candidates:
            if path.is_file():
                f = ImageFont.truetype(str(path), 100)
                break
    except (ImportError, OSError):
        pass

    if f is None and not _FONT_MISSING[0]:
        _FONT_MISSING[0] = True
        WARN.append(
            "font Source Sans 3 NON trovato: larghezze stimate, render non affidabile "
            "(vedi methods.txt, sez. 2)"
        )

    _FONTS[bold] = f
    return f


def width(txt, size, bold=False):
    f = _font(bold)
    if f is not None:
        return f.getlength(txt) * size / 100
    return len(txt) * size * 0.40


def wrap(ls, size, maxw, w=400):
    words = " ".join(ls).split()
    out, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if cur and width(trial, size, w == 700) > maxw:
            out.append(cur)
            cur = wd
        else:
            cur = trial
    return out + [cur]


def lines(x, y, ls, size, maxw, w=400, fill=SLATE, it=False, lh=1.22, anchor="start"):
    for line in ls:
        wd = width(line, size, w == 700)
        if wd > maxw:
            WARN.append(f"riga troppo larga ({wd:.0f}>{maxw:.0f}): {line}")
    return T(x, y, ls, size, w, fill, anchor, it=it, lh=lh)


def para(x, y, ls, size, maxw, **kw):
    out = wrap(ls, size, maxw, kw.get("w", 400))
    return lines(x, y, out, size, maxw, **kw), len(out)


def fmt(x, nd, lang):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "it" else s


def tsub(x, y, parts, size, w=400, fill=SLATE, anchor="start"):
    """Testo con pedici/apici usando elementi text con x esplicito."""
    segs = []
    for part in parts:
        kind, txt = part if isinstance(part, tuple) else ("n", part)
        txt = txt.replace(" ", "\u00a0")
        fs = size if kind == "n" else size * 0.68
        dy = {"n": 0.0, "sub": 0.20, "sup": -0.34}[kind] * size
        segs.append((txt, fs, dy, width(txt, fs, w == 700)))
    total = sum(seg[3] for seg in segs)
    cx = x - {"start": 0, "middle": total / 2, "end": total}[anchor]
    out = []
    wattr = f' font-weight="{w}"' if w != 400 else ""
    for txt, fs, dy, wd in segs:
        out.append(f'<text x="{cx:.1f}" y="{y + dy:.1f}" font-size="{fs:.1f}" fill="{fill}"{wattr}>{esc(txt)}</text>')
        cx += wd
    return "<g>" + "".join(out) + "</g>"


# ------------------------------------------------------------------ elementi
def header(title, subtitle):
    return T(48, 76, title, 58, 700, TEAL_D) + T(48, 122, subtitle, 30, 400, SLATE)


def card(x, y, w, h, rx=30):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#fff" stroke="#B7C6C4" stroke-width="2.6"/>'


def badge(cx, cy, n, r=19):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL_D}"/>' + T(cx, cy + 8, str(n), 23, 700, "#fff", "middle")


def pill_w(label, filled=False, size=18):
    return width(label, size, filled) + 22


def pill(x, y, label, filled=False, size=18):
    pw = pill_w(label, filled, size)
    h = size + 11
    if filled:
        return f'<rect x="{x:.1f}" y="{y}" width="{pw:.1f}" height="{h}" rx="{h/2}" fill="{TEAL_D}"/>' + T(x + 11, y + h - 9, label, size, 700, "#fff")
    return f'<rect x="{x:.1f}" y="{y}" width="{pw:.1f}" height="{h}" rx="{h/2}" fill="#fff" stroke="{GREY}" stroke-width="2.2"/>' + T(x + 11, y + h - 9, label, size, 400, SLATE)


def chevron(x, y, w, h, label, first=False, fill=TEAL_D, size=22, notch=20):
    pts = [(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h), (x, y + h)]
    if not first:
        pts.append((x + notch, y + h / 2))
    if width(label, size, True) > w - 2 * notch - 4:
        WARN.append(f"etichetta di chevron troppo larga: {label}")
    cx = x + w / 2 + (0 if first else notch / 3)
    points = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<polygon points="{points}" fill="{fill}" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>' + T(cx, y + h / 2 + 8, label, size, 700, "#fff", "middle")


def small_arrow(cx, cy):
    return f'<path d="M{cx-12},{cy-9} h10 v-9 l16,18 l-16,18 v-9 h-10 z" fill="{TEAL_D}"/>'


def arrow(x1, y1, x2, y2, col=TEAL_D, sw=4):
    ang = math.atan2(y2 - y1, x2 - x1)
    length = 12 + sw
    a1 = (x2 - length * math.cos(ang - 0.45), y2 - length * math.sin(ang - 0.45))
    a2 = (x2 - length * math.cos(ang + 0.45), y2 - length * math.sin(ang + 0.45))
    return (f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>'
            f'<path d="M{a1[0]:.1f},{a1[1]:.1f} L{x2:.1f},{y2:.1f} L{a2[0]:.1f},{a2[1]:.1f}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ icone a tratto
def icon(kind, cx, cy, col=TEAL_D):
    st = f'fill="none" stroke="{col}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
    g = [f'<g transform="translate({cx},{cy})" {st}>']
    if kind == "warn":
        g.append(f'<path d="M0,-21 L21,17 H-21 Z"/><path d="M0,-8 V5"/><circle cy="11" r="1.4" fill="{col}"/>')
    elif kind == "doc": g.append('<path d="M-14,-22 H6 L16,-12 V22 H-14 Z M6,-22 V-12 H16 M-7,-2 H9 M-7,7 H9 M-7,15 H3"/>')
    elif kind == "flag": g.append('<path d="M-14,22 V-22"/><path d="M-14,-22 H16 L8,-12 L16,-2 H-14"/>')
    elif kind == "pin": g.append('<path d="M0,22 C-14,6 -17,0 -17,-8 a17,17 0 0 1 34,0 c0,8 -3,14 -17,30z"/><circle cy="-8" r="5"/>')
    elif kind == "area": g.append('<path d="M-20,-4 L-8,-20 L14,-14 L20,6 L4,20 L-16,14 Z"/>')
    elif kind == "source": g.append('<path d="M-20,20 V-2 H-6 V20 M-6,20 V-22 H8 V20 M8,20 H22 M-24,20 H24"/>')
    elif kind == "gear":
        teeth = "".join(f'<path d="M{15*math.cos(a):.1f},{15*math.sin(a):.1f} L{22*math.cos(a):.1f},{22*math.sin(a):.1f}"/>' for a in [i * math.pi / 4 for i in range(8)])
        g.append(f'<circle r="11"/><circle r="4"/>{teeth}')
    elif kind == "baseline": g.append('<path d="M-20,-20 V20 H20"/><path d="M-14,2 H16" stroke-dasharray="5 5"/>')
    elif kind == "question": g.append(f'<path d="M-9,-10 a9,9 0 1 1 13,8 c-3,2 -4,4 -4,8"/><circle cy="17" r="1.6" fill="{col}"/>')
    elif kind == "check": g.append('<circle r="21"/><path d="M-10,1 L-3,9 L11,-9"/>')
    elif kind == "wave": g.append('<path d="M-22,6 C-14,-18 -6,-18 0,0 C6,18 14,18 22,-6"/><path d="M-22,20 H22" stroke-width="2.6"/>')
    elif kind == "canyon": g.append('<path d="M-22,22 V-14 H-8 V22 M8,22 V-18 H22 V22 M-26,22 H26"/>')
    elif kind == "people": g.append('<circle cx="-9" cy="-10" r="6"/><path d="M-20,16 v-6 a11,9 0 0 1 22,0 v6"/><circle cx="12" cy="-6" r="5"/><path d="M6,16 v-4 a9,8 0 0 1 16,0 v4"/>')
    elif kind == "road": g.append('<path d="M-9,22 L-4,-22 M9,22 L4,-22"/><path d="M0,-18 v8 M0,-2 v8 M0,12 v8" stroke-width="2.6"/>')
    elif kind == "leaf": g.append('<path d="M-18,16 C-20,-8 0,-22 20,-20 C22,0 6,18 -18,16 Z M-18,16 L8,-8"/>')
    elif kind == "grid":
        for i in (-14, 0, 14): g.append(f'<path d="M-21,{i} H21 M{i},-21 V21"/>')
    else: WARN.append(f"icona sconosciuta: {kind}")
    g.append("</g>")
    return "".join(g)


def circ_icon(kind, cx, cy, r=26, col=TEAL_D):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL}" fill-opacity=".12"/>' + icon(kind, cx, cy, col)


# ------------------------------------------------------------------ geometria
def smooth(P, closed=False):
    n = len(P)
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in (range(n) if closed else range(n - 1)):
        p0 = P[(i - 1) % n] if closed or i > 0 else P[0]
        p1, p2 = P[i], P[(i + 1) % n]
        p3 = P[(i + 2) % n] if closed or i + 2 < n else P[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + (" Z" if closed else "")


def sample(P, step):
    out = []
    for (x1, y1), (x2, y2) in zip(P[:-1], P[1:]):
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5
        if length == 0: continue
        k = max(1, int(length // step))
        for j in range(k):
            out.append((x1 + (x2 - x1) * j / k, y1 + (y2 - y1) * j / k, (x2 - x1) / length, (y2 - y1) / length))
    return out


# ------------------------------------------------------------------ uscita
def render(svg_text, stem, png_width=3840):
    stem = pathlib.Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    stem.with_suffix(".svg").write_text(svg_text, encoding="utf-8")
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(stem.with_suffix(".png")), output_width=png_width)
        cairosvg.svg2pdf(bytestring=svg_text.encode(), write_to=str(stem.with_suffix(".pdf")))
    except ImportError:
        WARN.append("cairosvg non installato: generato solo l'SVG")
    return stem
