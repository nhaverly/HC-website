# -*- coding: utf-8 -*-
"""Builds the static Haverly Consulting website into the repository root.

Usage:  python3 _build/build.py
Edit wording in _build/content.py and blog posts in _build/posts/. Then run this
script and commit the changed .html files. No other dependencies are needed.
"""
import html
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from content import (HOME_FOCUS, SITE, SERVICES, PRACTICE, CLIENTS, TESTIMONIALS, TEAM, POSTS,  # noqa: E402
                     SERVICE_PAGES, FRAMEWORKS, CASE_STUDIES, ABOUT_NICK,
                     S151_CHECKED, S151_CALENDAR, S151_BACKSTOPS, S151_BACKSTOP_SOURCE, S151_LIBRARY, S151_TAGS, S151_FIGURES,
                     S151_RESERVES_YEAR, S151_RESERVES_PUBLISHED, S151_RESERVES_TREND)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POST_DIR = os.path.join(os.path.dirname(__file__), "posts")
ASSET_V = "23"  # bump to bust browser caches after CSS/JS changes
e = html.escape


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


class Page:
    """Holds a page's output path and computes relative links from it."""

    def __init__(self, path):
        self.path = path  # e.g. "index.html", "pwlb-premium/discount-calculator.html"
        depth = path.count("/")
        self.base = "../" * depth

    def href(self, slug):
        if slug in ("", "/"):
            return self.base or "./"
        if slug.startswith(("http", "mailto:", "tel:", "#")):
            return slug
        return self.base + slug

    def asset(self, p):
        return f"{self.base}assets/{p}?v={ASSET_V}"

    @property
    def url(self):
        p = self.path
        if p == "index.html":
            return SITE["url"] + "/"
        return SITE["url"] + "/" + p[:-5]


OG_CARDS = []  # share images to render: (filename, eyebrow, title, byline)


def og_image(pg, title, eyebrow, byline):
    name = "home" if pg.path == "index.html" else pg.path[:-5].replace("/", "-")
    OG_CARDS.append((name, eyebrow, title, byline))
    return f"{SITE['url']}/assets/og/{name}.jpg"


def head(pg, title, desc, extra="", og_type="website", noindex=False,
         og_title=None, og_eyebrow="Housing finance advisory", og_byline="", body_class=""):
    full_title = title if title.endswith(SITE["name"]) else f"{title} | {SITE['name']}"
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    card_title = og_title or re.sub(r"\s*\|\s*" + re.escape(SITE["name"]) + r"$", "", full_title)
    img = "" if noindex else og_image(pg, card_title, og_eyebrow, og_byline)
    og_img = (f'<meta property="og:image" content="{img}">\n<meta property="og:image:width" content="1200">\n'
              f'<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{e(card_title)}">\n'
              f'<meta name="twitter:image" content="{img}">\n') if img else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{pg.url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{pg.url}">
<meta property="og:site_name" content="{SITE['name']}">
{og_img}<meta name="twitter:card" content="{'summary_large_image' if img else 'summary'}">
<meta name="theme-color" content="#090F54">
<link rel="icon" href="{pg.base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{pg.asset('css/site.css')}">
{extra}</head>
<body{f' class="{body_class}"' if body_class else ''}>
<a class="skip" href="#main">Skip to content</a>
"""


def header(pg, current=""):
    here = pg.path[:-5]

    def cur(slug, key=None):
        """aria-current for the page itself, or for its section in the main nav."""
        return ' aria-current="page"' if slug == here or (key and key == current) else ""
    svc_links = "".join(
        f'<a{cur(s["slug"])} href="{pg.href(s["slug"])}">{e(s["name"])}</a>' for s in SERVICES)
    mobile_svcs = "".join(
        f'<a{cur(s["slug"])} class="sub" href="{pg.href(s["slug"])}">{e(s["name"])}</a>' for s in SERVICES)
    svc_btn = ' aria-current="page"' if current == "services" else ""
    return f"""<header class="site-head">
  <div class="wrap">
    <a class="brand logo" href="{pg.href('')}" aria-label="Haverly Consulting home"><img src="{pg.base}assets/img/logo-wordmark.svg" alt="Haverly Consulting" width="78" height="44"><span class="brand-label">CONSULTING</span></a>
    <nav class="nav" aria-label="Main">
      <div class="drop">
        <button type="button" aria-expanded="false" aria-haspopup="true"{svc_btn}>Services</button>
        <div class="drop-panel">{svc_links}</div>
      </div>
      <a{cur('case-studies', 'cases')} href="{pg.href('case-studies')}">Case studies</a>
      <a{cur('blog', 'blog')} href="{pg.href('blog')}">Insights</a>
      <a{cur('our-team', 'team')} href="{pg.href('our-team')}">Team</a>
      <a{cur('useful-tools', 'tools')} href="{pg.href('useful-tools')}">Tools</a>
      <a{cur('contact')} class="btn btn-brass" href="{pg.href('contact')}">Book a consultation</a>
    </nav>
    <details class="menu">
      <summary>Menu</summary>
      <div class="menu-panel">
        <p>Services</p>
        {mobile_svcs}
        <p>Company</p>
        <a{cur('case-studies')} href="{pg.href('case-studies')}">Case studies</a>
        <a{cur('blog')} href="{pg.href('blog')}">Insights</a>
        <a{cur('our-team')} href="{pg.href('our-team')}">Team</a>
        <a{cur('testimonials')} href="{pg.href('testimonials')}">Testimonials</a>
        <a{cur('useful-tools')} href="{pg.href('useful-tools')}">Tools</a>
        <a{cur('section-151-officers')} href="{pg.href('section-151-officers')}">Section 151 hub</a>
        <a{cur('contact')} href="{pg.href('contact')}">Contact</a>
      </div>
    </details>
  </div>
</header>
"""

DIRECTORY_PRIVACY = """<h3 id="directory">Our directory of Section 151 officers</h3>
    <p>Our <a href="section-151-officers#s151-directory">Section 151 hub</a> includes a directory of the officers who hold the statutory Section 151 (chief finance officer) role at English councils. For each, we publish only the council, their name and their job title.</p>
    <ul>
      <li><strong>Where the information comes from:</strong> councils' own public documents, such as statements of accounts, council and committee reports, and their websites, and our own professional knowledge of the sector.</li>
      <li><strong>Why we publish it:</strong> to provide a public reference resource for the local government finance sector. Our lawful basis is our legitimate interest in doing so. The information relates only to people's public, statutory roles and is already published by their councils.</li>
      <li><strong>What we do not do:</strong> we do not collect or publish contact details, and we do not use the directory for marketing.</li>
      <li><strong>How long we keep it:</strong> we review the directory regularly and remove or update an entry when someone leaves the role.</li>
      <li><strong>Your rights:</strong> if you are listed, you can ask us to correct your entry, or object to it being shown, by emailing us at the address above. We will act on your request promptly.</li>
    </ul>"""

NO_ANALYTICS_PRIVACY = "<p>We do not use cookies, advertising trackers or analytics on this website. The fonts and code the site needs are served from the site itself.</p>"
ANALYTICS_PRIVACY = ("<p>We use Cloudflare Web Analytics to understand how many people visit the site, which pages they read and how they found us "
    "(for example, from LinkedIn or a search engine). It does not use cookies, does not track you across other websites and does not "
    "identify individual visitors. Cloudflare processes this information on our behalf and may do so outside the UK, under its own terms "
    "and appropriate safeguards. Our lawful basis is our legitimate interest in understanding and improving how the site is used.</p>\n"
    "    <p>We do not use cookies or advertising trackers on this website. Apart from the analytics script, the fonts and code the site needs "
    "are served from the site itself.</p>")


def analytics():
    """Cloudflare Web Analytics beacon (cookieless). Only added once a token is set."""
    tok = SITE.get("cf_analytics_token")
    if not tok:
        return ""
    return ("<!-- Cloudflare Web Analytics --><script type=\"module\" src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
            f"data-cf-beacon='{{\"token\": \"{e(tok)}\"}}'></script><!-- End Cloudflare Web Analytics -->\n")


def hra_widget(pg):
    """Site-wide HRA Assistant pop-up (inline on the assistant page)."""
    if not SITE.get("hra_endpoint"):
        return ""
    root = pg.base or "./"
    return (f'<script src="{pg.asset("js/hra-widget.js")}" data-endpoint="{e(SITE["hra_endpoint"])}" '
            f'data-site-root="{root}" defer></script>\n')


def contact_band(pg, heading="Talk to a housing finance specialist",
                 lede="Whether it is an HRA business plan, a TA cost pressure in your MTFP or a developer viability assessment, a 30-minute conversation is usually enough to tell you where the opportunity is."):
    return f"""<section class="contact" aria-labelledby="cta-h">
  <div class="wrap">
    <div>
      <p class="eyebrow">Free initial consultation</p>
      <h2 id="cta-h">{e(heading)}</h2>
      <p class="lede">{e(lede)}</p>
      <div class="ctas"><a class="btn btn-brass" href="{pg.href('contact')}">Request a call back</a></div>
    </div>
    <dl class="details">
      <dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd>
      <dt>Phone</dt><dd><a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a></dd>
      <dt>Office</dt><dd>{', '.join(SITE['address'])}</dd>
      <dt>Hours</dt><dd>Monday to Friday, 9:00 to 18:00</dd>
    </dl>
  </div>
</section>
"""


def footer(pg, scripts=""):
    svc = "".join(f'<li><a href="{pg.href(s["slug"])}">{e(s["name"])}</a></li>' for s in SERVICES)
    li = f'<li><a href="{SITE["linkedin"]}" rel="noopener">Nick on LinkedIn</a></li>' if SITE["linkedin"] else ""
    return f"""<footer class="site-foot">
  <div class="wrap cols">
    <div>
      <a class="brand logo" href="{pg.href('')}" aria-label="Haverly Consulting home"><img src="{pg.base}assets/img/logo-wordmark.svg" alt="Haverly Consulting" width="78" height="44"><span class="brand-label">CONSULTING</span></a>
      <p>Independent housing finance advisory for UK local authorities and the affordable housing sector.</p>
    </div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Company</h2><ul>
      <li><a href="{pg.href('case-studies')}">Case studies</a></li>
      <li><a href="{pg.href('our-team')}">Our team</a></li>
      <li><a href="{pg.href('testimonials')}">Testimonials</a></li>
      <li><a href="{pg.href('blog')}">Insights</a></li>
      <li><a href="{pg.href('useful-tools')}">Tools</a></li>
      <li><a href="{pg.href('section-151-officers')}">Section 151 hub</a></li>
    </ul></div>
    <div><h2>Contact</h2><ul>
      <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
      <li><a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a></li>
      <li>{'<br>'.join(SITE['address'])}</li>{li}
    </ul></div>
  </div>
  <div class="wrap legal">
    <span>© Haverly Consulting Ltd {date.today().year}. Registered in England and Wales, company number {SITE['company_number']}. Registered office: {', '.join(SITE['address'][:-1])} {SITE['address'][-1]}.</span>
    <span><a href="{pg.href('privacy')}">Privacy notice</a></span>
  </div>
</footer>
<script src="{pg.asset('js/site.js')}" defer></script>
{scripts}{hra_widget(pg)}{analytics()}</body>
</html>
"""


def page_hero(pg, crumbs, h1, lede="", eyebrow="", meta="", crumb=None):
    trail = " / ".join([f'<a href="{pg.href(href)}">{e(t)}</a>' for t, href in crumbs])
    eb = f'<p class="eyebrow" style="margin-top:18px">{e(eyebrow)}</p>' if eyebrow else ""
    ld = f'<p class="lede">{e(lede)}</p>' if lede else ""
    return f"""<section class="page-hero">
  <div class="wrap">
    <p class="crumbs">{trail} / <span>{e(crumb or (h1 if len(h1) < 40 else 'Article'))}</span></p>
    {eb}<h1>{e(h1)}</h1>
    {ld}{meta}
  </div>
</section>
"""


def aside(pg, exclude=None, heading="Book a free 30-minute consultation", buy_via=None):
    rel = "".join(f'<a href="{pg.href(s["slug"])}">{e(s["name"])}</a>'
                  for s in SERVICES if s["slug"] != exclude)
    via = ""
    if buy_via:
        items = "".join(f"<li><b>{e(r)}</b>{e(d)}</li>" for r, d in buy_via)
        via = f"""<div class="via">
    <p class="eyebrow">Available via</p>
    <ul>{items}</ul>
    <a class="link" href="{pg.href('contact')}#frameworks">Buying through a framework</a>
  </div>"""
    return f"""<aside class="aside">
  {via}
  <div class="cta-card">
    <p class="eyebrow">Talk to a specialist</p>
    <h2>{e(heading)}</h2>
    <p>Speak to an experienced housing finance consultant about your authority's position. No obligation.</p>
    <a class="btn btn-brass" href="{pg.href('contact')}">Request a call back</a>
    <p class="small"><a href="mailto:{SITE['email']}">{SITE['email']}</a><br><a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a></p>
  </div>
  <nav class="related" aria-label="Other services">
    <p class="eyebrow">Other services</p>
    {rel}
  </nav>
</aside>
"""


def write(pg, content):
    out = os.path.join(ROOT, pg.path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)


def redirect(path, target_slug):
    pg = Page(path)
    tgt = pg.href(target_slug)
    write(pg, f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<title>Redirecting</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE['url']}/{target_slug.split('#')[0]}">
<meta http-equiv="refresh" content="0; url={tgt}">
</head><body><p>This page has moved. <a href="{tgt}">Continue</a>.</p>
<script>location.replace({json.dumps(tgt)});</script></body></html>
""")


