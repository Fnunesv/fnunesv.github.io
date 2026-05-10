# fnunesv.github.io — Site Management Guide

Personal website built with [Hugo](https://gohugo.io/), hosted on GitHub Pages.
Live at: **https://fnunesv.github.io**

---

## Quick reference

| Task | File to edit |
|---|---|
| Home bio | `content/_index.md` |
| Research page | `content/research/_index.md` |
| Contact page | `content/contact/_index.md` |
| Colours / fonts | `assets/css/main.css` |
| Navigation links | `hugo.toml` |
| GitHub repos list | `data/repos.yaml` |
| Gallery captions | `data/gallery.yaml` |
| Publications | run `python3 scripts/fetch_orcid.py` |

---

## Setup (first time on a new machine)

1. Install Hugo:
   ```bash
   /opt/homebrew/bin/brew install hugo
   ```

2. Clone the repo:
   ```bash
   git clone git@github.com:fnunesv/fnunesv.github.io.git
   cd fnunesv.github.io
   ```

3. Start the local preview server:
   ```bash
   /opt/homebrew/bin/hugo server
   ```
   Open **http://localhost:1313** in your browser. The page reloads automatically every time you save a file.

---

## The update workflow

Every change follows the same three steps:

```bash
# 1. Make your edits and save the file
# 2. Commit
git add .
git commit -m "brief description of what you changed"
# 3. Push — GitHub rebuilds and redeploys automatically (~2 min)
git push
```

---

## Editing text content

All pages are plain Markdown files inside the `content/` folder. Open them in any text editor (Sublime Text, VSCode, etc.), edit the text below the `---` block, save.

**Markdown basics:**

```markdown
**bold text**
*italic text*
[link text](https://example.com)

## Section heading
### Subsection heading

- bullet point
- another point
```

---

## Adding a blog post / note

Create a new `.md` file in `content/notes/`. The filename becomes the URL slug.

```bash
# Example
touch content/notes/on-optogenetics.md
```

Paste this template and fill it in:

```markdown
---
title: "Your Post Title Here"
date: 2026-05-10
---

Your text here. Write in plain Markdown.

## A heading

More content.
```

The post appears automatically on the Notes page, sorted newest first.

---

## Uploading images (gallery)

**Step 1 — Copy image files** into `static/img/gallery/`:
```bash
cp ~/Desktop/my-image.jpg static/img/gallery/my-image.jpg
```
Supported formats: `.jpg`, `.png`, `.tif`, `.gif`. Keep filenames short with no spaces (use hyphens).

**Step 2 — Register the image** in `data/gallery.yaml`:
```yaml
- src: /img/gallery/my-image.jpg
  caption: Actin cortex — Airyscan, EMBL 2024
```
Add one block per image. Order in the file = order on the page.

---

## Uploading PDFs

Drop the file into `static/files/`:
```bash
cp ~/Desktop/poster-ascb2024.pdf static/files/poster-ascb2024.pdf
```

Then link to it anywhere in a Markdown file:
```markdown
[Download poster](/files/poster-ascb2024.pdf)
```

The CV is already at `static/files/cv.pdf` — replace that file to update it.

---

## Publications: what you can and cannot host

| Type | Can you host it? |
|---|---|
| Publisher PDF (typeset journal version) | ❌ No — belongs to the journal |
| Accepted manuscript (your final text, before typesetting) | ✅ Usually yes — check [Sherpa Romeo](https://v2.sherpa.ac.uk/romeo/) for each journal |
| Preprint (bioRxiv, etc.) | ✅ Always |
| Poster / talk slides | ✅ Always — it's yours |

Your *Science Advances* 2022 paper is open access — the published PDF can be shared freely. For others, use the **Request PDF** email button already on the publications page, or link to the preprint if one exists.

---

## Refreshing the publications list

Publications are fetched from ORCID. Run this whenever you add a new paper:

```bash
python3 scripts/fetch_orcid.py
git add data/publications.yaml
git commit -m "refresh publications"
git push
```

---

## Adding a GitHub repository to the Projects page

Edit `data/repos.yaml` and add a block:

```yaml
- name: "repo-name"
  description: "One sentence on what this does."
  url: "https://github.com/fnunesv/repo-name"
  language: "Python"
  lang_color: "#3572A5"
```

Common language colours:
- Python `#3572A5` · R `#198CE7` · MATLAB `#E16737` · Shell `#89E051` · JavaScript `#F1E05A`

---

## Changing colours, fonts, and layout

All visual styling is in `assets/css/main.css`. The variables at the top of the file control the whole site:

```css
:root {
  --bg: #FAFAF8;         /* page background */
  --accent: #0369A1;     /* links, buttons, highlights */
  --text: #111827;       /* main text colour */
  --text-muted: #6B7280; /* captions, secondary info */
  --border: #E5E7EB;     /* dividers */
}
```

Change a value, save, and http://localhost:1313 updates instantly.

**Fonts** are set a few lines below the variables — replace `'Lora'` or `'Inter'` with any [Google Fonts](https://fonts.google.com/) name and update the `@import` URL at the top of the file to match.

---

## Changing the navigation

Edit the `[[menu.main]]` blocks in `hugo.toml`:

```toml
[[menu.main]]
  name   = "New Page"
  url    = "/newpage/"
  weight = 8          # controls order: lower = further left
```

Remove a block to remove that link from the nav.

---

## Adding a new section / page

1. Create the content file:
   ```bash
   mkdir content/newpage
   touch content/newpage/_index.md
   ```
   Add frontmatter to the file:
   ```markdown
   ---
   title: "New Page"
   ---
   Your content here.
   ```

2. Create a layout (copy the closest existing one as a starting point):
   ```bash
   cp layouts/contact/list.html layouts/newpage/list.html
   ```
   Edit the HTML in that file to change what the page looks like.

3. Add it to the navigation in `hugo.toml` (see above).

---

## Deploying

Every `git push` to `main` triggers an automatic rebuild via GitHub Actions. You can watch it in real time:

`github.com/fnunesv/fnunesv.github.io` → **Actions** tab

A green ✓ means the site is live. A red ✗ means something failed — click the run to see the error log.

---

## File structure reference

```
fnunesv.github.io/
├── hugo.toml              # site config, nav, metadata
├── assets/css/main.css    # all styling
├── content/               # all page text (edit these)
│   ├── _index.md          # home page bio
│   ├── research/
│   ├── publications/
│   ├── projects/
│   ├── gallery/
│   ├── notes/             # add .md files here for blog posts
│   └── contact/
├── data/                  # structured data files
│   ├── publications.yaml  # auto-generated by fetch_orcid.py
│   ├── repos.yaml         # GitHub repos to highlight
│   └── gallery.yaml       # gallery image list
├── static/                # files served as-is
│   ├── img/               # images (profile photo, gallery)
│   └── files/             # PDFs (CV, posters, etc.)
├── layouts/               # HTML templates (rarely need editing)
├── scripts/
│   └── fetch_orcid.py     # fetches publications from ORCID
└── .github/workflows/
    └── deploy.yml         # automated build + deploy
```
