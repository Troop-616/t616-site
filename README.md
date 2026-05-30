# Boy Scout Troop 616 — Static Website

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

This site uses a **template compiler** so that you don't have to copy-paste the header and footer navigation menus onto every single page. 

### Step 1: Make your changes
* **To edit page content** (like adding a calendar event or updating text): Open the corresponding file in `pages/` (e.g. `pages/index.body.html`).
* **To change the logo or the navigation menu**: Edit `templates/header.html`.
* **To change the meeting times or footer links**: Edit `templates/footer.html`.
* **To update styles (colors, fonts, layout)**: Edit `style.css` in the root.
* **To add a new document to download**: Drop the file in the root `assets/downloads/` and link to it in `pages/resources.body.html` using `<a href="assets/downloads/filename.pdf">Download</a>`.

### Step 2: Compile the pages
After saving your changes, open your terminal/command prompt, navigate to this folder, and run:
```bash
python3 build.py
```
This will:
1. Merge your body content with the header/footer templates and save the compiled HTML pages inside the `/docs` folder.
2. Automatically copy your `style.css` and the entire `assets/` folder (images & downloads) into the `/docs` folder.

*Note: You never need to edit files in `docs/` directly.*

### Step 3: Preview locally
You can preview your changes exactly as they will look on the internet by starting a local web server:
```bash
python3 -m http.server 8000 --directory docs
```
Then, open your web browser and go to `http://localhost:8000`. When you're done, press `Ctrl + C` in the terminal to stop the server.

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

## 🚀 How to Host on GitHub Pages (Free)

GitHub Pages is 100% free and is the perfect platform for this website.

1. **Create a GitHub Repository**: Create a new public or private repository on GitHub (e.g., `t616-website`).
2. **Push the Code**: Initialize git in the `t616-static` folder, commit your files, and push them to GitHub.
3. **Enable GitHub Pages**:
   * Go to your repository settings on GitHub.
   * Click **Pages** in the left sidebar.
   * Under "Build and deployment", select **Deploy from a branch** and choose `main` (or `master`) and change the folder option to **`/docs`** (instead of `/(root)`).
   * Click **Save**.
4. **Point your Custom Domain**:
   * Under the GitHub Pages settings, add your custom domain: `t616.org`.
   * Configure your domain registrar (GoDaddy, Google Domains, etc.) to point `t616.org` to GitHub's DNS IP addresses.
