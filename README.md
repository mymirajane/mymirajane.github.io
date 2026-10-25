# Mirajane blog on GitHub Pages

This is Mirajane's bubbly, pastel personal blog. A small Python generator converts Markdown in `content/` into static pages in `public/`. GitHub Actions builds and publishes the site on every push to `main`. It uses only Python-Markdown and Jinja2 beyond the standard library; Jekyll is not required. The templates include MathJax for LaTeX, Prism.js for fenced code, ASCII art, and small CSS animations.

For the complete writing and deployment walkthrough, read [`BLOG_GUIDE.md`](BLOG_GUIDE.md).

## Add writing

Copy `content/sample-post.md` to a new `.md` file, change its title/date/body, and set `draft: false` when ready. Optional `slug` sets the clean URL; otherwise the filename becomes the slug. Set `type: writing`, `note`, or `link` for the home-page section. Frontmatter uses simple, one-line YAML values. For images, put files in `assets/` and use root-relative Markdown paths such as `![Alt text](/assets/photo.jpg)`.

## Build locally

In PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build.py
python -m http.server 8000 --directory public
```

Open `http://localhost:8000/`. On macOS or Linux, use `.venv/bin/python`. Each build replaces `public/`. Do not edit generated files there.

## Publish

Commit and push the Markdown change to `main`. The workflow at `.github/workflows/pages.yml` builds and deploys the site. In repository **Settings → Pages**, choose **GitHub Actions** as the build source. The default address is `https://mymirajane.github.io/`.

The author name, bio, projects, optional social links, and canonical site URL are in the `SITE` dictionary near the top of `build.py`.

## Use mymirajane.com after registering it

First add `mymirajane.com` in **Settings → Pages → Custom domain**. Then point its DNS to GitHub Pages using the current values in [GitHub's custom-domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). For the root domain, GitHub currently lists four A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`. For `www`, use a CNAME to `mymirajane.github.io`. Do not use the earlier Sites A/TXT records for this GitHub setup.

Once HTTPS is active, change `SITE["url"]` to `https://mymirajane.com` and push again. That updates RSS, sitemap, robots.txt, and canonical URLs. Domain registration and DNS changes happen at your registrar; they are not part of the repository.
