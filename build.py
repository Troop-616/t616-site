import os
import re
import shutil
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
PAGES_DIR = BASE_DIR / "pages"
OUTPUT_DIR = BASE_DIR / "docs"

# Source paths
SRC_ASSETS = BASE_DIR / "assets"
SRC_CSS = BASE_DIR / "style.css"

# Destination paths
DEST_ASSETS = OUTPUT_DIR / "assets"
DEST_CSS = OUTPUT_DIR / "style.css"

pages = [
    {
        "filename": "index.html",
        "title": "Home",
        "active_key": "index_active",
        "body_file": "index.body.html"
    },
    {
        "filename": "about-us.html",
        "title": "About Us",
        "active_key": "about_active",
        "body_file": "about-us.body.html"
    },
    {
        "filename": "resources.html",
        "title": "Resources",
        "active_key": "resources_active",
        "body_file": "resources.body.html"
    },
    {
        "filename": "links.html",
        "title": "Useful Links",
        "active_key": "links_active",
        "body_file": "links.body.html"
    },
    {
        "filename": "t616-eagle-scout-stories.html",
        "title": "Eagle Scout Stories",
        "active_key": "eagle_active",
        "body_file": "t616-eagle-scout-stories.body.html"
    }
]

def copy_static_resources():
    # Ensure docs directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Copy style.css to docs/
    if SRC_CSS.exists():
        shutil.copy2(SRC_CSS, DEST_CSS)
        print("Copied style.css to docs/")
    else:
        print("Warning: style.css not found in root.")

    # Copy assets/ to docs/
    if SRC_ASSETS.exists():
        shutil.copytree(SRC_ASSETS, DEST_ASSETS, dirs_exist_ok=True)
        print("Copied assets/ to docs/")
    else:
        print("Warning: assets/ folder not found in root.")

def verify_links(fail_on_broken=False):
    """
    Scans the compiled HTML files inside docs/ to verify that all relative local links
    (like styles, other html pages, and documents in assets/) resolve to actual files.
    """
    broken_links = 0
    checked_links = 0

    # Regex to find links starting with assets/, style.css, or other html pages
    local_link_pattern = re.compile(r'(?:href|src)="((?:assets/|style\.css|[a-zA-Z0-9.-]+\.html)[^"]*)"')

    print("\n--- Verifying Compiled Links & Assets ---")
    for page in pages:
        filepath = OUTPUT_DIR / page["filename"]
        if not filepath.exists():
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        matches = local_link_pattern.findall(content)
        for link in matches:
            # Strip query parameters (?ver=...) or hash anchors (#...)
            clean_link = link.split('?')[0].split('#')[0]
            if not clean_link:
                continue

            checked_links += 1
            link_path = OUTPUT_DIR / clean_link

            if not link_path.exists():
                print(f"  ❌ BROKEN LINK in docs/{page['filename']}: {link}")
                broken_links += 1

    if broken_links > 0:
        print(f"⚠️  Verification finished: found {broken_links} broken links!")
        if fail_on_broken:
            print("❌ Exiting with error because --fail-on-broken was set.")
            sys.exit(1)
    else:
        print(f"✅ Verification success: checked {checked_links} links, 0 broken links.")

