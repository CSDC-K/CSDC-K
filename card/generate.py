"""Builds Kuzey's terminal-style profile card (dark_mode.svg / light_mode.svg).

    python card/generate.py           # build with the repo count saved in card/stats.json
    python card/generate.py --stats   # fetch the current public repo count first (used by the workflow)

Edit the INFO list below to change what the card says.
"""
import json
import os
import sys
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARD = ROOT / "card"
USER = "CSDC-K"
KEYW = 11  # key column width (characters)

INFO = [
    ("title", "Kuzey Ceylan"),
    ("subtitle", "systems & autonomous software developer"),
    ("gap",),
    ("section", "about"),
    ("kv", "OS", "Arch Linux · CachyOS"),
    ("kv", "Host", "Vocational High School (AMP), Adana, TR"),
    ("kv", "Major", "Software Development · class of 2027"),
    ("kv", "Now", "IT intern @ Çukurova University Hospital"),
    ("kv", "Goal", "Software architect, backend systems"),
    ("kv", "Speaks", "Turkish · English"),
    ("gap",),
    ("section", "stack"),
    ("kv", "Languages", "Rust · Python · TypeScript · C#"),
    ("kv", "Frameworks", "Tauri · OpenCV · YOLOv8 · MediaPipe · Slint"),
    ("kv", "Hardware", "Raspberry Pi 5 · Hailo-8L · ESP32"),
    ("kv", "Tools", "Linux · Git · Roboflow"),
    ("gap",),
    ("section", "competitions"),
    ("rank", "1st", "gold", "Hack Club Horizons Arcana · Singapore '26"),
    ("rank", "2nd", "silver", "Mini Sumo · 17th MEB Robot Competition '25"),
    ("rank", "3rd", "bronze", "Mini Sumo & Maze · Kendin Yap, Kütahya '25"),
    ("rank", "TL", "tag", "Fast Line Follower · KodeLig, Kocaeli '26"),
    ("rank", "AUT", "tag", "Autonomous Car · 18th MEB Robot Comp. '26"),
    ("rank", "SCI", "tag", "TÜBİTAK 4006 Science Fair '25"),
    ("gap",),
    ("section", "projects"),
    ("text", "Defused · Autonomous-Vehicle · Trigox · Oryxis"),
    ("text", "Makereadme · M.E.D.A · TheSoundOfYourHardware"),
    ("gap",),
    ("contact",),
]

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#c9d1d9", dim="#6e7681",
                 key="#79c0ff", value="#e6edf3", section="#d2a8ff", title="#ffffff", prompt="#7ee787",
                 gold="#e3b341", silver="#b1bac4", bronze="#db8a4d", tag="#58a6ff"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#24292f", dim="#8c959f",
                  key="#0550ae", value="#1f2328", section="#8250df", title="#000000", prompt="#1a7f37",
                  gold="#9a6700", silver="#57606a", bronze="#953800", tag="#0969da"),
}
PALETTE = ["#ff7b72", "#ffa657", "#e3b341", "#7ee787", "#79c0ff", "#d2a8ff", "#ff9bce", "#c9d1d9"]


