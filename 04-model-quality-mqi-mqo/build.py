#!/usr/bin/env python3
"""Infografica 02 – MQI e MQO: la qualità dei modelli nella valutazione (Dir. 2024/2881, Allegato V).

Uso:  python build.py            # IT + EN, layout "wide" (16:9, slide)
      python build.py it         # solo italiano
Tutti i testi stanno in strings/<lingua>.yaml; geometrie e numeri sono calcolati qui, quindi le lingue non possono
divergere. I valori delle stazioni nel pannello 3 e le serie nel pannello 1 sono SINTETICI e dichiarati come tali.
Layout "mobile": non ancora previsto per questa infografica."""
import sys, pathlib
import numpy as np, yaml
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "common"))
from svgkit import *

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ valori normativi (vedi sources.md)
LV = 20.0                 # PM10, valore limite annuo, µg/m³
U_LV_REL = 0.20           # incertezza massima misure fisse al VL, relativa (4,0 µg/m³ su 20)
BETA = {"pm25": 1.7, "pm10": 1.3, "no2": 1.4}   # rapporto max modello / misure fisse, lungo termine
U_LV = U_LV_REL * LV      # 4,0 µg/m³ (= U_Ø per la media annua)
BETA10 = BETA["pm10"]

def u_fix(o):
    """U_O,fix(O): costante (= U_Ø) fino al VL, poi proporzionale (formula del documento tecnico, §3.4.1)."""
    o = np.asarray(o, float)
    return np.where(o <= LV, U_LV, o * U_LV / LV)

# ------------------------------------------------------------------ dati sintetici (pannelli 1 e 3)
# stazioni sintetiche del target plot: (CRMSE normalizzato con segno, bias normalizzato); MQI = distanza dall'origine
STATIONS = np.array([(-0.30, -0.15), (-0.18, -0.42), (0.25, -0.30), (-0.45, 0.20), (0.32, -0.46), (-0.52, -0.38),
                     (0.48, 0.30), (0.62, -0.52), (-0.70, 0.45), (0.55, 0.78), (-0.38, -0.85), (0.85, 0.72)])
MQI_STATIONS = np.hypot(STATIONS[:, 0], STATIONS[:, 1])
P90 = float(np.percentile(MQI_STATIONS, 90))
N_IN, N_ALL = int((MQI_STATIONS <= 1).sum()), len(MQI_STATIONS)
assert P90 <= 1.0 and N_IN / N_ALL >= 0.9, "esempio sintetico incoerente: l'MQO deve risultare soddisfatto"

def fmt(x, nd, lang):
    s = f"{x:.{nd}f}"
    return s.replace(".", ",") if lang == "it" else s

_FONTS = {}
def _width(txt, size, bold):
    """Larghezza del testo in px (metriche di Source Sans 3 se disponibile, altrimenti stima)."""
    try:
        from PIL import ImageFont
        key = (bold,)
        if key not in _FONTS:
            for d in (pathlib.Path.home() / ".fonts", pathlib.Path("/usr/share/fonts/opentype/source-sans"), pathlib.Path("/usr/share/fonts")):
                f = next(iter(d.rglob("SourceSans3-Bold.otf" if bold else "SourceSans3-Regular.otf")), None) if d.exists() else None
                if f: _FONTS[key] = ImageFont.truetype(str(f), 100); break
            else: _FONTS[key] = None
        if _FONTS[key]: return _FONTS[key].getlength(txt) * size / 100
    except ImportError:
        pass
    return len(txt) * size * 0.54

