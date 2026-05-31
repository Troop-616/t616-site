# Boy Scout Troop 616 Website

Welcome to the official repository for the Troop 616 public website! This site is designed to be lightweight, responsive, and completely self-contained. It serves as a beautiful front page to welcome prospective families, while linking directly to **TroopWebHost (TWH)** for member management and the calendar, and **Shutterfly** for photo archives.

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
├── templates/              # Shared Layout Templates
│   ├── header.html         # Top navigation and logo (edit here to change menus)
│   └── footer.html         # Bottom directory, meeting schedule, and copyright
│
├── pages/                  # Page-specific Body Content (EDIT THESE!)
│   ├── index.body.html
│   ├── about-us.body.html
│   ├── resources.body.html
│   ├── links.body.html
│   ├── photos.body.html
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

### Step 1: Make your changes
* **To edit page content** (like adding a calendar event or updating text): Open the corresponding file in `pages/` (e.g., `pages/index.body.html`).
* **To change the logo or the navigation menu**: Edit `templates/header.html`.
* **To change the meeting times or footer links**: Edit `templates/footer.html`.
* **To update styles (colors, fonts, layout)**: Edit `style.css` in the root.
* **To add a new document to download**: Drop the file in the root `assets/downloads/` and link to it in `pages/resources.body.html` using `<a href="assets/downloads/filename.pdf">Download</a>`.

### Step 2: Compile the pages (locally for testing)
After saving your changes, open your terminal, navigate to this folder, and run:
```bash
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

## 🔗 TroopWebHost & Shutterfly Integration

This site is configured to link to **TroopWebHost** for all members-only portals and contact entries.
* **TWH Portal & Login link**: Custom button in the header nav bar and footer.
* **TWH Contact link**: Pointed to the official TroopWebHost contact form.
* **TWH Calendar link**: Pointed to the TWH page.
* **Photos Portal**: Instructions and portal buttons point to your Shutterfly site (`http://troop616.shutterfly.com/`).

If your TroopWebHost subdomain or URL changes in the future, you only need to update the links in the following files:
* `templates/header.html` (the TroopWebHost Login button)
* `templates/footer.html` (the TroopWebHost Portal link)
* `pages/index.body.html` (the "Contact Us" buttons)

---

## 🚀 Hosting & Automated Deployment

This website is hosted on **GitHub Pages** and is automatically built and deployed via **GitHub Actions** on every push to the `main` branch.

### Setting Up GitHub Pages
1. Go to your repository settings on GitHub.
2. Click **Pages** in the left sidebar.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions** (instead of *Deploy from a branch*).
4. That's it! GitHub Actions will run `build.py` automatically, verify all links are correct, and push the live version to the internet.

For a detailed walkthrough on setting up local environments, using AI assistants, and completing the 6-month Webadmin role transition, see the [Scout Webadmin Handoff & Reference Guide](WEBADMIN_GUIDE.md).
