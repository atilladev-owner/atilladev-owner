"""Builds the profile's section images, dark and light, from the portfolio's brand.

GitHub strips CSS and fonts from a README, so each section is an SVG that carries its
own subset fonts, images and motion. Motion plays once on arrival, animates only
transform and opacity, and switches off under prefers-reduced-motion.

    python make.py        # writes ../assets/*.svg
"""

import base64
import io
import re
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from PIL import Image

HERE = Path(__file__).parent
OUT = HERE.parent / "assets"
BRAND = Path("C:/Users/owner/Projects/portfolio/public")
W = 1200

THEMES = {
    "dark": dict(bg="#0f0e0b", panel="#161510", ink="#ebe5d5", ink2="#cfc8b4", muted="#9a9481",
                 line="#2a2821", metal="#c9a44b", hair="#8a7031", tone="gold", sweep="#fff4d6", glow=".16", shadow="#050403"),
    "light": dict(bg="#f2efe7", panel="#e9e5da", ink="#16150f", ink2="#3a382f", muted="#5c594a",
                  line="#dcd6c6", metal="#7a5c14", hair="#a8862e", tone="black", sweep="#ffffff", glow=".07", shadow="#5c4a1f"),
}

FONTS = {"disp": "cg500.woff2", "ital": "cg500i.woff2", "smcp": "csc600.woff2",
         "body": "geist400.woff2", "bodym": "geist500.woff2"}
USED: dict[str, set] = {k: set() for k in FONTS}
_metrics = {k: TTFont(HERE / "fonts" / f) for k, f in FONTS.items()}


def text_width(font, s, size, spacing=0.0):
    tt = _metrics[font]
    cmap, hmtx, upm = tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm
    total = sum(hmtx[cmap.get(ord(c), cmap.get(32))][0] for c in s)
    return total * size / upm + spacing * max(len(s) - 1, 0)


def fit(font, s, size, max_w, spacing=0.0):
    """Largest size, at most `size`, at which the string fits `max_w`."""
    while size > 8 and text_width(font, s, size, spacing) > max_w:
        size -= 1
    return size


def T(font, s, x, y, size, fill, *, anchor="start", spacing=0.0, cls="", extra=""):
    USED[font].update(s)
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" fill="{fill}"'
            f' text-anchor="{anchor}"{ls}{c}{extra}>{escape(s)}</text>')


def img_uri(path_or_im, width, fmt="WEBP", quality=88):
    im = Image.open(path_or_im) if not isinstance(path_or_im, Image.Image) else path_or_im
    if im.mode == "RGBA":
        im = im.crop(im.getchannel("A").getbbox())
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    else:
        im.save(buf, fmt, quality=quality, method=6)
    mime = "image/jpeg" if fmt == "JPEG" else "image/webp"
    return f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode()}", im.size


def star(x, y, r, fill):
    """The portfolio's four point star, centred on (x, y)."""
    k = r * 0.22
    return (f'<path d="M{x},{y-r} L{x+k},{y-k} L{x+r},{y} L{x+k},{y+k} L{x},{y+r} '
            f'L{x-k},{y+k} L{x-r},{y} L{x-k},{y-k} Z" fill="{fill}"/>')


def rule(x1, x2, y, t, star_at_start=True):
    s = star(x1 + 7, y, 7, t["metal"]) if star_at_start else ""
    start = x1 + 22 if star_at_start else x1
    return s + f'<line x1="{start}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t["hair"]}" stroke-width="1"/>'


MOTION = """
.rise{animation:rise .8s cubic-bezier(.16,1,.3,1) both}
.fade{animation:fade 1s cubic-bezier(.16,1,.3,1) both}
.grow{transform-box:fill-box;transform-origin:center;animation:grow 1.1s cubic-bezier(.16,1,.3,1) both}
.sweep{animation:sweep 1.8s cubic-bezier(.45,0,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(14px)}}
@keyframes fade{from{opacity:0}}
@keyframes grow{from{opacity:0;transform:scale(.94)}}
@keyframes sweep{from{transform:translateX(-520px)}to{transform:translateX(1400px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.sweep{opacity:0}}
"""


