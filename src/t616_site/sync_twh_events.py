#!/usr/bin/env python3
"""
sync_twh_events.py — Scrapes Troop 616's public TroopWebHost page and writes
upcoming events and recent photo highlights to YAML data files for the static site.

Usage:
    python3 scripts/sync_twh_events.py [--dry-run]

Requirements:
    pip install playwright beautifulsoup4 pyyaml
    python3 -m playwright install chromium

Run weekly via GitHub Actions (.github/workflows/sync_events.yml).
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Run: pip install pyyaml")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 required. Run: pip install beautifulsoup4")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright required. Run: pip install playwright && python3 -m playwright install chromium")
    sys.exit(1)

# ── Constants ─────────────────────────────────────────────────────────────────

TWH_URL = "https://www.TroopWebHost.org/Index.aspx?Application_ID=3588"
TWH_BASE = "https://www.troopwebhost.org"
REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
EVENTS_FILE = CONTENT_DIR / "events.yaml"
HIGHLIGHTS_FILE = CONTENT_DIR / "highlights.yaml"

# How many upcoming events to include in the homepage cards
MAX_UPCOMING = 6
# How many past photo highlights to include
MAX_HIGHLIGHTS = 6

# Badge labels derived from event name keywords
BADGE_MAP = {
    "camp": "Campout",
    "backpack": "Backpack",
    "hike": "Hike",
    "meeting": "Meeting",
    "eagle": "Eagle",
    "celebration": "Celebration",
    "anniversary": "Celebration",
    "merit": "Merit Badge",
    "court": "CoH",
    "honor": "CoH",
    "swim": "Swim",
    "kayak": "Kayak",
    "canoe": "Kayak",
}

DEFAULT_BADGE = "Event"


def badge_for(title: str) -> str:
    title_lower = title.lower()
    for keyword, badge in BADGE_MAP.items():
        if keyword in title_lower:
            return badge
    return DEFAULT_BADGE


def fetch_page_html() -> str:
    """Launch a headless browser, navigate the TWH redirect chain, return full HTML."""
    print("Launching headless browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(TWH_URL, wait_until="networkidle", timeout=30000)
        # Wait for any AJAX content to settle
        page.wait_for_timeout(8000)
        print(f"  Landed on: {page.url}")
        html = page.content()
        browser.close()
    print(f"  Page size: {len(html):,} bytes")
    return html


def parse_upcoming_events(soup: BeautifulSoup) -> list[dict]:
    """Extract upcoming events from the widget table under the 'Upcoming Events' heading."""
    events = []

    # Find the h3 heading, then the table immediately after it
    heading = soup.find("h3", string=re.compile(r"Upcoming Events", re.I))
    if not heading:
        print("  ⚠️  'Upcoming Events' heading not found")
        return events

    table = heading.find_next("table")
    if not table:
        print("  ⚠️  Upcoming events table not found after heading")
        return events

    rows = table.find_all("tr")
    print(f"  Found {len(rows)} upcoming event rows")

    for row in rows[:MAX_UPCOMING]:
        p = row.find("p")
        if not p:
            continue
        bold = p.find("b")
        if not bold:
            continue
        title = bold.get_text(strip=True)

        # Date is the text node(s) in the <p> after stripping the <b> tag
        # Format examples: "(May 31 2026  7:00PM)" or "(Jun 09, 2026)"
        raw = p.get_text(" ", strip=True)
        date_match = re.search(r"\(([^)]+)\)", raw)
        date_text = date_match.group(1).strip() if date_match else ""

        # Normalize date to a cleaner display string
        date_display = re.sub(r"\s+", " ", date_text)

        events.append({
            "title": title,
            "badge": badge_for(title),
            "date": date_display,
            "description": f"Join us for {title}. Log in to TroopWebHost for full details and sign-up.",
            "location": "See TroopWebHost for location details",
            "image": "",
            "source_url": TWH_URL,
        })

    return events



def parse_photo_highlights(soup: BeautifulSoup) -> list[dict]:
    """Extract recent past events with photos from the photo gallery section."""
    highlights = []

    # Photos are <a> tags linking to FormDetail.aspx containing an <img> with a blob URL
    photo_links = soup.find_all(
        "a",
        href=re.compile(r"FormDetail\.aspx.*Form_ID=182"),
        limit=MAX_HIGHLIGHTS * 2   # grab extra in case some have no img
    )
    print(f"  Found {len(photo_links)} photo gallery links")

    for link in photo_links:
        img = link.find("img")
        if not img:
            continue

        img_src = img.get("src", "")
        alt_text = img.get("alt", "").strip()

        # alt format: "Event Name (MM/DD/YY)" — split off the date
        date_match = re.search(r"\((\d{2}/\d{2}/\d{2,4})\)\s*$", alt_text)
        if date_match:
            date_str = date_match.group(1)
            event_name = alt_text[: date_match.start()].strip()
            # Parse and reformat the date
            try:
                dt = datetime.strptime(date_str, "%m/%d/%y")
                date_display = dt.strftime("%b %d, %Y")
            except ValueError:
                try:
                    dt = datetime.strptime(date_str, "%m/%d/%Y")
                    date_display = dt.strftime("%b %d, %Y")
                except ValueError:
                    date_display = date_str
        else:
            event_name = alt_text
            date_display = ""

        # Convert thumbnail URL to full-size URL (remove /Thumbnails/ path)
        full_img_url = img_src.replace("/Thumbnails/", "/")

        href = link.get("href", "")
        detail_url = f"{TWH_BASE}/{href}" if href and not href.startswith("http") else href

        highlights.append({
            "title": event_name,
            "date": date_display,
            "badge": badge_for(event_name),
            "image": img_src,          # thumbnail URL (already on Azure CDN)
            "image_full": full_img_url,
            "source_url": detail_url,
        })

        if len(highlights) >= MAX_HIGHLIGHTS:
            break

    return highlights


def load_existing_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: dict, dry_run: bool = False) -> None:
    content = yaml.dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    if dry_run:
        print(f"\n  [DRY RUN] Would write {path.name}:")
        print(content[:800])
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ Wrote {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync events from TroopWebHost")
    parser.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    args = parser.parse_args()

    print("=" * 60)
    print("TroopWebHost Event Sync")
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)

    # ── Fetch page ────────────────────────────────────────────────────────────
    html = fetch_page_html()
    soup = BeautifulSoup(html, "html.parser")

    # ── Parse upcoming events ─────────────────────────────────────────────────
    print("\n📅 Parsing upcoming events...")
    upcoming = parse_upcoming_events(soup)
    print(f"  Parsed {len(upcoming)} upcoming events")
    for e in upcoming:
        print(f"    • {e['date']:20s} {e['title']}")

    # ── Parse past event photo highlights ─────────────────────────────────────
    print("\n📸 Parsing past event photo highlights...")
    highlights = parse_photo_highlights(soup)
    print(f"  Parsed {len(highlights)} highlights")
    for h in highlights:
        print(f"    • {h['date']:15s} {h['title']}")

    # ── Write YAML files ──────────────────────────────────────────────────────
    print("\n💾 Writing YAML files...")

    # Events file — Dict format with metadata: {events: [...]}
    events_data = {
        "events": upcoming,
        "_synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_source": TWH_URL,
    }
    write_yaml(EVENTS_FILE, events_data, dry_run=args.dry_run)

    # Highlights file — separate from manually curated events
    highlights_data = {
        "highlights": highlights,
        "_synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_source": TWH_URL,
    }
    write_yaml(HIGHLIGHTS_FILE, highlights_data, dry_run=args.dry_run)

    print("\n✅ Sync complete!")


if __name__ == "__main__":
    main()
