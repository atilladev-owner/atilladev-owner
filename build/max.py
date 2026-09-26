"""The full power layout. Every section keeps a slow ambient motion after it arrives;
all of it is transform and opacity, and all of it stops under prefers-reduced-motion,
where each element rests in its finished state.

    python max.py        # writes ../assets/*.svg
"""

import math
import random

import make as m
import seal
from make import BRAND, THEMES, T, W, delay, escape, fit, img_uri, rule, star, text_width

random.seed(7)

LOOPS = """
@keyframes spinloop{to{transform:rotate(360deg)}}
@keyframes spinback{to{transform:rotate(-360deg)}}
@keyframes breathe{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
@keyframes mote{0%{opacity:0;transform:translate(0,0)}15%{opacity:.9}100%{opacity:0;transform:translate(var(--dx),-150px)}}
@keyframes shineloop{0%{transform:translateX(-600px)}28%,100%{transform:translateX(1500px)}}
"""


def frame(h, body, t, css="", title="", panel=True, w=W):
    ground = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>'
              if panel else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"'
            f' role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>/*FONTS*/{m.MOTION}{LOOPS}{css}</style>{ground}{body}</svg>')


def loop_rot(cls, ox, oy, secs, back=False, box="view-box"):
    origin = f"{ox}px {oy}px" if box == "view-box" else "center"
    return (f".{cls}{{transform-box:{box};transform-origin:{origin};"
            f"animation:{'spinback' if back else 'spinloop'} {secs}s linear infinite}}")


def motes(n, x0, x1, y0, y1, color, r=(0.8, 2.2)):
    out = []
    for i in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        dur, dl = random.uniform(7, 13), random.uniform(0, 9)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(*r):.2f}" fill="{color}" opacity=".45"'
                   f' style="--dx:{random.uniform(-30,30):.0f}px;animation:mote {dur:.1f}s linear {dl:.1f}s infinite"/>')
    return "".join(out)


