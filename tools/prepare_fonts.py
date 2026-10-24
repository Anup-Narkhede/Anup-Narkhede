"""One-time font preparation for the Atlas plates.

Downloads the variable / static source fonts from google/fonts (all SIL OFL 1.1),
pins variable axes to static instances, subsets them to the characters the plates
use, and writes compact WOFF2 files to tools/fonts/. Those files are committed so
`build.py` (and the GitHub Action) never need the network.

    python tools/prepare_fonts.py
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fonts"
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

SOURCES = {
    "archivo": GF + "archivo/Archivo%5Bwdth,wght%5D.ttf",
    "serif": GF + "instrumentserif/InstrumentSerif-Regular.ttf",
    "serif-italic": GF + "instrumentserif/InstrumentSerif-Italic.ttf",
    "mono": GF + "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}

# (output name, source, axis pins)
INSTANCES = [
    ("ArchivoExpanded-ExtraBold", "archivo", {"wdth": 125, "wght": 800}),
    ("ArchivoExpanded-Medium", "archivo", {"wdth": 125, "wght": 500}),
    ("InstrumentSerif-Regular", "serif", None),
    ("InstrumentSerif-Italic", "serif-italic", None),
    ("JetBrainsMono-Regular", "mono", {"wght": 400}),
    ("JetBrainsMono-SemiBold", "mono", {"wght": 600}),
]

# Printable ASCII plus the handful of typographic marks the plates use.
CHARS = "".join(chr(c) for c in range(0x20, 0x7F)) + "×→←↑↓↗↘·—–°’‘“”…•▸▲▼●○✓Δλ≈±"


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url) as r:  # noqa: S310 - pinned https source
        return r.read()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    raw = {k: fetch(u) for k, u in SOURCES.items()}
    for name, src, pins in INSTANCES:
        font = TTFont(io.BytesIO(raw[src]))
        if pins:
            font = instancer.instantiateVariableFont(font, pins, updateFontNames=False)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt", "tnum", "case"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        sub = subset.Subsetter(opts)
        sub.populate(text=CHARS)
        sub.subset(font)
        font.flavor = "woff2"
        path = OUT / f"{name}.woff2"
        font.save(path)
        print(f"{path.name:36} {path.stat().st_size / 1024:6.1f} KB")
    for family in ("archivo", "instrumentserif", "jetbrainsmono"):
        (OUT / f"OFL-{family}.txt").write_bytes(fetch(GF + f"{family}/OFL.txt"))


if __name__ == "__main__":
    main()
