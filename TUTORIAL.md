# Field0notes: a small website you can learn by changing

This is the Markdown website starter from our conversation, preserved separately from the C64 computer in `public-space`. Nothing here depends on that computer. Keep this as your hand-built web playground.

You do not need to finish a course before using the site. Each session below should end with one visible change. Use a branch for experiments and keep the original working.

## Session 0 — run it and locate the moving parts (15 minutes)

```bash
git clone https://github.com/public-space/field0notes.git
cd field0notes
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Open http://127.0.0.1:8000. Leave that terminal running. A second terminal is useful for Git. Ctrl+C stops the preview.

Open `example-vault/Public/index.md` and change one sentence. Save. Watch the preview update. You edited content, not HTML. MkDocs converted Markdown into HTML, inserted it into the theme, and served the result.

**Done:** your sentence appears in the browser. Write down which file you changed and what you expected.

## Session 1 — follow a note to the screen (20 minutes)

Read these files in this order:

1. `mkdocs.yml`: configuration, like a Python dictionary written in YAML.
2. `example-vault/Public/index.md`: metadata between `---` lines, followed by Markdown.
3. `publish.py`: Python that decides which notes are public.
4. `theme/main.html`: Jinja template. `{{ value }}` inserts a value; `{% if ... %}` and `{% for ... %}` choose or repeat HTML.
5. `theme/style.css`: rules that control appearance.

In the template, find `{{ page.content }}`. That is the point where converted Markdown joins the surrounding HTML. Find the `<header>`, `<nav>`, `<main>`, and `<footer>` elements in the file and identify their visible counterparts.

**Exercise:** change the footer text, then undo it. This changes every generated page because all pages share the template.

**Done:** explain, in your own words, why changing a CSS file does not change your Markdown notes.

## Session 2 — make one design change (20 minutes)

Make a branch:

```bash
git switch -c experiment/type-and-spacing
```

At the top of `theme/style.css`, find `--accent`. Change its hex color. It is a CSS custom property used by multiple rules. Next, change the `max-width` of `.shell`, or the `font-size` of `h1`.

Read selectors as sentences: `.entry p` means paragraphs inside an element with class `entry`; `nav a` means links inside navigation. `padding` is space inside a box; `margin` is space outside it. Borders sit between them.

Open your browser's developer tools (F12). Inspect a heading and temporarily change its font size. Developer-tools changes disappear on reload; put the values you want in the CSS file.

**Done:** choose one color and one spacing change you like, then save them:

```bash
git diff
git add theme/style.css
git commit -m "Experiment with notebook typography"
```

Return to `main` with `git switch main`. Your committed experiment stays on its branch. You can return with `git switch experiment/type-and-spacing`. Do not use destructive reset commands to switch designs.

## Session 3 — write a real entry (15 minutes)

Copy `journal/starting-a-field-notebook.md` to a new filename in the same folder. Give it a new title, date, and summary. Replace the example prose with a short note about a game or Linux session.

- What did I try?
- What happened?
- What would I try next?

Set `publish: false` while writing. Set `publish: true` when ready. Watch the home page's recent-entry list update automatically. A title is the displayed name; a filename determines the path. Renaming a published file changes its URL.

**Done:** your entry appears in the journal and its links work. The old sample can be removed or marked private.

## Session 4 — connect your own vault (20 minutes)

Follow README section 2. Copy the example's public files into a new `Public` folder in your vault; keep this repository outside your vault. Set `VAULT_PUBLIC` to the absolute path of that folder.

```bash
export VAULT_PUBLIC="$HOME/Documents/My Vault/Public"
python -m mkdocs serve
```

Replace the example path. Quotes keep a path containing spaces together as one value. `$HOME` expands to your home directory. `export` makes the variable visible to child processes such as MkDocs. It does not rename or move anything.

**Exercise:** add a note with no `publish` property. Confirm it does not appear. Then add the boolean `publish: true` and confirm that it does. All attachments in Public/assets and apps in Public/playground are public, so put only deliberately shareable files there.

**Done:** you can edit one file in Obsidian and see the website update without copying the note each time.

Use standard Markdown links in public notes. This starter does not convert Obsidian `[[wikilinks]]` or Dataview. The README explains the exact supported syntax.

## Session 5 — add a project page (20 minutes)

Create `Public/projects/my-sampler.md`:

```markdown
---
title: My sampler
publish: true
---
# My sampler

A small sound experiment.

## Current experiment

## What works

## Next step
```

Link to it from `Public/projects/index.md` with `[My sampler](my-sampler.md)`. If it deserves a permanent navigation entry, add its path under `nav` in `mkdocs.yml`.

**Done:** the page is reachable from the project shelf, and its source still reads clearly in Obsidian.

## Session 6 — a tiny HTML/JavaScript experiment (25 minutes)

Open `Public/playground/agada/index.html`. There are three languages in one file:

- HTML creates a button and a paragraph.
- CSS styles them.
- JavaScript listens for a click, changes a color, and updates a count.

Find `addEventListener('click', ...)`. That callback runs after someone clicks; it does not run merely because the file loaded. Change the color array. Then make the paragraph show your own sentence using the existing count.

**Done:** you can predict what changes on the next click. Keep a console open and look for errors if it stops working.

This is not the original Agada application. It is a simple placeholder you can replace with a browser-compatible build of it.

## Session 7 — understand the public build (20 minutes)

```bash
python -m mkdocs build --strict
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Stop the development preview first if it already occupies port 8000. `dist` contains ordinary HTML, CSS, and public assets. That directory can be hosted without Python. It is generated; edit the source files and rebuild instead of changing `dist` by hand.

**Exercise:** inspect a generated page and find text from your note and HTML from your template. Change a public note to private, rebuild, and confirm its output page is removed.

**Done:** you understand exactly what you will upload. README section 6 explains Caddy, SSH/rsync, and removal of old server files. Hosting credentials are not part of this repo.

## A useful debugging habit

When something breaks, record: the file changed, the command used, the exact error, what you expected, and the smallest change that reproduces it. First check indentation in YAML, quotes/brackets in HTML or JavaScript, and relative link paths. Ask for an explanation of a specific error rather than replacing whole files blindly.

## Optional later experiments

| Small project | What it teaches |
| --- | --- |
| Add an About page | Markdown links and navigation |
| Restyle journal rows | CSS grid and spacing |
| Add a screenshot with alt text | Relative paths and accessibility |
| Display a new frontmatter field | YAML → Python → Jinja data flow |
| Change date formatting | Python strings and date objects |
| Add a print stylesheet | Media queries |
| Build a separate little audio page | DOM events and browser audio |

Useful official references: [MkDocs](https://www.mkdocs.org/), [MDN HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content), [MDN CSS](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics), [Jinja](https://jinja.palletsprojects.com/en/stable/templates/).
