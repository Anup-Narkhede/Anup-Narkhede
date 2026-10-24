"""PL. 04 — Exhibits. One card per featured repository: a small animated
schematic of how the project actually works, plus title, premise and stack."""
from __future__ import annotations

import math

from ..kit import Plate, Theme, anim, arc, chips, polar

W, H = 1200, 380
AX = 500  # art panel width

EXHIBITS = [
    dict(
        slug="exhibit-01", num="01", kind="GitOps · CI/CD",
        title=["Two-Repo", "GitOps"], line="Ship by commit; let the cluster pull.",
        spec="app repo → Jenkins → ECR   ·   manifest repo → Argo CD → K8s",
        chips=["Python", "Flask", "Docker", "Jenkins", "Amazon ECR", "Argo CD", "Terraform"],
        repo="cloud-native-monitoring-app-code",
        desc="A Flask and psutil monitoring app built by Jenkins into Docker images pushed to Amazon ECR, with a "
             "separate manifest repository that Argo CD syncs into Kubernetes.",
    ),
    dict(
        slug="exhibit-02", num="02", kind="Microservices · Kubernetes",
        title=["Pinger"], line="Is it up? How fast? Ask again, forever.",
        spec="frontend · pinger v1 + v2 · details   on a 3-worker kind cluster",
        chips=["Node.js", "Docker", "Kubernetes", "kind", "Prometheus", "Grafana"],
        repo="Pinger_App_K8S",
        desc="Three services that continuously probe URLs and record latency, response code and size, deployed "
             "to a local multi-node kind cluster with two pinger versions running side by side.",
    ),
    dict(
        slug="exhibit-03", num="03", kind="Infrastructure as code · AWS",
        title=["Modular", "Terraform"], line="Infrastructure assembled from parts.",
        spec="lambda module: IAM role · archive_file · source hash   ·   S3 state, native lockfile",
        chips=["Terraform", "AWS Lambda", "IAM", "S3 backend", "Python"],
        repo="terraform-project-an",
        desc="A module-per-service Terraform layout with remote state in S3. The Lambda module is built (IAM "
             "execution role, packaged source, environment); API Gateway, EC2 and MemoryDB modules are scaffolded.",
    ),
    dict(
        slug="exhibit-04", num="04", kind="Serverless · AWS",
        title=["Serverless", "Web App"], line="Nothing to patch. One request path.",
        spec="CloudFront + S3 → Cognito → API Gateway → Lambda → DynamoDB",
        chips=["S3", "CloudFront", "Cognito", "API Gateway", "Lambda", "DynamoDB"],
        repo="Serverless-Web-Application",
        desc="A web application with no servers: static hosting on S3 behind CloudFront, sign-in with Cognito, "
             "and an API Gateway and Lambda backend storing data in DynamoDB.",
    ),
]


def build_all(t: Theme) -> list[Plate]:
    return [_card(t, ex, art) for ex, art in zip(EXHIBITS, (_gitops, _pinger, _terraform, _serverless))]


def _card(t: Theme, ex: dict, art) -> Plate:
    p = Plate(ex["slug"], W, H, t, f"Exhibit {ex['num']} — {' '.join(ex['title'])}",
              f"{ex['desc']} Illustrated with an animated schematic. Repository: github.com/Anup-Narkhede/{ex['repo']}.")
    clip = p.uid("art")
    p.defs_add(f'<clipPath id="{clip}"><rect x="1" y="1" width="{AX}" height="{H - 2}" rx="15"/>'
               f'<rect x="20" y="1" width="{AX - 19}" height="{H - 2}"/></clipPath>')
    p.add(f'<g clip-path="url(#{clip})"><rect width="{AX}" height="{H}" fill="{t.fill}"/></g>',
          f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" stroke="{t.rule}"/>',
          f'<path d="M{AX} 1V{H - 1}" stroke="{t.rule}"/>')
    # art panel corner index
    p.t_(26, 38, f"FIG. {ex['num']}", "mono", 11, t.ink3, ls=0.22)
    art(p, t)

    x = AX + 52
    p.spans(x, 62, [(f"EXHIBIT {ex['num']}", "monob", t.accent), ("   ", "mono", t.ink),
                    (ex["kind"].upper(), "mono", t.ink3)], size=13, ls=0.18)
    y = 122
    for i, line in enumerate(ex["title"]):
        p.t_(x, y + i * 50, line, "disp", 44, t.ink, ls=-0.01, style=anim("rise", .9, .1 + i * .08))
    y += (len(ex["title"]) - 1) * 50 + 44
    p.t_(x, y, ex["line"], "serifi", 25, t.ink2, style=anim("fade", 1, .4))
    p.t_(x, y + 40, ex["spec"], "mono", 12.5, t.ink, ls=0.02, style=anim("fade", 1, .55))
    chips(p, x, y + 62, ex["chips"], size=12, h=24, pad=9, gap=7)
    p.spans(x, H - 30, [("github.com/Anup-Narkhede/", "mono", t.ink3), (ex["repo"], "monob", t.ink2),
                        ("  ↗", "mono", t.accent)], size=13)
    return p


