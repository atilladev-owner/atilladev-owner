"""The seal layout: a dial hero, an asymmetric evidence grid, a spread of the work,
a slim project index and an orbiting stack. Builds on the helpers in make.py.

    python seal.py        # writes ../assets/*.svg
"""

import math

import make as m
from make import BRAND, THEMES, T, W, delay, escape, fit, img_uri, rule, star, text_width


def frame(h, body, t, css="", title="", panel=True):
    ground = (f'<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}"/>'
              if panel else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}"'
            f' role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>/*FONTS*/{m.MOTION}{css}</style>{ground}{body}</svg>')


def spin(name, deg, ox, oy, ms=1600):
    """A group that turns into place about (ox, oy), once."""
    return (f".{name}{{transform-box:view-box;transform-origin:{ox}px {oy}px;"
            f"animation:{name} {ms}ms cubic-bezier(.16,1,.3,1) both}}"
            f"@keyframes {name}{{from{{opacity:0;transform:rotate({deg}deg)}}}}")


# ── Hero: the crest as a dial ───────────────────────────────────────────────

def hero(t):
    h, cx, cy = 640, W / 2, 262
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 600)
    size = 280
    crest_w = cw * size / ch

    rays = []
    for i in range(72):
        a = math.radians(i * 5)
        r1, r2 = (218, 620) if i % 2 == 0 else (218, 420)
        rays.append(f'<line x1="{cx+r1*math.cos(a):.1f}" y1="{cy+r1*math.sin(a):.1f}" '
                    f'x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}"/>')
    ticks = []
    for i in range(120):
        a = math.radians(i * 3 - 90)
        long_ = i % 10 == 0
        r1, r2 = (192, 210) if long_ else (199, 206)
        ticks.append(f'<line x1="{cx+r1*math.cos(a):.1f}" y1="{cy+r1*math.sin(a):.1f}" '
                     f'x2="{cx+r2*math.cos(a):.1f}" y2="{cy+r2*math.sin(a):.1f}"'
                     f'{" stroke-width=\"1.6\"" if long_ else ""}/>')

    typed = "Frontend first. Built to be hard to break."
    tsize = 25
    tw = text_width("body", typed, tsize)
    tx = cx - tw / 2
    steps = len(typed)
    css = (spin("rays", -10, cx, cy, 2200) + spin("dial", 40, cx, cy, 1800) +
           f".type{{transform-box:fill-box;transform-origin:left;animation:type {steps*50}ms steps({steps}) 1500ms both}}"
           f".caret{{animation:caret {steps*50}ms steps({steps}) 1500ms both,blink 1s step-end {1500+steps*50}ms 4}}"
           f"@keyframes type{{from{{transform:scaleX(0)}}}}"
           f"@keyframes caret{{from{{transform:translateX(-{tw:.1f}px)}}}}"
           f"@keyframes blink{{50%{{opacity:0}}}}")

    def corner(x, y, sx, sy):
        return (f'<path d="M{x},{y+sy*22} V{y} H{x+sx*22}" fill="none" stroke="{t["hair"]}" stroke-width="1.2"/>')

    cap = 14
    corners = [
        T("smcp", "Atilla Dev", 62, 66, cap + 2, t["ink2"], spacing=3),
        T("smcp", "Est. 2023", W - 62, 66, cap + 2, t["ink2"], anchor="end", spacing=3),
        T("body", "5.6037° N   0.1870° W", 62, h - 52, cap, t["muted"], spacing=1.6),
        T("body", "ACCRA  ·  GMT", W - 62, h - 52, cap, t["muted"], anchor="end", spacing=1.6),
    ]
    glow = (f'<radialGradient id="glow" cx=".5" cy="{cy/h:.3f}" r=".5">'
            f'<stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
            f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="rayfade" cx=".5" cy="{cy/h:.3f}" r=".55">'
            f'<stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    band = (f'<linearGradient id="band" x1="0" x2="1"><stop offset="0" stop-color="{t["sweep"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{t["sweep"]}" stop-opacity=".75"/>'
            f'<stop offset="1" stop-color="{t["sweep"]}" stop-opacity="0"/></linearGradient>')
    body = f"""<defs>{glow}{band}
<clipPath id="panel"><rect x="1" y="1" width="{W-2}" height="{h-2}" rx="23"/></clipPath>
<mask id="rm"><rect width="{W}" height="{h}" fill="url(#rayfade)"/></mask>
<mask id="cm" mask-type="alpha"><image href="{crest}" x="{cx-crest_w/2:.1f}" y="{cy-size/2}" width="{crest_w:.1f}" height="{size}"/></mask>
<clipPath id="tc"><rect class="type" x="{tx:.1f}" y="{538-tsize}" width="{tw+4:.1f}" height="{tsize*1.45:.1f}"/></clipPath></defs>
<g clip-path="url(#panel)">
<rect width="{W}" height="{h}" fill="url(#glow)" class="fade"/>
<g mask="url(#rm)"><g class="rays" stroke="{t['metal']}" stroke-opacity=".13" stroke-width="1">{''.join(rays)}</g></g>
</g>
<rect x="14.5" y="14.5" width="{W-29}" height="{h-29}" rx="16" fill="none" stroke="{t['hair']}" stroke-opacity=".5"/>
<g class="dial" stroke="{t['metal']}" stroke-opacity=".7">{''.join(ticks)}
<circle cx="{cx}" cy="{cy}" r="218" fill="none" stroke-opacity=".45"/>
<circle cx="{cx}" cy="{cy}" r="184" fill="none" stroke-opacity=".3" stroke-dasharray="1 5"/></g>
<image class="grow" href="{crest}" x="{cx-crest_w/2:.1f}" y="{cy-size/2}" width="{crest_w:.1f}" height="{size}"{delay(200)}/>
<g mask="url(#cm)"><rect class="sweep" x="{cx-crest_w/2-200:.1f}" y="{cy-size/2}" width="220" height="{size}" fill="url(#band)"{delay(1100)}/></g>
<g class="rise"{delay(700)}>{T("disp", "Prince Newson Viala", cx, 500, 72, t["ink"], anchor="middle")}</g>
<g clip-path="url(#tc)">{T("body", typed, tx, 538, tsize, t["metal"])}</g>
<rect class="caret" x="{tx+tw+2:.1f}" y="{538-tsize*0.8:.1f}" width="2.5" height="{tsize*0.95:.1f}" fill="{t['metal']}"/>
<g class="fade"{delay(1000)}>{''.join(corners)}{corner(34,34,1,1)}{corner(W-34,34,-1,1)}{corner(34,h-34,1,-1)}{corner(W-34,h-34,-1,-1)}</g>"""
    return frame(h, body, t, css, "Atilla Dev. Prince Newson Viala, full stack software engineer in Accra, Ghana. Frontend first. Built to be hard to break.")


