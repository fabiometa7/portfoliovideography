"""Builds the Dutch service and case pages from one template.

Run from the repository root after changing any page content below:
    python3 tools/build-pages.py
Each page is written as <slug>.html next to index.html, so on the server it
lands in public_html/portfolio/ with no extra folders.
"""
import html
import json
import pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://fabiometa.com/portfolio/"
BUSINESS_ID = "https://fabiometa.com/#business"
WA_NUMBER = "31682832393"
PUBLISHED = "2026-10-21"

# file stem -> (title shown under the player, client, seconds)
VIDEOS = {
    "albrecht-01": ("Bij Albrecht 01", "Bij Albrecht", 23),
    "albrecht-02": ("Bij Albrecht 02", "Bij Albrecht", 23),
    "albrecht-03": ("Bij Albrecht 03", "Bij Albrecht", 23),
    "hvc-trailer": ("Trailer", "The High Value Club", 114),
    "hvc-testimonial-01": ("Testimonial 01", "The High Value Club", 94),
    "hvc-testimonial-02": ("Testimonial 02", "The High Value Club", 94),
    "hvc-testimonial-03": ("Testimonial 03", "The High Value Club", 90),
    "hvc-testimonial-04": ("Testimonial 04", "The High Value Club", 97),
    "hvc-culture-insights-01": ("Culture Insights 01", "The High Value Club", 122),
    "hvc-coaches-corner": ("Coaches Corner", "The High Value Club", 31),
    "qbuzz-04": ("Veilig werken 01", "Qbuzz", 32),
    "qbuzz-01": ("Veilig werken 02", "Qbuzz", 46),
    "qbuzz-02": ("Veilig werken 03", "Qbuzz", 27),
    "qbuzz-03": ("Veilig werken 04", "Qbuzz", 34),
    "qbuzz-05": ("Veilig werken 05", "Qbuzz", 44),
    "ugc-gardpro": ("Gardpro", "UGC", 19),
    "ugc-oakley": ("Oakley", "UGC", 10),
    "ugc-oversized-studios": ("Oversized Studios", "UGC", 11),
}

SERVICE_LINKS = [
    ("bedrijfsvideo-eindhoven.html", "Bedrijfsvideo laten maken", "Trailers, medewerkersvideo's en bedrijfsfilms"),
    ("horeca-video.html", "Video & content voor horeca", "Restaurants, hotels, bars en events"),
    ("testimonial-video.html", "Testimonial video's", "Klantverhalen, interviews en podcasts"),
    ("social-media-content.html", "Reels, TikToks & ads", "Short-form content, UGC en paid ads"),
]
CASE_LINKS = [
    ("case-the-high-value-club.html", "Case: The High Value Club", "Ads, testimonials, podcasts en een eventdag"),
    ("case-bij-albrecht.html", "Case: Bij Albrecht", "Restaurantcontent van keuken tot bord"),
    ("case-qbuzz.html", "Case: Qbuzz", "Medewerkers aan het woord over veilig werken"),
]

WA_SVG = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35zM12.04 21.5h-.01a9.45 9.45 0 0 1-4.82-1.32l-.35-.21-3.58.94.96-3.49-.23-.36a9.43 9.43 0 0 1-1.45-5.03c0-5.22 4.25-9.47 9.48-9.47 2.53 0 4.91.99 6.7 2.78a9.41 9.41 0 0 1 2.77 6.7c0 5.22-4.25 9.47-9.47 9.47zm8.06-17.53A11.33 11.33 0 0 0 12.04.63C5.76.63.65 5.74.65 12.02c0 2.01.52 3.97 1.52 5.69L.55 23.6l6.04-1.58a11.36 11.36 0 0 0 5.44 1.39h.01c6.28 0 11.39-5.11 11.39-11.39 0-3.04-1.18-5.9-3.33-8.05z"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' "
           "fill='%230a0a0c'/%3E%3Ctext x='14' y='46' font-family='Arial,sans-serif' font-weight='800' font-size='40' fill='%23f4f4f6'%3EF%3C/text%3E"
           "%3Ccircle cx='48' cy='44' r='5' fill='%23ff5d3b'/%3E%3C/svg%3E")


