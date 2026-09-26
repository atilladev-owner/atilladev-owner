"""Writes ../README.md: the brand, and the tools. Nothing that pitches; that lives on
the portfolio.

    python readme.py
"""

from pathlib import Path

ROOT = Path(__file__).parent.parent


def pic(name, alt):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img src="assets/{name}-light.svg" alt="{alt}" width="100%"></picture>')


parts = [
    pic("crest", "Atilla Dev"),
    "",
    pic("stack", "Stack. Frontend: React, Next.js, TypeScript, Tailwind CSS. Backend and data: Node.js, Express, Python, PostgreSQL, Supabase, Redis. Ship: Git, GitHub Actions, Vercel, Railway, Linux. AI: Claude, GPT, Gemini, Grok, DeepSeek."),
    "",
]
(ROOT / "README.md").write_text("\n".join(parts), encoding="utf-8", newline="\n")
print("README.md written")
