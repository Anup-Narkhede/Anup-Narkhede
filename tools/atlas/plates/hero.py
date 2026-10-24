"""PL. 00 — Title card. A noisy signal (toil) enters a reconciliation loop
(observe → diff → act) and leaves as a steady line; the name is drawn like a plot."""
from __future__ import annotations

import math

from ..kit import Plate, Theme, anim, arc, crop_marks, dot_grid, grain, outline, polar, poly, rng

W, H = 1200, 750
CX, CY, R = 790, 318, 176
ORBIT = 9.0  # seconds per revolution
NODES = [(-90, "01", "OBSERVE"), (30, "02", "DIFF"), (150, "03", "ACT")]


def build(t: Theme) -> Plate:
    p = Plate(
        "hero", W, H, t,
        "Anup Narkhede — Cloud DevOps Engineer",
        "Animated title plate. A noisy signal labelled toil, drift and 3 a.m. pages travels into a "
        "reconciliation loop with three stations — observe, diff, act — and leaves as a calm, steady "
        "line. Tagline: Declare it once. Let the loop do the rest.",
    )
    gid = p.uid("glow")
    p.defs_add(
        f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="560">'
        f'<stop offset="0" stop-color="{t.panel_hi}"/><stop offset="1" stop-color="{t.panel}" stop-opacity="0"/>'
        f"</radialGradient>"
    )
    clip = p.uid("clip")
    p.defs_add(f'<clipPath id="{clip}"><rect width="{W}" height="{H}" rx="20"/></clipPath>')
    p.add(f'<rect width="{W}" height="{H}" rx="20" fill="{t.panel}"/>',
          f'<rect width="{W}" height="{H}" rx="20" fill="url(#{gid})"/>')
    dot_grid(p, cx=CX, cy=CY, radius=640, opacity=0.5, clip=clip)
    grain(p, 0.07 if t.name == "dark" else 0.05)
    if t.name == "light":
        p.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{t.rule}"/>')
    crop_marks(p)

    p.style(
        "@keyframes gdraw{0%{stroke-dashoffset:1;fill-opacity:0}55%{stroke-dashoffset:0;fill-opacity:0}"
        "100%{stroke-dashoffset:0;fill-opacity:1}}"
        "@keyframes pulse{0%{opacity:.95;transform:scale(1)}16%,100%{opacity:0;transform:scale(3.4)}}"
        f"@keyframes lit{{0%{{fill:{t.steady}}}22%,100%{{fill:{t.accent}}}}}"
        "@keyframes sweep{0%{opacity:1;transform:translateX(0)}88%{opacity:1;transform:translateX(1080px)}"
        "100%{opacity:0;transform:translateX(1080px)}}"
    )

    _masthead(p, t)
    _loop(p, t)
    _signal(p, t)
    _type(p, t)
    return p


def _masthead(p: Plate, t: Theme) -> None:
    p.spans(60, 58, [("ANUP NARKHEDE", "monob", t.ink), ("  —  ATLAS OF DESIRED STATE", "mono", t.ink2)],
            size=14, ls=0.14, style=anim("fade", 1.2, 0.1))
    p.t_(1140, 58, "VOL. 01 · REV. 2026.10", "mono", 13, t.ink3, anchor="end", ls=0.14,
         style=anim("fade", 1.2, 0.2))
    ticks = "".join(f"M{x} 78v{8 if i % 10 == 0 else 3}" for i, x in enumerate(range(60, 1141, 12)))
    p.add(f'<g style="{anim("fade", 1.4, 0.1)}"><path d="M60 78H1140" stroke="{t.rule}"/>'
          f'<path d="{ticks}" stroke="{t.ink3}" opacity=".5"/></g>')
    for i, line in enumerate(["observe → diff → act.", "repeat until reality", "matches intent."]):
        p.t_(60, 132 + i * 21, line, "mono", 13, t.ink3, ls=0.04, style=anim("fade", 1.0, 1.4 + i * 0.12))