def delay(ms):
    return f' style="animation-delay:{ms}ms"'


def svg(h, body, t, extra_css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"'
            f' role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>/*FONTS*/{MOTION}{extra_css}</style>'
            f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>'
            f'{body}</svg>')


# ── Sections ────────────────────────────────────────────────────────────────

def hero(t):
    h = 440
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 560)
    crest_h = 290
    crest_w = cw * crest_h / ch
    cx, cy = 72, (h - crest_h) / 2
    word, (ww, wh) = img_uri(BRAND / f"brand/wordmark-{t['tone']}.webp", 700)
    x0 = cx + crest_w + 64
    col = W - 70 - x0
    word_h = 44
    typed = "Frontend first. Built to be hard to break."
    tsize = fit("body", typed, 27, col)
    tw = text_width("body", typed, tsize)
    steps = len(typed)
    meta = "Full stack software engineer  ·  Accra, Ghana  ·  Open to relocation"
    msize = fit("smcp", meta, 19, col, 2.4)
    css = f"""
.type{{transform-box:fill-box;transform-origin:left;animation:type {steps*55}ms steps({steps}) 1300ms both}}
.caret{{animation:caret {steps*55}ms steps({steps}) 1300ms both,blink 1s step-end {1300+steps*55}ms 4}}
@keyframes type{{from{{transform:scaleX(0)}}}}
@keyframes caret{{from{{transform:translateX(-{tw:.1f}px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
"""
    glow = (f'<radialGradient id="glow" cx="{(cx+crest_w/2)/W:.3f}" cy=".5" r=".42">'
            f'<stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t['glow']}"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>')
    band = (f'<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="{t["sweep"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{t["sweep"]}" stop-opacity=".75"/>'
            f'<stop offset="1" stop-color="{t["sweep"]}" stop-opacity="0"/></linearGradient>')
    body = f"""<defs>{glow}{band}
<mask id="cm" mask-type="alpha"><image href="{crest}" x="{cx}" y="{cy}" width="{crest_w:.1f}" height="{crest_h}"/></mask>
<clipPath id="tc"><rect class="type" x="{x0}" y="{250-tsize}" width="{tw+4:.1f}" height="{tsize*1.4:.1f}"/></clipPath></defs>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".55"/>
<rect x="0" y="0" width="{W}" height="{h}" rx="24" fill="url(#glow)" class="fade"/>
<image class="grow" href="{crest}" x="{cx}" y="{cy}" width="{crest_w:.1f}" height="{crest_h}"/>
<g mask="url(#cm)"><rect class="sweep" x="{cx-200}" y="{cy}" width="220" height="{crest_h}" fill="url(#band)"{delay(900)}/></g>
<g class="rise"{delay(250)}><image href="{word}" x="{x0-4}" y="94" width="{ww*word_h/wh:.1f}" height="{word_h}"/></g>
<g class="rise"{delay(450)}>{T("disp", "Prince Newson Viala", x0, 200, 64, t["ink"])}</g>
<g clip-path="url(#tc)">{T("body", typed, x0, 250, tsize, t["metal"])}</g>
<rect class="caret" x="{x0+tw+2:.1f}" y="{250-tsize*0.8:.1f}" width="2.5" height="{tsize*0.95:.1f}" fill="{t['metal']}"/>
<g class="fade"{delay(700)}>{rule(x0, W-72, 298, t)}</g>
<g class="rise"{delay(850)}>{T("smcp", meta, x0, 346, msize, t["muted"], spacing=2.4)}</g>"""
    return svg(h, body, t, css, "Atilla Dev. Prince Newson Viala, full stack software engineer in Accra, Ghana. Frontend first. Built to be hard to break.")


def section_title(t, title, note, h=104):
    nw = fit("body", note, 16, 520)
    body = (f'<g class="rise">{T("disp", title, 56, 62, 40, t["ink"])}</g>'
            f'<g class="fade"{delay(200)}>{T("body", note, W-56, 62, nw, t["muted"], anchor="end")}'
            f'{rule(56, W-56, 82, t)}</g>')
    return svg(h, body, t, "", title)


