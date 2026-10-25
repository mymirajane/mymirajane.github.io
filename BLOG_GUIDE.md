# Mirajane's bubbly Markdown blog

This site is a static generator: each Markdown file in `content/` becomes a clean URL inside `public/`. GitHub Pages serves the generated files, so there is no database or server to maintain.

## 1. Write a new post

Copy `content/tiny-bayesian-notes.md`, give the file a memorable name, and edit the frontmatter. The fields below are the ones the generator reads:

```markdown
---
title: "A friendly note about Monte Carlo Dropout"
date: 2026-10-25
slug: friendly-monte-carlo-dropout
type: writing
description: "A visual explanation of repeated stochastic predictions."
tags: [bayesian, python, uncertainty]
draft: false
---

The posterior is written as $p(\theta \mid D)$, and a displayed equation can
use two dollar signs:

$$
\mathbb{E}[y \mid x, D] \approx \frac{1}{T}\sum_{t=1}^{T} f_{\theta_t}(x).
$$

Here is a Python example. The language name after the opening fence enables
Prism highlighting:

```python
import numpy as np

def mc_mean(model, x, samples=32):
    predictions = [model(x, training=True) for _ in range(samples)]
    return np.mean(np.stack(predictions), axis=0)
```
```

Use `draft: true` while a post is private. The build skips drafts. If `slug` is omitted, the filename is converted into a lowercase hyphenated URL. `type` can be `writing`, `note`, or `link`.

The generated article page loads MathJax from a CDN for LaTeX and Prism.js from a CDN for fenced code blocks. The page still contains useful text if either CDN is unavailable.

## 2. Preview locally

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build.py
python -m http.server 8000 --directory public
```

Open <http://localhost:8000/>. The build clears and recreates `public/`, so edit Markdown and templates instead of editing generated HTML.

## 3. Publish with GitHub Pages

The repository already includes `.github/workflows/pages.yml`. It runs `build.py` on every push to `main`, uploads `public/`, and deploys it with GitHub Pages.

1. Create the repository on GitHub (for this site it is `mymirajane/mymirajane.github.io`) and make sure the default branch is `main`.
2. In **Settings → Pages**, choose **GitHub Actions** as the source.
3. Commit your new post and push it:

```powershell
git add content/my-new-post.md templates build.py BLOG_GUIDE.md
git commit -m "Add a new note"
git push origin main
```

4. Open the **Actions** tab and wait for **Build and deploy Mirajane** to finish. The post will be available at `https://mymirajane.github.io/<slug>/`.

The workflow also writes `feed.xml`, `sitemap.xml`, and `robots.txt` into `public/` so search engines can discover the posts. After connecting `mymirajane.com`, update `SITE["url"]` in `build.py` to `https://mymirajane.com` and push once more.

## 4. Customize the personality

- Edit the CSS in `templates/base.html` to change the pastel palette, animations, or rounded cards.
- Change the ASCII computer in `templates/index.html` to a cat, cup of tea, or any tiny mascot.
- Add social links and update the bio in the `SITE` dictionary at the top of `build.py`.
- Put images in `assets/` and reference them from Markdown with a root-relative path such as `![a diagram](/assets/diagram.png)`.
