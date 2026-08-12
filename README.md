# ykim71.github.io

Personal academic website for Yujin Kim, built with the
[al-folio](https://github.com/alshedivat/al-folio) Jekyll theme and hosted on GitHub Pages.

## Editing the site

- **Bio / homepage:** `_pages/about.md`
- **Publications:** `_bibliography/papers.bib` (edit by hand; rendered by jekyll-scholar)
- **Projects:** `_pages/projects.md`
- **Teaching & service:** `_pages/teaching.md`
- **CV:** replace `assets/pdf/CV_Kim_public.pdf`
- **Profile photo:** replace `assets/img/prof_pic.jpg` with your own photo (same filename)
- **Name / URL / settings:** `_config.yml`
- **Links (email, Google Scholar, CV):** `_data/socials.yml`

## Deployment

`.github/workflows/deploy.yml` builds the site and publishes it to the `gh-pages`
branch on every push to `main`. **One-time setup:** in the repo's
**Settings → Pages**, set the source to **Deploy from a branch → `gh-pages` → `/ (root)`**.
