"""Build the profile's original SVG artwork using only the standard library."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
THEMES = {
    "dark": {
        "background": "#000000",
        "surface": "#121212",
        "foreground": "#F5F5F5",
        "secondary": "#B8B8B8",
        "line": "#333333",
        "accent": "#E6E6E6",
        "amber": "#CCCCCC",
        "rose": "#EEEEEE",
    },
    "light": {
        "background": "#FFFFFF",
        "surface": "#FFFFFF",
        "foreground": "#111111",
        "secondary": "#555555",
        "line": "#DDDDDD",
        "accent": "#333333",
        "amber": "#666666",
        "rose": "#444444",
    },
}


def text(x, y, value, size=16, color="#F5F5F5", weight=400, **attributes):
    attrs = " ".join(
        f'{key.replace("_", "-")}="{escape(str(value))}"'
        for key, value in attributes.items()
    )
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" {attrs}>{escape(value)}</text>'
    )


def document(width, height, title, description, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{escape(title)}</title>\n'
        f'<desc id="desc">{escape(description)}</desc>\n'
        '<g font-family="Inter, Segoe UI, Arial, sans-serif">\n'
        + body
        + "\n</g>\n</svg>\n"
    )


def node(x, y, label, palette, radius=18, accent=None):
    color = accent or palette["accent"]
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{palette["surface"]}" '
        f'stroke="{color}" stroke-width="1.5"/>'
        + text(x, y + 5, label, 14, color, 600, text_anchor="middle")
    )


def hero(theme, animated=True):
    p = THEMES[theme]
    motion = (
        """
<style>
 .original { animation: original 8s infinite; }
 .compressed { opacity: 0; animation: compressed 8s infinite; }
 @keyframes original { 0%,30%,92%,100% { opacity: 1; } 40%,82% { opacity: 0; } }
 @keyframes compressed { 0%,30%,92%,100% { opacity: 0; } 40%,82% { opacity: 1; } }
 @media (prefers-reduced-motion: reduce) { .original { animation: none; } .compressed { animation: none; opacity: 0; } }
