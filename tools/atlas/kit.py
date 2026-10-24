"""Shared drawing kit for the Atlas plates.

Every plate is a hand-composed SVG built from these primitives. Text is set in
fonts embedded as per-plate WOFF2 subsets, so plates render identically on every
platform; display lines can instead be converted to outlines (glyph paths) so
they can be stroke-drawn by CSS.

Animation rule used throughout: an element's *base* style is its final state and
keyframes only describe where it comes from. If animation is disabled (reduced
motion, or a renderer without CSS animation) every plate is still complete.
"""
from __future__ import annotations

import base64
import html
import io
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

# key -> (file, css family, weight, style)
FACES = {
    "disp": ("ArchivoExpanded-ExtraBold.woff2", "AtlasDisplay", 800, "normal"),
    "dispm": ("ArchivoExpanded-Medium.woff2", "AtlasDisplayMedium", 500, "normal"),
    "serif": ("InstrumentSerif-Regular.woff2", "AtlasSerif", 400, "normal"),
    "serifi": ("InstrumentSerif-Italic.woff2", "AtlasSerifItalic", 400, "italic"),
    "mono": ("JetBrainsMono-Regular.woff2", "AtlasMono", 400, "normal"),
    "monob": ("JetBrainsMono-SemiBold.woff2", "AtlasMonoBold", 600, "normal"),
}
FALLBACK = {
    "disp": "'Arial Black',Helvetica,Arial,sans-serif",
    "dispm": "Helvetica,Arial,sans-serif",
    "serif": "Georgia,'Times New Roman',serif",
    "serifi": "Georgia,'Times New Roman',serif",
    "mono": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
    "monob": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
}


# --------------------------------------------------------------------------- theme
@dataclass(frozen=True)
class Theme:
    name: str
    page: str      # GitHub page background the plate sits on
    panel: str     # background of full-bleed title/end cards
    panel_hi: str  # glow colour inside panels
    ink: str       # primary
    ink2: str      # secondary text
    ink3: str      # tertiary text, strong hairlines
    rule: str      # hairlines
    fill: str      # faint fills (cards, strata)
    accent: str    # vermilion: drift, toil, alerts, "before"
    steady: str    # converged state, "after"


DARK = Theme(
    name="dark", page="#0d1117", panel="#07090d", panel_hi="#141b26",
    ink="#ECE8DF", ink2="#A7AEBA", ink3="#6C7480", rule="#2A313B", fill="#121820",
    accent="#FF5B37", steady="#5BE0C0",
)
LIGHT = Theme(
    name="light", page="#ffffff", panel="#F3EFE6", panel_hi="#FFFDF8",
    ink="#16181D", ink2="#4D5461", ink3="#878D97", rule="#D9D4C9", fill="#F6F3EC",
    accent="#DC431F", steady="#08876C",
)
THEMES = (DARK, LIGHT)


# --------------------------------------------------------------------------- fonts
@lru_cache(maxsize=None)
def _font(key: str) -> TTFont:
    return TTFont(FONT_DIR / FACES[key][0])


@lru_cache(maxsize=None)
def _hb_font(key: str):
    import uharfbuzz as hb  # local-only dependency, used for outlined display text

    buf = io.BytesIO()
    f = TTFont(FONT_DIR / FACES[key][0])
    f.flavor = None
    f.save(buf)
    return hb.Font(hb.Face(hb.Blob(buf.getvalue())))


def text_width(key: str, s: str, size: float, ls: float = 0.0) -> float:
    """Advance width of a string (no kerning) in px; ls is letter-spacing in em."""
    f = _font(key)
    upm = f["head"].unitsPerEm
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    adv = sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in s)
    return adv * size / upm + ls * size * len(s)


def outline(key: str, s: str, size: float, x: float, y: float, ls: float = 0.0):
    """Shape `s` with HarfBuzz and return [(glyph_char, svg_path_d, x_advance_start)]."""
    import uharfbuzz as hb

    font = _hb_font(key)
    tt = _font(key)
    upm = tt["head"].unitsPerEm
    gs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    buf = hb.Buffer()
    buf.add_str(s)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    k = size / upm
    pen_x = x
    out = []
    for info, pos, ch in zip(buf.glyph_infos, buf.glyph_positions, s):
        name = order[info.codepoint]
        pen = SVGPathPen(gs)
        gx = pen_x + pos.x_offset * k
        gs[name].draw(TransformPen(pen, (k, 0, 0, -k, gx, y - pos.y_offset * k)))
        d = pen.getCommands()
        if d:
            out.append((ch, d, gx))
        pen_x += pos.x_advance * k + ls * size
    return out, pen_x - x


