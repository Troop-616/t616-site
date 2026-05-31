# 📋 GitHub Setup & Launch Checklist

This checklist contains the remaining administrative setup steps required on GitHub to get the Troop 616 website live and secure for Scout management.

---

## 🏢 Step 1: Create a GitHub Organization (Highly Recommended)
- [ ] Go to [github.com/organizations/plan](https://github.com/organizations/plan).
- [ ] Select the **Free Plan**.
- [ ] Choose an organization name (e.g. `scout-troop-616` or `troop616-sd`).
- [ ] Add at least one other adult leader (e.g. Committee Chair or Scoutmaster) as an **Owner** for redundancy.
- [ ] **Set up a Relay/Forwarder Email**: Create a generic forwarder (e.g. `webadmin@t616.org`) through your domain registrar or host. Configure it to forward to your email and/or the active Scout Webadmin's email. Use this address for any shared accounts to avoid tying them to personal email accounts.

---

## 📦 Step 2: Create and Push the Repository
- [ ] Inside your new Organization, click **New repository**.
- [ ] Name it `website` or `t616-website`.
- [ ] Set visibility to **Public** (required for free GitHub Pages hosting).
- [ ] Leave "Add README", ".gitignore", and "License" unchecked (we already have them).
- [ ] Open your terminal inside this folder and run:
  ```bash
  git add .
  git commit -m "chore: setup scout webadmin compiler and deployment actions"
  git remote add origin https://github.com/<your-org-name>/<your-repo-name>.git
  git branch -M main
  git push -u origin main
  ```

---

## 🌐 Step 3: Enable GitHub Pages
- [ ] In your new GitHub repository, click **Settings** along the top menu.
- [ ] Click **Pages** in the left sidebar under "Code and automation".
- [ ] Under **Build and deployment** -> **Source**, select **GitHub Actions** from the dropdown menu.
  * *Note: The deployment will run automatically on your next push, or you can trigger it manually under the "Actions" tab.*
- [ ] (Optional) Under **Custom domain**, type your domain `t616.org` and follow the instructions to update your DNS provider settings.

---

## 🛡️ Step 4: Protect the `main` Branch
This prevents scouts from accidentally breaking the live site by pushing buggy code directly to `main`.
- [ ] In your repository settings, click **Branches** in the left sidebar.
- [ ] Click **Add branch protection rule** (or click **Add rule**).
- [ ] Set **Branch pattern name** to `main`.
- [ ] Check **Require a pull request before merging**.
- [ ] Check **Require status checks to pass before merging**.
  - In the search box that appears below it, search for **`build`** (this is the build/link check job defined in `.github/workflows/deploy.yml`). Select it.
- [ ] Click **Save changes** at the bottom of the page.

---

## 👥 Step 5: Onboard the Scout Webadmin
- [ ] In repository settings, click **Collaborators** (or **Manage access**).
- [ ] Click **Add people** and invite the Scout Webadmin's GitHub username.
- [ ] Give them **Write** permission (this allows them to push branches and open Pull Requests).
- [ ] Show them the [WEBADMIN_GUIDE.md](WEBADMIN_GUIDE.md) to help them get set up locally.
