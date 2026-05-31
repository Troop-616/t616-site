# ⚜️ Troop 616 Webadmin Handoff & Reference Guide

Welcome to the **Troop 616 Webadmin** role! This guide is designed to help you maintain the troop website, keep it updated with troop events, use AI tools (like Gemini/Antigravity or Cursor/Copilot) safely, and seamlessly hand off the role to the next scout at the end of your 6-month term.

---

## 📂 1. Website Architecture

This website is a **static site**. Instead of using complex software frameworks, it uses a simple Python script (`build.py`) to merge shared parts (like the top navigation header and footer) with page-specific body text.

### The File System: Where to Edit

```
t616-site/ (Git Repository Root)
├── build.py                # The Compiler (Translates template files into the website)
├── style.css               # The Source Stylesheet (Edit here for colors, fonts, margins)
├── .gitignore              # Tells git what files to ignore
├── .cursorrules            # System rules to guide AI assistants
│
├── templates/              # Shared layouts
│   ├── header.html         # Top navigation and logo (edit here to change menus)
│   └── footer.html         # Bottom directory, schedule, and copyright
│
├── pages/                  # Page body content (EDIT THESE FILES FOR CONTENT!)
│   ├── index.body.html     # Homepage content (upcoming events, welcome message)
│   ├── about-us.body.html  # Joining information, troop history, leadership
│   ├── resources.body.html # Patrol planners, worksheets, checklists
│   ├── links.body.html     # External scout links (BSA, Council, Scoutbook)
│   ├── photos.body.html    # Links and archives of photos (Shutterfly)
│   └── t616-eagle-scout-stories.body.html # History of Troop 616 Eagles
│
├── assets/                 # Original media and downloads
│   ├── images/             # Store images here (use JPG/PNG)
│   └── downloads/          # Store PDFs, forms, and worksheets here
│
└── docs/                   # COMPILED WEB DIRECTORY (DO NOT EDIT DIRECTLY!)
```

> [!WARNING]
> **NEVER EDIT FILES INSIDE THE `docs/` DIRECTORY!**
> The `docs/` folder is automatically generated and updated by `build.py`. Any direct edits you make inside `docs/` will be **permanently deleted** the next time the script runs or when GitHub deploys the website.

---

## 💻 2. Local Setup & Commands

To test and compile changes on your computer:

### Prerequisites

