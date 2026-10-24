"""PL. 02 — Two Control Planes. Left: Kubernetes reconciling a crashed pod.
Right: an agent loop — intent, plan, human approval, tool calls over MCP, verify."""
from __future__ import annotations

from ..kit import Plate, Theme, anim, header

W, H = 1200, 610
LOOP = 10.0  # seconds, fig. A
AGENT = 8.0  # seconds, fig. B


def build(t: Theme) -> Plate:
    p = Plate(
        "planes", W, H, t, "Two Control Planes",
        "Two animated reconciliation loops side by side. Figure A, for containers: a Kubernetes control plane "
        "(api-server, scheduler, controller, etcd) watches three worker nodes; a pod crashes, ready replicas drop "
        "from 6 to 5, and the controller schedules a replacement on another node. Figure B, for intent: an intent "
        "goes to an agent, which waits for a human approval switch, then calls tools (kubectl, terraform, aws, gh) "
        "through MCP and verifies the result.",
    )
    header(p, "02", "Two Control Planes", "fig. a containers / fig. b intent")
    p.add(f'<path d="M600 108V520" stroke="{t.rule}"/>',
          f'<circle cx="600" cy="314" r="17" fill="{t.page}" stroke="{t.rule}"/>')
    p.t_(600, 321, "×", "serif", 24, t.ink3, anchor="middle")
    _containers(p, t)
    _intent(p, t)
    p.t_(600, 574, "Two reconciliation loops: one converges containers, the other converges intent.",
         "serifi", 23, t.ink2, anchor="middle")
    return p


def _pct(sec: float, total: float) -> str:
    return f"{sec / total * 100:.1f}%"


def _containers(p: Plate, t: Theme) -> None:
    p.spans(60, 118, [("FIG. A  ", "monob", t.accent), ("FOR CONTAINERS", "dispm", t.ink)], size=13, ls=0.16)
    p.t_(60, 152, "Declare replicas; the controller makes it so.", "serifi", 23, t.ink2)

    # control plane
    p.add(f'<rect x="80" y="182" width="460" height="86" rx="10" stroke="{t.ink2}" stroke-width="1.2"/>')
    p.t_(96, 202, "CONTROL PLANE", "mono", 10, t.ink3, ls=0.22)
    cells = ["api-server", "scheduler", "controller", "etcd"]
    for i, c in enumerate(cells):
        x = 96 + i * 110
        cls = ' class="ctl"' if c == "controller" else ""
        p.add(f'<rect{cls} x="{x}" y="216" width="98" height="36" rx="6" fill="{t.fill}" stroke="{t.rule}"/>')
        p.t_(x + 49, 238.5, c, "mono", 12, t.ink, anchor="middle")

    # nodes and pods
    slots = []
    for n in range(3):
        nx = 80 + n * 160
        cx = nx + 70
        p.add(f'<path d="M{cx} 268V332" stroke="{t.rule}"/>',
              f'<path d="M{cx} 268V332" stroke="{t.ink3}" stroke-dasharray="2 10" '
              f'style="animation:flowr 6s linear infinite"/>',
              f'<rect x="{nx}" y="332" width="140" height="122" rx="10" stroke="{t.ink3}" stroke-width="1"/>')
        p.t_(nx + 14, 353, f"node-{n + 1}", "mono", 11, t.ink3, ls=0.06)
        for k in range(3):
            sx = nx + 18 + k * 42
            slots.append((n, k, sx, 372))
            p.add(f'<rect x="{sx}" y="372" width="30" height="30" rx="6" stroke="{t.rule}" stroke-dasharray="3 3"/>')
        p.t_(nx + 14, 434, "kubelet", "mono", 10, t.ink3, ls=0.06)
        p.add(f'<circle cx="{nx + 70}" cy="430.5" r="2.5" fill="{t.steady}" '
              f'style="animation:blink 2s steps(1) {n * .5}s infinite"/>')

    T = LOOP
    p.style(
        f"@keyframes podA{{0%,{_pct(2.4, T)}{{fill:{t.ink2};opacity:1}}{_pct(2.7, T)}{{fill:{t.accent};opacity:1}}"
        f"{_pct(3.4, T)}{{fill:{t.accent};opacity:0}}{_pct(9.3, T)}{{fill:{t.ink2};opacity:0}}100%{{fill:{t.ink2};opacity:1}}}}"
        f"@keyframes podN{{0%,{_pct(4.8, T)}{{fill:{t.steady};opacity:0;transform:scale(.4)}}"
        f"{_pct(5.3, T)}{{fill:{t.steady};opacity:1;transform:scale(1)}}{_pct(7.2, T)}{{fill:{t.ink2};opacity:1}}"
        f"{_pct(9.3, T)}{{fill:{t.ink2};opacity:1;transform:scale(1)}}100%{{fill:{t.ink2};opacity:0;transform:scale(1)}}}}"
        f"@keyframes okA{{0%,{_pct(2.8, T)}{{opacity:1}}{_pct(2.9, T)},{_pct(5.7, T)}{{opacity:0}}{_pct(5.8, T)},100%{{opacity:1}}}}"
        f"@keyframes badA{{0%,{_pct(2.8, T)}{{opacity:0}}{_pct(2.9, T)},{_pct(5.7, T)}{{opacity:1}}{_pct(5.8, T)},100%{{opacity:0}}}}"
        f"@keyframes route{{0%,{_pct(3.6, T)}{{stroke-dashoffset:1;opacity:1}}{_pct(4.7, T)}{{stroke-dashoffset:0;opacity:1}}"
        f"{_pct(6.0, T)}{{stroke-dashoffset:0;opacity:1}}{_pct(6.6, T)},100%{{stroke-dashoffset:0;opacity:0}}}}"
        f"@keyframes ctl{{0%,{_pct(3.4, T)}{{stroke:{t.rule}}}{_pct(3.7, T)},{_pct(5.2, T)}{{stroke:{t.steady}}}"
        f"{_pct(5.8, T)},100%{{stroke:{t.rule}}}}}"
        f".ctl{{animation:ctl {T}s linear infinite}}"
    )
    for n, k, sx, sy in slots:
        if k == 2:
            continue
        style = ""
        if (n, k) == (1, 0):
            style = f' style="animation:podA {T}s linear infinite"'
        p.add(f'<rect x="{sx}" y="{sy}" width="30" height="30" rx="6" fill="{t.ink2}"{style}/>')
    nx, ny = slots[8][2], slots[8][3]
    p.add(f'<rect x="{nx}" y="{ny}" width="30" height="30" rx="6" fill="{t.steady}" opacity="0" '
          f'style="transform-origin:{nx + 15}px {ny + 15}px;transform-box:view-box;animation:podN {T}s cubic-bezier(.2,.8,.2,1) infinite"/>')
    p.add(f'<path d="M371 252V300H{nx + 15}V{ny - 4}" stroke="{t.steady}" stroke-width="1.6" pathLength="1" '
          f'stroke-dasharray="1" opacity="0" style="animation:route {T}s ease-in-out infinite"/>')

    # readout
    p.t_(80, 496, "REPLICAS", "mono", 11, t.ink3, ls=0.22)
    p.spans(180, 496, [("desired ", "mono", t.ink3), ("6", "monob", t.ink)], size=15)
    p.add(f'<g style="animation:okA {T}s linear infinite">')
    p.spans(300, 496, [("ready ", "mono", t.ink3), ("6/6", "monob", t.steady), ("  ✓ converged", "mono", t.steady)], size=15)
    p.add(f'</g><g opacity="0" style="animation:badA {T}s linear infinite">')
    p.spans(300, 496, [("ready ", "mono", t.ink3), ("5/6", "monob", t.accent), ("  ↻ reconciling", "mono", t.accent)], size=15)
    p.add("</g>")


