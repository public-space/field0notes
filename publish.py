"""Small MkDocs hook: opt-in pages and a chronological journal.

MkDocs owns Markdown conversion, file watching, links, and the build.
This file never writes to your vault. Edit the theme to change presentation.
"""
from pathlib import Path
from datetime import date
from mkdocs.utils.meta import get_data
from mkdocs.exceptions import PluginError


def on_files(files, config):
    posts = []
    root = Path(config['docs_dir']).resolve()
    for file in list(files):
        path = Path(file.abs_src_path)
        # Leave MkDocs theme files alone; apply the rules to vault files only.
        if not path.is_relative_to(root):
            continue
        # Do not follow links out of the public folder.
        if not path.resolve().is_relative_to(root) or any(
            part.startswith('.') for part in Path(file.src_uri).parts
        ):
            files.remove(file)
            continue
        if file.is_documentation_page():
            _, meta = get_data(path.read_text(encoding='utf-8'))
            if meta.get('publish') is not True or meta.get('draft') is True:
                files.remove(file)
                continue
            if file.src_uri.startswith('journal/') and file.src_uri != 'journal/index.md':
                try:
                    day = date.fromisoformat(str(meta['date']))
                    title = str(meta['title'])
                except (KeyError, ValueError) as exc:
                    raise PluginError(f'{file.src_uri}: journal posts need title and YYYY-MM-DD date') from exc
                posts.append({'title': title, 'date': str(day), 'url': file.url,
                              'summary': str(meta.get('summary', '')),
                              'topic': str(meta.get('topic', 'Notes'))})
        elif not file.src_uri.startswith(('assets/', 'playground/')):
            # Theme resources live outside docs_dir and remain available.
            if path.resolve().is_relative_to(root):
                files.remove(file)
    config.extra['journal'] = sorted(posts, key=lambda p: (p['date'], p['url']), reverse=True)
    return files
