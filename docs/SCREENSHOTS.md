# Screenshot Standards

Screenshots are part of the repo's documentation contract. Keep them clear, current, and reproducible.

## Paths and Naming

- Store assets in `docs/screenshots/`.
- Use lowercase kebab-case names.
- Prefer descriptive names tied to page sections, e.g.:
  - `hero-landing.png`
  - `gallery-overview.png`
  - `features-section.png`
  - `race-results.png`

## Capture Baseline

- Desktop width: ~1440px.
- Browser zoom: 100%.
- Avoid personal data, API keys, or machine-specific details.
- Capture after UI loads fully (no partial animations).

## Minimum Screenshot Set for Major UI Changes

- landing hero
- simulation gallery
- features/framework section
- race results section

If a UI change affects one of these areas, update the corresponding screenshot.

## Updating References

When adding/replacing screenshots:

- update references in `README.md`
- update references in `docs/index.html`
- ensure file paths are valid in GitHub and GitHub Pages
