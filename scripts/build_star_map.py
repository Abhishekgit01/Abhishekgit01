"""Build a local interactive companion to the GitHub profile image.

SPDX-License-Identifier: GPL-3.0-only
"""

import argparse
import json
import re
import shutil
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

import yaml
from update_galaxy import ROOT, validate_config


def star_positions(path):
    """Read the real repository glyph positions from a rendered SVG."""
    root = ET.parse(path).getroot()
    left, top, width, height = map(float, root.attrib["viewBox"].split())
    positions = {}
    for node in root.iter():
        key = node.attrib.get("data-repo")
        if key is None:
            continue
        match = re.fullmatch(
            r"translate\((-?[\d.]+) (-?[\d.]+)\)", node.attrib["transform"]
        )
        if match is None:
            raise ValueError(f"Invalid star position for {key}")
        x, y = map(float, match.groups())
        positions[key] = ((x - left) / width * 100, (y - top) / height * 100)
    return positions


def project_data(config, repositories, desktop, mobile):
    """Allow only featured repositories verified in the public snapshot."""
    username = config["username"]
    public = {}
    for repository in repositories:
        if repository.get("private") is not False:
            raise ValueError("Only public repositories can appear in the star map")
        if repository.get("owner", {}).get("login", "").lower() != username.lower():
            raise ValueError("Repository owner does not match the profile")
        public[repository["full_name"].lower()] = repository

    projects = []
    for entry in config["projects"][:3]:
        key = entry["repo"].lower()
        if key not in public or key not in desktop or key not in mobile:
            raise ValueError(f"Featured public repository is missing: {key}")
        repository = public[key]
        name = repository["name"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            raise ValueError("Invalid repository name")
        projects.append(
            {
                "name": name,
                "description": entry.get("description") or repository["description"],
                "url": f"https://github.com/{username}/{name}",
                "desktop": desktop[key],
                "mobile": mobile[key],
            }
        )
    if not projects:
        raise ValueError("At least one featured public repository is required")
    return projects


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--svg-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--output", type=Path, default=ROOT / "star-map.html")
    args = parser.parse_args()
    config = validate_config(yaml.safe_load((ROOT / "galaxy.yml").read_text()))
    repositories = json.loads(args.input.read_text())
    if not isinstance(repositories, list):
        raise TypeError("A public repository list is required")
    desktop = star_positions(args.svg_dir / "galaxy-dark-static.svg")
    mobile = star_positions(args.svg_dir / "galaxy-dark-mobile-static.svg")
    projects = project_data(config, repositories, desktop, mobile)
    buttons = []
    for index, project in enumerate(projects):
        x, y = project["desktop"]
        mx, my = project["mobile"]
        style = f"--x:{x:.4f}%;--y:{y:.4f}%;--mx:{mx:.4f}%;--my:{my:.4f}%"
        buttons.append(
            f'<button class="project-target" data-project="{index}" style="{style}" '
            f'aria-label="About {escape(project["name"], quote=True)}" '
            'aria-expanded="false" aria-controls="project-details">'
            '<span class="project-star" aria-hidden="true"></span>'
            '<span class="project-fallback" role="tooltip">'
            f"<strong>{escape(project['name'])}</strong>"
            f"<span>{escape(project['description'])}</span></span></button>"
        )
    serialized = json.dumps(projects).replace("<", "\\u003c")
    template = (ROOT / "star-map/index.html").read_text()
    html = template.replace("{{PROJECT_BUTTONS}}", "\n".join(buttons))
    html = html.replace("{{PROJECT_DATA}}", serialized)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    assets = args.output.parent / "star-map-assets"
    assets.mkdir(exist_ok=True)
    for name in ("star-map.css", "star-map.js"):
        content = (ROOT / "star-map" / name).read_text()
        if name.endswith(".css"):
            html = html.replace(
                '<link rel="stylesheet" href="star-map-assets/star-map.css" />',
                f"<style>{content}</style>",
            )
        else:
            html = html.replace(
                '<script src="star-map-assets/star-map.js" defer></script>',
                f"<script>{content}</script>",
            )
    for source in args.svg_dir.glob("galaxy-*.svg"):
        shutil.copy2(source, assets / source.name)
    args.output.write_text(html, encoding="utf-8")
    print(f"Built interactive map with {len(projects)} public repository stars")


if __name__ == "__main__":
    main()