def _loop(p: Plate, t: Theme) -> None:
    # dial ticks, outside the ring
    d = []
    for i in range(120):
        a = i * 3 - 90
        ln = 16 if i % 30 == 0 else (10 if i % 5 == 0 else 5)
        x0, y0 = polar(CX, CY, R + 6, a)
        x1, y1 = polar(CX, CY, R + 6 + ln, a)
        d.append(f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}")
    p.add(f'<g style="{anim("fade", 1.6, 0.2)}">'
          f'<path d="{"".join(d)}" stroke="{t.ink3}" stroke-width="1" opacity=".6"/>')
    for deg, lab in ((0, "000"), (180, "180")):
        x, y = polar(CX, CY, R + 38, deg - 90)
        p.t_(x, y + 4, lab, "mono", 11, t.ink3, anchor="middle", ls=0.1)
    p.add("</g>")

    # rings
    p.add(f'<circle cx="{CX}" cy="{CY}" r="{R}" stroke="{t.ink2}" stroke-width="1.2" pathLength="1" '
          f'style="stroke-dasharray:1;{anim("draw", 1.8, 0.2, "cubic-bezier(.6,0,.2,1)")}"/>',
          f'<circle class="spinr" cx="{CX}" cy="{CY}" r="{R - 30}" stroke="{t.ink3}" stroke-dasharray="1 7" '
          f'style="transform-origin:{CX}px {CY}px;animation:spinr 60s linear infinite"/>',
          f'<circle cx="{CX}" cy="{CY}" r="{R - 64}" stroke="{t.rule}" style="{anim("fade", 1.4, 0.6)}"/>',
          f'<g stroke="{t.rule}" style="{anim("fade", 1.4, 0.8)}"><circle cx="{CX}" cy="{CY}" r="24"/>'
          f'<path d="M{CX - 48} {CY - 48}L{CX + 48} {CY + 48}M{CX + 48} {CY - 48}L{CX - 48} {CY + 48}" '
          f'opacity=".6"/></g>')
    p.t_(CX, CY - 50, "RECONCILE", "mono", 11, t.ink3, anchor="middle", ls=0.3, style=anim("fade", 1, 1.2))
    p.add(f'<g style="{anim("fade", 1, 2.2)}">'
          f'<circle cx="{CX - 64}" cy="{CY + 58}" r="3" fill="{t.steady}" '
          f'style="animation:blink 1.6s steps(1) infinite"/>')
    p.t_(CX - 54, CY + 62, "STATE: CONVERGED", "mono", 11, t.steady, ls=0.16)
    p.add("</g>")

    # angular velocity annotation
    ax, ay = polar(CX, CY, R + 24, -38)
    bx, by = polar(CX, CY, R + 62, -38)
    p.add(f'<path d="M{ax:.1f} {ay:.1f}L{bx:.1f} {by:.1f}H{bx + 70:.1f}" stroke="{t.ink3}" '
          f'style="{anim("fade", 1, 1.8)}"/>')
    p.t_(bx + 6, by - 7, f"ω = {360 / ORBIT:.0f}°/s", "mono", 12, t.ink3, style=anim("fade", 1, 1.9))

    # orbiting probe with comet tail (rotates as a group from 12 o'clock)
    tail = []
    for k in range(10):
        a0 = -90 - 64 + k * 6.4
        tail.append(f'<path d="{arc(CX, CY, R, a0, a0 + 6.6)}" stroke="{t.steady}" stroke-width="2.6" '
                    f'stroke-linecap="round" opacity="{(k + 1) / 11:.2f}"/>')
    blur = p.uid("blur")
    p.defs_add(f'<filter id="{blur}" x="-200%" y="-200%" width="500%" height="500%">'
               f'<feGaussianBlur stdDeviation="5"/></filter>')
    p.add(f'<g style="{anim("fade", 0.8, 1.6)}"><g class="spin" style="transform-origin:{CX}px {CY}px;'
          f'animation:spin {ORBIT}s linear infinite">{"".join(tail)}'
          f'<circle cx="{CX}" cy="{CY - R}" r="9" fill="{t.steady}" filter="url(#{blur})" opacity=".8"/>'
          f'<circle cx="{CX}" cy="{CY - R}" r="5" fill="{t.steady}"/></g></g>')

    # stations; each flashes as the probe passes
    for deg, num, name in NODES:
        x, y = polar(CX, CY, R, deg)
        phase = ((deg + 90) % 360) / 360 * ORBIT
        p.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" stroke="{t.steady}" stroke-width="1.5" opacity="0" '
              f'style="transform-origin:{x:.1f}px {y:.1f}px;transform-box:view-box;'
              f'animation:pulse {ORBIT}s ease-out {phase:.2f}s infinite"/>',
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{t.panel}" stroke="{t.ink}" stroke-width="1.5" '
              f'style="{anim("fade", 0.6, 1.2)}"/>',
              f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{t.accent}" '
              f'style="animation:fade .6s 1.2s both,lit {ORBIT}s linear {phase:.2f}s infinite"/>')
        lx, ly = polar(CX, CY, R + 46, deg)
        anchor = "middle" if deg == -90 else ("start" if deg < 90 else "end")
        if deg == -90:
            ly -= 6
        else:
            ly += 18
        p.spans(lx, ly, [(num + "  ", "mono", t.accent), (name, "dispm", t.ink)], size=13, ls=0.18,
                anchor=anchor, style=anim("fade", 0.8, 1.3))


