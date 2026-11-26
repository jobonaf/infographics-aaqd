#!/usr/bin/env python3
"""Genera presentation.json, rileva i frame SVG e crea copertina e chiusura."""
import argparse
import base64
from datetime import date
import html
import json
from pathlib import Path, PurePosixPath
import re
import urllib.parse
import xml.etree.ElementTree as ET

PANEL_RE = re.compile(r"^panel[-_ ]?(\d+)$", re.I)
FRAME_RE = re.compile(r"^(?:frame|section)[-_](.+)$", re.I)
EXCLUDED_DIRS = {".git", ".github", ".venv", "__pycache__", "old", "work", "node_modules"}
EXCLUDED_IDS = {"defs", "background", "bg", "grid", "clip", "mask", "filters", "styles", "symbols", "markers", "decorations", "decoration"}


def find_repo_root(explicit=None):
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not root.is_dir():
            raise SystemExit(f"Directory inesistente: {root}")
        return root
    here = Path(__file__).resolve().parent
    for candidate in (here, *here.parents):
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit("Repository non trovato: specificarlo con --root")


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def unique(values):
    seen, out = set(), []
    for value in values:
        if value not in seen:
            seen.add(value); out.append(value)
    return out


def human_label(group_id):
    match = PANEL_RE.fullmatch(group_id)
    if match:
        return f"Pannello {int(match.group(1))}"
    match = FRAME_RE.fullmatch(group_id)
    value = match.group(1) if match else group_id
    value = re.sub(r"[-_]+", " ", value).strip()
    return value[:1].upper() + value[1:]


def frame_ids(svg_path):
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError as exc:
        raise SystemExit(f"SVG non valido: {svg_path}: {exc}") from exc
    all_ids = unique(e.get("id") for e in root.iter() if local_name(e.tag) == "g" and e.get("id"))
    explicit = [x for x in all_ids if FRAME_RE.fullmatch(x)]
    panels = [x for x in all_ids if PANEL_RE.fullmatch(x)]
    direct = [e.get("id") for e in list(root) if local_name(e.tag) == "g" and e.get("id")]
    candidates = explicit or sorted(panels, key=lambda x: int(PANEL_RE.fullmatch(x).group(1))) or direct
    return unique(x for x in candidates if x.lower() not in EXCLUDED_IDS and not x.startswith("_"))


def title_from_path(relative):
    folder = PurePosixPath(relative).parts[-3]
    value = re.sub(r"^\d+-", "", folder).replace("-", " ")
    return value[:1].upper() + value[1:]


def slide_id(relative):
    folder = PurePosixPath(relative).parts[-3]
    return re.sub(r"[^a-z0-9]+", "-", folder.lower()).strip("-")


def active_svg(path, root):
    parts = path.relative_to(root).parts
    return path.parent.name == "out" and not any(p in EXCLUDED_DIRS or p.startswith(".") for p in parts)


def font_css(root):
    font_dir = root / "assets" / "fonts"
    rules = []
    for weight, names in ((400, ("SourceSans3-Regular.ttf", "SourceSans3-Regular.otf")), (700, ("SourceSans3-Bold.ttf", "SourceSans3-Bold.otf"))):
        path = next((font_dir / n for n in names if (font_dir / n).is_file()), None)
        if path:
            mime = "font/ttf" if path.suffix.lower() == ".ttf" else "font/otf"
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            rules.append(f"@font-face{{font-family:'Source Sans 3';font-weight:{weight};src:url(data:{mime};base64,{data});}}")
    return "".join(rules)


def text_slide(path, root, kind, title, subtitle, lines, footer):
    path.parent.mkdir(parents=True, exist_ok=True)
    y0 = 510 if kind == "title" else 420
    rows = "".join(
        f'<text x="160" y="{y0+i*58}" font-size="30" fill="#22343A">{html.escape(str(line))}</text>'
        for i, line in enumerate(lines)
    )
    label = "PRESENTAZIONE" if kind == "title" else "RIFERIMENTI E LICENZA"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" font-family="Source Sans 3,Arial,sans-serif">