# --------------------------------------------------------------------------- art
def _doc(p, t, x, y, w, h, label, seed):
    f = 14
    p.add(f'<path d="M{x} {y}H{x + w - f}L{x + w} {y + f}V{y + h}H{x}Z" fill="{t.page}" stroke="{t.ink2}" stroke-width="1.2"/>'
          f'<path d="M{x + w - f} {y}V{y + f}H{x + w}" stroke="{t.ink2}"/>')
    widths = [(seed * 7 + k * 13) % 5 for k in range(6)]
    for k, wv in enumerate(widths):
        lw = 18 + wv * 9
        p.add(f'<path d="M{x + 12 + (k % 3 == 1) * 8} {y + 26 + k * 11}h{min(lw, w - 30)}" stroke="{t.ink3}" stroke-width="2.5" stroke-linecap="round"/>')
    p.t_(x, y + h + 20, label, "mono", 11, t.ink2, ls=0.12)


def _gear(cx, cy, r, teeth=8):
    pts = []
    for i in range(teeth * 4):
        a = i / (teeth * 4) * 360
        rr = r if (i % 4) in (0, 1) else r * 0.78
        pts.append(polar(cx, cy, rr, a))
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def _cube(cx, cy, s):
    h = s * 0.58
    top = f"M{cx} {cy - s}L{cx + s} {cy - s + h}L{cx} {cy - s + 2 * h}L{cx - s} {cy - s + h}Z"
    left = f"M{cx - s} {cy - s + h}L{cx} {cy - s + 2 * h}V{cy + h}L{cx - s} {cy}Z"
    right = f"M{cx + s} {cy - s + h}L{cx} {cy - s + 2 * h}V{cy + h}L{cx + s} {cy}Z"
    return top, left, right


def _hex(cx, cy, r):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (polar(cx, cy, r, a) for a in range(-90, 270, 60))) + "Z"


