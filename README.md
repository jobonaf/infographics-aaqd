# Air quality modelling infographics for the AAQD

[![Validate infographics](https://github.com/jobonaf/infographics-aaqd/actions/workflows/validate.yml/badge.svg)](https://github.com/jobonaf/infographics-aaqd/actions/workflows/validate.yml)

Bilingual Italian/English infographics on air quality modelling under Directive (EU) 2024/2881 (AAQD) and related technical guidance.

The project is organised as a set of 17 code-generated slides for presentations, training, technical working groups and publications. SVG is the primary editable format; PNG and PDF are optional exports.

## Project plan and status

| # | Chapter | Infographic | Repository status |
|---:|---|---|---|
| 01 | Framework and quality | Role of modelling in the AAQD | Planned |
| 02 | Framework and quality | Anatomy of a modelling system | Planned |
| 03 | Framework and quality | Fitness-for-purpose | Developed, review pending |
| 04 | Framework and quality | MQI and MQO | Developed, scientific review pending |
| 05 | Monitoring network | Spatial representativeness | Developed in wide and mobile layouts, legal review pending |
| 06 | Monitoring network | Monitoring network design | Planned |
| 07 | Assessment | Assessment modelling, natural sources, sanding and salting | Planned |
| 08 | Assessment | Exceedance situation indicators (ESI) | Developed, review pending |
| 09 | Assessment | Population exposure and health impact assessment | Planned |
| 10 | Source apportionment | Definitions and methods | Planned |
| 11 | Source apportionment | The six source-apportionment steps | Planned |
| 12 | Source apportionment | Transboundary pollution and EU products | Planned |
| 13 | Plans and roadmaps | From assessment to air quality plans | Planned |
| 14 | Plans and roadmaps | The seven emission scenarios | Developed, review pending |
| 15 | Plans and roadmaps | Projections: background, meteorology and bias correction | Planned |
| 16 | Forecasting | Forecasting systems | Planned |
| 17 | Forecasting | Forecasts as triggers for short-term action plans | Planned |

The directory number follows the final sequence of the 17-slide project, not the order in which the infographics were developed.

## Repository structure

```text
common/
└── svgkit.py                   shared palette, fonts and SVG primitives

NN-english-name/
├── build.py                    geometry, calculated values and build logic
├── strings/
│   ├── it.yaml                 Italian text
│   └── en.yaml                 English text
├── sources.md                  sources and verification status
└── out/                        generated SVG, PNG and PDF files

requirements.txt
CITATION.cff
LICENSE                         MIT license for code
LICENSE-CC-BY-4.0               CC BY 4.0 for figures, text and graphic assets
```

Currently developed directories:

```text
03-fitness-for-purpose/
04-model-quality-mqi-mqo/
05-spatial-representativeness/
08-exceedance-situation-indicators/
14-emission-scenarios/
```

## Requirements

- Python 3
- `numpy`
- `PyYAML`
- `CairoSVG`, optional but required for PNG and PDF export
- Source Sans 3, recommended

Install the Python dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Without CairoSVG, each build still generates the SVG files and reports:

```text
cairosvg non installato: generato solo l'SVG
```

The SVG files reference Source Sans 3 by name, with Source Sans Pro, Helvetica Neue, Arial and sans-serif fallbacks. DejaVu Sans is used as a fallback for mathematical symbols.

## Building the infographics

Build all currently developed infographics from the repository root:

```bash
for dir in [0-9][0-9]-*; do
  [ -f "$dir/build.py" ] || continue
  echo "==> $dir"
  (cd "$dir" && python build.py)
done
```

Build one infographic:

```bash
cd 05-spatial-representativeness
python build.py
```

The spatial-representativeness build also accepts language and layout arguments:

```bash
python build.py en mobile
```

Other currently developed infographics generate the wide layout. Their build scripts accept `it` or `en` where implemented.

## Layouts

| Layout | Canvas | Typical use | Current availability |
|---|---:|---|---|
| `wide` | 1920 x 1080, 16:9 | Slides and large displays | All developed infographics |
| `mobile` | 1200 x 1960, portrait | Smartphones, messaging and narrow pages | Spatial representativeness |

The mobile layout uses a minimum text size of 29 px on a 1200 px canvas, approximately 2.4% of the width. New infographics should preserve comparable readability; a mobile-first design is recommended when both layouts are planned.

## Authoring conventions

- **One text source per language:** translatable text is stored in `strings/it.yaml` and `strings/en.yaml`.
- **Shared geometry:** Italian and English versions use the same drawing code.
- **Calculated graphics:** dimensions and plotted values are derived from values in code rather than adjusted manually.
- **Synthetic data:** invented concentration fields, station data and illustrative values are explicitly identified in the figure and source sheet.
- **Editable SVG:** text remains live and meaningful graphical groups use IDs where practical.
- **Accessibility:** each SVG contains a title and description; the teal/ochre palette is designed to remain distinguishable under common colour-vision deficiencies.
- **Documented evidence:** each infographic has a `sources.md` file recording references and verification status.

## Adding a new infographic

1. Create the directory using its project number and an English slug:

   ```text
   NN-english-name/
   ```

2. Add `build.py`, `strings/it.yaml`, `strings/en.yaml`, `sources.md` and `out/`.
3. Reuse the shared elements in `common/svgkit.py`.
4. Keep one principal message per panel and move detailed qualifications to `sources.md` or accompanying notes.
5. Record each technical or regulatory statement in `sources.md`, including its source, consultation date and verification status.
6. Build both languages and inspect the resulting SVG files before committing.

Do not copy an existing infographic without also changing its title, alternative description, output stem and source sheet.

## Verification status

The infographics are explanatory material and do not replace the applicable legal texts.

The source sheets use the following status markers:

- `✔` verified in the cited text;
- `◐` derived from a secondary source or draft and requiring confirmation;
- `✖` not yet verified.

Items marked `◐` or `✖` must be resolved before the first public release. Scientific review is also required where a visual simplification could alter the interpretation, including the MQI/MQO target plot and nonlinear zero-emission scenarios.

## Packaging

Create a clean ZIP from the current committed revision, excluding `.git/` and untracked files:

```bash
git archive --format=zip   --prefix=infographics-aaqd/   -o latest.zip HEAD
```

Inspect the archive before distribution:

```bash
unzip -l latest.zip
```

## Publication and citation

The intended publication workflow is GitHub plus Zenodo:

1. enable the GitHub repository in Zenodo before creating the first release;
2. create a versioned GitHub release;
3. let Zenodo archive the release and assign a version DOI and concept DOI;
4. add the concept DOI and release metadata to `CITATION.cff` and this README.

When legal or technical references change, publish a new version and record the review date in the relevant source sheets.

## Licences

- Source code: [MIT License](LICENSE)
- Figures, text and graphic assets: [Creative Commons Attribution 4.0](LICENSE-CC-BY-4.0)

Use of institutional names or logos, including ARPA FVG, SNPA or FAIRMODE, may require separate authorisation and is not granted by these licences.
