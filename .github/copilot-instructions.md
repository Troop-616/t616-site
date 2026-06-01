# AI Coding Guidelines for Troop 616 Website

This project is a static site structured with a custom Python compiler. Follow these rules when modifying code.

---

## ⚠️ CRITICAL RULES (MUST READ FIRST)

1. **DO NOT edit HTML files inside the `docs/` folder directly** (`docs/index.html`, etc.).
   * The files in the `docs/` folder are **auto-generated** by `build.py`.
   * Any direct edits made to them will be **permanently overwritten** the next time `build.py` is run.
2. **Do NOT edit style.css or assets/ inside `docs/` directly**:
   * The styling is defined in the root `style.css` file. It is copied to `docs/style.css` automatically during build.
   * Media assets are stored in the root `assets/` directory. They are copied to `docs/assets/` automatically during build.
3. **Always edit content in `pages/` and templates in `templates/`**:
   * Page body content is inside `pages/*.body.html`.
   * The shared header is inside `templates/header.html`.
   * The shared footer is inside `templates/footer.html`.
4. **Always prompt the user to run uv run build.py** (or `python3 build.py`) after making changes so their final HTML output compiles.

---

## 🎨 Design System & Colors
* **Theme**: Boy Scouts / Outdoors aesthetic.
* **Color Palette**:
  * Primary (Forest Green): `#0A4F39`
  * Secondary (Scout Gold): `#E5A93B`
  * Text Color (Charcoal Dark): `#2b302a`
  * Background Color (Warm white/sand): `#fcfcfb`
  * Accent backgrounds: `#eef5f1` (light green) or `#fffcf6` (light gold)
* **Fonts**:
  * Headings: Montserrat (Google Font)
  * Body: Inter (Google Font)
* **Responsiveness**: Use CSS Flexbox/Grid. Mobile navigation is toggled via vanilla JS. Keep style sheets clean in the root `style.css`.

---

## 🛠️ Common Tasks

### To Add a Calendar Card or Event
1. Open `pages/index.body.html`.
2. Locate the `<div class="cards-grid">` section.
3. Duplicate one of the `<div class="card">` blocks, updating:
   * Event image src (`assets/images/...` - link works relatively relative to docs)
   * Badge text (`Meeting`, `Campout`, `Hike`, etc.)
   * Event Title, Date, and Description
   * Location metadata block at the bottom of the card.
4. Run `uv run build.py` (or `python3 build.py`).

### To Add a Downloadable Document
1. Save the document (PDF, DOC) in the root `assets/downloads/` with a clean lowercase snake_case filename.
2. Open `pages/resources.body.html`.
3. Locate the appropriate category (Camping, Advancement, or Leadership).
4. Add a `<div class="resource-item">` block using the following format:
   ```html
   <div class="resource-item">
     <div class="resource-info">
       <span class="resource-name">Your Document Name</span>
       <span class="resource-type">PDF Download</span>
     </div>
     <a href="assets/downloads/your_document_file.pdf" target="_blank" class="resource-btn" aria-label="Download PDF">⬇</a>
   </div>
   ```
5. Run `uv run build.py` (or `python3 build.py`).

### To Add a New Page to the Site
1. Create a body file inside `pages/`, named `pages/your-page.body.html`.
2. Open `templates/header.html` and add a list item with a template placeholder:
   ```html
   <li><a href="your-page.html" class="nav-link {{your_page_active}}">Your Page Title</a></li>
   ```
3. Open `templates/footer.html` and add a footer link:
   ```html
   <li><a href="your-page.html" class="footer-link">Your Page Title</a></li>
   ```
4. Open `build.py` and:
   * Add a page dictionary in the `pages = [...]` list.
   * Add your active page key (e.g. `your_page_active`) to the `keys = [...]` list inside the `build_site()` function.
5. Run `uv run build.py` (or `python3 build.py`) to generate the new page inside `/docs`.

---

## 🐍 Python Environment & Dependency Management

This project uses **astral-sh/uv** to manage packaging and dependencies.
* **requires-python**: `>=3.12`
* **Common Commands**:
  * Build the site: `uv run build.py` (or fallback to `python3 build.py`)
  * Sync events & photos from TroopWebHost: `uv run sync-twh-events`
  * Local setup: `uv sync` followed by `uv run playwright install chromium`
