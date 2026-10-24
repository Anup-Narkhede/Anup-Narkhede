"""Masthead strips for the plates whose body is a set of separate images
(PL. 04 exhibits, PL. 05 seals), so every chapter opens the same way."""
from __future__ import annotations

from ..kit import Plate, Theme, header

SECTIONS = [
    ("section-exhibits", "04", "Exhibits", "four public repositories"),
    ("section-credentials", "05", "Credentials", "verified on credly"),
]


def build_all(t: Theme) -> list[Plate]:
    out = []
    for slug, num, title, meta in SECTIONS:
        p = Plate(slug, 1200, 84, t, f"Plate {num} — {title}", f"Section heading: plate {num}, {title}, {meta}.")
        header(p, num, title, meta)
        out.append(p)
    return out