def font_face_css(key: str, chars: set[str]) -> str:
    file, family, weight, style = FACES[key]
    font = TTFont(FONT_DIR / file)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    sub.subset(font)
    font.flavor = "woff2"
    buf = io.BytesIO()
    font.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (
        f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
        f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    )


# --------------------------------------------------------------------------- plate
BASE_CSS = """
text{font-kerning:normal;}
.anim,.spin,.spinr{transform-box:view-box;}
@keyframes fade{from{opacity:0}}
@keyframes rise{from{opacity:0;transform:translateY(10px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes spinr{to{transform:rotate(-360deg)}}
@keyframes flow{to{stroke-dashoffset:-240}}
@keyframes flowr{to{stroke-dashoffset:240}}
@keyframes draw{from{stroke-dashoffset:1}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.smil{display:none}}
"""


class Plate:
    """Accumulates SVG markup, CSS and the characters used per font face."""

    def __init__(self, slug: str, w: int, h: int, theme: Theme, title: str, desc: str):
        self.slug, self.w, self.h, self.t = slug, w, h, theme
        self.title, self.desc = title, desc
        self.body: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = [BASE_CSS]
        self.chars: dict[str, set[str]] = defaultdict(set)
        self._uid = 0

    # -- plumbing
    def uid(self, prefix: str = "u") -> str:
        self._uid += 1
        return f"{prefix}{self._uid}"

    def add(self, *parts: str) -> None:
        self.body.extend(parts)

    def style(self, css: str) -> None:
        self.css.append(css)

    def defs_add(self, s: str) -> None:
        self.defs.append(s)

    # -- typography
    def text(self, x, y, s, face="mono", size=14, fill=None, anchor="start", ls=0.0,
             upper=False, opacity=None, cls="", style="", attrs="") -> str:
        s = s.upper() if upper else s
        self.chars[face].update(s)
        fill = fill or self.t.ink
        classes = f"f-{face} {cls}".strip()
        a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'class="{classes}"', f'font-size="{size}"', f'fill="{fill}"']
        if anchor != "start":
            a.append(f'text-anchor="{anchor}"')
        if ls:
            a.append(f'letter-spacing="{ls * size:.2f}"')
        if opacity is not None:
            a.append(f'opacity="{opacity}"')
        if style:
            a.append(f'style="{style}"')
        if attrs:
            a.append(attrs)
        el = f"<text {' '.join(a)}>{html.escape(s, quote=False)}</text>"
        return el

    def t_(self, *args, **kw) -> None:
        """text() and append."""
        self.add(self.text(*args, **kw))

    def spans(self, x, y, runs, size=14, anchor="start", ls=0.0, cls="", style="") -> None:
        """One line made of differently styled runs: [(text, face, fill)]."""
        parts = []
        for s, face, fill in runs:
            self.chars[face].update(s)
            parts.append(f'<tspan class="f-{face}" fill="{fill}">{html.escape(s, quote=False)}</tspan>')
        a = f'x="{x:.1f}" y="{y:.1f}" font-size="{size}"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        if ls:
            a += f' letter-spacing="{ls * size:.2f}"'
        if cls:
            a += f' class="{cls}"'
        if style:
            a += f' style="{style}"'
        self.add(f"<text {a}>{''.join(parts)}</text>")

    # -- output
    def render(self) -> str:
        faces = "".join(font_face_css(k, v) for k, v in sorted(self.chars.items()) if v)
        fams = "".join(
            f".f-{k}{{font-family:'{FACES[k][1]}',{FALLBACK[k]};font-weight:{FACES[k][2]};"
            f"font-style:{FACES[k][3]};}}"
            for k in sorted(self.chars)
        )
        css = faces + fams + "".join(self.css)
        css = " ".join(line.strip() for line in css.splitlines())
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-labelledby="title desc" fill="none">'
            f"<title id=\"title\">{html.escape(self.title)}</title>"
            f"<desc id=\"desc\">{html.escape(self.desc)}</desc>"
            f"<style>{css}</style>"
            f"<defs>{''.join(self.defs)}</defs>"
            f"{''.join(self.body)}</svg>"
        )


# --------------------------------------------------------------------------- geometry
def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1):
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}"


def poly(points, close=False) -> str:
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return d + ("Z" if close else "")


def smooth(points, close=False, tension=0.5) -> str:
    """Catmull-Rom spline through points, as cubic Béziers."""
    pts = list(points)
    if close:
        pts = pts[-1:] + pts + pts[:2]
    else:
        pts = pts[:1] + pts + pts[-1:]
    d = f"M{pts[1][0]:.1f} {pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + ("Z" if close else "")


