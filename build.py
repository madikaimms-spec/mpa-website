#!/usr/bin/env python3
"""Build the MPA website pages from the shared parts in src/.

Edit files in src/ (sections, site.css, site.js), then run:  python3 build.py
It writes the page .html files at the repo root and assets/site.css + assets/site.js.
"""
import html as htmllib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / 'src'
SECTIONS = SRC / 'sections'

NAV = [
    ('/', 'Home'),
    ('/about', 'About us'),
    ('/initiatives', 'Initiatives'),
    ('/office-bearers', 'Office bearers'),
    ('/gallery', 'Gallery'),
    ('/contact', 'Contact us'),
]

DESC = ('Madikai Pravasi Association (MPA) — a community for families from Madikai Panchayath, Kasaragod, '
        'living in the UAE. Member welfare, Sneha Veedu homes, palliative ambulance support back home and '
        'cultural events since 2013.')


def part(name: str) -> str:
    return (SECTIONS / f'{name}.html').read_text()


def strip_intro(html: str) -> tuple[str, str, str]:
    """Remove the section's own eyebrow / h2 / lede (the page banner shows them) and return them."""
    eyebrow = re.search(r'\n\s*<p class="eyebrow">(.*?)</p>', html)
    h2 = re.search(r'\n\s*<h2>(.*?)</h2>', html)
    lede = re.search(r'\n\s*<p class="lede">(.*?)</p>', html)
    for m in (eyebrow, h2, lede):
        if m:
            html = html.replace(m.group(0), '', 1)
    return html, (h2.group(1) if h2 else ''), (lede.group(1) if lede else '')


def banner(title: str, lede: str, eyebrow: str = 'Madikai Pravasi Association') -> str:
    return f'''  <section class="page-banner">
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{title}</h1>
      {f'<p class="lede">{lede}</p>' if lede else ''}
    </div>
  </section>
  <div class="kasavu" aria-hidden="true"></div>

'''


