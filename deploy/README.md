# Files for the rest of fabiometa.com

The repository root is the portfolio: its contents go in
`public_html/portfolio/` on Vimexx (`index.html`, `sitemap.xml`, `assets/`).

The files in `deploy/public_html/` go one level up, in `public_html/` itself:

| File | Goes to | What it does |
|---|---|---|
| `index.html` | `public_html/index.html` | Sends fabiometa.com to the portfolio (replaces the Flow State page) |
| `robots.txt` | `public_html/robots.txt` | Tells search engines where the sitemap is |
| `fabiomedia/index.html` | `public_html/fabiomedia/index.html` | Sends the old portfolio link to the new one |

Leave everything else in `public_html` alone, especially `shop/`, `cgi-bin/`
and the Google verification file `google2aac0d0b5ff29d71.html`.