def tsub(x, y, parts, size, w=400, fill=SLATE, anchor="start"):
    """Testo con pedici/apici: parts = stringhe oppure tuple ('sub'|'sup', testo).
    Ogni pezzo è un <text> con x esplicito (metriche misurate): resa identica in tutti i renderer."""
    segs = []
    for p in parts:
        kind, txt = p if isinstance(p, tuple) else ("n", p)
        txt = txt.replace(" ", "\u00a0")          # gli spazi ai bordi del pezzo non vanno collassati
        fs = size if kind == "n" else size * 0.68
        dy = {"n": 0.0, "sub": 0.20, "sup": -0.34}[kind] * size
        segs.append((txt, fs, dy, _width(txt, fs, w == 700)))
    total = sum(sg[3] for sg in segs)
    cx = x - {"start": 0, "middle": total / 2, "end": total}[anchor]
    out = []
    for txt, fs, dy, wd in segs:
        wattr = f' font-weight="{w}"' if w != 400 else ""
        out.append(f'<text x="{cx:.1f}" y="{y + dy:.1f}" font-size="{fs:.1f}" fill="{fill}"{wattr}>{esc(txt)}</text>')
        cx += wd
    return "<g>" + "".join(out) + "</g>"

def small_arrow(cx, cy):
    return f'<path d="M{cx-12},{cy-9} h10 v-9 l16,18 l-16,18 v-9 h-10 z" fill="{TEAL_D}"/>'

# ================================================================== pannello 1: l'indicatore
def panel1(t, lang, x0, y0, w):
    s = ['<g id="panel1">', panel(x0, y0, w, 710, 1, t["h1"])]
    # serie sintetiche osservato / modellato e scarto tra le due
    L, R, top, bot = x0 + 30, x0 + w - 30, y0 + 96, y0 + 232
    n = 36
    tt = np.linspace(0, 1, n)
    obs = 30 + 11 * np.sin(6.0 * tt) + 3.5 * np.sin(17 * tt + 0.6)
    mod = 28 + 8.5 * np.sin(6.0 * tt + 0.42) + 2.0 * np.sin(15 * tt)
    lo, hi = 10, 50
    X = lambda i: L + (R - L) * tt[i]
    Y = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    s.append(f'<path d="M{L},{bot} H{R}" stroke="{SLATE}" stroke-width="2.2"/>')
    gap = " ".join(f"{X(i):.1f},{Y(obs[i]):.1f}" for i in range(n)) + " " + " ".join(f"{X(i):.1f},{Y(mod[i]):.1f}" for i in range(n - 1, -1, -1))
    s.append(f'<polygon points="{gap}" fill="{RED}" fill-opacity=".16"/>')
    s.append(f'<polyline points="{" ".join(f"{X(i):.1f},{Y(obs[i]):.1f}" for i in range(n))}" fill="none" stroke="{SLATE}" stroke-width="3.2" stroke-linejoin="round"/>')
    s.append(f'<polyline points="{" ".join(f"{X(i):.1f},{Y(mod[i]):.1f}" for i in range(n))}" fill="none" stroke="{TEAL}" stroke-width="3.6" stroke-linejoin="round"/>')
    ly = y0 + 262
    s.append(f'<path d="M{L},{ly-7} h30" stroke="{SLATE}" stroke-width="3.2"/>' + T(L + 38, ly, t["leg_obs"], 22))
    s.append(f'<path d="M{L+175},{ly-7} h30" stroke="{TEAL}" stroke-width="3.6"/>' + T(L + 213, ly, t["leg_mod"], 22))
    s.append(T(L, y0 + 292, t["synthetic"], 20, 400, SLATE, it=True))
    # frazione MQI = RMSE / sqrt(U_O² + U_M²)
    yb, cxf = y0 + 380, x0 + 238
    s.append(T(x0 + 28, yb + 10, "MQI =", 30, 700, TEAL_D))
    s.append(f'<path d="M{cxf-118},{yb} H{cxf+118}" stroke="{SLATE}" stroke-width="2.6"/>')
    s.append(T(cxf, yb - 14, "RMSE", 30, 700, SLATE, "middle"))
    s.append(tsub(cxf, yb + 38, ["√( U", ("sub", "O"), ("sup", "2"), " + U", ("sub", "M"), ("sup", "2"), " )"], 28, 700, SLATE, "middle"))
    s.append(T(x0 + 30, y0 + 472, t["rmse_def"], 22))
    s.append(T(x0 + 30, y0 + 540, t["u_def"], 22))
    s.append(T(x0 + 30, y0 + 620, t["longterm"], 24, 700, TEAL_D))
    return "".join(s) + "</g>"

