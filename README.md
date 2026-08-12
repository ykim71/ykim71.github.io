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

## Adding a publication

Publications live in `_bibliography/papers.bib` and are approved by you — nothing is
added automatically. To add one, paste this block at the **top** of the file (newest
first), fill in the fields, and delete any you don't have:

```bibtex
@article{kim2027keyword,
  bibtex_show = {true},
  selected    = {true},
  abbr        = {Pol. Comm.},
  title       = {Your Paper Title},
  author      = {Kim, Yujin and Coauthor, Name},
  journal     = {Journal Name},
  year        = {2027},
  volume      = {00},
  number      = {0},
  pages       = {1--20},
  doi         = {10.xxxx/xxxxxx}
}
```

Notes: the citation key on the first line (`kim2027keyword`) must be unique; your name
(`Kim, Yujin`) is bolded automatically; `selected = {true}` also lists it on the
homepage (remove that line to keep it on the publications page only); the title links
to the DOI automatically. For a conference paper, use `@inproceedings{...}` with
`booktitle = {...}` instead of `journal`. Then commit and push.

## Deployment

`.github/workflows/deploy.yml` builds the site and publishes it to the `gh-pages`
branch on every push to `main`. **One-time setup:** in the repo's
**Settings → Pages**, set the source to **Deploy from a branch → `gh-pages` → `/ (root)`**.
