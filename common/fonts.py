from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_DIR = ROOT / "assets" / "fonts"

SOURCE_SANS_REGULAR = FONT_DIR / "SourceSans3-Regular.ttf"
SOURCE_SANS_SEMIBOLD = FONT_DIR / "SourceSans3-SemiBold.ttf"
SOURCE_SANS_BOLD = FONT_DIR / "SourceSans3-Bold.ttf"


def check_fonts():
    missing = [
        p for p in (
            SOURCE_SANS_REGULAR,
            SOURCE_SANS_SEMIBOLD,
            SOURCE_SANS_BOLD,
        )
        if not p.exists()
    ]
    if missing:
        raise RuntimeError(
            "Missing fonts:\n" + "\n".join(map(str, missing))
        )