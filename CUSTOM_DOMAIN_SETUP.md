# Custom Domain Setup: t616.org

Instructions for pointing `t616.org` to this GitHub Pages site when ready.

The site is structurally prepared — all internal links use relative paths and
there are no hardcoded references to `troop-616.github.io`. No template or page
edits are needed; just the three steps below.

---

## Step 1: Add a CNAME file (code change)

GitHub Pages requires a `CNAME` file in the deployed output to know which custom
domain to serve.

Create a file named `CNAME` in the repository root containing only the domain:

```
t616.org
```

Then open `build.py` and add the following line inside `copy_static_resources()`,
after the `style.css` copy block:

```python
if (BASE_DIR / "CNAME").exists():
    shutil.copy2(BASE_DIR / "CNAME", OUTPUT_DIR / "CNAME")
```

Commit and push both files. The next deploy will include `CNAME` in `docs/`.

---

## Step 2: Configure GitHub Pages (repo settings)

1. Go to the repository on GitHub.
2. Click **Settings → Pages**.
3. Under **Custom domain**, enter `t616.org` and click **Save**.
4. GitHub will verify the domain and provision an HTTPS certificate automatically
   via Let's Encrypt. This usually takes a few minutes.
5. Once the certificate is ready, check **Enforce HTTPS**.

---

## Step 3: Configure DNS on GoDaddy

Log in to GoDaddy and open the DNS settings for `t616.org`.

### Apex domain (t616.org)

Add four A records pointing to GitHub Pages' servers:

| Type | Name | Value           | TTL  |
|------|------|-----------------|------|
| A    | @    | 185.199.108.153 | 1hr  |
| A    | @    | 185.199.109.153 | 1hr  |
| A    | @    | 185.199.110.153 | 1hr  |
| A    | @    | 185.199.111.153 | 1hr  |

### www subdomain (optional)

To redirect `www.t616.org` to the apex domain, add:

| Type  | Name | Value                    | TTL  |
|-------|------|--------------------------|------|
| CNAME | www  | troop-616.github.io      | 1hr  |

DNS propagation typically takes a few minutes to a few hours.

---

## Verification

Once DNS has propagated and the GitHub Pages certificate is issued:

1. Visit `https://t616.org` — the site should load with a valid padlock.
2. Visit `http://t616.org` — should redirect to `https://t616.org` automatically.
3. If you added the www CNAME, visit `https://www.t616.org` — should also redirect.

If the site doesn't load after a few hours, check:
- The `CNAME` file exists in `docs/` after a build (`uv run build.py`)
- GitHub Pages shows "DNS check successful" in Settings → Pages
- GoDaddy shows the four A records saved correctly (no duplicates with old records)
