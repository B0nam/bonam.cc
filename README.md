# bonam.cc

Personal blog built with [Hugo](https://gohugo.io) and [hugo-theme-stack](https://github.com/CaiJimmy/hugo-theme-stack), deployed to GitHub Pages at <https://bonam.cc>.

## Local development

Requires Hugo **extended** and Go (the theme is loaded as a Hugo Module).

```sh
hugo server          # http://localhost:1313, drafts: add -D
hugo --gc --minify   # production build into public/
```

## Writing a post

```sh
hugo new post/my-new-post/index.md
```

Put images next to `index.md` in the same folder and reference them by file name. Set `image:` in the front matter for the cover. Remove `draft: true` when it's ready.

Pushing to `main` builds and deploys the site (`.github/workflows/deploy.yml`). After each deploy, the `indexnow` job sends the sitemap's URLs to Bing, Yandex, Seznam and Naver through [IndexNow](https://www.indexnow.org). Its key file is `static/<key>.txt`.

### SEO checklist

- `description`: about 150 characters, using the words people would search for. It's shown in search results.
- `locale`: `en_US` or `pt_BR`.
- `slug`: short and keyword-rich. It becomes the URL (`/p/<slug>/`).
- `image`: a cover image, used for search and social previews.
- Descriptive alt text on every image: `![Playwright test running in VS Code](shot.png)`.

## Publishing to Medium (blog first)

1. Push the post and wait for the deploy to finish.
2. Open <https://medium.com/p/import>.
3. Paste the post URL, e.g. `https://bonam.cc/p/my-new-post/`, and click **Import**.
4. Review the draft and publish.

Medium sets the story's canonical link to bonam.cc, so search engines treat the blog as the original.

## Importing posts from Medium

Posts first published on Medium can be pulled in with:

```sh
python3 scripts/medium_import.py            # skips posts that already exist
python3 scripts/medium_import.py --force    # re-imports everything
```

The script reads `https://medium.com/feed/@danibonam` (it only has the 10 most recent posts), converts each post to Markdown and downloads its images. It sets `canonicalUrl` to the Medium URL and keeps the post out of the sitemap, so search engines index the Medium original. After importing, add `categories` and rewrite the generated `description` by hand.

## Theme

`.github/workflows/update-theme.yml` updates the theme module daily. Theme overrides live in `layouts/`:

- `_partials/helper/responsive-image.html` skips srcset resizing for GIFs, since resizing animated GIFs is very slow.
- `_partials/head/custom.html`:
  - generates the favicons from `assets/img/favicon.jpg`
  - adds JSON-LD structured data
  - marks tag, category and search pages `noindex`
- `_partials/data/title.html` appends the site name to page titles.
- `_partials/data/description.html` cleans up and shortens meta descriptions.
- `robots.txt` points crawlers to the sitemap.

Dark mode colors are in `assets/scss/custom.scss`.