def wa_link(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


def video_figure(stem):
    title, client, _ = VIDEOS[stem]
    return (f'<figure class="vid"><video controls playsinline preload="none" poster="assets/work/{stem}.jpg" '
            f'src="assets/work/{stem}.mp4" aria-label="{html.escape(title)}, {html.escape(client)}"></video>'
            f'<figcaption><b>{html.escape(title)}</b> · {html.escape(client)}</figcaption></figure>')


def video_object(stem, description):
    title, client, seconds = VIDEOS[stem]
    return {
        "@type": "VideoObject",
        "name": f"{title}: {client}" if client != "UGC" else f"UGC: {title}",
        "description": description,
        "thumbnailUrl": f"{SITE}assets/work/{stem}.jpg",
        "contentUrl": f"{SITE}assets/work/{stem}.mp4",
        "uploadDate": PUBLISHED,
        "duration": f"PT{seconds}S",
    }


def render(page):
    url = SITE + page["slug"]
    links = [l for l in SERVICE_LINKS + CASE_LINKS if l[0] != page["slug"]]
    graph = [
        {"@type": "ProfessionalService", "@id": BUSINESS_ID, "name": "Fabio Media", "url": SITE},
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Portfolio", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url},
            ],
        },
        {
            "@type": "Service" if page["kind"] == "service" else "CreativeWork",
            "name": page["h1"],
            "description": page["description"],
            ("provider" if page["kind"] == "service" else "creator"): {"@id": BUSINESS_ID},
            **({"areaServed": ["Eindhoven", "Noord-Brabant", "Nederland"]} if page["kind"] == "service" else {}),
            "url": url,
        },
        *[video_object(stem, page["description"]) for stem in page["videos"]],
    ]
    if page.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]],
        })
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

    wa = wa_link(page["wa_text"])
    videos_class = "videos four" if len(page["videos"]) == 4 else "videos"
    sections = "\n".join(f'    <section>\n      <div class="wrap">\n        <h2>{h}</h2>\n{body}\n      </div>\n    </section>'
                         for h, body in page["sections"])
    faq = ""
    if page.get("faq"):
        items = "\n".join(f'        <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in page["faq"])
        faq = f'    <section>\n      <div class="wrap">\n        <h2>Veelgestelde vragen</h2>\n{items}\n      </div>\n    </section>'
    more = "\n".join(f'          <a href="{href}">{html.escape(label)}<span>{html.escape(sub)}</span></a>' for href, label, sub in links)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>{html.escape(page["title"])}</title>
<meta name="description" content="{html.escape(page["description"])}" />
<link rel="canonical" href="{url}" />
<meta name="theme-color" content="#0a0a0c" />
<link rel="icon" href="{FAVICON}" />
<link rel="stylesheet" href="assets/site.css" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Fabio Media" />
<meta property="og:locale" content="nl_NL" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{html.escape(page["title"])}" />
<meta property="og:description" content="{html.escape(page["description"])}" />
<meta property="og:image" content="{SITE}assets/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a class="brand" href="./">FABIO<span>.</span></a>
      <div class="nav-links">
        <a href="./">Portfolio</a>
        <a href="./#services">Diensten</a>
        <a href="./#cases">Cases</a>
        <a class="nav-wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </nav>

  <main>
    <header class="hero">
      <div class="wrap">
        <p class="crumbs"><a href="./">Portfolio</a> / {html.escape(page["crumb"])}</p>
        <div class="eyebrow" style="margin-top:22px">{html.escape(page["eyebrow"])}</div>
        <h1>{html.escape(page["h1"])}</h1>
        <p class="lead">{page["lead"]}</p>
        <div class="ctas">
          <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}Stuur een WhatsApp</a>
          <a class="btn btn-ghost" href="./#work">Bekijk al het werk</a>
        </div>
      </div>
    </header>

    <section>
      <div class="wrap">
        <h2>{html.escape(page["videos_title"])}</h2>
        <div class="{videos_class}">
          {"".join(video_figure(s) for s in page["videos"])}
        </div>
      </div>
    </section>

