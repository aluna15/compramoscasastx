#!/usr/bin/env python3
"""Build the Spanish Compramos Casas TX site into docs/ for GitHub Pages."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
CHA = Path("/Users/work/Downloads/CHA_Website")
SITE = "https://www.compramoscasastx.com"
EN = "https://www.cashhomeadvisors.com"
PHONE = "(817) 520-8319"
TEL = "+18175208319"
EMAIL = "adrian@cashhomeadvisors.com"
GA4_ID = "G-BJY8TC7V1C"
# Facts a Spanish answer can quote. Approved claims only; no ranking, no address.
ORG_DESCRIPTION = (
    "Compramos Casas TX es el sitio en español de Cash Home Advisors, LLC. "
    "La empresa compra casas en Texas como principal, no como el agente del vendedor. "
    "Cierre en 7 a 14 días. Pagamos todos los gastos de cierre. "
    "Venda tal como está, sin reparaciones. Sin comisiones de agente. "
    "Gratis, sin compromiso. Una persona real le devuelve la llamada."
)
_EN_ORG_DESC = (
    "Cash Home Advisors buys houses for cash in Dallas\u2013Fort Worth, Houston, and across Texas. "
    "Sell as-is with no repairs and no agent commissions. We pay all closing costs. "
    "Close in 7\u201314 days. Se habla español."
)
ENTITY_ANSWER = (
    ORG_DESCRIPTION
    + " Teléfono (817) 520-8319. Adrian Luna, agente de bienes raíces de Texas, TREC #675272-SA."
)
QUOTE_PAGES = (
    "index.html",
    "como-funciona.html",
    "compramos-casas-texas.html",
    "compramos-casas-dallas.html",
    "compramos-casas-fort-worth.html",
    "compramos-casas-houston.html",
    "compramos-casas-san-antonio.html",
    "compramos-casas-austin.html",
    "por-que-nosotros.html",
    "formas-de-vender.html",
    "preguntas-frecuentes.html",
    "sobre-nosotros.html",
    "blog/es/index.html",
    "ciudades.html",
)
LLMS_LINKS = (
    ("Inicio", SITE + "/"),
    ("Cómo funciona", SITE + "/como-funciona"),
    ("Texas", SITE + "/compramos-casas-texas"),
    ("Dallas", SITE + "/compramos-casas-dallas"),
    ("Fort Worth", SITE + "/compramos-casas-fort-worth"),
    ("Houston", SITE + "/compramos-casas-houston"),
    ("San Antonio", SITE + "/compramos-casas-san-antonio"),
    ("Austin", SITE + "/compramos-casas-austin"),
    ("Guías", SITE + "/blog/es/"),
    ("Ciudades", SITE + "/ciudades"),
)
ENDPOINT = "https://services.leadconnectorhq.com/hooks/eRpXDjkyyScY5hEr424s/webhook-trigger/RkJTfvGE7v99bZynCdAE"

PATHS = {
    "/get-offer": "/oferta",
    "/how-it-works": "/como-funciona",
    "/why-us": "/por-que-nosotros",
    "/ways-to-sell": "/formas-de-vender",
    "/faq": "/preguntas-frecuentes",
    "/contact": "/contacto",
    "/about": "/sobre-nosotros",
    "/privacy": "/privacidad",
    "/terms": "/terminos-de-uso",
    "/sms-terms": "/terminos-sms",
    "/editorial-policy": "/politica-editorial",
    "/reviews": "/resenas",
    "/opiniones": "/resenas",
    "/wholesalers": "/mayoristas",
    "/we-buy-houses-dallas": "/compramos-casas-dallas",
    "/we-buy-houses-fort-worth": "/compramos-casas-fort-worth",
    "/we-buy-houses-houston": "/compramos-casas-houston",
    "/we-buy-houses-austin": "/compramos-casas-austin",
    "/we-buy-houses-san-antonio": "/compramos-casas-san-antonio",
    "/we-buy-houses-texas": "/compramos-casas-texas",
    "/we-buy-houses-dfw": "/zonas-donde-compramos",
    "/we-buy-houses": "/situaciones",
    "/areas-we-serve": "/zonas-donde-compramos",
    "/zonas": "/zonas-donde-compramos",
    "/sell-house-with-tenants-texas": "/vender-casa-con-inquilinos-texas",
    "/sell-house-job-relocation-texas": "/vender-casa-por-mudanza-texas",
    "/sell-house-to-downsize-texas": "/vender-casa-para-reducir-texas",
    "/sell-house-needing-repairs-texas": "/vender-casa-que-necesita-reparaciones-texas",
    "/seller-net-proceeds-calculator": "/calculadora-ganancia-neta",
    "/holding-cost-calculator": "/calculadora-costos-de-mantener",
    "/how-cash-offers-are-calculated": "/como-se-calcula-una-oferta-en-efectivo",
    "/como-se-calcula-una-oferta-en-efectivo": "/como-se-calcula-una-oferta-en-efectivo",
    "/sell-inherited-house-texas": "/vender-casa-heredada-texas",
    "/stop-foreclosure-sell-house-texas": "/evitar-embargo-vender-casa-texas",
    "/calculadora-costos-de-mantener": "/calculadora-costos-de-mantener",
    "/privacy": "/privacidad",
    "/sms-terms": "/terminos-sms",
}

EN_TWIN = {
    "compramos-casas-dallas": "/we-buy-houses-dallas",
    "compramos-casas-fort-worth": "/we-buy-houses-fort-worth",
    "compramos-casas-houston": "/we-buy-houses-houston",
    "compramos-casas-austin": "/we-buy-houses-austin",
    "compramos-casas-san-antonio": "/we-buy-houses-san-antonio",
    "compramos-casas-texas": "/we-buy-houses-texas",
    "evitar-embargo-vender-casa-texas": "/stop-foreclosure-sell-house-texas",
    "vender-casa-condominio-texas": "/sell-condo-texas",
    "vender-casa-danada-por-incendio-texas": "/sell-fire-damaged-house-texas",
    "vender-casa-en-bancarrota-texas": "/sell-house-during-bankruptcy-texas",
    "vender-casa-heredada-texas": "/sell-inherited-house-texas",
    "vender-casa-impuestos-atrasados-texas": "/sell-house-back-taxes-texas",
    "vender-casa-llena-de-pertenencias-texas": "/sell-hoarder-house-texas",
    "vender-casa-movil-texas": "/sell-mobile-home-texas",
    "vender-casa-multifamiliar-texas": "/sell-multifamily-texas",
    "vender-casa-por-divorcio-texas": "/sell-house-divorce-texas",
    "vender-casa-terreno-baldio-texas": "/sell-vacant-land-cash-texas",
    "vender-casa-con-inquilinos-texas": "/sell-house-with-tenants-texas",
    "vender-casa-por-mudanza-texas": "/sell-house-job-relocation-texas",
    "vender-casa-para-reducir-texas": "/sell-house-to-downsize-texas",
    "vender-casa-que-necesita-reparaciones-texas": "/sell-house-needing-repairs-texas",
    "como-se-calcula-una-oferta-en-efectivo": "/how-cash-offers-are-calculated",
    "como-funciona": "/how-it-works",
    "por-que-nosotros": "/why-us",
    "formas-de-vender": "/ways-to-sell",
    "preguntas-frecuentes": "/faq",
    "contacto": "/contact",
    "oferta": "/get-offer",
    "sobre-nosotros": "/about",
    "privacidad": "/privacy",
    "terminos-de-uso": "/terms",
    "terminos-sms": "/sms-terms",
    "politica-editorial": "/editorial-policy",
    "resenas": "/reviews",
    "mayoristas": "/wholesalers",
    "situaciones": "/we-buy-houses",
    "zonas-donde-compramos": "/areas-we-serve",
    "calculadora-ganancia-neta": "/seller-net-proceeds-calculator",
    "calculadora-costos-de-mantener": "/holding-cost-calculator",
    "": "/",
}

SITS = [
    ("/evitar-embargo-vender-casa-texas", "Riesgo de embargo"),
    ("/vender-casa-heredada-texas", "Casas heredadas y sucesiones"),
    ("/vender-casa-por-divorcio-texas", "Vender por divorcio"),
    ("/vender-casa-que-necesita-reparaciones-texas", "Casa que necesita reparaciones"),
    ("/vender-casa-danada-por-incendio-texas", "Casa dañada por incendio"),
    ("/vender-casa-llena-de-pertenencias-texas", "Casa llena de pertenencias"),
    ("/vender-casa-condominio-texas", "Condominio"),
    ("/vender-casa-multifamiliar-texas", "Dúplex y multifamiliar pequeño"),
    ("/vender-casa-movil-texas", "Casa prefabricada"),
    ("/vender-casa-terreno-baldio-texas", "Terreno baldío"),
    ("/vender-casa-en-bancarrota-texas", "Casa en bancarrota"),
    ("/vender-casa-con-inquilinos-texas", "Casa con inquilinos"),
    ("/vender-casa-por-mudanza-texas", "Mudanza por trabajo"),
    ("/vender-casa-para-reducir-texas", "Mudarse a algo más pequeño"),
    ("/vender-casa-impuestos-atrasados-texas", "Impuestos de propiedad atrasados"),
]

METROS = [
    ("/compramos-casas-dallas", "Dallas"),
    ("/compramos-casas-fort-worth", "Fort Worth"),
    ("/compramos-casas-houston", "Houston"),
    ("/compramos-casas-san-antonio", "San Antonio"),
    ("/compramos-casas-austin", "Austin"),
    ("/compramos-casas-texas", "Todo Texas"),
]


_ES_CACHE = None


def es_dict():
    global _ES_CACHE
    if _ES_CACHE is None:
        text = (CHA / "docs/assets/site.js").read_text(encoding="utf-8")
        i = text.find("var ES=")
        _ES_CACHE, _ = json.JSONDecoder().raw_decode(text[i + 7 :])
    return _ES_CACHE


# Filled in main() before any page is rewritten. English path -> Spanish path on this site.
OUR_PATHS = set()
EN_TO_ES = {}


def _norm(path):
    if not path:
        return "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path or "/"


def _split_href(href):
    if href.startswith(EN):
        rest = href[len(EN):] or "/"
    elif href.startswith("/") and not href.startswith("//"):
        rest = href
    else:
        return None
    base, sep, frag = rest.partition("#")
    query = ""
    if "?" in base:
        base, q = base.split("?", 1)
        query = "?" + q
    return (base or "/"), query, ("#" + frag) if sep else ""


def _has_path(path):
    return _norm(path) in OUR_PATHS or path in OUR_PATHS


def _local_target(base, query, frag):
    path = _norm(base)
    if path.startswith("/assets/checklists"):
        return None
    if path.startswith("/assets") or path == "/favicon.ico":
        return base + query + frag
    if _has_path(path):
        return path + query + frag
    mapped = PATHS.get(path) or PATHS.get(base)
    if mapped:
        return _norm(mapped) + query + frag
    if path in EN_TO_ES:
        return _norm(EN_TO_ES[path]) + query + frag
    return None


def _retarget(href, lang_switch):
    if href.startswith(("mailto:", "tel:", "sms:", "javascript:", "#")):
        return href
    if lang_switch:
        if href.startswith("/"):
            return EN + href
        return href
    parts = _split_href(href)
    if parts is None:
        return href
    local = _local_target(*parts)
    if local is not None:
        return local
    if href.startswith(EN):
        return href
    if href.startswith("/"):
        return EN + href
    return href


def rewrite(fragment):
    fragment = fragment.replace('href="/get-offer#es"', 'href="/oferta"')
    for old, new in sorted(PATHS.items(), key=lambda kv: -len(kv[0])):
        fragment = fragment.replace(f'href="{old}#es"', f'href="{new}"')
        fragment = fragment.replace(f'href="{old}"', f'href="{new}"')
        fragment = fragment.replace(f'href="{old}#', f'href="{new}#')

    def fix_anchor(match):
        tag = match.group(0)
        hm = re.search(r'href="([^"]*)"', tag)
        if not hm:
            return tag
        href = hm.group(1)
        new = _retarget(href, "data-lang-switch" in tag)
        if new != href:
            tag = tag.replace(f'href="{href}"', f'href="{new}"', 1)
        return tag

    fragment = re.sub(r"<a\b[^>]*>", fix_anchor, fragment)
    fragment = fragment.replace(
        'href="/assets/checklists/',
        'href="https://www.cashhomeadvisors.com/assets/checklists/',
    )
    fragment = re.sub(r'\sdata-i18n(?:-alt|-al|-ph)?="[^"]*"', '', fragment)
    return fragment


def spanish_sources():
    pages = []
    for path in (CHA / "docs").rglob("*.html"):
        head = path.read_text(encoding="utf-8", errors="ignore")[:600]
        if "<html lang=\"es\"" in head or "<html lang='es'" in head:
            pages.append(path)
    return pages


def rel_url(path):
    rel = path.relative_to(CHA / "docs")
    if rel.name == "index.html":
        parent = rel.parent.as_posix()
        return "/" if parent == "." else "/" + parent + "/"
    return "/" + rel.with_suffix("").as_posix()


def prepare_maps():
    global OUR_PATHS, EN_TO_ES
    OUR_PATHS = {"/"}
    EN_TO_ES = {}
    for path in spanish_sources():
        url = rel_url(path)
        OUR_PATHS.add(_norm(url))
        OUR_PATHS.add(url)
        text = path.read_text(encoding="utf-8", errors="ignore")[:12000]
        en = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)"', text)
        if not en:
            continue
        target = en.group(1)
        if target.startswith(EN):
            target = target[len(EN):] or "/"
        if target.startswith("/"):
            EN_TO_ES[_norm(target.split("#")[0])] = _norm(url)
    for slug in (
        "oferta", "mayoristas", "gracias", "gracias-listada", "politica-editorial",
        "compramos-casas-austin", "compramos-casas-san-antonio", "ciudades",
        "vender-casa-con-inquilinos-texas", "vender-casa-por-mudanza-texas",
        "vender-casa-para-reducir-texas", "vender-casa-que-necesita-reparaciones-texas",
    ):
        OUR_PATHS.add("/" + slug)


def _es_text(ES, key, fallback):
    if key not in ES:
        return fallback
    val = ES[key]
    return val if "<" in val else html.escape(val)


def apply_es_fragment(fragment, ES):
    def span(match):
        return _es_text(ES, match.group(1), match.group(0))

    fragment = re.sub(r'<span data-i18n="([^"]+)">.*?</span>', span, fragment, flags=re.S)

    def tagged(match):
        tag, key, inner = match.group(1), match.group(2), match.group(3)
        text = _es_text(ES, key, inner)
        return f"<{tag}>{text}</{tag}>"

    fragment = re.sub(
        r"<([a-z0-9]+)\b[^>]*\sdata-i18n=\"([^\"]+)\"[^>]*>([^<]*)</\1>",
        tagged,
        fragment,
    )

    def tag_ph(match):
        tag = match.group(0)
        keym = re.search(r'data-i18n-ph="([^"]+)"', tag)
        if not keym or keym.group(1) not in ES:
            return tag
        ph = html.escape(ES[keym.group(1)], quote=True)
        if re.search(r'placeholder="[^"]*"', tag):
            return re.sub(r'placeholder="[^"]*"', f'placeholder="{ph}"', tag, count=1)
        return tag[:-1] + f' placeholder="{ph}">'

    return re.sub(r"<input\b[^>]*>", tag_ph, fragment)


def replace_lead_cards(fragment, fid):
    token = '<div class="card lead-card"'
    out = []
    i = 0
    n = 0
    while True:
        j = fragment.find(token, i)
        if j < 0:
            out.append(fragment[i:])
            break
        out.append(fragment[i:j])
        pos = j
        depth = 0
        end = None
        while pos < len(fragment):
            nxt_open = fragment.find("<div", pos)
            nxt_close = fragment.find("</div>", pos)
            if nxt_close < 0:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                pos = nxt_open + 4
            else:
                depth -= 1
                pos = nxt_close + len("</div>")
                if depth == 0:
                    end = pos
                    break
        if end is None:
            out.append(fragment[j:])
            break
        n += 1
        use = fid if n == 1 else f"{fid}-{n}"
        out.append(form(use))
        i = end
    return "".join(out)


def homepage_main(ES):
    raw = (CHA / "docs/index.html").read_text(encoding="utf-8")
    main = re.search(r'<main id="main">(.*)</main>', raw, re.S).group(1)
    main = apply_es_fragment(main, ES)
    main = replace_lead_cards(main, "hero")
    main = main.replace("/assets/cha-logo-360.png", "/assets/logo-360.png")
    main = main.replace("/assets/cha-logo-900.png", "/assets/logo-900.png")
    return rewrite(main)


def faqs_from_html(fragment):
    """Read only real questions. A greedy details/summary match was swallowing the nav into the first FAQ."""
    sect = re.search(r'<section[^>]*\bid="faq"[^>]*>(.*)</section>', fragment, re.S)
    scope = sect.group(1) if sect else fragment
    faqs = []
    pat = re.compile(
        r"<details><summary>((?:(?!</summary>).)*)</summary>\s*<p>((?:(?!</p>).)*)</p></details>",
        re.S,
    )
    for match in pat.finditer(scope):
        q = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", match.group(1))).strip()
        a = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", match.group(2))).strip()
        if q.startswith("¿") and a:
            faqs.append({"q": q, "a": a})
    return faqs


def rewrite_jsonld(js):
    for path in sorted(OUR_PATHS, key=len, reverse=True):
        if path.startswith("/assets"):
            continue
        js = js.replace(EN + path, SITE + path)
    js = js.replace(EN + "/about#adrian", SITE + "/sobre-nosotros#adrian")
    js = js.replace(EN + "/about", SITE + "/sobre-nosotros")
    js = js.replace(EN + "/editorial-policy", SITE + "/politica-editorial")
    js = js.replace(EN + "/#business", SITE + "/#business")
    js = js.replace(EN + "/#website", SITE + "/#website")
    js = js.replace("https://www.cashhomeadvisors.com/assets/cha-logo-360.png", SITE + "/assets/logo-360.png")
    js = js.replace("https://www.cashhomeadvisors.com/assets/cha-logo-900.png", SITE + "/assets/logo-900.png")
    js = js.replace("/assets/cha-logo-360.png", "/assets/logo-360.png")
    js = js.replace("/assets/cha-logo-900.png", "/assets/logo-900.png")
    js = js.replace('"name": "Cash Home Advisors"', '"name": "Compramos Casas TX"')
    # Domain swap above turns /about into a Spanish-host path before the English-host replace runs.
    js = js.replace(SITE + "/about#adrian", SITE + "/sobre-nosotros#adrian")
    js = js.replace(SITE + "/editorial-policy", SITE + "/politica-editorial")
    js = js.replace(SITE + "/about", SITE + "/sobre-nosotros")
    js = js.replace('"url": "' + EN + '"', '"url": "' + SITE + '/"')
    js = js.replace(_EN_ORG_DESC, ORG_DESCRIPTION)
    js = js.replace('"inLanguage": ["en", "es"]', '"inLanguage": "es"')
    js = js.replace('"jobTitle": "Founder"', '"jobTitle": "Fundador"')
    js = js.replace(
        "Texas real estate sales agent license #675272-SA",
        "Licencia de agente de bienes raíces de Texas #675272-SA",
    )
    return js


def ga4_snippet():
    """Same measurement ID as cashhomeadvisors.com. US visits are measured. EU/UK stay opted out."""
    regions = (
        '["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU",'
        '"MT","NL","PL","PT","RO","SK","SI","ES","SE","IS","LI","NO","GB","CH"]'
    )
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',region:{regions}}});
gtag('js',new Date());
gtag('set',{{page_language:'es'}});
gtag('config',{json.dumps(GA4_ID)},{{page_location:location.href.replace(/([?&])ref=[^&#]*&?/,'$1').replace(/[?&](#|$)/,'$1'),allow_google_signals:false,allow_ad_personalization_signals:false}});
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a[href^="tel:"],a[href^="sms:"]');if(!a)return;
var w=a.closest('header,footer,.stickybar,.panel');
gtag('event',a.getAttribute('href').indexOf('tel:')===0?'click_to_call':'click_to_text',{{link_location:w?(w.classList[0]||w.tagName.toLowerCase()):'body'}});}},true);</script>"""


