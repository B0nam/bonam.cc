---
name: publish-post
description: Publish a Markdown draft as a new bonam.cc blog post. Fixes grammar and spelling, organizes and lints the Markdown, writes the Hugo front matter (title, description, slug, tags, etc.), creates the page bundle with its images, then commits, pushes and verifies the deploy. Use when the user hands over a .md file (or pasted Markdown) to post on the blog.
argument-hint: <path/to/draft.md>
---

# Publish a post on bonam.cc

The user passes a Markdown draft (a file path in `$ARGUMENTS`, or pasted text). Turn it into a polished post and publish it.

Repo: `/mnt/d/data/personal/bonam.cc` (Hugo + Stack theme, deployed to GitHub Pages by `.github/workflows/deploy.yml` on push to `main`).
Tools live in `~/.local/bin`, so start every Bash command with `export PATH=$HOME/.local/bin:$PATH`.

If no draft was given, ask for the file path or the Markdown text, and do nothing else.

## 1. Prepare

- Windows paths like `C:\Users\...\post.md` map to `/mnt/c/Users/.../post.md`.
- In the repo, run `git status --short` and `git pull --ff-only`. If there are uncommitted changes that aren't yours, stop and ask.
- Read the whole draft. Note any images it references, local or remote.
- Detect the language: Portuguese → `pt_BR`, English → `en_US`. Never translate the post.

## 2. Fix grammar and spelling

Correct grammar, spelling, punctuation, agreement and accents (Portuguese: crase, acentuação, concordância), and obvious typos. Keep technical terms consistent ("Playwright", "GitHub", "JavaScript").

Preserve the author's voice, tone, meaning, structure and opinions. Do not rewrite sentences that are already correct, add or remove content, or make the text more formal. Never change anything inside code blocks, inline code, URLs, commands or file paths.

Keep a short list of the meaningful corrections (skip trivial ones) for the final report.

## 3. Organize the Markdown

- The post title lives in front matter, so remove any H1 (`#`) from the body. Body headings start at `##`, with no skipped levels and no bold inside headings.
- Fenced code blocks (```` ``` ````) always get a language: `bash`, `json`, `yaml`, `typescript`, `javascript`, `python`, `text`, etc.
- Lists use `-`, and ordered lists use `1.`, `2.`, … Put blank lines around headings, lists and code blocks.
- Turn bare URLs into links (`[text](url)` or `<url>`).
- Remove trailing whitespace and repeated blank lines, and end the file with exactly one newline.

## 4. Images

- Every image goes into the post's bundle folder, `content/post/<slug>/`:
  - Copy local images there.
  - Download remote images with `curl -sL` (except embeds such as YouTube).
- Give each image a descriptive kebab-case file name (`playwright-test-report.png`), and reference it by that relative name.
- Every image gets alt text, written in the post's language, that describes what it shows.
- If the body starts with an image, it becomes the cover: set `image:` in front matter and remove it from the body, since the theme already shows the cover on top. Otherwise leave `image` out.

## 5. Front matter

Write YAML front matter with the fields in this order:

```yaml
---
title: "…"
description: "…"
date: 2026-01-31T10:00:00-03:00
slug: "…"
locale: "pt_BR"
image: "cover.png"          # only when there is a cover
categories:
    - "AI"
tags:
    - "playwright"
    - "português"
draft: false
---
```

- **title:** the author's title, from the draft's H1 or front matter, with grammar fixed. If there is none, propose one that reflects the content.
- **description:** 120–155 characters, in the post's language. It's shown as the search result snippet, so it should include the main terms people would search for and summarize what the reader learns. No clickbait.
- **date:** now, from `date -Iseconds`.
- **slug:** ASCII kebab-case, no accents, keyword-focused, ≤ 60 characters. It must not already exist in `content/post/`.
- **locale:** `pt_BR` or `en_US`.
- **categories:** exactly one. Reuse an existing category (`grep -h -A1 '^categories:' content/post/*/index.md`, currently "AI" and "Smart Cities"). Create a new one only if none fits.
- **tags:** 3–6 lowercase kebab-case tags, reusing existing tags where they fit. Always add the language tag `português` or `english`.
- Do **not** set `canonicalUrl`: the blog is the original, and Medium imports from it.

Write the result to `content/post/<slug>/index.md`.

## 6. Lint

```bash
npx -y markdownlint-cli2 "content/post/<slug>/index.md"
```

The rules are in `.markdownlint-cli2.jsonc`. Fix every issue and re-run until it reports 0 issues. Don't disable rules inline.

## 7. Build

```bash
hugo --gc --minify
```

- The build must finish with no `ERROR`.
- `public/p/<slug>/index.html` must exist.
- Its `<title>` and `<meta name=description>` must be correct.

## 8. Publish

```bash
git add content/post/<slug>
git commit -m "Add post: <title>"
git push
```

End the commit message with the co-author trailer from the session's attribution instructions. Then follow the deploy with `gh run watch <id> --exit-status`.

Once the deploy succeeds, confirm `curl -s -o /dev/null -w '%{http_code}' https://bonam.cc/p/<slug>/` returns `200`. If the deploy fails, show the failing log lines and fix the cause.

## 9. Report

Write the report in the user's language, and keep it brief:

- the live URL `https://bonam.cc/p/<slug>/`
- the main grammar fixes, as a short list
- the chosen title, description, category and tags
- what the lint and organization steps changed, in one line
- the next step for Medium: open <https://medium.com/p/import>, paste the post URL, review and publish. Medium will set the canonical link to bonam.cc.