{sections}

{faq}

    <section>
      <div class="wrap">
        <h2>Meer werk en diensten</h2>
        <div class="more">
{more}
        </div>
      </div>
    </section>

    <section class="final">
      <div class="wrap">
        <h2>{html.escape(page["final_title"])}</h2>
        <p>Stuur een WhatsApp met wat je bedrijf doet en wat je zoekt. Je krijgt ideeën en een voorstel op maat, zonder verplichtingen.</p>
        <div class="ctas">
          <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{WA_SVG}Stuur een WhatsApp</a>
          <a class="btn btn-ghost" href="./#contact">Liever een formulier</a>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <span>© 2026 Fabio Media · Eindhoven · KvK 42019388</span>
      <span><a href="./#privacy">Privacyverklaring</a> · <a href="https://www.instagram.com/fabiometa_/" target="_blank" rel="noopener">Instagram</a> · <a href="mailto:fabiometacollabs@gmail.com">fabiometacollabs@gmail.com</a></span>
    </div>
  </footer>

  <a class="wa-float" href="{wa}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a>
</body>
</html>
"""


def prose(inner):
    return f'        <div class="prose">\n{inner}\n        </div>'


def cards(items):
    body = "\n".join(f'          <div class="card"><h3>{h}</h3><p>{t}</p></div>' for h, t in items)
    return f'        <div class="cards">\n{body}\n        </div>'


def steps(items):
    body = "\n".join(f'          <div class="step"><h3>{h}</h3><p>{t}</p></div>' for h, t in items)
    return f'        <div class="steps">\n{body}\n        </div>'


PROCESS = steps([
    ("Kennismaken", "Je stuurt een WhatsApp of we bellen kort. Ik wil weten wat je bedrijf doet, wie je klanten zijn en wat de video moet opleveren."),
    ("Plan", "Je krijgt een voorstel met ideeën, een globaal script of draaiboek en een planning. Pas als dat klopt, gaan we filmen."),
    ("Opnamedag", "Ik film op jouw locatie met eigen camera, licht en geluid. We plannen het zo dat je bedrijf gewoon kan doordraaien."),
    ("Montage en oplevering", "Ik monteer, voeg ondertitels en muziek toe en verwerk jouw feedback. Je krijgt de video's in alle formaten die je nodig hebt."),
])

PAGES = [
    {
        "slug": "bedrijfsvideo-eindhoven.html",
        "kind": "service",
        "crumb": "Bedrijfsvideo",
        "title": "Bedrijfsvideo laten maken in Eindhoven | Fabio Media",
        "description": "Bedrijfsvideo laten maken in Eindhoven of Brabant? Fabio Media maakt bedrijfsfilms, trailers, medewerkersvideo's en klantverhalen voor je website, socials en advertenties.",
        "eyebrow": "Videoproductie · Eindhoven & Brabant",
        "h1": "Bedrijfsvideo laten maken in Eindhoven",
        "lead": "Een goede bedrijfsvideo laat in een paar minuten zien waar je voor staat, wie er achter je bedrijf zitten en waarom klanten voor je kiezen. Ik bedenk het verhaal, film en monteer, zodat jij een video krijgt die je op je website, op social media en in advertenties kunt gebruiken.",
        "wa_text": "Hoi Fabio, ik zag je pagina over bedrijfsvideo's en wil graag meer weten.",
        "videos_title": "Voorbeelden",
        "videos": ["hvc-trailer", "qbuzz-04", "hvc-testimonial-01"],
        "sections": [
            ("Wat voor bedrijfsvideo's ik maak", cards([
                ("Bedrijfstrailer", "Een korte film over je bedrijf, je mensen en je plek, zoals de trailer voor sportschool The High Value Club."),
                ("Medewerkersvideo's", "Je eigen mensen vertellen het verhaal. Sterk voor employer branding en interne campagnes, zoals de reeks voor Qbuzz."),
                ("Klantverhalen", "Tevreden klanten die in hun eigen woorden vertellen wat je voor ze hebt gedaan."),
                ("Eventvideo's", "Een eventdag, opening of lancering, vastgelegd voor je socials en je website."),
            ])),
            ("Eén opnamedag, veel content", prose(
                "          <p>Een bedrijfsvideo hoeft niet op één plek te blijven staan. Van dezelfde opnames maak ik naast de hoofdvideo ook <strong>korte verticale versies</strong> voor Instagram, TikTok en LinkedIn, en <strong>advertentieversies</strong> met verschillende openingen om te testen. Zo haal je veel meer uit één opnamedag.</p>\n"
                "          <p>Alle video's krijgen ondertitels, omdat de meeste mensen op hun telefoon kijken zonder geluid.</p>")),
            ("Zo werkt het", PROCESS),
            ("Voor wie", prose(
                "          <p>Ik werk voor ondernemers, sportclubs, horeca, merken en organisaties in <strong>Eindhoven en de rest van Brabant</strong>. Voor projecten elders in Nederland kom ik ook langs, dat spreken we per opdracht af. Video's maak ik in het Nederlands of het Engels.</p>")),
        ],
        "faq": [
            ("Wat kost een bedrijfsvideo?", "Dat hangt af van het aantal opnamedagen, video's en versies. Een pilot met één opnamedag en zes korte video's begint vanaf 750 euro. Voor grotere projecten of maandelijkse content krijg je een voorstel op maat."),
            ("Hoe lang duurt het voordat mijn video klaar is?", "Dat hangt af van de omvang van het project. De planning spreek ik vooraf met je af, zodat je precies weet wanneer je wat krijgt."),
            ("Werk je alleen in Eindhoven?", "Ik werk vooral in Eindhoven en Brabant, maar kom ook naar andere plekken in Nederland. Dat bespreken we per project."),
            ("Krijg ik ook versies voor social media?", "Ja. Naast de hoofdvideo maak ik verticale versies voor Instagram, TikTok en LinkedIn, met ondertitels."),
            ("Mag ik de video's gebruiken voor advertenties?", "Ja. Je kunt de video's zelf inzetten op je website, je socials en in advertenties. Op verzoek maak ik er speciale advertentieversies van."),
        ],
        "final_title": "Een bedrijfsvideo die echt iets oplevert?",
    },
    {
        "slug": "horeca-video.html",
        "kind": "service",
        "crumb": "Horeca video",
        "title": "Horeca video en content laten maken | Restaurant, hotel en events | Fabio Media",
        "description": "Video en social media content voor restaurants, hotels, bars en events in Eindhoven en Brabant. Korte video's van je keuken, gerechten en sfeer die gasten naar binnen halen.",
        "eyebrow": "Restaurants · hotels · bars · events",
        "h1": "Video en content voor horeca",
        "lead": "Gasten kiezen met hun ogen. Voor ze reserveren, kijken ze op Instagram, TikTok en Google hoe je zaak eruitziet. Ik maak korte video's van je keuken, je gerechten en de sfeer, die laten zien waarom ze juist bij jou moeten zijn.",
        "wa_text": "Hoi Fabio, ik zag je pagina over horeca video's en wil graag meer weten.",
        "videos_title": "Voorbeelden: restaurant Bij Albrecht",
        "videos": ["albrecht-02", "albrecht-01", "albrecht-03"],
        "sections": [
            ("Wat ik voor je maak", cards([
                ("Gerechten", "Close-ups van het opmaken en serveren, zodat mensen het eten bijna kunnen proeven."),
                ("Keuken en team", "Je chef en je team in actie. Dat geeft je zaak een gezicht."),
                ("Sfeer en interieur", "De plek, het licht en de gasten: het gevoel van een avond bij jou."),
                ("Menu's en events", "Een nieuw seizoensmenu, een proeverij of een opening, vastgelegd voor je socials."),
            ])),
            ("Waarom video werkt in de horeca", prose(
                "          <p>Een foto van een gerecht laat zien wat er op het bord ligt. Een video laat zien hoe het er komt, hoe de zaak klinkt en hoe het voelt om er te zitten. Precies dat maakt het verschil tussen doorscrollen en reserveren.</p>\n"
                "          <p>Korte verticale video's werken op <strong>Instagram, TikTok en je Google-profiel</strong>. Met een vaste stroom content blijf je zichtbaar bij mensen die nog moeten kiezen waar ze gaan eten.</p>")),
            ("Hoe een opnamedag eruitziet", prose(
                "          <p>Ik film rond jullie service, bijvoorbeeld voor openingstijd of op een rustig moment, zodat de keuken en de gasten er geen last van hebben. Gerechten film ik terwijl ze echt worden opgemaakt. Dat ziet er natuurlijker uit dan alles neerzetten voor de camera.</p>\n"
                "          <p>Na de opnamedag krijg je kant-en-klare video's met ondertitels, klaar om te posten.</p>")),
            ("Eenmalig of elke maand", prose(
                "          <p>Je kunt beginnen met een <strong>pilot</strong>: één opnamedag en zes korte video's. Bevalt het, dan kan het maandelijks, met vaste opnamedagen en elke maand nieuwe content. Zo hoef je zelf niet meer na te denken over wat je moet posten.</p>")),
        ],
        "faq": [
            ("Kun je filmen zonder dat het de service stoort?", "Ja. We plannen de opnames voor openingstijd of op een rustig moment, en ik werk met een kleine set zodat keuken en gasten er weinig van merken."),
            ("Hoeveel video's krijg ik per opnamedag?", "Dat hangt af van wat we filmen. Bij een pilot zijn het zes korte video's van één opnamedag."),
            ("Plaats je de video's ook?", "Ik lever de video's kant-en-klaar aan, met suggesties voor de teksten. Wil je ook hulp bij de planning van je posts, dan nemen we dat mee in het voorstel."),
            ("Werk je ook voor hotels, bars en events?", "Ja. Ik maak content voor restaurants, hotels, bars, eventlocaties en evenementen in Eindhoven, Brabant en daarbuiten."),
        ],
        "final_title": "Zin in video's die gasten naar binnen halen?",
    },
    {
        "slug": "testimonial-video.html",
        "kind": "service",
        "crumb": "Testimonial video",
        "title": "Testimonial video laten maken | Klantverhalen op video | Fabio Media",
        "description": "Testimonialvideo's en klantverhalen laten maken in Eindhoven en Brabant. Echte klanten aan het woord, mooi gefilmd en ondertiteld, voor je website, socials en advertenties.",
        "eyebrow": "Klantverhalen · interviews · podcasts",
        "h1": "Testimonial video's die vertrouwen opbouwen",
        "lead": "Niets overtuigt een twijfelende klant zo goed als iemand die hem voorging. Ik film je klanten terwijl ze in hun eigen woorden vertellen wat jouw bedrijf voor ze heeft gedaan, en maak daar ondertitelde video's van die je overal kunt gebruiken.",
        "wa_text": "Hoi Fabio, ik zag je pagina over testimonial video's en wil graag meer weten.",
        "videos_title": "Voorbeelden: leden van The High Value Club",
        "videos": ["hvc-testimonial-01", "hvc-testimonial-02", "hvc-testimonial-03", "hvc-testimonial-04"],
        "sections": [
            ("Wat je krijgt", cards([
                ("Echt verhaal", "Geen script, maar een ontspannen interview. Zo klinken je klanten als zichzelf."),
                ("Beelden erbij", "Naast het interview film ik je klant in actie, zodat de video blijft boeien."),
                ("Ondertiteld", "De meeste mensen kijken zonder geluid. Met ondertitels komt je boodschap toch over."),
                ("Elke lengte", "Een langere versie voor je website en korte versies voor socials en advertenties."),
            ])),
            ("Zo maak ik een testimonial", prose(
                "          <p>Vooraf stemmen we af welke klanten we filmen en wat je wilt laten zien. Tijdens het interview stel ik open vragen, zodat het een gesprek wordt in plaats van een opgezegd lijstje. Daarna film ik beelden van de klant bij jou, zoals bij The High Value Club, waar leden ook tijdens hun training te zien zijn.</p>\n"
                "          <p>In de montage haal ik de sterkste momenten eruit en maak ik er een strak verhaal van, met ondertitels en muziek.</p>")),
            ("Ook podcasts en interviews", prose(
                "          <p>Naast testimonials monteer ik ook podcasts en interviewreeksen. Voor The High Value Club maakte ik de reeksen <strong>Culture Insights</strong> en <strong>Coaches Corner</strong>: korte, ondertitelde video's waarin leden en coaches vertellen over de club.</p>")),
            ("Zo werkt het", PROCESS),
        ],
        "faq": [
            ("Mijn klanten zijn niet gewend aan een camera. Is dat een probleem?", "Nee. Ik werk zonder script en stel open vragen, zodat het als een gewoon gesprek voelt. De meeste mensen vergeten de camera na een paar minuten."),
            ("Hoeveel klanten kun je op één dag filmen?", "Op één locatie kunnen vaak meerdere klanten na elkaar aan de beurt komen. Dat plannen we samen, zodat het voor iedereen goed uitkomt."),
            ("Krijgen de video's ondertitels?", "Ja, alle testimonials worden ondertiteld, in het Nederlands of het Engels."),
            ("Kan ik testimonials gebruiken als advertentie?", "Ja. Testimonials zijn juist sterk als advertentie. Ik maak er op verzoek korte versies van met verschillende openingen om te testen."),
        ],
        "final_title": "Laat je klanten het verhaal vertellen",
    },
    {
        "slug": "social-media-content.html",
        "kind": "service",
        "crumb": "Reels, TikToks en ads",
        "title": "Reels, TikToks en ads laten maken | Social media content | Fabio Media",
        "description": "Social media content en video-advertenties laten maken: reels, TikToks, YouTube Shorts, UGC en paid ads voor Meta en TikTok. Videoproductie uit Eindhoven voor heel Nederland.",
        "eyebrow": "Short-form content · UGC · paid ads",
        "h1": "Reels, TikToks en ads laten maken",
        "lead": "Op social media heb je één seconde om op te vallen. Ik maak korte video's met een sterke opening, een strakke montage en ondertitels, voor je eigen kanalen en voor advertenties op Meta en TikTok.",
        "wa_text": "Hoi Fabio, ik zag je pagina over social media content en ads en wil graag meer weten.",
        "videos_title": "Voorbeelden",
        "videos": ["ugc-gardpro", "hvc-coaches-corner", "ugc-oakley"],
        "sections": [
            ("Wat ik maak", cards([
                ("Organische content", "Reels, TikToks en Shorts die je merk zichtbaar maken en volgers omzetten in klanten."),
                ("Paid ads", "Concept, script, opname en montage voor advertenties op Meta en TikTok, in meerdere versies om te testen."),
                ("UGC", "Video's in de stijl van een creator, die voelen als een aanbeveling in plaats van reclame."),
                ("AI-content", "AI-effecten en visuals die opvallen in de feed. Mijn best bekeken video haalde meer dan 500.000 views."),
            ])),
            ("Ads die je kunt testen", prose(
                "          <p>Bij advertenties wint niet altijd de mooiste video, maar de video die het beste werkt. Daarom lever ik ads in <strong>meerdere versies</strong>: andere openingen, andere lengtes en formaten voor feed, stories en reels. Zo zie je snel wat jouw doelgroep aanspreekt.</p>\n"
                "          <p>Voor The High Value Club maakte ik onder meer advertenties om nieuwe leden te werven, naast organische content zoals de reeks Coaches Corner.</p>")),
            ("UGC voor merken", prose(
                "          <p>Als UGC-creator maakte ik video's voor merken als <strong>Oakley, DJI, Comma Football, Oversized Studios, Gardpro, Hears en Retropia</strong>. UGC werkt goed voor webshops en productmerken, omdat het voelt als een eerlijke aanbeveling.</p>")),
            ("Ook alleen montage", prose(
                "          <p>Heb je zelf al beelden? Dan kan ik ook alleen de montage doen. Voor Boxbollen monteerde ik bijvoorbeeld de content van hun Ecom School, en voor The High Value Club hun podcasts.</p>")),
            ("Per project of elke maand", prose(
                "          <p>Je kunt starten met een pilot van één opnamedag en zes korte video's. Daarna kan het maandelijks, met vaste opnamedagen, een contentplan en elke maand nieuwe video's.</p>")),
        ],
        "faq": [
            ("Wat is het verschil tussen organische content en ads?", "Organische content plaats je op je eigen kanalen om zichtbaar te blijven en vertrouwen op te bouwen. Ads zijn video's waarmee je betaald een specifieke doelgroep bereikt, met een duidelijke actie zoals een aanvraag of aankoop."),
            ("Wat is UGC?", "UGC staat voor user-generated content: video's in de stijl van een gewone gebruiker of creator. Ze voelen als een aanbeveling en werken daardoor vaak goed in advertenties."),
            ("Lever je meerdere versies voor advertenties?", "Ja. Ik maak varianten met verschillende openingen, lengtes en formaten, zodat je kunt testen wat het beste werkt."),
            ("Kun je ook mijn eigen beelden monteren?", "Ja. Ik doe ook alleen montage, bijvoorbeeld van podcasts, cursussen of beelden die je zelf hebt gefilmd."),
        ],
        "final_title": "Content die opvalt in de feed?",
    },
    {
        "slug": "case-the-high-value-club.html",
        "kind": "case",
        "crumb": "Case: The High Value Club",
        "title": "Case The High Value Club | Ads, testimonials en podcasts voor een sportschool | Fabio Media",
        "description": "Hoe Fabio Media voor sportschool The High Value Club paid ads, een trailer, ledentestimonials, podcastreeksen en een eventdag maakte. De samenwerking werd verlengd met een groter pakket.",
        "eyebrow": "Case · sportschool",
        "h1": "The High Value Club: ads, testimonials en podcasts voor een sportschool",
        "lead": "The High Value Club wilde meer leden en een vaste stroom content. Ik maakte advertenties, een trailer, testimonials met leden, podcastreeksen en video's van een eventdag. De club verlengde de samenwerking met een groter tweede pakket.",
        "wa_text": "Hoi Fabio, ik zag de case van The High Value Club en wil graag meer weten.",
        "videos_title": "Een selectie van het werk",
        "videos": ["hvc-trailer", "hvc-testimonial-02", "hvc-culture-insights-01", "hvc-coaches-corner"],
        "sections": [
            ("De vraag", prose(
                "          <p>The High Value Club wilde <strong>meer nieuwe leden</strong> en tegelijk een vaste stroom content om de club online zichtbaar te houden. Eén losse video was niet genoeg: er was een mix nodig van advertenties en content voor de eigen kanalen.</p>")),
            ("Wat ik maakte", cards([
                ("Paid ads", "Advertenties gericht op het werven van nieuwe leden."),
                ("Trailer", "Een video over de club, opgenomen bij de club zelf."),
                ("Ledentestimonials", "Een reeks ondertitelde video's waarin leden vertellen wat de club voor ze betekent."),
                ("Podcasts en een eventdag", "De reeksen Culture Insights en Coaches Corner, en de opnames van een eventdag."),
            ])),
            ("Resultaat", '        <div class="prose"><p>De club was tevreden over de samenwerking en verlengde die met een <strong>groter tweede pakket</strong>, met podcasts, testimonials en een eventdag.</p></div>\n        <p class="result">Verlengd met een groter tweede pakket</p>'),
        ],
        "faq": [],
        "final_title": "Ook zo'n mix van ads en content voor jouw bedrijf?",
    },
    {
        "slug": "case-bij-albrecht.html",
        "kind": "case",
        "crumb": "Case: Bij Albrecht",
        "title": "Case Bij Albrecht | Restaurant video en content | Fabio Media",
        "description": "Hoe Fabio Media voor restaurant Bij Albrecht korte video's maakte van de keuken, het opmaken van de gerechten en de zaak, voor Instagram en TikTok.",
        "eyebrow": "Case · restaurant",
        "h1": "Bij Albrecht: restaurantcontent van keuken tot bord",
        "lead": "Restaurant Bij Albrecht wilde laten zien wat er in de keuken gebeurt en hoe de zaak voelt. Ik maakte korte verticale video's van de keuken, het opmaken van de gerechten en het restaurant.",
        "wa_text": "Hoi Fabio, ik zag de case van Bij Albrecht en wil graag meer weten over content voor mijn zaak.",
        "videos_title": "De video's",
        "videos": ["albrecht-01", "albrecht-02", "albrecht-03"],
        "sections": [
            ("De vraag", prose(
                "          <p>Bij Albrecht wilde de <strong>keuken, de gerechten en de sfeer</strong> van het restaurant laten zien, op een manier die past bij Instagram en TikTok. Mensen moesten na het kijken zin krijgen om er te gaan eten.</p>")),
            ("Wat ik maakte", prose(
                "          <p>Drie korte verticale video's. Ik filmde in de keuken terwijl de gerechten werden opgemaakt, de rijen borden die klaarstaan voor de service, het interieur en het naambord van het restaurant. Door echt mee te kijken in de keuken voelen de video's eerlijk en dichtbij, in plaats van als reclame.</p>\n"
                "          <p>De video's zijn kort, verticaal en klaar om direct te posten.</p>")),
            ("Waarom dit werkt voor een restaurant", prose(
                "          <p>Gasten willen weten waar ze aan toe zijn voordat ze reserveren. Korte video's van het eten en de sfeer beantwoorden die vraag sneller dan een menukaart of een foto. Lees meer over wat ik voor <a href=\"horeca-video.html\">restaurants, hotels en events</a> maak.</p>")),
        ],
        "faq": [],
        "final_title": "Ook zulke video's voor jouw zaak?",
    },
    {
        "slug": "case-qbuzz.html",
        "kind": "case",
        "crumb": "Case: Qbuzz",
        "title": "Case Qbuzz | Medewerkersvideo's over veilig werken | Fabio Media",
        "description": "Hoe Fabio Media voor vervoersbedrijf Qbuzz een reeks van vijf ondertitelde shorts maakte waarin medewerkers zelf vertellen over veilig werken.",
        "eyebrow": "Case · openbaar vervoer",
        "h1": "Qbuzz: medewerkers aan het woord over veilig werken",
        "lead": "Qbuzz wilde dat medewerkers zelf zouden vertellen over veilig werken. Ik maakte een reeks van vijf ondertitelde shorts voor de campagne Veilig werken doen we samen.",
        "wa_text": "Hoi Fabio, ik zag de case van Qbuzz en wil graag meer weten over medewerkersvideo's.",
        "videos_title": "De reeks",
        "videos": ["qbuzz-04", "qbuzz-01", "qbuzz-02", "qbuzz-03"],
        "sections": [
            ("De vraag", prose(
                "          <p>Veiligheid op het werk is belangrijk, maar een boodschap van bovenaf wordt snel overgeslagen. Qbuzz wilde daarom dat <strong>medewerkers het zelf zouden vertellen</strong>, in hun eigen woorden, voor de campagne <strong>Veilig werken doen we samen</strong>.</p>")),
            ("Wat ik maakte", prose(
                "          <p>Een reeks van <strong>vijf korte video's</strong> waarin medewerkers vertellen wat veilig werken voor hen betekent. Elke video is ondertiteld, zodat hij ook zonder geluid werkt, en alle video's zijn opgenomen voor de campagneposter, zodat de reeks direct herkenbaar is.</p>\n"
                "          <p>Door collega's zelf aan het woord te laten, voelt de boodschap herkenbaar en geloofwaardig.</p>")),
            ("Ook voor jouw organisatie", prose(
                "          <p>Medewerkersvideo's werken voor interne campagnes, employer branding en werving. Lees meer over <a href=\"bedrijfsvideo-eindhoven.html\">bedrijfsvideo's laten maken</a>.</p>")),
        ],
        "faq": [],
        "final_title": "Je eigen mensen het verhaal laten vertellen?",
    },
]


def main():
    for page in PAGES:
        (ROOT / page["slug"]).write_text(render(page), encoding="utf-8")
        print("wrote", page["slug"])


if __name__ == "__main__":
    main()
