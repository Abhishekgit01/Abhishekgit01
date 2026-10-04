"""Draw the profile galaxy from public GitHub repository metadata.

SPDX-License-Identifier: GPL-3.0-only
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "vendor/galaxy-profile"))

from generator.config import validate_config
from generator.data import from_rest
from generator.model import galaxy
from generator.plates.galaxy import render
from generator.themes import get_theme


def fetch_repositories(username):
    """Read the public user endpoint, with bounded pagination and timeouts."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", username):
        raise ValueError("Invalid GitHub username")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-galaxy-artwork",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    repositories = []
    for page in range(1, 21):
        request = urllib.request.Request(
            f"https://api.github.com/users/{username}/repos"
            f"?type=owner&per_page=100&page={page}",
            headers=headers,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                batch = json.load(response)
        except urllib.error.HTTPError as error:
            raise RuntimeError(
                f"GitHub repository request failed with HTTP {error.code}"
            ) from error
        if not isinstance(batch, list):
            raise TypeError("GitHub did not return a repository list")
        repositories.extend(batch)
        if len(batch) < 100:
            return repositories
    raise RuntimeError("Repository query exceeded its pagination limit")


def render_variants(repositories, config, today):
    """Render every variant before writing any output."""
    username = config["username"]
    if not isinstance(repositories, list) or not repositories:
        raise ValueError("A nonempty public repository list is required")
    for repository in repositories:
        if not isinstance(repository, dict) or repository.get("private") is not False:
            raise ValueError("The galaxy accepts public repository metadata only")
        if repository.get("owner", {}).get("login", "").lower() != username.lower():
            raise ValueError("Repository owner does not match the profile")
    snapshot = from_rest(username, {}, repositories, {}, None, None, today)
    view = galaxy(snapshot, config)
    variants = {}
    for mode in ("dark", "light"):
        theme = get_theme(config["themes"][mode], mode, config["themes"]["overrides"])
        for mobile in (False, True):
            for motion in (True, False):
                name = f"galaxy-{mode}"
                if mobile:
                    name += "-mobile"
                if not motion:
                    name += "-static"
                variants[name + ".svg"] = render(
                    view, config["profile"], theme, mobile, motion, seed=username
                )
    return variants


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "galaxy.yml")
    parser.add_argument("--input", type=Path, help="Use a public repository snapshot")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument(
        "--date", type=date.fromisoformat, help="Reproduce a dated render"
    )
    args = parser.parse_args()
    config = validate_config(yaml.safe_load(args.config.read_text(encoding="utf-8")))
    if args.input:
        repositories = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        repositories = fetch_repositories(config["username"])
    today = args.date or datetime.now(timezone.utc).date()
    variants = render_variants(repositories, config, today)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, artwork in variants.items():
        destination = args.output / name
        temporary = destination.with_suffix(".tmp")
        temporary.write_text(artwork, encoding="utf-8")
        temporary.replace(destination)
    print(f"Rendered {len(variants)} galaxy variants from public repositories")


if __name__ == "__main__":
    main()
