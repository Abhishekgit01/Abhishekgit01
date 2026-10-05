# Profile artwork

The space header is adapted from [galaxy-profile](https://github.com/vinimlo/galaxy-profile). Stars are drawn from public repositories; particle dust is decorative. Repository and focus-area labels are hidden so the galaxy remains clear of text.

The compact header uses black, white, and grey. Three thin, exploratory star trails gradually tighten into the galaxy's ordered spiral. They interpret the profile's “Learning by making things work” tagline: curiosity becomes focus through building and iteration. The particles become less scattered as they approach the core, and the wisps share the galaxy's greyscale palette and bloom. Clouds and their dust fade in just after the core begins forming, then drift together around the galaxy's centre. A soft mask keeps the name and tagline clear. No project names or diagrams are displayed in the image. Fine background stars add depth across the header. The clouds and fine dust are decorative and do not represent repositories or contribution metrics. Desktop/mobile and dark/light variants are provided, with static alternatives for reduced motion. The tool strip retains the official Skill Icons colours. All other content beneath the header is ordinary README text, including the email and LinkedIn details under “Connect with me”. The profile has no extra poster, project showcase, contribution snake, or duplicate activity widgets.

## Regenerate the header

```sh
python3 -m pip install -r requirements-artwork.txt
python3 scripts/update_galaxy.py --output dist
```

Edit `galaxy.yml` to change the identity or featured public repositories. The `profile.show_labels: false` setting hides the chart annotations. To reproduce a stored public snapshot:

```sh
python3 scripts/update_galaxy.py --input public-repositories.json --date 2026-10-05 --output dist
```

The profile workflow runs daily and on changes to its renderer or configuration. It refreshes the galaxy and publishes its SVGs to the `output` branch. The README uses those generated files. A set of header SVGs is also kept in `assets/`.

The workflow reads public repository metadata through GitHub's public user endpoint and uses its built-in GitHub token on a standard public Actions runner. It does not read private application source or use an inference provider.

Older illustrations and activity helpers remain available as source history, but they are not displayed or refreshed by the current workflow. GitHub's own contribution graph remains on the profile.

## Interactive star map

A separate web page lets visitors hover, focus, or tap three ringed public repository stars. Positions are read from the actual SVG glyphs, so each target sits on its repository's star. Details stay hidden until selected. Keyboard focus, Escape, touch input, and reduced motion are supported. A CSS fallback reveals names and descriptions when JavaScript is unavailable. The page uses public repository descriptions only.

GitHub displays the README header as an image; individual stars inside it cannot receive hover events or activate links. The image links to the companion star map hosted on GitHub Pages. The artwork workflow builds the image and page from the same public snapshot. To build the local page from a saved public snapshot and generated artwork:

```sh
python3 scripts/build_star_map.py --input public-repositories.json --svg-dir dist --output star-map.html
```

## Sources and licenses

- [galaxy-profile](https://github.com/vinimlo/galaxy-profile): GPL-3.0 renderer, with its source, revision, modifications, and license in `vendor/galaxy-profile/`.
- Spectral: SIL Open Font License, included with the renderer.
- [Skill Icons](https://github.com/tandpfun/skill-icons): the tool logos retain their original colours and MIT license, with the adaptation note in `vendor/skill-icons/`.

GitHub Actions are pinned to full commit hashes.
