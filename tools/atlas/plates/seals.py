"""PL. 05 — Credentials. Engraved seals for the Credly-verified certifications."""
from __future__ import annotations

from ..kit import Plate, Theme, anim, polar, text_width

S = 300
C = S / 2

SEALS = [
    ("seal-saa", "SAA", "Solutions Architect", "ASSOCIATE", "AMAZON WEB SERVICES"),
    ("seal-dva", "DVA", "Developer", "ASSOCIATE", "AMAZON WEB SERVICES"),
    ("seal-clf", "CLF", "Cloud Practitioner", "FOUNDATIONAL", "AMAZON WEB SERVICES"),
    ("seal-az900", "AZ-900", "Azure Fundamentals", "FUNDAMENTALS", "MICROSOFT AZURE"),
]


def build_all(t: Theme) -> list[Plate]:
    return [_seal(t, i, *s) for i, s in enumerate(SEALS)]


def _seal(t: Theme, i: int, slug: str, code: str, name: str, level: str, vendor: str) -> Plate:
    p = Plate(slug, S, S, t, f"{vendor.title()} — {name} ({level.title()})",
              f"Engraved seal for the {vendor.title()} {name} certification, exam code {code}, verified on Credly.")
    ring = p.uid("ring")
    r_text = 116
    p.defs_add(f'<path id="{ring}" d="M{C} {C - r_text}A{r_text} {r_text} 0 1 1 {C - 0.01} {C - r_text}"/>')
    p.add(f'<circle cx="{C}" cy="{C}" r="140" stroke="{t.ink2}" stroke-width="1.2"/>',
          f'<circle cx="{C}" cy="{C}" r="134" stroke="{t.rule}"/>',
          f'<circle cx="{C}" cy="{C}" r="98" stroke="{t.ink2}"/>')
    # ticks between the inner rings
    d = []
    for k in range(72):
        x0, y0 = polar(C, C, 92, k * 5)
        x1, y1 = polar(C, C, 92 - (7 if k % 6 == 0 else 3), k * 5)
        d.append(f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}")
    p.add(f'<path d="{"".join(d)}" stroke="{t.accent}" opacity=".8"/>')

    # circular legend, slowly turning
    legend = f"{vendor}  ·  CERTIFIED  ·  {level}  ·  VERIFIED ON CREDLY  ·  "
    p.chars["mono"].update(legend)
    circ = 2 * 3.14159 * r_text
    p.add(f'<g class="spin" style="transform-origin:{C}px {C}px;animation:spin {60 + i * 8}s linear infinite">'
          f'<text class="f-mono" font-size="11" fill="{t.ink2}" letter-spacing="2">'
          f'<textPath href="#{ring}" textLength="{circ - 6:.0f}" lengthAdjust="spacing">{legend}</textPath></text></g>')

    # centre
    size = min(52, 150 / (text_width("disp", code, 1) or 1))
    p.t_(C, C + 6, code, "disp", round(size, 1), t.ink, anchor="middle", ls=-0.01, style=anim("rise", .8, .1 + i * .1))
    p.t_(C, C + 36, name, "serifi", 19, t.ink2, anchor="middle")
    p.t_(C, C - 38, level, "mono", 10, t.accent, anchor="middle", ls=0.3)
    p.add(f'<path d="M{C - 16} {C + 52}H{C + 16}" stroke="{t.rule}"/>')
    return p