def shine_band(gid, color, peak=".7"):
    return (f'<linearGradient id="{gid}" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{color}" stop-opacity="{peak}"/>'
            f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>')


# ── Hero ────────────────────────────────────────────────────────────────────

LINES = ["Frontend first. Built to be hard to break.",
         "Interfaces that feel instant on any phone.",
         "Payments that never charge twice.",
         "Every build attacked before it ships."]


def hero(t):
    h, cx, cy = 720, W / 2, 300
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 600)
    size = 280
    crest_w = cw * size / ch

    rays = []
    for i in range(60):
        a = math.radians(i * 6)
        r2 = 640 if i % 2 == 0 else 440
        rays.append(f'<line x1="{cx+222*math.cos(a):.1f}" y1="{cy+222*math.sin(a):.1f}" '
                    f'x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}"/>')
    ticks = []
    for i in range(120):
        a = math.radians(i * 3 - 90)
        long_ = i % 10 == 0
        r1, r2 = (190, 210) if long_ else (198, 206)
        ticks.append(f'<line x1="{cx+r1*math.cos(a):.1f}" y1="{cy+r1*math.sin(a):.1f}" '
                     f'x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}"'
                     f'{" stroke-width=\"1.7\"" if long_ else ""}/>')

    # Name: each letter rises on its own beat.
    name, nsize, ny = "Prince Newson Viala", 76, 596
    nw = text_width("disp", name, nsize)
    x = cx - nw / 2
    letters = []
    for k, ch_ in enumerate(name):
        adv = text_width("disp", ch_, nsize)
        if ch_ != " ":
            letters.append(f'<g class="rise"{delay(700+k*38)}>{T("disp", ch_, x, ny, nsize, t["ink"])}</g>')
        x += adv

    # Tagline: four lines typed, held and cleared in turn, forever.
    ty, tsize, cycle = 640, 25, 18
    seg = 100 / len(LINES)
    css = [seal.spin("raysin", -12, cx, cy, 2400), seal.spin("dialin", 50, cx, cy, 2000),
           loop_rot("dialspin", cx, cy, 160), loop_rot("dashspin", cx, cy, 90, back=True),
           loop_rot("spark", cx, cy, 14), ".glow{animation:breathe 5s ease-in-out infinite}",
           f".crestshine{{animation:shineloop 7s cubic-bezier(.45,0,.2,1) 1.2s infinite}}",
           ".blink{animation:blink 1s step-end infinite}@keyframes blink{50%{opacity:0}}"]
    tag = []
    for i, line in enumerate(LINES):
        n = len(line)
        tw = text_width("body", line, tsize)
        tx = cx - tw / 2
        s0, s1, s2, s3 = i * seg, i * seg + seg * .38, i * seg + seg * .88, i * seg + seg * .97
        first = i == 0
        css.append(
            f"@keyframes ty{i}{{0%{{transform:scaleX(0)}}{s0:.2f}%{{transform:scaleX(0);animation-timing-function:steps({n})}}"
            f"{s1:.2f}%,100%{{transform:scaleX(1)}}}}"
            f"@keyframes cr{i}{{0%{{transform:translateX(-{tw:.1f}px)}}{s0:.2f}%{{transform:translateX(-{tw:.1f}px);animation-timing-function:steps({n})}}"
            f"{s1:.2f}%,100%{{transform:translateX(0)}}}}"
            f"@keyframes op{i}{{0%{{opacity:0}}{max(s0-0.01,0):.2f}%{{opacity:0}}{s0:.2f}%{{opacity:1}}{s2:.2f}%{{opacity:1}}{s3:.2f}%,100%{{opacity:0}}}}"
            f".ty{i}{{transform-box:fill-box;transform-origin:left;animation:ty{i} {cycle}s linear 1.6s infinite backwards}}"
            f".cr{i}{{animation:cr{i} {cycle}s linear 1.6s infinite backwards}}"
            f".op{i}{{{'' if first else 'opacity:0;'}animation:op{i} {cycle}s linear 1.6s infinite backwards}}")
        tag.append(f'<clipPath id="tc{i}"><rect class="ty{i}" x="{tx:.1f}" y="{ty-tsize}" width="{tw+4:.1f}" height="{tsize*1.45:.1f}"/></clipPath>'
                   f'<g class="op{i}"><g clip-path="url(#tc{i})">{T("body", line, tx, ty, tsize, t["metal"])}</g>'
                   f'<g class="cr{i}"><rect class="blink" x="{tx+tw+3:.1f}" y="{ty-tsize*0.8:.1f}" width="2.5" height="{tsize*0.95:.1f}" fill="{t["metal"]}"/></g></g>')

    def corner(x, y, sx, sy):
        return f'<path d="M{x},{y+sy*22} V{y} H{x+sx*22}" fill="none" stroke="{t["hair"]}" stroke-width="1.2"/>'

    corners = [T("smcp", "Atilla Dev", 62, 66, 16, t["ink2"], spacing=3),
               T("smcp", "Est. 2023", W - 62, 66, 16, t["ink2"], anchor="end", spacing=3),
               T("body", "5.6037° N   0.1870° W", 62, h - 52, 14, t["muted"], spacing=1.6),
               T("body", "ACCRA  ·  GMT", W - 62, h - 52, 14, t["muted"], anchor="end", spacing=1.6)]
    defs = (f'<radialGradient id="glow" cx=".5" cy="{cy/h:.3f}" r=".5"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="rayfade" cx=".5" cy="{cy/h:.3f}" r=".55"><stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="sparkg"><stop offset="0" stop-color="{t["sweep"]}"/><stop offset=".35" stop-color="{t["metal"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            + shine_band("band", t["sweep"], ".75"))
    udefs, under, over, ucss = ufotable(t, cx, cy)
    css.append(ucss)
    body = f"""<defs>{defs}{udefs}
<clipPath id="panel"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="23"/></clipPath>
<mask id="rm"><rect width="{W}" height="{h}" fill="url(#rayfade)"/></mask>
<mask id="cm" mask-type="alpha"><image href="{crest}" x="{cx-crest_w/2:.1f}" y="{cy-size/2}" width="{crest_w:.1f}" height="{size}"/></mask>
{''.join(tag[:0])}</defs>
<g clip-path="url(#panel)">
<rect width="{W}" height="{h}" fill="url(#glow)" class="fade"/>
<g mask="url(#rm)"><g class="raysin" stroke="{t['metal']}" stroke-opacity=".13">{''.join(rays)}</g></g>
</g>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".5"/>
<circle class="glow" cx="{cx}" cy="{cy}" r="200" fill="url(#halo)"/>
<g class="dialin" stroke="{t['metal']}" stroke-opacity=".7" fill="none">
  <g class="dialspin">{''.join(ticks)}</g>
  <circle cx="{cx}" cy="{cy}" r="222" stroke-opacity=".45"/>
  <g class="dashspin"><circle cx="{cx}" cy="{cy}" r="180" stroke-opacity=".35" stroke-dasharray="2 7"/></g>
</g>
<g class="fade"{delay(1800)}><g class="spark"><circle cx="{cx}" cy="{cy-222}" r="11" fill="url(#sparkg)"/></g></g>
{under}
<image class="grow" href="{crest}" x="{cx-crest_w/2:.1f}" y="{cy-size/2}" width="{crest_w:.1f}" height="{size}"{delay(200)}/>
<g clip-path="url(#panel)">{over}</g>
<g mask="url(#cm)"><rect class="crestshine" x="{cx-crest_w/2-220:.1f}" y="{cy-size/2}" width="220" height="{size}" fill="url(#band)"/></g>
{''.join(letters)}
<g class="fade"{delay(1500)}>{''.join(tag)}</g>
<g class="fade"{delay(1000)}>{''.join(corners)}{corner(34,34,1,1)}{corner(W-34,34,-1,1)}{corner(34,h-34,1,-1)}{corner(W-34,h-34,-1,-1)}</g>"""
    return frame(h, body, t, "".join(css),
                 "Atilla Dev. Prince Newson Viala, full stack software engineer in Accra, Ghana. " + " ".join(LINES))


def ufotable(t, cx, cy):
    """Breathing style light: two comet trails chasing round the crest, an impact flash
    with speed lines as the crest lands, and embers with bloom. Returns defs, the layer
    under the crest, the layer over it, and its CSS."""
    defs = ('<filter id="bloom" x="-30%" y="-30%" width="160%" height="160%">'
            '<feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
            '<feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<radialGradient id="flash"><stop offset="0" stop-color="{t["sweep"]}" stop-opacity=".95"/>'
            f'<stop offset=".45" stop-color="{t["metal"]}" stop-opacity=".45"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>')

    def trail(r, span, width, color, head):
        segs, n = [], 44
        for k in range(n):
            a0 = math.radians(-90 - span * k / n)
            a1 = math.radians(-90 - span * (k + 1) / n)
            fade = (1 - k / n) ** 1.6
            segs.append(f'<path d="M{cx+r*math.cos(a0):.1f},{cy+r*math.sin(a0):.1f} A{r},{r} 0 0 0 {cx+r*math.cos(a1):.1f},{cy+r*math.sin(a1):.1f}"'
                        f' stroke="{color}" stroke-opacity="{fade:.3f}" stroke-width="{max(width*fade,0.6):.2f}" fill="none" stroke-linecap="round"/>')
        segs.append(f'<circle cx="{cx}" cy="{cy-r}" r="{head}" fill="{t["sweep"]}"/>')
        return "".join(segs)

    under = (f'<g class="fade"{delay(1500)} filter="url(#bloom)">'
             f'<g class="tr1">{trail(238, 150, 7, t["metal"], 3.2)}</g>'
             f'<g class="tr2">{trail(254, 110, 4.5, t["hair"], 2.4)}</g></g>')
    lines = "".join(f'<line x1="{cx+232*math.cos(math.radians(a)):.1f}" y1="{cy+232*math.sin(math.radians(a)):.1f}" '
                    f'x2="{cx+(470+(a*37)%160)*math.cos(math.radians(a)):.1f}" y2="{cy+(470+(a*37)%160)*math.sin(math.radians(a)):.1f}"/>'
                    for a in range(0, 360, 9))
    over = (f'<circle class="flash" cx="{cx}" cy="{cy}" r="190" fill="url(#flash)"/>'
            f'<g class="speed" stroke="{t["sweep"]}" stroke-width="1.6" stroke-linecap="round">{lines}</g>')
    embers = []
    for i in range(34):
        x, y = random.uniform(80, W - 80), random.uniform(380, 700)
        dur, dl = random.uniform(4.5, 9), random.uniform(0, 8)
        embers.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.2,2.8):.2f}" fill="{t["metal"]}" opacity="0"'
                      f' style="--dx:{random.uniform(-60,60):.0f}px;animation:ember {dur:.1f}s cubic-bezier(.2,.6,.4,1) {dl:.1f}s infinite"/>')
    over += f'<g filter="url(#bloom)">{"".join(embers)}</g>'
    css = (loop_rot("tr1", cx, cy, 5.5) + loop_rot("tr2", cx, cy, 8, back=True) +
           ".flash{opacity:0;transform-box:fill-box;transform-origin:center;animation:flash .9s cubic-bezier(.16,1,.3,1) .35s both}"
           "@keyframes flash{from{opacity:1;transform:scale(.5)}to{opacity:0;transform:scale(1.9)}}"
           f".speed{{opacity:0;transform-box:view-box;transform-origin:{cx}px {cy}px;animation:speed .7s cubic-bezier(.16,1,.3,1) .4s both}}"
           "@keyframes speed{from{opacity:.9;transform:scale(.7)}to{opacity:0;transform:scale(1.15)}}"
           "@keyframes ember{0%{opacity:0;transform:translate(0,0) scale(1)}12%{opacity:1}100%{opacity:0;transform:translate(var(--dx),-260px) scale(.3)}}")
    return defs, under, over, css


