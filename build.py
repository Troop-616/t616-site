import os
import re
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/jeff/git/httrack/t616-backup/t616-static")
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
        "filename": "photos.html",
        "title": "Photo Gallery",
        "active_key": "photos_active",
        "body_file": "photos.body.html"
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

def verify_links():
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
    else:
        print(f"✅ Verification success: checked {checked_links} links, 0 broken links.")

def build_site():
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
        keys = ["index_active", "about_active", "resources_active", "links_active", "photos_active", "eagle_active"]
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
    verify_links()

if __name__ == "__main__":
    build_site()