def _intent(p: Plate, t: Theme) -> None:
    p.spans(660, 118, [("FIG. B  ", "monob", t.accent), ("FOR INTENT", "dispm", t.ink)], size=13, ls=0.16)
    p.t_(660, 152, "State the goal. An agent plans; a human approves.", "serifi", 23, t.ink2)
    y = 306
    # intent card
    p.add(f'<rect x="660" y="{y - 42}" width="118" height="84" rx="8" stroke="{t.ink2}" stroke-width="1.2"/>')
    p.t_(674, y - 20, "INTENT", "mono", 10, t.ink3, ls=0.22)
    p.t_(674, y + 6, "“ship v2,", "serifi", 19, t.ink)
    p.t_(674, y + 28, "safely”", "serifi", 19, t.ink)
    # agent
    ax = 852
    p.add(f'<path d="M778 {y}H{ax - 46}M{ax + 46} {y}H938M990 {y}H1022" stroke="{t.ink3}"/>',
          f'<circle cx="{ax}" cy="{y}" r="46" stroke="{t.ink2}" stroke-width="1.2"/>',
          f'<circle class="spin" cx="{ax}" cy="{y}" r="32" stroke="{t.ink3}" stroke-dasharray="2 5" '
          f'style="transform-origin:{ax}px {y}px;animation:spin 14s linear infinite"/>',
          f'<circle cx="{ax}" cy="{y}" r="11" fill="{t.steady}" class="core"/>')
    p.t_(ax, y + 74, "AGENT", "dispm", 13, t.ink, anchor="middle", ls=0.18)
    p.t_(ax, y + 94, "plan · call · verify", "mono", 11, t.ink3, anchor="middle")

    # approval switch
    gx, gw = 938, 52
    T = AGENT
    p.style(
        f"@keyframes knob{{0%,{_pct(1.6, T)}{{transform:translateX(0);fill:{t.accent}}}"
        f"{_pct(2.4, T)},{_pct(7.4, T)}{{transform:translateX(26px);fill:{t.steady}}}100%{{transform:translateX(0);fill:{t.accent}}}}}"
        f"@keyframes hold{{0%,{_pct(1.9, T)}{{opacity:1}}{_pct(2.0, T)},{_pct(7.4, T)}{{opacity:0}}{_pct(7.5, T)},100%{{opacity:1}}}}"
        f"@keyframes ok{{0%,{_pct(1.9, T)}{{opacity:0}}{_pct(2.0, T)},{_pct(7.4, T)}{{opacity:1}}{_pct(7.5, T)},100%{{opacity:0}}}}"
        f"@keyframes tool{{0%,{_pct(4.2, T)}{{stroke:{t.rule}}}{_pct(4.4, T)},{_pct(5.4, T)}{{stroke:{t.steady}}}{_pct(6, T)},100%{{stroke:{t.rule}}}}}"
        f"@keyframes core{{0%,{_pct(6.7, T)}{{transform:scale(1)}}{_pct(7.0, T)}{{transform:scale(1.5)}}{_pct(7.6, T)},100%{{transform:scale(1)}}}}"
        f".core{{transform-origin:{ax}px {y}px;transform-box:view-box;animation:core {T}s ease-out infinite}}"
    )
    p.add(f'<rect x="{gx}" y="{y - 13}" width="{gw}" height="26" rx="13" stroke="{t.ink2}" stroke-width="1.2"/>',
          f'<circle cx="{gx + 13}" cy="{y}" r="8" fill="{t.accent}" style="transform-box:view-box;'
          f'animation:knob {T}s cubic-bezier(.5,0,.2,1) infinite"/>')
    p.t_(gx + gw / 2, y - 30, "HUMAN", "dispm", 12, t.ink, anchor="middle", ls=0.18)
    p.add(f'<g style="animation:hold {T}s linear infinite">')
    p.t_(gx + gw / 2, y + 36, "awaiting", "mono", 11, t.accent, anchor="middle")
    p.add(f'</g><g opacity="0" style="animation:ok {T}s linear infinite">')
    p.t_(gx + gw / 2, y + 36, "approved", "mono", 11, t.steady, anchor="middle")
    p.add("</g>")

    # MCP bus and tools
    bx = 1022
    tools = ["kubectl", "terraform", "aws", "gh"]
    ty = [y - 84, y - 28, y + 28, y + 84]
    p.add(f'<path d="M{bx} {ty[0]}V{ty[-1] + 40}" stroke="{t.ink}" stroke-width="3" stroke-linecap="round"/>')
    p.t_(bx, ty[0] - 22, "MCP", "monob", 12, t.ink, anchor="middle", ls=0.2)
    for name, yy in zip(tools, ty):
        cls = ' style="animation:tool %ss linear infinite"' % T if name == "terraform" else ""
        p.add(f'<path d="M{bx} {yy}H1040" stroke="{t.ink3}"/>',
              f'<rect x="1040" y="{yy - 14}" width="100" height="28" rx="14" stroke="{t.rule}" stroke-width="1.4"{cls}/>')
        p.t_(1090, yy + 4.5, name, "mono", 12, t.ink2, anchor="middle")

    # feedback arc
    fb = f"M{bx} {ty[-1] + 40}C{bx} {y + 168} {ax} {y + 168} {ax} {y + 112}"
    p.add(f'<path d="{fb}" stroke="{t.ink3}" stroke-dasharray="2 6"/>')
    p.t_((bx + ax) / 2 + 6, y + 172, "result → verify", "mono", 11, t.ink3, anchor="middle")

    # packets (SMIL motion)
    fwd = f"M778 {y}H{bx}V{ty[1]}H1040"
    flen = (bx - 778) + (y - ty[1]) + (1040 - bx)
    at_gate = (gx - 4 - 778) / flen
    p.add(f'<g class="smil"><circle r="5" fill="{t.accent}">'
          f'<animateMotion dur="{T}s" repeatCount="indefinite" path="{fwd}" calcMode="linear" '
          f'keyPoints="0;{at_gate:.3f};{at_gate:.3f};1;1" keyTimes="0;.2;.3;.53;1"/>'
          f'<animate attributeName="fill" dur="{T}s" repeatCount="indefinite" values="{t.accent};{t.accent};{t.steady};{t.steady}" keyTimes="0;.29;.3;1" calcMode="discrete"/>'
          f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;.54;.55;1" calcMode="discrete"/>'
          f'</circle>'
          f'<circle r="5" fill="{t.steady}" opacity="0">'
          f'<animateMotion dur="{T}s" repeatCount="indefinite" path="{fb}" calcMode="linear" '
          f'keyPoints="0;0;1;1" keyTimes="0;.62;.84;1"/>'
          f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.62;.84;.85;1" calcMode="discrete"/>'
          f'</circle></g>')
