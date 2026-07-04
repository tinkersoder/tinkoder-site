# Tinkoder — tinkoder.fi

Complete bilingual (FI/EN) static website. No build step, no frameworks —
semantic HTML5, modern CSS, vanilla JS. Deployable to any static host
(Netlify, Cloudflare Pages, GitHub Pages, or a plain nginx server).

## Structure

```
/                      Finnish site (default language)
├── index.html         Etusivu
├── palvelut.html      Palvelut (6 service areas with anchors)
├── portfolio.html     Portfolio (6 case studies)
├── tietoa.html        Tietoa meistä
├── yhteys.html        Yhteystiedot + lomake
├── tietosuoja.html    Tietosuojaseloste
├── 404.html           Not found (bilingual)
├── en/                English site (mirrors every page)
│   ├── index.html  services.html  portfolio.html
│   ├── about.html  contact.html   privacy.html
├── css/styles.css     Design tokens, themes, components
├── css/animations.css Motion (respects prefers-reduced-motion)
├── js/script.js       Language memory, theme, nav, reveals, form
├── assets/            logo.svg, favicon.svg  (+ add og-image.png)
├── robots.txt
└── sitemap.xml        Bilingual, hreflang-annotated
```

## Brand guide

| Element     | Choice |
|-------------|--------|
| Tagline FI  | "Me rakennamme sen, mitä ei ole olemassa." |
| Tagline EN  | "We build what doesn't exist yet." |
| Personality | Nordic workshop: calm, precise, quietly playful. Technical but never intimidating. Says "let's see what's possible" instead of "no". |
| Palette     | Birch paper `#F6F7F4` · Spruce `#1B5E4A` · Signal amber `#E9A13B` · Ink `#182420` · Night `#0F1513` (dark bg) |
| Display type| Bricolage Grotesque |
| Body type   | Instrument Sans |
| Spec/labels | Spline Sans Mono — used for the CAD-drawing motif |
| Logo        | Hex nut containing a "T" whose stem ends in a circuit node (assets/logo.svg) |
| Signature   | CAD dimension-line motif: hero technical drawing that draws itself in, mono spec chips ("PETG · 0.2 mm") and dimension-tick eyebrows throughout |
| Icon style  | 2px stroke, rounded caps, single colour (currentColor) |
| Illustration| Line-art technical drawings, never stock photos |

## Language system

- Finnish at the root, English under `/en/` — real URLs, ideal for SEO.
- The switch in the nav stores the choice in `localStorage`
  (`tinkoder-lang`); returning visitors landing on the front page are
  redirected to their preferred language once per session, but an explicit
  click always wins.
- Every page pair carries `hreflang` alternates, localized `<title>`,
  meta description, Open Graph and JSON-LD; the sitemap repeats the
  hreflang pairs.

## Dark / light mode

Follows the OS by default; the toggle stores an override in
`localStorage` (`tinkoder-theme`). An inline `<head>` script applies the
theme before first paint to prevent flashing.

## Before going live

1. Replace `info@tinkoder.fi` placeholder details, business ID, opening
   hours and social links.
2. Add `assets/og-image.png` (1200×630) for link previews.
3. Wire the contact form: in `js/script.js`, replace the demo `setTimeout`
   with a `fetch()` to Formspree/Web3Forms or your own endpoint.
4. Replace placeholder testimonials with real ones.
5. Configure the server to serve `404.html` for missing paths, and
   `/en/` → `/en/index.html`.

## Future expansion (already accounted for)

The flat-URL structure and shared shell leave clean namespaces for:
`/kauppa/` (shop), `/blogi/` (blog), `/ohjeet/` (knowledge base),
`/galleria/`, `/asiakas/` (customer portal), `/varaa/` (booking) and a
quote calculator on the contact page. New pages only need the shared
header/footer and a content block — see how `build_pages.py`
(included for reference at the repo root during development) composed
the current pages.
