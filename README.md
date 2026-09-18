# Field0notes — Donovan’s fieldnotes

A small, self-hostable blog and project notebook. Write in Obsidian; build a website from the same Markdown files. Python-based MkDocs handles rendering, links, and live reload. One Python hook selects public notes and builds a date-sorted journal. One HTML template and one stylesheet control the appearance. No database, frontend framework, account system, or browser JavaScript is needed for the notebook.

The included independent playground has a tiny JavaScript example. It is a place to host future Agada experiments; it is **not** the existing Agada application.

Start with [TUTORIAL.md](TUTORIAL.md) for seven short, hands-on sessions. This repository is separate from the C64-style `public-space` website.

## 1. Try the example first

Unzip this folder. Open a terminal inside `agada-fieldnotes`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Open http://127.0.0.1:8000 in your browser. Keep that terminal running. Edit a note, `theme/main.html`, or `theme/style.css`, then save; the preview reloads. Stop with Ctrl+C.

If `python3` is missing on Fedora, install it with `sudo dnf install python3 python3-pip`. No Node installation is needed.

After building with `python -m mkdocs build --strict`, preview the generated `dist/` directory:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Opening the HTML directly with `file://` is not the recommended preview: directory links expect a web server.

## 2. Connect your existing Obsidian vault

Create a new `Public` folder **inside your existing vault**. Copy the contents of `example-vault/Public/` into it using your file manager. Do not overwrite an existing Public folder. Keep the site source folder outside your vault, for example `~/Projects/agada-fieldnotes`.

From the site folder, set the absolute path to your public notes:

```bash
export VAULT_PUBLIC="$HOME/Documents/My Vault/Public"
python -m mkdocs serve
```

Change `My Vault` to your actual vault path. The folder should contain `index.md`, `journal/`, and `projects/` from the example. Use the same environment variable for builds. The variable lasts for the current terminal session; add it to your own shell configuration or replace `docs_dir` in `mkdocs.yml` with an absolute path when you are happy with the setup.

The source notes remain in place. Builds never rewrite, move, or delete them. Edit the site’s theme independently of the notes.

## 3. Write and publish a note

Create `Public/journal/first-kyoto-session.md` in Obsidian:

```markdown
---
title: First Kyoto session
date: 2026-09-18
topic: Games
summary: A few observations from the first session.
publish: false
---
# First Kyoto session

## What I tried

## What I noticed

## Next time
```

When ready, set `publish: true` (a YAML boolean, without quotes). A dated journal note then appears automatically on the home page and journal page. `title` and a `YYYY-MM-DD` date are required for journal entries. Change the sample date to your own session date.

Publication rules:

- Only Markdown notes with `publish: true` are built.
- `draft: true` overrides `publish: true`.
- A missing `publish` field excludes a note.
- Future dates do not schedule publication; a future-dated public note is built immediately.
- All files under `Public/assets/` and non-Markdown files under `Public/playground/` are public, whether linked or not. Keep private recordings elsewhere.
- Files outside those two asset folders are excluded unless they are opted-in Markdown pages.
- Hidden files and links that resolve outside Public are excluded.
- A navigation entry is not a privacy setting. The hook is what filters the output.

The included sample entry is explicitly labeled as a sample. Rewrite or remove it before your first public deployment. The homepage and project descriptions are starter copy you can edit.

## 4. Markdown that works in both places

Use ordinary Markdown links, relative to the note:

```markdown
[Agada](../projects/agada.md)
![A frame from the session](../assets/kyoto-frame.jpg)
[Watch the session](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

MkDocs translates `.md` links into website URLs. Obsidian can follow the original Markdown links. In Obsidian, Settings → Files and links → turn off **Use [[Wikilinks]]** for new links, and choose relative paths if needed. This does not convert existing links.

Supported: headings, paragraphs, lists, blockquotes, tables, fenced code, ordinary links and images, YAML properties, and raw HTML. **Not implemented:** `[[wikilinks]]`, `![[note embeds]]`, Obsidian block references, Dataview, Canvas, or plugin-generated views. Existing notes using those features need standard Markdown equivalents in the public version. This starter does not claim pixel-identical rendering of every Obsidian feature.

For YouTube, start with a normal link. If you want an embedded player, raw HTML works:

```html
<iframe src="https://www.youtube-nocookie.com/embed/YOUR_VIDEO_ID"
  title="Kyoto session recording" loading="lazy" allowfullscreen></iframe>
