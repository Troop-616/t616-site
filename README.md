# Boy Scout Troop 616 Website

Welcome to the official repository for the Troop 616 public website! This site is designed to be lightweight, responsive, and completely self-contained. It serves as a beautiful front page to welcome prospective families, while linking directly to **TroopWebHost (TWH)** for member management, the calendar, and photo archives.

This codebase is built using **Vanilla HTML and CSS** (no heavy frameworks like React, Node, or Vite) making it extremely fast, easy to learn, and 100% free to host.

---

## 📂 Project Structure

To keep the repository clean, the source files are kept in the root, and the compiled site output goes into the **`docs/`** folder. The `docs/` folder is what is actually hosted on the internet!

```
t616-static/ (Git Root)
├── build.py                # Python compiler (run this to build pages)
├── style.css               # Source global stylesheet (styles pages & layout)
├── .gitignore              # Tells git to ignore cache files
├── .cursorrules            # Instructions for AI assistants (like Cursor/Copilot)
│
├── content/                # Dynamic Data Files (Auto-updated from TroopWebHost)
│   ├── events.yaml         # Sync'ed upcoming events
│   └── highlights.yaml     # Sync'ed past adventure photos
│
├── src/                    # Python Source Files
│   └── t616_site/          # Main project package
│       ├── __init__.py     # Declares the package namespace
│       └── sync_twh_events.py # Playwright sync script to scrape TroopWebHost
│
├── templates/              # Shared Layout Templates
│   ├── header.html         # Top navigation and logo (edit here to change menus)
│   └── footer.html         # Bottom directory, meeting schedule, and copyright
│
├── pages/                  # Page-specific Body Content (EDIT THESE!)
│   ├── index.body.html
│   ├── about-us.body.html
│   ├── resources.body.html
│   ├── links.body.html
│   └── t616-eagle-scout-stories.body.html
│
├── assets/                 # Source Media Assets (images & documents)
│   ├── images/             # Logos, banner photos, and icons
│   └── downloads/          # Patrol planners, checklists, merit badge guides
│
└── docs/                   # COMPILED/HOSTED DIRECTORY (Auto-updated by build.py)
    ├── index.html          # Main HTML pages merged with headers & footers
    ├── about-us.html       # ...
    ├── style.css           # Automatically copied by compiler
    └── assets/             # Automatically copied by compiler
```

---

## 🛠️ How to Edit the Website (For Scouts)

This site uses a template compiler so that you don't have to copy-paste the header and footer navigation menus onto every single page.

### Initial Setup (One-time)
Before making edits locally, set up the project dependencies in your terminal:
```bash
# Option A: Using uv (Recommended)
uv sync

# Option B: Using standard Python (Fallback)
python3 -m pip install pyyaml
```

### Step 1: Make your changes
* **To edit page content** (like adding a resource or updating text): Open the corresponding file in `pages/` (e.g., `pages/resources.body.html`).
* **To change the logo or the navigation menu**: Edit `templates/header.html`.
* **To change the meeting times or footer links**: Edit `templates/footer.html`.
* **To update styles (colors, fonts, layout)**: Edit `style.css` in the root.
* **To add a new document to download**: Drop the file in the root `assets/downloads/` and link to it in `pages/resources.body.html` using `<a href="assets/downloads/filename.pdf">Download</a>`.

### Step 2: Compile the pages (locally for testing)
After saving your changes, open your terminal, navigate to this folder, and run:
```bash
# Recommended (using uv):
uv run build.py

# Fallback (standard Python):
python3 build.py
```
This will merge your body content with templates and save them inside the `docs/` folder, and check for any broken local links. *Note: You never need to edit files in `docs/` directly.*

### Step 3: Preview locally
You can preview your changes exactly as they will look on the internet by starting a local web server:
```bash
python3 -m http.server 8000 --directory docs
```
Then, open your web browser and go to `http://localhost:8000`. Press `Ctrl + C` in the terminal to stop the server when done.

---

## 🔄 Dynamic Event Syncing

The homepage displays two sections dynamically loaded from the troop's official **TroopWebHost** portal:
1. **Upcoming Meetings & Outings** (derived from upcoming calendar events)
2. **Highlights from Past Adventures** (derived from recent past events containing photo gallery uploads)

### How it works:
* A background sync script (**`src/t616_site/sync_twh_events.py`**) launches a headless browser (via Playwright) to navigate the troop's public page, scrape events and high-resolution photo gallery details, and write them to the data files in `content/`.
* A **GitHub Actions Workflow** (`sync_events.yml`) runs this scraper automatically **every day at 6:00 AM UTC**.
* If any new events or photos are detected, it commits them directly to the repository and triggers a rebuild/deploy workflow automatically.

### Running a Manual Sync:
If you need to force an immediate sync of events/photos, you can run the sync script manually from your local command line:

#### Option A: Using uv (Recommended)
1. Initialize the virtual environment and fetch chromium browser:
   ```bash
   uv sync
   uv run playwright install chromium
   ```
2. Run the sync and rebuild:
   ```bash
   uv run sync-twh-events
   uv run build.py
   ```

#### Option B: Using standard Python (Fallback)
1. Install dependencies for your interpreter:
   ```bash
   python3 -m pip install playwright beautifulsoup4 pyyaml
   python3 -m playwright install chromium
   ```
2. Run the sync and rebuild:
   ```bash
   python3 src/t616_site/sync_twh_events.py
   python3 build.py
   ```

---

## 🚀 Hosting & Automated Deployment

This website is hosted on **GitHub Pages** and is automatically built and deployed via **GitHub Actions** on every push to the `main` branch.

For a detailed walkthrough on setting up local environments, using AI assistants, and completing the 6-month Webadmin role transition, see the [Scout Webadmin Handoff & Reference Guide](WEBADMIN_GUIDE.md).
