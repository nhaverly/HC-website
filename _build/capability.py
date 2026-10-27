# -*- coding: utf-8 -*-
"""Builds the downloadable capability statement PDF from the website content.

Called automatically by build.py (needs Playwright with Chromium). If Playwright
isn't available, the existing PDF is left as it is.
"""
import html
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(HERE, "fonts")
OUT_DIR = os.path.join(ROOT, "assets", "docs")
OUT_NAME = "haverly-consulting-capability-statement.pdf"
e = html.escape


def _html(c):
    S = c.SITE
    logo = open(os.path.join(ROOT, "assets", "img", "logo-wordmark.svg"), encoding="utf-8").read()
    services = "".join(f"<div class='svc'><b>{e(s['name'])}</b><p>{e(s['blurb'])}</p></div>" for s in c.SERVICES)
    creds = "".join(f"<li>{e(x)}</li>" for x in c.ABOUT_NICK["points"])
    fw = "".join(f"<li><b>{e(f['name'])}</b> {e(f['detail'])}</li>" for f in c.FRAMEWORKS)
    cases = ""
    for cs in c.CASE_STUDIES:
        fig = f"<span class='fig'>{e(cs['figure'])}</span>" if cs.get("figure") else ""
        cases += (f"<div class='case'><p class='eb'>{e(cs['client'])}</p><h3>{fig}{e(cs['title'])}</h3>"
                  f"<p>{e(cs['summary'])}</p></div>")
    clients = " · ".join(e(x) for x in c.CLIENTS)
    quotes = "".join(f"<blockquote>“{e(t['quote'])}”<cite>{e(t['role'])}, {e(t['org'])}</cite></blockquote>"
                     for t in (c.TESTIMONIALS[0], c.TESTIMONIALS[1]))
    addr = ", ".join(S["address"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Serif;src:url("file://{FONTS}/serif.woff2")}}