def fetch_repos():
    req = urllib.request.Request(f"https://api.github.com/users/{USER}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-card"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        repos = json.load(r)["public_repos"]
    (CARD / "stats.json").write_text(json.dumps({"repos": repos}, indent=2) + "\n")
    return repos


def saved_repos():
    p = CARD / "stats.json"
    return json.loads(p.read_text())["repos"] if p.exists() else "-"


def span(color, s, extra=""):
    return f'<tspan fill="{color}"{extra}>{escape(s)}</tspan>'


def portrait(theme, x, y, lh):
    data = json.loads((CARD / "face.json").read_text())
    out = [f'<text x="{x}" y="{y}" font-size="7px">']
    for i, row in enumerate(data[theme]):
        parts, cur, buf = [], None, ""
        for ch, color in row:
            color = color or "none"
            if color != cur and buf:
                parts.append((cur, buf)); buf = ""
            cur = color; buf += ch
        if buf:
            parts.append((cur, buf))
        while parts and not parts[-1][1].strip():
            parts.pop()
        body = "".join(escape(b) if c == "none" else span(c, b) for c, b in parts)
        out.append(f'<tspan x="{x}" y="{y + i * lh:.1f}">{body}</tspan>')
    out.append("</text>")
    return out, len(data[theme])


def build(theme, repos):
    t = THEMES[theme]
    W, bar = 980, 34
    ix, iy, ilh = 452, bar + 62, 17
    rows = len(json.loads((CARD / "face.json").read_text())[theme])
    H = max(bar + 52 + rows * 8.4, iy + len(INFO) * ilh) + 40

    o = ["<?xml version='1.0' encoding='UTF-8'?>",
         f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" '
         f'font-family="\'JetBrains Mono\',Consolas,\'DejaVu Sans Mono\',monospace">',
         "<style>text,tspan{white-space:pre}"
         "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:blink 1.1s steps(1) infinite}</style>",
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1:.0f}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>',
         f'<path d="M0.5 12.5 a12 12 0 0 1 12 -12 h{W-25} a12 12 0 0 1 12 12 v{bar-12} h-{W-1} z" fill="{t["bar"]}" stroke="{t["border"]}"/>']
    for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        o.append(f'<circle cx="{22 + k * 20}" cy="{bar/2+0.5}" r="6" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="{bar/2+5}" text-anchor="middle" font-size="13px" fill="{t["dim"]}">kuzey@CSDC-K: ~</text>')

    # prompt line
    py = bar + 26
    o.append(f'<text x="20" y="{py}" font-size="13px">{span(t["prompt"], "kuzey@CSDC-K")}{span(t["text"], ":")}'
             f'{span(t["key"], "~")}{span(t["text"], "$ kfetch --user kuzey")}</text>')

    face, n = portrait(theme, 20, bar + 56, 8.4)
    o += face

    o.append(f'<text x="{ix}" y="{iy}" font-size="13px" fill="{t["text"]}">')
    for i, item in enumerate(INFO):
        y, kind = iy + i * ilh, item[0]
        if kind == "gap":
            continue
        if kind == "title":
            s = span(t["title"], item[1], ' font-weight="bold" font-size="18px"')
        elif kind == "subtitle":
            s = span(t["dim"], item[1])
        elif kind == "section":
            s = span(t["section"], f"── {item[1]} ") + span(t["border"], "─" * (52 - len(item[1])))
        elif kind == "kv":
            s = span(t["key"], item[1].ljust(KEYW)) + span(t["value"], item[2])
        elif kind == "rank":
            s = span(t[item[2]], f"[{item[1]:^3}]", ' font-weight="bold"') + " " + span(t["value"], item[3])
        elif kind == "text":
            s = span(t["value"], item[1])
        elif kind == "contact":
            s = (span(t["key"], "Web ") + span(t["value"], "kuzey.dev") + span(t["dim"], "   ·   ") +
                 span(t["key"], "GitHub ") + span(t["value"], USER) + span(t["dim"], "   ·   ") +
                 span(t["key"], "Repos ") + span(t["value"], str(repos)))
        o.append(f'<tspan x="{ix}" y="{y}">{s}</tspan>')
    o.append("</text>")

    # colour palette + blinking prompt at the bottom
    by = H - 26
    for k, c in enumerate(PALETTE):
        o.append(f'<rect x="{ix + k * 26}" y="{by - 12}" width="22" height="14" rx="2" fill="{c}"/>')
    o.append(f'<text x="20" y="{by}" font-size="13px">{span(t["prompt"], "kuzey@CSDC-K")}{span(t["text"], ":")}'
             f'{span(t["key"], "~")}{span(t["text"], "$ ")}</text>')
    o.append(f'<rect class="cur" x="{20 + 16 * 7.8:.0f}" y="{by - 12}" width="8" height="15" fill="{t["text"]}"/>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main():
    repos = fetch_repos() if "--stats" in sys.argv else saved_repos()
    for theme in THEMES:
        (ROOT / f"{theme}_mode.svg").write_text(build(theme, repos), encoding="utf-8")
    print("built, repos =", repos)


if __name__ == "__main__":
    main()
