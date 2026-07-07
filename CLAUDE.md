# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static site hosted at **xarp.us** via GitHub Pages (CNAME set). No build step, no package manager, no framework — every file is served as-is. Deploy by pushing to `master`.

## Structure

- `index.html` — landing page, links to `/osrs`, `/stuff`, and `/resources`
- `osrs/index.html` — nav hub for all OSRS tools; **add new tools here**
- `osrs/*.html` — individual tools, each self-contained (HTML + inline CSS + inline JS)
- `osrs/rl-proxy-worker.js` — Cloudflare Worker that proxies the RuneLite maven metadata XML to add CORS headers; deployed separately, not part of the static site
- `raw/` — source Python scripts that the JS simulators were ported from
- `stuff/index.html` — legacy downloads page (JSON file downloads); do not modify layout
- `resources/index.html` — resources hub; accordion sections, each collapsible (only one open at a time)
- `resources/nylos.html` — Nylocas wave reference; 31 waves with lane spawn data, wave/timestamp jump inputs

## resources/ conventions

- Section labels are accordion toggles (`.section-label` + `.group-body`); clicking one closes all others.
- Subsections use `.sub-label` inside `.group-body`.
- Nylo chips: outlined = small, filled = big; M=melee (orange `#e87a2e`), G=mage (blue `#4e8ae8`), R=range (green `#4ec94e`).
- `resources/nylos.html` drives timing from a `STEPS` array — each entry is 4 ticks (2.4 s); `{ wave: null }` rows are natural stalls. Tick = 0.6 s.

## Design system

All newer pages share a dark theme. Use these values consistently:

- Background: `#0f0f11`
- Card/section background: `#16161a`
- Borders: `#2a2a2e`
- Body text: `#e8e8e8`, muted: `#555`, dimmer labels: `#3a3a42`
- Section label style: `0.67rem, font-weight 700, letter-spacing 2px, uppercase, color #3a3a42`
- Input background: `#0f0f11`, border `#2a2a2e`, focus border `#4a4a54`
- Accent colours: green `#4ec94e`, yellow `#e8b84e`, orange `#e87a2e`, red `#e54e4e`
- Font: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Max content width: `680px` (tools), `480px` (nav/landing pages)

`bloat.html`, `p1.html`, and `rlver.html` have been migrated to the dark theme.

## Adding a new tool

1. Create `osrs/<name>.html` as a self-contained page with the dark theme above.
2. Add a back link: `<a class="back" href="/osrs/">← back</a>`
3. Add an entry to `osrs/index.html` under the appropriate section label (`Simulators` or `Misc`).

## Simulator math conventions

Damage distributions are modelled as **Uniform[0, 2×avg_hit]** per swing (assumes 100% accuracy). Multiple independent swings are combined via **normal approximation** (sum of variances). The erf-based `normCDF` implementation used across simulators is:

```js
function erf(x) {
  const sign = x >= 0 ? 1 : -1;
  x = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * x);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return sign * y;
}
function normCDF(x, mu, sigma) {
  if (sigma <= 0) return x > mu ? 1 : 0;
  return 0.5 * (1 + erf((x - mu) / (sigma * Math.SQRT2)));
}
```

Variance per swing for a player doing `avgHit` average: `avgHit² / 3`.