<defs><style>{font_css(root)}</style></defs>
<rect width="1920" height="1080" fill="#EFEBDD"/><rect width="34" height="1080" fill="#1F5F63"/>
<text x="160" y="170" font-size="22" font-weight="700" letter-spacing="3" fill="#2A9D9A">{label}</text>
<text x="160" y="285" font-size="68" font-weight="700" fill="#1F5F63">{html.escape(title)}</text>
<text x="160" y="355" font-size="34" fill="#22343A">{html.escape(subtitle)}</text>
{rows}
<text x="160" y="990" font-size="22" fill="#667879">{html.escape(footer)}</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def rel_src(path, output_path):
    return path.relative_to(output_path.parent).as_posix()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root")
    ap.add_argument("--repo", default="jobonaf/infographics-aaqd")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--language", default="it", choices=("it", "en"))
    ap.add_argument("--output", default="presentation.json")
    ap.add_argument("--local-src", action="store_true")
    ap.add_argument("--no-summary", action="store_true")
    ap.add_argument("--presentation-title", default="Infografiche AAQD")
    ap.add_argument("--presentation-subtitle", default="Modellistica e valutazione della qualità dell’aria")
    ap.add_argument("--author", default="Giovanni Bonafè")
    ap.add_argument("--affiliation", default="ARPA FVG")
    ap.add_argument("--date", dest="presentation_date", default=date.today().strftime("%d/%m/%Y"))
    ap.add_argument("--reference", action="append", default=[], help="ripetibile")
    ap.add_argument("--licence", default="Infografiche: CC BY 4.0 · codice del prototipo: MIT")
    args = ap.parse_args()

    root = find_repo_root(args.root)
    output = Path(args.output).expanduser().resolve()
    generated = output.parent / "assets" / "generated"
    cover = generated / "title.svg"
    closing = generated / "references.svg"
    text_slide(cover, root, "title", args.presentation_title, args.presentation_subtitle,
               (args.author, args.affiliation, args.presentation_date),
               "Presentazione animata delle infografiche del progetto AAQD")
    references = args.reference or [
        "Direttiva (UE) 2024/2881 sulla qualità dell’aria ambiente",
        "Commissione europea, documento tecnico di supporto (aprile 2025)",
        f"Repository: https://github.com/{args.repo}",
    ]
    text_slide(closing, root, "closing", "Riferimenti", "Fonti principali e condizioni di riuso",
               (*references, args.licence), f"{args.author} · {args.affiliation}")

    slides = [{"id": "title", "title": args.presentation_title, "src": rel_src(cover, output),
               "enabled": True, "language": args.language,
               "frames": [{"id": "overview", "label": "Titolo"}]}]
    svg_files = sorted(p for p in root.rglob(f"*_{args.language}.svg") if active_svg(p, root))
    for svg_path in svg_files:
        relative = svg_path.relative_to(root).as_posix()
        detected = frame_ids(svg_path)
        if args.local_src:
            src = Path(svg_path).relative_to(output.parent).as_posix()
        else:
            src = f"https://raw.githubusercontent.com/{args.repo}/{args.branch}/{urllib.parse.quote(relative, safe='/')}"
        frames = [{"id": "overview", "label": "Panoramica"}]
        frames += [{"id": x, "label": human_label(x)} for x in detected]
        if detected and not args.no_summary:
            frames.append({"id": "overview", "label": "Riepilogo"})
        slides.append({"id": slide_id(relative), "title": title_from_path(relative), "src": src,
                       "enabled": True, "language": args.language, "frames": frames})
        print(f"{relative}: {', '.join(detected) if detected else 'nessun dettaglio'}")

    slides.append({"id": "references", "title": "Riferimenti e licenza", "src": rel_src(closing, output),
                   "enabled": True, "language": args.language,
                   "frames": [{"id": "overview", "label": "Riferimenti"}]})
    manifest = {"version": 2, "title": args.presentation_title,
                "defaults": {"duration": 1050, "padding": 0.08}, "slides": slides}
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Scritto {output}: {len(slides)} slide")


if __name__ == "__main__":
    main()