def rng(seed: str) -> random.Random:
    return random.Random(seed)


def anim(name, dur, delay=0.0, ease="cubic-bezier(.2,.7,.2,1)", count="1", fill="both") -> str:
    return f"animation:{name} {dur}s {ease} {delay:.2f}s {count} {fill};"


# --------------------------------------------------------------------------- furniture
def header(p: Plate, num: str, title: str, meta: str, y: int = 46, x0: int = 60, x1: int | None = None) -> None:
    """Plate masthead: number, title, meta and a measuring-rule underline."""
    t = p.t
    x1 = x1 or p.w - 60
    p.spans(x0, y, [(f"PL. {num}", "monob", t.accent), ("   ", "mono", t.ink),
                    (title.upper(), "dispm", t.ink)], size=17, ls=0.14)
    p.t_(x1, y, meta.upper(), "mono", 13, t.ink3, anchor="end", ls=0.12)
    ry = y + 18
    ticks = []
    for i, x in enumerate(range(x0, x1 + 1, 12)):
        h = 9 if i % 25 == 0 else (5 if i % 5 == 0 else 2.5)
        ticks.append(f"M{x} {ry}v{h}")
    p.add(f'<path d="M{x0} {ry}H{x1}" stroke="{t.rule}" stroke-width="1"/>',
          f'<path d="{"".join(ticks)}" stroke="{t.ink3}" stroke-width="1" opacity=".55"/>')


def crop_marks(p: Plate, inset: int = 22, size: int = 12, color: str | None = None) -> None:
    c = color or p.t.ink3
    d = []
    for x, y, sx, sy in ((inset, inset, 1, 1), (p.w - inset, inset, -1, 1),
                         (inset, p.h - inset, 1, -1), (p.w - inset, p.h - inset, -1, -1)):
        d.append(f"M{x} {y + sy * size}V{y}H{x + sx * size}")
    p.add(f'<path d="{"".join(d)}" stroke="{c}" stroke-width="1" opacity=".7"/>')


def registration(p: Plate, x: float, y: float, r: float = 7, color: str | None = None) -> None:
    c = color or p.t.ink3
    p.add(f'<g stroke="{c}" stroke-width="1" opacity=".8"><circle cx="{x}" cy="{y}" r="{r}"/>'
          f'<path d="M{x - r * 1.8} {y}H{x + r * 1.8}M{x} {y - r * 1.8}V{y + r * 1.8}"/></g>')


def grain(p: Plate, opacity: float = 0.06) -> None:
    fid = p.uid("grain")
    p.defs_add(
        f'<filter id="{fid}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" stitchTiles="stitch"/>'
        f'<feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 1.6 -0.55"/></filter>'
    )
    p.add(f'<rect width="{p.w}" height="{p.h}" filter="url(#{fid})" opacity="{opacity}" rx="20"/>')


def dot_grid(p: Plate, step=24, r=0.9, cx=None, cy=None, radius=None, opacity=0.55, clip=None) -> None:
    pid, mid, gid = p.uid("dots"), p.uid("mask"), p.uid("fade")
    t = p.t
    p.defs_add(
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{t.ink3}"/></pattern>'
    )
    cx = p.w / 2 if cx is None else cx
    cy = p.h / 2 if cy is None else cy
    radius = radius or max(p.w, p.h) * 0.6
    p.defs_add(
        f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{radius}">'
        f'<stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".55"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="{mid}"><rect width="{p.w}" height="{p.h}" fill="url(#{gid})"/></mask>'
    )
    cl = f' clip-path="url(#{clip})"' if clip else ""
    p.add(f'<g mask="url(#{mid})"{cl}><rect width="{p.w}" height="{p.h}" fill="url(#{pid})" opacity="{opacity}"/></g>')


def chip(p: Plate, x, y, label, size=13, color=None, stroke=None, pad=10, h=26) -> float:
    """Hairline tag. Returns its width."""
    t = p.t
    w = text_width("mono", label, size, 0.04) + pad * 2
    p.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
          f'stroke="{stroke or t.rule}" stroke-width="1"/>')
    p.t_(x + pad, y + h / 2 + size * 0.36, label, "mono", size, color or t.ink2, ls=0.04)
    return w


def chips(p: Plate, x, y, labels, gap=8, **kw) -> float:
    for lab in labels:
        x += chip(p, x, y, lab, **kw) + gap
    return x
