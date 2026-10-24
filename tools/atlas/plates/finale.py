"""PL. 07 — Open Channel. The end card: the loop from the title plate returns,
fully converged, and the signal comes to rest."""
from __future__ import annotations

import math

from ..kit import Plate, Theme, anim, arc, crop_marks, dot_grid, grain, poly, polar

W, H = 1200, 540
CX, CY, R = 952, 250, 128


def build(t: Theme) -> Plate:
    p = Plate(
        "finale", W, H, t, "Open Channel — let’s build something that runs itself",
        "Closing plate. The reconciliation loop from the title returns, fully converged, as a steady signal comes "
        "to rest inside it. Text: Let's build something that runs itself. Open to conversations about cloud "
        "platforms, DevOps, SRE and AI-driven automation. LinkedIn, portfolio and GitHub links follow below.",
    )
    gid, clip = p.uid("glow"), p.uid("clip")
    p.defs_add(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="460">'
               f'<stop offset="0" stop-color="{t.panel_hi}"/><stop offset="1" stop-color="{t.panel}" stop-opacity="0"/>'
               f'</radialGradient><clipPath id="{clip}"><rect width="{W}" height="{H}" rx="20"/></clipPath>')
    p.add(f'<rect width="{W}" height="{H}" rx="20" fill="{t.panel}"/>',
          f'<rect width="{W}" height="{H}" rx="20" fill="url(#{gid})"/>')
    dot_grid(p, cx=CX, cy=CY, radius=560, opacity=.45, clip=clip)
    grain(p, 0.07 if t.name == "dark" else 0.05)
    if t.name == "light":
        p.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{t.rule}"/>')
    crop_marks(p)

    # masthead
    p.spans(60, 58, [("PL. 07", "monob", t.accent), ("   ", "mono", t.ink), ("OPEN CHANNEL", "dispm", t.ink)],
            size=15, ls=0.16)
    p.t_(1140, 58, "END OF ATLAS · VOL. 01", "mono", 13, t.ink3, anchor="end", ls=0.14)
    p.add(f'<path d="M60 78H1140" stroke="{t.rule}"/>')

    # converged loop
    d = []
    for i in range(96):
        a = i * 3.75
        ln = 12 if i % 24 == 0 else (7 if i % 4 == 0 else 3)
        x0, y0 = polar(CX, CY, R + 6, a)
        x1, y1 = polar(CX, CY, R + 6 + ln, a)
        d.append(f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}")
    p.add(f'<path d="{"".join(d)}" stroke="{t.ink3}" opacity=".55"/>',
          f'<circle cx="{CX}" cy="{CY}" r="{R}" stroke="{t.steady}" stroke-width="1.6" pathLength="1" '
          f'style="stroke-dasharray:1;{anim("draw", 2.2, .3, "cubic-bezier(.6,0,.2,1)")}"/>',
          f'<circle cx="{CX}" cy="{CY}" r="{R - 26}" stroke="{t.ink3}" stroke-dasharray="1 7" class="spinr" '
          f'style="transform-origin:{CX}px {CY}px;animation:spinr 70s linear infinite"/>')
    tail = "".join(f'<path d="{arc(CX, CY, R, -90 - 60 + k * 6, -90 - 54 + k * 6)}" stroke="{t.steady}" '
                   f'stroke-width="2.6" stroke-linecap="round" opacity="{(k + 1) / 11:.2f}"/>' for k in range(10))
    p.add(f'<g style="{anim("fade", .8, 2.2)}"><g class="spin" style="transform-origin:{CX}px {CY}px;'
          f'animation:spin 12s linear infinite">{tail}<circle cx="{CX}" cy="{CY - R}" r="5" fill="{t.steady}"/></g></g>')

    # the signal arrives, calm, and settles to a line at the centre
    pts = []
    for x in range(600, CX + 1, 3):
        u = (x - 600) / (CX - 600)
        pts.append((x, CY + 9 * (1 - u) ** 2 * math.sin((x - 600) / 26 * math.pi)))
    sig = poly(pts)
    p.add(f'<path d="{sig}" stroke="{t.steady}" stroke-width="1.8" stroke-linecap="round" pathLength="1" '
          f'style="stroke-dasharray:1;{anim("draw", 1.6, 1.0, "ease-out")}"/>',
          f'<path d="{sig}" stroke="{t.steady}" stroke-width="2.6" stroke-dasharray="2 10" stroke-linecap="round" '
          f'style="animation:flow 9s linear infinite,fade 1s 2.4s both"/>',
          f'<circle cx="{CX}" cy="{CY}" r="6" fill="{t.steady}" style="{anim("fade", .6, 2.4)}"/>',
          f'<circle cx="{CX}" cy="{CY}" r="16" stroke="{t.steady}" opacity=".5" style="{anim("fade", .6, 2.5)}"/>')
    p.t_(CX, CY + 46, "Δ = 0", "mono", 13, t.steady, anchor="middle", ls=0.1, style=anim("fade", .8, 2.6))
    p.t_(CX, CY - 40, "READY FOR THE NEXT LOOP", "mono", 10, t.ink3, anchor="middle", ls=0.22,
         style=anim("fade", .8, 2.7))

    # copy
    rise = lambda dl: anim("rise", 1.0, dl)  # noqa: E731
    p.t_(60, 186, "Let’s build something", "serifi", 68, t.ink, style=rise(.4))
    p.spans(60, 256, [("that ", "serifi", t.ink), ("runs itself.", "serifi", t.steady)], size=68, style=rise(.6))
    p.t_(62, 306, "OPEN TO CONVERSATIONS ABOUT CLOUD PLATFORMS, DEVOPS, SRE", "mono", 13, t.ink2, ls=0.12,
         style=anim("fade", 1, 1.0))
    p.t_(62, 328, "AND AI-DRIVEN AUTOMATION.", "mono", 13, t.ink2, ls=0.12, style=anim("fade", 1, 1.05))
    rows = [("linkedin", "/in/anup-narkhede-3291211ab"), ("portfolio", "anup-narkhede.github.io/Portfolio"),
            ("github", "@Anup-Narkhede")]
    for i, (k, v) in enumerate(rows):
        y = 392 + i * 30
        st = anim("fade", .8, 1.3 + i * .12)
        p.t_(62, y, "→", "mono", 15, t.accent, style=st)
        p.t_(88, y, k, "mono", 15, t.ink3, style=st)
        p.t_(200, y, v, "monob", 15, t.ink, style=st)
    p.add(f'<path d="M60 {H - 56}H1140" stroke="{t.rule}"/>')
    p.t_(60, H - 30, "fig. 07 — the loop closes. Thanks for reading the atlas.", "serifi", 17, t.ink3)
    p.t_(1140, H - 30, "PL. 07 / 07", "mono", 12, t.ink3, anchor="end", ls=0.16)
    return p