#### 1. Install Git
* **Mac**: Git is usually installed by default. To check, open the Terminal app and type `git --version`. If it prompts you to install command-line developer tools, click **Install**.
* **Windows**: Download and install [Git for Windows](https://git-scm.com/download/win).

#### 2. Install Python 3
* **Windows (Easiest Method)**:
  1. Open the **Microsoft Store** app on your computer.
  2. Search for **Python 3.12** (or the latest version) and click **Get / Install**.
  * *Note: Installing from the Microsoft Store is highly recommended because it automatically configures your system path, avoiding command-line setup errors!*
* **Mac (Easiest Method)**:
  1. Go to [python.org/downloads](https://www.python.org/downloads/).
  2. Click the button to download the latest installer for macOS.
  3. Run the installer package and follow the standard setup wizard.


### Step-by-Step Edit & Preview Flow
1. **Open Terminal**: Navigate to your project folder:
   ```bash
   cd path/to/t616-site
   ```
2. **Make your changes**: Edit files in `pages/`, `templates/`, or update `style.css`.
3. **Compile the site**:
   ```bash
   python3 build.py
   ```
   *This compiles files into `/docs` and automatically scans for broken links.*
4. **Start a local test server**:
   ```bash
   python3 -m http.server 8000 --directory docs
   ```
5. **Preview**: Open your web browser and go to `http://localhost:8000` to see your changes!
6. **Stop Server**: In the terminal, press `Ctrl + C` to stop the server when done.

---

## 🤖 3. Guidelines for Using AI Assistants

If you use AI coding assistants (like Google Gemini, ChatGPT, Cursor, Copilot, or Antigravity) to help you write code, add features, or update styling:

### Copy-Paste System Prompt for AIs
When starting a chat session with an AI, paste the following message first:

> "I am working on the static website for Boy Scout Troop 616. The site uses a custom Python compiler. 
> 
> CRITICAL RULES:
> 1. Do NOT make or suggest edits directly inside the `docs/` directory.
> 2. All body content edits must be made inside `pages/` (e.g. `pages/index.body.html`).
> 3. Layout changes must be made in `templates/header.html` or `templates/footer.html`.
> 4. Global CSS styles must be changed in the root `style.css`.
> 5. If you modify anything, remind me to run `python3 build.py` to compile changes."

---

## 🚀 4. Automated Deployment (GitHub Actions)

We have configured **GitHub Actions** to compile and deploy the site automatically!
* Every time you push a commit to the `main` branch on GitHub, a workflow runs in the background.
* It sets up Python, runs `python3 build.py --fail-on-broken`, and deploys the output directly to **GitHub Pages**.
* **Automatic Link Checking**: If you accidentally commit a broken link or reference a missing image, the GitHub Actions check will **fail** and alert you, preventing the broken version of the site from going live!

---

## 📋 5. The 6-Month Webadmin Rotation Checklist

At the end of your term, you must complete this handoff checklist with the incoming Webadmin to ensure a smooth transition.

### 📤 Phase 1: Outgoing Webadmin Checklist
- [ ] **Clean the Repository**: Make sure all local changes are fully tested, compiled with `python3 build.py`, verified with no broken links, and pushed to the `main` branch.
- [ ] **Invite Incoming Webadmin to GitHub**:
  1. Go to the GitHub repository.
  2. Click **Settings** -> **Collaborators**.
  3. Click **Add people** and invite the new Webadmin's GitHub username.
  4. Ensure they have **Admin** or **Write** access.
- [ ] **Schedule Handoff Meeting**: Schedule a 30-minute virtual or in-person meeting with the new Webadmin.

### 📥 Phase 2: Joint Handoff Meeting Checklist
- [ ] **Clone repository**: Help the incoming Webadmin clone the repository to their computer.
- [ ] **Run local build**: Verify they can run `python3 build.py` and start the local server `python3 -m http.server 8000 --directory docs`.
- [ ] **Review Project Structure**: Walk through the folders (`pages/`, `templates/`, `assets/`, `docs/`) and explain the core compiler rules.
- [ ] **Update Email Forwarder/Alias**: Log into the domain control panel (or contact the adult Webmaster) to update the destination of the `webadmin@t616.org` forwarder to point to the incoming Webadmin's personal email (and parents' emails).
- [ ] **TroopWebHost Credentials**: Confirm they have the necessary Scout/Adult Webadmin access level on **TroopWebHost** to update the calendar integration or custom pages if needed.
- [ ] **Submit Handoff Form**: Notify the Scoutmaster or Committee Webmaster that the handoff is complete.

---

## ⚜️ 6. Scout Quickstart: New to Code & Git?

If you have never written code or used Git before, do not worry! This website is a great place to start. Here is the easiest way to get set up:

### 1. Create a GitHub Account
1. Go to [github.com/join](https://github.com/join).
2. **Age Requirement**: You must be at least 13 years old to create a GitHub account. If you are younger, please set it up with your parent.
3. **Pick a Clean Username**: Choose a clean, semi-professional username (like `scout-coder-616` or `t616-webmaster`) that you can use on school projects or college applications later.

### 2. The Easiest Way to Use Git (GitHub Desktop)
Command-line Git is cool, but it can be confusing. The easiest, most visual way to manage your changes is **GitHub Desktop**:
1. Download and install **[GitHub Desktop](https://desktop.github.com/)** (Free for Mac/Windows).
2. Open the app and click **Sign in to GitHub.com**. It will open your web browser, ask you to log in, and authenticate automatically. No SSH keys or terminal configuration needed!
3. Click **Clone a repository** and choose `t616-website` (which you have write access to).
4. Now you can make edits, see exactly what lines of code changed in the app, type a summary of what you did, and click **Commit** and **Push** visually!

*If you prefer using the command line: Install the [GitHub CLI (`gh`)](https://cli.github.com/) and run `gh auth login`. It will log you in via the browser securely without needing SSH keys.*

### 3. Easiest and Free AI Coding Setup
To use AI coding tools to help you update the website:
* **Option A: VS Code + Browser AI (Easiest & 100% Free)**:
  1. Download **[Visual Studio Code (VS Code)](https://code.visualstudio.com/)** to edit files.
  2. Use a free AI chat like **Gemini** (gemini.google.com) or **Claude** (claude.ai) in your browser.
  3. Copy and paste the prompt template from [Section 3](#-3-guidelines-for-using-ai-assistants) of this guide into the browser chat, then paste your code and ask it to write updates.
* **Option B: GitHub Student Developer Pack (Free Copilot)**:
  * If you have a school-provided email address, you can apply for the **[GitHub Student Developer Pack](https://education.github.com/pack)**.
  * Once approved, you get **GitHub Copilot** (the industry-standard AI coding assistant) for **free**. You can install the GitHub Copilot extension directly inside VS Code!
* **Option C: Cursor IDE (Free Tier)**:
  * Download **[Cursor](https://www.cursor.com/)** (an AI-focused code editor). It has built-in AI chat and reads your `.cursorrules` file automatically. The free tier gives you 50 fast AI responses per month.

### 4. Golden Rules for New Webadmins
* **Don't panic!** Git is like a time machine. If you make a mistake, delete a file, or write buggy code, we can easily press "revert" and restore the site to how it looked yesterday. You cannot permanently break the website.
* **Test locally**: Always run `python3 build.py` locally and preview it on `http://localhost:8000` in your browser before committing.
* **Use Branches**: Instead of editing the `main` branch directly, create a branch (e.g. `add-campout-june`), make your edits, and open a **Pull Request (PR)** on GitHub. This lets other scouts or adults see your changes before they go live!

