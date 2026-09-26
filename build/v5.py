"""Version five: a wide cinematic banner, short strips, a tile grid and a side by side
close, so the profile scrolls about half as far. Reuses the helpers in make.py and
max.py.

    python v5.py        # writes ../assets/*.svg
"""

import math
import random

import make as m
import max as mx
import seal
from make import BRAND, THEMES, T, W, delay, img_uri, rule, star, text_width
from max import LOOPS, frame, loop_rot, odometer, shine_band

random.seed(11)

# Where the ring's centre sits inside each trimmed crest image (measured from the side
# spikes, which the gold file's outer glow would otherwise pull off centre).
CREST_CENTRE = {"gold": (0.465, 0.493), "black": (0.500, 0.495)}


def crest_at(t, cx, cy, height, width_px=520):
    uri, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", width_px)
    w = cw * height / ch
    fx, fy = CREST_CENTRE[t["tone"]]
    return uri, cx - fx * w, cy - fy * height, w


def comet(cx, cy, r, span, width, color, head_color, head):
    segs, n = [], 40
    for k in range(n):
        a0, a1 = math.radians(-90 - span * k / n), math.radians(-90 - span * (k + 1) / n)
        fade = (1 - k / n) ** 1.6
        segs.append(f'<path d="M{cx+r*math.cos(a0):.1f},{cy+r*math.sin(a0):.1f} A{r},{r} 0 0 0 {cx+r*math.cos(a1):.1f},{cy+r*math.sin(a1):.1f}"'
                    f' stroke="{color}" stroke-opacity="{fade:.3f}" stroke-width="{max(width*fade,0.6):.2f}" fill="none" stroke-linecap="round"/>')
    segs.append(f'<circle cx="{cx}" cy="{cy-r}" r="{head}" fill="{head_color}"/>')
    return "".join(segs)


def embers(n, x0, x1, y0, y1, color, rise=240):
    out = []
    for _ in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.1,2.6):.2f}" fill="{color}" opacity="0"'
                   f' style="--dx:{random.uniform(-60,60):.0f}px;--rise:-{rise}px;animation:ember {random.uniform(4.5,9):.1f}s cubic-bezier(.2,.6,.4,1) {random.uniform(0,8):.1f}s infinite"/>')
    return "".join(out)


