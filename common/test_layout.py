"""Prova di common/layout.py: genera una pagina con tutte le funzioni e stampa gli avvisi. Uso: python test_layout.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svgkit import *
from layout import *

kinds = "warn doc flag pin area source gear baseline question check wave canyon people road leaf grid".split()
b = [f'<rect width="{W}" height="{H}" fill="{BEIGE}"/>', header("Prova di layout.py", "Tutte le funzioni di common/layout.py")]
b.append(card(36, 150, 1848, 150))
for i, k in enumerate(kinds):
    b.append(circ_icon(k, 90 + i * 112, 200)); b.append(T(90 + i * 112, 270, k, 20, 400, SLATE, "middle"))
b.append(card(36, 320, 900, 190))
for i, nm in enumerate(["Valutazione", "Screening", "Misure", "Scenari", "Adozione"]):
    b.append(chevron(64 + i * 154, 350, 164, 62, nm, first=(i == 0)))
for i in range(1, 6): b.append(badge(80 + (i - 1) * 60, 470, i))
b.append(pill(400, 450, "richiesto", True)); b.append(pill(400 + pill_w("richiesto", True) + 10, 450, "se serve"))
b.append(card(956, 320, 928, 190))
b.append(tsub(990, 380, ["MQI", ("sub", "90"), " = 0,97 µg/m", ("sup", "3")], 30, 700, TEAL_D))
b.append(T(990, 430, fmt(1234.5678, 2, "it") + "  /  " + fmt(1234.5678, 2, "en"), 26, 400, SLATE))
b.append(small_arrow(1300, 400)); b.append(arrow(1360, 400, 1560, 360, OCHRE, 4))
P = [(1620, 470), (1680, 380), (1760, 440), (1840, 360)]
b.append(f'<path d="{smooth(P)}" fill="none" stroke="{TEAL_D}" stroke-width="5"/>')
for (x, y, dx, dy) in sample(P, 40): b.append(dot(x, y, 4, RED))
b.append(card(36, 530, 1848, 340))
svg, n = para(64, 580, ["Questo paragrafo viene ri-spezzato automaticamente in base alla larghezza disponibile e si ferma entro i limiti del riquadro."], 24, 700)
b.append(svg)
b.append(lines(64, 700, ["Riga volutamente troppo lunga per la larghezza massima indicata, per provare che l'avviso scatti"], 24, 400))
b.append(icon("inesistente", 900, 800))
b.append(f'<g id="definition">{band(36, 910, 1848, 120, "Prova:", ["fascia di definizione di svgkit.", "Seconda riga."])}</g>')
stem = render(svg_wrap("\n".join(b), "Prova layout", "Pagina di prova di layout.py", "it", W, H), "/tmp/layout_test", 1920)
print("scritto", stem, "| paragrafo:", n, "righe")
for m in WARN: print("ATTENZIONE:", m)