# ================================================================== pannello 2: incertezza ammessa
def panel2(t, lang, x0, y0, w):
    s = ['<g id="panel2">', panel(x0, y0, w, 710, 2, t["h2"])]
    left, right, top, bot = x0 + 78, x0 + w - 28, y0 + 118, y0 + 356
    XMAX, YMAX = 70.0, 20.0
    X = lambda o: left + (right - left) * o / XMAX
    Y = lambda u: bot - (bot - top) * u / YMAX
    for v in range(0, 21, 5):                                             # griglia e tacche dell'asse y
        s.append(f'<path d="M{left},{Y(v):.1f} H{right}" stroke="{GREY}" stroke-opacity=".45" stroke-width="1.6"/>')
        s.append(T(left - 10, Y(v) + 8, str(v), 22, 400, SLATE, "end"))
    for v in (0, 20, 40, 60):
        s.append(f'<path d="M{X(v):.1f},{bot} v8" stroke="{SLATE}" stroke-width="2.2"/>')
        s.append(T(X(v), bot + 34, str(v), 22, 400, SLATE, "middle"))
    s.append(f'<path d="M{left},{top-6} V{bot} H{right}" fill="none" stroke="{SLATE}" stroke-width="2.4"/>')
    s.append(T(left - 58, top - 24, t["y_title"], 22, 400, SLATE))
    s.append(T((left + right) / 2, bot + 66, t["x_title"], 22, 400, SLATE, "middle"))
    # linea del valore limite
    s.append(f'<path d="M{X(LV):.1f},{top-6} V{bot}" stroke="{SLATE}" stroke-width="2.6" stroke-dasharray="9 6"/>')
    s.append(T(X(LV) + 10, top + 14, t["lv_label"].format(LV=fmt(LV, 0, lang)), 22, 700, SLATE))
    # curve: misure fisse e modello (= β · misure fisse)
    oo = np.linspace(0, XMAX, 141)
    um = u_fix(oo)
    um_model = BETA10 * um
    pts = lambda u: " ".join(f"{X(o):.1f},{Y(v):.1f}" for o, v in zip(oo, u))
    s.append(f'<polyline points="{pts(um_model)}" fill="none" stroke="{OCHRE}" stroke-width="4.6" stroke-linejoin="round"/>')
    s.append(f'<polyline points="{pts(um)}" fill="none" stroke="{TEAL_D}" stroke-width="4.6" stroke-linejoin="round"/>')
    s.append(T(X(5), Y(BETA10 * U_LV) - 10, fmt(BETA10 * U_LV, 1, lang), 22, 700, "#8A5F0C"))
    s.append(T(X(5), Y(U_LV) + 26, fmt(U_LV, 1, lang), 22, 700, TEAL_D))
    # legenda
    ly = y0 + 456
    s.append(f'<path d="M{x0+30},{ly-7} h34" stroke="{TEAL_D}" stroke-width="4.6"/>')
    s.append(tsub(x0 + 74, ly, [t["leg_meas"] + ": U", ("sub", "O,fix")], 22))
    s.append(f'<path d="M{x0+30},{ly+28} h34" stroke="{OCHRE}" stroke-width="4.6"/>')
    s.append(tsub(x0 + 74, ly + 35, [t["leg_model"] + ": U", ("sub", "M"), " = β · U", ("sub", "O,fix")], 22))
    s.append(T(x0 + 30, y0 + 527, t["cap2a"], 22, 700, SLATE))
    s.append(T(x0 + 30, y0 + 554, t["cap2b"].format(LV=fmt(LV, 0, lang), beta=fmt(BETA10, 1, lang)), 22))
    s.append(T(x0 + 30, y0 + 596, t["cap2c"], 22))
    b2 = f"PM{fmt(2.5,1,lang)} {fmt(BETA['pm25'],1,lang)} · PM10 {fmt(BETA['pm10'],1,lang)} · NO2 {fmt(BETA['no2'],1,lang)}"
    s.append(T(x0 + 30, y0 + 656, [t["beta_lines"][0], b2], 22, 700, TEAL_D))
    return "".join(s) + "</g>"