EVIDENCE = [
    ("7", "critical findings closed", "Yifan platform"),
    ("261", "tests on real Postgres", "Plutus"),
    ("39/40", "on a design review", "Marissa"),
    ("9", "days to production", "Marissa"),
]


def evidence(t):
    h = 316
    parts = [f'<g class="rise">{T("disp", "Engineering evidence", 56, 66, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Each figure checked against the project’s own repository.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>']
    colw = (W - 112) / 4
    for i, (n, label, src) in enumerate(EVIDENCE):
        x = 56 + i * colw + (0 if i == 0 else 28)
        if i:
            parts.append(f'<line x1="{56+i*colw:.1f}" y1="118" x2="{56+i*colw:.1f}" y2="284" stroke="{t["line"]}" class="fade"{delay(300+i*120)}/>')
        parts.append(f'<g class="rise"{delay(300+i*140)}>'
                     f'{T("disp", n, x, 184, 80, t["metal"])}'
                     f'{T("body", label, x, 242, fit("body", label, 19, colw-40), t["ink"])}'
                     f'{T("smcp", src, x, 270, 15, t["muted"], spacing=2)}</g>')
    return svg(h, "".join(parts), t, "", "Engineering evidence: 7 critical findings closed on the Yifan platform. 261 tests on real Postgres in Plutus. 39 of 40 on a design review for Marissa. 9 days to production for Marissa.")


PROJECTS = [
    ("marissa", "Marissa", "E-commerce  ·  Client build", ["630 automated tests", "Row locked reservations", "39 of 40 on a design review"], "marissa-home.jpg"),
    ("yifan", "Yifan Travel", "Travel technology  ·  Sole technical owner", ["57,000+ lines of code", "Flights, hotels and payments", "15 section admin console"], "yifan-home.jpg"),
    ("plutus", "Plutus", "Financial infrastructure  ·  Public source", ["261 tests on real Postgres", "Row locked transfers", "Hash chained journal"], "plutus-home.png"),
    ("bubbles", "Bubbles", "Offline first app  ·  Live", ["81 tests", "Works with no signal", "Halves a recipe in one tap"], "bubbles-home-halved.png"),
]


def card(t, slug, name, meta, stats, shot):
    h = 420
    uri, (sw, sh) = img_uri(BRAND / "work" / shot, 1300, "JPEG", 82)
    fx, fy, fw, fh = 520, 36, 644, 348
    left = fx - 56 - 48
    parts = [
        f'<defs><clipPath id="f"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="14"/></clipPath></defs>',
        f'<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="{t["panel"]}" stroke="{t["line"]}"/>',
        f'<g class="rise">{T("smcp", meta, 56, 88, fit("smcp", meta, 16, left, 2.2), t["muted"], spacing=2.2)}</g>',
        f'<g class="rise"{delay(120)}>{T("disp", name, 56, 158, fit("disp", name, 66, left), t["ink"])}</g>',
        f'<g class="fade"{delay(260)}>{rule(56, 56 + left, 192, t)}</g>',
    ]
    for i, s in enumerate(stats):
        y = 244 + i * 40
        parts.append(f'<g class="rise"{delay(320+i*110)}>{star(62, y-7, 5, t["metal"])}'
                     f'{T("body", s, 80, y, fit("body", s, 21, left-24), t["ink2"])}</g>')
    parts.append(f'<g class="rise"{delay(700)}>{T("bodym", "Read the case", 56, 372, 18, t["metal"])}'
                 f'<path d="M{56+text_width("bodym", "Read the case", 18)+10:.1f},366 h16 m-6,-6 l6,6 l-6,6" fill="none" stroke="{t["metal"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>')
    parts.append(f'<g class="grow"{delay(150)}><g clip-path="url(#f)"><image href="{uri}" x="{fx}" y="{fy}" width="{fw}" height="{fh}" preserveAspectRatio="xMidYMin slice"/></g>'
                 f'<rect x="{fx+.5}" y="{fy+.5}" width="{fw-1}" height="{fh-1}" rx="14" fill="none" stroke="{t["line"]}"/></g>')
    return svg(h, "".join(parts), t, "", f"{name}. {meta.replace('  ·  ', ', ')}. " + ". ".join(stats) + ".")


