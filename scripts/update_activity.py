"""Render an activity card from public GitHub contribution data."""

import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from build_artwork import THEMES, document, text

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(privacy: PUBLIC, isFork: false, ownerAffiliations: OWNER) { totalCount }
    contributionsCollection {
      commitContributionsByRepository(maxRepositories: 100) {
        repository { isPrivate }
        contributions { totalCount }
      }
      pullRequestContributionsByRepository(maxRepositories: 100) {
        repository { isPrivate }
        contributions { totalCount }
      }
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""


def fetch_activity(username):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", username):
        raise ValueError("Invalid GitHub username")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required to refresh the activity card")
    payload = json.dumps({"query": QUERY, "variables": {"login": username}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-activity-artwork",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("GitHub activity query failed: " + str(result["errors"]))
    if not result.get("data", {}).get("user"):
        raise RuntimeError("GitHub user was not returned")
    return result["data"]["user"]


def public_contributions(groups):
    if len(groups) >= 100:
        raise RuntimeError("Contribution query reached its repository limit")
    total = 0
    for group in groups:
        count = group["contributions"]["totalCount"]
        if not isinstance(count, int) or count < 0:
            raise ValueError("GitHub returned an invalid contribution count")
        if not group["repository"]["isPrivate"]:
            total += count
    return total


def render_activity(data, theme, updated):
    palette = THEMES[theme]
    collection = data["contributionsCollection"]
    days = [
        day
        for week in collection["contributionCalendar"]["weeks"]
        for day in week["contributionDays"]
    ]
    metrics = [
        (data["repositories"]["totalCount"], "PUBLIC ORIGINAL REPOS"),
        (
            public_contributions(collection["commitContributionsByRepository"]),
            "PUBLIC COMMITS / YEAR",
        ),
        (
            public_contributions(collection["pullRequestContributionsByRepository"]),
            "PUBLIC PRs / YEAR",
        ),
    ]
    body = (
        f'<rect x=".5" y=".5" width="899" height="175" rx="16" '
        f'fill="{palette["background"]}" stroke="{palette["line"]}"/>'
        + text(
            25,
            29,
            "PUBLIC GITHUB ACTIVITY",
            11,
            palette["secondary"],
            600,
            letter_spacing="1.6",
        )
        + text(
            875,
            29,
            f"Updated {updated} UTC",
            11,
            palette["secondary"],
            text_anchor="end",
        )
    )
    for index, (number, label) in enumerate(metrics):
        if not isinstance(number, int) or number < 0:
            raise ValueError("GitHub returned an invalid activity count")
        x = 25 + index * 198
        body += text(
            x, 85, f"{number:,}", 38, palette["foreground"], 600, letter_spacing="-1"
        )
        body += text(x, 113, label, 9, palette["secondary"], 500, letter_spacing=".9")
    for index, day in enumerate(days[-35:]):
        count = day["contributionCount"]
        if not isinstance(count, int) or count < 0:
            raise ValueError("GitHub returned an invalid contribution count")
        intensity = min(count / 8, 1)
        x = 660 + (index // 7) * 25
        y = 52 + (index % 7) * 13
        body += (
            f'<rect x="{x}" y="{y}" width="19" height="9" rx="2" '
            f'fill="{palette["blue"]}" opacity="{0.13 + 0.87 * intensity:.2f}"/>'
        )
    body += text(660, 154, "Recent contribution activity", 10, palette["secondary"])
    body += text(
        25,
        154,
        "Public repositories and contribution activity over the past year.",
        11,
        palette["secondary"],
    )
    return document(
        900,
        176,
        "Abhishek's public GitHub activity",
        "Public repository, commit and pull request counts from GitHub; contributions cover the past year.",
        body,
    )


def render_calendar(data, theme):
    palette = THEMES[theme]
    weeks = data["contributionsCollection"]["contributionCalendar"]["weeks"]
    column_step = min(16, 840 / max(len(weeks), 1))
    body = (
        f'<rect x=".5" y=".5" width="899" height="163" rx="16" '
        f'fill="{palette["background"]}" stroke="{palette["line"]}"/>'
        + text(
            25,
            29,
            "CONTRIBUTIONS / PAST YEAR",
            11,
            palette["secondary"],
            600,
            letter_spacing="1.6",
        )
    )
    for column, week in enumerate(weeks):
        for day in week["contributionDays"]:
            row = (datetime.fromisoformat(day["date"]).weekday() + 1) % 7
            intensity = min(day["contributionCount"] / 8, 1)
            body += (
                f'<rect x="{25 + column * column_step:.2f}" y="{45 + row * 13}" '
                f'width="{column_step - 4:.2f}" height="9" rx="2" '
                f'fill="{palette["blue"]}" opacity="{0.13 + 0.87 * intensity:.2f}"/>'
            )
    return document(
        900,
        164,
        "GitHub contribution calendar",
        "A static contribution calendar for visitors who prefer reduced motion.",
        body,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Abhishekgit01")
    parser.add_argument(
        "--input", type=Path, help="Use a previously fetched public API response"
    )
    parser.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    if args.input:
        data = json.loads(args.input.read_text())
        if "data" in data:
            data = data["data"]["user"]
    else:
        data = fetch_activity(args.username)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    args.output.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        target = args.output / f"activity-{theme}.svg"
        target.write_text(render_activity(data, theme, updated), encoding="utf-8")
        target = args.output / f"contribution-static-{theme}.svg"
        target.write_text(render_calendar(data, theme), encoding="utf-8")
    print("Refreshed activity artwork using GitHub's public data.")


if __name__ == "__main__":
    main()