# ================================================================== pannello 3: obiettivo MQO (target plot FAIRMODE)
def panel3(t, lang, x0, y0, w):
    s = ['<g id="panel3">', panel(x0, y0, w, 710, 3, t["h3"])]
    side, R1 = 266, 95.0                                   # lato del riquadro; raggio del cerchio MQI = 1
    left, top = x0 + 66, y0 + 104
    cx, cy = left + side / 2, top + side / 2
    right, bottom = left + side, top + side
    s.append(f'<rect id="target-frame" x="{left}" y="{top}" width="{side}" height="{side}" fill="#fff" stroke="{GREY}" stroke-width="2"/>')
    s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R1}" fill="{TEAL}" fill-opacity=".10"/>')
    s.append(f'<path d="M{left},{cy:.1f} H{right} M{cx:.1f},{top} V{bottom}" stroke="{SLATE}" stroke-width="1.8"/>')
    s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R1/2}" fill="none" stroke="{TEAL_D}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append(f'<circle id="mqo-circle" cx="{cx:.1f}" cy="{cy:.1f}" r="{R1}" fill="none" stroke="{TEAL_D}" stroke-width="3.6"/>')
    s.append(T(cx + R1 / 2 + 5, cy - 7, fmt(0.5, 1, lang), 20, 400, SLATE))
    s.append(T(cx + R1 + 8, cy + 22, "1", 20, 700, TEAL_D))
    s.append(T(cx + 8, top + 19, t["bias_pos"], 20, 400, SLATE))
    s.append(T(cx + 8, bottom - 8, t["bias_neg"], 20, 400, SLATE))
    s.append(T(left + 10, cy - 8, "R", 22, 700, SLATE))
    s.append(T(right - 10, cy - 8, "SD", 22, 700, SLATE, "end"))
    for (xn, yn), m in zip(STATIONS, MQI_STATIONS):
        s.append(dot(cx + xn * R1, cy - yn * R1, 8.5, OCHRE if m > 1 else TEAL, 'stroke="#fff" stroke-width="2"'))
    s.append(T(left + 8, top + 24, t["count3"].format(n=N_IN, N=N_ALL), 20, 700, TEAL_D))
    s.append(T(cx, bottom + 30, t["axis_x3"], 22, 400, SLATE, "middle"))
    s.append(T(x0 + 38, cy, t["axis_y3"], 22, 400, SLATE, "middle", extra=f'transform="rotate(-90 {x0+38} {cy:.1f})"'))
    s.append(T(x0 + 30, y0 + 440, t["cap3a"], 21, 400, SLATE))
    s.append(T(x0 + 30, y0 + 464, t["cap3b"], 21, 400, SLATE))
    s.append(T(x0 + 30, y0 + 488, t["synthetic"], 20, 400, SLATE, it=True))
    s.append(T(x0 + 30, y0 + 532, t["ok_line1"], 26, 700, TEAL_D))
    s.append(tsub(x0 + 30, y0 + 564, ["MQI", ("sub", "90"), " ≤ 1"], 26, 700, TEAL_D))
    w_h = _width("MQI", 26, True) + _width("90", 26 * 0.68, True) + _width("\u00a0≤\u00a01", 26, True)
    s.append(T(x0 + 30 + w_h + 14, y0 + 564, t["ex3"].format(p90=fmt(P90, 2, lang)), 21, 400, SLATE, it=True))
    for i, key in enumerate(("b1", "b2")):
        yy = y0 + 612 + i * 58
        s.append(dot(x0 + 38, yy - 6, 5.5, TEAL_D))
        s.append(T(x0 + 56, yy, t[key], 22))
    return "".join(s) + "</g>"