def port_shell(title, desc, path, en_url, main, extra_json, og_image, og_type, calc):
    url = SITE + path
    hreflang = (
        f'<link rel="alternate" hreflang="es" href="{url}">'
        f'<link rel="alternate" hreflang="en" href="{html.escape(en_url, quote=True)}">'
        f'<link rel="alternate" hreflang="x-default" href="{html.escape(en_url, quote=True)}">'
    )
    desk, drawer = nav()
    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1E398C">
<meta property="og:type" content="{html.escape(og_type)}">
<meta property="og:site_name" content="Compramos Casas TX">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{html.escape(og_image, quote=True)}">
<meta property="og:locale" content="es_US">
@@JSON@@
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Oswald:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/site-es.css">
{hreflang}
{ga4_snippet()}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="hdr">
 <div class="wrap">
  <a class="logo" href="/" aria-label="Inicio de Compramos Casas TX"><img src="/assets/logo-360.png" alt="Logotipo de Compramos Casas TX" width="720" height="433"></a>
  <nav class="mnav" aria-label="Principal">{desk}</nav>
  <div class="grow"></div>
  <a class="tel" href="tel:{TEL}"><b>{PHONE}</b><small><span lang="en">We speak English too</span></small></a>
  <a class="btn" href="/oferta">Obtenga su oferta</a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="mdrawer" aria-label="Menú"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
 </div>
 <div class="drawer" id="mdrawer" hidden>{drawer}<a class="btn" href="/oferta">Obtenga su oferta</a><a class="dcall" href="tel:{TEL}">{PHONE}</a></div>
</header>
<main id="main">
@@MAIN@@
</main>
@@FOOTER@@
@@CALC@@
</body>
</html>
"""
    return (
        page.replace("@@JSON@@", extra_json)
        .replace("@@MAIN@@", main)
        .replace("@@FOOTER@@", footer())
        .replace("@@CALC@@", calc)
    )


def port_spanish_pages():
    banned = ["el mejor", "número 1", "numero 1", "garantiz", "oficina local", "5709 vandalia", "grand prairie, tx 75052"]
    written = []
    for src in spanish_sources():
        raw = src.read_text(encoding="utf-8")
        title = html.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1)).strip()
        title = re.sub(r"\s*\|\s*Cash Home Advisors\s*$", " | Compramos Casas TX", title)
        desc_m = re.search(r'<meta name="description" content="([^"]*)"', raw)
        desc = html.unescape(desc_m.group(1)) if desc_m else ""
        main_m = re.search(r'<main id="main">(.*)</main>', raw, re.S)
        if not main_m:
            raise SystemExit(f"no main in {src}")
        main = main_m.group(1)
        main = main.replace('href="/compramos-casas-texas">Inicio', 'href="/">Inicio')
        main = main.replace("/assets/cha-logo-360.png", "/assets/logo-360.png")
        main = main.replace("/assets/cha-logo-900.png", "/assets/logo-900.png")
        fid = re.sub(r"[^a-z0-9]+", "-", rel_url(src).strip("/"))[:48] or "page"
        main = replace_lead_cards(main, fid)
        main = rewrite(main)
        blob = (title + " " + desc + " " + main).lower()
        for word in banned:
            if word in blob:
                raise SystemExit(f"banned copy in {src.name}: {word}")
        en = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)"', raw)
        en_url = en.group(1) if en else EN + "/"
        if en_url.startswith("/"):
            en_url = EN + en_url
        og_type_m = re.search(r'<meta property="og:type" content="([^"]+)"', raw)
        og_type = og_type_m.group(1) if og_type_m else "website"
        og_m = re.search(r'<meta property="og:image" content="([^"]+)"', raw)
        og = SITE + "/assets/logo-900.png"
        if og_m:
            og = og_m.group(1).split("?")[0].replace(EN, SITE)
            og = og.replace("/assets/cha-logo-360.png", "/assets/logo-360.png")
            og = og.replace("/assets/cha-logo-900.png", "/assets/logo-900.png")
        blocks = []
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
            blocks.append("<script type=\"application/ld+json\">" + rewrite_jsonld(block.strip()) + "</script>")
        calc = '<script src="/assets/calc.js"></script>' if "calc.js" in raw else ""
        path = rel_url(src)
        html_out = port_shell(title, desc, path, en_url, main, "\n".join(blocks), og, og_type, calc)
        dest = DOCS / src.relative_to(CHA / "docs")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html_out, encoding="utf-8")
        written.append(path)
    return written


def copy_media():
    src_assets = CHA / "docs/assets"
    dst_assets = DOCS / "assets"
    for sub in ("photos", "og"):
        src = src_assets / sub
        if not src.is_dir():
            continue
        dest = dst_assets / sub
        dest.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            if item.is_file():
                target = dest / item.name
                if not target.exists() or target.stat().st_size != item.stat().st_size:
                    shutil.copy2(item, target)
    calc = src_assets / "calc.js"
    if calc.exists():
        shutil.copy2(calc, dst_assets / "calc.js")
    head = src_assets / "adrian-luna-headshot.webp"
    if head.exists() and not (dst_assets / "adrian-luna-headshot.webp").exists():
        shutil.copy2(head, dst_assets / "adrian-luna-headshot.webp")


def check_internal_links():
    missing = []
    for path in DOCS.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'href="(/[^"]*)"', text):
            bare = href.split("#", 1)[0].split("?", 1)[0]
            if bare.startswith("/assets") or bare in ("/favicon.ico", "/", ""):
                continue
            rel = bare.lstrip("/")
            options = [DOCS / rel, DOCS / (rel + ".html"), DOCS / rel / "index.html"]
            if not any(opt.exists() for opt in options):
                missing.append((path.relative_to(DOCS).as_posix(), href))
    return missing


def extract_prose(path):
    raw = Path(path).read_text(encoding="utf-8")
    m = re.search(r'<div class="prose">(.*)</div>\s*(?:<section class="final"|</main>)', raw, re.S)
    if not m:
        raise SystemExit(f"no prose in {path}")
    return rewrite(m.group(1))


def load_landers():
    pages = []
    for path in sorted((CHA / "content/landers").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("lang") != "es":
            continue
        slug = data["slug"]
        pages.append({
            "slug": slug,
            "title": data["title"],
            "desc": data["meta_desc"],
            "h1": data["h1"],
            "sub": data.get("hero_sub") or "",
            "body": rewrite(data.get("body_html") or ""),
            "faq": data.get("faq") or [],
            "home": False,
        })
    offer = json.loads((CHA / "content/pages/how-cash-offers-are-calculated.json").read_text(encoding="utf-8"))["es"]
    pages.append({
        "slug": "como-se-calcula-una-oferta-en-efectivo",
        "title": "Cómo se calcula una oferta en efectivo",
        "desc": offer["meta_desc"],
        "h1": offer["h1"],
        "sub": offer.get("hero_sub") or "",
        "body": rewrite(offer["body_html"]),
        "faq": offer.get("faq") or [],
        "home": False,
    })
    return pages


def nav():
    def item(href, label):
        return f'<a href="{href}">{html.escape(label)}</a>'

    metros = "".join(item(h, l) for h, l in METROS)
    sits = "".join(item(h, l) for h, l in SITS)
    sits += item("/situaciones", "Todas las situaciones")
    process = (
        item("/como-funciona", "Cómo funciona")
        + item("/por-que-nosotros", "Por qué vendernos")
        + item("/formas-de-vender", "Formas de vender")
        + item("/oferta", "Reciba su oferta")
        + item("/preguntas-frecuentes", "Preguntas")
        + item("/como-se-calcula-una-oferta-en-efectivo", "Cómo se calcula la oferta")
        + item("/calculadora-ganancia-neta", "Anunciar o efectivo")
    )
    about = (
        item("/sobre-nosotros", "Sobre Adrian")
        + item("/resenas", "Opiniones")
        + item("/contacto", "Contacto")
        + item("/mayoristas", "Mayoristas")
    )
    blog = (
        item("/blog/es/category/selling", "Vender su casa")
        + item("/blog/es/category/foreclosure", "Embargo y deudas")
        + item("/blog/es/category/inherited", "Herencias y sucesiones")
        + item("/blog/es/category/squatters-vacant", "Ocupantes ilegales y casas vacías")
        + item("/blog/es/", "Todas las guías")
    )
    chev = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    desk = (
        f'<div class="dd"><a class="top" href="/zonas-donde-compramos">Dónde compramos{chev}</a><div class="menu">{metros}{item("/ciudades","Ciudades por área")}{item("/zonas-donde-compramos","Todas las áreas")}</div></div>'
        f'<div class="dd"><a class="top" href="/situaciones">Situaciones{chev}</a><div class="menu">{sits}</div></div>'
        f'<div class="dd"><a class="top" href="/como-funciona">Proceso{chev}</a><div class="menu">{process}</div></div>'
        f'<div class="dd"><a class="top" href="/blog/es/">Guías{chev}</a><div class="menu">{blog}</div></div>'
        f'<div class="dd"><a class="top" href="/sobre-nosotros">Nosotros{chev}</a><div class="menu">{about}</div></div>'
    )
    drawer = (
        f'<details><summary>Dónde compramos{chev}</summary><div>{metros}{item("/ciudades","Ciudades por área")}</div></details>'
        f'<details><summary>Situaciones{chev}</summary><div>{sits}</div></details>'
        f'<details><summary>Proceso{chev}</summary><div>{process}</div></details>'
        f'<details><summary>Guías{chev}</summary><div>{blog}</div></details>'
        f'<details><summary>Nosotros{chev}</summary><div>{about}</div></details>'
    )
    return desk, drawer


def footer():
    where = "".join(f"<li><a href=\"{h}\">{html.escape(l)}</a></li>" for h, l in METROS[:5])
    where += '<li><a href="/ciudades">Ciudades por área</a></li>'
    where += '<li><a href="/zonas-donde-compramos">Todas las áreas</a></li>'
    sits = "".join(f"<li><a href=\"{h}\">{html.escape(l)}</a></li>" for h, l in SITS)
    sits += '<li><a href="/situaciones">Todas las situaciones</a></li>'
    return f"""
