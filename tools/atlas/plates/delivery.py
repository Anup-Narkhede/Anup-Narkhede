"""PL. 01 — The Delivery Line. The CI/CD path drawn as a transit map: a delivery
line, an infrastructure-as-code branch that interchanges at RUN, and a feedback
loop that carries what production learns back to the next commit."""
from __future__ import annotations

import math

from ..kit import Plate, Theme, anim, header

W, H = 1200, 500
Y_MAIN, Y_IAC, Y_LOOP = 262, 158, 404
X0, X1 = 132, 1068
STEP = (X1 - X0) / 6
LOOP_R = 26
TRIP = 15.0  # seconds for one full lap

STATIONS = [
    ("01", "COMMIT", ["git · GitHub"]),
    ("02", "BUILD", ["Jenkins"]),
    ("03", "PACKAGE", ["Docker"]),
    ("04", "REGISTRY", ["Amazon ECR"]),
    ("05", "SYNC", ["Argo CD", "GitOps"]),
    ("06", "RUN", ["Kubernetes", "Amazon EKS"]),
    ("07", "OBSERVE", ["Prometheus", "Grafana"]),
]


def _lap() -> tuple[str, float]:
    r = LOOP_R
    xl, xr, yb = X0 - 58, X1 + 58, Y_LOOP
    d = (f"M{X0} {Y_MAIN}H{xr - r}A{r} {r} 0 0 1 {xr} {Y_MAIN + r}V{yb - r}"
         f"A{r} {r} 0 0 1 {xr - r} {yb}H{xl + r}A{r} {r} 0 0 1 {xl} {yb - r}V{Y_MAIN + r}"
         f"A{r} {r} 0 0 1 {xl + r} {Y_MAIN}H{X0}")
    straight = (xr - r - X0) + (yb - Y_MAIN - 2 * r) * 2 + (xr - xl - 2 * r) + (X0 - xl - r)
    return d, straight + 4 * (math.pi * r / 2)


