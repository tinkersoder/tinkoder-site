#!/usr/bin/env python3
"""Generate Tinkoder subpages from a shared shell + per-page content."""
import os

ROOT = "/home/claude/tinkoder"

HEAD = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://tinkoder.fi{canon}">
  <link rel="alternate" hreflang="fi" href="https://tinkoder.fi{fi_url}">
  <link rel="alternate" hreflang="en" href="https://tinkoder.fi{en_url}">
  <link rel="alternate" hreflang="x-default" href="https://tinkoder.fi{fi_url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Tinkoder">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://tinkoder.fi{canon}">
  <meta property="og:image" content="https://tinkoder.fi/assets/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;600;700&family=Instrument+Sans:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">
  <link rel="stylesheet" href="/css/animations.css">
  <script>
    (function(){{try{{var t=localStorage.getItem("tinkoder-theme");
    if(t==="dark"||(!t&&matchMedia("(prefers-color-scheme: dark)").matches))
    document.documentElement.setAttribute("data-theme","dark");}}catch(e){{}}}})();
  </script>
</head>
<body>
"""

NAV_FI = """  <a class="skip-link" href="#main">Siirry sisältöön</a>
  <header class="header">
    <nav class="nav container" aria-label="Päävalikko">
      <a class="nav__logo" href="/" aria-label="Tinkoder — etusivu">
        <svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 4 L54 16 V48 L32 60 L10 48 V16 Z" stroke="var(--primary)" stroke-width="4" stroke-linejoin="round"/><path d="M20 22 H44 M32 22 V42" stroke="var(--primary)" stroke-width="4" stroke-linecap="round"/><circle cx="32" cy="46" r="4" fill="var(--accent)"/></svg>
        Tinkoder
      </a>
      <button class="nav__burger" aria-expanded="false" aria-controls="nav-links" aria-label="Avaa valikko">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      </button>
      <ul class="nav__links" id="nav-links">
        <li><a href="/"{c_home}>Etusivu</a></li>
        <li><a href="/palvelut.html"{c_services}>Palvelut</a></li>
        <li><a href="/portfolio.html"{c_portfolio}>Portfolio</a></li>
        <li><a href="/tietoa.html"{c_about}>Tietoa</a></li>
        <li><a href="/yhteys.html"{c_contact}>Yhteystiedot</a></li>
      </ul>
      <div class="nav__actions">
        <div class="lang-switch" aria-label="Kielivalinta">
          <span aria-current="true" lang="fi">FI</span>
          <a href="{alt_url}" data-lang-link="en" lang="en" hreflang="en">EN</a>
        </div>
        <button class="theme-toggle" aria-label="Vaihda tumman ja vaalean tilan välillä">
          <svg class="icon-moon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
          <svg class="icon-sun" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
      </div>
    </nav>
  </header>
  <main id="main">