<footer>
 <div class="wrap">
  <div class="fpills"><a href="tel:{TEL}">Llamar</a><a href="sms:{TEL}">Mensaje</a><a href="mailto:{EMAIL}">Correo</a></div>
  <div class="cols">
   <div class="fbrand">
    <img src="/assets/logo-360.png" alt="Logotipo de Compramos Casas TX" width="720" height="433">
    <p style="margin-top:12px">Compramos Casas TX</p>
    <a class="ftel" href="tel:{TEL}">{PHONE}</a>
    <p class="fhabla"><span lang="en">We speak English too</span></p>
   </div>
   <details class="fcol" open><summary><h4>Dónde compramos</h4></summary><ul>{where}</ul></details>
   <details class="fcol" open><summary><h4>Situaciones</h4></summary><ul>{sits}</ul></details>
   <details class="fcol" open><summary><h4>Empresa</h4></summary><ul>
     <li><a href="/sobre-nosotros">Nosotros</a></li>
     <li><a href="/como-funciona">Cómo funciona</a></li>
     <li><a href="/formas-de-vender">Formas de vender</a></li>
     <li><a href="/preguntas-frecuentes">Preguntas</a></li>
     <li><a href="/por-que-nosotros">Por qué nosotros</a></li>
     <li><a href="/resenas">Opiniones</a></li>
     <li><a href="/blog/es/">Guías</a></li>
     <li><a href="/contacto">Contacto</a></li>
     <li><a href="/mayoristas">Mayoristas</a></li>
     <li><a href="{EN}/">Sitio en inglés</a></li>
   </ul></details>
   <details class="fcol" open><summary><h4>Comuníquese</h4></summary><ul>
     <li><a href="/contacto">Contacto</a></li>
     <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><a href="https://www.facebook.com/Adrianbuyshomes/" rel="noopener">Facebook</a></li>
   </ul></details>
   <div class="flegal"><h4>Legal</h4><ul>
     <li><a href="/privacidad">Política de privacidad</a></li>
     <li><a href="/terminos-de-uso">Términos de uso</a></li>
     <li><a href="/terminos-sms">Términos de SMS</a></li>
   </ul></div>
  </div>
  <p class="disc trust">Quién está detrás de este sitio: Cash Home Advisors, LLC. <a href="/sobre-nosotros">Nosotros</a> · <a href="/politica-editorial">Cómo escribimos este sitio</a></p>
  <p class="disc">Adrian Luna es agente de bienes raíces con licencia en el Estado de Texas (TREC #675272-SA). Cash Home Advisors, LLC compra propiedades como principal y no actúa como su agente, prestamista ni asesor. Podemos comprar su casa nosotros mismos o con un inversionista socio, y le decimos cuál antes de que firme. Las ofertas son gratis y sin compromiso. Compramos Casas TX es el nombre en español de este sitio.</p>
 </div>
</footer>
<div class="stickybar">
 <a class="sb-call" href="tel:{TEL}">Llamar</a>
 <a class="sb-offer" href="/oferta">Obtenga su oferta</a>
</div>
<script src="/assets/site.js"></script>
"""


def form(fid):
    ES = es_dict()
    consent = rewrite(ES["form.consent"])
    pills_sit = "".join(
        f'<label class="pill"><input type="radio" name="situation" value="{v}"> {html.escape(lab)}</label>'
        for v, lab in [
            ("inherited", "Herencia / sucesión"),
            ("foreclosure", "Embargo / pagos atrasados"),
            ("divorce", "Divorcio"),
            ("landlord", "Casero cansado / renta"),
            ("repairs", "Necesita muchas reparaciones"),
            ("relocating", "Mudanza"),
            ("other", "Otra"),
        ]
    )
    pills_tl = "".join(
        f'<label class="pill"><input type="radio" name="timeline" value="{v}"> {html.escape(lab)}</label>'
        for v, lab in [
            ("asap", "Lo antes posible"),
            ("1-3mo", "1–3 meses"),
            ("3mo+", "3+ meses / flexible"),
            ("curious", "Solo quiero saber mi oferta"),
        ]
    )
    return f"""
<div class="card lead-card" id="offer-form-{fid}">
 <h3>Reciba su oferta gratis</h3>
 <p class="step-meta" aria-live="polite">Paso <b>1</b> de 3</p>
 <form class="lead" novalidate data-validate>
  <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-5000px" aria-hidden="true">
  <input type="hidden" name="form_version" value="cct1">
  <input type="hidden" name="cta_module" value="{fid}">
  <input type="hidden" name="brand" value="CCT">
  <fieldset class="step" data-step="1">
   <label for="addr-{fid}">Dirección de la propiedad</label>
   <input id="addr-{fid}" name="address" required autocomplete="street-address" placeholder="Calle, ciudad, TX">
   <div class="step-nav"><button class="btn" type="button" data-step-go="next">Obtenga su oferta</button></div>
  </fieldset>
  <fieldset class="step" data-step="2" hidden>
   <fieldset class="radio"><legend>¿La propiedad está listada con un agente?</legend>
    <label><input type="radio" name="listed_with_realtor" value="no" required> No</label>
    <label><input type="radio" name="listed_with_realtor" value="yes"> Sí</label>
   </fieldset>
   <fieldset class="pills"><legend>¿Cuál describe mejor su situación? (opcional)</legend><div class="opts">{pills_sit}</div></fieldset>
   <fieldset class="pills"><legend>¿Qué tan pronto quiere vender?</legend><div class="opts">{pills_tl}</div></fieldset>
   <div class="step-nav"><button class="linkbtn" type="button" data-step-go="back">Atrás</button><button class="btn" type="button" data-step-go="next">Siguiente</button></div>
  </fieldset>
  <fieldset class="step" data-step="3" hidden>
   <label for="name-{fid}">Su nombre</label>
   <input id="name-{fid}" name="name" required autocomplete="name">
   <label for="phone-{fid}">Número de teléfono</label>
   <input id="phone-{fid}" name="phone" type="tel" required autocomplete="tel">
   <label for="price-{fid}">¿Qué precio está buscando?</label>
   <input id="price-{fid}" name="asking_price" required autocomplete="off">
   <label for="email-{fid}">Correo electrónico (opcional)</label>
   <input id="email-{fid}" name="email" type="email" autocomplete="email">
   <div class="consent"><input type="checkbox" name="consent" required id="consent-{fid}">
    <label for="consent-{fid}" style="margin:0;font-weight:400">{consent}</label></div>
   <button class="btn" type="submit">Obtenga su oferta en efectivo</button>
   <div class="step-nav"><button class="linkbtn" type="button" data-step-go="back">Atrás</button></div>
  </fieldset>
 </form>
 <div class="panel ok hide" role="status"><h3>Recibido. Estamos revisando su propiedad.</h3><p>Le llamaremos o le enviaremos un texto pronto.</p><a class="btn" href="tel:{TEL}">Llame al {PHONE}</a></div>
 <div class="panel err hide" role="alert"><p>Algo salió mal al enviar su información. Llámenos directamente:</p><a class="btn" href="tel:{TEL}">Llame al {PHONE}</a></div>
</div>
"""


def schema(page, url):
    org = {
        "@type": "Organization",
        "@id": SITE + "/#business",
        "name": "Compramos Casas TX",
        "legalName": "Cash Home Advisors, LLC",
        "url": SITE + "/",
        "telephone": "+1-817-520-8319",
        "email": EMAIL,
        "description": ORG_DESCRIPTION,
        "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo-360.png"},
        "image": SITE + "/assets/logo-360.png",
        "founder": {"@id": SITE + "/sobre-nosotros#adrian"},
        "knowsLanguage": ["es", "en"],
        "areaServed": {"@type": "State", "name": "Texas"},
        "publishingPrinciples": SITE + "/politica-editorial",
        "sameAs": [
            EN + "/",
            "https://www.facebook.com/Adrianbuyshomes/",
            "https://www.yelp.com/biz/cash-home-advisors-kennedale",
        ],
    }
    web = {
        "@type": "WebSite",
        "@id": SITE + "/#website",
        "url": SITE + "/",
        "name": "Compramos Casas TX",
        "inLanguage": "es",
        "publisher": {"@id": SITE + "/#business"},
    }
    graph = [org, web]
    if page["slug"] == "sobre-nosotros":
        graph.append({
            "@type": "Person",
            "@id": SITE + "/sobre-nosotros#adrian",
            "name": "Adrian Luna",
            "jobTitle": "Fundador",
            "worksFor": {"@id": SITE + "/#business"},
            "knowsLanguage": ["es", "en"],
            "url": SITE + "/sobre-nosotros",
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "name": "Licencia de agente de bienes raíces de Texas #675272-SA",
                "identifier": "675272-SA",
                "credentialCategory": "Texas real estate sales agent license",
                "recognizedBy": {"@type": "Organization", "name": "Texas Real Estate Commission"},
            },
            "image": SITE + "/assets/adrian-luna-headshot.webp",
        })
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
        ],
    }
    if page.get("crumbs"):
        for i, (name, href) in enumerate(page["crumbs"], start=2):
            crumbs["itemListElement"].append({
                "@type": "ListItem", "position": i, "name": name, "item": SITE + href,
            })
    elif page["slug"]:
        crumbs["itemListElement"].append({
            "@type": "ListItem", "position": 2, "name": page["h1"], "item": url,
        })
    graph.append(crumbs)
    blocks = [json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)]
    if page.get("faq"):
        blocks.append(json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in page["faq"]
            ],
        }, ensure_ascii=False))
    return "\n".join(f'<script type="application/ld+json">{b}</script>' for b in blocks)


def faq_html(faqs):
    if not faqs:
        return ""
    rows = []
    for q in faqs:
        rows.append(
            "<details><summary>" + html.escape(q["q"])
            + '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary><p>'
            + html.escape(q["a"]) + "</p></details>"
        )
    return '<section class="alt" id="faq"><div class="wrap"><div class="kicker"><h2>Preguntas frecuentes</h2></div><div class="acc one">' + "".join(rows) + "</div></div></section>"


def page_html(page, desk, drawer):
    slug = page["slug"]
    path = "/" if not slug else f"/{slug}"
    url = SITE + path
    title = page["title"] if "|" in page["title"] else page["title"] + " | Compramos Casas TX"
    desc = page["desc"]
    if page.get("skip_hreflang"):
        hreflang = ""
    else:
        en_path = EN_TWIN.get(slug, "/")
        hreflang = (
            f'<link rel="alternate" hreflang="es" href="{url}">'
            f'<link rel="alternate" hreflang="en" href="{EN}{en_path}">'
            f'<link rel="alternate" hreflang="x-default" href="{EN}{en_path}">'
        )
    if page.get("home"):
        main = page["body"]
    else:
        sub = f"<p>{html.escape(page['sub'])}</p>" if page.get("sub") else ""
        main = f"""
<div class="lhero"><div class="wrap"><h1>{page['h1']}</h1>{sub}</div></div>
<div class="prose">{page['body']}</div>
{faq_html(page.get('faq'))}
<section class="final"><div class="wrap"><h2>Reciba su oferta en efectivo sin compromiso</h2>
<p>Gratis, sin compromiso. Una persona real le devuelve la llamada.</p>
{form('final')}
<a class="outpill" href="tel:{TEL}">{PHONE}</a>
</div></section>
"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#1E398C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Compramos Casas TX">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/logo-900.png">
<meta property="og:locale" content="es_US">
{schema(page, url)}
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Oswald:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/site-es.css">
{hreflang}
{ga4_snippet()}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="hdr">
 <div class="wrap">
  <a class="logo" href="/" aria-label="Inicio de Compramos Casas TX"><img src="/assets/logo-360.png" alt="Logotipo de Compramos Casas TX" width="720" height="433"></a>
  <nav class="mnav" aria-label="Principal">{desk}</nav>
  <div class="grow"></div>
  <a class="tel" href="tel:{TEL}"><b>{PHONE}</b><small><span lang="en">We speak English too</span></small></a>
  <a class="btn" href="/oferta">Obtenga su oferta</a>
  <button class="burger" type="button" aria-expanded="false" aria-controls="mdrawer" aria-label="Menú"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
 </div>
 <div class="drawer" id="mdrawer" hidden>{drawer}<a class="btn" href="/oferta">Obtenga su oferta</a><a class="dcall" href="tel:{TEL}">{PHONE}</a></div>
</header>
<main id="main">
{main}
</main>
{footer()}
</body>
</html>
"""


def extra_pages(ES):
    core_faq = [
        {"q": ES["faq.1q"], "a": ES["faq.1a"]},
        {"q": ES["faq.2q"], "a": ES["faq.2a"]},
        {"q": ES["faq.3q"], "a": ES["faq.3a"]},
        {"q": ES["faq.5q"], "a": ES["faq.5a"]},
        {"q": ES["faq.6q"], "a": ES["faq.6a"]},
        {"q": ES["faq.8q"], "a": ES["faq.8a"]},
    ]
    sits_list = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for h, l in SITS)
    metros_list = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for h, l in METROS)
    home_body = homepage_main(ES)
    home_faq = faqs_from_html(home_body) or core_faq
    pages = [{
        "slug": "",
        "title": "Compramos casas en Texas en efectivo | Compramos Casas TX",
        "desc": "Compramos Casas TX es el sitio en español de Cash Home Advisors, LLC. Compramos casas en Texas. Venda tal como está, sin reparaciones. Pagamos todos los gastos de cierre. Una persona real le devuelve la llamada.",
        "h1": "Venda su casa rápido por dinero en efectivo",
        "sub": "",
        "body": home_body,
        "faq": home_faq,
        "home": True,
    }, {
        "slug": "como-funciona",
        "title": "Cómo funciona",
        "desc": "Tres pasos para vender su casa en efectivo en Texas: la dirección, la oferta y el cierre en una compañía de títulos. Gratis y sin compromiso.",
        "h1": "Cómo funciona: tres pasos sencillos",
        "sub": "Gratis, sin compromiso. Esto es lo que pasa, desde su dirección hasta el día del cierre.",
        "body": """
<p>Compramos Casas TX es el sitio en español de Cash Home Advisors, LLC. El proceso es el mismo en español y en inglés.</p>
<ol>
<li><strong>Envíe su dirección.</strong> Revisamos ventas recientes, el estado de la casa y los gravámenes que aparezcan en el título.</li>
<li><strong>Reciba una oferta en efectivo.</strong> Una persona real le llama. La oferta es gratis y sin compromiso. Puede compararla, platicarla en familia y decir que no.</li>
<li><strong>Cierre y reciba su dinero.</strong> Si acepta, la firma es en una compañía de títulos de Texas, con un contrato estándar de la Texas Real Estate Commission (TREC). Podemos cerrar en 7 a 14 días una vez que el título esté limpio. Pagamos todos los gastos de cierre. La venta no depende de un préstamo bancario.</li>
</ol>
<p>Cash Home Advisors, LLC firma el contrato de compra con usted. Podemos comprar su casa nosotros mismos o con un inversionista socio, y le decimos cuál antes de que firme.</p>
<p>Si quiere ver de dónde sale el número, lea <a href="/como-se-calcula-una-oferta-en-efectivo">cómo se calcula una oferta en efectivo</a>.</p>
""",
        "faq": core_faq,
        "home": False,
    }, {
        "slug": "por-que-nosotros",
        "title": "Por qué vendernos",
        "desc": "Cash Home Advisors, LLC compra casas tal como están, en efectivo, y firma el contrato con usted. Cierre en 7 a 14 días. Pagamos todos los gastos de cierre.",
        "h1": "Por qué los vendedores eligen Cash Home Advisors",
        "sub": "Cash Home Advisors, LLC compra casas tal como están, en efectivo, y firma el contrato con usted.",
        "body": """
<ul>
<li>Cierre en 7 a 14 días, una vez que el título esté limpio.</li>
<li>Venda tal como está, sin reparaciones.</li>
<li>Pagamos todos los gastos de cierre.</li>
<li>Sin comisiones de agente en esta venta.</li>
<li>Gratis, sin compromiso.</li>
<li>Una persona real le devuelve la llamada. Puede hacer todo el trato en español.</li>
</ul>
<p>No decimos que seamos los más rápidos ni los que más pagan. La oferta es un número por escrito. Usted la compara con anunciar la casa o con otra oferta y decide.</p>
<p><a href="/formas-de-vender">Vea las tres formas de vender</a> una casa en Texas.</p>
""",
        "faq": core_faq,
        "home": False,
    }, {
        "slug": "formas-de-vender",
        "title": "Formas de vender su casa en Texas",
        "desc": "Tres formas de vender en Texas: anunciar con un agente, una oferta en línea o una venta en efectivo tal como está. Compare tiempo, reparaciones y gastos.",
        "h1": "Tres formas de vender su casa en Texas",
        "sub": "Cada opción le sirve a una casa y a un vendedor distinto.",
        "body": """
<h2>Anunciar con un agente</h2>
<p>Suele dejar más dinero si la casa está en buen estado y usted puede esperar. Usted se encarga de reparaciones, visitas, la comisión y la aprobación del préstamo del comprador. Adrian Luna es agente de bienes raíces con licencia en Texas (TREC #675272-SA). Listar la casa es una conversación distinta de la oferta en efectivo.</p>
<h2>Una oferta en línea de un iBuyer</h2>
<p>Algunas empresas dan un precio rápido para casas recientes y en buen estado. Las tarifas de servicio y los descuentos por reparaciones salen del precio después de la inspección. No es lo mismo que la oferta de Cash Home Advisors.</p>
<h2>Vender a un comprador en efectivo</h2>
<p>Venda tal como está, sin reparaciones. Sin comisiones de agente, y pagamos todos los gastos de cierre. Podemos cerrar en 7 a 14 días. La venta no depende de un préstamo bancario. El precio suele ser menor que el de una casa ya reparada y anunciada, porque el comprador resta el trabajo y el tiempo de volver a venderla. El cálculo está en <a href="/como-se-calcula-una-oferta-en-efectivo">cómo se calcula una oferta en efectivo</a>.</p>
""",
        "faq": core_faq,
        "home": False,
    }, {
        "slug": "preguntas-frecuentes",
        "title": "Preguntas frecuentes",
        "desc": "Respuestas sobre tiempos, gastos de cierre, reparaciones y quién compra la casa. Cash Home Advisors, LLC. Se habla español.",
        "h1": "Preguntas que nos hacen",
        "sub": "Respuestas claras sobre tiempos, gastos de cierre y situaciones difíciles.",
        "body": "<p>Si no ve la suya, llame o escriba al " + PHONE + ".</p>",
        "faq": core_faq + [
            {"q": ES["faq.7q"], "a": ES["faq.7a"]},
            {"q": "¿Compran en todo Texas?", "a": "Compramos en Dallas–Fort Worth, Houston, San Antonio, Austin y otras ciudades de Texas. Si su ciudad no tiene página, igual puede pedir la oferta."},
        ],
        "home": False,
    }, {
        "slug": "contacto",
        "title": "Contacto",
        "desc": "Llame o envíe un mensaje al (817) 520-8319, o escriba a adrian@cashhomeadvisors.com. Atendemos en español.",
        "h1": "Comuníquese con Cash Home Advisors",
        "sub": "Llame, envíe un mensaje o escriba. We speak English too.",
        "body": f"""
<p>Teléfono y mensaje: <a href="tel:{TEL}">{PHONE}</a></p>
<p>Correo: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Si ya tiene un contrato y es mayorista, use <a href="/mayoristas">la página de mayoristas</a>.</p>
""",
        "faq": [],
        "home": False,
    }, {
        "slug": "oferta",
        "title": "Reciba su oferta gratis en efectivo",
        "desc": "Pida una oferta en efectivo por su casa en Texas. Gratis, sin compromiso. Una persona real le devuelve la llamada.",
        "h1": "Reciba su oferta gratis en efectivo",
        "sub": "Gratis, sin compromiso. Una persona real le devuelve la llamada.",
        "body": form("oferta") + "<p>También puede llamar al <a href=\"tel:" + TEL + "\">" + PHONE + "</a>.</p>",
        "faq": core_faq[:4],
        "home": False,
    }, {
        "slug": "sobre-nosotros",
        "title": "Sobre Adrian y Cash Home Advisors",
        "desc": "Compramos Casas TX es el sitio en español de Cash Home Advisors, LLC. Adrian Luna es agente de bienes raíces con licencia en Texas, TREC #675272-SA.",
        "h1": "Sobre Adrian y Cash Home Advisors",
        "sub": "Con licencia en Texas. El sitio y las llamadas, en español.",
        "body": f"""
<p><img src="/assets/adrian-luna-headshot.webp" alt="Adrian Luna" width="320" height="320"></p>
<p>Compramos Casas TX es el nombre de este sitio. La empresa es Cash Home Advisors, LLC. Adrian Luna es el fundador y es agente de bienes raíces con licencia en el Estado de Texas (TREC #675272-SA).</p>
<p>En una venta en efectivo, Cash Home Advisors, LLC compra como principal. No actúa como su agente, prestamista ni asesor. Podemos comprar la casa nosotros mismos o con un inversionista socio, y le decimos cuál antes de que firme. Cada venta cierra en una compañía de títulos de Texas con un contrato estándar TREC.</p>
<p>Puede hacer la llamada, la oferta y las preguntas del cierre en español. También atendemos en inglés en <a href="{EN}/">cashhomeadvisors.com</a>.</p>
<p>Los comentarios de vendedores están en el perfil público de Google, no en esta página. Léalos en <a href="/resenas">Opiniones</a>.</p>
""",
        "faq": [{"q": ES["faq.8q"], "a": ES["faq.8a"]}],
        "home": False,
    }, {
        "slug": "situaciones",
        "title": "Situaciones en las que compramos casas",
        "desc": "Herencia, embargo, divorcio, reparaciones, inquilinos, terreno e impuestos atrasados. Compramos casas en Texas tal como están.",
        "h1": "Situaciones en las que ayudamos",
        "sub": "Herencia, pagos atrasados, divorcio o reparaciones: venda tal como está, en efectivo.",
        "body": f"<ul>{sits_list}</ul><p>Si su caso no está en la lista, pida la oferta igual. El formulario sirve para cualquier casa en Texas.</p>",
        "faq": [],
        "home": False,
    }, {
        "slug": "zonas",
        "title": "Dónde compramos casas en Texas",
        "desc": "Compramos casas en Dallas–Fort Worth, Houston, San Antonio, Austin y otras ciudades de Texas. Venda tal como está.",
        "h1": "Dónde compramos casas en Texas",
        "sub": "Dallas–Fort Worth, Houston, San Antonio y Austin. Si su ciudad no tiene página, igual puede pedir la oferta.",
        "body": f"""
<p>Cada zona de abajo explica las oficinas de ese condado: el distrito de tasación, la oficina de impuestos y dónde se registra la escritura. La oferta no cambia de idioma.</p>
<ul>{metros_list}</ul>
<p>Las ciudades de las 26 áreas metropolitanas están en <a href="/ciudades">ciudades por área</a>. Si su dirección está en Texas y no aparece, use <a href="/oferta">el formulario</a> o llame al {PHONE}.</p>
""",
        "faq": [{"q": "¿Compran fuera de estas ciudades?", "a": "Sí, en otras ciudades de Texas. Pida la oferta con la dirección y le decimos si podemos hacer esa compra."}],
        "home": False,
    }]
    # Legal pages already written in Spanish on the main site.
    for slug, src, title, desc, h1 in [
        ("privacidad", "privacidad.html", "Política de privacidad", "Política de privacidad de Cash Home Advisors, LLC.", "Política de privacidad"),
        ("terminos-de-uso", "terminos-de-uso.html", "Términos de uso", "Términos de uso de este sitio.", "Términos de uso"),
        ("terminos-sms", "terminos-sms.html", "Términos de SMS", "Términos de los mensajes de texto de Cash Home Advisors, LLC.", "Términos de SMS"),
    ]:
        pages.append({
            "slug": slug, "title": title, "desc": desc, "h1": h1, "sub": "",
            "body": extract_prose(CHA / "docs" / src), "faq": [], "home": False,
        })
    pages.append({
        "slug": "politica-editorial",
        "title": "Cómo escribimos este sitio",
        "desc": "Quién responde por Compramos Casas TX, cómo se usan herramientas de inteligencia artificial y cómo avisar de un error.",
        "h1": "Cómo escribimos este sitio",
        "sub": "Quién es responsable, cómo usamos herramientas de inteligencia artificial y cómo avisarnos de un error.",
        "body": """
<h2>Quién responde por este sitio</h2>
<p>Cash Home Advisors, LLC responde por todo lo que aparece en Compramos Casas TX. El fundador, Adrian Luna, es agente de bienes raíces con licencia en el Estado de Texas (TREC #675272-SA).</p>
<h2>Herramientas de inteligencia artificial</h2>
<p>Usamos herramientas de inteligencia artificial para ayudar a redactar, revisar y traducir páginas. Ninguna página se publica sin la aprobación de Adrian.</p>
<h2>Hechos y fuentes</h2>
<p>Cuando una guía explica una ley de Texas o un trámite del condado, enlaza la fuente oficial, como el estatuto, el condado o el juzgado, para que usted pueda comprobarlo.</p>
<p>Las guías explican reglas de Texas en lenguaje claro. No son consejo legal, de impuestos ni financiero. Para su caso, hable con un abogado de Texas o con un contador.</p>
<h2>Correcciones</h2>
<p>¿Vio algo mal o desactualizado? Llame o envíe un mensaje al <a href="tel:+18175208319">(817) 520-8319</a> o escriba a <a href="mailto:adrian@cashhomeadvisors.com">adrian@cashhomeadvisors.com</a>.</p>
""",
        "faq": [],
        "home": False,
    })
    pages += gap_pages()
    pages += [
        {
            "slug": "calculadora-costos-de-mantener",
            "title": "Costos de mantener una casa",
            "desc": "Qué se suma cada mes mientras una casa en Texas no se vende: hipoteca, impuestos, seguro, servicios y mantenimiento. Use sus propios números.",
            "h1": "Costos de mantener una casa",
            "sub": "Sume sus propios recibos. Esta página no guarda lo que usted escribe porque no hay formulario de cálculo.",
            "body": """
<p>Mientras la casa no se cierra, alguien paga cada mes la hipoteca, los impuestos prediales, el seguro, la luz, el agua, el gas, el césped y las reparaciones que no pueden esperar. En una venta anunciada esos meses salen de su bolsillo. En la oferta en efectivo, ese tiempo va dentro del precio que le damos, junto con el trabajo que la casa necesita.</p>
<p>Saque la cuenta con sus estados de cuenta. No publicamos un total de ejemplo porque el de su vecino no es el suyo. El orden de la oferta está en <a href="/como-se-calcula-una-oferta-en-efectivo">cómo se calcula una oferta en efectivo</a>.</p>
""",
            "faq": [],
            "home": False,
        },
        {
            "slug": "calculadora-ganancia-neta",
            "title": "Anunciar la casa o vender en efectivo",
            "desc": "Qué se resta en una venta anunciada y qué se resta en una venta en efectivo en Texas. Sin números inventados: use los suyos.",
            "h1": "Anunciar la casa o vender en efectivo",
            "sub": "Ponga sus propios números. Esta página no calcula una oferta.",
            "body": """
<p>Una venta anunciada suele restar comisiones, reparaciones, meses de hipoteca, impuestos, seguro y los gastos de cierre del vendedor. Una venta en efectivo con nosotros resta el trabajo y el tiempo dentro del precio de oferta: usted no paga comisión de agente y nosotros pagamos los gastos de cierre. El saldo de su préstamo, los gravámenes y su parte de los impuestos del año salen del precio al cerrar en los dos caminos.</p>
<p>No publicamos un precio de ejemplo porque cada casa es distinta. El orden del cálculo de la oferta en efectivo está en <a href="/como-se-calcula-una-oferta-en-efectivo">cómo se calcula una oferta</a>.</p>
""",
            "faq": [],
            "home": False,
        },
        {
            "slug": "mayoristas",
            "title": "Mayoristas",
            "desc": "Si tiene un contrato de compra en Texas y busca quien lo cierre, envíenos la dirección y los números. Una persona real le responde.",
            "h1": "Mayoristas: envíenos su contrato",
            "sub": "Dirección, precio del contrato y fecha de cierre. Le decimos si podemos seguir.",
            "body": form("mayoristas") + """
<p>En el formulario, ponga la dirección de la casa. En la llamada le pedimos el precio del contrato, la fecha de cierre y la tarifa de cesión. No prometa al vendedor un cierre que todavía no tenemos.</p>
""",
            "faq": [],
            "home": False,
        },
        {
            "slug": "gracias",
            "title": "Recibido",
            "desc": "Recibimos su dirección. Le llamaremos o le enviaremos un texto desde el (817) 520-8319.",
            "h1": "Recibido. Estamos revisando su propiedad.",
            "sub": "Le llamaremos o le enviaremos un texto pronto desde el (817) 520-8319.",
            "body": f'<p>Si prefiere no esperar, llame al <a href="tel:{TEL}">{PHONE}</a>.</p>',
            "faq": [],
            "home": False,
        },
        {
            "slug": "gracias-listada",
            "title": "Su casa está listada",
            "desc": "Si su casa ya está listada con un agente, igual podemos hablar. Hay reglas de la licencia que hay que respetar.",
            "h1": "Gracias. Su casa está listada con un agente.",
            "sub": "Así es como aún podemos ayudarle.",
            "body": """
<p>Si la casa ya está en el mercado con un agente, no le pedimos que rompa ese acuerdo. Llámenos y vemos si el agente puede presentar la oferta, o si conviene esperar a que el listado termine.</p>
<p>Teléfono: <a href="tel:+18175208319">(817) 520-8319</a>.</p>
""",
            "faq": [],
            "home": False,
        },
    ]
    return pages


def gap_pages():
    return [
        {
            "slug": "vender-casa-con-inquilinos-texas",
            "title": "Vender una casa con inquilinos en Texas",
            "desc": "Puede vender una casa rentada en Texas con el inquilino adentro. El contrato de renta y el depósito pasan con la casa. Compramos tal como está.",
            "h1": "Venda su casa en Texas con inquilinos adentro",
            "sub": "El inquilino no impide la venta. El contrato de renta y el depósito siguen la casa.",
            "body": """
<div class="summary"><b>Respuesta corta</b><p>Sí. Puede vender una casa de Texas con inquilinos. Tenga a la mano el contrato de renta, el registro de pagos y el depósito. Las visitas dependen de lo que diga ese contrato.</p></div>
<p>La venta cambia al casero, no el contrato de renta. El comprador queda obligado por el plazo que ya está firmado, salvo que el propio contrato diga que termina con la venta. La <a href="https://www.sll.texas.gov/faqs/landlord-tenant-property-sale/">biblioteca de leyes del estado</a> lo resume así.</p>
<h2>El depósito</h2>
<p>La <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.92.htm#92.105">sección 92.105 del Código de Propiedad</a> hace responsable al nuevo dueño por el depósito desde que recibe el título, y le pide entregar al inquilino un escrito con la cantidad exacta. Usted sigue responsable de los depósitos que cobró hasta que el nuevo dueño los reciba o asuma esa deuda. Confirme el texto vigente en el enlace.</p>
<h2>Avisos</h2>
<p>Con renta mensual, la <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.91.htm#91.001">sección 91.001</a> termina la tenencia en la fecha del aviso o un mes después, lo que sea más tarde, salvo un plazo distinto firmado por las dos partes. No aplica igual a un incumplimiento del contrato.</p>
<p>No hay una ley estatal única sobre entrar a la casa: manda el contrato. La <a href="https://www.sll.texas.gov/faqs/landlord-entry/">guía de la biblioteca de leyes</a> lo dice. Si el contrato no permite visitas de compradores, puede necesitar el permiso del inquilino. Un abogado le dice cómo aplicar eso a su contrato.</p>
<p>No cambie las cerraduras ni corte los servicios para sacar a alguien. La <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.92.htm#92.0081">sección 92.0081</a> prohíbe impedir la entrada salvo por un proceso judicial, con excepciones estrechas. La <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.92.htm#92.008">sección 92.008</a> prohíbe cortar servicios salvo reparaciones de verdad, obra o una emergencia.</p>
<p>Compramos la casa tal como está, con o sin inquilino. Pagamos todos los gastos de cierre. Una persona real le devuelve la llamada.</p>
""",
            "faq": [
                {"q": "¿Vender la casa termina el contrato del inquilino?", "a": "No. La venta cambia al casero, no el contrato, salvo que el contrato diga que termina con la venta."},
                {"q": "¿Quién devuelve el depósito?", "a": "La sección 92.105 del Código de Propiedad hace responsable al nuevo dueño desde que toma el título. Usted sigue responsable hasta que el nuevo dueño reciba el depósito o asuma esa deuda. Lea el estatuto y confírmelo con la compañía de títulos."},
                {"q": "¿Puedo cambiar las cerraduras para que se vaya?", "a": "No. La sección 92.0081 exige un proceso judicial, con excepciones estrechas. Cortar los servicios también está limitado por la sección 92.008."},
            ],
            "home": False,
        },
        {
            "slug": "vender-casa-por-mudanza-texas",
            "title": "Vender su casa en Texas por una mudanza de trabajo",
            "desc": "Si un trabajo nuevo tiene fecha de inicio, compare anunciar la casa, el programa de su empleador o una venta en efectivo. Compramos tal como está.",
            "h1": "Vender su casa en Texas porque se muda por trabajo",
            "sub": "El trabajo nuevo ya tiene fecha. Estas son las vías para la casa que deja.",
            "body": """
<div class="summary"><b>Respuesta corta</b><p>Puede anunciar la casa, usar el programa de venta de su empleador, rentarla o venderla en efectivo tal como está. Compare el número neto y la fecha en que tiene que estar en el otro trabajo.</p></div>
<p>Pida a recursos humanos el número del programa de recompra y la fecha límite por escrito. Compare ese número con un precio realista de anuncio, menos comisión, gastos de cierre y los meses que seguiría pagando la casa. Pregunte si puede anunciar primero y dejar el programa como respaldo.</p>
<p>Esta página no explica si el dinero de la mudanza paga impuestos. Pregunte a recursos humanos cómo lo van a reportar y a un contador cómo entra en su declaración.</p>
<p>Antes de irse, deje en la compañía de títulos su nueva dirección, un teléfono que sí contesta, el contacto para el saldo del préstamo, el contacto de la asociación de propietarios y un plan para las llaves. Confirme las instrucciones del transferencia llamando a un número que usted ya tenía, no a uno que llegó por correo.</p>
<p>Si el tiempo no da para reparar y anunciar, la venta en efectivo es la otra vía: tal como está, sin comisión de agente, y nosotros pagamos los gastos de cierre. Podemos cerrar en 7 a 14 días una vez que el título esté limpio. No depende de un préstamo bancario.</p>
""",
            "faq": [
                {"q": "¿Me conviene el programa de mi empleador o anunciar?", "a": "Compare el número del programa con un precio de anuncio menos comisión, gastos de cierre y los meses que cargaría la casa. Pida la fecha límite por escrito."},
                {"q": "¿El dinero de reubicación paga impuestos?", "a": "Esta página no cubre ese trato fiscal. Pregunte a recursos humanos cómo lo reportan y a un contador cómo entra en su declaración."},
            ],
            "home": False,
        },
        {
            "slug": "vender-casa-para-reducir-texas",
            "title": "Vender su casa en Texas para mudarse a algo más pequeño",
            "desc": "Si se muda a una casa más pequeña o más cerca de la familia, vea la exención de homestead, el tope escolar y la diferencia entre anunciar y vender en efectivo.",
            "h1": "Vender su casa en Texas para mudarse a algo más pequeño",
            "sub": "La venta, el tope de impuestos escolares y quién puede firmar si la casa ya está vacía.",
            "body": """
<div class="summary"><b>Respuesta corta</b><p>Puede anunciar la casa o venderla en efectivo tal como está. Si tiene exención de homestead o el tope de impuestos escolares por edad, avise al distrito de tasación cuando deje de vivir ahí. Un contador le explica la parte del IRS.</p></div>
<p>El <a href="https://comptroller.texas.gov/forms/50-114.pdf">formulario 50-114 del Contralor</a> pide al dueño avisar por escrito al tasador jefe antes del 1 de mayo del año siguiente a que se acaba el derecho a la exención. La <a href="https://statutes.capitol.texas.gov/Docs/TX/htm/TX.11.htm#11.13">sección 11.13 del Código de Impuestos</a> exige que la casa sea su residencia principal. Confirme el texto vigente.</p>
<p>La <a href="https://statutes.capitol.texas.gov/Docs/TX/htm/TX.11.htm#11.26">sección 11.26</a> trata el tope del impuesto escolar. Si la casa nueva va a un fideicomiso, la sección 11.26(f) dice que el tope no se acaba solo porque el dueño la pasa a un fideicomiso que califica bajo la sección 11.13(j), si el dueño o su cónyuge es el fideicomitente y puede vivir ahí. Si su fideicomiso califica es pregunta para el tasador o para un abogado.</p>
<p>Si un padre está en un asilo y la casa está vacía, la compañía de títulos decide quién firma. Si esa persona no puede firmar, pregunte a un abogado si un poder que ya existe alcanza, antes de pedir la oferta.</p>
<p>La publicación 523 del IRS habla de la exclusión por venta de vivienda. No es consejo de impuestos: un contador aplica esa publicación a su caso. El enlace está en <a href="https://www.irs.gov/publications/p523">irs.gov/publications/p523</a>.</p>
<p>Si no quiere reparar la casa grande antes de irse, la compramos tal como está. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días.</p>
""",
            "faq": [
                {"q": "¿Tengo que avisar al distrito de tasación cuando me mude?", "a": "Sí. El formulario 50-114 del Contralor pide un aviso por escrito antes del 1 de mayo del año siguiente a que se acaba el derecho a la exención de homestead."},
                {"q": "¿Quién firma si mi padre ya no vive en la casa?", "a": "La compañía de títulos busca al dueño o a quien tenga autoridad legal para firmar. Si no puede firmar, pregunte a un abogado si el poder que ya existe alcanza."},
            ],
            "home": False,
        },
        {
            "slug": "vender-casa-que-necesita-reparaciones-texas",
            "title": "Vender una casa que necesita reparaciones en Texas",
            "desc": "Techo, cimentación o avisos de código. Puede vender tal como está. La revelación del vendedor sigue aplicando. Pagamos todos los gastos de cierre.",
            "h1": "Venda en Texas una casa que necesita reparaciones",
            "sub": "Arreglarla, anunciarla tal como está o venderla en efectivo. Qué pide la revelación y el contrato TREC.",
            "body": """
<div class="summary"><b>Respuesta corta</b><p>Sí. Puede vender tal como está una casa que necesita reparaciones o trabajo de cimentación. Anunciarla igual exige revelar lo que usted sabe. En una venta en efectivo el trabajo va dentro del precio, y usted no lo paga antes.</p></div>
<p>Hay tres caminos. Arreglar y anunciar cuesta contratistas, permisos y los meses que la casa sigue a su cargo, y el inspector del comprador puede encontrar algo más. Anunciar tal como está evita la obra, pero menos compradores consiguen préstamo y el precio se vuelve a hablar después de la inspección. Vender en efectivo pone el costo de la obra dentro de la oferta.</p>
<p>La <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.5.htm">sección 5.008 del Código de Propiedad</a> pide la revelación del vendedor en la venta de una vivienda de no más de una unidad, con excepciones. El aviso pregunta lo que usted sabe, incluso defectos de cimentación. El formulario de la TREC está en <a href="https://www.trec.texas.gov/forms/sellers-disclosure-notice">trec.texas.gov</a>. No es una lista de todo lo que un ingeniero encontraría.</p>
<p>Un detalle barato que el visitante ve al entrar, como un grifo que gotea o un detector de humo sin pila, a veces conviene arreglarlo porque quita una objeción fácil. Las obras grandes espérelas hasta tener presupuestos por escrito y ver si se pagan solas.</p>
<p>Si hay un reclamo de seguro abierto, dígale al comprador del daño y del reclamo, y deje por escrito quién se queda con el dinero que la aseguradora todavía no paga. Un abogado de bienes raíces en Texas puede redactar esa frase. Pregunte al ajustador y al administrador del préstamo, antes de firmar, qué cambia la venta.</p>
<p>Compramos la casa tal como está, sin reparaciones. Pagamos todos los gastos de cierre. Sin comisiones de agente. Una persona real le devuelve la llamada.</p>
""",
            "faq": [
                {"q": "¿Tengo que reparar antes de vender?", "a": "No. Compramos casas tal como están, sin reparaciones. La revelación de lo que usted sabe sigue aplicando en una venta de vivienda."},
                {"q": "¿Un avalúo siempre ve el problema de cimentación?", "a": "No. La mirada del valuador es visual y limitada. La revelación del vendedor pregunta si usted conoce defectos en la cimentación o en la losa."},
                {"q": "¿Puedo vender con un reclamo de seguro abierto?", "a": "Se puede. Hay que decir el daño y el reclamo, y escribir quién se queda con el dinero que todavía no pagan. Un abogado y el ajustador le confirman el efecto de la venta."},
            ],
            "home": False,
        },
        {
            "slug": "compramos-casas-austin",
            "title": "Compramos casas en Austin, Texas",
            "desc": "Compramos casas en el área de Austin tal como están. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días. Condados de Travis, Williamson, Hays, Bastrop y Caldwell.",
            "h1": "Compramos casas en el área de Austin",
            "sub": "Travis, Williamson, Hays, Bastrop y Caldwell llevan sus propios registros. Venda tal como está. Pagamos todos los gastos de cierre.",
            "body": """
<p>Cash Home Advisors, LLC compra casas en el área de Austin y en el resto de Texas. Puede vender tal como está, sin reparaciones. Podemos cerrar en 7 a 14 días. Una persona real le devuelve la llamada, en español o en inglés.</p>
<p>El <a href="https://www.whitehouse.gov/wp-content/uploads/2023/07/OMB-Bulletin-23-01.pdf">boletín OMB 23-01</a> define el área metropolitana. Round Rock está en los condados de Travis y de Williamson, según el archivo de lugares por condado del Censo de 2020. El distrito del condado donde está la casa es el que la tasa. El directorio del Contralor lista <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/travis.php">Travis</a>, <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/williamson.php">Williamson</a>, <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/hays.php">Hays</a>, <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/bastrop.php">Bastrop</a> y <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/caldwell.php">Caldwell</a>.</p>
<p>El plazo usual para protestar el avalúo está en la <a href="https://statutes.capitol.texas.gov/Docs/TX/htm/TX.41.htm">sección 41.44 del Código de Impuestos</a>: el 15 de mayo o 30 días después de que le entreguen el aviso, lo que sea más tarde. Confirme el año en curso en el aviso que le llegó.</p>
<p>La revelación del vendedor de la <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.5.htm">sección 5.008</a> es la misma en Austin que en el resto del estado para una vivienda de una unidad. Hay transferencias exentas, como una orden del juez o una venta por embargo.</p>
""",
            "faq": [
                {"q": "¿Qué distrito tasa una casa en Round Rock?", "a": "Round Rock está en Travis y en Williamson. La tasa el distrito del condado donde está su casa. El aviso de avalúo trae el nombre."},
                {"q": "¿Cuándo vence la protesta del avalúo?", "a": "La sección 41.44 marca como plazo usual el 15 de mayo o 30 días después de la entrega del aviso, lo que sea más tarde."},
                {"q": "¿La revelación es distinta en Austin?", "a": "No. La sección 5.008 del Código de Propiedad aplica a viviendas de una unidad en todo Texas, con las excepciones que el mismo estatuto lista."},
            ],
            "home": False,
        },
        {
            "slug": "compramos-casas-san-antonio",
            "title": "Compramos casas en San Antonio, Texas",
            "desc": "Compramos casas en San Antonio y el área tal como están. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días. Oficinas de Bexar, Comal y Guadalupe.",
            "h1": "Compramos casas en el área de San Antonio",
            "sub": "San Antonio entra en los condados de Bexar, Comal y Medina. Venda tal como está. Pagamos todos los gastos de cierre.",
            "body": """
<p>Cash Home Advisors, LLC compra casas en San Antonio y en otras ciudades de Texas. Puede vender tal como está, sin reparaciones. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días.</p>
<p>New Braunfels está en los condados de Comal y de Guadalupe, según el archivo de lugares por condado del Censo de 2020. El distrito de Comal está en New Braunfels y el de Guadalupe en Seguin. Su aviso de avalúo nombra el que le toca. El directorio del Contralor: <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/bexar.php">Bexar</a>, <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/comal.php">Comal</a> y <a href="https://comptroller.texas.gov/taxes/property-tax/county-directory/guadalupe.php">Guadalupe</a>.</p>
<p>En un homestead, el cónyuge normalmente tiene que firmar. La <a href="https://statutes.capitol.texas.gov/Docs/FA/htm/FA.5.htm">sección 5.001 del Código de Familia</a> dice que ningún cónyuge puede vender el homestead sin la firma del otro, sea propiedad separada o de la sociedad, salvo lo que ese capítulo u otra ley permita.</p>
<p>La <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.5.htm">sección 5.008</a> no aplica a una transferencia hecha por un fiduciario al administrar la herencia de quien falleció. Un heredero que vende a su propio nombre es otro caso: la compañía de títulos le dice cuál es el suyo. La guía en español de declaración jurada de herencia del Juzgado de Sucesiones núm. 2 de Bexar está en el sitio del condado.</p>
<p>Las ventas por embargo en Texas son el primer martes del mes, entre las 10 a.m. y las 4 p.m., o el primer miércoles si ese martes es 1 de enero o 4 de julio, según la <a href="https://statutes.capitol.texas.gov/Docs/PR/htm/PR.51.htm">sección 51.002</a>. El aviso se presenta al secretario del condado al menos 21 días antes. Si esa fecha se le acerca, vea <a href="/evitar-embargo-vender-casa-texas">vender antes del embargo</a>.</p>
""",
            "faq": [
                {"q": "¿Qué distrito tasa una casa en New Braunfels?", "a": "New Braunfels está en Comal y en Guadalupe. El aviso de avalúo nombra el distrito de su casa."},
                {"q": "¿Mi cónyuge tiene que firmar la venta del homestead?", "a": "En general sí. La sección 5.001 del Código de Familia pide la firma de los dos cónyuges, con las excepciones de esa ley."},
                {"q": "¿Cuándo es la subasta de embargo en el condado de Bexar?", "a": "La sección 51.002 la pone el primer martes del mes, entre las 10 a.m. y las 4 p.m., con la regla del miércoles si ese martes es 1 de enero o 4 de julio."},
            ],
            "home": False,
        },
    ]


def write_site_js():
    js = r"""
(function(){
  var ENDPOINT = "%(endpoint)s";
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('mdrawer');
  if (burger && drawer) burger.addEventListener('click', function(){
    var open = drawer.hidden;
    drawer.hidden = !open;
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  function showStep(form, n){
    form.querySelectorAll('fieldset.step').forEach(function(fs){
      fs.hidden = fs.getAttribute('data-step') !== String(n);
    });
    form.setAttribute('data-step-active', String(n));
    var meta = form.parentElement.querySelector('.step-meta b');
    if (meta) meta.textContent = String(n);
  }
  document.querySelectorAll('form.lead').forEach(function(form){
    showStep(form, 1);
    form.addEventListener('click', function(ev){
      var btn = ev.target.closest('[data-step-go]');
      if (!btn) return;
      var cur = Number(form.getAttribute('data-step-active') || '1');
      if (btn.getAttribute('data-step-go') === 'back') { showStep(form, Math.max(1, cur-1)); return; }
      var fs = form.querySelector('fieldset.step[data-step="'+cur+'"]');
      var bad = false;
      fs.querySelectorAll('input[required]').forEach(function(inp){
        if (inp.type === 'radio') {
          var any = form.querySelector('input[name="'+inp.name+'"]:checked');
          if (!any) { bad = true; inp.reportValidity && inp.reportValidity(); }
        } else if (!inp.checkValidity()) { bad = true; inp.reportValidity(); }
      });
      if (bad) return;
      showStep(form, Math.min(3, cur+1));
    });
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      if (form.querySelector('[name=website]').value) return;
      var consent = form.querySelector('[name=consent]');
      if (consent && !consent.checked) { consent.focus(); return; }
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {brand:'CCT', source_page: location.pathname, language:'es',
        consent_ts: new Date().toISOString(), page_url: location.href.split('#')[0],
        page_title: document.title, referrer: document.referrer || ''};
      var vals = {};
      new FormData(form).forEach(function(v,k){
        if (k === 'website') return;
        (vals[k] = vals[k] || []).push(v);
      });
      Object.keys(vals).forEach(function(k){ data[k] = vals[k].filter(Boolean).join(', '); });
      var parts = String(data.name||'').trim().split(/\s+/);
      data.first_name = parts[0] || '';
      data.last_name = parts.slice(1).join(' ');
      data.lead_note = ['Compramos Casas TX lead (seller)',
        'CONSENT: '+(data.consent==='on'?'consent box checked, '+data.consent_ts:'not checked'),
        'Name: '+(data.name||''), 'Phone: '+(data.phone||''), 'Email: '+(data.email||''),
        'Property: '+(data.address||''),
        'Price they are looking for: '+(data.asking_price||''),
        'Listed: '+(data.listed_with_realtor||''),
        'Situation: '+(data.situation||''), 'Timeline: '+(data.timeline||''),
        'Page: '+data.page_url].join('\n');
      data.lead_note_html = data.lead_note.split('\n').map(function(line){
        return String(line).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
      }).join('<br>');
      var btn = form.querySelector('[type=submit]');
      if (btn) btn.disabled = true;
      fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)})
        .then(function(r){
          if (!r.ok) throw new Error('bad');
          var to = data.listed_with_realtor === 'yes' ? '/gracias-listada' : '/gracias';
          if (window.gtag) gtag('event','generate_lead',{lead_source:'web_form',listed:data.listed_with_realtor||'',page_language:'es'});
          location.href = to;
        })
        .catch(function(){
          if (btn) btn.disabled = false;
          form.classList.add('hide');
          var p = form.parentElement.querySelector('.panel.err');
          if (p) p.classList.remove('hide');
        });
    });
  });
})();
""" % {"endpoint": ENDPOINT}
    (DOCS / "assets/site.js").write_text(js, encoding="utf-8")


def write_css():
    extra = """
.hdr .wrap{height:84px}
.hdr .logo img{height:68px;width:auto}
footer .fbrand img{height:96px;width:auto}
.summary{background:#f4f7fb;border-radius:12px;padding:14px 16px;margin:0 0 18px}
.tags{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin:0}
.tags a{display:inline-block;background:#fff;border:1px solid #e6eaf4;border-radius:999px;padding:8px 14px;text-decoration:none;font-weight:700}
.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.home-offer-hero{position:relative}
.founder img[src$="logo-360.png"]{width:184px;height:auto;border-radius:0;background:none;object-fit:contain}
.city-index ul{columns:2;padding-left:1.2rem}
#datos-locales{border-top:1px solid #e6eaf4}
.entity-answer{margin:12px 0 0;max-width:70ch;font-size:1.05rem;line-height:1.55;font-weight:600;color:var(--ink)}
.entity-band{background:#f4f7fb;border-bottom:1px solid #e6eaf4}
.entity-band .wrap{padding-top:22px;padding-bottom:22px}
.entity-band .entity-answer{margin:0}
@media(max-width:700px){.city-index ul{columns:1}}
"""
    (DOCS / "assets/site-es.css").write_text(extra, encoding="utf-8")


CITY_JSON = Path("/Users/work/Claude/_cct_metro_build/ciudades.json")
DRAFT_ROOT = Path("/Users/work/Claude")
EXISTING_CITY_SLUGS = {
    "compramos-casas-dallas",
    "compramos-casas-fort-worth",
    "compramos-casas-houston",
    "compramos-casas-austin",
    "compramos-casas-san-antonio",
}
METRO_PAGES = {
    "Dallas-Fort Worth-Arlington, TX": [
        ("/compramos-casas-dallas", "Dallas"),
        ("/compramos-casas-fort-worth", "Fort Worth"),
    ],
    "Houston-Pasadena-The Woodlands, TX": [("/compramos-casas-houston", "Houston")],
    "Austin-Round Rock-San Marcos, TX": [("/compramos-casas-austin", "Austin")],
    "San Antonio-New Braunfels, TX": [("/compramos-casas-san-antonio", "San Antonio")],
}
KIND_CLAUSE = {
    "city": "Es una ciudad incorporada",
    "town": "Es un lugar incorporado que el Censo nombra como town",
    "village": "Es un lugar incorporado que el Censo nombra como village",
    "CDP": "Es un lugar designado por el Censo (CDP), no es una ciudad incorporada",
}
USTED_RE = re.compile(r"\b(tú|tu|puedes|llámanos|llamanos|contáctanos|contactanos)\b", re.I)


def _commas(n):
    return f"{int(n):,}"


def _county_plain(name):
    return name[:-7] if str(name).endswith(" County") else str(name)


def _metro_anchor(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _city_slug(city):
    folder = city["folder"]
    if not folder.startswith("compramoscasas-"):
        raise SystemExit(f"unexpected city folder {folder}")
    return "compramos-casas-" + folder[len("compramoscasas-"):]


def _load_cities():
    cities = json.loads(CITY_JSON.read_text(encoding="utf-8"))["cities"]
    if len(cities) != 726:
        raise SystemExit(f"expected 726 cities, got {len(cities)}")
    return cities


def _opening(city):
    name = city["name"]
    metro = city["metro"]
    if city["kind"] == "CDP":
        return (
            f"Cash Home Advisors, LLC compra casas en {name}. "
            f"{name} es ciudad principal de {metro}. "
            "Es un lugar designado por el Censo (CDP), no es una ciudad incorporada, "
            "y el archivo Vintage 2025 de lugares incorporados no publica su población. "
            "El archivo de lugares de 2020 lo ubica en los condados de Harris y de Montgomery. "
            "Harris figura como Central y Montgomery como Outlying en esa área. "
            "Venda tal como está, sin reparaciones. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días. "
            "Sin comisiones de agente. La oferta es gratis, sin compromiso, y una persona real le devuelve la llamada."
        )
    pop = _commas(city["pop_2025_07_01"])
    county = _county_plain(city["primary_county"])
    role = city["primary_role"]
    if city["principal"]:
        rank = f"{name} es ciudad principal de {metro}."
    else:
        rank = f"El boletín OMB 23-01 no nombra a {name} como ciudad principal de {metro}."
    return (
        f"Cash Home Advisors, LLC compra casas en {name}. "
        f"{KIND_CLAUSE[city['kind']]}. "
        f"La estimación del Censo al 1 de julio de 2025 es de {pop} habitantes. "
        f"La mayor parte de esa población está en el condado de {county}, que figura como {role} en {metro}. "
        f"{rank} "
        "Venda tal como está, sin reparaciones. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días. "
        "Sin comisiones de agente. La oferta es gratis, sin compromiso, y una persona real le devuelve la llamada."
    )


def _city_h1(city):
    name = city["name"]
    if city["kind"] == "CDP":
        return f"Venda su casa en {name}: ciudad principal, CDP en Harris y Montgomery"
    pop = _commas(city["pop_2025_07_01"])
    county = _county_plain(city["primary_county"])
    rank = "ciudad principal" if city["principal"] else "no es ciudad principal"
    return (
        f"Venda su casa en {name}: {pop} habitantes, {rank}, "
        f"figura como {city['primary_role']} en el condado de {county}"
    )


def _city_title(city):
    name = city["name"]
    if city["kind"] == "CDP":
        return (
            f"Compramos casas en {name}: ciudad principal, CDP en Harris y Montgomery | Compramos Casas TX"
        )
    pop = _commas(city["pop_2025_07_01"])
    county = _county_plain(city["primary_county"])
    rank = "ciudad principal" if city["principal"] else "no es ciudad principal"
    return (
        f"Compramos casas en {name}: {pop} habitantes, {rank}, "
        f"condado de {county} ({city['primary_role']}) | Compramos Casas TX"
    )


def _city_desc(city):
    if city["kind"] == "CDP":
        return (
            "Compramos casas en The Woodlands, ciudad principal de Houston-Pasadena-The Woodlands. "
            "El Censo lo ubica como CDP en los condados de Harris y de Montgomery. "
            "Venda tal como está, sin reparaciones."
        )
    pop = _commas(city["pop_2025_07_01"])
    county = _county_plain(city["primary_county"])
    rank = "Es ciudad principal" if city["principal"] else "No es ciudad principal"
    return (
        f"Compramos casas en {city['name']}, condado de {county}: {pop} habitantes al 1 de julio de 2025. "
        f"{rank}. El condado figura como {city['primary_role']} en {city['metro']}. "
        "Venda tal como está, sin reparaciones."
    )


def _extract_facts(city):
    path = DRAFT_ROOT / city["folder"] / "index.html"
    raw = path.read_text(encoding="utf-8")
    match = re.search(r'<section id="ciudad">\s*<div class="wrap">(.*?)</div>\s*</section>', raw, re.S)
    if not match:
        raise SystemExit(f"no city facts in {path}")
    inner = match.group(1)
    inner = re.sub(r"\s*<p class=\"eyebrow\">.*?</p>", "", inner, count=1, flags=re.S)
    inner = re.sub(r"\s*<h2>.*?</h2>", "", inner, count=1, flags=re.S)
    facts = inner.strip()
    if "noindex" in facts or "compramoscasas" in facts and "compramoscasastx.com" not in facts:
        raise SystemExit(f"draft boilerplate leaked into facts for {city['name']}")
    return facts


def _related_links(city, slug):
    anchor = _metro_anchor(city["metro"])
    links = [
        f'<a href="/ciudades#{anchor}">{html.escape(city["metro"])}</a>',
        '<a href="/compramos-casas-texas">todo Texas</a>',
        '<a href="/oferta">pedir una oferta</a>',
    ]
    for href, label in METRO_PAGES.get(city["metro"], []):
        if href != "/" + slug:
            links.append(f'<a href="{href}">{html.escape(label)}</a>')
    key = city["folder"][len("compramoscasas-"):]
    vender = f"vender-mi-casa-rapido-{key}-tx.html"
    if (DOCS / vender).exists() or (CHA / "docs" / vender).exists():
        links.append(
            f'<a href="/vender-mi-casa-rapido-{key}-tx">vender rápido en {html.escape(city["name"])}</a>'
        )
    return "<p>También: " + " · ".join(links) + ".</p>"


def _reject_city_copy(slug, blob):
    banned = [
        "el mejor", "número 1", "numero 1", "garantiz", "oficina local",
        "5709 vandalia", "grand prairie, tx 75052", "el más rápido", "la más rápida",
    ]
    low = blob.lower()
    found = [word for word in banned if word in low]
    if USTED_RE.search(low):
        found.append("usted")
    if found:
        raise SystemExit(f"banned city copy in {slug}: {found}")


def metro_city_pages():
    cities = _load_cities()
    new_pages = []
    existing = {}
    seen_title = {}
    seen_h1 = {}
    seen_open = {}
    groups = {}
    for city in cities:
        if city["kind"] != "CDP":
            if city.get("pop_2025_07_01") is None or not city.get("primary_county") or not city.get("primary_role"):
                raise SystemExit(f"incomplete city record for {city['name']}")
        slug = _city_slug(city)
        title = _city_title(city)
        h1 = _city_h1(city)
        opening = _opening(city)
        for label, value, seen in (
            ("title", title, seen_title),
            ("h1", h1, seen_h1),
            ("opening", opening, seen_open),
        ):
            if value in seen:
                raise SystemExit(f"duplicate {label} for {city['name']} and {seen[value]}")
            seen[value] = city["name"]
        facts = _extract_facts(city)
        _reject_city_copy(slug, title + "\n" + h1 + "\n" + opening + "\n" + facts)
        groups.setdefault(city["metro"], []).append(city)
        if slug in EXISTING_CITY_SLUGS:
            existing[slug] = city
            continue
        new_pages.append({
            "slug": slug,
            "title": title,
            "desc": _city_desc(city),
            "h1": h1,
            "sub": opening,
            "body": "<h2>La ciudad y el condado</h2>\n" + facts + "\n" + _related_links(city, slug),
            "faq": [],
            "home": False,
            "skip_hreflang": True,
            "crumbs": [("Ciudades", "/ciudades"), (city["name"], "/" + slug)],
        })
    if len(existing) != 5:
        raise SystemExit(f"expected 5 existing city pages, found {sorted(existing)}")
    hub_parts = [
        "<div class=\"city-index\">",
        "<p>Estas páginas cubren los lugares incorporados de las 26 áreas metropolitanas de Texas del boletín OMB 23-01, más The Woodlands. "
        "Cada una trae la población del Censo al 1 de julio de 2025 cuando el archivo la publica, el papel del condado en el área "
        "y la ficha del distrito de avalúo en el directorio del Contralor. "
        "Cash Home Advisors, LLC compra casas en Texas. Venda tal como está, sin reparaciones. "
        "Pagamos todos los gastos de cierre. Si no ve su ciudad, <a href=\"/oferta\">envíenos la dirección</a>.</p>",
    ]
    for metro in sorted(groups):
        rows = sorted(groups[metro], key=lambda row: row["name"])
        items = []
        for city in rows:
            slug = _city_slug(city)
            if city["kind"] == "CDP":
                detail = "CDP, ciudad principal, sin población de lugar incorporado"
            else:
                rank = "ciudad principal" if city["principal"] else "no es ciudad principal"
                detail = f"{_commas(city['pop_2025_07_01'])} habitantes, {rank}"
            items.append(
                f'<li><a href="/{slug}">{html.escape(city["name"])}</a> — {html.escape(detail)}</li>'
            )
        area = ""
        if metro in METRO_PAGES:
            area = "<p>Página del área: " + " · ".join(
                f'<a href="{href}">{html.escape(label)}</a>' for href, label in METRO_PAGES[metro]
            ) + ".</p>"
        hub_parts.append(
            f'<h2 id="{_metro_anchor(metro)}">{html.escape(metro)}</h2>{area}<ul>{"".join(items)}</ul>'
        )
    hub_parts.append("</div>")
    hub = {
        "slug": "ciudades",
        "title": "Ciudades de Texas donde compramos casas | Compramos Casas TX",
        "desc": "Índice de las ciudades incorporadas en las 26 áreas metropolitanas de Texas, más The Woodlands. Cada página trae la población al 1 de julio de 2025 y la ficha del condado.",
        "h1": "Ciudades de Texas donde compramos casas",
        "sub": "26 áreas metropolitanas del boletín OMB 23-01, más The Woodlands. Elija su ciudad.",
        "body": "\n".join(hub_parts),
        "faq": [],
        "home": False,
        "skip_hreflang": True,
        "crumbs": [("Ciudades", "/ciudades")],
    }
    _reject_city_copy("ciudades", hub["title"] + hub["desc"] + hub["h1"] + hub["sub"] + hub["body"])
    new_pages.append(hub)
    return new_pages, existing


def improve_existing_city_pages(existing):
    updated = 0
    for slug, city in existing.items():
        path = DOCS / f"{slug}.html"
        if not path.exists():
            raise SystemExit(f"missing existing city page {path}")
        text = path.read_text(encoding="utf-8")
        title = _city_title(city)
        h1 = _city_h1(city)
        desc = _city_desc(city)
        opening = _opening(city)
        facts = _extract_facts(city)
        text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", text, count=1, flags=re.S)
        text = re.sub(
            r'(<meta name="description" content=")[^"]*"',
            lambda m, value=html.escape(desc, quote=True): m.group(1) + value + '"',
            text,
            count=1,
        )
        text = re.sub(
            r'(<meta property="og:title" content=")[^"]*"',
            lambda m, value=html.escape(title, quote=True): m.group(1) + value + '"',
            text,
            count=1,
        )
        text = re.sub(
            r'(<meta property="og:description" content=")[^"]*"',
            lambda m, value=html.escape(desc, quote=True): m.group(1) + value + '"',
            text,
            count=1,
        )
        text = re.sub(r"<h1>.*?</h1>", f"<h1>{html.escape(h1)}</h1>", text, count=1, flags=re.S)
        if 'class="local-open"' not in text:
            text = text.replace("</h1>", "</h1>" + f'<p class="local-open">{html.escape(opening)}</p>', 1)
        if 'id="datos-locales"' not in text:
            block = (
                '<section id="datos-locales"><div class="wrap"><h2>La ciudad y el condado</h2>\n'
                + facts
                + "\n"
                + _related_links(city, slug)
                + "</div></section>\n"
            )
            if "</main>" not in text:
                raise SystemExit(f"no main in {slug}")
            text = text.replace("</main>", block + "</main>", 1)
        if f"<title>{html.escape(title)}</title>" not in text:
            raise SystemExit(f"title was not updated for {slug}")
        if city["kind"] != "CDP" and _commas(city["pop_2025_07_01"]) not in text:
            raise SystemExit(f"population missing after update of {slug}")
        path.write_text(text, encoding="utf-8")
        updated += 1
    return updated


def link_area_city_spans():
    cities = _load_cities()
    counts = {}
    name_to_href = {}
    for city in cities:
        counts[city["name"]] = counts.get(city["name"], 0) + 1
    for city in cities:
        if counts[city["name"]] == 1:
            name_to_href[city["name"]] = "/" + _city_slug(city)
    path = DOCS / "zonas-donde-compramos.html"
    text = path.read_text(encoding="utf-8")
    before = text.count('<span class="city"')

    def repl(match):
        name = re.sub(r"\s+", " ", match.group(2)).strip()
        href = name_to_href.get(name)
        if not href:
            return match.group(0)
        return f'<a class="city" href="{href}">{match.group(1)}{match.group(2)}</a>'

    text = re.sub(r'<span class="city">(<svg.*?</svg>)([^<]*)</span>', repl, text, flags=re.S)
    note = "Una ciudad sin enlace todavía no tiene su propia página. Igual puede enviarnos la dirección."
    if note not in text:
        raise SystemExit("areas page note missing")
    text = text.replace(
        note,
        'El índice de ciudades por área metropolitana está en <a href="/ciudades">ciudades de Texas</a>. Si su ciudad no aparece, envíenos la dirección.',
    )
    linked = before - text.count('<span class="city"')
    if before and linked == 0:
        raise SystemExit("no area city spans were linked")
    path.write_text(text, encoding="utf-8")
    return linked


def assert_indexable_city_pages(slugs):
    bad = []
    for slug in slugs:
        text = (DOCS / f"{slug}.html").read_text(encoding="utf-8")
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        expected = f"{SITE}/{slug}"
        if not canon or canon.group(1) != expected:
            bad.append((slug, "canonical", None if not canon else canon.group(1)))
        if "noindex" in text:
            bad.append((slug, "noindex"))
        if 'name="brand" value="CCT"' not in text:
            bad.append((slug, "form"))
        if "data-lang-switch" in text or ">ES<" in text or ">EN<" in text:
            bad.append((slug, "language-switch"))
    if bad:
        raise SystemExit("city page check failed: " + repr(bad[:12]))


def lint(pages):
    banned = ["el mejor", "número 1", "numero 1", "garantiz", "oficina local", "5709 vandalia", "grand prairie, tx 75052"]
    bad = []
    checked = list(pages) + [{
        "slug": "quien-compra",
        "title": "",
        "desc": "",
        "h1": "",
        "sub": "",
        "body": ENTITY_ANSWER,
        "faq": [],
    }]
    for page in checked:
        blob = (
            page["title"] + page["desc"] + page["h1"] + (page.get("sub") or "") + page["body"]
            + " ".join(q["a"] for q in page.get("faq") or [])
        ).lower()
        for word in banned:
            if word in blob:
                bad.append((page["slug"] or "/", word))
    if USTED_RE.search(ENTITY_ANSWER.lower()):
        bad.append(("quien-compra", "informal-tu"))
    claims = [
        "Cierre en 7 a 14 días",
        "Pagamos todos los gastos de cierre",
        "Venda tal como está, sin reparaciones",
        "Sin comisiones de agente",
        "Gratis, sin compromiso",
        "Una persona real le devuelve la llamada",
    ]
    for claim in claims:
        if claim not in ENTITY_ANSWER:
            bad.append(("quien-compra", "missing-claim:" + claim))
    if bad:
        raise SystemExit("banned copy: " + repr(bad))


def _section_end(fragment, start):
    depth = 0
    for match in re.finditer(r"</?section\b[^>]*>", fragment[start:], re.I):
        if match.group(0).lower().startswith("</"):
            depth -= 1
            if depth == 0:
                return start + match.end()
        else:
            depth += 1
    return None


def insert_entity_answer(fragment):
    if 'id="quien-compra"' in fragment:
        return fragment
    paragraph = '<p class="entity-answer">' + ENTITY_ANSWER + "</p>"
    hero = re.search(r'<section class="hero\b', fragment)
    if hero:
        end = _section_end(fragment, hero.start())
        if end:
            band = '<section class="entity-band" id="quien-compra"><div class="wrap">' + paragraph + "</div></section>"
            return fragment[:end] + band + fragment[end:]
    h1 = re.search(r"</h1>", fragment, re.I)
    if h1:
        return fragment[:h1.end()] + paragraph.replace(
            '<p class="entity-answer">',
            '<p class="entity-answer" id="quien-compra">',
            1,
        ) + fragment[h1.end():]
    return '<section class="entity-band" id="quien-compra"><div class="wrap">' + paragraph + "</div></section>" + fragment


def stamp_quote_pages():
    """Put the same quotable facts on the pages a Spanish answer would cite."""
    for rel in QUOTE_PAGES:
        path = DOCS / rel
        if not path.exists():
            raise SystemExit(f"quote page missing: {rel}")
        text = path.read_text(encoding="utf-8")
        match = re.search(r'(<main id="main">)(.*)(</main>)', text, re.S)
        if not match:
            raise SystemExit(f"no main in {rel}")
        main = insert_entity_answer(match.group(2))
        if 'id="quien-compra"' not in main:
            raise SystemExit(f"entity answer was not inserted in {rel}")
        path.write_text(text[:match.start(2)] + main + text[match.end(2):], encoding="utf-8")


def lint_built_quotes():
    banned = [
        "el mejor", "número 1", "numero 1", "garantiz", "oficina local",
        "5709 vandalia", "grand prairie, tx 75052", "localbusiness",
        "aggregaterating", "the best", "fastest",
    ]
    claims = [
        "Cierre en 7 a 14 días",
        "Pagamos todos los gastos de cierre",
        "Venda tal como está, sin reparaciones",
        "Sin comisiones de agente",
        "Gratis, sin compromiso",
        "Una persona real le devuelve la llamada",
        "Cash Home Advisors, LLC",
        "sitio en español",
        "Texas",
        "TREC #675272-SA",
    ]
    for rel in QUOTE_PAGES:
        text = (DOCS / rel).read_text(encoding="utf-8")
        found = re.search(
            r'<p class="entity-answer"[^>]*>(.*?)</p>',
            text,
            re.S,
        )
        if not found:
            raise SystemExit(f"claims lint: no entity paragraph in {rel}")
        paragraph = re.sub(r"<[^>]+>", "", found.group(1))
        low = paragraph.lower()
        for word in banned:
            if word in low:
                raise SystemExit(f"claims lint: {rel} entity has '{word}'")
        if USTED_RE.search(low):
            raise SystemExit(f"claims lint: {rel} entity uses informal address")
        for claim in claims:
            if claim not in paragraph:
                raise SystemExit(f"claims lint: {rel} missing {claim}")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            if "LocalBusiness" in block or "AggregateRating" in block or '"@type": "Review"' in block:
                raise SystemExit(f"claims lint: rating or local business schema in {rel}")
            if "buys houses for cash" in block or '"url": "' + EN + '"' in block:
                raise SystemExit(f"claims lint: English organization facts still in {rel}")
            if "/about#adrian" in block or "/editorial-policy" in block:
                raise SystemExit(f"claims lint: English entity URL still in {rel}")
    home = (DOCS / "index.html").read_text(encoding="utf-8")
    faq = re.search(r'"@type": "FAQPage".*?</script>', home, re.S)
    if not faq:
        raise SystemExit("claims lint: homepage FAQ schema missing")
    questions = re.findall(r'"name": "(.*?)"', faq.group(0))
    if not questions or not questions[0].startswith("¿") or "Riesgo de embargoRiesgo" in questions[0]:
        raise SystemExit("claims lint: homepage FAQ schema is not a real question: " + repr(questions[:1]))
    llms = (DOCS / "llms.txt").read_text(encoding="utf-8")
    if llms.count("\n- https://") > 12:
        raise SystemExit("claims lint: llms.txt still lists too many URLs")
    for claim in claims[:6]:
        if claim not in llms:
            raise SystemExit("claims lint: llms.txt missing " + claim)
    for _label, url in LLMS_LINKS:
        if url not in llms:
            raise SystemExit("claims lint: llms.txt missing " + url)
    robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
    for bot in ("Googlebot", "Google-Extended", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot"):
        if f"User-agent: {bot}" not in robots or "Disallow" in robots:
            raise SystemExit(f"claims lint: robots.txt does not allow {bot}")
    print("claims lint ok")


def write_llms():
    # A short summary for AI crawlers. llms.txt is not a Google ranking file.
    lines = [
        "# Compramos Casas TX",
        "",
        "> " + ORG_DESCRIPTION,
        "",
        "Empresa legal: Cash Home Advisors, LLC",
        "Sitio: " + SITE + "/",
        "Idioma: español",
        "Sitio en inglés: " + EN + "/",
        "Teléfono: " + PHONE,
        "Correo: " + EMAIL,
        "Licencia: Adrian Luna, agente de bienes raíces de Texas, TREC #675272-SA",
        "Área: Texas",
        "",
        "Afirmaciones:",
        "- Cierre en 7 a 14 días",
        "- Pagamos todos los gastos de cierre",
        "- Venda tal como está, sin reparaciones",
        "- Sin comisiones de agente",
        "- Gratis, sin compromiso",
        "- Una persona real le devuelve la llamada",
        "",
        "En una compra en efectivo, Cash Home Advisors, LLC compra como principal. "
        "No actúa como el agente del vendedor. Puede comprar sola o con un inversionista socio, "
        "y le dice cuál antes de la firma. El cierre es en una compañía de títulos de Texas.",
        "",
        "## Páginas principales",
    ]
    for label, url in LLMS_LINKS:
        lines.append(f"- {label}: {url}")
    lines.extend(["", "Índice completo: " + SITE + "/sitemap.xml", ""])
    (DOCS / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def write_robots():
    bots = (
        "*",
        "Googlebot",
        "Google-Extended",
        "Bingbot",
        "GPTBot",
        "OAI-SearchBot",
        "ChatGPT-User",
        "PerplexityBot",
    )
    groups = [f"User-agent: {bot}\nAllow: /\n" for bot in bots]
    text = "\n".join(groups) + "\nSitemap: " + SITE + "/sitemap.xml\n"
    (DOCS / "robots.txt").write_text(text, encoding="utf-8")


def main():
    prepare_maps()
    ES = es_dict()
    pages = extra_pages(ES)
    have = {p["slug"] for p in pages}
    for page in load_landers():
        if page["slug"] in have:
            continue
        pages.append(page)
        have.add(page["slug"])
    city_pages, existing_cities = metro_city_pages()
    for page in city_pages:
        if page["slug"] in have:
            raise SystemExit(f"city slug collides with an existing page: {page['slug']}")
        pages.append(page)
        have.add(page["slug"])
    lint(pages)
    desk, drawer = nav()
    write_site_js()
    write_css()
    ported_rels = {p.relative_to(CHA / "docs").as_posix() for p in spanish_sources()}
    skip_slugs = {"zonas", "opiniones"}
    for page in pages:
        slug = page["slug"]
        if slug in skip_slugs:
            continue
        name = "index.html" if not slug else slug + ".html"
        if name in ported_rels:
            continue
        (DOCS / name).write_text(page_html(page, desk, drawer), encoding="utf-8")
    ported = port_spanish_pages()
    copy_media()
    for stale in ("zonas.html", "opiniones.html"):
        stale_path = DOCS / stale
        if stale_path.exists():
            stale_path.unlink()
    updated_cities = improve_existing_city_pages(existing_cities)
    linked_spans = link_area_city_spans()
    assert_indexable_city_pages([page["slug"] for page in city_pages] + list(existing_cities))
    not_found = page_html({
        "slug": "404",
        "title": "Página no encontrada",
        "desc": "Esa página no está en Compramos Casas TX.",
        "h1": "Página no encontrada",
        "sub": "Pruebe el inicio o pida la oferta.",
        "body": '<p><a class="btn" href="/">Ir al inicio</a> <a class="btn" href="/oferta">Pedir una oferta</a></p>',
        "faq": [],
        "home": False,
    }, desk, drawer).replace('content="index, follow', 'content="noindex')
    (DOCS / "404.html").write_text(not_found, encoding="utf-8")
    (DOCS / "CNAME").write_text("www.compramoscasastx.com\n", encoding="utf-8")
    write_robots()
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    urls = []
    for path in sorted(DOCS.rglob("*.html")):
        if path.name == "404.html":
            continue
        rel = path.relative_to(DOCS)
        if rel.name == "index.html":
            parent = rel.parent.as_posix()
            urls.append(SITE + "/" if parent == "." else SITE + "/" + parent + "/")
        else:
            urls.append(SITE + "/" + rel.with_suffix("").as_posix())
    missing = check_internal_links()
    if missing:
        raise SystemExit("missing internal links: " + repr(missing[:30]) + f" count={len(missing)}")
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        body.append(f"<url><loc>{url}</loc></url>")
    body.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")
    write_llms()
    stamp_quote_pages()
    lint_built_quotes()
    print(
        f"ported {len(ported)} sitemap {len(urls)} "
        f"new_urls {len(city_pages)} updated_city_pages {updated_cities} area_spans_linked {linked_spans}"
    )


if __name__ == "__main__":
    main()