# ------------------------------------------------------------------ components
def services_grid(pg, arrows=False):
    arrow = '\n          <span class="service-arrow" aria-hidden="true">↗</span>' if arrows else ""
    return "".join(f"""<a class="svc" href="{pg.href(s['slug'])}">
          <h3>{e(s['name'])}</h3>
          <p>{e(s['blurb'])}</p>
          <span class="tags">{e(s['tags'])}</span>{arrow}
        </a>""" for s in SERVICES)


def quote_fig(t):
    return f"""<figure class="quote">
          <blockquote>{e(t['quote'])}</blockquote>
          <figcaption><b>{e(t['role'])}</b>{e(t['org'])}</figcaption>
        </figure>"""


def post_cards(pg, posts):
    return "".join(f"""<a class="post" href="{pg.href(p['slug'])}">
          <time datetime="{p['date']}">{fmt_date(p['date'])}</time>
          <h3>{e(p.get('short', p['title']))}</h3>
          <p>{e(p['desc'])}</p>
        </a>""" for p in posts)


HRA_PROMPT_SERVICES = {"advisory-partnership", "financial-reviews"}
HRA_PROMPT_TAGS = {"HRA and rents", "Right to Buy", "Housing companies", "Social housing", "Temporary accommodation"}


def hra_prompt(pg):
    if not SITE.get("hra_endpoint"):
        return ""
    return f"""<aside class="hra-prompt" aria-label="HRA Assistant">
      <span class="glyph">HRA</span>
      <div>
        <p class="hra-prompt-title">Have a quick HRA question?</p>
        <p>Try our free HRA Assistant for answers on rents, the ring-fence, Right to Buy receipts, borrowing and more, drawn from our knowledge base with sources.</p>
        <a class="link" href="{pg.href('hra-assistant')}">Ask the HRA Assistant</a>
      </div>
    </aside>"""


def faq_html(items):
    return '<div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in items) + "</div>"


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>\n'


