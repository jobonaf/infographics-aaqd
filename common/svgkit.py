"""svgkit: elementi grafici e stile condivisi dalla serie di infografiche AAQD.
Solo libreria standard + numpy; l'output è SVG puro (testo vivo, gruppi con id)."""
import html, math

# ---- design tokens (palette ispirata al logo del pacchetto R spatrep) ----
TEAL, TEAL_D, BEIGE = "#2A9D9A", "#1F5F63", "#EFEBDD"
RED, RED_T = "#D7372B", "#B5302A"          # RED per i simboli, RED_T per il testo (contrasto)
GREY, SLATE, OCHRE, ZONE = "#A9A59B", "#22343A", "#C58B1A", "#E6E4DC"
FONT = "'Source Sans 3','Source Sans Pro','Helvetica Neue',Arial,sans-serif"
W, H = 1920, 1080                           # tela 16:9
SYM_FONT = "'DejaVu Sans','Arial Unicode MS',sans-serif"   # per glifi matematici assenti nel font base


def esc(s):
    s = html.escape(s, quote=False)
    return s.replace("≤", f'<tspan font-family="{SYM_FONT}">≤</tspan>')


def T(x, y, s, size=24, w=400, fill=SLATE, anchor="start", it=False, lh=1.22, extra=""):
    """Testo (una riga o lista di righe)."""
    lines = s if isinstance(s, list) else [s]
    a = f'x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
    if w != 400: a += f' font-weight="{w}"'
    if it: a += ' font-style="italic"'
    if anchor != "start": a += f' text-anchor="{anchor}"'
    if extra: a += " " + extra
    if len(lines) == 1:
        return f"<text {a}>{esc(lines[0])}</text>"
    ts = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else round(size * lh, 1)}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    return f"<text {a}>{ts}</text>"


def panel(x, y, w, h, num, heading, gid=None, hs=36):
    k = hs / 36
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="#fff" stroke="{TEAL_D}" stroke-opacity=".35" stroke-width="2"/>'
            f'<circle cx="{x + 40}" cy="{y + 48}" r="{24 * k:.1f}" fill="{TEAL_D}"/>'
            + T(x + 40, y + 48 + 10 * k, str(num), round(28 * k), 700, "#fff", "middle")
            + T(x + 40 + 36 * k + 4, y + 48 + 12 * k, heading, hs, 700, TEAL_D))


def block_arrow(cx, cy):
    return f'<path d="M{cx-19},{cy-9} h16 v-12 l24,21 l-24,21 v-12 h-16 z" fill="{TEAL_D}"/>'


def band(x, y, w, h, bold, lines):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{TEAL_D}"/>'
            f'<text x="{x+38}" y="{y+50}" font-size="27" fill="#fff"><tspan font-weight="700">{esc(bold)}</tspan> {esc(lines[0])}</text>'
            f'<text x="{x+38}" y="{y+90}" font-size="27" fill="#fff">{esc(lines[1])}</text>')


def dot(x, y, r, fill, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" {extra}/>'


def excluded(x, y, r=9):
    d = r * 0.4
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
            f'<path d="M{x-d:.1f},{y-d:.1f} L{x+d:.1f},{y+d:.1f} M{x-d:.1f},{y+d:.1f} L{x+d:.1f},{y-d:.1f}" stroke="{GREY}" stroke-width="1.8" stroke-linecap="round"/>')


def station(x, y, label=None):
    s = dot(x, y, 11.5, RED, 'stroke="#fff" stroke-width="2.5"')
    if label:
        s += T(x + 17, y - 15, label, 30, 700, "#fff", extra='stroke="#fff" stroke-width="6" stroke-linejoin="round"')
        s += T(x + 17, y - 15, label, 30, 700, RED_T)
    return s


def point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def catmull(pts, n=24):
    """Spline Catmull-Rom: restituisce (campioni densi, path SVG cubico)."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    dense, d = [], ""
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        if i == 1: d = f"M{p1[0]:.1f},{p1[1]:.1f}"
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
        for k in range(n):
            t = k / n; u = 1 - t
            dense.append((u**3*p1[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3*p2[0],
                          u**3*p1[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3*p2[1]))
    dense.append(P[-2])
    return dense, d


def arc_arrow(cx, cy, r, a0, a1, color, sw=3.2):
    """Arco con punta di freccia (angoli in gradi, senso orario in coordinate SVG)."""
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    t = math.radians(a1 + 90)                       # tangente in uscita
    hx, hy = x1 + 5.5 * math.cos(t), y1 + 5.5 * math.sin(t)
    nx, ny = math.cos(math.radians(a1)), math.sin(math.radians(a1))
    tri = f"{hx:.1f},{hy:.1f} {x1+5*nx:.1f},{y1+5*ny:.1f} {x1-5*nx:.1f},{y1-5*ny:.1f}"
    return (f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<polygon points="{tri}" fill="{color}"/>')


def svg_wrap(body, title, desc, lang, w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" lang="{lang}" '
            f'font-family="{FONT}" role="img" aria-labelledby="t d">\n<title id="t">{html.escape(title)}</title>\n'
            f'<desc id="d">{html.escape(desc)}</desc>\n{body}\n</svg>\n')


def band_wrapped(x, y, w, h, bold, text, size, chars):
    """Banda con testo a capo automatico; la parte iniziale `bold` è in grassetto."""
    import textwrap
    lines = textwrap.wrap(bold + " " + text, chars)
    lh = size * 1.3
    y0 = y + (h - len(lines) * lh) / 2 + size * 0.85
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{TEAL_D}"/>']
    for i, ln in enumerate(lines):
        body = (f'<tspan font-weight="700">{esc(bold)}</tspan>{esc(ln[len(bold):])}' if i == 0 else esc(ln))
        out.append(f'<text x="{x + 38}" y="{y0 + i * lh:.1f}" font-size="{size}" fill="#fff">{body}</text>')
    return "".join(out)