def header(active: str) -> str:
    current = ' aria-current="page"'
    items = '\n'.join(
        f'        <li><a href="{href}"{current if href == active else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f'''<a class="skip" href="#main">Skip to content</a>

<header class="site">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Madikai Pravasi Association, home">
      <img class="brand-mark" src="/logo.webp" alt="" width="96" height="96">
      <span class="brand-name">Madikai Pravasi Association<small>Kasaragod · UAE</small></span>
    </a>
    <a class="lang-switch" href="@@ALT@@" hreflang="ml" lang="ml">മലയാളം</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="main" id="nav" aria-label="Main">
      <ul>
{items}
      </ul>
    </nav>
  </div>
</header>
'''


FOOTER = '''<div class="kasavu" aria-hidden="true"></div>
<footer class="site">
  <div class="wrap">
    <span>© <span id="y">2026</span> Madikai Pravasi Association (MPA). Established 2013. Reg No: KSR/124/2026</span>
    <nav class="foot-links" aria-label="Footer">
      <a href="/about">About</a><a href="/office-bearers">Office bearers</a><a href="/gallery">Gallery</a><a href="/contact">Contact</a>
    </nav>
  </div>
</footer>
'''


def page(path: str, title: str, main: str, extra: str = '', og_image: str = '/photos/hero-group.webp') -> str:
    full_title = 'Madikai Pravasi Association (MPA)' if path == '/' else f'{title} · Madikai Pravasi Association'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="Supporting our community, connecting our roots. Since 2013.">
<meta property="og:image" content="{og_image}">
<meta name="theme-color" content="#7A1518">
<link rel="icon" href="/logo.webp" type="image/webp">
<link rel="apple-touch-icon" href="/logo.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wdth,wght@75..125,300..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<link rel="alternate" hreflang="en" href="{path}">
<link rel="alternate" hreflang="ml" href="{ml_path(path)}">
</head>
<body>
{header(path).replace('@@ALT@@', ml_path(path))}
<main id="main">
{main}</main>
{extra}
{FOOTER}
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


EXPLORE = [
    ('/about', 'About us', 'Who we are, since 2013.', '/photos/members-group.webp'),
    ('/initiatives', 'Our initiatives', 'Sneha Veedu, the palliative ambulance and welfare back home.', '/photos/ambulance-handover.webp'),
    ('/office-bearers', 'Office bearers', 'The members who lead MPA, present and past.', '/photos/general-body-2025.webp'),
    ('/gallery', 'Gallery', 'Moments from our events and work.', '/photos/pookalam.webp'),
    ('/contact', 'Contact us', 'Membership, events and how to reach us.', '/photos/gramotsavam-teams.webp'),
]


def explore() -> str:
    cards = '\n'.join(
        f'''        <a class="tile" href="{href}">
          <img src="{img}" alt="" loading="lazy" decoding="async">
          <span class="tile-text"><b>{title}</b><span>{text}</span></span>
        </a>'''
        for href, title, text, img in EXPLORE
    )
    return f'''  <section class="block explore" id="explore">
    <div class="wrap">
      <p class="eyebrow">Explore</p>
      <h2>Find your way around</h2>
      <div class="tiles">
{cards}
      </div>
    </div>
  </section>
'''


PAGE_PATHS = ('/about', '/initiatives', '/office-bearers', '/gallery', '/contact')
ML = json.loads((SRC / 'ml.json').read_text())


def ml_path(path: str) -> str:
    return '/ml' if path == '/' else f'/ml{path}'


def tr(text: str, missing: set) -> str:
    """Translate one English string (whitespace-normalised) to Malayalam."""
    key = ' '.join(text.split())
    if not key or not any(c.isalpha() for c in key) or any('\u0d00' <= c <= '\u0d7f' for c in key):
        return text
    if key.startswith('View larger: ') and key[13:] in ML:
        out = 'വലുതായി കാണുക: ' + ML[key[13:]]
    elif key in ML:
        out = ML[key]
    elif ' · ' in key and all(p in ML for p in key.split(' · ')):
        out = ' · '.join(ML[p] for p in key.split(' · '))
    else:
        missing.add(key)
        return text
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return lead + out + trail


def to_malayalam(doc: str, path: str, missing: set) -> str:
    """Make the Malayalam copy of a built English page."""
    # Translate visible text, leaving <script> and <style> alone.
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', doc, flags=re.S)
    for i, chunk in enumerate(parts):
        if not chunk or chunk.startswith('<'):
            continue
        parts[i] = tr(htmllib.unescape(chunk), missing)
    doc = ''.join(parts)

    # Translate readable attributes.
    def attr(m: re.Match) -> str:
        name, value = m.group(1), m.group(2)
        if name == 'content' and not re.search(r'[A-Za-z]{3,} ', htmllib.unescape(value)):
            return m.group(0)
        return f'{name}="{htmllib.escape(tr(htmllib.unescape(value), missing), quote=True)}"'
    doc = re.sub(r'\b(alt|aria-label|title|content)="([^"]*)"', attr, doc)

    # Internal page links point to the Malayalam pages.
    doc = doc.replace('<html lang="en">', '<html lang="ml">', 1)
    doc = doc.replace('href="/"', 'href="/ml"')
    for p in PAGE_PATHS:
        doc = doc.replace(f'href="{p}"', f'href="/ml{p}"')
    # Keep the alternate-language links correct.
    doc = doc.replace(f'<link rel="alternate" hreflang="en" href="{ml_path(path)}">', f'<link rel="alternate" hreflang="en" href="{path}">')
    # Language switch goes back to English.
    doc = re.sub(r'<a class="lang-switch" href="[^"]*" hreflang="ml" lang="ml">മലയാളം</a>',
                 f'<a class="lang-switch" href="{path}" hreflang="en" lang="en">English</a>', doc)
    # The hero shows the name in the other language under the logo; drop duplicate Malayalam labels.
    doc = doc.replace('<p class="hero-ml" lang="ml">മടിക്കൈ പ്രവാസി അസോസിയേഷൻ</p>', '<p class="hero-ml" lang="en">Madikai Pravasi Association</p>')
    doc = doc.replace(' <span class="ml" lang="ml">സ്നേഹവീട്</span>', '')
    return doc


def build() -> None:
    hero = part('top').replace('href="#about"', 'href="/about"').replace('href="#gallery"', 'href="/gallery"')
    about = part('about')
    support = part('support')

    about_page = about.replace('        <p class="eyebrow">About us</p>\n', '')
    pages = {
        'index.html': ('/', 'Home', hero + '  <div class="kasavu" aria-hidden="true"></div>\n\n' + about + '\n' + explore() + '\n' + support, ''),
        'about.html': ('/about', 'About us', banner('About us', 'A community of families from Madikai Panchayath, Kasaragod, living in the UAE.') + about_page, ''),
    }
    # The hero section file already ends before the kasavu strip; keep it clean.
    for file, (path, sec_id, label) in {
        'initiatives.html': ('/initiatives', 'initiatives', 'Our initiatives'),
        'office-bearers.html': ('/office-bearers', 'bearers', 'Office bearers'),
        'gallery.html': ('/gallery', 'gallery', 'Gallery'),
        'contact.html': ('/contact', 'contact', 'Contact us'),
    }.items():
        body, h2, lede = strip_intro(part(sec_id))
        main = banner(label, lede) + body
        if sec_id == 'contact':
            main += '\n' + support
        pages[file] = (path, label, main, part('lightbox') if sec_id == 'gallery' else '')

    missing: set = set()
    (ROOT / 'ml').mkdir(exist_ok=True)
    for file, (path, title, main, extra) in pages.items():
        doc = page(path, title, main, extra)
        (ROOT / file).write_text(doc)
        (ROOT / 'ml' / file).write_text(to_malayalam(doc, path, missing))
    if missing:
        print('Missing Malayalam for:')
        for m in sorted(missing):
            print('  -', m)

    (ROOT / 'assets').mkdir(exist_ok=True)
    (ROOT / 'assets' / 'site.css').write_text((SRC / 'site.css').read_text())
    (ROOT / 'assets' / 'site.js').write_text((SRC / 'site.js').read_text())
    print('Built:', ', '.join(pages))


if __name__ == '__main__':
    build()