# ------------------------------------------------------------------ pages
def build_home():
    pg = Page("index.html")
    org = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Haverly Consulting Ltd",
           "url": SITE["url"] + "/", "email": SITE["email"], "telephone": SITE["phone_intl"],
           "description": "Independent housing finance advisory for UK local authorities and the affordable housing sector.",
           "address": {"@type": "PostalAddress", "streetAddress": ", ".join(SITE["address"][:-2]), "addressLocality": SITE["address"][-2],
                       "postalCode": SITE["address"][-1], "addressCountry": "GB"},
           "areaServed": "GB", "founder": {"@type": "Person", "name": "Nick Haverly", "jobTitle": "Director", "sameAs": [SITE["linkedin"]]}}
    clients = "".join(f"<li>{e(c)}</li>" for c in CLIENTS)
    focus = "".join(
        f'<li><a href="{pg.href(slug)}"><span>{i:02d}</span> {e(label)} <b aria-hidden="true">↗</b></a></li>'
        for i, (label, slug) in enumerate(HOME_FOCUS, 1))
    body = f"""{header(pg)}
<main id="main">
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow"><span class="brand-rule"></span> Independent housing finance specialists</p>
        <h1>Financial clarity.<br><em>Better housing.</em></h1>
        <p class="lede">Practical, independent advice for local authorities and the affordable housing sector. We help you structure funding, test viability and make confident financial decisions.</p>
        <div class="ctas">
          <a class="btn btn-civic" href="{pg.href('contact')}">Book a free consultation <span aria-hidden="true">↗</span></a>
          <a class="text-link" href="{pg.href('case-studies')}">Explore our work <span aria-hidden="true">→</span></a>
        </div>
        <p class="hero-caption">Strategic advice. Experienced practitioners. Lasting impact.</p>
      </div>
      <aside class="hero-focus" aria-labelledby="focus-title">
        <div class="focus-top">
          <p class="eyebrow">Our focus</p>
          <svg class="brand-mark" viewBox="0 0 92 96" aria-hidden="true"><path d="M0 0h21v96H0zM71 0h21v96H71z" fill="#FFFFFF"/><path d="M35 0h21v38H35zM35 54h21v42H35z" fill="#1DB6D0"/></svg>
        </div>
        <h2 id="focus-title">Complex challenges.<br>Clear direction.</h2>
        <ul class="focus-list">{focus}</ul>
        <p class="focus-foot">Specialist support, from strategy to delivery.</p>
      </aside>
    </div>
  </section>

  <div class="clients" aria-label="Selected clients">
    <div class="wrap">
      <p class="eyebrow">Selected clients</p>
      <ul>{clients}</ul>
    </div>
  </div>

  <section class="block" id="services">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Services</p>
          <h2>Expertise where it matters.</h2>
        </div>
        <p class="intro">From an annual advisory subscription to a single independent appraisal, every engagement is led by practitioners who have run council finance functions themselves.</p>
      </div>
      <div class="services">{services_grid(pg, arrows=True)}</div>
    </div>
  </section>

  <section class="block" id="results">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Recent transactions</p>
          <h2>Advice that moves housing forward.</h2>
        </div>
        <p class="intro">Two funding structures for Westminster City Council’s temporary accommodation portfolio, drawing on different pools of long-term capital.</p>
      </div>
      <div class="deals">
        <article class="tomb">
          <p class="eyebrow">Institutional funding · Temporary accommodation</p>
          <p class="tomb-client">Westminster City Council</p>
          <p class="tomb-figure">368<small>homes acquired that were previously leased as temporary accommodation</small></p>
          <dl>
            <dt>Term</dt><dd>42 years, index-linked</dd>
            <dt>Retrofit</dt><dd>£33.5m embedded in the structure</dd>
            <dt>Outcome</dt><dd>Volatile nightly costs replaced by structured payments; assets unencumbered at lease expiry</dd>
          </dl>
          <div class="foot"><span>Led by Nick Haverly</span><a class="link" href="{pg.href('section-151-officers-is-your-temporary-accommodation-strategy-financially-sustainable')}">Read the case</a></div>
        </article>
        <article class="tomb">
          <p class="eyebrow">Sale and leaseback · Temporary accommodation</p>
          <p class="tomb-client">City of Westminster Pension Fund</p>
          <p class="tomb-figure">£50m<small>capital released from existing temporary accommodation stock</small></p>
          <dl>
            <dt>Term</dt><dd>40 years, index-linked</dd>
            <dt>Portfolio</dt><dd>124 properties via a council-owned LLP</dd>
            <dt>Outcome</dt><dd>Receipt reinvested in new TA supply; Council retains full use under the leaseback</dd>
          </dl>
          <div class="foot"><span>Led by Nick Haverly</span><a class="link" href="{pg.href('westminster-city-council-pension-fund-50m-sale-and-leaseback-frees-up-capital-for-new-temporary-accommodation')}">Read the case</a></div>
        </article>
      </div>
      <figure class="pull">
        <p>Two different pools of long-term capital, one goal: turning an unmanaged financial risk into planned, asset-backed housing supply.</p>
        <cite><b>Nick Haverly</b>Director</cite>
      </figure>
    </div>
  </section>

  {about_nick_html(pg)}

  <section class="block tools-band" id="tools">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Free tools</p>
          <h2>A practical head start.</h2>
        </div>
      </div>
      {tools_html(pg, open_hra=True)}
    </div>
  </section>

  <section class="block alt" id="testimonials">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Client feedback</p>
          <h2>Trusted by the teams we work with.</h2>
        </div>
        <p class="intro"><a class="link" href="{pg.href('testimonials')}">All testimonials</a></p>
      </div>
      <div class="quotes featured-quote">{quote_fig(TESTIMONIALS[0])}</div>
    </div>
  </section>

  <section class="block" id="insights">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Insights</p>
          <h2>Perspectives on housing finance.</h2>
        </div>
        <p class="intro"><a class="link" href="{pg.href('blog')}">All articles</a></p>
      </div>
      <div class="posts">{post_cards(pg, POSTS[:3])}</div>
    </div>
  </section>

  {frameworks_html(pg)}

  {contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Housing Finance Consultancy for Local Authorities | Haverly Consulting",
                   "Specialist housing finance consultants supporting UK local authorities with HRA, temporary accommodation, financial appraisals, business partnering and advisory services.",
                   extra=ld(org), og_title="Financial clarity. Better housing.",
                   og_eyebrow="Independent housing finance specialists",
                   og_byline="Practical, independent advice for local authorities and the affordable housing sector",
                   body_class="home") + body + footer(pg))


def frameworks_html(pg):
    items = "".join(f'<li><b>{e(f["name"])}</b><span>via {e(f["via"])}</span></li>' for f in FRAMEWORKS)
    return f"""<section class="buy" aria-labelledby="buy-h">
    <div class="wrap">
      <div>
        <p class="eyebrow">How to buy</p>
        <h2 id="buy-h">Commission us without a full tender</h2>
        <p>We are an approved supplier on three public sector procurement routes. <a class="link" href="{pg.href('contact')}#frameworks">How it works</a></p>
        <p style="margin-top:10px"><a class="link" href="{pg.base}assets/docs/haverly-consulting-capability-statement.pdf">Download our capability statement (PDF)</a></p>
      </div>
      <ul>{items}</ul>
    </div>
  </section>"""


def tools_html(pg, open_hra=False):
    hra = ""
    if SITE.get("hra_endpoint"):
        trigger = " data-open-hra" if open_hra else ""
        hra = f"""<a class="tool"{trigger} href="{pg.href('hra-assistant')}">
          <span class="glyph">HRA</span>
          <div><h3>HRA Assistant</h3><p>Ask questions about the Housing Revenue Account in England and get answers drawn from our HRA knowledge base, with sources.</p></div>
        </a>
        """
    return f"""<div class="tools">
        {hra}<a class="tool" href="{pg.href('pwlb-premium/discount-calculator')}">
          <span class="glyph">PWLB</span>
          <div><h3>Early Repayment Calculator</h3><p>Calculate the premium or discount on early repayment of PWLB debt, whether EIP, annuity or maturity.</p></div>
        </a>
        <a class="tool" href="{pg.href('pwlb-v-il')}">
          <span class="glyph">NPV</span>
          <div><h3>PWLB vs Index-Linked Comparison</h3><p>Compare the net present value of PWLB annuity, EIP and maturity borrowing with index-linked private placement, using live reference rates.</p></div>
        </a>
      </div>"""


def build_services():
    for s in SERVICES:
        slug = s["slug"]
        d = SERVICE_PAGES[slug]
        pg = Page(f"{slug}.html")
        crumbs = [("Home", ""), ("Services", "#services")]
        crumbs = [("Home", ""), ("Services", "#services")]
        hero = page_hero(pg, [("Home", ""), ("Services", "")], d["h1"], d["lede"], eyebrow="Services")
        # the "Services" crumb should land on the home page services grid
        hero = hero.replace(f'href="{pg.href("")}">Services', f'href="{pg.href("")}#services">Services')
        body = f"""{header(pg, 'services')}
<main id="main">
{hero}
<div class="wrap layout">
  <article class="prose">
    {d['body']}
    {hra_prompt(pg) if slug in HRA_PROMPT_SERVICES else ''}
    <h2>Frequently asked questions</h2>
    {faq_html(d['faq'])}
  </article>
  {aside(pg, exclude=slug, buy_via=d.get('buy_via'))}
</div>
{contact_band(pg)}
</main>
"""
        write(pg, head(pg, d["title"], d["desc"], extra=ld(faq_schema(d["faq"])),
                       og_title=d["h1"], og_eyebrow="Services", og_byline=d["lede"]) + body + footer(pg))


def build_testimonials():
    pg = Page("testimonials.html")
    body = f"""{header(pg)}
<main id="main">
{page_hero(pg, [("Home", "")], "Testimonials", "What councils and partners say about working with us.", eyebrow="Client feedback")}
<section class="block">
  <div class="wrap">
    <div class="quotes two">{''.join(quote_fig(t) for t in TESTIMONIALS)}</div>
  </div>
</section>
<div class="clients" aria-label="Selected clients">
  <div class="wrap">
    <p class="eyebrow">Selected clients</p>
    <ul>{''.join(f'<li>{e(c)}</li>' for c in CLIENTS)}</ul>
  </div>
</div>
{contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Client Testimonials",
                   "What UK local authorities say about working with Haverly Consulting. Trusted by councils including Westminster, Ealing, Guildford and the Isle of Wight.") + body + footer(pg))


def build_team():
    pg = Page("our-team.html")
    people = ""
    for p in TEAM:
        bio = "".join(f"<p>{e(x)}</p>" for x in p["bio"])
        people += f"""<article class="person" id="{p['id']}">
        <div class="portrait" aria-hidden="true"><img src="{pg.base}assets/img/team/{p['id']}.jpg" alt="" loading="lazy" onerror="this.remove()"></div>
        <div>
          <h2>{e(p['name'])}</h2>
          <p class="role">{e(p['role'])}</p>
          <div class="bio">{bio}</div>
        </div>
      </article>"""
    body = f"""{header(pg, 'team')}
<main id="main">
{page_hero(pg, [("Home", "")], "Our team", "Housing finance specialists with over 70 years of combined public sector experience. We care deeply about public services and work to protect front line services and maximise value for money.", eyebrow="People")}
<section class="block">
  <div class="wrap">
    <div class="team">{people}</div>
  </div>
</section>
{contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Our Team | Housing Finance Experts",
                   "Meet the Haverly Consulting team: housing finance specialists with over 70 years of combined public sector experience across UK local authorities.") + body + footer(pg))
    for p in TEAM:
        redirect(f"{p['id']}.html", f"our-team#{p['id']}")


def build_contact():
    pg = Page("contact.html")
    action = f"https://formspree.io/f/{SITE['formspree_id']}"
    body = f"""{header(pg)}