# ── Ticker ──────────────────────────────────────────────────────────────────

TICKER = ["Interface first", "Built to be hard to break", "Row locked", "Hash chained", "Offline first",
          "Attacked before it ships", "Accra, Ghana", "Open to relocation"]


def ticker(t):
    h, size, gap = 76, 21, 64
    items, x = [], 0.0
    for word in TICKER:
        items.append(T("smcp", word, x, 47, size, t["ink2"], spacing=2.6))
        x += text_width("smcp", word, size, 2.6) + gap / 2
        items.append(star(x, 40, 6, t["metal"]))
        x += gap / 2
    seg = x
    reps = math.ceil(W / seg) + 1
    row = "".join(f'<g transform="translate({seg*r:.1f} 0)">{"".join(items)}</g>' for r in range(reps))
    css = f".run{{animation:run {seg/60:.1f}s linear infinite}}@keyframes run{{to{{transform:translateX(-{seg:.1f}px)}}}}"
    body = (f'<defs><linearGradient id="ef" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="edge"><rect width="{W}" height="{h}" fill="url(#ef)"/></mask></defs>'
            f'<line x1="0" y1=".5" x2="{W}" y2=".5" stroke="{t["hair"]}" stroke-opacity=".6"/>'
            f'<line x1="0" y1="{h-.5}" x2="{W}" y2="{h-.5}" stroke="{t["hair"]}" stroke-opacity=".6"/>'
            f'<g mask="url(#edge)"><g class="run">{row}</g></g>')
    return frame(h, body, t, css, " · ".join(TICKER), panel=False)


