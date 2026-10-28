# Infographics on Directive (EU) 2024/2881 (AAQD) and related implementing acts

This repository contains a series of **vector graphics (SVG)**, bilingual (IT/EN), generated from code using string-based source files.
They are intended for reusable slides, training material, technical working groups (SNPA, FAIRMODE), and, when needed, publications.

| # | Infographic | Status |
|---|---|---|
| 01 | Spatial representativeness of a sampling point | v0.1 – to be verified against the current legal text (see `01-rappresentativita-spaziale/sources.md`) |

## Repository structure

```
common/svgkit.py              palette, font, and shared SVG primitives used across the series
NN-name/build.py              generates SVG, PDF and PNG files; geometry and values are computed here
NN-name/strings/it.yaml      Italian text content (lists are already line-broken)
NN-name/strings/en.yaml      English text content
NN-name/out/                  output for each language and layout: *.svg, *.pdf, *.png
NN-name/sources.md           source references and verification status for each element
```

## Build instructions

```bash
pip install -r requirements.txt
cd 01-rappresentativita-spaziale
python build.py              # IT + EN, both layouts
python build.py en mobile    # example: English only, mobile layout only
```

Font: **Source Sans 3** (SIL OFL license). The SVG references it by name with a fallback to Helvetica/Arial. PDF and PNG output already embed it. The `≤` symbol uses DejaVu Sans as fallback.

## Two layouts from the same source

| Layout | Files | Canvas | Use |
|---|---|---|---|
| `wide` | `spatrep_it.*`, `spatrep_en.*` | 1920×1080 (16:9), PNG 3840×2160 | slides, large displays |
| `mobile` | `spatrep_it_mobile.*`, `spatrep_en_mobile.*` | 1200×1960 (portrait), PNG 2400×3920 | smartphones, messaging, journal pages |

The `mobile` layout follows a readability rule: **minimum text size 29 px on 1200 px, i.e. ≥ 2.4% of width**, so it remains legible even on a 390 px screen. In the `wide` layout, the minimum text size is ~1.1% of the width: acceptable on a full-screen presentation, not on a phone. For new infographics, it is better to design the `mobile` layout first.

## Conventions

- **One source per language**: no text is embedded directly into the code. The two language versions share the same geometry, so they cannot diverge. Decimal separator: comma in IT, dot in EN.
- **Exact values**: bar lengths are calculated from the underlying values (17–23 and 8–12 on a 0–30 scale), rather than drawn by hand.
- **Synthetic map data**: concentration fields and zone shapes are fictional and explicitly declared as such in the figure.
- **Editable SVG**: live text; groups with ids (`panel1`, `panel2`, `panel3`, `cells`, `road`, `zone`, `expert-patch`, `definition`, `background`). Remove the `background` element for a transparent slide background.
- **Accessibility**: `title` and `desc` elements in the SVG provide alt text; palette checked for color-vision deficiency (teal/ochre).
- **Style**: palette and dot pattern inspired by the logo of the R package *spatrep*.

## Adding a new infographic

Copy the `01-…` folder, update `strings/*.yaml`, and adjust the `panelN()` functions in `build.py`; reuse `common/svgkit.py`.
Populate `sources.md`: each statement in the figure must include a source (CELEX/ELI), date of consultation, and status.

## GitHub + Zenodo publication (DOI)

1. Create the repository on GitHub and upload this folder.
2. On <https://zenodo.org>, sign in with GitHub, go to *Account → GitHub* and **enable the repository before creating the release**.
3. Create a GitHub release with tag `v0.1.0`: Zenodo records the snapshot and assigns a **version DOI** and a **concept DOI** (the latter always points to the latest version and is the one to cite in general).
4. Add the DOI to `CITATION.cff` and the Zenodo badge to the README, then publish subsequent versions with new releases.
5. If the legal text changes, publish a new version and indicate the verification date in the source sheet: the version DOI allows precise citation of the exact text that was valid.

### Before the first release (open decisions)

- **License**: proposed CC BY 4.0 for figures and text, permissive code license (e.g. MIT) for the code; add the official `LICENSE` files.
  Verify ARPA FVG policy on dissemination. Zenodo copies the license into record metadata.
- **Licenses applied in this repository**: code under `LICENSE` (MIT); figures, text and graphic assets under `LICENSE-CC-BY-4.0` (CC BY 4.0).
- **Affiliation and logos**: if institutional names or logos appear (ARPA FVG, SNPA, FAIRMODE), obtain explicit authorization first.
- **Regulatory verification**: close the items marked as “to be verified” in `01-rappresentativita-spaziale/sources.md`.