# ── Evidence: one monument figure and three companions ─────────────────────

def evidence(t):
    h = 580
    top, bot, x0, x1, xm = 116, 540, 56, W - 56, 600
    ym, xs = (top + bot) / 2, (xm + x1) / 2
    cells = [
        # (x, y, w, h, figure, label, source, figure size)
        (x0, top, xm - x0, bot - top, "261", "tests on real Postgres", "Plutus", 210),
        (xm, top, x1 - xm, ym - top, "7", "critical findings closed", "Yifan platform", 110),
        (xm, ym, xs - xm, bot - ym, "39/40", "on a design review", "Marissa", 92),
        (xs, ym, x1 - xs, bot - ym, "9", "days to production", "Marissa", 92),
    ]
    grid = "".join(f'<line x1="{x0+i*24}" y1="{top}" x2="{x0+i*24}" y2="{bot}"/>' for i in range(1, 23)) + \
           "".join(f'<line x1="{x0}" y1="{top+i*24}" x2="{xm}" y2="{top+i*24}"/>' for i in range(1, 18))
    parts = [
        f'<defs><radialGradient id="eg" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
        f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gf" cx=".5" cy=".5" r=".55"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="gm"><rect x="{x0}" y="{top}" width="{xm-x0}" height="{bot-top}" fill="url(#gf)"/></mask></defs>',
        f'<g class="rise">{T("disp", "Engineering evidence", 56, 66, 40, t["ink"])}</g>',
        f'<g class="fade"{delay(150)}>{T("body", "Each figure checked against the project’s own repository.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>',
        f'<rect x="{x0}" y="{top}" width="{xm-x0}" height="{bot-top}" fill="url(#eg)" class="fade"/>',
        f'<g mask="url(#gm)" stroke="{t["metal"]}" stroke-opacity=".12" class="fade"{delay(200)}>{grid}</g>',
        f'<g stroke="{t["line"]}" class="fade"{delay(250)}><line x1="{xm}" y1="{top}" x2="{xm}" y2="{bot}"/>'
        f'<line x1="{xm}" y1="{ym}" x2="{x1}" y2="{ym}"/><line x1="{xs}" y1="{ym}" x2="{xs}" y2="{bot}"/>'
        f'<line x1="{x0}" y1="{bot}" x2="{x1}" y2="{bot}"/></g>',
    ]
    for i, (x, y, w, hh, n, label, src, fs) in enumerate(cells):
        mid = x + w / 2
        ls = 22 if i == 0 else 19
        tail = fs * 0.26
        block = fs * 0.70 + tail + 14 + ls + 16 + 14
        base = y + (hh - block) / 2 + fs * 0.70
        lab = base + tail + 14 + ls
        parts.append(f'<g class="rise"{delay(300+i*160)}>'
                     f'{T("disp", n, mid, base, fs, t["metal"], anchor="middle")}'
                     f'{T("body", label, mid, lab, ls, t["ink"], anchor="middle")}'
                     f'{T("bodym", src.upper(), mid, lab + 30, 14, t["ink2"], anchor="middle", spacing=2.6)}</g>')
    return frame(h, "".join(parts), t, "", "Engineering evidence: 261 tests on real Postgres in Plutus. 7 critical findings closed on the Yifan platform. 39 of 40 on a design review for Marissa. 9 days to production for Marissa.")


# ── Work: the four sites spread across a desk ──────────────────────────────

SHOTS = [("marissa-home.jpg", "Marissa"), ("yifan-home.jpg", "Yifan Travel"),
         ("plutus-home.png", "Plutus"), ("bubbles-home-halved.png", "Bubbles")]


def spread(t):
    h = 700
    sw, sh = 560, 306
    # A shallow isometric plane: each sheet is skewed and squashed onto the desk.
    place = [(60, 250), (430, 222), (220, 420), (590, 392)]
    parts = [f'<g class="rise">{T("disp", "Selected work", 56, 66, 40, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Four products, each owned end to end.", W-56, 66, 16, t["muted"], anchor="end")}{rule(56, W-56, 86, t)}</g>',
             f'<defs><radialGradient id="sg" cx=".52" cy=".62" r=".55"><stop offset="0" stop-color="{t["metal"]}" stop-opacity="{t["glow"]}"/>'
             f'<stop offset="1" stop-color="{t["metal"]}" stop-opacity="0"/></radialGradient>'
             f'<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="{t["shadow"]}" flood-opacity=".55"/></filter></defs>',
             f'<clipPath id="stage"><rect x="1" y="104" width="{W-2}" height="{h-105}" rx="0"/></clipPath>',
             f'<rect x="1" y="100" width="{W-2}" height="{h-101}" fill="url(#sg)" class="fade"/>',
             '<g clip-path="url(#stage)"><g transform="translate(62 50) scale(0.88)">']
    for i, ((shot, name), (x, y)) in enumerate(zip(SHOTS, place)):
        uri, _ = img_uri(BRAND / "work" / shot, 1120, "JPEG", 80)
        mat = f"matrix(0.86 0.30 -0.62 0.62 {x+140} {y-120})"
        parts.append(
            f'<g class="rise"{delay(250+i*170)}><g transform="{mat}" filter="url(#sh)">'
            f'<clipPath id="c{i}"><rect width="{sw}" height="{sh}" rx="12"/></clipPath>'
            f'<g clip-path="url(#c{i})"><image href="{uri}" width="{sw}" height="{sh}" preserveAspectRatio="xMidYMin slice"/></g>'
            f'<rect x=".5" y=".5" width="{sw-1}" height="{sh-1}" rx="12" fill="none" stroke="{t["hair"]}" stroke-opacity=".8"/></g></g>')
    parts.append("</g></g>")
    return frame(h, "".join(parts), t, "", "Selected work: Marissa, Yifan Travel, Plutus and Bubbles, their front pages spread across a desk.")


# ── Index: one slim row per project, no box ────────────────────────────────

INDEX = [
    ("Marissa", "E-commerce", ["630 automated tests", "Row locked reservations", "39 of 40 on design"]),
    ("Yifan Travel", "Travel technology", ["57,000+ lines", "Flights, hotels, payments", "Sole technical owner"]),
    ("Plutus", "Financial infrastructure", ["261 tests", "Row locked transfers", "Hash chained journal"]),
    ("Bubbles", "Offline first app", ["81 tests", "Works with no signal", "Halves a recipe in one tap"]),
]


def index_row(t, name, kind, stats, last):
    h = 132
    sx, gap = 470, 34
    size = 18
    while size > 12 and sum(text_width("body", x, size) for x in stats) + gap * (len(stats) - 1) > 620:
        size -= 1
    stat_parts, x = [], sx
    for k, st in enumerate(stats):
        if k:
            stat_parts.append(star(x - gap / 2, 68, 5, t["metal"]))
        stat_parts.append(T("body", st, x, 74, size, t["ink2"]))
        x += text_width("body", st, size) + gap
    parts = [
        f'<line x1="0" y1="1" x2="{W}" y2="1" stroke="{t["hair"]}" stroke-opacity=".7"/>',
        f'<g class="rise">{T("disp", name, 8, 78, fit("disp", name, 58, 420), t["ink"])}'
        f'{T("bodym", kind.upper(), 10, 108, 13, t["metal"], spacing=2.6)}</g>',
        f'<g class="fade"{delay(150)}>{"".join(stat_parts)}</g>',
        f'<g class="rise"{delay(250)}><circle cx="{W-34}" cy="66" r="26" fill="none" stroke="{t["metal"]}" stroke-opacity=".7"/>'
        f'<path d="M{W-44},66 h20 m-7,-7 l7,7 l-7,7" fill="none" stroke="{t["metal"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>',
    ]
    if last:
        parts.append(f'<line x1="0" y1="{h-1}" x2="{W}" y2="{h-1}" stroke="{t["hair"]}" stroke-opacity=".7"/>')
    return frame(h, "".join(parts), t, "", f"{name}, {kind}. " + ". ".join(stats) + ". Read the case.", panel=False)


# ── Stack: the tools in orbit around the crest ─────────────────────────────

ORBITS = [
    ("Frontend", 112, -30, [("react", "React"), ("nextdotjs", "Next.js"), ("typescript", "TypeScript"), ("tailwindcss", "Tailwind CSS")]),
    ("Backend and data", 182, -18, [("nodedotjs", "Node.js"), ("express", "Express"), ("python", "Python"), ("postgresql", "PostgreSQL"), ("supabase", "Supabase"), ("redis", "Redis")]),
    ("Ship and AI", 252, -10, [("git", "Git"), ("githubactions", "GitHub Actions"), ("vercel", "Vercel"), ("railway", "Railway"), ("linux", "Linux"), ("claude", "Claude Code")]),
]


def stack(t):
    h = 600
    ox, oy = 830, 300
    crest, (cw, ch) = img_uri(BRAND / f"brand/crest-{t['tone']}.webp", 220)
    css = "".join(spin(f"o{i}", deg, ox, oy, 1700 + i * 250) for i, (_, _, deg, _) in enumerate(ORBITS))
    parts = [f'<g class="rise">{T("disp", "Stack", 56, 92, 48, t["ink"])}</g>',
             f'<g class="fade"{delay(150)}>{T("body", "Frontend first, with the systems", 58, 128, 17, t["muted"])}'
             f'{T("body", "underneath it.", 58, 152, 17, t["muted"])}{rule(56, 480, 184, t)}</g>']
    y = 238
    for i, (group, _, _, items) in enumerate(ORBITS):
        names = [l for _, l in items]
        lines, cur = [], ""
        for n in names:
            nxt = f"{cur}, {n}" if cur else n
            if text_width("body", nxt, 17) > 400:
                lines.append(cur + ",")
                cur = n
            else:
                cur = nxt
        lines.append(cur)
        block = f'<g class="rise"{delay(300+i*160)}>{T("bodym", group.upper(), 58, y, 13, t["metal"], spacing=2.6)}'
        for j, ln in enumerate(lines):
            block += T("body", ln, 58, y + 28 + j * 24, 17, t["ink2"])
        parts.append(block + "</g>")
        y += 28 + len(lines) * 24 + 40
    parts.append(f'<g stroke="{t["line"]}" fill="none" class="fade"{delay(200)}>' +
                 "".join(f'<circle cx="{ox}" cy="{oy}" r="{r}"/>' for _, r, _, _ in ORBITS) + "</g>")
    for i, (group, r, _, items) in enumerate(ORBITS):
        g = [f'<g class="o{i}"{delay(250+i*200)}>']
        for k, (slug, _) in enumerate(items):
            a = math.radians(-90 + (360 / len(items)) * k + i * 22)
            x, yy = ox + r * math.cos(a), oy + r * math.sin(a)
            g.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="27" fill="{t["bg"]}" stroke="{t["hair"]}" stroke-opacity=".8"/>'
                     f'<g transform="translate({x-15:.1f},{yy-15:.1f}) scale({30/24})"><path d="{m.icon_path(slug)}" fill="{t["metal"]}"/></g>')
        parts.append("".join(g) + "</g>")
    parts.append(f'<image class="grow" href="{crest}" x="{ox-46}" y="{oy-46*ch/cw:.1f}" width="92" height="{92*ch/cw:.1f}"/>')
    names = "; ".join(f"{g}: " + ", ".join(l for _, l in items) for g, _, _, items in ORBITS)
    return frame(h, "".join(parts), t, css, f"Stack. {names}.")


def main():
    m.OUT.mkdir(exist_ok=True)
    for old in m.OUT.glob("*.svg"):
        old.unlink()
    for p in m.OUT.glob("*.jpg"):
        p.unlink()
    for p in m.OUT.glob("banner-*.png"):
        p.unlink()
    built = {}
    for theme, t in THEMES.items():
        built[f"hero-{theme}"] = hero(t)
        built[f"evidence-{theme}"] = evidence(t)
        built[f"work-{theme}"] = spread(t)
        for i, (name, kind, stats) in enumerate(INDEX):
            slug = name.split()[0].lower()
            built[f"row-{slug}-{theme}"] = index_row(t, name, kind, stats, i == len(INDEX) - 1)
        built[f"stack-{theme}"] = stack(t)
        built[f"footer-{theme}"] = m.footer(t)
    for name, s in built.items():
        fams = [k for k in m.FONTS if f'font-family="{k}"' in s]
        s = s.replace("/*FONTS*/", m.font_css(fams))
        (m.OUT / f"{name}.svg").write_text(s, encoding="utf-8")
        print(f"{name}.svg  {len(s)//1024} KB")


if __name__ == "__main__":
    main()
