#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[1]
DIR_PATTERN = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = (
    "build.py",
    "strings/it.yaml",
    "strings/en.yaml",
    "sources.md",
)
OPEN_MARKERS = {
    "◐": "PARTIAL",
    "✖": "UNVERIFIED",
}

errors = []
warnings = []


def fail(message):
    errors.append(message)
    print(f"ERROR: {message}")


def warn(message):
    warnings.append(message)
    print(f"WARNING: {message}")


def infographic_dirs():
    return sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def validate_structure(path):
    if not DIR_PATTERN.fullmatch(path.name):
        fail(f"{path.name}: nome della cartella non conforme")

    for relative in REQUIRED:
        if not (path / relative).is_file():
            fail(f"{path.name}: manca {relative}")

    out = path / "out"
    if not out.is_dir():
        fail(f"{path.name}: manca la cartella out/")


def validate_yaml(path):
    documents = {}

    for lang in ("it", "en"):
        yaml_path = path / "strings" / f"{lang}.yaml"

        if not yaml_path.is_file():
            continue

        try:
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"{yaml_path.relative_to(ROOT)}: YAML non valido: {exc}")
            continue

        if not isinstance(data, dict):
            fail(f"{yaml_path.relative_to(ROOT)}: radice YAML non mapping")
            continue

        documents[lang] = data

    if set(documents) == {"it", "en"}:
        italian_keys = set(documents["it"])
        english_keys = set(documents["en"])

        if italian_keys != english_keys:
            missing_en = sorted(italian_keys - english_keys)
            missing_it = sorted(english_keys - italian_keys)

            if missing_en:
                fail(f"{path.name}: chiavi mancanti in en.yaml: {missing_en}")
            if missing_it:
                fail(f"{path.name}: chiavi mancanti in it.yaml: {missing_it}")


def validate_sources(path):
    sources = path / "sources.md"

    if not sources.is_file():
        return

    text = sources.read_text(encoding="utf-8")

    for marker, label in OPEN_MARKERS.items():
        count = text.count(marker)
        if count:
            warn(
                f"{path.name}/sources.md: "
                f"{count} markers {label} still open"
            )


def run_build(path):
    result = subprocess.run(
        [sys.executable, "build.py"],
        cwd=path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    print(result.stdout, end="")

    if result.returncode:
        fail(f"{path.name}: build terminata con codice {result.returncode}")

    if "ATTENZIONE:" in result.stdout or "WARNING:" in result.stdout:
        warn(f"{path.name}: la build ha prodotto avvisi di impaginazione")


def validate_svg(path):
    svg_files = sorted((path / "out").glob("*.svg"))

    if not svg_files:
        fail(f"{path.name}: nessun SVG generato")
        return

    for svg in svg_files:
        if svg.stat().st_size == 0:
            fail(f"{svg.relative_to(ROOT)}: file vuoto")
            continue

        try:
            ET.parse(svg)
        except ET.ParseError as exc:
            fail(f"{svg.relative_to(ROOT)}: XML/SVG non valido: {exc}")


def main():
    directories = infographic_dirs()

    if not directories:
        fail("nessuna cartella NN-english-name trovata")

    expected_numbers = set(range(1, 18))

    for path in directories:
        number = int(path.name[:2])
        if number not in expected_numbers:
            fail(f"{path.name}: numero esterno all'intervallo 01-17")

        print(f"\n==> {path.name}")
        validate_structure(path)
        validate_yaml(path)
        validate_sources(path)
        run_build(path)
        validate_svg(path)

    print(
        f"\nRisultato: {len(errors)} errori, "
        f"{len(warnings)} avvisi."
    )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