<main id="main">
{page_hero(pg, [("Home", "")], "Contact us", "Leave your details and one of our housing finance specialists will call you back to arrange a free 30-minute consultation.", eyebrow="Free initial consultation")}
<div class="wrap contact-grid">
  <div>
    <h2 style="font-size:1.6rem;font-weight:750;margin-bottom:24px">Request a call back</h2>
    <form class="form" id="contact-form" action="{action}" method="POST">
      <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="phone">Phone number</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
      <input type="hidden" name="_subject" value="Website enquiry: call back request">
      <label class="hp" aria-hidden="true">Leave blank<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
      <p class="hint" style="font-size:.86rem;color:var(--muted)">We'll only use your details to respond to your enquiry. See our <a href="{pg.href('privacy')}" style="color:var(--civic)">privacy notice</a>.</p>
      <div><button class="btn btn-civic" type="submit">Request a call back</button></div>
      <p class="form-status" id="form-status" role="status" hidden></p>
    </form>
  </div>
  <div>
    <h2 style="font-size:1.6rem;font-weight:750;margin-bottom:24px">Contact details</h2>
    <dl class="info-list">
      <dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd>
      <dt>Phone</dt><dd><a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a></dd>
      <dt>Office</dt><dd>Haverly Consulting Ltd<br>{'<br>'.join(SITE['address'])}</dd>
      <dt>Hours</dt><dd>Monday to Friday, 9:00 to 18:00<br>Closed weekends</dd>
    </dl>
    <h2 id="frameworks" style="font-size:1.6rem;font-weight:750;margin:48px 0 12px;scroll-margin-top:100px">Buying through a framework</h2>
    <p style="color:var(--muted);margin-bottom:20px">Public sector buyers can commission us through any of these routes, by direct award or mini-competition depending on the framework rules, without running a full tender of their own.</p>
    <dl class="info-list">{''.join(f"<dt>{e(f['name'])}</dt><dd>{e(f['detail'])} <a href=\"{f['url']}\" rel=\"noopener\" target=\"_blank\">Framework details</a></dd>" for f in FRAMEWORKS)}</dl>
    <p style="margin-top:20px"><a class="btn btn-outline" href="{pg.base}assets/docs/haverly-consulting-capability-statement.pdf">Download capability statement (PDF)</a></p>
  </div>
</div>
</main>
"""
    write(pg, head(pg, "Contact Haverly Consulting | Free Initial Consultation",
                   "Get in touch with Haverly Consulting to arrange a free consultation with one of our housing finance specialists. We work with local authorities across the UK.") + body + footer(pg))
    redirect("contact-us.html", "contact")


def read_time(text):
    words = len(re.sub(r"<[^>]+>", " ", text).split())
    return max(1, round(words / 220))


def tidy_post(raw):
    # standalone bold paragraphs become section headings
    raw = re.sub(r"<p><strong>([^<]{3,90})</strong></p>", r"<h2>\1</h2>", raw)
    # an opening h3 becomes the stand-first
    raw = re.sub(r"^\s*<h3>(.*?)</h3>", r'<p class="intro-line">\1</p>', raw, count=1, flags=re.S)
    # absolute links to the old site become relative
    raw = raw.replace('href="/contact"', 'href="contact"')
    return raw


def build_posts():
    for i, p in enumerate(POSTS):
        pg = Page(f"{p['slug']}.html")
        with open(os.path.join(POST_DIR, p["slug"] + ".html"), encoding="utf-8") as f:
            raw = tidy_post(f.read())
        raw = raw.replace('href="contact"', f'href="{pg.href("contact")}"')
        mins = read_time(raw)
        meta = f'<p class="post-meta"><span>By Nick Haverly</span><span><time datetime="{p["date"]}">{fmt_date(p["date"])}</time></span><span>{mins} min read</span></p>'
        newer = POSTS[i - 1] if i > 0 else None
        older = POSTS[i + 1] if i + 1 < len(POSTS) else None
        nav = '<nav class="post-nav" aria-label="More articles">'
        nav += f'<a href="{pg.href(older["slug"])}"><span>Previous article</span><b>{e(older["title"])}</b></a>' if older else "<span></span>"
        nav += f'<a href="{pg.href(newer["slug"])}"><span>Next article</span><b>{e(newer["title"])}</b></a>' if newer else "<span></span>"
        nav += "</nav>"
        schema = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
                  "datePublished": p["date"], "description": p["desc"],
                  "author": {"@type": "Person", "name": "Nick Haverly"},
                  "publisher": {"@type": "Organization", "name": "Haverly Consulting Ltd"},
                  "mainEntityOfPage": pg.url}
        body = f"""{header(pg, 'blog')}
<main id="main">
{page_hero(pg, [("Home", ""), ("Insights", "blog")], p['title'], eyebrow=p['tag'], meta=meta)}
<div class="wrap layout">
  <article class="prose">
    {f'<div class="update-note"><p><strong>Update, October 2026.</strong> {e(p["update"])}</p></div>' if p.get('update') else ''}
    {raw}
    {hra_prompt(pg) if p['tag'] in HRA_PROMPT_TAGS else ''}
    {nav}
  </article>
  {aside(pg, heading="Discuss this with Nick")}
</div>
</main>
"""
        write(pg, head(pg, p["title"], p["desc"], extra=ld(schema), og_type="article",
                       og_eyebrow=p["tag"], og_byline=f"Nick Haverly FCPFA  ·  {fmt_date(p['date'])}") + body + footer(pg))


def build_blog():
    pg = Page("blog.html")
    items = "".join(f"""<li><a href="{pg.href(p['slug'])}">
        <time datetime="{p['date']}">{fmt_date(p['date'])}</time>
        <div><p class="eyebrow" style="color:var(--civic);margin-bottom:6px">{e(p['tag'])}</p><h2>{e(p['title'])}</h2><p>{e(p['desc'])}</p></div>
      </a></li>""" for p in POSTS)
    body = f"""{header(pg, 'blog')}
<main id="main">
{page_hero(pg, [("Home", "")], "Insights", "Commentary on housing finance, the HRA, temporary accommodation, local authority housing companies and public sector financial management.", eyebrow="Blog")}
<section class="block" style="padding-top:56px">
  <div class="wrap">
    <ul class="archive">{items}</ul>
  </div>
</section>
{contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Housing Finance Insights and News",
                   "Expert commentary on housing finance, HRA, local authority housing companies, MRP, temporary accommodation and public sector financial management from Haverly Consulting.") + body + footer(pg))


def build_tools():
    pg = Page("useful-tools.html")
    body = f"""{header(pg, 'tools')}
<main id="main">
{page_hero(pg, [("Home", "")], "Useful tools", "Free calculators for local authority treasury and finance teams.", eyebrow="Tools")}
<section class="block">
  <div class="wrap">{tools_html(pg)}
    <p style="margin-top:32px">Looking for legislation, codes and key dates? See our <a class="link" href="{pg.href('section-151-officers')}">resources for Section 151 officers</a>.</p>
  </div>
</section>
{contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Useful Tools for Local Authority Finance Teams",
                   "Free PWLB calculators for local authorities: early repayment premium and discount, and an NPV comparison of PWLB and index-linked borrowing.", og_eyebrow="Free tool") + body + footer(pg))


def engagements_html(pg):
    cards = "".join(f"""<a class="eng" href="{pg.href('case-studies')}#{c['id']}">
          <p class="eyebrow">{e(c['client'])}</p>
          <h3>{e(c['headline'])}</h3>
          <p>{e(c['summary'])}</p>
          <span class="link">Read the case study</span>
        </a>""" for c in CASE_STUDIES if c.get("home"))
    return f"""<section class="block alt" id="engagements">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Selected engagements</p>
          <h2>Regeneration, appraisal and viability work for councils</h2>
        </div>
        <p class="intro"><a class="link" href="{pg.href('case-studies')}">All case studies</a></p>
      </div>
      <div class="engs">{cards}</div>
    </div>
  </section>"""


def about_nick_html(pg):
    nick = next(t for t in TEAM if t["id"] == "nick")
    return f"""<section class="block about" id="about">
    <div class="wrap about-grid">
      <div class="about-photo"><div class="portrait big"><img src="{pg.base}assets/img/team/nick.jpg" alt="Nick Haverly, Director" loading="lazy" onerror="this.remove()"></div></div>
      <div>
        <p class="eyebrow">Who you work with</p>
        <h2>{e(nick['name'])}</h2>
        <p class="role">{e(nick['role'])}</p>
        <p class="about-lede">{e(ABOUT_NICK['lede'])}</p>
        <div class="ctas" style="margin-top:24px">
          <a class="btn btn-civic" href="{pg.href('contact')}">Book a call with Nick</a>
          <a class="btn btn-outline" href="{pg.href('our-team')}">Meet the team</a>
          <a class="btn btn-outline" href="{SITE['linkedin']}" rel="noopener">Follow on LinkedIn</a>
        </div>
      </div>
    </div>
  </section>"""


def build_case_studies():
    pg = Page("case-studies.html")
    items = ""
    for c in CASE_STUDIES:
        facts = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in c["facts"])
        fig = (f'<p class="tomb-figure">{e(c["figure"])}<small>{e(c["figure_label"])}</small></p>'
               if c.get("figure") else f'<p class="tomb-figure txt">{e(c["headline"])}</p>')
        body = "".join(f"<p>{e(x)}</p>" for x in c["body"])
        did = "".join(f"<li>{e(x)}</li>" for x in c["did"])
        quote = ""
        if c.get("testimonial") is not None:
            t = TESTIMONIALS[c["testimonial"]]
            quote = f'<figure class="quote"><blockquote>{e(t["quote"])}</blockquote><figcaption><b>{e(t["role"])}</b>{e(t["org"])}</figcaption></figure>'
        more = f'<p><a class="link" href="{pg.href(c["article"])}">Read the full article</a></p>' if c.get("article") else ""
        items += f"""<article class="case" id="{c['id']}">
      <div class="tomb">
        <p class="eyebrow">{e(c['client'])}</p>
        <p class="tomb-client">{e(c['title'])}</p>
        {fig}
        <dl>{facts}</dl>
      </div>
      <div class="case-body prose">
        <p class="intro-line">{e(c['summary'])}</p>
        {body}
        <h3>What we did</h3>
        <ul>{did}</ul>
        {quote}
        {more}
      </div>
    </article>"""
    body = f"""{header(pg, 'cases')}
