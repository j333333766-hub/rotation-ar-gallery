"""Refresh existing viewers without importing ZIPs or modifying model assets."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent


def update_viewer(old, template):
    title = re.search(r'<title>(.*?)</title>', old, re.S)
    navigation = re.search(r'<header\b[^>]*>.*?<style>#wb-qr\[hidden\]\{display:none!important\}</style>', old, re.S)
    if not title or not navigation:
        raise ValueError('Existing gallery title or navigation is missing')
    name = html.unescape(re.sub(r'\s*·\s*(?:AR로 보기|3D 뷰어 \(AR\))\s*$', '', title[1]))
    updated = template.replace('__WORK_NAME__', html.escape(name))
    updated = re.sub(r'<title>.*?</title>', lambda _: title[0], updated, count=1, flags=re.S)
    updated = re.sub(r'<header>.*?</header>', lambda _: navigation[0], updated, count=1, flags=re.S)
    return updated


def main():
    template = (ROOT / 'viewer.tpl.html').read_text(encoding='utf-8')
    # Prepare all changes before writing any file. A mismatched page aborts the run.
    replacements = [(p, update_viewer(p.read_text(encoding='utf-8'), template))
                    for p in sorted((ROOT / 'works').glob('*/index.html'))]
    changed = 0
    for page, text in replacements:
        if page.read_text(encoding='utf-8') != text:
            page.write_text(text, encoding='utf-8')
            changed += 1
    print(f'Updated {changed} AR viewers; model files and gallery listing unchanged.')


if __name__ == '__main__':
    main()
