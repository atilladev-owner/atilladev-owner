"""Version seven: the crest as a total eclipse. A dark disc slides into place, the corona
blazes out, a diamond ring flares at totality, then the crest and wordmark arrive. After
that the corona flickers and breathes, stars twinkle, and the diamond ring returns now
and then. No rotating rings.

    python v7.py        # writes ../assets/*.svg
"""

import math
import random

import make as m
import v6
from make import BRAND, THEMES, W, delay, img_uri
from max import frame, shine_band
from v5 import BLOOM, EMBER_CSS, crest_at, embers

random.seed(23)

DISC = {"dark": "#070605", "light": "#e6dfcf"}


def inked(t, theme):
    """Light mode draws in ink: every gold element turns black."""
    if theme == "dark":
        return dict(t, flare=t["sweep"], core="#fff", flash=".55")
    return dict(t, metal="#16150f", hair="#3a382f", glow=".08", flare="#16150f", core="#16150f", flash=".18")


def eclipse(t, theme):
    h, cx, cy, R = 620, W / 2, 262, 150
    size = 228
    uri, ix, iy, iw = crest_at(t, cx, cy, size, 520)
    wuri, (ww, wh) = img_uri(BRAND / f"brand/wordmark-{t['tone']}.webp", 900)
    word_h = 70
    word_w = ww * word_h / wh
    wx, wy = cx - word_w / 2, 536
    total, crest_in, impact = 1700, 1950, 2400

    # Corona: long thin streamers in six groups that flicker out of step.
    groups = [[] for _ in range(6)]
    for i in range(150):
        a = math.radians(random.uniform(0, 360))
        length = random.choice([random.uniform(30, 90)] * 3 + [random.uniform(110, 260)])
        r1, r2 = R + 2, R + length
        sway = random.uniform(-0.06, 0.06)
        mx_, my_ = cx + (r1 + r2) / 2 * math.cos(a + sway), cy + (r1 + r2) / 2 * math.sin(a + sway)
        groups[i % 6].append(
            f'<path d="M{cx+r1*math.cos(a):.1f},{cy+r1*math.sin(a):.1f} Q{mx_:.1f},{my_:.1f} {cx+r2*math.cos(a+sway*1.6):.1f},{cy+r2*math.sin(a+sway*1.6):.1f}"'
            f' stroke-width="{random.uniform(.6, 1.8):.2f}" stroke-opacity="{random.uniform(.35, .9):.2f}"/>')
    corona = "".join(f'<g class="fl{k}">{"".join(g)}</g>' for k, g in enumerate(groups))

    stars = "".join(
        f'<circle cx="{random.uniform(40, W-40):.1f}" cy="{random.uniform(30, h-30):.1f}" r="{random.uniform(.5, 1.4):.2f}" fill="{t["ink2"]}"'
        f' style="opacity:.35;animation:twinkle {random.uniform(3, 7):.1f}s ease-in-out {random.uniform(0, 6):.1f}s infinite"/>'
        for _ in range(70))

    fa = math.radians(-38)
    fx, fy = cx + (R + 1) * math.cos(fa), cy + (R + 1) * math.sin(fa)
    flare = (f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="46" fill="url(#flareg)"/>'
             f'<path d="M{fx:.1f},{fy-70:.1f} L{fx+3:.1f},{fy-3:.1f} L{fx+110:.1f},{fy:.1f} L{fx+3:.1f},{fy+3:.1f} L{fx:.1f},{fy+70:.1f} '
             f'L{fx-3:.1f},{fy+3:.1f} L{fx-110:.1f},{fy:.1f} L{fx-3:.1f},{fy-3:.1f} Z" fill="{t["flare"]}"/>'
             f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="7" fill="{t["core"]}"/>')

    css = [
        # The disc slides in; the corona and rim come up as it reaches totality.
        f".disc{{animation:disc {total}ms cubic-bezier(.25,.8,.25,1) both}}@keyframes disc{{from{{transform:translateX(-130px)}}}}",
        f".corona{{transform-box:view-box;transform-origin:{cx}px {cy}px;animation:corona 1.2s cubic-bezier(.16,1,.3,1) {total-500}ms both}}"
        "@keyframes corona{from{opacity:0;transform:scale(.82)}}",
        "".join(f".fl{k}{{animation:flick {random.uniform(2.6, 5.2):.1f}s ease-in-out {random.uniform(0, 3):.1f}s infinite}}" for k in range(6)),
        "@keyframes flick{0%,100%{opacity:1}35%{opacity:.45}60%{opacity:.85}80%{opacity:.6}}",
        ".rim{animation:rim 4s ease-in-out 2.4s infinite}@keyframes rim{0%,100%{opacity:1}50%{opacity:.6}}",
        # Diamond ring: a burst at totality, then a quieter return every twelve seconds.
        f".flare{{opacity:0;transform-box:fill-box;transform-origin:center;animation:flare1 1.3s cubic-bezier(.16,1,.3,1) {total}ms both,"
        f"flare2 12s ease-in-out {total+6000}ms infinite}}"
        "@keyframes flare1{0%{opacity:0;transform:scale(.2)}18%{opacity:1;transform:scale(1.25)}100%{opacity:0;transform:scale(.9)}}"
        "@keyframes flare2{0%,82%,100%{opacity:0;transform:scale(.4)}88%{opacity:.8;transform:scale(1)}}",
        f".flash{{opacity:0;animation:fl 1s ease-out {total}ms forwards}}@keyframes fl{{0%{{opacity:{t['flash']}}}100%{{opacity:0}}}}",
        f".shake{{animation:shake .38s linear {total}ms both}}"
        "@keyframes shake{0%,100%{transform:none}20%{transform:translate(-4px,2px)}40%{transform:translate(4px,-2px)}60%{transform:translate(-3px,-1px)}80%{transform:translate(2px,1px)}}",
        f".crest{{transform-box:fill-box;transform-origin:center;animation:crest 1.2s cubic-bezier(.16,1,.3,1) {crest_in}ms both}}"
        "@keyframes crest{from{opacity:0;transform:scale(.9)}}",
        ".crestshine{animation:shineloop 7s cubic-bezier(.45,0,.2,1) 3.2s infinite}",
        f".slam{{transform-box:fill-box;transform-origin:center;animation:slam .6s cubic-bezier(.2,1.4,.4,1) {impact}ms both}}"
        "@keyframes slam{0%{opacity:0;transform:scale(1.5)}55%{opacity:1}100%{opacity:1;transform:none}}",
        f".wflash{{opacity:0;animation:wflash .8s ease-out {impact+60}ms both}}@keyframes wflash{{0%{{opacity:.9}}100%{{opacity:0}}}}",
        f".wave{{opacity:0;transform-box:fill-box;transform-origin:center;animation:wave 1.1s cubic-bezier(.16,1,.3,1) {impact+80}ms both}}"
        "@keyframes wave{0%{opacity:1;transform:scaleX(0)}60%{opacity:1}100%{opacity:0;transform:scaleX(1)}}",
        ".wordshine{animation:shineloop 8s cubic-bezier(.45,0,.2,1) 3.8s infinite}",
        "@keyframes twinkle{0%,100%{opacity:.15}50%{opacity:.7}}",
        EMBER_CSS,
    ]

    def corner(x, y, sx, sy):
        return f'<path d="M{x},{y+sy*22} V{y} H{x+sx*22}" fill="none" stroke="{t["hair"]}" stroke-width="1.2"/>'

    body = f"""<defs>{BLOOM}
<radialGradient id="corona" cx="{cx}" cy="{cy}" r="{R*2.3}" gradientUnits="userSpaceOnUse">
  <stop offset="{R/(R*2.3):.3f}" stop-color="{t['metal']}" stop-opacity=".95"/>
  <stop offset="{(R+14)/(R*2.3):.3f}" stop-color="{t['metal']}" stop-opacity=".5"/>
  <stop offset="{(R+60)/(R*2.3):.3f}" stop-color="{t['metal']}" stop-opacity=".16"/>
  <stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<radialGradient id="rayfade" cx="{cx}" cy="{cy}" r="{R+260}" gradientUnits="userSpaceOnUse">
  <stop offset="{R/(R+260):.3f}" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="flareg"><stop offset="0" stop-color="{t['core']}"/><stop offset=".3" stop-color="{t['flare']}" stop-opacity=".9"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<radialGradient id="sky" cx=".5" cy="{cy/h:.3f}" r=".6"><stop offset="0" stop-color="{t['metal']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></radialGradient>
<linearGradient id="waveg" x1="0" x2="1"><stop offset="0" stop-color="{t['metal']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['sweep']}"/><stop offset="1" stop-color="{t['metal']}" stop-opacity="0"/></linearGradient>
{shine_band("band", t["sweep"], ".7")}
<clipPath id="panel"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="23"/></clipPath>
<mask id="rm"><rect width="{W}" height="{h}" fill="url(#rayfade)"/></mask>
<mask id="cm" mask-type="alpha"><image href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{size}"/></mask>
<mask id="wm" mask-type="alpha"><image href="{wuri}" x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}"/></mask>
</defs>
<g class="shake">
<g clip-path="url(#panel)">
<g class="fade">{stars}</g>
<rect class="corona" width="{W}" height="{h}" fill="url(#sky)"/>
<g class="corona">
  <circle cx="{cx}" cy="{cy}" r="{R*2.3}" fill="url(#corona)"/>
  <g mask="url(#rm)" fill="none" stroke="{t['metal']}" stroke-linecap="round" filter="url(#bloom)">{corona}</g>
</g>
<g filter="url(#bloom)">{embers(16, 80, W-80, 360, h, t['metal'], 260)}</g>
</g>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".5"/>
<g class="fade"{delay(1200)}>{corner(34,34,1,1)}{corner(W-34,34,-1,1)}{corner(34,h-34,1,-1)}{corner(W-34,h-34,-1,-1)}</g>
<g class="disc"><circle cx="{cx}" cy="{cy}" r="{R}" fill="{DISC[theme]}"/></g>
<g class="corona"><circle class="rim" cx="{cx}" cy="{cy}" r="{R+.5}" fill="none" stroke="{t['flare']}" stroke-width="2" filter="url(#bloom)"/></g>
<image class="crest" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{size}"/>
<g mask="url(#cm)"><rect class="crestshine" x="{ix-200:.1f}" y="{iy:.1f}" width="200" height="{size}" fill="url(#band)"/></g>
<g class="flare" filter="url(#bloom)">{flare}</g>
<rect class="flash" width="{W}" height="{h}" rx="24" fill="{t['flare']}"/>
<g class="slam"><image href="{wuri}" x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}"/>
<g class="wflash" mask="url(#wm)"><rect x="{wx:.1f}" y="{wy-word_h/2:.1f}" width="{word_w:.1f}" height="{word_h}" fill="{t['sweep']}"/></g></g>
<g mask="url(#wm)"><rect class="wordshine" x="{wx-260:.1f}" y="{wy-word_h/2:.1f}" width="240" height="{word_h}" fill="url(#band)"/></g>
<rect class="wave" x="{cx-360}" y="{wy+word_h/2+12:.1f}" width="720" height="2" fill="url(#waveg)"/>
</g>"""
    return frame(h, body, t, "".join(css), "Atilla Dev")


# ── Stack: four rings, AI on the outside ───────────────────────────────────

RINGS = [
    ("Frontend", [("react", "React"), ("nextdotjs", "Next.js"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind CSS")]),
    ("Backend and data", [("nodedotjs", "Node.js"), ("express", "Express"), ("python", "Python"), ("postgresql", "PostgreSQL"), ("supabase", "Supabase"), ("redis", "Redis")]),
    ("Ship", [("git", "Git"), ("githubactions", "GitHub Actions"), ("vercel", "Vercel"), ("railway", "Railway"), ("linux", "Linux")]),
    ("AI", [("claude", "Claude"), ("openai", "GPT"), ("googlegemini", "Gemini"), ("grok", "Grok"), ("deepseek", "DeepSeek")]),
]


def stack(t):
    import seal
    from make import T, rule, text_width
    from max import loop_rot
    h = 720
    ox, oy = 820, 360
    radii, speeds, entry = [92, 158, 224, 292], [70, 110, 150, 190], [-30, -18, -12, -8]
    uri, ix, iy, iw = crest_at(t, ox, oy, 80, 240)
    css = ["".join(seal.spin(f"o{i}", d, ox, oy, 1700 + i * 250) for i, d in enumerate(entry)),
           ".glow{animation:breathe 5s ease-in-out infinite}"]
    parts = [f'<defs><radialGradient id="halo"><stop offset="0" stop-color="{t["metal"]}" stop-opacity=".3"/><stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient></defs>',
             f'<g class="rise">{T("disp", "Stack", 56, 100, 48, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Tools in daily use.", 58, 136, 17, t["muted"])}{rule(56, 470, 168, t)}</g>']
    y = 224
    for i, (group, items) in enumerate(RINGS):
        lines, cur = [], ""
        for _, n in items:
            nxt = f"{cur}, {n}" if cur else n
            if text_width("body", nxt, 17) > 400:
                lines.append(cur + ",")
                cur = n
            else:
                cur = nxt
        lines.append(cur)
        block = f'<g class="rise"{delay(300+i*140)}>{T("bodym", group.upper(), 58, y, 13, t["metal"], spacing=2.6)}'
        block += "".join(T("body", ln, 58, y + 28 + j * 24, 17, t["ink2"]) for j, ln in enumerate(lines))
        parts.append(block + "</g>")
        y += 28 + len(lines) * 24 + 36
    parts.append(f'<circle class="glow" cx="{ox}" cy="{oy}" r="110" fill="url(#halo)"/>')
    parts.append(f'<g stroke="{t["line"]}" fill="none" class="fade"{delay(200)}>' + "".join(f'<circle cx="{ox}" cy="{oy}" r="{r}"/>' for r in radii) + "</g>")
    for i, ((group, items), r) in enumerate(zip(RINGS, radii)):
        back = i % 2 == 1
        css.append(loop_rot(f"orb{i}", ox, oy, speeds[i], back=back))
        css.append(f".up{i}{{transform-box:fill-box;transform-origin:center;animation:{'spinloop' if back else 'spinback'} {speeds[i]}s linear infinite}}")
        g = [f'<g class="o{i}"{delay(250+i*200)}><g class="orb{i}">']
        for k, (slug, _) in enumerate(items):
            a = math.radians(-90 + (360 / len(items)) * k + i * 22)
            x, yy = ox + r * math.cos(a), oy + r * math.sin(a)
            g.append(f'<g class="up{i}"><circle cx="{x:.1f}" cy="{yy:.1f}" r="27" fill="{t["bg"]}" stroke="{t["hair"]}" stroke-opacity=".8"/>'
                     f'<g transform="translate({x-15:.1f},{yy-15:.1f}) scale({30/24})"><path d="{m.icon_path(slug)}" fill="{t["metal"]}" fill-rule="evenodd"/></g></g>')
        parts.append("".join(g) + "</g></g>")
    parts.append(f'<image class="grow" href="{uri}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="80"/>')
    names = "; ".join(f"{g}: " + ", ".join(l for _, l in items) for g, items in RINGS)
    return frame(h, "".join(parts), t, "".join(css), f"Stack. {names}.")


def main():
    m.OUT.mkdir(exist_ok=True)
    for old in m.OUT.glob("*.svg"):
        old.unlink()
    built = {}
    for theme, t in THEMES.items():
        ti = inked(t, theme)
        built[f"crest-{theme}"] = eclipse(ti, theme)
        built[f"stack-{theme}"] = stack(ti)
    for name, s in built.items():
        fams = [k for k in m.FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", m.font_css(fams))
        (m.OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
