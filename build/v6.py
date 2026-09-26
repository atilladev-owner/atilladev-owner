"""Version six: the profile carries the brand and nothing that pitches. The crest in its
dial from version four, the wordmark where the name was, and the stack in orbit.

    python v6.py        # writes ../assets/*.svg
"""

import math

import make as m
import max as mx
from make import BRAND, THEMES, W, delay, img_uri
from max import frame, loop_rot, shine_band
from v5 import crest_at


def crest_panel(t):
    h, cx, cy = 640, W / 2, 262
    size = 280
    uri, ix, iy, iw = crest_at(t, cx, cy, size, 600)
    wuri, (ww, wh) = img_uri(BRAND / f"brand/wordmark-{t['tone']}.webp", 900)
    word_h = 74
    word_w = ww * word_h / wh
    wx, wy = cx - word_w / 2, 530
    impact = 1100

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

    udefs, under, over, ucss = mx.ufotable(t, cx, cy)
    css = [mx.seal.spin("raysin", -12, cx, cy, 2400), mx.seal.spin("dialin", 50, cx, cy, 2000),
           loop_rot("dialspin", cx, cy, 160), loop_rot("dashspin", cx, cy, 90, back=True),
           loop_rot("spark", cx, cy, 14), ".glow{animation:breathe 5s ease-in-out infinite}",
           ".crestshine{animation:shineloop 7s cubic-bezier(.45,0,.2,1) 1.2s infinite}",
           ucss,
           # The wordmark lands where the name used to be: a slam, a flash of itself,
           # and a shockwave line; then light keeps passing across it.
           f".slam{{transform-box:fill-box;transform-origin:center;animation:slam .6s cubic-bezier(.2,1.4,.4,1) {impact}ms both}}"
           "@keyframes slam{0%{opacity:0;transform:scale(1.5)}55%{opacity:1}100%{opacity:1;transform:none}}"
           f".wflash{{opacity:0;animation:wflash .8s ease-out {impact+60}ms both}}@keyframes wflash{{0%{{opacity:.9}}100%{{opacity:0}}}}"
           f".wave{{opacity:0;transform-box:fill-box;transform-origin:center;animation:wave 1.1s cubic-bezier(.16,1,.3,1) {impact+80}ms both}}"
           "@keyframes wave{0%{opacity:1;transform:scaleX(0)}60%{opacity:1}100%{opacity:0;transform:scaleX(1)}}"
           f".shake{{animation:shake .38s linear {impact}ms both}}"
           "@keyframes shake{0%,100%{transform:none}20%{transform:translate(-4px,2px)}40%{transform:translate(4px,-2px)}60%{transform:translate(-3px,-1px)}80%{transform:translate(2px,1px)}}"
           ".wordshine{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 2.6s infinite}"]

    def corner(x, y, sx, sy):
        return f'<path d="M{x},{y+sy*22} V{y} H{x+sx*22}" fill="none" stroke="{t["hair"]}" stroke-width="1.2"/>'

    defs = (f'<radialGradient id="glow" cx=".5" cy="{cy/h:.3f}" r=".5"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="rayfade" cx=".5" cy="{cy/h:.3f}" r=".55"><stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="sparkg"><stop offset="0" stop-color="{t["sweep"]}"/><stop offset=".35" stop-color="{t["metal"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="waveg" x1="0" x2="1"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="0"/><stop offset=".5" stop-color="{t["sweep"]}"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></linearGradient>'
            + shine_band("band", t["sweep"], ".75"))
    body = f"""<defs>{defs}{udefs}
<clipPath id="panel"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="23"/></clipPath>
<mask id="rm"><rect width="{W}" height="{h}" fill="url(#rayfade)"/></mask>
<mask id="cm" mask-type="alpha"><image href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{size}"/></mask>
<mask id="wm" mask-type="alpha"><image href="{wuri}" x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}"/></mask>
</defs>
<g class="shake">
<g clip-path="url(#panel)">
<rect width="{W}" height="{h}" fill="url(#glow)" class="fade"/>
<g mask="url(#rm)"><g class="raysin" stroke="{t['metal']}" stroke-opacity=".13">{''.join(rays)}</g></g>
</g>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".5"/>
<g class="fade"{delay(1000)}>{corner(34,34,1,1)}{corner(W-34,34,-1,1)}{corner(34,h-34,1,-1)}{corner(W-34,h-34,-1,-1)}</g>
<circle class="glow" cx="{cx}" cy="{cy}" r="200" fill="url(#halo)"/>
<g class="dialin" stroke="{t['metal']}" stroke-opacity=".7" fill="none">
  <g class="dialspin">{''.join(ticks)}</g>
  <circle cx="{cx}" cy="{cy}" r="222" stroke-opacity=".45"/>
  <g class="dashspin"><circle cx="{cx}" cy="{cy}" r="180" stroke-opacity=".35" stroke-dasharray="2 7"/></g>
</g>
<g class="fade"{delay(1800)}><g class="spark"><circle cx="{cx}" cy="{cy-222}" r="11" fill="url(#sparkg)"/></g></g>
{under}
<image class="grow" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{size}"{delay(200)}/>
<g clip-path="url(#panel)">{over}</g>
<g mask="url(#cm)"><rect class="crestshine" x="{ix-220:.1f}" y="{iy:.1f}" width="220" height="{size}" fill="url(#band)"/></g>
<g class="slam"><image href="{wuri}" x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}"/>
<g class="wflash" mask="url(#wm)"><rect x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}" fill="{t['sweep']}"/></g></g>
<g mask="url(#wm)"><rect class="wordshine" x="{wx-260:.1f}" y="{wy-word_h/2:.1f}" width="240" height="{word_h}" fill="url(#band)"/></g>
<rect class="wave" x="{cx-360}" y="{wy+word_h/2+14:.1f}" width="720" height="2" fill="url(#waveg)"/>
</g>"""
    return frame(h, body, t, "".join(css), "Atilla Dev")


def stack(t):
    s = mx.stack(t)
    return (s.replace("Frontend first, with the systems", "Tools in daily use.")
             .replace(">underneath it.<", "><"))


def main():
    m.OUT.mkdir(exist_ok=True)
    for old in m.OUT.glob("*.svg"):
        old.unlink()
    built = {}
    for theme, t in THEMES.items():
        built[f"crest-{theme}"] = crest_panel(t)
        built[f"stack-{theme}"] = stack(t)
    for name, s in built.items():
        fams = [k for k in m.FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", m.font_css(fams))
        (m.OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