<main id="main">
{page_hero(pg, [("Home", "")], "Case studies", "Funding structures, regeneration programmes and viability work for local authorities.", eyebrow="Our work")}
<section class="block">
  <div class="wrap cases">{items}</div>
</section>
{contact_band(pg, "Facing a similar challenge?", "Whether it is a regeneration programme, a temporary accommodation pressure or a site that won't stack up, a 30-minute conversation is usually enough to tell you where the opportunity is.")}
</main>
"""
    write(pg, head(pg, "Case Studies", "Case studies from Haverly Consulting: Westminster temporary accommodation funding, Guildford's £467m Weyside Urban Village, Waverley development appraisals and a One Public Estate commission for a Gosport housing site.",
                   og_eyebrow="Case studies", og_title="Funding, regeneration and viability for councils",
                   og_byline="Westminster · Guildford · Waverley · Gosport") + body + footer(pg))


PRIVACY_UPDATED = "2026-10-27"


def build_privacy():
    pg = Page("privacy.html")
    addr = ", ".join(SITE["address"])
    body = f"""{header(pg)}
<main id="main">
{page_hero(pg, [("Home", "")], "Privacy notice", "How Haverly Consulting collects and uses personal information through this website.", eyebrow="Legal")}
<div class="wrap layout">
  <article class="prose">
    <p><em>Last updated {fmt_date(PRIVACY_UPDATED)}</em></p>

    <h2>Who we are</h2>
    <p>This website is run by Haverly Consulting Ltd, a company registered in England and Wales (company number {SITE['company_number']}), with its registered office at {addr}. We are the data controller for personal information collected through this website.</p>
    <p>If you have any questions about this notice or how we use your information, email <a href="mailto:{SITE['email']}">{SITE['email']}</a> or write to us at the address above.</p>

    <h2>Information we collect</h2>
    <h3>When you contact us</h3>
    <p>If you use our contact form, we collect your name, email address and phone number. If you email or call us, we collect whatever details you choose to share.</p>
    <p>We use this information only to respond to your enquiry and, if we go on to work together, to manage that relationship. Our lawful basis is our legitimate interest in responding to people who contact us, or taking steps at your request before entering into a contract.</p>
    <p>The contact form is processed by <a href="https://formspree.io">Formspree</a>, a form-handling service that forwards your details to us by email. Formspree may process this information outside the UK, under its own privacy terms and appropriate safeguards.</p>

    <h3 id="hra-assistant">When you use the HRA Assistant</h3>
    <p>Questions you type into the HRA Assistant are sent, together with the rest of that conversation, to Anthropic, the company that provides the Claude AI model, so that it can generate an answer. The service runs on Cloudflare, which passes your question to Anthropic and returns the answer.</p>
    <ul>
      <li>We do not keep a record of the questions you ask or the answers you receive.</li>
      <li>Anthropic states that it automatically deletes inputs and outputs from its systems within 30 days, other than in limited circumstances such as enforcing its usage policies or meeting legal requirements.</li>
      <li>To prevent misuse, we count the number of questions asked from each network (IP) address per day. These counts are stored by Cloudflare and deleted automatically after two days.</li>
      <li>Your browser remembers how many free questions you have used today. This is stored only on your own device and is not sent to us.</li>
    </ul>
    <p>Please don't include personal information, or confidential information about your organisation, in your questions. Our lawful basis for operating the assistant is our legitimate interest in providing a useful public information tool. Anthropic and Cloudflare may process this information outside the UK, under their own terms and appropriate safeguards.</p>

    {DIRECTORY_PRIVACY if os.path.exists(os.path.join(ROOT, "assets", "data", "s151-directory.json")) else ""}
    <h3>When you browse the site</h3>
    <p>This website is hosted by GitHub Pages. Like most web hosts, GitHub may record visitors' IP addresses in its server logs for security and operational purposes. The PWLB comparison tool loads daily reference rates from GitHub, which may also see your IP address.</p>
    {ANALYTICS_PRIVACY if SITE.get("cf_analytics_token") else NO_ANALYTICS_PRIVACY}

    <h2>How long we keep your information</h2>
    <p>We keep enquiry details for as long as we need them to respond and follow up. If we go on to work together, we keep relevant records for the duration of that relationship and for up to six years afterwards, to meet legal and accounting requirements. If we don't work together, we delete enquiry details within two years.</p>

    <h2>Sharing your information</h2>
    <p>We do not sell your information or share it for marketing. We share it only with the service providers named in this notice, who process it on our behalf, or where the law requires us to.</p>

    <h2>Your rights</h2>
    <p>Under UK data protection law you have the right to:</p>
    <ul>
      <li>ask for a copy of the personal information we hold about you</li>
      <li>ask us to correct information that is wrong or incomplete</li>
      <li>ask us to delete your information</li>
      <li>object to, or ask us to restrict, how we use your information</li>
    </ul>
    <p>To use any of these rights, email <a href="mailto:{SITE['email']}">{SITE['email']}</a>. We will respond within one month.</p>
    <p>If you are unhappy with how we have handled your information, you can complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a>. We would welcome the chance to put things right first, so please contact us before going to the ICO.</p>

    <h2>Changes to this notice</h2>
    <p>We may update this notice from time to time. The date at the top shows when it was last changed.</p>
  </article>
  <aside class="aside">
    <div class="via">
      <p class="eyebrow">Data controller</p>
      <ul>
        <li><b>Haverly Consulting Ltd</b>Company number {SITE['company_number']}</li>
        <li><b>Registered office</b>{addr}</li>
        <li><b>Contact</b><a href="mailto:{SITE['email']}" style="color:var(--civic)">{SITE['email']}</a></li>
      </ul>
    </div>
  </aside>
</div>
</main>
"""
    write(pg, head(pg, "Privacy Notice", "How Haverly Consulting collects and uses personal information through its website, contact form and HRA Assistant.",
                   og_eyebrow="Legal") + body + footer(pg))


def build_hra_assistant():
    pg = Page("hra-assistant.html")
    body = f"""{header(pg, 'tools')}
<main id="main">
{page_hero(pg, [("Home", ""), ("Tools", "useful-tools")], "A clearer starting point for your HRA questions.", "Ask a question about the Housing Revenue Account and get a clear answer drawn from our HRA knowledge base, with sources.", eyebrow="Tools", crumb="HRA Assistant")}
<div class="wrap layout">
  <div data-hra-inline></div>
  <aside class="aside">
    <div class="via">
      <p class="eyebrow">What it covers</p>
      <ul>
        <li><b>Rents and income</b>Rent setting, service charges and the Rent Standard</li>
        <li><b>The ring-fence</b>What can and can't be charged to the HRA</li>
        <li><b>Capital and borrowing</b>Right to Buy receipts, the HRA CFR, PWLB and MRP</li>
        <li><b>Property and regulation</b>Appropriations, disposals, Awaab's Law and consumer standards</li>
      </ul>
    </div>
    <div class="cta-card">
      <p class="eyebrow">Advisory Partnership</p>
      <h2>Need advice on your council's position?</h2>
      <p>Get unlimited access to our housing finance specialists through one annual subscription, with no per-query charges.</p>
      <a class="btn btn-brass" href="{pg.href('advisory-partnership')}">Find out more</a>
    </div>
  </aside>
</div>
</main>
"""
    write(pg, head(pg, "HRA Assistant | Housing Revenue Account Questions Answered",
                   "Free AI assistant answering questions about the Housing Revenue Account in England, drawing on Haverly Consulting's HRA knowledge base with sources cited.",
                   noindex=not SITE.get("hra_endpoint"), og_eyebrow="Free tool")
          + body + footer(pg))


def build_pwlb_repayment():
    pg = Page("pwlb-premium/discount-calculator.html")
    body = f"""{header(pg, 'tools')}