def build(t: Theme) -> Plate:
    p = Plate(
        "delivery", W, H, t, "The Delivery Line",
        "Transit-map diagram of a delivery pipeline. Line 1 runs commit (git, GitHub), build (Jenkins), "
        "package (Docker), registry (Amazon ECR), sync (Argo CD, GitOps), run (Kubernetes, Amazon EKS) and "
        "observe (Prometheus, Grafana). Line 2, infrastructure as code (Terraform plan and apply), joins at run. "
        "A feedback loop returns metrics and alerts to the next commit. An animated train travels the loop.",
    )
    header(p, "01", "The Delivery Line", "schematic · not to scale")
    lap, lap_len = _lap()

    # feedback loop (dashed), drawn under everything
    p.add(f'<path d="{lap}" stroke="{t.ink3}" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round" '
          f'style="animation:flow 18s linear infinite"/>')
    lbl = "LOOP ◂ METRICS · ALERTS · POSTMORTEMS → THE NEXT COMMIT"
    p.add(f'<rect x="{W / 2 - 250}" y="{Y_LOOP - 12}" width="500" height="24" fill="{t.page}"/>')
    p.t_(W / 2, Y_LOOP + 4.5, lbl, "mono", 12, t.ink3, anchor="middle", ls=0.12)

    # line 2: infrastructure as code
    xs = [X0 + i * STEP for i in range(7)]
    x_run = xs[5]
    dx = Y_MAIN - Y_IAC
    iac_start = xs[3] - 30
    iac = f"M{iac_start} {Y_IAC}H{x_run - dx}L{x_run} {Y_MAIN}"
    p.add(f'<path d="{iac}" stroke="{t.steady}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" '
          f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 1.4, 0.9)}"/>')
    for x, num, name, tool in ((xs[3] + 20, "2A", "PLAN", "terraform plan"),
                               (xs[4] - 10, "2B", "APPLY", "terraform apply")):
        p.add(f'<circle cx="{x}" cy="{Y_IAC}" r="9" fill="{t.page}" stroke="{t.steady}" stroke-width="3.5" '
              f'style="{anim("fade", .6, 1.6)}"/>')
        p.spans(x, Y_IAC - 44, [(num + "  ", "mono", t.steady), (name, "dispm", t.ink)], size=16, ls=0.14,
                anchor="middle", style=anim("fade", .8, 1.7))
        p.t_(x, Y_IAC - 23, tool, "mono", 13, t.ink2, anchor="middle", style=anim("fade", .8, 1.8))
    p.t_(iac_start - 16, Y_IAC + 5, "LINE 2", "monob", 11, t.steady, anchor="end", ls=0.2,
         style=anim("fade", .8, 1.6))

    # line 1: delivery
    p.add(f'<path d="M{X0} {Y_MAIN}H{X1}" stroke="{t.ink}" stroke-width="6" stroke-linecap="round" '
          f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 1.6, 0.3, "cubic-bezier(.6,0,.2,1)")}"/>')
    p.t_(X0 - 22, Y_MAIN - 14, "LINE 1", "monob", 10, t.ink, anchor="end", ls=0.2, style=anim("fade", .8, .4))

    p.style("@keyframes halo{0%{opacity:.9;transform:scale(1)}10%,100%{opacity:0;transform:scale(2.6)}}")
    for i, (num, name, tools) in enumerate(STATIONS):
        x = xs[i]
        phase = (x - X0) / lap_len * TRIP
        inter = name == "RUN"
        r = 13 if inter else 10
        p.add(f'<circle cx="{x}" cy="{Y_MAIN}" r="{r}" stroke="{t.accent}" stroke-width="2" opacity="0" '
              f'style="transform-origin:{x}px {Y_MAIN}px;transform-box:view-box;'
              f'animation:halo {TRIP}s ease-out {phase:.2f}s infinite"/>',
              f'<circle cx="{x}" cy="{Y_MAIN}" r="{r}" fill="{t.page}" stroke="{t.ink}" stroke-width="4" '
              f'style="{anim("fade", .5, .4 + i * .12)}"/>')
        if inter:
            p.add(f'<circle cx="{x}" cy="{Y_MAIN}" r="5" fill="{t.steady}" style="{anim("fade", .5, 1.8)}"/>')
        st = anim("fade", .8, .6 + i * .12)
        if inter:
            p.t_(x + 20, Y_MAIN - 16, num, "mono", 11, t.accent, ls=0.1, style=st)
        else:
            p.t_(x, Y_MAIN - 22, num, "mono", 11, t.accent, anchor="middle", ls=0.1, style=st)
        p.t_(x, Y_MAIN + 42, name, "dispm", 16, t.ink, anchor="middle", ls=0.12, style=st)
        for j, tool in enumerate(tools):
            p.t_(x, Y_MAIN + 66 + j * 19, tool, "mono", 13, t.ink2, anchor="middle", style=st)
    p.t_(x_run + 42, Y_MAIN - 16, "INTERCHANGE", "mono", 10, t.ink3, ls=0.2, style=anim("fade", .8, 2))

    # the train: one change, riding the whole loop
    blur = p.uid("blur")
    p.defs_add(f'<filter id="{blur}" x="-100%" y="-200%" width="300%" height="500%">'
               f'<feGaussianBlur stdDeviation="4"/></filter>')
    p.add(f'<g class="smil" style="{anim("fade", .6, 1.2)}"><g>'
          f'<rect x="-20" y="-7" width="40" height="14" rx="7" fill="{t.accent}" filter="url(#{blur})" opacity=".7"/>'
          f'<rect x="-17" y="-6" width="34" height="12" rx="6" fill="{t.accent}"/>'
          f'<circle cx="9" cy="0" r="2.2" fill="{t.page}"/>'
          f'<animateMotion dur="{TRIP}s" repeatCount="indefinite" rotate="auto" path="{lap}"/></g></g>')

    # legend + caption
    ly = H - 30
    p.add(f'<path d="M60 {ly - 4}h34" stroke="{t.ink}" stroke-width="5" stroke-linecap="round"/>'
          f'<path d="M290 {ly - 4}h34" stroke="{t.steady}" stroke-width="5" stroke-linecap="round"/>'
          f'<path d="M660 {ly - 4}h34" stroke="{t.ink3}" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>')
    p.t_(104, ly, "LINE 1 · DELIVERY", "mono", 12, t.ink2, ls=0.12)
    p.t_(334, ly, "LINE 2 · INFRASTRUCTURE AS CODE", "mono", 12, t.ink2, ls=0.12)
    p.t_(704, ly, "LOOP · FEEDBACK", "mono", 12, t.ink2, ls=0.12)
    p.t_(1140, ly + 1, "Nothing reaches production by hand.", "serifi", 21, t.ink2, anchor="end")
    return p
