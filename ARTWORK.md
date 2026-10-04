# Profile artwork

The header and project cards are original SVGs. Regenerate them with:

```sh
python3 scripts/build_artwork.py
```

The header illustrates path compression: finding D redirects C and D to root A. Static alternatives are selected for reduced motion. Project illustrations describe the work; they are not app screenshots.

The profile workflow runs daily and on changes to its scripts. It uses the repository's built-in GitHub token, filters commit and pull request counts to public repositories, and publishes activity cards and contribution animations to the `output` branch. It does not access private app source or call an inference provider. The job uses a standard runner in this public repository.

Graphics tools:

- [Skill Icons](https://github.com/tandpfun/skill-icons) for the tool strip.
- [Shields.io](https://shields.io/) for contact links.
- [snk](https://github.com/Platane/snk) for contribution animations.

GitHub Actions are pinned to full commit hashes. Generated files are stored in Git rather than a temporary runtime or a shared stats endpoint.