STACK = [
    ("Frontend", [("react", "React"), ("nextdotjs", "Next.js"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind")]),
    ("Backend and data", [("nodedotjs", "Node.js"), ("express", "Express"), ("python", "Python"), ("postgresql", "Postgres"), ("supabase", "Supabase"), ("redis", "Redis")]),
    ("Ship", [("git", "Git"), ("githubactions", "Actions"), ("vercel", "Vercel"), ("railway", "Railway"), ("linux", "Linux")]),
    ("AI engineering", [("claude", "Claude Code")]),
]


def icon_path(slug):
    s = (HERE / "icons" / f"{slug}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', s).group(1)


def stack(t):
    top, row = 118, 112
    h = top + row * len(STACK) + 12
    parts = [f'<g class="rise">{T("disp", "Stack", 56, 66, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Frontend first, with the systems underneath.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>']
    for r, (group, items) in enumerate(STACK):
        y = top + r * row
        parts.append(f'<g class="rise"{delay(250+r*140)}>')
        parts.append(T("smcp", group, 56, y + 44, 17, t["muted"], spacing=2.2))
        for i, (slug, label) in enumerate(items):
            x = 330 + i * 136
            parts.append(f'<g transform="translate({x},{y+10}) scale({42/24})"><path d="{icon_path(slug)}" fill="{t["metal"]}"/></g>')
            parts.append(T("body", label, x + 21, y + 84, 15, t["ink2"], anchor="middle"))
        parts.append("</g>")
        if r < len(STACK) - 1:
            parts.append(f'<line x1="56" y1="{y+row-6}" x2="{W-56}" y2="{y+row-6}" stroke="{t["line"]}"/>')
    names = "; ".join(f"{g}: " + ", ".join(l for _, l in items) for g, items in STACK)
    return svg(h, "".join(parts), t, "", f"Stack. {names}.")


def footer(t):
    h = 250
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 160)
    line = "Build it. Break it. Prove it."
    size = 50
    lw = text_width("ital", line, size)
    band = (f'<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{t["metal"]}"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></linearGradient>')
    USED["ital"].update(line)
    body = f"""<defs>{band}<mask id="tm" mask-type="alpha"><text x="{W/2}" y="160" font-family="ital" font-size="{size}" text-anchor="middle">{escape(line)}</text></mask></defs>
<g class="grow"><image href="{crest}" x="{W/2-34}" y="40" width="68" height="{68*ch/cw:.1f}"/></g>
<g class="rise"{delay(200)}>{T("ital", line, W/2, 160, size, t["ink"], anchor="middle")}</g>
<g mask="url(#tm)"><rect class="sweep" x="{W/2-lw/2-240}" y="110" width="240" height="70" fill="url(#band)"{delay(1100)}/></g>
<g class="fade"{delay(500)}>{T("smcp", "Product of Atilla Dev", W/2, 208, 16, t["muted"], anchor="middle", spacing=2.6)}</g>"""
    return svg(h, body, t, "", "Build it. Break it. Prove it. Product of Atilla Dev.")


# ── Fonts and output ────────────────────────────────────────────────────────

def font_css(used_fonts):
    rules = []
    for key in used_fonts:
        chars = USED[key]
        if not chars:
            continue
        tt = TTFont(HERE / "fonts" / FONTS[key])
        opts = Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        sub = Subsetter(opts)
        sub.populate(text="".join(chars))
        sub.subset(tt)
        buf = io.BytesIO()
        tt.flavor = "woff2"
        tt.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:{key};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(rules)


def main():
    OUT.mkdir(exist_ok=True)
    built = {}
    for theme, t in THEMES.items():
        built[f"hero-{theme}"] = hero(t)
        built[f"evidence-{theme}"] = evidence(t)
        built[f"work-{theme}"] = section_title(t, "Selected work", "Each card opens its case study.")
        for slug, name, meta, stats, shot in PROJECTS:
            built[f"card-{slug}-{theme}"] = card(t, slug, name, meta, stats, shot)
        built[f"stack-{theme}"] = stack(t)
        built[f"footer-{theme}"] = footer(t)
    for name, s in built.items():
        fams = [k for k in FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", font_css(fams))
        (OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