<main id="main">
{page_hero(pg, [("Home", ""), ("Tools", "useful-tools")], "PWLB early repayment calculator", "Estimate the premium payable or discount receivable on early repayment of PWLB debt, for EIP, annuity or maturity loans.", eyebrow="Tools")}
<div class="wrap calc">
  <form class="panel" id="calcForm" novalidate>
    <fieldset>
      <legend>Loan details</legend>
      <div class="field"><label for="loanType">Loan type</label>
        <select id="loanType"><option value="EIP" selected>EIP (Equal Instalment of Principal)</option><option value="Maturity">Maturity</option><option value="Annuity">Annuity</option></select></div>
      <div class="grid-2">
        <div class="field"><label for="loanRepaidDate">Loan to be repaid on</label><input id="loanRepaidDate" type="date" value="2015-10-02"></div>
        <div class="field"><label for="finalPaymentDate">Date of final payment</label><input id="finalPaymentDate" type="date" value="2045-09-10"></div>
      </div>
      <div class="grid-2">
        <div class="field"><label for="prevInterestDate">Previous interest payment</label><input id="prevInterestDate" type="date" value="2015-09-10"></div>
        <div class="field"><label for="amount">Amount to be repaid (£)</label><input id="amount" type="number" inputmode="decimal" min="0" step="0.01" value="5000000"></div>
      </div>
    </fieldset>
    <fieldset>
      <legend>Rates</legend>
      <div class="grid-2">
        <div class="field"><label for="discountRate">Discount rate (%)</label><input id="discountRate" type="number" inputmode="decimal" step="0.01" value="2.12"></div>
        <div class="field"><label for="loanRate">Loan rate (%)</label><input id="loanRate" type="number" inputmode="decimal" step="0.01" value="3.27"></div>
      </div>
    </fieldset>
    <button class="btn btn-civic" type="submit">Calculate premium / discount</button>
    <p class="err-msg" id="errorMsg" role="alert" hidden></p>
  </form>
  <div class="panel" aria-live="polite">
    <div class="result-hero">
      <p class="eyebrow" id="resultLabel">Premium payable</p>
      <p class="value" id="resultValue">£0.00</p>
    </div>
    <h3>All methods</h3>
    <dl class="kv">
      <div id="rowMaturity" style="display:contents"><dt>Maturity</dt><dd id="valMaturity"></dd></div>
      <div id="rowEIP" style="display:contents"><dt>EIP</dt><dd id="valEIP"></dd></div>
      <div id="rowAnnuity" style="display:contents"><dt>Annuity</dt><dd id="valAnnuity"></dd></div>
    </dl>
    <h3>Workings</h3>
    <dl class="kv">
      <dt>Semi-annual discount rate (id)</dt><dd id="bId"></dd>
      <dt>Semi-annual loan rate (il)</dt><dd id="bIl"></dd>
      <dt>Days since previous interest payment (D)</dt><dd id="bD"></dd>
      <dt>Semi-annual periods remaining (N)</dt><dd id="bN"></dd>
      <dt>Annuity factor at discount rate (A1)</dt><dd id="bA1"></dd>
      <dt>Present value factor (PV1)</dt><dd id="bPV1"></dd>
      <dt>Annuity factor at loan rate (A2)</dt><dd id="bA2"></dd>
    </dl>
    <p class="note">For guidance only. Always verify against official PWLB documentation before making a repayment decision.</p>
  </div>
</div>
{contact_band(pg, "Reviewing your debt portfolio?", "A debt and MRP review often finds savings that more than cover its cost. We can model restructuring options and early repayment scenarios for your authority.")}
</main>
"""
    write(pg, head(pg, "PWLB Early Repayment Premium and Discount Calculator",
                   "Free calculator for the premium or discount on early repayment of PWLB loans, covering EIP, annuity and maturity loans, with full workings.", og_eyebrow="Free tool")
          + body + footer(pg, f'<script src="{pg.asset("js/pwlb-repayment.js")}" defer></script>\n'))


def build_pwlb_vs_il():
    pg = Page("pwlb-v-il.html")
    body = f"""{header(pg, 'tools')}
<main id="main">
{page_hero(pg, [("Home", ""), ("Tools", "useful-tools")], "PWLB vs index-linked borrowing", "Compare annuity, EIP, maturity and index-linked financing on a net present value basis, using daily-updated DMO and Bank of England reference rates.", eyebrow="Tools")}
<div class="wrap calc">
  <form class="panel" id="calcForm" novalidate>
    <fieldset>
      <legend>Loan details</legend>
      <div class="grid-2">
        <div class="field"><label for="principal">Loan principal (£)</label><input id="principal" type="number" inputmode="decimal" min="0" step="1000" value="50000000"></div>
        <div class="field"><label for="term">Loan term (years)</label><input id="term" type="number" inputmode="numeric" min="1" max="50" step="1" value="40"></div>
      </div>
    </fieldset>
    <fieldset>
      <legend>PWLB reference rate</legend>
      <div class="field"><label for="pwlbRateDisplay">Certainty Rate for this term</label><input id="pwlbRateDisplay" type="text" readonly value="Loading reference rates…">
        <span class="hint">Each repayment type has its own published DMO curve. Shown net of the 20bps Certainty Rate discount.</span></div>
    </fieldset>
    <fieldset>
      <legend>Index-linked private placement</legend>
      <div class="field"><label for="giltRateDisplay">Index-linked gilt real yield for this term</label><input id="giltRateDisplay" type="text" readonly value="…"></div>
      <div class="grid-2">
        <div class="field"><label for="margin">Margin over gilt yield (bps)</label><input id="margin" type="number" inputmode="numeric" step="1" value="100"></div>
        <div class="field"><label for="rpi">Long-term RPI assumption (%)</label><input id="rpi" type="number" inputmode="decimal" step="0.1" value="3.0"></div>
      </div>
    </fieldset>
    <fieldset>
      <legend>NPV assumptions</legend>
      <div class="field"><label for="discRate">Discount rate for NPV comparison (%)</label><input id="discRate" type="number" inputmode="decimal" step="0.01">
        <span class="hint">Defaults to the PWLB annuity rate above. Override it to test a different discount rate.</span></div>
    </fieldset>
    <button class="btn btn-civic" type="submit">Calculate comparison</button>
  </form>
  <div class="panel" aria-live="polite">
    <h2>NPV cost of borrowing</h2>
    <div class="npv-grid" id="resultGrid" style="margin-top:20px"><p class="note">Loading reference rates…</p></div>
    <div class="callout" id="ctaCallout" hidden>
      <p class="headline">This scenario shows a potential <b id="ctaSaving"></b> NPV saving over your cheapest PWLB option.</p>
      <p>Index-linked financing won't suit every capital programme, but when the numbers line up like this it's worth a conversation. We can help you work through whether it's right for your authority.</p>
      <div><a class="btn btn-brass" id="ctaLink" href="mailto:{SITE['email']}">Email Haverly Consulting</a></div>
    </div>
    <h3>Annual payments</h3>
    <div class="chart-box" id="chartBox"><canvas id="paymentChart" aria-label="Annual payment profile for each borrowing option" role="img"></canvas></div>
  </div>
</div>
<section class="wrap" style="padding-bottom:64px">
  <div class="panel">
    <h2>Reference rates</h2>
    <p class="note" style="margin-top:8px">As at <span id="ratesAsOf">…</span>. <span id="ratesSource"></span> PWLB rates are shown net of the 20bps Certainty Rate discount, interpolated where needed.</p>
    <div class="table-wrap"><table class="rates" id="ratesTable"></table></div>
    <p class="note">This tool provides an illustrative, high-level comparison only and does not constitute financial, accounting, legal or investment advice. Minimum Revenue Provision (asset life, annuity method) and IFRS 9 amortised cost workings are not shown in this summary view; contact Haverly Consulting for the full detailed model. Rates should be checked against live DMO and market data before use in any financing decision.</p>
  </div>
