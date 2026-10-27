# -*- coding: utf-8 -*-
"""Renders 1200x630 share images (used by LinkedIn, X, Teams, Slack previews).

Called automatically by build.py. Needs Playwright with Chromium:
    pip install playwright && python -m playwright install chromium
If Playwright isn't available, existing images are kept and any missing ones
fall back to a copy of assets/og/home.jpg.
"""
import html
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "og")
FONTS = os.path.join(HERE, "fonts")

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Serif;src:url("file://%(fonts)s/serif.woff2")}
@font-face{font-family:Sans;src:url("file://%(fonts)s/sans.ttf")}
@font-face{font-family:Sans;font-weight:700;src:url("file://%(fonts)s/sans-bold.ttf")}
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#FFFFFF;color:#0B090A;font-family:Sans,Arial,sans-serif;position:relative}
.side{position:absolute;top:0;right:0;bottom:0;width:250px;background:#090F54;border-top:8px solid #1DB6D0;display:flex;align-items:center;justify-content:center}
.side svg{width:96px;height:auto}
.wrap{position:absolute;top:0;left:0;bottom:0;right:250px;padding:56px 64px 0 72px;display:flex;flex-direction:column}
.logo svg{height:74px;width:auto}
.eyebrow{display:flex;align-items:center;gap:16px;font-size:19px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#090F54;margin-top:52px}
.eyebrow i{display:inline-block;width:40px;height:4px;background:#1DB6D0}
h1{font-family:Serif,Georgia,serif;font-weight:400;color:#090F54;line-height:1.08;letter-spacing:-.035em;margin-top:22px;max-width:820px}
.by{font-size:24px;color:#0B090A;margin-top:22px;max-width:780px;line-height:1.45}
.foot{position:absolute;left:72px;right:314px;bottom:44px;display:flex;justify-content:space-between;font-size:18px;color:#090F54;border-top:1px solid rgba(9,15,84,.16);padding-top:18px}
.foot b{font-weight:700}
</style></head><body>
<div class="side"><svg viewBox="0 0 92 96" aria-hidden="true"><path d="M0 0h21v96H0zM71 0h21v96H71z" fill="#FFFFFF"/><path d="M35 0h21v38H35zM35 54h21v42H35z" fill="#1DB6D0"/></svg></div>
<div class="wrap">
<div class="logo">%(logo)s</div>
<p class="eyebrow"><i></i>%(eyebrow)s</p>
<h1 id="t">%(title)s</h1>
%(byline)s
</div>
<div class="foot"><b>haverlyconsulting.co.uk</b><span>Financial clarity. Better housing.</span></div>
<script>
const t=document.getElementById('t');let size=68;t.style.fontSize=size+'px';
const by=document.querySelector('.by');const limit=by?220:300;
while(t.scrollHeight>limit&&size>36){size-=2;t.style.fontSize=size+'px';}
</script></body></html>"""


GOOGLE_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Serif;src:url("file://%(fonts)s/serif.woff2")}
@font-face{font-family:Sans;src:url("file://%(fonts)s/sans.ttf")}
@font-face{font-family:Sans;font-weight:700;src:url("file://%(fonts)s/sans-bold.ttf")}
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:900px;overflow:hidden}
body{background:#FFFFFF;color:#0B090A;font-family:Sans,Arial,sans-serif;position:relative;border-top:12px solid #1DB6D0}
.edge{position:absolute;top:0;bottom:0;width:130px;background:#090F54}
.edge.l{left:0}.edge.r{right:0}
.edge svg{position:absolute;left:50%%;bottom:56px;transform:translateX(-50%%);width:54px;height:auto}
.wrap{position:absolute;top:0;bottom:0;left:130px;right:130px;padding:70px 70px 0;display:flex;flex-direction:column;align-items:center;text-align:center}
.logo svg{height:96px;width:auto}
.eyebrow{display:flex;align-items:center;gap:14px;font-size:22px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:#090F54;margin-top:56px}
.eyebrow i{display:inline-block;width:36px;height:4px;background:#1DB6D0}
h1{font-family:Serif,Georgia,serif;font-weight:400;color:#090F54;line-height:1.1;letter-spacing:-.03em;margin-top:30px}
.foot{position:absolute;left:200px;right:200px;bottom:52px;text-align:center;font-size:24px;color:#090F54;border-top:1px solid rgba(9,15,84,.16);padding-top:22px;font-weight:700}
</style></head><body>
<div class="edge l"><svg viewBox="0 0 92 96" aria-hidden="true"><path d="M0 0h21v96H0zM71 0h21v96H71z" fill="#FFFFFF"/><path d="M35 0h21v38H35zM35 54h21v42H35z" fill="#1DB6D0"/></svg></div>
<div class="edge r"></div>
<div class="wrap">
<div class="logo">%(logo)s</div>
<p class="eyebrow"><i></i>%(eyebrow)s<i></i></p>
<h1 id="t">%(title)s</h1>
</div>
<div class="foot">haverlyconsulting.co.uk</div>
<script>
const t=document.getElementById('t');let size=76;t.style.fontSize=size+'px';
while(t.scrollHeight>380&&size>40){size-=2;t.style.fontSize=size+'px';}
</script></body></html>"""


def render_cards(cards, google=()):
    """Render share images. Cards whose name is in `google` also get a
    1200x900 version for Google Business Profile posts (assets/og/google/),
    laid out so Google's squarer crop doesn't cut the headline."""
    os.makedirs(OUT, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        _fallback(cards)
        return 0
    with open(os.path.join(ROOT, "assets", "img", "logo-wordmark.svg"), encoding="utf-8") as f:
        logo = f.read()
    tmp = os.path.join(HERE, ".og-tmp.html")
    n = 0
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 630})
            for name, eyebrow, title, byline in cards:
                doc = TEMPLATE % {
                    "fonts": FONTS, "logo": logo, "eyebrow": html.escape(eyebrow),
                    "title": html.escape(title),
                    "byline": f'<p class="by">{html.escape(byline)}</p>' if byline else "",
                }
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(doc)
                page.goto("file://" + tmp)
                page.evaluate("document.fonts.ready")
                page.screenshot(path=os.path.join(OUT, name + ".jpg"), type="jpeg", quality=86)
                n += 1
                if name in google:
                    gdir = os.path.join(OUT, "google")
                    os.makedirs(gdir, exist_ok=True)
                    page.set_viewport_size({"width": 1200, "height": 900})
                    with open(tmp, "w", encoding="utf-8") as f:
                        f.write(GOOGLE_TEMPLATE % {"fonts": FONTS, "logo": logo,
                                "eyebrow": html.escape(eyebrow), "title": html.escape(title)})
                    page.goto("file://" + tmp)
                    page.evaluate("document.fonts.ready")
                    page.screenshot(path=os.path.join(gdir, name + ".jpg"), type="jpeg", quality=88)
                    page.set_viewport_size({"width": 1200, "height": 630})
            browser.close()
    except Exception as exc:  # e.g. Chromium not installed
        print("Share images not rendered:", exc)
        _fallback(cards)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return n


def _fallback(cards):
    default = os.path.join(OUT, "home.jpg")
    for name, *_ in cards:
        target = os.path.join(OUT, name + ".jpg")
        if not os.path.exists(target) and os.path.exists(default):
            shutil.copy(default, target)
