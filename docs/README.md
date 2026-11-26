# AAQD zoom presentation – prototype

Small open-source prototype for presenting the repository's SVG infographics as a conventional slide sequence with smooth camera zooms into individual panels.

## Demo

The prototype currently uses `04-model-quality-mqi-mqo/out/mqi_mqo_it.svg` from the `jobonaf/infographics-aaqd` repository. The SVG is fetched from GitHub at runtime, so an internet connection is required.

## Prepare presentation

```bash
 python generate_presentation.py --root /c/scratch/projects/infographics-aaqd --repo jobonaf/infographics-aaqd --branch main --language it --output presentation.json
```

## Run locally

Browsers generally block `fetch()` from `file://`; serve this directory over HTTP instead:

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>.

## Controls

- Arrow keys / Space: next frame
- Left arrow: previous frame
- Buttons below the canvas: jump directly to an overview or panel
- `F`: toggle fullscreen

## How it works

1. Fetches the original SVG without rasterising it.
2. Imports the SVG inline into the presentation viewport.
3. Finds groups with IDs `panel1`, `panel2`, etc. and measures their bounds with `getBBox()`.
4. Computes a 16:9 viewBox for each panel, retaining the complete panel in view.
5. Animates the SVG `viewBox` with cubic ease-in-out interpolation. This produces a continuous zoom/pan while keeping vector text and graphics sharp.

## Add another infographic

Add an entry to the `slides` array in `app.js`, with its SVG URL and the IDs of its panel groups. The panel labels are presentation labels and can be edited independently of the source SVG.

Example:

```js
{
  title: 'Spatial representativeness',
  src: 'https://raw.githubusercontent.com/jobonaf/infographics-aaqd/main/05-spatial-representativeness/out/spatial_representativeness_it.svg',
  frames: [
    { id: 'overview', label: 'Panoramica' },
    { id: 'panel1', label: '1 · ...' },
    { id: 'panel2', label: '2 · ...' },
  ],
}
```

Check the actual SVG output filename before adding a slide. A panel must be a named SVG group with a stable ID. The current MQI/MQO infographic already has `panel1`–`panel4`.

## Current limitations

- This is a browser-based prototype, not yet a full video exporter.
- It currently demonstrates one infographic (Italian MQI/MQO).
- Each zoom fits the complete panel into the 16:9 viewport. For tall panels this necessarily leaves some horizontal breathing room; a later iteration could support nested sub-panels or custom crop rectangles.
- SVGs are loaded from the public GitHub raw-content endpoint; for offline use, download the SVG and change `src` to a local relative path.

## Licence

The prototype code is released under the repository's MIT licence. The infographic remains subject to the repository's CC BY 4.0 licence.
