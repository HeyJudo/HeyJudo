"""Builds assets/stack.svg: skillicons grouped by row, popping in one by one.

Edit GROUPS, then run: python scripts/build_stack.py
Icon ids: https://github.com/tandpfun/skill-icons#icons-list
"""
import html
import re
import urllib.request
from pathlib import Path

GROUPS = [
    ("FRONTEND", "ts,js,react,nextjs,tailwind,vite"),
    ("BACKEND & CLOUD", "cs,dotnet,supabase,postgres,docker,vercel"),
    ("SYSTEMS & GAMES", "cpp,c,wasm,godot"),
    ("ALSO", "py,java,git"),
]
ICON, GAP, ROW, LABEL_W = 48, 12, 64, 200


def icons(ids):
    url = f"https://skillicons.dev/icons?i={ids}&perline=50"
    req = urllib.request.Request(url, headers={"User-Agent": "build_stack"})
    svg = urllib.request.urlopen(req).read().decode()
    # each icon is a nested 256x256 <svg> inside a translate <g>
    return re.findall(r'<g transform="translate\([^)]*\)">\s*(<svg.*?</svg>)\s*</g>', svg, re.S)


def build():
    body, n = [], 0
    for r, (label, ids) in enumerate(GROUPS):
        y = r * ROW
        body.append(
            f'<circle cx="4" cy="{y + ICON / 2}" r="3" class="dot"/>'
            f'<text x="16" y="{y + ICON / 2 + 5}" class="lbl">{html.escape(label)}</text>'
        )
        for c, icon in enumerate(icons(ids)):
            icon = icon.replace('width="256" height="256"', f'width="{ICON}" height="{ICON}"', 1)
            x = LABEL_W + c * (ICON + GAP)
            body.append(
                f'<g transform="translate({x},{y})"><g class="pop" style="animation-delay:{n * 0.07:.2f}s">'
                f'<g class="bob" style="animation-delay:{n * 0.18:.2f}s">{icon}</g></g></g>'
            )
            n += 1
    cols = max(len(ids.split(",")) for _, ids in GROUPS)
    w, h = LABEL_W + cols * (ICON + GAP) - GAP, len(GROUPS) * ROW - (ROW - ICON)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<style>
.lbl{{font:600 13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:.12em;fill:#57606a}}
.dot{{fill:#6366f1}}
.pop{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .55s cubic-bezier(.34,1.56,.64,1) forwards}}
.bob{{transform-box:fill-box;animation:bob 3.2s ease-in-out infinite}}
@keyframes pop{{from{{opacity:0;transform:scale(.4) translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
@media (prefers-color-scheme:dark){{.lbl{{fill:#8b949e}}.dot{{fill:#818cf8}}}}
@media (prefers-reduced-motion:reduce){{.pop,.bob{{animation:none;opacity:1}}}}
</style>
{chr(10).join(body)}
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "stack.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print("wrote", out)