def _gitops(p: Plate, t: Theme):
    _doc(p, t, 56, 72, 82, 98, "app repo", 1)
    _doc(p, t, 56, 222, 82, 98, "manifest repo", 2)
    # build lane
    p.add(f'<path d="M138 120H196M244 120H300" stroke="{t.ink3}"/>',
          f'<g class="spin" style="transform-origin:220px 120px;animation:spin 8s linear infinite">'
          f'<path d="{_gear(220, 120, 22)}" stroke="{t.ink}" stroke-width="1.3" fill="{t.page}"/>'
          f'<circle cx="220" cy="120" r="7" stroke="{t.ink}"/></g>')
    p.t_(220, 166, "jenkins", "mono", 11, t.ink2, anchor="middle", ls=0.12)
    top, left, right = _cube(330, 124, 26)
    p.add(f'<path d="{top}" fill="{t.page}" stroke="{t.ink}" stroke-width="1.2"/>'
          f'<path d="{left}" fill="{t.ink3}" fill-opacity=".25" stroke="{t.ink}" stroke-width="1.2"/>'
          f'<path d="{right}" fill="{t.ink3}" fill-opacity=".5" stroke="{t.ink}" stroke-width="1.2"/>')
    p.t_(330, 182, "ecr", "mono", 11, t.ink2, anchor="middle", ls=0.12)
    # sync lane
    p.add(f'<path d="M138 270H190M250 270H352" stroke="{t.ink3}"/>',
          f'<g class="spin" style="transform-origin:220px 270px;animation:spinr 5s linear infinite">'
          f'<path d="{arc(220, 270, 22, 200, 340)}" stroke="{t.steady}" stroke-width="2"/>'
          f'<path d="{arc(220, 270, 22, 20, 160)}" stroke="{t.steady}" stroke-width="2"/>'
          f'<path d="M238.7 255.8l4.9 -.5-1.5 5.2M201.3 284.2l-4.9 .5 1.5-5.2" stroke="{t.steady}" stroke-width="2"/></g>')
    p.t_(220, 318, "argo cd · sync", "mono", 11, t.ink2, anchor="middle", ls=0.12)
    # cluster
    p.add(f'<path d="{_hex(410, 262, 58)}" stroke="{t.ink}" stroke-width="1.3" fill="{t.page}"/>',
          f'<path d="M330 156C330 210 360 214 380 222" stroke="{t.ink3}" stroke-dasharray="3 4"/>')
    p.t_(372, 208, "pull", "mono", 10, t.ink3, ls=0.1)
    p.style("@keyframes pod{0%,100%{opacity:.55}50%{opacity:1}}")
    for i, (px, py) in enumerate(((392, 246), (414, 266), (390, 284))):
        p.add(f'<rect x="{px}" y="{py}" width="16" height="16" rx="3" fill="{t.steady}" '
              f'style="animation:pod 2.4s ease-in-out {i * .4}s infinite"/>')
    p.t_(410, 342, "cluster", "mono", 11, t.ink2, anchor="middle", ls=0.12)
    for path, dur, beg, col in (("M138 120H330", 3.2, 0, t.accent), ("M138 270H384", 3.2, 1.6, t.steady)):
        p.add(f'<circle class="smil" r="4" fill="{col}"><animateMotion dur="{dur}s" begin="{beg}s" '
              f'repeatCount="indefinite" path="{path}"/></circle>')