@font-face{{font-family:Sans;src:url("file://{FONTS}/sans.ttf")}}
@font-face{{font-family:Sans;font-weight:700;src:url("file://{FONTS}/sans-bold.ttf")}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0}}
body{{font-family:Sans,Arial,sans-serif;font-size:9.6pt;line-height:1.45;color:#0B090A}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always}}
.page:last-child{{page-break-after:auto}}
  .band{{background:#090F54;border-top:2mm solid #1DB6D0;color:#FFFFFF;padding:14mm 16mm 10mm}}
.top{{display:flex;justify-content:space-between;align-items:flex-start}}
.logo{{background:#fff;padding:2.4mm 3.4mm;border-radius:1mm;display:flex}}.logo svg{{height:15mm;width:auto}}
.doc{{font-weight:700;font-size:7.6pt;letter-spacing:.15em;text-transform:uppercase;color:#1DB6D0;text-align:right}}
.doc span{{display:block;color:#FFFFFF;margin-top:1.5mm}}
h1{{font-family:Serif,Georgia,serif;font-weight:400;font-size:28pt;line-height:1.1;letter-spacing:-.03em;margin-top:9mm}}
.lede{{color:#FFFFFF;font-size:11pt;margin-top:3mm;max-width:160mm}}
.body{{padding:8mm 16mm 0;display:grid;gap:6mm}}
.cols{{display:grid;grid-template-columns:1.25fr 1fr;gap:8mm}}
h2{{font-weight:700;font-size:7.6pt;letter-spacing:.15em;text-transform:uppercase;color:#090F54;border-bottom:.3mm solid rgba(9,15,84,.16);padding-bottom:1.5mm;margin-bottom:3mm}}
.svcs{{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm 6mm}}
.svc b{{font-family:Sans,Arial,sans-serif;font-weight:700;font-size:10.5pt;color:#090F54;display:block}}
.svc p{{color:#0B090A;font-size:8.8pt;margin-top:.6mm}}
ul{{padding-left:0;list-style:none;display:grid;gap:2mm}}
ul.creds2{{grid-template-columns:1fr 1fr;gap:2mm 7mm}}
li{{padding-left:3mm;border-left:.6mm solid #1DB6D0;font-size:9pt}}
.box{{background:#FFFFFF;border:.3mm solid rgba(9,15,84,.16);padding:4mm 5mm}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:1.4mm 4mm;font-size:9pt}}
dt{{font-weight:700;font-size:7pt;letter-spacing:.06em;text-transform:uppercase;color:#0B090A;padding-top:.5mm}}
.fw li b{{font-weight:700;display:block;font-size:10pt;color:#090F54}}
.cases{{display:grid;grid-template-columns:1fr 1fr;gap:5mm 7mm}}
.case{{border-top:.8mm solid #090F54;padding-top:2.5mm}}
.case .eb{{font-weight:700;font-size:7pt;letter-spacing:.08em;text-transform:uppercase;color:#090F54}}
.case h3{{font-family:Serif,Georgia,serif;font-weight:400;font-size:13pt;color:#090F54;line-height:1.15;margin:1mm 0 1.2mm}}
.case .fig{{color:#090F54;margin-right:2mm}}
.case p{{color:#0B090A;font-size:8.8pt}}
blockquote{{font-size:9pt;border-left:.6mm solid #090F54;padding-left:3.5mm;margin-bottom:3.5mm}}
cite{{display:block;font-style:normal;font-size:8pt;color:#0B090A;margin-top:1mm}}
.clients{{font-size:9.6pt;line-height:1.7;color:#090F54}}
.foot{{position:absolute;left:0;right:0;bottom:0;background:#090F54;color:#FFFFFF;border-top:1mm solid #1DB6D0;padding:4mm 16mm;font-size:7.6pt;display:flex;justify-content:space-between}}
.foot b{{color:#FFFFFF;font-weight:400}}
</style></head><body>
<div class="page">
  <div class="band">
    <div class="top"><div class="logo">{logo}</div><p class="doc">Capability statement<span>{date.today().strftime('%B %Y')}</span></p></div>
    <h1>Independent housing finance advisory for local government</h1>
    <p class="lede">We structure funding, test viability and stabilise budgets so councils can deliver more homes with less risk.</p>
  </div>
  <div class="body">
    <div class="cols">
      <section><h2>Services</h2><div class="svcs">{services}</div></section>
      <section>
        <h2>Company details</h2>
        <div class="box"><dl>
          <dt>Company</dt><dd>Haverly Consulting Ltd</dd>
          <dt>Number</dt><dd>{e(S['company_number'])} (England and Wales)</dd>
          <dt>Office</dt><dd>{e(addr)}</dd>
          <dt>Contact</dt><dd>{e(S['email'])}<br>{e(S['phone'])}</dd>
          <dt>Web</dt><dd>haverlyconsulting.co.uk</dd>
        </dl></div>
      </section>
    </div>
    <section><h2>Procurement routes</h2><ul class="fw">{fw}</ul></section>
  </div>
  <div class="foot"><b>haverlyconsulting.co.uk</b><span>{e(S['email'])} · {e(S['phone'])}</span></div>
</div>
<div class="page">
  <div class="body" style="padding-top:14mm">
    <section><h2>Leadership: {e(next(t for t in c.TEAM if t['id']=='nick')['name'])}, Director</h2><ul class='creds2'>{creds}</ul></section>
    <section><h2>Selected work</h2><div class="cases">{cases}</div></section>
    <div class="cols">
      <section><h2>Client feedback</h2>{quotes}</section>
      <section><h2>Selected clients</h2><p class="clients">{clients}</p></section>
    </div>
  </div>
  <div class="foot"><b>Haverly Consulting Ltd · Company {e(S['company_number'])}</b><span>{e(addr)}</span></div>
</div>
</body></html>"""


def build_capability(content_module):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    os.makedirs(OUT_DIR, exist_ok=True)
    tmp = os.path.join(HERE, ".cap-tmp.html")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(_html(content_module))
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page()
            page.goto("file://" + tmp)
            page.evaluate("document.fonts.ready")
            page.pdf(path=os.path.join(OUT_DIR, OUT_NAME), format="A4", print_background=True,
                     margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            b.close()
        return True
    except Exception as exc:
        print("Capability statement not rendered:", exc)
        return False
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
