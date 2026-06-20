# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for Boy Scout Troop 616, built with vanilla HTML/CSS/JS and a custom Python template compiler. No Node.js, no React, no build frameworks — the entire frontend is plain HTML. Hosted via GitHub Pages from the `docs/` directory.

## Commands

```bash
# One-time setup
uv sync
uv run playwright install chromium   # Only needed for event syncing

# Build the site (always run after any change)
uv run build.py

# Build with CI strictness (fails on broken links, PII, or oversized assets)
uv run build.py --fail-on-broken

# Preview locally
python3 -m http.server 8000 --directory docs
# Then open http://localhost:8000

# Sync upcoming events and past photo highlights from TroopWebHost
uv run sync-twh-events
```

Fallback if `uv` is unavailable: `python3 build.py` (after `pip install pyyaml beautifulsoup4`).

## CRITICAL: Never Edit `docs/`

**`docs/` is entirely auto-generated.** Every file in it — HTML pages, `style.css`, and `assets/` — is overwritten on every `build.py` run. Always edit the source files instead:

| What to change | Where to edit |
|---|---|
| Page body content | `pages/*.body.html` |
| Navigation menu / `<head>` | `templates/header.html` |
| Footer, meeting times | `templates/footer.html` |
| Styles | `style.css` (root) |
| Images, downloads | `assets/images/`, `assets/downloads/` |
| Upcoming events / highlights | `content/events.yaml`, `content/highlights.yaml` (or run sync) |

Always run `uv run build.py` after making changes to regenerate `docs/`.

## Architecture: Template Compilation System

`build.py` is the entire build pipeline. For each page defined in the `pages` list (top of `build.py`):

1. Reads `templates/header.html` and substitutes `{{title}}` and active-nav placeholders (`{{index_active}}`, `{{about_active}}`, etc.) with either `"active"` or `""`.
2. Reads the corresponding `pages/*.body.html` file.
3. Replaces `<!-- EVENTS_PLACEHOLDER -->` and `<!-- HIGHLIGHTS_PLACEHOLDER -->` comments in the body with HTML rendered from `content/events.yaml` and `content/highlights.yaml`.
4. Concatenates header + body + `templates/footer.html` and writes to `docs/<filename>.html`.

After building all pages, the script runs three validation passes automatically:
- **Link verification** — checks that all relative `href`/`src` paths resolve to real files in `docs/`
- **PII scan** — detects phone numbers and personal emails (whitelisted domains: `t616.org`, `troop616.org`, `troopwebhost.org`, `scouting.org`, `github.com`, `vimeo.com`)
- **File size check** — images/assets max 3 MB; PDFs/docs max 15 MB

## Adding a New Page

1. Create `pages/your-page.body.html`
2. Add a nav `<li>` to `templates/header.html` using `{{your_page_active}}` as the class placeholder
3. Add a footer link to `templates/footer.html`
4. Add an entry to the `pages` list in `build.py` and add `"your_page_active"` to the `keys` list inside `build_site()`
5. Run `uv run build.py`

## Adding a Downloadable Resource

Save the file in `assets/downloads/` (use lowercase snake_case filenames), then add a `<div class="resource-item">` block to `pages/resources.body.html`:

```html
<div class="resource-item">
  <div class="resource-info">
    <span class="resource-name">Document Name</span>
    <span class="resource-type">PDF Download</span>
  </div>
  <a href="assets/downloads/your_file.pdf" target="_blank" class="resource-btn" aria-label="Download PDF">⬇</a>
</div>
```

## Event Syncing

`src/t616_site/sync_twh_events.py` uses Playwright (headless Chromium) to scrape TroopWebHost's public page and write `content/events.yaml` and `content/highlights.yaml`. It caps output at 6 upcoming events and 6 highlights. A GitHub Actions workflow (`sync_events.yml`) runs this daily at 6:00 AM UTC and commits any changes, which triggers the deploy workflow automatically.

## Design System

Use these CSS variables (defined in `style.css`) — do not hardcode colors:

- Primary (Forest Green): `#0A4F39`
- Secondary (Scout Gold): `#E5A93B`
- Text (Charcoal Dark): `#2b302a`
- Background (Warm white): `#fcfcfb`
- Accent backgrounds: `#eef5f1` (light green), `#fffcf6` (light gold)
- Fonts: Montserrat (headings), Inter (body) — loaded from Google Fonts in the header template
- Layout: CSS Flexbox/Grid only; mobile nav toggled via vanilla JS in `templates/footer.html`

## Formatting Requirements (enforced by pre-commit)

- No trailing whitespace on any line
- Every file ends with exactly one `\n` (no blank trailing line)
- LF line endings only — no CRLF
- No files over 5 MB

## CI/CD

Two GitHub Actions workflows:
- **`deploy.yml`** — Triggered on push to `main`; runs `uv run build.py --fail-on-broken` then deploys `docs/` to GitHub Pages. Fails hard on broken links, PII, or oversized assets.
- **`sync_events.yml`** — Runs daily at 6:00 AM UTC; scrapes TroopWebHost, commits updated YAML files if changed, which then triggers `deploy.yml`.
