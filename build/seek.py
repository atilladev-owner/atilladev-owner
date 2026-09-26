"""Freezes every animation in an SVG at exact moments and screenshots each one.

    python seek.py hero-dark 800 4000 7500 12000
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
name, times = sys.argv[1], [int(x) for x in sys.argv[2:]]
svg = (ROOT / "assets" / f"{name}.svg").read_text(encoding="utf-8")
w, h = svg.split('width="', 1)[1].split('"')[0], svg.split('height="', 1)[1].split('"')[0]
for ms in times:
    page = ROOT / "preview" / f"seek-{name}-{ms}.html"
    page.write_text(f"""<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#0d1117">{svg}
<script>document.getAnimations().forEach(a=>{{a.pause();a.currentTime={ms};}});</script></body></html>""", encoding="utf-8")
    out = ROOT / "preview" / f"seek-{name}-{ms}.png"
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--screenshot={out}", page.as_uri()], capture_output=True)
    print(out.name)
