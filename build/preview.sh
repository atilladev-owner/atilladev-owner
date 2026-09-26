#!/bin/sh
# Renders ../README.md with GitHub's own formatter into forced dark and light pages,
# then screenshots each with motion off (the finished frame). Output: ../preview/
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
P="$ROOT/preview"
mkdir -p "$P"
/c/Users/owner/tools/gh/bin/gh.exe api markdown -f mode=gfm -f text="$(cat "$ROOT/README.md")" > "$P/body.html"
python - "$P" <<'EOF'
import re, sys
P = sys.argv[1]
body = open(f"{P}/body.html", encoding="utf-8").read()
body = re.sub(r"<source[^>]*>", "", body).replace('src="assets/', 'src="../assets/')
for theme, bg in [("dark", "#0d1117"), ("light", "#ffffff")]:
    b = body.replace("-light.svg", f"-{theme}.svg")
    open(f"{P}/{theme}.html", "w", encoding="utf-8").write(f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-{theme}.css">
<style>body{{background:{bg};margin:0}}.markdown-body{{box-sizing:border-box;max-width:880px;margin:0 auto;padding:32px}}</style></head>
<body><article class="markdown-body">{b}</article></body></html>""")
EOF
C="/c/Program Files/Google/Chrome/Application/chrome.exe"
WP="$(cygpath -m "$P")"
for t in dark light; do
  "$C" --headless=new --hide-scrollbars --force-prefers-reduced-motion --window-size=880,${HEIGHT:-4200} --screenshot="$WP/$t-static.png" "file:///$WP/$t.html" 2>/dev/null
done
echo "previews in $P"
