# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.

## What this is

This is the source for **xarp.us**, a personal static website hosted via
GitHub Pages from `levex/levex.github.io` (see `CNAME`). It's a collection of
Old School RuneScape (OSRS) tools, simulators, raid checklists, and a few
misc utilities — all "vanilla" HTML/CSS/JS, no frameworks, no build step,
no package manager.

GitHub Pages serves the repo root directly, so every committed `.html`/`.js`/
`.json` file is immediately live at the corresponding path on the domain.
There is no CI, no build pipeline, and no test suite — what you commit is
what ships.

## Repository layout

```
/index.html              Landing page ("xarp.us") — top-level nav hub
/CNAME                    Custom domain config for GitHub Pages (xarp.us)

/osrs/                    OSRS simulators, checklists, and utilities
  index.html              Hub page for "OSRS Sims" (Simulators section)
  p1.html                 Verzik P1 Simulator
  bloat.html              Pestilent Bloat walk-pattern simulator
  zikp2.html              Verzik P2 — one-down reds tool
  vintlist.html           ToB Checklist Review tool
  tob2.html               ToB (Beta) Checklist tool
  coxlist.html            CoX Checklist Review tool
  votes.html              ToB Skill Poll
  isgameup.html           "Is OSRS up?" server status checker
  rlver.html              RuneLite version history monitor
  widgetpacker.html       Widget ID packer/unpacker
  hitchance.html          Hit Chance Diff calculator
  rl-proxy-worker.js      Cloudflare Worker — CORS proxy for RuneLite's
                          maven-metadata.xml (used by rlver.html); deployed
                          separately to Cloudflare, not served by Pages
  nylo_radius_markers.json  Downloadable data file (Nylocas room markers)

/misc/
  index.html              "Misc Tools" hub — links to utility pages under
                          /osrs/ (isgameup, rlver, widgetpacker, hitchance)
                          and to /vintage

/stuff/
  index.html              "Downloads & Resources" hub — lists downloadable
                          files (e.g. nylo_radius_markers.json) with
                          copy-to-clipboard and download actions

/vintage/
  index.html              "vintage" hub — links to the raid checklist tools
                          (vintlist, tob2, coxlist) under /osrs/

/raw/
  "Bloat for online.py"   Standalone Python simulation script used as a
                          reference/source for bloat.html's logic; not
                          served by the site
```

## Site navigation map

- `/` → links to `/osrs`, `/stuff`, `/misc` (and a "Coming Soon" ToB Data
  button)
- `/osrs` → "Simulators" group (p1, bloat, zikp2); back-links to `/`
- `/misc` → utility tools (isgameup, rlver, widgetpacker, hitchance) plus a
  link into `/vintage`; back-links to `/`
- `/vintage` → raid checklist tools (vintlist, tob2, coxlist); back-links to
  `/misc`
- `/stuff` → downloadable resources; back-links to `/`

When adding a new page, also add a corresponding entry/link on the relevant
hub page (and update its parent hub if the page introduces a new section).

## Conventions

### Page structure

Every page is a **single self-contained HTML file**: inline `<style>` in the
`<head>`, inline `<script>` before `</body>` if JS is needed. No external
stylesheets, no bundlers, no shared CSS/JS files. Each page repeats the
shared design tokens below rather than importing them.

### Visual design system (dark theme)

- Background: `#0f0f11`, text: `#e8e8e8`
- Headings (`h1`): `#fff`, `font-weight: 600`, `letter-spacing: -0.03em`
- Muted/secondary text: `#555` / `#666` / `#3a3a42`
- Borders: `#2a2a2e`, hover border: `#555`
- Hover background: `#1a1a1e`
- Font: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Monospace (for code/file names): `"SF Mono", "Fira Code", monospace`
- CSS reset at top of every `<style>` block:
  `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
- Centered `.card` / `.page` container, `max-width` typically `480px`
  (wider, e.g. `640px`–`680px`, for content-heavy pages like checklists and
  downloads)
- Xarpus logo: `https://oldschool.runescape.wiki/images/Xarpus.png?a39b0`
  (96x96, `image-rendering: pixelated`) — used on hub/landing pages
- Item rows (`.item` / `.download-item`): bordered rounded boxes
  (`border-radius: 8px`), icon + name + description, hover effects on
  border/background/text color (transitions ~0.15s)
- A `.back` link (`← back`) near the top of every non-root page, pointing to
  its parent hub
- Discord contact footer `discord @lkurusa` on top-level hub pages

### Conventions to follow when adding/editing pages

- Match the existing dark color palette and spacing exactly — don't
  introduce new colors or a light theme.
- Keep pages dependency-free: no CDN frameworks, no build tooling. Plain
  HTML/CSS/JS only.
- Reuse the `.back`, `.card`/`.page`, `.item`/`.group-items` patterns from
  similar existing pages instead of inventing new layout primitives.
- Tool/simulator pages tend to use `<title>Name — xarp.us</title>` or
  `<title>Name · xarp.us</title>` formatting; checklist pages use
  "X Checklist Review — xarp.us" style titles.
- `rl-proxy-worker.js` is a Cloudflare Worker, not a normal site asset — if
  modifying it, remember it must be deployed to Cloudflare separately (it
  is not served via GitHub Pages).
- Files in `/raw/` are reference/working scripts, not site content; they
  don't need to follow the HTML/CSS conventions above.

## Development workflow

- There is no local dev server, build step, or test command. Edit HTML
  files directly and open them in a browser (e.g. `file:///...` or any
  static file server) to preview.
- Changes pushed to the default branch go live on GitHub Pages
  automatically (subject to GitHub Pages' own build/propagation delay).
- Verify pages render correctly and that interactive JS (calculators,
  simulators, copy/download buttons) still works after edits — there are no
  automated tests to catch regressions.
