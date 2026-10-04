# Galaxy renderer

Source: https://github.com/vinimlo/galaxy-profile/tree/ca7706590fe6f3f012b3e63e4ff5d101380f60b2

Vendored renderer modules from galaxy-profile, revision `ca7706590fe6f3f012b3e63e4ff5d101380f60b2`. The renderer is GPL-3.0; see `LICENSE`. Spectral glyph atlases are distributed under the SIL Open Font License; see `assets/fonts/OFL-Spectral.txt`. The upstream font atlas build script is included under `tools/`.

Local change, 5 October 2026: the identity tagline in `generator/plates/galaxy.py` may wrap to two lines, with the following description moved down accordingly. This keeps “Artificial Intelligence and Robotics student” visible.

Local change, 5 October 2026: `generator/themes.py` adds a monochrome palette with black, white, and grey stars, text, and backgrounds in both modes.

Only the modules needed to draw the header are included. `scripts/update_galaxy.py` supplies a public repository snapshot and renders the eight desktop/mobile, dark/light, and static/animated variants. No private repository content is fetched.
