# Mackinder Lab website

The website of the Mackinder Lab, Department of Biology, University of York.
It is a [Jekyll](https://jekyllrb.com) site hosted on GitHub Pages.

- **Editors:** see [EDITING.md](EDITING.md). All day-to-day editing happens in [Pages CMS](https://app.pagescms.org).
- **Content:** news in `_posts/`, people in `_people/`, publications in `_data/publications.yml`, other pages in `pages/`, menu in `_data/navigation.yml`, home page text in `_data/home.yml`.
- **Templates:** `_layouts/`, `_includes/`, `assets/css/style.css`.
- **Editor setup:** `.pages.yml` defines the Pages CMS forms.

## How it builds

Every push to `main` runs `.github/workflows/pages.yml`, which:

1. runs `scripts/fill_dois.py` to fill in missing publication details from Crossref, and
2. builds the site with Jekyll and publishes it to GitHub Pages.

## Run it locally

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

## One-off migration from Weebly

`scripts/download_assets.py` copies images and downloads from the old
mackinderlab.weebly.com site. Run it on a network where the old site loads.
People photos and three research images have to be saved by hand; the script
lists where they go.