def scan_for_pii(fail_on_broken=False):
    """
    Scans source files in templates/ and pages/ to prevent accidentally posting
    PII (Personally Identifiable Information) like phone numbers and personal emails.
    """
    pii_found = 0

    # Matches common US phone number patterns: e.g. 123-456-7890, (123) 456-7890, 123.456.7890
    phone_pattern = re.compile(r'\b(?:\+?1[-.\s]?)?\(?[2-9]\d{2}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    # Matches standard emails
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b')

    # Whitelisted domains (generic organization/official domains are allowed)
    email_whitelist_domains = {
        "t616.org",
        "troop616.org",
        "troopwebhost.org",
        "shutterfly.com",
        "vimeo.com",
        "github.com",
        "scouting.org"
    }

    print("\n--- Scanning for PII (Personally Identifiable Information) ---")

    # Files to scan: all files in pages/ and templates/
    dirs_to_scan = [PAGES_DIR, TEMPLATES_DIR]
    files_to_scan = []
    for d in dirs_to_scan:
        if d.exists():
            files_to_scan.extend(d.glob("*.html"))

    # Include style.css
    if (BASE_DIR / "style.css").exists():
        files_to_scan.append(BASE_DIR / "style.css")

    for filepath in files_to_scan:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Scan for phone numbers
        phones = phone_pattern.findall(content)
        for phone in phones:
            print(f"  ⚠️  POTENTIAL PHONE NUMBER in {filepath.relative_to(BASE_DIR)}: '{phone}'")
            pii_found += 1

        # Scan for emails
        for match in email_pattern.finditer(content):
            full_email = match.group(0)
            domain = match.group(1).lower()
            if domain not in email_whitelist_domains:
                print(f"  ⚠️  POTENTIAL PERSONAL EMAIL in {filepath.relative_to(BASE_DIR)}: '{full_email}'")
                pii_found += 1

    if pii_found > 0:
        print(f"⚠️  PII Scan finished: found {pii_found} warnings.")
        print("   Please ensure no private scout/adult phone numbers or personal emails are committed.")
        if fail_on_broken:
            print("❌ Exiting with error because PII warnings were found in CI mode.")
            sys.exit(1)
    else:
        print("✅ PII Scan success: 0 personal emails or phone numbers detected.")

def check_file_sizes(fail_on_broken=False):
    """
    Scans the assets/ folder for any files exceeding reasonable size limits:
    - Documents (PDF, DOC, DOCX, ZIP): Max 15MB
    - Images and other assets: Max 3MB
    This prevents scouts from committing massive raw images or documents that bloat
    the Git repository and make the live website load slowly.
    """
    large_files = 0

    print("\n--- Checking Asset File Sizes ---")
    if not SRC_ASSETS.exists():
        print("✅ No assets folder found to check.")
        return

    for path in SRC_ASSETS.rglob("*"):
        if path.is_file():
            # Skip hidden files
            if path.name.startswith("."):
                continue

            try:
                size = path.stat().st_size
                ext = path.suffix.lower()

                # Documents (PDFs, presentations) get a larger limit than raw images
                if ext in {".pdf", ".doc", ".docx", ".zip", ".ppt", ".pptx"}:
                    limit = 15 * 1024 * 1024
                    limit_name = "15.00MB"
                else:
                    limit = 3 * 1024 * 1024
                    limit_name = "3.00MB"

                if size > limit:
                    size_mb = size / (1024 * 1024)
                    print(f"  ⚠️  LARGE FILE: {path.relative_to(BASE_DIR)} is {size_mb:.2f}MB (Max limit: {limit_name})")
                    large_files += 1
            except Exception as e:
                print(f"  ⚠️  Could not read file size for {path.name}: {e}")

    if large_files > 0:
        print(f"⚠️  Size check finished: found {large_files} files exceeding size limits.")
        print("   Please compress these images or PDFs before committing them to keep the site fast!")
        if fail_on_broken:
            print("❌ Exiting with error because large files were found in CI mode.")
            sys.exit(1)
    else:
        print("✅ Size check success: all assets are within size limits.")

def build_site(fail_on_broken=False):
    header_path = TEMPLATES_DIR / "header.html"
    footer_path = TEMPLATES_DIR / "footer.html"

    if not header_path.exists() or not footer_path.exists():
        print("Error: Header or Footer template missing.")
        return

    with open(header_path, 'r', encoding='utf-8') as f:
        header_template = f.read()

    with open(footer_path, 'r', encoding='utf-8') as f:
        footer_template = f.read()

    # Copy assets and styles first
    copy_static_resources()

    for page in pages:
        body_path = PAGES_DIR / page["body_file"]

        # If body file doesn't exist, create an empty one
        if not body_path.exists():
            with open(body_path, 'w', encoding='utf-8') as f:
                f.write(f"<!-- {page['title']} Body Content -->\n")
            print(f"Created empty body file: {page['body_file']}")

        with open(body_path, 'r', encoding='utf-8') as f:
            body_content = f.read()

        # Build header with active state
        header = header_template.replace("{{title}}", page["title"])

        # Set active classes
        keys = ["index_active", "about_active", "resources_active", "links_active", "eagle_active"]
        for key in keys:
            if key == page["active_key"]:
                header = header.replace(f"{{{{{key}}}}}", "active")
            else:
                header = header.replace(f"{{{{{key}}}}}", "")

        # Merge content
        full_html = header + "\n" + body_content + "\n" + footer_template

        output_path = OUTPUT_DIR / page["filename"]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"Built: docs/{page['filename']}")

    # Run the verification step automatically
    verify_links(fail_on_broken=fail_on_broken)
    scan_for_pii(fail_on_broken=fail_on_broken)
    check_file_sizes(fail_on_broken=fail_on_broken)

if __name__ == "__main__":
    fail_on_broken = "--fail-on-broken" in sys.argv
    build_site(fail_on_broken=fail_on_broken)