def _pinger(p: Plate, t: Theme):
    cx, cy = 250, 196
    for r in (36, 76, 116, 150):
        p.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{t.rule}"/>')
    p.add(f'<path d="M{cx - 160} {cy}H{cx + 160}M{cx} {cy - 160}V{cy + 160}" stroke="{t.rule}" stroke-dasharray="2 4"/>')
    sweeps = ((t.steady, 4.0, "v2"), (t.ink2, 6.0, "v1"))
    for col, dur, _ in sweeps:
        gid = p.uid("sw")
        x1, y1 = polar(cx, cy, 150, -90)
        x0, y0 = polar(cx, cy, 150, -90 - 44)
        p.defs_add(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}">'
                   f'<stop offset="0" stop-color="{col}" stop-opacity="0"/><stop offset="1" stop-color="{col}" stop-opacity=".35"/></linearGradient>')
        p.add(f'<g class="spin" style="transform-origin:{cx}px {cy}px;animation:spin {dur}s linear infinite">'
              f'<path d="M{cx} {cy}L{x0:.1f} {y0:.1f}A150 150 0 0 1 {x1:.1f} {y1:.1f}Z" fill="url(#{gid})"/>'
              f'<path d="M{cx} {cy}L{x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="1.6"/></g>')
    p.style("@keyframes blip{0%{opacity:1;transform:scale(1.6)}30%,100%{opacity:.35;transform:scale(1)}}")
    targets = [(-50, 120, "42 ms"), (20, 70, "118 ms"), (110, 132, "7 ms"), (200, 96, "timeout"), (250, 46, "63 ms")]
    for ang, r, lab in targets:
        x, y = polar(cx, cy, r, ang)
        col = t.accent if lab == "timeout" else t.ink
        delay = ((ang + 90) % 360) / 360 * 4.0
        p.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{col}" style="transform-origin:{x:.1f}px {y:.1f}px;'
              f'transform-box:view-box;animation:blip 4s ease-out {delay:.2f}s infinite"/>')
        p.t_(x + 9, y + 4, lab, "mono", 11, col if lab == "timeout" else t.ink2)
    p.add(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{t.ink}"/>')
    p.t_(26, H - 26, "sweep v1", "mono", 11, t.ink2, ls=0.1)
    p.add(f'<path d="M100 {H - 30}h18" stroke="{t.ink2}" stroke-width="2"/>')
    p.t_(140, H - 26, "sweep v2", "mono", 11, t.steady, ls=0.1)
    p.add(f'<path d="M214 {H - 30}h18" stroke="{t.steady}" stroke-width="2"/>')


def _slab(p, t, cx, cy, w, d, h, label, delay, built=False):
    """Isometric module slab: solid when built, a dashed blueprint when only scaffolded."""
    k = 0.5
    top = f"M{cx} {cy - d * k}L{cx + w} {cy}L{cx} {cy + d * k}L{cx - w} {cy}Z"
    left = f"M{cx - w} {cy}L{cx} {cy + d * k}V{cy + d * k + h}L{cx - w} {cy + h}Z"
    right = f"M{cx + w} {cy}L{cx} {cy + d * k}V{cy + d * k + h}L{cx + w} {cy + h}Z"
    if built:
        edge, dash, fl, fr, ft = t.steady, "", ".22", ".45", t.page
    else:
        edge, dash, fl, fr, ft = t.ink3, ' stroke-dasharray="4 4"', "0", "0", "none"
    p.add(f'<g style="{anim("rise", .8, delay)}"><path d="{left}" fill="{t.ink3}" fill-opacity="{fl}" stroke="{edge}" stroke-width="1.2"{dash}/>'
          f'<path d="{right}" fill="{t.ink3}" fill-opacity="{fr}" stroke="{edge}" stroke-width="1.2"{dash}/>'
          f'<path d="{top}" fill="{ft}" stroke="{edge}" stroke-width="1.2"{dash}/>')
    p.t_(cx, cy + 4, label, "mono", 11, t.ink if built else t.ink3, anchor="middle")
    if not built:
        p.t_(cx, cy + 18, "scaffold", "mono", 9, t.ink3, anchor="middle", ls=0.16)
    p.add("</g>")


def _terraform(p: Plate, t: Theme):
    mods = [(170, 290, "memorydb"), (330, 290, "ec2"), (170, 196, "lambda"), (330, 196, "api_gateway")]
    for i, (x, y, lab) in enumerate(mods):
        _slab(p, t, x, y, 70, 80, 16, lab, .1 + i * .15, built=lab == "lambda")
    # plan/apply scan
    p.style("@keyframes scan{0%{transform:translateY(-40px);opacity:0}15%{opacity:.9}70%{opacity:.9}"
            "100%{transform:translateY(240px);opacity:0}}")
    p.add(f'<path d="M130 110H400" stroke="{t.steady}" stroke-width="1.4" opacity="0" '
          f'style="animation:scan 5s cubic-bezier(.5,0,.5,1) 1s infinite"/>')
    p.t_(400, 102, "terraform plan", "mono", 10, t.steady, anchor="end", ls=0.1, style="animation:fade 1s 1s both")
    # event path: request → api_gateway → lambda → slack
    ev = "M470 120C430 120 410 180 360 192M300 196H200M150 186C110 150 92 112 70 96"
    p.add(f'<path d="{ev}" stroke="{t.accent}" stroke-width="1.2" stroke-dasharray="3 5"/>')
    p.add(f'<rect x="34" y="66" width="62" height="30" rx="8" stroke="{t.ink3}" stroke-dasharray="4 4"/>'
          f'<path d="M48 96l-6 9 14-9" stroke="{t.ink3}" stroke-dasharray="4 4"/>')
    p.t_(65, 86, "slack", "mono", 11, t.ink3, anchor="middle")
    p.t_(474, 110, "event", "mono", 10, t.accent, anchor="end")
    p.add(f'<circle class="smil" r="4" fill="{t.accent}"><animateMotion dur="4s" repeatCount="indefinite" '
          f'path="M470 120C430 120 410 180 360 192L200 196C150 186 110 150 70 96"/></circle>')
    # state backend
    p.add(f'<ellipse cx="420" cy="306" rx="26" ry="8" stroke="{t.ink2}" fill="{t.page}"/>'
          f'<path d="M394 306V334A26 8 0 0 0 446 334V306" stroke="{t.ink2}"/>'
          f'<rect x="413" y="314" width="14" height="11" rx="2" stroke="{t.steady}"/>'
          f'<path d="M416 314v-4a4 4 0 0 1 8 0v4" stroke="{t.steady}"/>')
    p.t_(420, 356, "s3 state · lock", "mono", 10, t.ink2, anchor="middle")


def _serverless(p: Plate, t: Theme):
    r1, r2 = 132, 262
    nodes1 = [(70, "user"), (190, "cloudfront"), (310, "s3")]
    nodes2 = [(70, "cognito"), (190, "api gw"), (310, "lambda"), (430, "dynamodb")]
    path = f"M70 {r1}H310M190 {r1}C190 {r1 + 60} 70 {r2 - 60} 70 {r2}H430"
    p.add(f'<path d="{path}" stroke="{t.ink3}"/>')

    def node(x, y, kind):
        p.add(f'<circle cx="{x}" cy="{y}" r="26" fill="{t.page}" stroke="{t.ink}" stroke-width="1.2"/>')
        if kind == "user":
            p.add(f'<circle cx="{x}" cy="{y - 6}" r="6" stroke="{t.ink}"/><path d="M{x - 11} {y + 13}a11 9 0 0 1 22 0" stroke="{t.ink}"/>')
        elif kind == "cloudfront":
            p.add(f'<circle cx="{x}" cy="{y}" r="13" stroke="{t.ink}"/><ellipse cx="{x}" cy="{y}" rx="5.5" ry="13" stroke="{t.ink}"/>'
                  f'<path d="M{x - 13} {y}H{x + 13}" stroke="{t.ink}"/>')
        elif kind == "s3":
            p.add(f'<path d="M{x - 12} {y - 9}H{x + 12}L{x + 9} {y + 12}H{x - 9}Z" stroke="{t.ink}"/>'
                  f'<ellipse cx="{x}" cy="{y - 9}" rx="12" ry="3.5" stroke="{t.ink}" fill="{t.page}"/>')
        elif kind == "cognito":
            p.add(f'<path d="M{x} {y - 14}L{x + 11} {y - 9}V{y + 1}C{x + 11} {y + 8} {x + 5} {y + 12} {x} {y + 15}'
                  f'C{x - 5} {y + 12} {x - 11} {y + 8} {x - 11} {y + 1}V{y - 9}Z" stroke="{t.ink}"/>'
                  f'<path d="M{x - 4} {y}l3 3 6-7" stroke="{t.steady}" stroke-width="1.6"/>')
        elif kind == "api gw":
            p.add(f'<path d="M{x - 8} {y - 12}h-5v24h5M{x + 8} {y - 12}h5v24h-5M{x - 5} {y}H{x + 5}" stroke="{t.ink}"/>')
        elif kind == "lambda":
            p.t_(x, y + 9, "λ", "serifi", 30, t.ink, anchor="middle")
        elif kind == "dynamodb":
            p.add(f'<rect x="{x - 12}" y="{y - 11}" width="24" height="22" rx="2" stroke="{t.ink}"/>'
                  f'<path d="M{x - 12} {y - 3}H{x + 12}M{x - 12} {y + 4}H{x + 12}M{x - 3} {y - 11}V{y + 11}" stroke="{t.ink}"/>')
        p.t_(x, y + 48, kind, "mono", 11, t.ink2, anchor="middle", ls=0.08)

    for x, k in nodes1:
        node(x, r1, k)
    for x, k in nodes2:
        node(x, r2, k)
    p.t_(372, r1 + 4, "static", "mono", 10, t.ink3, ls=0.14)
    p.t_(372, r1 + 20, "site", "mono", 10, t.ink3, ls=0.14)
    p.t_(250, r2 - 40, "api", "mono", 10, t.ink3, ls=0.14)
    p.add(f'<circle class="smil" r="4.5" fill="{t.accent}"><animateMotion dur="5s" repeatCount="indefinite" '
          f'path="M70 {r1}H190C190 {r1 + 60} 70 {r2 - 60} 70 {r2}H430"/>'
          f'<animate attributeName="fill" dur="5s" repeatCount="indefinite" values="{t.accent};{t.steady}" '
          f'keyTimes="0;.45" calcMode="discrete"/></circle>')
