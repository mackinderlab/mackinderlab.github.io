# Mackinder Lab website

The website of the Mackinder Lab, Department of Biology, University of York.
It is a [Jekyll](https://jekyllrb.com) site hosted on GitHub Pages.

- **Editors:** see [EDITING.md](EDITING.md). All day-to-day editing happens in [Pages CMS](https://app.pagescms.org).
- **Content:** news in `_posts/`, people in `_people/`, publications in `_data/publications.yml`, other pages in `pages/`, menu in `_data/navigation.yml`, home page text and banner in `_data/home.yml`, upcoming events in `_data/events.yml`.
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

## Migration from Weebly

Images and files were copied from mackinderlab.weebly.com with
`scripts/download_assets.py` (run once in GitHub Actions). The original page
HTML is kept on the `weebly-archive` branch for reference.