def _signal(p: Plate, t: Theme) -> None:
    r = rng("toil")
    x_in, x_out = CX - R, CX + R
    pts, x = [], 60.0
    while x < x_in:
        taper = min(1.0, (x_in - x) / 48)
        a = 34 * taper
        y = CY + a * (0.55 * math.sin(x / 23) + r.uniform(-0.85, 0.85))
        if r.random() < 0.09:
            y = CY + r.choice((-1, 1)) * a * 1.7
        pts.append((x, y))
        x += r.uniform(4, 9)
    pts.append((x_in, CY))
    noisy = poly(pts)
    steady = poly([(xx, CY + 5 * math.sin((xx - x_out) / 58 * 2 * math.pi)) for xx in range(int(x_out), 1141, 3)])

    g = p.uid("grad")
    p.defs_add(f'<linearGradient id="{g}" gradientUnits="userSpaceOnUse" x1="{x_in}" x2="{x_out}">'
               f'<stop offset=".08" stop-color="{t.accent}"/><stop offset=".92" stop-color="{t.steady}"/>'
               f"</linearGradient>")
    p.add(
        f'<path d="{noisy}" stroke="{t.accent}" stroke-width="1.3" opacity=".6" stroke-linejoin="round" '
        f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 1.6, 0.3, "cubic-bezier(.5,0,.2,1)")}"/>',
        f'<path d="{noisy}" stroke="{t.accent}" stroke-width="2.4" stroke-dasharray="2 10" '
        f'stroke-linecap="round" style="animation:flow 7s linear infinite,fade 1s 1.4s both"/>',
        f'<path d="M{x_in} {CY}H{x_out}" stroke="url(#{g})" stroke-width="1.4" '
        f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 1.0, 1.4)}"/>',
        f'<path d="{steady}" stroke="{t.steady}" stroke-width="1.8" stroke-linecap="round" '
        f'pathLength="1" style="stroke-dasharray:1;{anim("draw", 0.9, 2.0, "ease-out")}"/>',
        f'<path d="{steady}" stroke="{t.steady}" stroke-width="2.6" stroke-dasharray="2 10" '
        f'stroke-linecap="round" style="animation:flow 9s linear infinite,fade 1s 2.4s both"/>',
    )
    p.t_(60, CY - 62, "IN ▸ TOIL · DRIFT · 3 A.M. PAGES", "mono", 13, t.accent, ls=0.12,
         style=anim("fade", 1, 0.9))
    p.t_(1140, CY - 40, "OUT ▸ STEADY STATE", "mono", 13, t.steady, anchor="end", ls=0.12,
         style=anim("fade", 1, 2.4))


def _type(p: Plate, t: Theme) -> None:
    rise = lambda d: anim("rise", 1.1, d)  # noqa: E731
    p.t_(60, 450, "Declare it once.", "serifi", 56, t.ink, style=rise(1.7))
    p.spans(60, 512, [("Let the ", "serifi", t.ink), ("loop", "serifi", t.steady),
                      (" do the rest.", "serifi", t.ink)], size=56, style=rise(1.9))
    p.t_(60, 562, "CLOUD DEVOPS ENGINEER — AWS · KUBERNETES · TERRAFORM · PYTHON · AI AGENTS",
         "mono", 13, t.ink2, ls=0.12, style=anim("fade", 1.2, 2.3))

    # the name, outlined and plotted glyph by glyph
    probe, w = outline("disp", "ANUP NARKHEDE", 100, 0, 0, ls=-0.01)
    size = 100 * 1080 / w
    glyphs, _ = outline("disp", "ANUP NARKHEDE", size, 60, 684, ls=-0.01)
    for i, (_ch, d, _x) in enumerate(glyphs):
        p.add(f'<path d="{d}" fill="{t.ink}" stroke="{t.ink}" stroke-width="1.1" pathLength="1" '
              f'style="stroke-dasharray:1;animation:gdraw 2.4s cubic-bezier(.55,0,.25,1) {0.5 + i * 0.075:.3f}s both"/>')
    p.add(f'<path d="M60 596V700" stroke="{t.accent}" stroke-width="1.5" opacity="0" '
          f'style="animation:sweep 2.6s cubic-bezier(.55,0,.35,1) .45s both"/>')

    p.t_(60, 726, "fig. 00 — noise enters the reconciliation loop and leaves as steady state.",
         "serifi", 17, t.ink3, style=anim("fade", 1.2, 3.0))
    p.t_(1140, 726, "PL. 00 / 07", "mono", 12, t.ink3, anchor="end", ls=0.16, style=anim("fade", 1.2, 3.0))
