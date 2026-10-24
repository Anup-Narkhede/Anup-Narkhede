# Atlas of Desired State — plate generator

Every image on the profile README is an SVG drawn by the Python in this folder.
Nothing is hand-edited in `assets/plates/`. Change the code, then rebuild.

```
tools/
├── build.py              # builds every plate in both themes → assets/plates/<slug>-{dark,light}.svg
├── fetch_activity.py     # pulls the contributions calendar → data/contributions.json
├── prepare_fonts.py      # one-time: instances + subsets the OFL fonts → fonts/*.woff2
├── requirements.txt      # fonttools + brotli (all CI needs)
├── requirements-dev.txt  # + uharfbuzz, for outlined display type (the hero name)
├── data/contributions.json
├── fonts/                # static WOFF2 subsets + their SIL OFL licences
└── atlas/
    ├── kit.py            # themes, font embedding, text, geometry, shared plate furniture
    └── plates/           # one module per plate
        ├── hero.py       # PL. 00  title card: noise → reconciliation loop → steady state
        ├── delivery.py   # PL. 01  CI/CD as a transit map
        ├── planes.py     # PL. 02  Kubernetes controller vs. agent-over-MCP loop
        ├── strata.py     # PL. 03  the stack as a geological cross-section
        ├── exhibits.py   # PL. 04  one card per featured repository
        ├── seals.py      # PL. 05  certification seals
        ├── signal.py     # PL. 06  contributions as a seismograph (auto-updated)
        └── finale.py     # PL. 07  end card
```

## Rebuild

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements-dev.txt
python tools/build.py              # everything
python tools/build.py exhibits     # or just some plates
```

Output is deterministic: the procedural elements (the hero's noise, the strata
folds) use fixed seeds, so a rebuild without code changes produces identical files.

## Common edits

| To change… | Edit |
|---|---|
| Featured projects, their copy and chips | `EXHIBITS` in `atlas/plates/exhibits.py`, plus the matching blockquote in `README.md` |
| Stack layers and notes | `LAYERS` in `atlas/plates/strata.py` |
| Pipeline stations | `STATIONS` in `atlas/plates/delivery.py` |
| Certifications | `SEALS` in `atlas/plates/seals.py`, plus the Credly links in `README.md` |
| Colours for both themes | `DARK` / `LIGHT` in `atlas/kit.py` |
| Tagline / name | `_type()` in `atlas/plates/hero.py` |

If you add a character the fonts don't cover yet (outside ASCII and the marks
listed in `prepare_fonts.py`), add it to `CHARS` and re-run `prepare_fonts.py`.

## The Signal plate (PL. 06)

`.github/workflows/signal.yml` runs every Monday (and on demand from the Actions
tab). It fetches the public contributions calendar with the workflow's own
`GITHUB_TOKEN`, redraws `signal-{dark,light}.svg`, and commits only when
something changed. No third-party stats service is involved. If the API call
fails, the job fails and the previous plate stays in place.

To refresh it locally:

```bash
GITHUB_TOKEN=$(gh auth token) python tools/fetch_activity.py
python tools/build.py signal
```

## How the plates are made to work on GitHub

- **Themes.** Each plate is built twice and swapped with `<picture>` +
  `prefers-color-scheme`. To make a plate clickable, wrap the whole
  `<picture>` in `<a>`. Never put the `<a>` inside `<picture>`, because the
  `<img>` must stay a direct child or the dark source is ignored. GitHub's
  `/markdown` API renders these differently from github.com itself, so verify
  on the live page.
- **Fonts.** Each SVG embeds only the glyphs it uses, as base64 WOFF2, so type
  renders identically everywhere (GitHub serves SVGs as isolated images, so
  web fonts can't be loaded any other way). The hero name is converted to
  outlines so it can be stroke-drawn.
- **Motion.** Plain CSS keyframes, plus SMIL `animateMotion` for things that
  travel along paths. No JavaScript, since GitHub would strip it anyway. Intros
  play once on load, and ambient loops are slow and low-contrast.
- **Fallbacks.** `prefers-reduced-motion: reduce` turns every animation off and
  hides the SMIL movers. The static state of each plate is its finished
  composition. Every image has descriptive `alt` text, and the facts on each
  plate are repeated as real text in the README.
- **Weight.** ~1 MB for all 28 files; the largest plate (strata) is ~115 KB.