# ── Buttons ─────────────────────────────────────────────────────────────────

def button(t, label, primary, dl):
    w, h = 384, 92
    fill = t["metal"] if primary else "none"
    ink = t["bg"] if primary else t["ink"]
    lw = text_width("bodym", label, 24)
    x = (w - lw - 34) / 2
    body = (f'<defs>{shine_band("b", t["sweep"], ".55" if primary else ".22")}'
            f'<clipPath id="bc"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14"/></clipPath></defs>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{fill}" stroke="{t["metal"]}" stroke-width="1.5"/>'
            f'<g clip-path="url(#bc)"><rect class="bs" x="-200" y="0" width="180" height="{h}" fill="url(#b)"/></g>'
            f'{T("bodym", label, x, 55, 24, ink)}'
            f'<path d="M{x+lw+14:.1f},47 h18 m-7,-7 l7,7 l-7,7" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    css = f".bs{{animation:shineb 6s cubic-bezier(.45,0,.2,1) {dl}s infinite}}@keyframes shineb{{0%{{transform:translateX(0)}}30%,100%{{transform:translateX(640px)}}}}"
    return frame(h, body, t, css, label, panel=False, w=w)


# ── Evidence: the figures roll in like an odometer ─────────────────────────

def odometer(n, cx, base, fs, color, idx, dl):
    """Each digit is a reel of 0 to 9, twice, that spins down to its value."""
    L = fs * 1.15
    widths = [text_width("disp", c, fs) for c in n]
    x = cx - sum(widths) / 2
    out, css = [], []
    for k, (c, wd) in enumerate(zip(n, widths)):
        if c.isdigit():
            d = int(c)
            final = -(10 + d) * L
            cid = f"r{idx}_{k}"
            reel = "".join(T("disp", str(j % 10), x + wd / 2, base + j * L, fs, color, anchor="middle") for j in range(20))
            dur = 1.5 + k * 0.28
            css.append(f".{cid}{{transform:translateY({final:.1f}px);animation:{cid} {dur:.2f}s cubic-bezier(.16,1,.3,1) {dl}ms both}}"
                       f"@keyframes {cid}{{from{{transform:translateY(0)}}}}")
            out.append(f'<clipPath id="c{cid}"><rect x="{x-6:.1f}" y="{base-fs*0.8:.1f}" width="{wd+12:.1f}" height="{fs*1.08:.1f}"/></clipPath>'
                       f'<g clip-path="url(#c{cid})"><g class="{cid}">{reel}</g></g>')
        else:
            out.append(f'<g class="fade"{delay(dl)}>{T("disp", c, x, base, fs, color)}</g>')
        x += wd
    return "".join(out), "".join(css)


def evidence(t):
    h = 580
    top, bot, x0, x1, xm = 116, 540, 56, W - 56, 600
    ym, xs = (top + bot) / 2, (xm + x1) / 2
    cells = [(x0, top, xm - x0, bot - top, "261", "tests on real Postgres", "Plutus", 210),
             (xm, top, x1 - xm, ym - top, "7", "critical findings closed", "Yifan platform", 110),
             (xm, ym, xs - xm, bot - ym, "39/40", "on a design review", "Marissa", 92),
             (xs, ym, x1 - xs, bot - ym, "9", "days to production", "Marissa", 92)]
    grid = "".join(f'<line x1="{x0+i*24}" y1="{top}" x2="{x0+i*24}" y2="{bot}"/>' for i in range(1, 23)) + \
           "".join(f'<line x1="{x0}" y1="{top+i*24}" x2="{xm}" y2="{top+i*24}"/>' for i in range(1, 18))
    css = [".gridshine{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 2.5s infinite}", ".glow{animation:breathe 6s ease-in-out infinite}"]
    parts = [
        f'<defs><radialGradient id="eg" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
        f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gf" cx=".5" cy=".5" r=".55"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="gm"><rect x="{x0}" y="{top}" width="{xm-x0}" height="{bot-top}" fill="url(#gf)"/></mask>'
        f'<mask id="gl" mask-type="alpha"><g stroke="#000" stroke-width="1.4">{grid}</g></mask>'
        + shine_band("gs", t["sweep"], ".9") + '</defs>',
        f'<g class="rise">{T("disp", "Engineering evidence", 56, 66, 40, t["ink"])}</g>',
        f'<g class="fade"{delay(150)}>{T("body", "Each figure checked against the project’s own repository.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>',
        f'<rect class="glow" x="{x0}" y="{top}" width="{xm-x0}" height="{bot-top}" fill="url(#eg)"/>',
        f'<g mask="url(#gm)" stroke="{t["metal"]}" stroke-opacity=".12" class="fade"{delay(200)}>{grid}</g>',
        f'<g mask="url(#gl)"><g mask="url(#gm)"><rect class="gridshine" x="{x0-300}" y="{top}" width="260" height="{bot-top}" fill="url(#gs)"/></g></g>',
        f'<g stroke="{t["line"]}" class="fade"{delay(250)}><line x1="{xm}" y1="{top}" x2="{xm}" y2="{bot}"/>'
        f'<line x1="{xm}" y1="{ym}" x2="{x1}" y2="{ym}"/><line x1="{xs}" y1="{ym}" x2="{xs}" y2="{bot}"/>'
        f'<line x1="{x0}" y1="{bot}" x2="{x1}" y2="{bot}"/></g>']
    for i, (x, y, w, hh, n, label, src, fs) in enumerate(cells):
        mid = x + w / 2
        ls = 22 if i == 0 else 19
        tail = fs * 0.26
        block = fs * 0.70 + tail + 14 + ls + 16 + 14
        base = y + (hh - block) / 2 + fs * 0.70
        lab = base + tail + 14 + ls
        reel, rcss = odometer(n, mid, base, fs, t["metal"], i, 300 + i * 180)
        css.append(rcss)
        parts.append(reel)
        parts.append(f'<g class="rise"{delay(700+i*160)}>{T("body", label, mid, lab, ls, t["ink"], anchor="middle")}'
                     f'{T("bodym", src.upper(), mid, lab + 30, 14, t["ink2"], anchor="middle", spacing=2.6)}</g>')
    return frame(h, "".join(parts), t, "".join(css), "Engineering evidence: 261 tests on real Postgres in Plutus. 7 critical findings closed on the Yifan platform. 39 of 40 on a design review for Marissa. 9 days to production for Marissa.")


# ── How I build: three stations and a pulse between them ──────────────────

STEPS = [("Build it.", ["Products owned end to end:", "interface, architecture,", "database and deployment."]),
         ("Break it.", ["Concurrency, permissions,", "duplicate payments and recovery", "paths attacked before release."]),
         ("Prove it.", ["Tests against a real database,", "checked against what the", "system has to do."])]


def process(t):
    h, ny = 440, 196
    xs = [230, 600, 970]
    css = [".pulse{animation:pulse 4.5s cubic-bezier(.45,0,.55,1) 1.5s infinite}"
           f"@keyframes pulse{{0%{{opacity:0;transform:translateX(0)}}8%{{opacity:1}}92%{{opacity:1}}100%{{opacity:0;transform:translateX({xs[2]-xs[0]}px)}}}}"]
    parts = [f'<defs><radialGradient id="pg"><stop offset="0" stop-color="{t["sweep"]}"/><stop offset=".4" stop-color="{t["metal"]}" stop-opacity=".8"/>'
             f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="ng"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".28"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient></defs>',
             f'<g class="rise">{T("disp", "How I build", 56, 66, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "The same three moves on every product.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>',
             f'<line x1="{xs[0]}" y1="{ny}" x2="{xs[2]}" y2="{ny}" stroke="{t["hair"]}" stroke-dasharray="3 6" class="fade"{delay(300)}/>',
             f'<circle class="pulse" cx="{xs[0]}" cy="{ny}" r="14" fill="url(#pg)"/>']
    for i, (x, (title, lines)) in enumerate(zip(xs, STEPS)):
        css.append(f".n{i}{{transform-box:fill-box;transform-origin:center;animation:ring 4.5s ease-out {1.5+i*1.9:.2f}s infinite}}")
        parts.append(f'<g class="grow"{delay(250+i*180)}>'
                     f'<circle cx="{x}" cy="{ny}" r="74" fill="url(#ng)"/>'
                     f'<circle class="n{i}" cx="{x}" cy="{ny}" r="52" fill="none" stroke="{t["metal"]}" stroke-opacity=".5"/>'
                     f'<circle cx="{x}" cy="{ny}" r="46" fill="{t["bg"]}" stroke="{t["metal"]}" stroke-width="1.4"/>'
                     f'{star(x, ny, 18, t["metal"])}</g>')
        parts.append(f'<g class="rise"{delay(450+i*180)}>{T("disp", title, x, ny + 110, 38, t["ink"], anchor="middle")}'
                     + "".join(T("body", ln, x, ny + 146 + j * 24, 16, t["muted"], anchor="middle") for j, ln in enumerate(lines)) + "</g>")
    css.append("@keyframes ring{0%{opacity:.8;transform:scale(1)}70%,100%{opacity:0;transform:scale(1.45)}}")
    return frame(h, "".join(parts), t, "".join(css),
                 "How I build. " + " ".join(f"{a} {' '.join(b)}" for a, b in STEPS))


# ── Work: the spread, now floating, labelled and swept with light ──────────

def spread(t):
    h = 700
    sw, sh = 560, 306
    place = [(60, 250), (430, 222), (220, 420), (590, 392)]
    names = ["Marissa", "Yifan Travel", "Plutus", "Bubbles"]
    css = [".desk{animation:shineloop 9s cubic-bezier(.45,0,.2,1) 3s infinite}"]
    parts = [f'<g class="rise">{T("disp", "Selected work", 56, 66, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Four products, each owned end to end.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>',
             f'<defs><radialGradient id="sg" cx=".52" cy=".62" r=".55"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
             f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             f'<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="{t["shadow"]}" flood-opacity=".55"/></filter>'
             + shine_band("ds", t["sweep"], ".28") + '</defs>',
             f'<clipPath id="stage"><rect x="1" y="104" width="{W-2}" height="{h-105}"/></clipPath>',
             f'<rect x="1" y="100" width="{W-2}" height="{h-101}" fill="url(#sg)" class="fade"/>',
             f'<g clip-path="url(#stage)">{motes(14, 60, W-60, 380, h-30, t["metal"])}<g transform="translate(62 50) scale(0.88)">']
    labels = []
    for i, ((shot, _), (x, y)) in enumerate(zip(seal.SHOTS, place)):
        uri, _ = img_uri(BRAND / "work" / shot, 1120, "JPEG", 80)
        e, f = x + 140, y - 120
        css.append(f".fl{i}{{animation:floaty {6+i*0.7:.1f}s ease-in-out {i*0.9:.1f}s infinite}}")
        parts.append(
            f'<g class="rise"{delay(250+i*170)}><g class="fl{i}"><g transform="matrix(0.86 0.30 -0.62 0.62 {e} {f})" filter="url(#sh)">'
            f'<clipPath id="c{i}"><rect width="{sw}" height="{sh}" rx="12"/></clipPath>'
            f'<g clip-path="url(#c{i})"><image href="{uri}" width="{sw}" height="{sh}" preserveAspectRatio="xMidYMin slice"/>'
            f'<rect class="desk" x="-300" y="-200" width="260" height="{sh+400}" fill="url(#ds)" transform="rotate(20)"/></g>'
            f'<rect x=".5" y=".5" width="{sw-1}" height="{sh-1}" rx="12" fill="none" stroke="{t["hair"]}" stroke-opacity=".8"/></g></g></g>')
        # A tag pinned to the sheet's far corner, in page space.
        if i in (1, 3):
            px, py = 62 + 0.88 * (e + 0.86 * sw), 50 + 0.88 * (f + 0.30 * sw)
        else:
            px, py = 62 + 0.88 * (e - 0.62 * sh), 50 + 0.88 * (f + 0.62 * sh)
        labels.append((px, py, names[i], i))
    parts.append("</g></g>")
    for px, py, name, i in labels:
        if i in (1, 3):
            lx, ly, anchor = min(px + 18, W - 40), py - 26, "end" if px + 18 > W - 200 else "start"
        else:
            lx, ly, anchor = px + 8, py + 40, "start"
        parts.append(f'<g class="rise"{delay(900+i*150)}><g class="fl{i}">'
                     f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{t["metal"]}"/>'
                     f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx:.1f}" y2="{ly+(8 if anchor == "end" or i in (1, 3) else -18):.1f}" stroke="{t["metal"]}" stroke-opacity=".7"/>'
                     f'{T("smcp", name, lx - 4 if anchor == "end" else lx, ly, 17, t["ink"], anchor=anchor, spacing=2.2)}</g></g>')
    return frame(h, "".join(parts), t, "".join(css), "Selected work: Marissa, Yifan Travel, Plutus and Bubbles, their front pages floating above a desk.")


def index_row(t, name, kind, stats, last):
    s = seal.index_row(t, name, kind, stats, last)
    under = (f'<line class="draw" x1="0" y1="{131 if last else 1}" x2="{W}" y2="{131 if last else 1}" stroke="{t["metal"]}" stroke-width="1.4"/>')
    css = (".draw{transform-box:fill-box;transform-origin:left;animation:draw 1.4s cubic-bezier(.16,1,.3,1) .2s both}"
           "@keyframes draw{from{transform:scaleX(0)}}"
           ".nudge{animation:nudge 2.8s ease-in-out 1.5s infinite}@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}")
    s = s.replace("</style>", css + "</style>", 1)
    s = s.replace(f'<path d="M{W-44},66', f'<path class="nudge" d="M{W-44},66', 1)
    return s.replace("</svg>", under + "</svg>")


# ── Stack: orbits that never stop turning ──────────────────────────────────

def stack(t):
    h = 600
    ox, oy = 830, 300
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 220)
    speeds = [70, 110, 150]
    css = ["".join(seal.spin(f"o{i}", deg, ox, oy, 1700 + i * 250) for i, (_, _, deg, _) in enumerate(seal.ORBITS)),
           ".glow{animation:breathe 5s ease-in-out infinite}"]
    parts = [f'<defs><radialGradient id="halo"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".35"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="sparkg"><stop offset="0" stop-color="{t["sweep"]}"/><stop offset=".35" stop-color="{t["metal"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient></defs>',
             f'<g class="rise">{T("disp", "Stack", 56, 92, 48, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Frontend first, with the systems", 58, 128, 17, t["muted"])}'
             f'{T("body", "underneath it.", 58, 152, 17, t["muted"])}{rule(56, 480, 184, t)}</g>']
    y = 238
    for i, (group, _, _, items) in enumerate(seal.ORBITS):
        names, lines, cur = [l for _, l in items], [], ""
        for n in names:
            nxt = f"{cur}, {n}" if cur else n
            if text_width("body", nxt, 17) > 400:
                lines.append(cur + ",")
                cur = n
            else:
                cur = nxt
        lines.append(cur)
        block = f'<g class="rise"{delay(300+i*160)}>{T("bodym", group.upper(), 58, y, 13, t["metal"], spacing=2.6)}'
        block += "".join(T("body", ln, 58, y + 28 + j * 24, 17, t["ink2"]) for j, ln in enumerate(lines))
        parts.append(block + "</g>")
        y += 28 + len(lines) * 24 + 40
    parts.append(f'<circle class="glow" cx="{ox}" cy="{oy}" r="120" fill="url(#halo)"/>')
    parts.append(f'<g stroke="{t["line"]}" fill="none" class="fade"{delay(200)}>' +
                 "".join(f'<circle cx="{ox}" cy="{oy}" r="{r}"/>' for _, r, _, _ in seal.ORBITS) + "</g>")
    for i, (group, r, _, items) in enumerate(seal.ORBITS):
        back = i % 2 == 1
        css.append(loop_rot(f"orb{i}", ox, oy, speeds[i], back=back))
        g = [f'<g class="o{i}"{delay(250+i*200)}><g class="orb{i}">']
        if i == 2:
            g.append(f'<circle cx="{ox+r}" cy="{oy}" r="10" fill="url(#sparkg)"/>')
        for k, (slug, _) in enumerate(items):
            a = math.radians(-90 + (360 / len(items)) * k + i * 22)
            x, yy = ox + r * math.cos(a), oy + r * math.sin(a)
            cls = f"up{i}"
            g.append(f'<g class="{cls}"><circle cx="{x:.1f}" cy="{yy:.1f}" r="27" fill="{t["bg"]}" stroke="{t["hair"]}" stroke-opacity=".8"/>'
                     f'<g transform="translate({x-15:.1f},{yy-15:.1f}) scale({30/24})"><path d="{m.icon_path(slug)}" fill="{t["metal"]}"/></g></g>')
        css.append(f".up{i}{{transform-box:fill-box;transform-origin:center;animation:{'spinloop' if back else 'spinback'} {speeds[i]}s linear infinite}}")
        parts.append("".join(g) + "</g></g>")
    parts.append(f'<image class="grow" href="{crest}" x="{ox-46}" y="{oy-46*ch/cw:.1f}" width="92" height="{92*ch/cw:.1f}"/>')
    names = "; ".join(f"{g}: " + ", ".join(l for _, l in items) for g, _, _, items in seal.ORBITS)
    return frame(h, "".join(parts), t, "".join(css), f"Stack. {names}.")


