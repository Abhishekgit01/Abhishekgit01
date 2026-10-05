# Galaxy renderer

Source: https://github.com/vinimlo/galaxy-profile/tree/ca7706590fe6f3f012b3e63e4ff5d101380f60b2

Vendored renderer modules from galaxy-profile, revision `ca7706590fe6f3f012b3e63e4ff5d101380f60b2`. The renderer is GPL-3.0; see `LICENSE`. Spectral glyph atlases are distributed under the SIL Open Font License; see `assets/fonts/OFL-Spectral.txt`. The upstream font atlas build script is included under `tools/`.

Local change, 5 October 2026: the identity tagline in `generator/plates/galaxy.py` may wrap to two lines, with the following description moved down accordingly.

Local change, 5 October 2026: `profile.show_labels` controls repository and focus-area labels. This profile disables both, keeping the galaxy clear of overlapping text.

Local change, 5 October 2026: the desktop and mobile frames are shorter, with the identity and galaxy repositioned to fit. The background has a denser fine starfield and a faint monochrome dust band behind the identity.

Local change, 5 October 2026: three thin nebula trails now join the logarithmic galaxy arms with matching tangents. Loose particles gradually gather into more orderly flows, interpreting the learning-through-building tagline without project labels. The wisps use the galaxy palette and bloom, adapt to mobile, and protect the identity with a soft mask. Clouds and dust share a delayed entrance and gentle drift, synchronized with the core's formation. Static and reduced-motion variants remain still. Public repository stars and the existing galaxy motion remain unchanged.

Local change, 5 October 2026: `generator/themes.py` adds a monochrome palette with black, white, and grey stars, text, and backgrounds in both modes.

Local change, 5 October 2026: repository glyph groups include their public repository key and an escaped title. A companion web preview uses these positions for three hover, keyboard, and tap targets; image rendering on GitHub stays noninteractive.

Only the modules needed to draw the header are included. `scripts/update_galaxy.py` supplies a public repository snapshot and renders the eight desktop/mobile, dark/light, and static/animated variants. No private repository content is fetched.
