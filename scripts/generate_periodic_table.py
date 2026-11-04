#!/usr/bin/env python3
"""
Builds assets/periodic-table.svg for the GitHub profile README.

Edit CATEGORIES / ELEMENTS below, then run:
    python scripts/generate_periodic_table.py
"""
from math import ceil
from pathlib import Path
from xml.sax.saxutils import escape

# key: (legend label, tag shown on tile, base colour)
CATEGORIES = {
    "frontend":  ("Frontend",            "FRONTEND",  "#1d4ed8"),
    "backend":   ("Backend",             "BACKEND",   "#15803d"),
    "tools":     ("Stack & Tools",       "TOOLS",     "#7e22ce"),
    "dsa":       ("DSA & Algorithms",    "DSA",       "#c2410c"),
    "exploring": ("Currently Exploring", "EXPLORING", "#b45309"),
}

# (symbol, name, category) - atomic numbers follow list order
ELEMENTS = [
    ("Py", "Python",          "backend"),
    ("Dj", "Django",          "backend"),
    ("Ht", "HTML5",           "frontend"),
    ("Cs", "CSS3",            "frontend"),
    ("Bs", "Bootstrap",       "frontend"),
    ("Js", "JavaScript",      "frontend"),
    ("Gt", "Git",             "tools"),
    ("Gh", "GitHub",          "tools"),
    ("Vc", "VS Code",         "tools"),
    ("Ds", "Data Structures", "dsa"),
    ("Sw", "Sliding Window",  "dsa"),
    ("2p", "Two Pointers",    "dsa"),
    ("Bi", "Binary Search",   "dsa"),
    ("Re", "React",           "exploring"),
    ("Ph", "PHP",             "exploring"),
]

COLS = 5
TILE_W, TILE_H, GAP, PAD = 140, 150, 14, 24
LEGEND_H = 64


def shade(hex_color: str, toward: int, amount: float) -> str:
    """Mix a colour toward white (255) or black (0)."""
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    mixed = [round(c + (toward - c) * amount) for c in rgb]
    return "#" + "".join(f"{c:02x}" for c in mixed)


def build() -> str:
    rows = ceil(len(ELEMENTS) / COLS)
    width = PAD * 2 + COLS * TILE_W + (COLS - 1) * GAP
    grid_h = rows * TILE_H + (rows - 1) * GAP
    height = PAD + grid_h + LEGEND_H

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Periodic table of my tech stack">',
        "<defs>",
    ]

    for key, (_, _, base) in CATEGORIES.items():
        out.append(
            f'<linearGradient id="g-{key}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{shade(base, 255, 0.22)}"/>'
            f'<stop offset="1" stop-color="{shade(base, 0, 0.22)}"/></linearGradient>'
        )

    out += [
        '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#fff" stop-opacity="0.28"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity="0.35"/></filter>',
        f'<clipPath id="clip"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>',
        "</defs>",
        "<style>",
        "text{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}",
        ".sym{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:700}",
        ".tile{opacity:0;transform-box:fill-box;transform-origin:center;"
        "animation:pop .55s cubic-bezier(.2,.9,.3,1.2) forwards}",
        ".shine{animation:sweep 7s ease-in-out infinite}",
        "@keyframes pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}",
        "@keyframes sweep{0%,70%{transform:translateX(-70px) skewX(-20deg)}"
        "100%{transform:translateX(230px) skewX(-20deg)}}",
        "@media (prefers-reduced-motion:reduce){.tile{animation:none;opacity:1}.shine{display:none}}",
        "</style>",
    ]

    for i, (sym, name, cat) in enumerate(ELEMENTS):
        label, tag, _ = CATEGORIES[cat]
        col, row = i % COLS, i // COLS
        x = PAD + col * (TILE_W + GAP)
        y = PAD // 2 + row * (TILE_H + GAP)
        pop_delay = i * 0.08
        shine_delay = 1.5 + i * 0.3
        out.append(
            f'<g transform="translate({x},{y})"><g class="tile" style="animation-delay:{pop_delay:.2f}s">'
            f'<title>{escape(name)} - {escape(label)}</title>'
            f'<rect width="{TILE_W}" height="{TILE_H}" rx="14" fill="url(#g-{cat})" filter="url(#shadow)"/>'
            f'<rect x=".75" y=".75" width="{TILE_W - 1.5}" height="{TILE_H - 1.5}" rx="13.5" '
            f'fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="1.5"/>'
            f'<g clip-path="url(#clip)"><rect class="shine" x="0" y="-10" width="46" height="{TILE_H + 20}" '
            f'fill="url(#shine)" style="animation-delay:{shine_delay:.2f}s"/></g>'
            f'<text x="12" y="25" font-size="13" font-weight="600" fill="#fff" fill-opacity=".85">{i + 1:02d}</text>'
            f'<text x="{TILE_W - 12}" y="24" font-size="8.5" letter-spacing="1" text-anchor="end" '
            f'fill="#fff" fill-opacity=".75">{tag}</text>'
            f'<text class="sym" x="{TILE_W / 2}" y="90" font-size="46" text-anchor="middle" fill="#fff">{escape(sym)}</text>'
            f'<text x="{TILE_W / 2}" y="127" font-size="14" font-weight="600" text-anchor="middle" '
            f'fill="#fff">{escape(name)}</text>'
            f"</g></g>"
        )

    # Legend, centred under the grid
    legend_y = PAD // 2 + grid_h + 38
    widths = [len(v[0]) * 7.4 + 34 for v in CATEGORIES.values()]
    x = (width - sum(widths) + 14) / 2
    for (key, (label, _, base)), w in zip(CATEGORIES.items(), widths):
        out.append(
            f'<circle cx="{x + 6:.1f}" cy="{legend_y - 4}" r="6" fill="{base}"/>'
            f'<text x="{x + 20:.1f}" y="{legend_y}" font-size="13" fill="#8b949e">{escape(label)}</text>'
        )
        x += w

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    target = Path(__file__).resolve().parent.parent / "assets" / "periodic-table.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(), encoding="utf-8")
    print(f"Wrote {target}")