```

Replace the ID. The theme sizes the player responsively. A plain link is the most portable option across Markdown editors. Avoid pasting raw recordings into the vault; link the uploaded video and keep only selected screenshots in `assets/`.

## 5. Build the website

In the activated virtual environment, with `VAULT_PUBLIC` set if using your vault:

```bash
python -m mkdocs build --strict
```

The complete site is in `dist/`. A strict build fails for broken ordinary Markdown file links, including links to excluded draft notes. It cannot check private information in prose, external websites, raw HTML links, or Obsidian-specific syntax. Review the output before upload. If a build fails, fix it and rebuild before deploying anything from `dist/`.

Serve `dist/` locally with the command in section 1 for a final review.

## 6. Host it yourself

Only the **contents of `dist/`** belong in the web server’s document root. The host does not need Python, MkDocs, or your vault. Any static host works. Keep source notes, `.venv/`, and config outside the public document root.

For a Linux server running Caddy, create a dedicated document root such as `/srv/fieldnotes`. Ensure Caddy can read it, point your domain’s DNS to the server, and allow HTTP/HTTPS traffic. Example Caddyfile (replace the domain):

```caddyfile
notes.example.com {
    root * /srv/fieldnotes
    file_server
}
```

Caddy supplies HTTPS for a correctly configured reachable domain. The directory must be writable by your upload user and readable by the Caddy service. Distribution-specific service permissions and SELinux policies may need configuration on your own host.

Copy the built files using your host’s normal upload method. With SSH and rsync, preview an update:

```bash
rsync -av --delete --dry-run dist/ YOUR_USER@YOUR_HOST:/srv/fieldnotes/
```

After checking that the destination is the **dedicated site directory** and the deletion list is correct:

```bash
rsync -av --delete dist/ YOUR_USER@YOUR_HOST:/srv/fieldnotes/
```

The trailing slash copies the contents. `--delete` removes old published pages that no longer exist in the build; never aim this at a shared directory. Merely hiding a note and uploading new files without removing the old page would leave the old page accessible. This simple upload is not atomic; a larger site can later use versioned release directories and a symlink switch.

Before production, add your real URL to `mkdocs.yml` so the sitemap has the correct base:

```yaml
site_url: https://notes.example.com/
```

A subdirectory such as `https://example.com/notebook/` also works: set that complete URL and serve `dist/` from that subdirectory. The template uses relative links. There are no SPA rewrite rules to configure.

A private/local preview remains private until you upload it. No hosting account or domain was changed when this starter was created.

## 7. Where to experiment

| File or folder | What it controls | First exercise |
| --- | --- | --- |
| `theme/style.css` | Colors, typography, spacing, mobile layout, dark mode | Change `--accent` |
| `theme/main.html` | Shared page layout, navigation, journal rows | Change the running header |
| `mkdocs.yml` | Title, description, navigation, source folder | Rename the site |
| `publish.py` | Public-note filter and journal metadata | Read `on_files` line by line |
| `Public/journal/` | Dated entries | Write a short session log |
| `Public/projects/` | Long-lived project pages | Add a project and link from the shelf |
| `Public/playground/` | Independent HTML/CSS/JS apps | Replace the sample Agada playground |
| `Public/assets/` | Deliberately public screenshots and downloads | Add one screenshot |
| `dist/` | Generated output | Inspect the generated HTML; do not edit here |

The original name is repeated in `theme/main.html`, not just `site_name`. Edit both when renaming. The theme uses system fonts and no external font/CDN requests. It includes a narrow-screen layout, automatic dark mode, keyboard focus indicators, and a skip link.

For browser apps, put each built app in its own `playground/name/` folder. Keep asset URLs relative or configure that app’s base path. A native Linux/Python application needs a download and instructions; static hosting cannot run its server process. WebAudio demos may need a user gesture before sound starts.

## A lightweight recording rhythm

1. Record the session while doing the thing you came to do.
2. Keep one interesting moment or a short lightly edited clip.
3. Write three bullets: tried / noticed / next.
4. Add a screenshot or YouTube link if useful.
5. Build and upload when you feel like sharing.

No posting schedule is required. Your notebook is useful even when the video never gets edited. Back up recordings you care about to another drive; an SD card is a working copy.

## Maintenance and troubleshooting

- `No module named mkdocs`: activate `.venv`, then install `requirements.txt`.
- Changes do not appear: check `VAULT_PUBLIC`, `publish: true`, and whether the preview command is still running.
- `Aborted with ... warnings`: fix the paths printed by `--strict`.
- A draft is still online: rebuild successfully, then remove the old server copy through your deployment process.
- New navigation item: add its Markdown path under `nav` in `mkdocs.yml`; this does not publish it without `publish: true`.
- Journal sorting is by date, then URL; notes on the same date do not have a time-of-day ordering.
- Keep source code in Git if desired. Keep your private vault out of a public repository. `dist/` is ignored by the included `.gitignore`.

Built by OpenAI Codex as an editable starter. Review the code and personalize the copy. It deliberately contains no analytics, login, comments service, or automated uploads.

References: [MkDocs content](https://www.mkdocs.org/user-guide/writing-your-docs/), [MkDocs theme development](https://www.mkdocs.org/dev-guide/themes/), [Caddy file server](https://caddyserver.com/docs/caddyfile/directives/file_server).