</section>
{contact_band(pg, "Exploring index-linked finance?", "We led a 42-year institutional funding structure and a 40-year pension fund sale-and-leaseback for Westminster City Council. We can model the options for your capital programme.")}
</main>
"""
    scripts = (f'<script src="{pg.base}assets/js/vendor/chart-4.5.0.umd.min.js" defer></script>\n'
               f'<script src="{pg.asset("js/pwlb-vs-il.js")}" defer></script>\n')
    write(pg, head(pg, "PWLB vs Index-Linked Borrowing Cost Comparison",
                   "Free tool comparing the NPV cost of PWLB annuity, EIP and maturity loans with index-linked private placement, using daily-updated DMO and Bank of England rates.", og_eyebrow="Free tool")
          + body + footer(pg, scripts))


def s151_data_version():
    """Short hash of the hub's data files, appended to their URLs so browsers fetch new data when it changes."""
    import hashlib
    h = hashlib.md5()
    for n in ("s151-reserves.json", "s151-audit.json"):
        with open(os.path.join(ROOT, "assets", "data", n), "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:10]


def s151_directory_html(pg):
    """Directory of S151 officers, from assets/data/s151-directory.json (built from councils' own sources)."""
    path = os.path.join(ROOT, "assets", "data", "s151-directory.json")
    mail = f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'
    if not os.path.exists(path):
        intro = ("<p>We are compiling a directory of Section 151 officers across English councils, showing each officer's name "
                 "and role as published by their own council, with a link to that source. It will be published here shortly.</p>")
        return "", intro
    with open(path, encoding="utf-8") as f:
        D = json.load(f)
    n = sum(1 for x in D["entries"] if x.get("name"))
    intro = (f'<p>Our <a href="#s151-directory">directory</a> lists the Section 151 officer at {n} English councils, '
             "drawn from councils' own published documents.</p>")
    html = f"""<section class="block" id="s151-directory" style="padding-bottom:0">
  <div class="wrap" id="dir" data-base="{pg.base}" data-v="{s151_data_version()}">
    <div class="sec-head">
      <div><p class="eyebrow">Directory</p><h2>Section 151 officers in England.</h2></div>
      <p class="intro">The Section 151 officer at each English council, with their job title, drawn from councils' own published documents, such as their 2025/26 statements of accounts.</p>
    </div>
    <div class="dir-tools">
      <div><label for="dirSearch">Search</label><input id="dirSearch" type="search" placeholder="Council or name" autocomplete="off"></div>
      <div><label for="dirType">Type of council</label><select id="dirType"><option value="">All councils</option></select></div>
      <p class="dir-count" id="dirCount" aria-live="polite"></p>
    </div>
    <div class="table-wrap"><table class="rates dir-t"><thead><tr><th scope="col">Council</th><th scope="col">Section 151 officer</th></tr></thead><tbody id="dirBody"><tr><td colspan="2">Loading…</td></tr></tbody></table></div>
    <p class="note">Names and job titles only; we do not publish contact details. Last checked {e(D.get("checked", ""))}. If you are listed and would like your entry corrected or removed, or you know of a change, email {mail}. See our <a href="{pg.href('privacy')}#directory">privacy notice</a>.</p>
  </div>
</section>"""
    return html, intro


def s151_insights_html(pg):
    """Data insights charts. Spread statistics are computed from the comparison data at build time."""
    import statistics as st
    with open(os.path.join(ROOT, "assets", "data", "s151-reserves.json"), encoding="utf-8") as f:
        R = json.load(f)
    with open(os.path.join(ROOT, "assets", "data", "s151-audit.json"), encoding="utf-8") as f:
        A = json.load(f)
    rows = ""
    spread = {}
    for k in ["SC", "UA", "MD", "LB", "SD"]:
        v = sorted(c["r31"] / c["nre"] * 100 for c in R["councils"] if c["c"] == k and "r31" in c)
        q = st.quantiles(v, n=4)
        spread[k] = (len(v), v[0], q[0], q[1], q[2], v[-1])
        rows += f"<tr><td>{e(R['classes'][k])}s</td><td>{len(v)}</td><td>{v[0]:.0f}%</td><td>{q[0]:.0f}%</td><td>{q[1]:.0f}%</td><td>{q[2]:.0f}%</td><td>{v[-1]:.0f}%</td></tr>"
    trend_rows = "".join(f"<tr><td>{e(d)}</td><td>£{r:.1f}bn</td><td>£{n:.1f}bn</td><td>{r / n * 100:.0f}%</td></tr>" for d, r, n in S151_RESERVES_TREND)
    t0, t1 = S151_RESERVES_TREND[0], S151_RESERVES_TREND[-1]
    tl = A.get("timeliness", [])
    worst = min((x for x in tl if x["basis"] == "deadline"), key=lambda x: x["pct"])
    latest = [x for x in tl if x["basis"] == "backstop"][-1]
    ua = spread["UA"]
    trend_json = e(json.dumps(S151_RESERVES_TREND))
    src = 'rel="noopener"'
    return f"""<section class="block" id="data-insights" style="padding-bottom:0">
  <div class="wrap" id="insights-data" data-base="{pg.base}" data-v="{s151_data_version()}" data-trend="{trend_json}">
    <div class="sec-head">
      <div><p class="eyebrow">Data insights</p><h2>What the numbers show.</h2></div>
      <p class="intro">Our analysis of the official data on council audits and reserves. Hover over or tap a chart for the figures, or open the table beneath it.</p>
    </div>
    <div class="ins-grid">
      <figure class="ins">
        <figcaption><h3>The audit backlog, and the backstop</h3>
        <p>Only {worst['timely']} of {worst['councils']} council audits for {worst['year']} were signed by the statutory deadline. Backstop dates have pushed completion to {latest['pct']:.0f}% for {latest['year']}, but PSAA reports that more than half of the 2024/25 opinions issued by the end of March 2026 were disclaimed or qualified.</p></figcaption>
        <p class="ins-key"><span class="ki"><span class="k1"></span>Signed by the statutory deadline</span> <span class="ki"><span class="k2"></span>Signed by the backstop date</span></p>
        <div class="ins-chart"><canvas id="chartAudit" role="img" aria-label="Bar chart of the share of council audits signed by the deadline or backstop, by year"></canvas></div>
        <details><summary>Show the data</summary><div class="table-wrap"><table class="rates ins-t"><thead><tr><th scope="col">Accounts</th><th scope="col">Measured against</th><th scope="col">Signed in time</th><th scope="col">Share</th></tr></thead><tbody id="tblAudit"></tbody></table></div></details>
        <p class="note">Principal councils in England (districts, unitaries, metropolitan districts, London boroughs and counties) audited under PSAA's scheme. Source: <a href="{e(A['source'])}" {src}>PSAA audit opinion data</a>, as at {e(A['asAt'])}.</p>
      </figure>
      <figure class="ins">
        <figcaption><h3>Reserves are holding in cash terms, but shrinking against spending</h3>
        <p>English councils held £{t1[1]:.1f}bn of non-ringfenced reserves at {t1[0]}, close to the level of recent years. As a share of net revenue expenditure, they have fallen from {t0[1] / t0[2] * 100:.0f}% in {t0[0][9:]} to {t1[1] / t1[2] * 100:.0f}% in {t1[0][9:]}.</p></figcaption>
        <div class="ins-chart"><canvas id="chartTrend" role="img" aria-label="Line chart of non-ringfenced reserves as a share of net revenue expenditure, 2022 to 2026"></canvas></div>
        <details><summary>Show the data</summary><div class="table-wrap"><table class="rates ins-t"><thead><tr><th scope="col">At</th><th scope="col">Non-ringfenced reserves</th><th scope="col">Net revenue expenditure</th><th scope="col">Reserves as share</th></tr></thead><tbody>{trend_rows}</tbody></table></div></details>
        <p class="note">All English local authorities. Other earmarked reserves (as adjusted by MHCLG for comparability where it provides an adjustment) plus unallocated reserves, as reported in each year's revenue outturn. Source: <a href="https://www.gov.uk/government/collections/local-authority-revenue-expenditure-and-financing" {src}>MHCLG revenue expenditure and financing</a>.</p>
      </figure>
      <figure class="ins ins-wide">
        <figcaption><h3>Reserves vary widely within every type of council</h3>
        <p>Among unitary authorities, the middle half hold between {ua[2]:.0f}% and {ua[4]:.0f}% of net revenue expenditure in non-ringfenced reserves, and the lowest just {ua[1]:.0f}%. Districts hold more relative to their spending because their net budgets are small. Use <a href="#compare">Compare your council</a> to find any council.</p></figcaption>
        <div class="ins-chart tall"><canvas id="chartSpread" role="img" aria-label="Dot plot of each council's reserves as a share of net revenue expenditure, grouped by type of council"></canvas></div>
        <details><summary>Show the data</summary><div class="table-wrap"><table class="rates ins-t"><thead><tr><th scope="col">Type of council</th><th scope="col">Councils</th><th scope="col">Lowest</th><th scope="col">Lower quartile</th><th scope="col">Median</th><th scope="col">Upper quartile</th><th scope="col">Highest</th></tr></thead><tbody>{rows}</tbody></table></div></details>
        <p class="note">Non-ringfenced reserves at 31 March 2026 as a share of {e(S151_RESERVES_YEAR)} net revenue expenditure, for the {sum(x[0] for x in spread.values())} councils with usable returns. Shown on a log scale so that districts and counties fit on one chart. Source: <a href="https://www.gov.uk/government/statistics/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-individual-local-authority-data-outturn" {src}>MHCLG revenue outturn {e(S151_RESERVES_YEAR)}</a>.</p>
      </figure>
    </div>
  </div>
</section>"""


def build_s151():
    pg = Page("section-151-officers.html")
    ext = ' rel="noopener"'

    def src(label, url):
        return f' <a href="{e(url)}"{ext}>{e(label)}</a>' if url else ""
    cal = "".join(f"<li><b>{e(w)}</b><span>{e(t)}{(' Source:' + src(l, u)) if u else ''}</span></li>"
                  for w, t, l, u in S151_CALENDAR)
    backstops = "".join(f"<li><b>{e(y)} accounts</b><span>{e(d)}</span></li>" for y, d in S151_BACKSTOPS)
    lib = ""
    for group, items in S151_LIBRARY:
        rows = "".join(f'<li><b><a href="{e(u)}"{ext}>{e(t)}</a></b><span>{e(n)}</span></li>' for t, u, n in items)
        lib += f"\n    <h3>{e(group)}</h3>\n    <ul class=\"scope\">{rows}</ul>"
    posts = [p for p in POSTS if p.get("tag") in S151_TAGS][:6]
    toc = [("figures", "Key figures"), ("compare", "Compare your council"), ("data-insights", "Data insights"), ("role", "The role at a glance"), ("calendar", "The annual cycle"), ("library", "Guidance library"),
           ("directory", "Directory of Section 151 officers"), ("tools", "Free tools"), ("insights", "Insights")]
    toc_html = "".join(f'<a href="#{a}">{e(t)}</a>' for a, t in toc)
    tiles = "".join(f"""<div class="fig">
        <p class="eyebrow">{e(lbl)}</p>
        <p class="num">{e(num)}</p>
        <p>{e(det)}</p>
        <p class="src">Source: <a href="{e(u)}"{ext}>{e(sl)}</a>, {e(asat)}</p>
      </div>""" for lbl, num, det, sl, u, asat in S151_FIGURES)
    tiles += """<div class="fig">
        <p class="eyebrow">PWLB maturity rates</p>
        <div class="rates-mini" id="pwlbLive" aria-live="polite"><span>Loading today's rates…</span></div>
        <p>Certainty rate (standard rate less 20 basis points), updated daily from Debt Management Office data.</p>
        <p class="src">As at <span id="pwlbAsOf">today</span>. <a href="https://dmo.gov.uk/responsibilities/local-authority-lending/lending-arrangements" rel="noopener">DMO</a></p>
      </div>"""
    insights = s151_insights_html(pg)
    directory, S151_DIR_INTRO = s151_directory_html(pg)
    figures = f"""<section class="block" id="figures" style="padding-bottom:0">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Key figures</p><h2>Where the sector stands.</h2></div>
      <p class="intro">The latest national figures for English councils, each linked to its official source. Updated monthly.</p>
    </div>
    <div class="figs">
      {tiles}
    </div>
  </div>
</section>"""
    body = f"""{header(pg, 'tools')}
<main id="main">
{page_hero(pg, [("Home", "")], "Resources for Section 151 officers", "The legislation, codes, deadlines and tools that chief finance officers rely on, gathered in one place and checked against official sources.", eyebrow="Section 151 hub", crumb="Section 151 hub")}
{figures}
<section class="block" id="compare" style="padding-bottom:0">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Compare your council</p><h2>Reserves and audit status, against your peers.</h2></div>
      <p class="intro">Choose an English council to see its reserves against councils of the same type, and the status of its external audits.</p>
    </div>
    <div id="cmp" data-base="{pg.base}" data-v="{s151_data_version()}">
      <div class="cmp-pick">
        <div><label for="cmpCouncil">Council</label>
        <input id="cmpCouncil" list="councilList" autocomplete="off" placeholder="Start typing a council name" disabled>
        <datalist id="councilList"></datalist></div>
      </div>
      <div id="cmpOut" aria-live="polite"></div>
      <p class="note">Reserves are non-ringfenced (unallocated plus earmarked, excluding schools, Dedicated Schools Grant and public health) as reported by each council in its {S151_RESERVES_YEAR} revenue outturn return to MHCLG, published {S151_RESERVES_PUBLISHED}. They are not audited figures and may differ from the council's statement of accounts. Net revenue expenditure is used to compare councils of different sizes. <a href="https://www.gov.uk/government/statistics/local-authority-revenue-expenditure-and-financing-england-2025-to-2026-individual-local-authority-data-outturn" rel="noopener">Source data</a>.</p>
    </div>
  </div>
</section>
{insights}
<div class="wrap layout">
  <article class="prose">
    <p class="intro-line">A practical reference for chief finance officers and their teams in English local government.</p>
    <p>Every link below goes to the official source. We check the dates and links each year before the budget cycle begins. Last checked {fmt_date(S151_CHECKED)}.</p>

    <h2 id="role">The role at a glance</h2>
    <p>Section 151 of the <a href="https://www.legislation.gov.uk/ukpga/1972/70/section/151"{ext}>Local Government Act 1972</a> requires every council to make arrangements for the proper administration of its financial affairs, and to make one officer responsible for them. That officer, usually the director of finance, is known as the section 151 officer or chief finance officer.</p>
    <p>Three statutory duties define the role in practice:</p>
    <ul>
      <li><strong>Section 114 reports.</strong> Under the <a href="https://www.legislation.gov.uk/ukpga/1988/41/section/114"{ext}>Local Government Finance Act 1988</a>, the chief finance officer must report if the council has made, or is about to make, unlawful expenditure, or if expenditure is likely to exceed the resources available to meet it.</li>
      <li><strong>Section 25 reports.</strong> Under the <a href="https://www.legislation.gov.uk/ukpga/2003/26/section/25"{ext}>Local Government Act 2003</a>, the chief finance officer must report to council, when it sets the budget, on the robustness of the estimates and the adequacy of reserves.</li>
      <li><strong>Prudential borrowing.</strong> The council sets its own borrowing limits under the <a href="https://cipfa.org/policy-and-guidance/publications/t/the-prudential-code-for-capital-finance-in-local-authorities-2021-edition"{ext}>CIPFA Prudential Code</a>, and the chief finance officer advises on whether capital plans are affordable, prudent and sustainable.</li>
    </ul>
    <p>CIPFA's statement on <a href="https://www.cipfa.org/policy-and-guidance/reports/the-role-of-the-chief-financial-officer-in-local-government"{ext}>the role of the chief financial officer in local government</a> sets out the principles behind the role, including direct access to the chief executive and a seat at the leadership table.</p>
    <p class="note">This page focuses on England. Sections 151 and 114 also apply in Wales, where councils follow Welsh Government guidance. Scotland and Northern Ireland have their own frameworks.</p>

    <h2 id="calendar">The annual cycle</h2>
    <p>The key statutory and regulatory dates in a typical English council's financial year.</p>
    <ul class="scope">{cal}</ul>
    <h3>Audit backstop dates</h3>
    <p>Accounts must be audited, with the auditor's opinion published, by these statutory backstop dates. <a href="{S151_BACKSTOP_SOURCE}"{ext}>Written ministerial statement, 4 March 2025</a>.</p>
    <ul class="scope">{backstops}</ul>

    <h2 id="library">Guidance library</h2>
    <p>The primary sources Section 151 officers refer to most often.</p>{lib}

    <h2 id="directory">Directory of Section 151 officers</h2>
    {S151_DIR_INTRO}

    <p class="note">Spotted something out of date? Please <a href="mailto:{SITE['email']}">let us know</a>. This page is general information, not legal or financial advice.</p>
  </article>
  <aside class="aside">
    <nav class="related" aria-label="On this page">
      <p class="eyebrow">On this page</p>
      {toc_html}
    </nav>
    <div class="cta-card">
      <p class="eyebrow">Talk to a specialist</p>
      <h2>Need a second opinion?</h2>
      <p>We support Section 151 officers on HRA business plans, temporary accommodation costs, capital financing and MTFP pressures.</p>
      <a class="btn btn-brass" href="{pg.href('contact')}">Request a call back</a>
      <p class="small"><a href="mailto:{SITE['email']}">{SITE['email']}</a><br><a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a></p>
    </div>
  </aside>
</div>
{directory}
<section class="block" id="tools" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Free tools</p><h2>Calculators and the HRA Assistant.</h2></div>
      <p class="intro">Built for local authority treasury and housing finance teams. Free to use.</p>
    </div>
    {tools_html(pg)}
  </div>
</section>
<section class="block" id="insights" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Insights</p><h2>For Section 151 officers.</h2></div>
      <p class="intro"><a class="link" href="{pg.href('blog')}">All articles</a></p>
    </div>
    <div class="posts">{post_cards(pg, posts)}</div>
  </div>
</section>
{frameworks_html(pg)}
{contact_band(pg)}
</main>
"""
    write(pg, head(pg, "Resources for Section 151 Officers",
                   "Legislation, codes, key dates and free tools for local authority Section 151 officers and chief finance officers, checked against official sources.",
                   og_eyebrow="Section 151 hub") + body + footer(pg, f'<script src="{pg.asset("js/s151-figures.js")}" defer></script>\n<script src="{pg.asset("js/s151-compare.js")}" defer></script>\n<script src="{pg.base}assets/js/vendor/chart-4.5.0.umd.min.js" defer></script>\n<script src="{pg.asset("js/s151-insights.js")}" defer></script>\n<script src="{pg.asset("js/s151-directory.js")}" defer></script>\n'))


def build_404():
    pg = Page("404.html")
    # 404 is served from any depth, so use absolute links here
    pg.base = "/"
    body = f"""{header(pg)}
<main id="main">
{page_hero(pg, [("Home", "")], "Page not found", "The page you were looking for has moved or no longer exists.", eyebrow="404")}
<section class="block">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Where next</p><h2>Our services</h2></div></div>
    <div class="services">{services_grid(pg)}</div>
  </div>
</section>
</main>
"""
    write(pg, head(pg, "Page not found", "Page not found.", noindex=True) + body + footer(pg))


def build_sitemap():
    today = date.today().isoformat()
    urls = [("", today), ("blog", today), ("our-team", today), ("testimonials", today), ("contact", today),
            ("useful-tools", today), ("pwlb-premium/discount-calculator", today), ("pwlb-v-il", today),
            ("case-studies", today), ("privacy", today), ("section-151-officers", today)]
    if SITE.get("hra_endpoint"):
        urls.append(("hra-assistant", today))
    urls += [(s["slug"], today) for s in SERVICES]
    urls += [(p["slug"], p["date"]) for p in POSTS]
    body = "".join(f"<url><loc>{SITE['url']}/{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")


if __name__ == "__main__":
    build_home()
    build_services()
    build_testimonials()
    build_team()
    build_contact()
    build_posts()
    build_blog()
    build_tools()
    build_pwlb_repayment()
    build_pwlb_vs_il()
    build_hra_assistant()
    build_case_studies()
    build_privacy()
    build_s151()
    build_404()
    build_sitemap()
    from og import render_cards
    import content as _c
    n = render_cards(OG_CARDS, google={p_["slug"] for p_ in _c.POSTS})
    import content as _content
    from capability import build_capability
    pdf = build_capability(_content)
    print("Built site into", ROOT, f"({n} share images, capability statement {'updated' if pdf else 'unchanged'})")