BLOOM = ('<filter id="bloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
EMBER_CSS = "@keyframes ember{0%{opacity:0;transform:translate(0,0) scale(1)}12%{opacity:1}100%{opacity:0;transform:translate(var(--dx),var(--rise)) scale(.3)}}"


# ── Banner ──────────────────────────────────────────────────────────────────

TAGLINES = ["Frontend first. Built to be hard to break.",
            "Interfaces that feel instant on any phone.",
            "Payments that never charge twice.",
            "Every build attacked before it ships."]


def banner(t):
    h = 540
    cx, cy = 300, 270
    uri, ix, iy, iw = crest_at(t, cx, cy, 214)
    x0 = 590
    impact = 900  # ms: the moment the name lands

    rays = "".join(f'<line x1="{cx+200*math.cos(math.radians(a)):.1f}" y1="{cy+200*math.sin(math.radians(a)):.1f}" '
                   f'x2="{cx+(700 if a % 12 == 0 else 460)*math.cos(math.radians(a)):.1f}" y2="{cy+(700 if a % 12 == 0 else 460)*math.sin(math.radians(a)):.1f}"/>'
                   for a in range(0, 360, 6))
    ticks = []
    for i in range(120):
        a = math.radians(i * 3 - 90)
        long_ = i % 10 == 0
        r1, r2 = (152, 170) if long_ else (159, 166)
        ticks.append(f'<line x1="{cx+r1*math.cos(a):.1f}" y1="{cy+r1*math.sin(a):.1f}" x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}"'
                     f'{" stroke-width=\"1.7\"" if long_ else ""}/>')
    speed = "".join(f'<line x1="{cx+190*math.cos(math.radians(a)):.1f}" y1="{cy+190*math.sin(math.radians(a)):.1f}" '
                    f'x2="{cx+(380+(a*37)%140)*math.cos(math.radians(a)):.1f}" y2="{cy+(380+(a*37)%140)*math.sin(math.radians(a)):.1f}"/>'
                    for a in range(0, 360, 9))

    # The name: two words that slam down, each with a white flash of itself.
    words = [("Prince Newson", 214, 0), ("Viala", 312, 140)]
    name_parts, css = [], []
    for k, (word, y, lag) in enumerate(words):
        size = m.fit("disp", word, 92, 1200 - x0 - 64)
        css.append(f".w{k}{{transform-box:fill-box;transform-origin:left bottom;animation:slam .55s cubic-bezier(.2,1.4,.4,1) {impact+lag}ms both}}"
                   f".wf{k}{{opacity:0;animation:wflash .7s ease-out {impact+lag+60}ms both}}")
        name_parts.append(f'<g class="w{k}">{T("disp", word, x0, y, size, t["ink"])}'
                          f'<g class="wf{k}">{T("disp", word, x0, y, size, t["sweep"])}</g></g>')
    css.append("@keyframes slam{0%{opacity:0;transform:scale(1.45) translateY(-18px)}55%{opacity:1}100%{opacity:1;transform:none}}"
               "@keyframes wflash{0%{opacity:.95}100%{opacity:0}}")

    # Taglines: a blade of light cuts across and the line is there behind it.
    ty, tsize, cycle = 388, 26, 20
    seg = 100 / len(TAGLINES)
    tag = []
    for i, line in enumerate(TAGLINES):
        tw = text_width("body", line, tsize)
        s0 = i * seg
        a, b, c, d = s0, s0 + seg * 0.16, s0 + seg * 0.84, s0 + seg * 0.97
        hold0 = max(a - 0.01, 0)
        css.append(
            f"@keyframes rv{i}{{0%,{hold0:.2f}%{{transform:scaleX(0)}}{a:.2f}%{{transform:scaleX(0);animation-timing-function:cubic-bezier(.7,0,.2,1)}}{b:.2f}%,100%{{transform:scaleX(1)}}}}"
            f"@keyframes bl{i}{{0%,{hold0:.2f}%{{opacity:0;transform:translateX(0)}}{a:.2f}%{{opacity:1;transform:translateX(0);animation-timing-function:cubic-bezier(.7,0,.2,1)}}"
            f"{b:.2f}%{{opacity:1;transform:translateX({tw+60:.0f}px)}}{b+1.5:.2f}%,100%{{opacity:0;transform:translateX({tw+60:.0f}px)}}}}"
            f"@keyframes ex{i}{{0%,{hold0:.2f}%{{opacity:0;transform:none}}{a:.2f}%{{opacity:1;transform:none}}{c:.2f}%{{opacity:1;transform:none}}"
            f"{d:.2f}%,100%{{opacity:0;transform:translateY(-14px)}}}}"
            f".rv{i}{{transform-box:fill-box;transform-origin:left;animation:rv{i} {cycle}s linear 1.9s infinite backwards}}"
            f".bl{i}{{opacity:0;animation:bl{i} {cycle}s linear 1.9s infinite backwards}}"
            f".ex{i}{{{'' if i == 0 else 'opacity:0;'}animation:ex{i} {cycle}s linear 1.9s infinite backwards}}")
        tag.append(f'<clipPath id="tc{i}"><rect class="rv{i}" x="{x0-4}" y="{ty-tsize-6}" width="{tw+12:.1f}" height="{tsize*1.6:.1f}"/></clipPath>'
                   f'<g class="ex{i}"><g clip-path="url(#tc{i})">{T("body", line, x0, ty, tsize, t["metal"])}</g></g>'
                   f'<g class="bl{i}"><g filter="url(#bloom)"><path d="M{x0-18},{ty+14} L{x0-4},{ty-tsize-16} L{x0},{ty-tsize-16} L{x0-14},{ty+14} Z" fill="{t["sweep"]}"/></g></g>')

    meta = "Full stack software engineer  ·  Open to relocation worldwide"
    css += [seal.spin("raysin", -12, cx, cy, 2400), seal.spin("dialin", 50, cx, cy, 2000),
            loop_rot("dialspin", cx, cy, 160), loop_rot("dashspin", cx, cy, 90, back=True),
            loop_rot("tr1", cx, cy, 5.5), loop_rot("tr2", cx, cy, 8, back=True),
            ".glow{animation:breathe 5s ease-in-out infinite}",
            ".crestshine{animation:shineloop 7s cubic-bezier(.45,0,.2,1) 1.4s infinite}",
            ".flash{opacity:0;transform-box:fill-box;transform-origin:center;animation:flash .9s cubic-bezier(.16,1,.3,1) .35s both}"
            "@keyframes flash{from{opacity:1;transform:scale(.5)}to{opacity:0;transform:scale(1.9)}}",
            f".speed{{opacity:0;transform-box:view-box;transform-origin:{cx}px {cy}px;animation:speed .7s cubic-bezier(.16,1,.3,1) .4s both}}"
            "@keyframes speed{from{opacity:.9;transform:scale(.7)}to{opacity:0;transform:scale(1.15)}}",
            f".wave{{opacity:0;transform-box:fill-box;transform-origin:left;animation:wave 1s cubic-bezier(.16,1,.3,1) {impact+80}ms both}}"
            "@keyframes wave{0%{opacity:1;transform:scaleX(0)}60%{opacity:1}100%{opacity:.0;transform:scaleX(1)}}",
            f".shake{{animation:shake .38s linear {impact}ms both}}"
            "@keyframes shake{0%,100%{transform:none}20%{transform:translate(-4px,2px)}40%{transform:translate(4px,-2px)}60%{transform:translate(-3px,-1px)}80%{transform:translate(2px,1px)}}",
            EMBER_CSS]

    corner = lambda x, y, sx, sy: f'<path d="M{x},{y+sy*22} V{y} H{x+sx*22}" fill="none" stroke="{t["hair"]}" stroke-width="1.2"/>'
    word = img_uri(BRAND / f"brand/wordmark-{t['tone']}.webp", 520)
    wuri, (ww, wh) = word
    body = f"""<defs>{BLOOM}
<radialGradient id="glow" cx="{cx/W:.3f}" cy=".5" r=".45"><stop offset="0" stop-color="{t['metal']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{t['metal']}" stop-opacity=".35"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<radialGradient id="rayfade" cx="{cx/W:.3f}" cy=".5" r=".5"><stop offset=".25" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="flashg"><stop offset="0" stop-color="{t['sweep']}" stop-opacity=".95"/><stop offset=".45" stop-color="{t['metal']}" stop-opacity=".45"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<linearGradient id="waveg" x1="0" x2="1"><stop offset="0" stop-color="{t['sweep']}"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></linearGradient>
{shine_band("band", t["sweep"], ".75")}
<clipPath id="panel"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="23"/></clipPath>
<mask id="rm"><rect width="{W}" height="{h}" fill="url(#rayfade)"/></mask>
<mask id="cm" mask-type="alpha"><image href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="214"/></mask>
</defs>
<g class="shake"><g clip-path="url(#panel)">
<rect width="{W}" height="{h}" fill="url(#glow)" class="fade"/>
<g mask="url(#rm)"><g class="raysin" stroke="{t['metal']}" stroke-opacity=".13">{rays}</g></g>
</g>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".5"/>
<g class="fade"{delay(900)}>{corner(34,34,1,1)}{corner(W-34,34,-1,1)}{corner(34,h-34,1,-1)}{corner(W-34,h-34,-1,-1)}</g>
<circle class="glow" cx="{cx}" cy="{cy}" r="160" fill="url(#halo)"/>
<g class="dialin" stroke="{t['metal']}" stroke-opacity=".7" fill="none">
  <g class="dialspin">{''.join(ticks)}</g>
  <circle cx="{cx}" cy="{cy}" r="180" stroke-opacity=".45"/>
  <g class="dashspin"><circle cx="{cx}" cy="{cy}" r="142" stroke-opacity=".35" stroke-dasharray="2 7"/></g>
</g>
<g class="fade"{delay(1500)} filter="url(#bloom)"><g class="tr1">{comet(cx, cy, 196, 150, 6, t['metal'], t['sweep'], 3)}</g>
<g class="tr2">{comet(cx, cy, 210, 110, 4, t['hair'], t['sweep'], 2.2)}</g></g>
<image class="grow" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="214"{delay(200)}/>
<g clip-path="url(#panel)"><circle class="flash" cx="{cx}" cy="{cy}" r="150" fill="url(#flashg)"/>
<g class="speed" stroke="{t['sweep']}" stroke-width="1.6" stroke-linecap="round">{speed}</g>
<g filter="url(#bloom)">{embers(30, 60, W-60, 300, h, t['metal'])}</g></g>
<g mask="url(#cm)"><rect class="crestshine" x="{ix-220:.1f}" y="{iy:.1f}" width="220" height="214" fill="url(#band)"/></g>
<g class="rise"{delay(500)}><image href="{wuri}" x="{x0-3}" y="84" width="{ww*34/wh:.1f}" height="34"/></g>
{''.join(name_parts)}
<rect class="wave" x="{x0}" y="338" width="{W-x0-70}" height="2" fill="url(#waveg)"/>
<g class="fade"{delay(1700)}>{''.join(tag)}</g>
<g class="fade"{delay(1300)}>{rule(x0, W-70, 430, t)}{T("smcp", meta, x0, 470, m.fit("smcp", meta, 18, W-x0-70, 2.4), t["muted"], spacing=2.4)}</g>
</g>"""
    return frame(h, body, t, "".join(css),
                 "Atilla Dev. Prince Newson Viala, full stack software engineer. " + " ".join(TAGLINES))


# ── Evidence strip ──────────────────────────────────────────────────────────

def evidence(t):
    h = 350
    top, bot, x0, x1 = 112, 322, 56, W - 56
    cols = [(x0, 380, "261", "tests on real Postgres", "Plutus", 132),
            (x0 + 380, 236, "7", "critical findings closed", "Yifan platform", 96),
            (x0 + 616, 236, "39/40", "on a design review", "Marissa", 84),
            (x0 + 852, 236, "9", "days to production", "Marissa", 96)]
    grid = "".join(f'<line x1="{x0+i*24}" y1="{top}" x2="{x0+i*24}" y2="{bot}"/>' for i in range(1, 16)) + \
           "".join(f'<line x1="{x0}" y1="{top+i*24}" x2="{x0+380}" y2="{top+i*24}"/>' for i in range(1, 8))
    css = [".gridshine{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 2.5s infinite}", ".glow{animation:breathe 6s ease-in-out infinite}"]
    parts = [
        f'<defs><radialGradient id="eg" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gf" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="gm"><rect x="{x0}" y="{top}" width="380" height="{bot-top}" fill="url(#gf)"/></mask>'
        f'<mask id="gl" mask-type="alpha"><g stroke="#000" stroke-width="1.4">{grid}</g></mask>' + shine_band("gs", t["sweep"], ".9") + '</defs>',
        f'<g class="rise">{m.T("disp", "Engineering evidence", 56, 64, 40, t["ink"])}</g>',
        f'<g class="fade"{delay(150)}>{T("body", "Each figure checked against the project’s own repository.", W-56, 64, 16, t["muted"], anchor="end")}{rule(56, W-56, 84, t)}</g>',
        f'<rect class="glow" x="{x0}" y="{top}" width="380" height="{bot-top}" fill="url(#eg)"/>',
        f'<g mask="url(#gm)" stroke="{t["metal"]}" stroke-opacity=".12" class="fade"{delay(200)}>{grid}</g>',
        f'<g mask="url(#gl)"><g mask="url(#gm)"><rect class="gridshine" x="{x0-300}" y="{top}" width="260" height="{bot-top}" fill="url(#gs)"/></g></g>']
    for i, (x, w, n, label, src, fs) in enumerate(cols):
        if i:
            parts.append(f'<line x1="{x}" y1="{top+10}" x2="{x}" y2="{bot-10}" stroke="{t["line"]}" class="fade"{delay(250+i*100)}/>')
        mid = x + w / 2
        base = top + 22 + fs * 0.66
        lab = bot - 44
        reel, rcss = odometer(n, mid, base, fs, t["metal"], i, 300 + i * 180)
        css.append(rcss)
        parts.append(reel)
        parts.append(f'<g class="rise"{delay(700+i*160)}>{T("body", label, mid, lab, 19, t["ink"], anchor="middle")}'
                     f'{T("bodym", src.upper(), mid, lab + 28, 14, t["ink2"], anchor="middle", spacing=2.6)}</g>')
    return frame(h, "".join(parts), t, "".join(css), "Engineering evidence: 261 tests on real Postgres in Plutus. 7 critical findings closed on the Yifan platform. 39 of 40 on a design review for Marissa. 9 days to production for Marissa.")


# ── How I build: three words that do what they say ─────────────────────────

def process(t):
    h = 350
    cols = [200, 600, 1000]
    wy, size = 214, 104
    css = []
    parts = [f'<defs>{BLOOM}<radialGradient id="seal"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".22"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient></defs>',
             f'<g class="rise">{T("disp", "How I build", 56, 64, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "The same three moves on every product.", W-56, 64, 16, t["muted"], anchor="end")}{rule(56, W-56, 84, t)}</g>']
    for i in (1, 2):
        parts.append(f'<line x1="{(cols[i-1]+cols[i])/2}" y1="130" x2="{(cols[i-1]+cols[i])/2}" y2="{h-40}" stroke="{t["line"]}"/>')

    # Build: the letters assemble one by one.
    wordw = text_width("ital", "Build.", size)
    x = cols[0] - wordw / 2
    for k, ch in enumerate("Build."):
        css.append(f".b{k}{{animation:assemble .7s cubic-bezier(.2,1.3,.4,1) {400+k*90}ms both}}")
        parts.append(f'<g class="b{k}">{T("ital", ch, x, wy, size, t["ink"])}</g>')
        x += text_width("ital", ch, size)
    css.append("@keyframes assemble{from{opacity:0;transform:translateY(40px) rotate(-8deg)}}")

    # Break: a blade cuts the word and the halves slide apart along the cut.
    bw = text_width("ital", "Break.", size)
    bx = cols[1] - bw / 2
    yl, yr = wy - size * 0.24, wy - size * 0.46
    cut_top = f"M{bx-20},{wy-size} L{bx+bw+20},{wy-size} L{bx+bw+20},{yr} L{bx-20},{yl} Z"
    cut_bot = f"M{bx-20},{yl} L{bx+bw+20},{yr} L{bx+bw+20},{wy+size*0.4} L{bx-20},{wy+size*0.4} Z"
    run, rise_ = bw + 40, yr - yl
    ln = math.hypot(run, rise_)
    dx, dy = 9 * run / ln, 9 * rise_ / ln
    parts.append(f'<clipPath id="ct"><path d="{cut_top}"/></clipPath><clipPath id="cb"><path d="{cut_bot}"/></clipPath>'
                 f'<g class="rise"{delay(700)}><g class="halfa"><g clip-path="url(#ct)">{T("ital", "Break.", bx, wy, size, t["ink"])}</g></g>'
                 f'<g class="halfb"><g clip-path="url(#cb)">{T("ital", "Break.", bx, wy, size, t["ink"])}</g></g></g>'
                 f'<g class="slash" filter="url(#bloom)"><line x1="{bx-30}" y1="{yl:.1f}" x2="{bx+bw+30}" y2="{yr:.1f}" stroke="{t["sweep"]}" stroke-width="3" stroke-linecap="round"/></g>')
    css.append(f".halfa{{transform:translate({dx:.1f}px,{dy:.1f}px);animation:ha 4s cubic-bezier(.2,1,.3,1) 1.3s infinite backwards}}"
               f".halfb{{transform:translate({-dx:.1f}px,{-dy:.1f}px);animation:hb 4s cubic-bezier(.2,1,.3,1) 1.3s infinite backwards}}"
               f"@keyframes ha{{0%,14%{{transform:none}}22%,88%{{transform:translate({dx:.1f}px,{dy:.1f}px)}}100%{{transform:none}}}}"
               f"@keyframes hb{{0%,14%{{transform:none}}22%,88%{{transform:translate({-dx:.1f}px,{-dy:.1f}px)}}100%{{transform:none}}}}"
               ".slash{opacity:0;transform-box:fill-box;transform-origin:left;animation:slash 4s cubic-bezier(.7,0,.2,1) 1.3s infinite backwards}"
               "@keyframes slash{0%,4%{opacity:0;transform:scaleX(0)}5%{opacity:1;transform:scaleX(0)}14%{opacity:1;transform:scaleX(1)}24%,100%{opacity:0;transform:scaleX(1)}}")

    # Prove: a seal stamps down behind the word.
    pw = text_width("ital", "Prove.", size)
    sx, sy = cols[2], wy - size * 0.32
    ring = "".join(f'<line x1="{sx+64*math.cos(math.radians(a)):.1f}" y1="{sy+64*math.sin(math.radians(a)):.1f}" x2="{sx+72*math.cos(math.radians(a)):.1f}" y2="{sy+72*math.sin(math.radians(a)):.1f}"/>' for a in range(0, 360, 10))
    parts.append(f'<g class="stamp"><circle cx="{sx}" cy="{sy:.1f}" r="84" fill="url(#seal)"/>'
                 f'<circle cx="{sx}" cy="{sy:.1f}" r="76" fill="none" stroke="{t["metal"]}" stroke-opacity=".55" stroke-width="1.5"/>'
                 f'<g stroke="{t["metal"]}" stroke-opacity=".5">{ring}</g>'
                 f'<circle cx="{sx}" cy="{sy:.1f}" r="60" fill="none" stroke="{t["metal"]}" stroke-opacity=".35" stroke-dasharray="2 5"/></g>'
                 f'<g class="rise"{delay(900)}>{T("ital", "Prove.", sx - pw / 2, wy, size, t["ink"])}</g>')
    css.append(".stamp{transform-box:fill-box;transform-origin:center;animation:stamp .6s cubic-bezier(.3,1.6,.5,1) 1.6s both}"
               "@keyframes stamp{from{opacity:0;transform:scale(1.8) rotate(-25deg)}}")

    notes = [["Owned end to end: interface,", "architecture, data, deployment."],
             ["Races, permissions, double charges", "and recovery paths, attacked first."],
             ["Tests on a real database, checked", "against what the system must do."]]
    for i, lines in enumerate(notes):
        parts.append(f'<g class="rise"{delay(1100+i*150)}>' + "".join(
            T("body", ln, cols[i], 266 + j * 25, 17, t["muted"], anchor="middle") for j, ln in enumerate(lines)) + "</g>")
    return frame(h, "".join(parts), t, "".join(css),
                 "How I build. Build: owned end to end. Break: races, permissions, double charges and recovery paths attacked first. Prove: tests on a real database.")


# ── Work: a strip title and four full image tiles ───────────────────────────

def work_title(t):
    h = 96
    body = (f'<g class="rise">{T("disp", "Selected work", 56, 62, 40, t["ink"])}</g>'
            f'<g class="fade"{delay(150)}>{T("body", "Four products, each owned end to end. Tap a tile for the case.", W-56, 62, 16, t["muted"], anchor="end")}{rule(56, W-56, 82, t)}</g>')
    return frame(h, body, t, "", "Selected work", panel=False)


TILES = [("marissa", "Marissa", "E-commerce", "630 tests  ·  Row locked reservations", "marissa-home.jpg"),
         ("yifan", "Yifan Travel", "Travel technology", "57,000+ lines  ·  Sole technical owner", "yifan-home.jpg"),
         ("plutus", "Plutus", "Financial infrastructure", "261 tests  ·  Hash chained journal", "plutus-home.png"),
         ("bubbles", "Bubbles", "Offline first app", "81 tests  ·  Works with no signal", "bubbles-home-halved.png")]


def tile(t, i, name, kind, stats, shot):
    w, h = 600, 420
    uri, _ = img_uri(BRAND / "work" / shot, 1000, "JPEG", 80)
    css = (f".kb{{transform-box:view-box;transform-origin:{300 + (i%2)*40}px 160px;animation:kb 16s ease-in-out {i*1.3:.1f}s infinite alternate}}"
           "@keyframes kb{from{transform:scale(1)}to{transform:scale(1.09)}}"
           f".tsh{{animation:shineloop 9s cubic-bezier(.45,0,.2,1) {2+i*1.7:.1f}s infinite}}"
           ".nudge{animation:nudge 2.8s ease-in-out 1.5s infinite}@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}")
    ground = t["bg"]
    body = f"""<defs><clipPath id="tc"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath>
<linearGradient id="veil" x1="0" y1="0" x2="0" y2="1"><stop offset=".25" stop-color="{ground}" stop-opacity="0"/><stop offset=".55" stop-color="{ground}" stop-opacity=".86"/><stop offset=".72" stop-color="{ground}" stop-opacity=".97"/><stop offset="1" stop-color="{ground}"/></linearGradient>
{shine_band("ts", t["sweep"], ".22")}</defs>
<g clip-path="url(#tc)">
<rect width="{w}" height="{h}" fill="{ground}"/>
<g class="fade"><g class="kb"><image href="{uri}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMinYMin slice"/></g></g>
<rect width="{w}" height="{h}" fill="url(#veil)"/>
<rect class="tsh" x="-300" y="-100" width="220" height="{h+200}" fill="url(#ts)" transform="rotate(18)"/>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="none" stroke="{t['hair']}" stroke-opacity=".8"/>
<g class="rise"{delay(250)}>{T("bodym", kind.upper(), 34, h-118, 15, t["metal"], spacing=2.6)}
{T("disp", name, 32, h-62, m.fit("disp", name, 60, w-150), t["ink"])}
{T("body", stats, 34, h-30, 18, t["ink2"])}</g>
<g class="rise"{delay(400)}><circle cx="{w-58}" cy="{h-66}" r="28" fill="{ground}" fill-opacity=".6" stroke="{t['metal']}" stroke-opacity=".8"/>
<path class="nudge" d="M{w-68},{h-66} h20 m-7,-7 l7,7 l-7,7" fill="none" stroke="{t['metal']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>"""
    return frame(h, body, t, css, f"{name}, {kind}. {stats.replace('  ·  ', '. ')}. Read the case.", panel=False, w=w)


# ── Close: the stack in orbit beside an open door ───────────────────────────

def stack_tile(t):
    w, h = 600, 560
    ox, oy = 300, 316
    radii, speeds = [86, 150, 214], [70, 110, 150]
    uri, ix, iy, iw = crest_at(t, ox, oy, 78, 240)
    css = ["".join(seal.spin(f"o{i}", d, ox, oy, 1700 + i * 250) for i, d in enumerate([-30, -18, -10])),
           ".glow{animation:breathe 5s ease-in-out infinite}"]
    parts = [f'<defs><radialGradient id="halo"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".35"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="sparkg"><stop offset="0" stop-color="{t["sweep"]}"/><stop offset=".35" stop-color="{t["metal"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient></defs>',
             f'<g class="rise">{T("disp", "Stack", 40, 70, 44, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Frontend first, systems underneath.", w-40, 70, 17, t["muted"], anchor="end")}</g>',
             f'<circle class="glow" cx="{ox}" cy="{oy}" r="100" fill="url(#halo)"/>',
             f'<g stroke="{t["line"]}" fill="none" class="fade"{delay(200)}>' + "".join(f'<circle cx="{ox}" cy="{oy}" r="{r}"/>' for r in radii) + "</g>"]
    for i, ((group, _, _, items), r) in enumerate(zip(seal.ORBITS, radii)):
        back = i % 2 == 1
        css.append(loop_rot(f"orb{i}", ox, oy, speeds[i], back=back))
        css.append(f".up{i}{{transform-box:fill-box;transform-origin:center;animation:{'spinloop' if back else 'spinback'} {speeds[i]}s linear infinite}}")
        g = [f'<g class="o{i}"{delay(250+i*200)}><g class="orb{i}">']
        if i == 2:
            g.append(f'<circle cx="{ox+r}" cy="{oy}" r="10" fill="url(#sparkg)"/>')
        for k, (slug, _) in enumerate(items):
            a = math.radians(-90 + (360 / len(items)) * k + i * 22)
            x, y = ox + r * math.cos(a), oy + r * math.sin(a)
            g.append(f'<g class="up{i}"><circle cx="{x:.1f}" cy="{y:.1f}" r="25" fill="{t["bg"]}" stroke="{t["hair"]}" stroke-opacity=".8"/>'
                     f'<g transform="translate({x-14:.1f},{y-14:.1f}) scale({28/24})"><path d="{m.icon_path(slug)}" fill="{t["metal"]}"/></g></g>')
        parts.append("".join(g) + "</g></g>")
    parts.append(f'<image class="grow" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="78"/>')
    names = "; ".join(f"{g}: " + ", ".join(l for _, l in items) for g, _, _, items in seal.ORBITS)
    return frame(h, "".join(parts), t, "".join(css), f"Stack. {names}.", w=w)


def contact_tile(t):
    w, h = 600, 560
    uri, ix, iy, iw = crest_at(t, 300, 150, 150, 320)
    lines = ["Open to frontend and", "product engineering roles."]
    css = [".crestshine{animation:shineloop 7s cubic-bezier(.45,0,.2,1) 1.4s infinite}",
           ".glow{animation:breathe 5s ease-in-out infinite}", EMBER_CSS,
           ".sweeploop{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 2.2s infinite}"]
    motto = "Build it. Break it. Prove it."
    mw = text_width("ital", motto, 40)
    m.USED["ital"].update(motto)
    parts = [f'<defs>{BLOOM}<radialGradient id="halo"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".3"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             + shine_band("band", t["sweep"], ".75") + shine_band("mb", t["metal"], "1") +
             f'<mask id="cm" mask-type="alpha"><image href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="150"/></mask>'
             f'<mask id="mm" mask-type="alpha"><text x="{w/2}" y="{h-86}" font-family="ital" font-size="40" text-anchor="middle">{motto}</text></mask>'
             f'<clipPath id="pc"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23"/></clipPath></defs>',
             f'<circle class="glow" cx="300" cy="150" r="130" fill="url(#halo)"/>',
             f'<g clip-path="url(#pc)" filter="url(#bloom)">{embers(16, 40, w-40, 200, h, t["metal"], 300)}</g>',
             f'<image class="grow" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="150"/>',
             f'<g mask="url(#cm)"><rect class="crestshine" x="{ix-200:.1f}" y="{iy:.1f}" width="200" height="150" fill="url(#band)"/></g>']
    for j, ln in enumerate(lines):
        parts.append(f'<g class="rise"{delay(300+j*120)}>{T("disp", ln, w/2, 300 + j*48, 40, t["ink"], anchor="middle")}</g>')
    parts.append(f'<g class="rise"{delay(560)}>{T("body", "Remote, or relocating anywhere in the world.", w/2, 396, 18, t["muted"], anchor="middle")}</g>')
    parts.append(f'<g class="fade"{delay(700)}>{rule(150, w-150, 432, t)}</g>')
    parts.append(f'<g class="rise"{delay(800)}>{T("ital", motto, w/2, h-86, 40, t["ink"], anchor="middle")}</g>'
                 f'<g mask="url(#mm)"><rect class="sweeploop" x="{w/2-mw/2-240:.1f}" y="{h-140}" width="240" height="70" fill="url(#mb)"/></g>'
                 f'<g class="fade"{delay(1000)}>{T("smcp", "Product of Atilla Dev", w/2, h-44, 16, t["muted"], anchor="middle", spacing=2.6)}</g>')
    return frame(h, "".join(parts), t, "".join(css), "Open to frontend and product engineering roles. Remote, or relocating anywhere in the world. Build it. Break it. Prove it.", w=w)


def main():
    m.OUT.mkdir(exist_ok=True)
    for old in m.OUT.glob("*.svg"):
        old.unlink()
    built = {}
    for theme, t in THEMES.items():
        built[f"banner-{theme}"] = banner(t)
        built[f"ticker-{theme}"] = mx.ticker(t)
        for label, primary, dl in [("Portfolio", True, 2.0), ("Resume", False, 2.4), ("Email", False, 2.8)]:
            built[f"btn-{label.lower()}-{theme}"] = mx.button(t, label, primary, dl)
        built[f"evidence-{theme}"] = evidence(t)
        built[f"process-{theme}"] = process(t)
        built[f"work-{theme}"] = work_title(t)
        for i, (slug, name, kind, stats, shot) in enumerate(TILES):
            built[f"tile-{slug}-{theme}"] = tile(t, i, name, kind, stats, shot)
        built[f"stack-{theme}"] = stack_tile(t)
        built[f"contact-{theme}"] = contact_tile(t)
    for name, s in built.items():
        fams = [k for k in m.FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", m.font_css(fams))
        (m.OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
