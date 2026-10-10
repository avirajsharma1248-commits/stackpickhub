# StackPick

SEO-ready static website: AI tool overviews, guides and comparisons for US small businesses.
No frameworks and no JavaScript. `build.py` generates every page into `public/`.

## Folder map
- `build.py` – generates the whole site (edit content here)
- `public/` – the finished website (generated)
- `CONTENT_PLAN.md` – 30 article topics and a weekly routine
- `.github/workflows/deploy.yml` – publishes the site to GitHub Pages automatically

## Publish on GitHub Pages (free)
1. Create a GitHub repository. Use a custom domain, or name the repo `YOURUSERNAME.github.io`.
   (Links start with `/`, so the site must be served from a domain root, not `username.github.io/repo-name/`.)
2. Upload all files from this folder (keep the `.github` folder).
3. Repo **Settings > Pages > Source: GitHub Actions**.
4. Repo **Settings > Secrets and variables > Actions > Variables > New repository variable**:
   name `SITE_DOMAIN`, value `https://yourdomain.com` (or `https://YOURUSERNAME.github.io`).
5. Go to the **Actions** tab, open "Deploy to GitHub Pages" and click **Run workflow**. Your site goes live in a minute or two.
6. Custom domain: in your domain's DNS add the records GitHub lists under Settings > Pages, then tick "Enforce HTTPS".

## Add affiliate links
In `build.py` find `AFF = {}` and set e.g. `AFF = {"canva": "https://your-affiliate-link"}`. Commit; the site rebuilds itself.

## Get on Google
1. Add your site at search.google.com/search-console.
2. Submit `https://yourdomain.com/sitemap.xml`.
3. Request indexing for the home page.

## Before launch
- Put your real contact email on the About page (`build.py`, search "Contact").
- Check each tool's current free plan and price on its official site.
- Publish new guides regularly; see `CONTENT_PLAN.md`.

## Build locally
    DOMAIN=https://yourdomain.com python3 build.py