def footer(t):
    s = m.footer(t)
    s = s.replace('class="sweep"', 'class="sweeploop"')
    css = ".sweeploop{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 1.2s infinite}" + LOOPS
    return s.replace("</style>", css + "</style>", 1)


def main():
    m.OUT.mkdir(exist_ok=True)
    for old in m.OUT.glob("*.svg"):
        old.unlink()
    built = {}
    for theme, t in THEMES.items():
        built[f"hero-{theme}"] = hero(t)
        built[f"ticker-{theme}"] = ticker(t)
        for label, primary, dl in [("Portfolio", True, 2.0), ("Resume", False, 2.4), ("Email", False, 2.8)]:
            built[f"btn-{label.lower()}-{theme}"] = button(t, label, primary, dl)
        built[f"evidence-{theme}"] = evidence(t)
        built[f"process-{theme}"] = process(t)
        built[f"work-{theme}"] = spread(t)
        for i, (name, kind, stats) in enumerate(seal.INDEX):
            built[f"row-{name.split()[0].lower()}-{theme}"] = index_row(t, name, kind, stats, i == len(seal.INDEX) - 1)
        built[f"stack-{theme}"] = stack(t)
        built[f"footer-{theme}"] = footer(t)
    for name, s in built.items():
        fams = [k for k in m.FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", m.font_css(fams))
        (m.OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