"""

NAV_EN = NAV_FI.replace("Siirry sisältöön", "Skip to content") \
    .replace('aria-label="Päävalikko"', 'aria-label="Main navigation"') \
    .replace('href="/" aria-label="Tinkoder — etusivu"', 'href="/en/" aria-label="Tinkoder — home"') \
    .replace('aria-label="Avaa valikko"', 'aria-label="Open menu"') \
    .replace('<li><a href="/"{c_home}>Etusivu</a></li>', '<li><a href="/en/"{c_home}>Home</a></li>') \
    .replace('<li><a href="/palvelut.html"{c_services}>Palvelut</a></li>', '<li><a href="/en/services.html"{c_services}>Services</a></li>') \
    .replace('<li><a href="/portfolio.html"{c_portfolio}>Portfolio</a></li>', '<li><a href="/en/portfolio.html"{c_portfolio}>Portfolio</a></li>') \
    .replace('<li><a href="/tietoa.html"{c_about}>Tietoa</a></li>', '<li><a href="/en/about.html"{c_about}>About</a></li>') \
    .replace('<li><a href="/yhteys.html"{c_contact}>Yhteystiedot</a></li>', '<li><a href="/en/contact.html"{c_contact}>Contact</a></li>') \
    .replace('aria-label="Kielivalinta"', 'aria-label="Language selection"') \
    .replace('<span aria-current="true" lang="fi">FI</span>\n          <a href="{alt_url}" data-lang-link="en" lang="en" hreflang="en">EN</a>',
             '<a href="{alt_url}" data-lang-link="fi" lang="fi" hreflang="fi">FI</a>\n          <span aria-current="true" lang="en">EN</span>') \
    .replace('aria-label="Vaihda tumman ja vaalean tilan välillä"', 'aria-label="Toggle between dark and light mode"')

FOOTER_FI = """  </main>
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="nav__logo" href="/">Tinkoder</a>
          <p style="color:var(--muted); max-width:26em; margin-top:.8rem">Räätälöidyt tekniset ratkaisut Tampereelta koko Suomeen. Suunnittelemme ja rakennamme sen, mitä kaupasta ei saa.</p>
        </div>
        <div>
          <h4>Palvelut</h4>
          <ul>
            <li><a href="/palvelut.html#3d-tulostus">3D-tulostus</a></li>
            <li><a href="/palvelut.html#elektroniikka">Elektroniikka</a></li>
            <li><a href="/palvelut.html#alykoti">Älykoti</a></li>
            <li><a href="/palvelut.html#tuotekehitys">Tuotekehitys</a></li>
          </ul>
        </div>
        <div>
          <h4>Yritys</h4>
          <ul>
            <li><a href="/tietoa.html">Tietoa meistä</a></li>
            <li><a href="/portfolio.html">Portfolio</a></li>
            <li><a href="/yhteys.html">Yhteystiedot</a></li>
            <li><a href="/tietosuoja.html">Tietosuoja</a></li>
          </ul>
        </div>
        <div>
          <h4>Yhteys</h4>
          <ul>
            <li><a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a></li>
            <li>Tampere, Suomi</li>
            <li><a href="#" aria-label="Instagram (paikkamerkki)">Instagram</a></li>
            <li><a href="#" aria-label="YouTube (paikkamerkki)">YouTube</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__meta">
        <span>© 2026 Tinkoder · Y-tunnus 0000000-0</span>
        <span><a href="{alt_url}" data-lang-link="en" hreflang="en">This page in English</a></span>
      </div>
    </div>
  </footer>
  <script src="/js/script.js" defer></script>
</body>
</html>
"""

FOOTER_EN = """  </main>
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <a class="nav__logo" href="/en/">Tinkoder</a>
          <p style="color:var(--muted); max-width:26em; margin-top:.8rem">Custom technical solutions from Tampere, serving all of Finland. We design and build what you can't buy off the shelf.</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="/en/services.html#3d-printing">3D printing</a></li>
            <li><a href="/en/services.html#electronics">Electronics</a></li>
            <li><a href="/en/services.html#smart-home">Smart home</a></li>
            <li><a href="/en/services.html#product-development">Product development</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="/en/about.html">About us</a></li>
            <li><a href="/en/portfolio.html">Portfolio</a></li>
            <li><a href="/en/contact.html">Contact</a></li>
            <li><a href="/en/privacy.html">Privacy policy</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="mailto:info@tinkoder.fi">info@tinkoder.fi</a></li>
            <li>Tampere, Finland</li>
            <li><a href="#" aria-label="Instagram (placeholder)">Instagram</a></li>
            <li><a href="#" aria-label="YouTube (placeholder)">YouTube</a></li>
          </ul>
        </div>
      </div>
      <div class="footer__meta">
        <span>© 2026 Tinkoder · Business ID 0000000-0</span>
        <span><a href="{alt_url}" data-lang-link="fi" hreflang="fi">Tämä sivu suomeksi</a></span>
      </div>
    </div>
  </footer>
  <script src="/js/script.js" defer></script>
</body>
</html>
"""

def build(path, lang, title, desc, fi_url, en_url, active, content):
    canon = fi_url if lang == "fi" else en_url
    head = HEAD.format(lang=lang, title=title, desc=desc, canon=canon,
                       fi_url=fi_url, en_url=en_url,
                       og_locale="fi_FI" if lang == "fi" else "en_GB")
    cur = {k: "" for k in ("c_home", "c_services", "c_portfolio", "c_about", "c_contact")}
    if active: cur["c_" + active] = ' aria-current="page"'
    alt = en_url if lang == "fi" else fi_url
    nav = (NAV_FI if lang == "fi" else NAV_EN).format(alt_url=alt, **cur)
    foot = (FOOTER_FI if lang == "fi" else FOOTER_EN).format(alt_url=alt)
    full = head + nav + content + foot
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(full)
    print("wrote", path)

# Page content is defined in content_pages.py to keep this file readable
from content_pages import PAGES
for p in PAGES:
    build(**p)
print("done")
