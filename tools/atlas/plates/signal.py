"""PL. 06 — Signal. The last twelve months of GitHub contributions plotted as a
seismograph trace. Regenerated weekly by .github/workflows/signal.yml from
tools/data/contributions.json."""
from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

from ..kit import Plate, Theme, anim, header, poly

W, H = 1200, 340
DATA = Path(__file__).resolve().parents[2] / "data" / "contributions.json"
TX0, TX1, BASE, AMP = 360, 1140, 196, 84
MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def _stats(days):
    counts = [c for _, c in days]
    weeks = [sum(counts[i:i + 7]) for i in range(0, len(counts), 7)]
    best_streak = run = 0
    for c in counts:
        run = run + 1 if c else 0
        best_streak = max(best_streak, run)
    peak = max(range(len(days)), key=lambda i: counts[i])
    return dict(active=sum(1 for w in weeks if w), weeks=len(weeks), best_week=max(weeks),
                streak=best_streak, peak=peak, max=counts[peak])


def build(t: Theme) -> Plate:
    data = json.loads(DATA.read_text())
    days = data["days"]
    total = data["total"]
    st = _stats(days)
    p = Plate(
        "signal", W, H, t, "Signal — contributions, last 12 months",
        f"{total} GitHub contributions over the last twelve months, plotted as a seismograph trace. "
        f"Busiest week: {st['best_week']} contributions; longest streak: {st['streak']} days; "
        f"active in {st['active']} of {st['weeks']} weeks. Updated {data['fetched']}.",
    )
    header(p, "06", "Signal", f"last 12 months · updated {data['fetched']}")

    # left: readout
    p.t_(60, 170, f"{total}", "disp", 72, t.ink, ls=-0.02, style=anim("rise", .9, .1))
    p.t_(62, 198, "CONTRIBUTIONS · 12 MONTHS", "mono", 11, t.ink3, ls=0.2)
    rows = [("busiest week", str(st["best_week"])), ("longest streak", f"{st['streak']} days"),
            ("active weeks", f"{st['active']}/{st['weeks']}")]
    for i, (k, v) in enumerate(rows):
        y = 236 + i * 22
        p.t_(62, y, k, "mono", 13, t.ink2)
        p.t_(300, y, v, "monob", 13, t.ink, anchor="end")
        p.add(f'<path d="M{62 + len(k) * 8.4 + 8:.0f} {y - 4}H{300 - len(v) * 8.4 - 8:.0f}" stroke="{t.rule}" stroke-dasharray="1 4"/>')

    # trace
    n = len(days)
    mx = max(st["max"], 1)
    pts = []
    for i, (_, c) in enumerate(days):
        x = TX0 + i * (TX1 - TX0) / (n - 1)
        a = AMP * math.sqrt(c / mx) if c else 1.2 * math.sin(i * 2.7)
        sign = 1 if i % 2 else -1
        pts.append((x, BASE - sign * a * (0.75 + 0.25 * math.sin(i * 1.3))))
    trace = poly(pts)
    gid = p.uid("trace")
    p.defs_add(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{TX0}" x2="{TX1}">'
               f'<stop offset="0" stop-color="{t.steady}" stop-opacity=".35"/>'
               f'<stop offset=".7" stop-color="{t.steady}"/></linearGradient>')
    grid = "".join(f"M{TX0} {BASE + k * AMP / 2:.0f}H{TX1}" for k in (-2, -1, 1, 2))
    p.add(f'<path d="{grid}" stroke="{t.rule}" stroke-dasharray="1 5"/>',
          f'<path d="M{TX0} {BASE}H{TX1}" stroke="{t.rule}"/>',
          f'<path d="{trace}" stroke="url(#{gid})" stroke-width="1.3" stroke-linejoin="round" pathLength="1" '
          f'style="stroke-dasharray:1;{anim("draw", 3.4, .3, "linear")}"/>')
    # pen at the live end
    ex, ey = pts[-1]
    p.add(f'<g style="{anim("fade", .4, 3.6)}"><path d="M{ex} {BASE - AMP - 10}V{BASE + AMP + 6}" stroke="{t.ink3}"/>'
          f'<circle cx="{ex}" cy="{ey:.1f}" r="4" fill="{t.steady}" style="animation:blink 1.2s steps(1) infinite"/></g>')

    # peak marker
    pk = st["peak"]
    px, py = pts[pk]
    pd = date.fromisoformat(days[pk][0])
    top = BASE - AMP - 14
    p.add(f'<path d="M{px:.1f} {min(py, BASE) - 4:.1f}V{top + 6}" stroke="{t.accent}" style="{anim("fade", .6, 2.4)}"/>')
    label = f"peak · {st['max']} on {pd.strftime('%d %b %Y')}"
    anchor = "end" if px > TX1 - 200 else "start"
    p.t_(px + (-6 if anchor == "end" else 6), top + 4, label.upper(), "mono", 10, t.accent, anchor=anchor, ls=0.14,
         style=anim("fade", .6, 2.5))

    # month ticks
    ticks = []
    for i, (ds, _) in enumerate(days):
        d = date.fromisoformat(ds)
        if d.day == 1:
            x = TX0 + i * (TX1 - TX0) / (n - 1)
            ticks.append(f"M{x:.1f} {BASE + AMP + 10}v6")
            p.t_(x + 4, BASE + AMP + 26, MONTHS[d.month - 1], "mono", 10, t.ink3, ls=0.16)
    p.add(f'<path d="{"".join(ticks)}" stroke="{t.ink3}"/>')
    return p