</style>
"""
        if animated
        else ""
    )
    diagram = (
        f'<g fill="none" stroke="{p["line"]}" stroke-width="1">'
        '<circle cx="734" cy="148" r="108"/><circle cx="734" cy="148" r="88"/>'
        '<path d="M604 148H864M734 22V274" stroke-dasharray="3 7"/></g>'
        f'<g fill="none" stroke="{p["accent"]}" stroke-width="2" marker-end="url(#arrow)">'
        '<path d="M720 121L684 91"/>'
        '<g class="original"><path d="M689 182L724 148"/>'
        '<path d="M788 202H715"/></g>'
        '<g class="compressed" opacity="0"><path d="M674 180V103"/>'
        '<path d="M804 184Q810 63 696 77"/></g></g>'
        + node(674, 76, "A", p, 23)
        + node(737, 134, "B", p)
        + node(674, 203, "C", p)
        + node(808, 203, "D", p)
        + text(
            660, 266, "find(D) → A", 15, p["secondary"], 500, font_family="monospace"
        )
    )
    body = (
        motion + f'<defs><linearGradient id="wash" x1="0" x2="1" y1="1" y2="0">'
        f'<stop stop-color="{p["background"]}"/><stop offset="1" stop-color="{p["surface"]}"/>'
        f'</linearGradient><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10Z" fill="{p["accent"]}"/></marker></defs>'
        f'<rect x=".5" y=".5" width="899" height="319" rx="20" fill="url(#wash)" '
        f'stroke="{p["line"]}"/>'
        f'<rect x="42" y="36" width="5" height="15" rx="2" fill="{p["accent"]}"/>'
        + text(
            57,
            49,
            "ABHISHEK / WORKSPACE",
            12,
            p["secondary"],
            600,
            letter_spacing="2",
        )
        + text(41, 123, "Abhishek R P", 57, p["foreground"], 700, letter_spacing="-2")
        + text(43, 166, "I build products and explore AI.", 23, p["secondary"], 400)
        + text(
            43,
            218,
            "ARTIFICIAL INTELLIGENCE AND ROBOTICS STUDENT",
            11,
            p["accent"],
            600,
            letter_spacing="1",
        )
        + f'<path d="M43 253H548" stroke="{p["line"]}"/>'
        + text(43, 283, "DSCE · Bengaluru", 13, p["secondary"])
        + text(339, 283, "Founder, Bento · Mysuru", 13, p["secondary"])
        + diagram
    )
    return document(
        900,
        320,
        "Abhishek R P — products, AI and algorithms",
        "Artificial Intelligence and Robotics student at DSCE, Bengaluru, and founder of Bento in Mysuru. "
        "The illustration shows disjoint-set path compression from D through C and B to A.",
        body,
    )


def visdsr_art(p):
    return (
        f'<rect x="29" y="45" width="128" height="112" rx="12" fill="{p["surface"]}" stroke="{p["line"]}"/>'
        + text(44, 70, "parent map", 12, p["secondary"], 500, font_family="monospace")
        + text(45, 96, '"A": "A"', 13, p["accent"], 500, font_family="monospace")
        + text(45, 118, '"B": "A"', 13, p["accent"], 500, font_family="monospace")
        + text(45, 140, '"C": "A"', 13, p["accent"], 500, font_family="monospace")
        + text(179, 110, "↔", 23, p["secondary"], 400, text_anchor="middle")
        + f'<g stroke="{p["accent"]}" stroke-width="1.5"><path d="M248 90L218 113M253 90L278 113"/></g>'
        + node(251, 70, "A", p, 17)
        + node(205, 128, "B", p, 17)
        + node(291, 128, "C", p, 17)
    )


def bento_art(p):
    tiles = []
    for x, y, width, height in [
        (35, 48, 123, 101),
        (170, 48, 111, 43),
        (170, 103, 51, 46),
        (233, 103, 48, 46),
    ]:
        tiles.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" '
            f'fill="{p["surface"]}" stroke="{p["line"]}"/>'
        )
    tiles.extend(
        [
            f'<circle cx="95" cy="98" r="32" fill="none" stroke="{p["amber"]}" stroke-width="1.5"/>',
            f'<circle cx="95" cy="98" r="24" fill="none" stroke="{p["amber"]}" stroke-width="1" opacity=".4"/>',
            text(186, 75, "MYSURU", 12, p["amber"], 600, letter_spacing="1.6"),
            text(183, 134, "7", 24, p["amber"], 600),
            f'<path d="M247 118V136M253 118V136M247 123H253M265 118V136" stroke="{p["amber"]}" stroke-width="2" stroke-linecap="round"/>',
        ]
    )
    return "".join(tiles)


def us_art(p):
    return (
        f'<rect x="67" y="45" width="110" height="83" rx="20" fill="{p["surface"]}" stroke="{p["rose"]}"/>'
        f'<rect x="143" y="83" width="111" height="72" rx="20" fill="{p["surface"]}" stroke="{p["line"]}"/>'
        f'<path d="M113 76C104 64 87 75 100 88L115 101L130 88C142 75 126 64 115 77Z" fill="{p["rose"]}" opacity=".8"/>'
        f'<path d="M176 113H222M176 128H208" stroke="{p["rose"]}" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
        f'<rect x="227" y="51" width="22" height="20" rx="5" fill="{p["rose"]}"/>'
        f'<path d="M232 51V46A6 6 0 0 1 244 46V51" fill="none" stroke="{p["rose"]}" stroke-width="2"/>'
        f'<circle cx="238" cy="60" r="2" fill="{p["background"]}"/>'
    )


def card(name, theme):
    p = THEMES[theme]
    config = {
        "visdsr": (
            "01 / RESEARCH",
            "VisDSR",
            "Text. Images. DSU reasoning.",
            "C++ · Python · Qwen · InternVL",
            "accent",
            visdsr_art,
        ),
        "bento": (
            "02 / FOUNDER",
            "Bento",
            "Dine-in, built for Mysuru.",
            "7 restaurant collabs · Pre-launch",
            "amber",
            bento_art,
        ),
        "us": (
            "03 / PRODUCT",
            "US",
            "A space for two.",
            "React Native · Expo · Supabase",
            "rose",
            us_art,
        ),
    }
    label, title, subtitle, stack, accent, illustration = config[name]
    body = (
        f'<rect x=".5" y=".5" width="319" height="309" rx="16" '
        f'fill="{p["background"]}" stroke="{p["line"]}"/>'
        + text(23, 28, label, 10, p["secondary"], 600, letter_spacing="1.7")
        + illustration(p)
        + f'<path d="M24 175H296" stroke="{p["line"]}"/>'
        + text(23, 216, title, 33, p["foreground"], 700, letter_spacing="-.8")
        + text(23, 244, subtitle, 15, p["secondary"])
        + text(23, 283, stack, 11, p[accent], 500)
    )
    return document(320, 310, f"{title} — {subtitle}", stack, body)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (ASSETS / f"hero-{theme}.svg").write_text(hero(theme), encoding="utf-8")
        (ASSETS / f"hero-{theme}-static.svg").write_text(
            hero(theme, animated=False), encoding="utf-8"
        )
        for name in ("visdsr", "bento", "us"):
            (ASSETS / f"{name}-{theme}.svg").write_text(
                card(name, theme), encoding="utf-8"
            )
    print("Built 10 original SVG assets.")


if __name__ == "__main__":
    main()
