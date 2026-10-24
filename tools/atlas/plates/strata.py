"""PL. 03 — Stratigraphy of a Stack. The toolset as a geological cross-section:
oldest foundations at the bottom, the newest deposit on top, folded into an
anticline and cut by a fault; boreholes carry signal upward through every layer."""
from __future__ import annotations

import math

from ..kit import Plate, Theme, anim, header, rng, smooth

W, H = 1200, 730
SX0, SX1 = 96, 700          # section extents
TOP, BOTTOM = 150, 676
FAULT = ((452, BOTTOM), (488, TOP - 40))  # bottom → top
THROW = 18                  # vertical offset of the right-hand block

# youngest first: (number, name, tools, note, nominal thickness)
LAYERS = [
    ("07", "Intelligence", "Python · LLM agents · MCP", "the newest deposit; still settling.", 50),
    ("06", "Observability", "Prometheus · Grafana · CloudWatch", "you can’t reconcile what you can’t see.", 58),
    ("05", "Delivery", "Git · Jenkins · Argo CD", "the repository is the source of truth.", 64),
    ("04", "Containers", "Docker · Kubernetes · kind · EKS", "the unit of deployment.", 74),
    ("03", "Infrastructure as code", "Terraform · CloudFormation · Boto3", "infrastructure, reviewed like code.", 66),
    ("02", "Cloud", "AWS · Azure", "certified: AWS ×3, Azure ×1.", 78),
    ("01", "Bedrock", "Linux · Bash · Networking · C", "everything rests on this.", 160),
]


def _patterns(p: Plate, t: Theme) -> list[str]:
    c = t.ink3
    specs = [
        ("dots", 10, f'<circle cx="5" cy="5" r="1.3" fill="{t.steady}"/>'),
        ("wave", 22, f'<path d="M0 11q5.5-7 11 0t11 0" stroke="{c}" stroke-width="1.1"/>'),
        ("hatch", 11, f'<path d="M-2 13L13 -2M-2 2L2 -2M9 13L13 9" stroke="{c}" stroke-width="1.1"/>'),
        ("boxes", 18, f'<rect x="3.5" y="3.5" width="10" height="10" rx="1.5" stroke="{c}" stroke-width="1.1"/>'),
        ("cross", 12, f'<path d="M0 6H12M6 0V12" stroke="{c}" stroke-width="1"/>'),
        ("cells", 16, f'<circle cx="8" cy="8" r="4" stroke="{c}" stroke-width="1.1"/>'),
        ("rock", 26, f'<path d="M2 8l6-5 7 3 5 7-6 5-8-2zM15 20l5-3 5 4-3 5" stroke="{c}" stroke-width="1"/>'),
    ]
    ids = []
    for name, s, body in specs:
        pid = p.uid(name)
        p.defs_add(f'<pattern id="{pid}" width="{s}" height="{s}" patternUnits="userSpaceOnUse">{body}</pattern>')
        ids.append(pid)
    return ids


def _boundaries() -> list[list[tuple[float, float]]]:
    """Folded boundaries, surface first. Thickness pinches and swells along x."""
    r = rng("strata")
    xs = [SX0 - 30 + i * (SX1 - SX0 + 60) / 30 for i in range(31)]
    n = len(LAYERS)
    lines = []
    for i in range(n + 1):
        depth = i / n
        pts = []
        for x in xs:
            u = (x - SX0) / (SX1 - SX0)
            dome = 74 * math.exp(-((u - 0.34) / 0.26) ** 2) + 12 * math.sin(u * 5.2)
            acc = 0.0
            for k, (*_, th) in enumerate(LAYERS[:i]):
                acc += th * (1 + 0.24 * math.sin(2 * math.pi * u * (0.8 + 0.35 * k) + k * 1.7))
            y = TOP + 36 + acc - dome * (0.3 + 0.7 * depth)
            if i == n:
                y = BOTTOM + 120  # bedrock continues below the frame
            y += r.uniform(-7, 7) if i == 0 else r.uniform(-1.5, 1.5)
            pts.append((x, y))
        lines.append(pts)
    return lines


