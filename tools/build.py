"""Build every Atlas plate in both GitHub themes.

    python tools/build.py              # all plates
    python tools/build.py hero signal  # selected plates

Writes assets/plates/<slug>-dark.svg and assets/plates/<slug>-light.svg.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atlas.kit import THEMES  # noqa: E402
from atlas.plates import PLATES  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "assets" / "plates"


def main(selected: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    unknown = set(selected) - set(PLATES)
    if unknown:
        sys.exit(f"unknown plate(s): {', '.join(sorted(unknown))}; choose from {', '.join(PLATES)}")
    for slug, builder in PLATES.items():
        if selected and slug not in selected:
            continue
        for theme in THEMES:
            for plate in builder(theme):
                path = OUT / f"{plate.slug}-{theme.name}.svg"
                svg = plate.render()
                path.write_text(svg, encoding="utf-8")
                print(f"{path.relative_to(OUT.parent.parent)}  {len(svg.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