# ================================================================== pannello 4: data fusion, leave-one-out
def panel4(t, lang, x0, y0, w):
    s = ['<g id="panel4">', panel(x0, y0, w, 710, 4, t["h4"])]
    cx, cy, R, n = x0 + w / 2, y0 + 215, 68, 7
    for k in range(n):
        a = np.radians(-90 + k * 360 / n)
        x, y = cx + R * np.cos(a), cy + R * np.sin(a)
        if k == 0:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#fff" stroke="{RED_T}" stroke-width="3.6" stroke-dasharray="5 4"/>')
            s.append(T(x, y - 26, t["excluded"], 22, 700, RED_T, "middle"))
        else:
            s.append(dot(x, y, 13, TEAL, 'stroke="#fff" stroke-width="2.5"'))
    s.append(T(cx, cy - 3, t["center"], 22, 400, SLATE, "middle", lh=1.1))
    s.append(arc_arrow(cx, cy, 102, 125, 235, TEAL_D, 3.8) + arc_arrow(cx, cy, 102, 305, 415, TEAL_D, 3.8))
    for i, key in enumerate(("step1", "step2", "step3", "step4")):
        yy = y0 + 372 + i * 66
        s.append(T(x0 + 30, yy, str(i + 1), 26, 700, TEAL_D))
        s.append(T(x0 + 62, yy, t[key], 22))
    s.append(T(x0 + 30, y0 + 650, t["alt_subset"], 22, 400, SLATE, it=True))
    return "".join(s) + "</g>"

# ================================================================== layout "wide" (1920×1080, slide)
def layout_wide(t, lang):
    y0, gap = 170, 46
    ws = [395, 470, 400, 437]
    xs = [40]
    for wd in ws[:-1]: xs.append(xs[-1] + wd + gap)
    body = [f'<rect id="background" width="{W}" height="{H}" fill="{BEIGE}"/>',
            T(48, 86, t["title"], 58, 700, TEAL_D), T(48, 134, t["subtitle"], 30, 400, SLATE),
            panel1(t, lang, xs[0], y0, ws[0]), small_arrow(xs[0] + ws[0] + gap / 2, y0 + 355),
            panel2(t, lang, xs[1], y0, ws[1]), small_arrow(xs[1] + ws[1] + gap / 2, y0 + 355),
            panel3(t, lang, xs[2], y0, ws[2]), small_arrow(xs[2] + ws[2] + gap / 2, y0 + 355),
            panel4(t, lang, xs[3], y0, ws[3]),
            f'<g id="definition">{band(48, 910, 1824, 120, t["def_bold"], [t["def_l1"], t["def_l2"]])}</g>']
    return "\n".join(body), W, H

LAYOUTS = {"wide": (layout_wide, "", 3840)}

def build(lang, layout="wide"):
    t = yaml.safe_load((HERE / "strings" / f"{lang}.yaml").read_text(encoding="utf-8"))
    fn, suffix, png_w = LAYOUTS[layout]
    body, w, h = fn(t, lang)
    svg = svg_wrap(body, t["alt_title"], " ".join(t["alt_desc"].split()), lang, w, h)
    stem = OUT / f"mqi_mqo_{lang}{suffix}"
    stem.with_suffix(".svg").write_text(svg, encoding="utf-8")
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(stem.with_suffix(".png")), output_width=png_w)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(stem.with_suffix(".pdf")))
    except ImportError:
        print("cairosvg non installato: generato solo l'SVG")
    return stem

if __name__ == "__main__":
    langs = [a for a in sys.argv[1:] if a in ("it", "en")] or ["it", "en"]
    print("U_LV=%.1f µg/m³ | U_M(LV)=%.1f | MQI90 (sintetico)=%.3f | dentro il cerchio: %d/%d" % (U_LV, BETA10 * U_LV, P90, N_IN, N_ALL))
    for lang in langs:
        print("scritto", build(lang).name)