def _surface_y(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def _section(p: Plate, t: Theme, pats, lines, clip, layer_delay) -> str:
    out = [f'<g clip-path="url(#{clip})">']
    for i in range(len(LAYERS)):
        top, bot = lines[i], lines[i + 1]
        d = smooth(top) + "L" + smooth(list(reversed(bot)))[1:] + "Z"
        tint = t.steady if i == 0 else t.ink
        op = 0.12 if i == 0 else (0.02 + i * 0.012)
        out.append(f'<path d="{d}" fill="{tint}" fill-opacity="{op:.3f}" style="{layer_delay(i)}"/>'
                   f'<path d="{d}" fill="url(#{pats[i]})" opacity="{0.9 if i == 0 else 0.5}" style="{layer_delay(i)}"/>')
    for i, pts in enumerate(lines[1:], start=1):
        out.append(f'<path d="{smooth(pts)}" stroke="{t.ink2}" stroke-width="1.1" opacity=".75"/>')
    out.append(f'<path d="{smooth(lines[0])}" stroke="{t.ink}" stroke-width="1.8"/>')
    # boreholes, cased, with signal rising through every layer
    for bx, seed in ((250, 0), (590, 1)):
        out.append(f'<rect x="{bx - 4}" y="{TOP - 90}" width="8" height="{BOTTOM - TOP + 120}" fill="{t.page}"/>'
                   f'<path d="M{bx - 4} {TOP - 90}V{BOTTOM + 30}M{bx + 4} {TOP - 90}V{BOTTOM + 30}" stroke="{t.ink2}"/>')
        for k in range(6):
            dur = 7 + seed
            out.append(f'<circle cx="{bx}" cy="{BOTTOM}" r="2.3" fill="{t.steady}" opacity="0" '
                       f'style="animation:ascend {dur}s linear {k * dur / 6 + seed * .6:.2f}s infinite"/>')
    out.append("</g>")
    return "".join(out)


def build(t: Theme) -> Plate:
    p = Plate(
        "strata", W, H, t, "Stratigraphy of a Stack",
        "Geological cross-section of a technology stack, oldest at the bottom: bedrock (Linux, Bash, networking, C), "
        "cloud (AWS, Azure), infrastructure as code (Terraform, CloudFormation, Boto3), containers (Docker, "
        "Kubernetes, kind, EKS), delivery (Git, Jenkins, Argo CD), observability (Prometheus, Grafana, CloudWatch) "
        "and, newest on top, intelligence (Python, LLM agents, MCP). The layers are folded and offset by a fault; "
        "two boreholes carry rising particles upward through every layer.",
    )
    header(p, "03", "Stratigraphy of a Stack", "cross-section · youngest on top")
    p.style("@keyframes ascend{from{transform:translateY(0);opacity:0}10%{opacity:1}85%{opacity:1}"
            f"to{{transform:translateY(-{BOTTOM - TOP + 40}px);opacity:0}}}}")
    pats = _patterns(p, t)
    lines = _boundaries()

    sec = p.uid("sec")
    p.defs_add(f'<clipPath id="{sec}"><path d="{smooth(lines[0])}L{SX1 + 40} {BOTTOM}L{SX0 - 40} {BOTTOM}Z"/></clipPath>')
    (fx0, fy0), (fx1, fy1) = FAULT
    left, right = p.uid("blkL"), p.uid("blkR")
    p.defs_add(f'<clipPath id="{left}"><path d="M{SX0} 0H{fx1}L{fx0} {BOTTOM}H{SX0}Z"/></clipPath>'
               f'<clipPath id="{right}"><path d="M{fx1} 0H{SX1}V{BOTTOM}H{fx0}Z"/></clipPath>')

    delay = lambda i: anim("fade", 1.0, 0.2 + (6 - i) * 0.13)  # noqa: E731
    body = _section(p, t, pats, lines, sec, delay)
    p.add(f'<g clip-path="url(#{left})">{body}</g>',
          f'<g clip-path="url(#{right})"><g transform="translate(0 {THROW})">{body}</g></g>')

    # fault trace
    p.add(f'<path d="M{fx0} {BOTTOM}L{fx1} {fy1}" stroke="{t.accent}" stroke-width="1.6" stroke-dasharray="7 5" '
          f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 1.2, 1.6)}"/>',
          f'<path d="M{fx0 - 14} {BOTTOM - 80}l10 6M{fx0 - 4} {BOTTOM - 74}l-2 -10" stroke="{t.accent}"/>')
    p.t_(fx1 + 10, fy1 + 8, "F-1", "monob", 11, t.accent, ls=0.18)
    p.t_(fx1 + 10, fy1 + 24, "fault: the stack held", "serifi", 15, t.ink3)

    # frame
    p.add(f'<path d="M{SX0} {BOTTOM}H{SX1}" stroke="{t.ink2}"/>'
          f'<path d="M{SX0} 96V{BOTTOM}M{SX1} 96V{BOTTOM}" stroke="{t.rule}"/>')
    p.t_(SX0 + 12, 112, "▾ SURFACE · PRODUCTION", "mono", 11, t.ink3, ls=0.18)
    for bx, name, dy in ((250, "BH-1", 0), (590, "BH-2", THROW)):
        sy = _surface_y(lines[0], bx) + dy
        p.add(f'<path d="M{bx - 9} {sy:.1f}L{bx} {sy - 26:.1f}L{bx + 9} {sy:.1f}M{bx - 5} {sy - 11:.1f}H{bx + 5}" '
              f'stroke="{t.ink2}" stroke-linejoin="round"/>')
        p.t_(bx + 14, sy - 16, name, "mono", 10, t.ink3, ls=0.2)

    # time axis
    ax = 66
    ticks = "".join(f"M{ax} {y}h{12 if (y - TOP) % 50 == 0 else 5}" for y in range(TOP, BOTTOM + 1, 10))
    p.add(f'<path d="M{ax} {TOP}V{BOTTOM}" stroke="{t.ink3}"/><path d="{ticks}" stroke="{t.ink3}" opacity=".7"/>')
    p.t_(ax - 6, TOP + 4, "2026", "mono", 11, t.ink2, anchor="end")
    p.t_(ax - 6, BOTTOM + 4, "2021", "mono", 11, t.ink2, anchor="end")

    # callouts, evenly spaced on the right; leaders point at each layer's right edge
    lx = 776
    gap = (BOTTOM - TOP) / len(LAYERS)
    for i, (num, name, tools, note, _) in enumerate(LAYERS):
        top, bot = lines[i], lines[i + 1]
        edge = min(range(len(top)), key=lambda j: abs(top[j][0] - (SX1 - 6)))
        my = (top[edge][1] + min(bot[edge][1], BOTTOM - THROW)) / 2 + THROW
        by = TOP + gap * (i + 0.5)
        p.add(f'<g style="{anim("rise", 0.9, 1.0 + i * 0.12)}"><circle cx="{SX1}" cy="{my:.1f}" r="3" fill="{t.ink}"/>'
              f'<path d="M{SX1} {my:.1f}C{SX1 + 34} {my:.1f} {lx - 46} {by - 18:.1f} {lx - 12} {by - 18:.1f}" stroke="{t.ink3}"/>')
        p.spans(lx, by - 14, [(num + "  ", "monob", t.steady if i == 0 else t.accent), (name.upper(), "dispm", t.ink)],
                size=14, ls=0.14)
        p.t_(lx, by + 8, tools, "mono", 14, t.ink)
        p.t_(lx, by + 30, note, "serifi", 18, t.ink2)
        p.add("</g>")
    return p
