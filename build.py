#!/usr/bin/env python3
"""Build the Spanish Compramos Casas TX site into docs/ for GitHub Pages."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
CHA = Path("/Users/work/Downloads/CHA_Website")
SITE = "https://www.compramoscasastx.com"
EN = "https://www.cashhomeadvisors.com"
PHONE = "(817) 520-8319"
TEL = "+18175208319"
EMAIL = "adrian@cashhomeadvisors.com"
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
    "/reviews": "/opiniones",
    "/resenas": "/opiniones",
    "/wholesalers": "/mayoristas",
    "/we-buy-houses-dallas": "/compramos-casas-dallas",
    "/we-buy-houses-fort-worth": "/compramos-casas-fort-worth",
    "/we-buy-houses-houston": "/compramos-casas-houston",
    "/we-buy-houses-austin": "/compramos-casas-austin",
    "/we-buy-houses-san-antonio": "/compramos-casas-san-antonio",
    "/we-buy-houses-texas": "/compramos-casas-texas",
    "/we-buy-houses-dfw": "/zonas",
    "/we-buy-houses": "/situaciones",
    "/areas-we-serve": "/zonas",
    "/sell-house-with-tenants-texas": "/vender-casa-con-inquilinos-texas",
    "/sell-house-job-relocation-texas": "/vender-casa-por-mudanza-texas",
    "/sell-house-to-downsize-texas": "/vender-casa-para-reducir-texas",
    "/sell-house-needing-repairs-texas": "/vender-casa-que-necesita-reparaciones-texas",
    "/blog/es/vender-casa-tal-como-esta-texas": "/vender-casa-que-necesita-reparaciones-texas",
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
    "opiniones": "/reviews",
    "mayoristas": "/wholesalers",
    "situaciones": "/we-buy-houses",
    "zonas": "/areas-we-serve",
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


def es_dict():
    text = (CHA / "docs/assets/site.js").read_text(encoding="utf-8")
    i = text.find("var ES=")
    obj, _ = json.JSONDecoder().raw_decode(text[i + 7 :])
    return obj


def rewrite(fragment):
    fragment = fragment.replace('href="/get-offer#es"', 'href="/oferta"')
    for old, new in sorted(PATHS.items(), key=lambda kv: -len(kv[0])):
        fragment = fragment.replace(f'href="{old}#es"', f'href="{new}"')
        fragment = fragment.replace(f'href="{old}"', f'href="{new}"')
        fragment = fragment.replace(f'href="{old}#', f'href="{new}#')
    fragment = re.sub(r'href="/vender-mi-casa-rapido-[^"]*"', 'href="/compramos-casas-texas"', fragment)
    fragment = re.sub(r'href="(/blog/[^"]*)"', r'href="https://www.cashhomeadvisors.com\1"', fragment)
    fragment = fragment.replace(
        'href="/assets/checklists/',
        'href="https://www.cashhomeadvisors.com/assets/checklists/',
    )
    fragment = re.sub(r'\sdata-i18n(?:-alt|-al|-ph)?="[^"]*"', '', fragment)
    return fragment


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
        if slug == "resenas":
            slug = "opiniones"
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
        + item("/opiniones", "Opiniones")
        + item("/contacto", "Contacto")
        + item("/mayoristas", "Mayoristas")
    )
    chev = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
    desk = (
        f'<div class="dd"><a class="top" href="/zonas">Dónde compramos{chev}</a><div class="menu">{metros}{item("/zonas","Todas las áreas")}</div></div>'
        f'<div class="dd"><a class="top" href="/situaciones">Situaciones{chev}</a><div class="menu">{sits}</div></div>'
        f'<div class="dd"><a class="top" href="/como-funciona">Proceso{chev}</a><div class="menu">{process}</div></div>'
        f'<div class="dd"><a class="top" href="/sobre-nosotros">Nosotros{chev}</a><div class="menu">{about}</div></div>'
    )
    drawer = (
        f'<details><summary>Dónde compramos{chev}</summary><div>{metros}</div></details>'
        f'<details><summary>Situaciones{chev}</summary><div>{sits}</div></details>'
        f'<details><summary>Proceso{chev}</summary><div>{process}</div></details>'
        f'<details><summary>Nosotros{chev}</summary><div>{about}</div></details>'
    )
    return desk, drawer


def footer():
    where = "".join(f"<li><a href=\"{h}\">{html.escape(l)}</a></li>" for h, l in METROS[:5])
    where += '<li><a href="/zonas">Todas las áreas</a></li>'
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
     <li><a href="/opiniones">Opiniones</a></li>
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
        "description": "Compramos Casas TX es el sitio en español de Cash Home Advisors, LLC. Compramos casas en Texas tal como están. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días.",
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
    if page["slug"]:
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
    en_path = EN_TWIN.get(slug, "/")
    title = page["title"] if "|" in page["title"] else page["title"] + " | Compramos Casas TX"
    desc = page["desc"]
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
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="hdr">
 <div class="wrap">
  <a class="logo" href="/" aria-label="Inicio de Compramos Casas TX"><img src="/assets/logo-360.png" alt="Logotipo de Compramos Casas TX" width="720" height="433"></a>
  <nav class="mnav" aria-label="Principal">{desk}</nav>
  <div class="grow"></div>
  <a class="tel" href="tel:{TEL}"><b>{PHONE}</b><small><span lang="en">We speak English too</span></small></a>
  <div class="langlink" aria-label="Idioma"><span class="on" aria-current="page">ES</span><a href="{EN}{en_path}" hreflang="en">EN</a></div>
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
    home_body = f"""
<section class="hero home-offer-hero" id="hero">
 <picture><source media="(max-width: 640px)" srcset="/assets/photos/moving-day-640.jpg"><img class="hero-img" src="/assets/photos/moving-day.jpg" width="1152" height="864" alt="Cajas de mudanza y una planta junto a una puerta principal abierta"></picture>
 <div class="wrap"><div class="proof-national-card">
  <h1>Venda su casa rápido por dinero en efectivo</h1>
  <ul class="proof-national-points">
   <li>Venda tal como está, sin reparaciones</li>
   <li>Sin comisiones de agente</li>
   <li>Pagamos todos los gastos de cierre</li>
  </ul>
  {form('hero')}
 </div></div>
</section>
<div class="claimsbar"><div class="wrap"><ul>
 <li>Cierre en 7 a 14 días</li>
 <li>Pagamos todos los gastos de cierre</li>
 <li>Venda tal como está, sin reparaciones</li>
 <li>Sin comisiones de agente</li>
</ul></div></div>
<section id="why"><div class="why-photo" aria-hidden="true"><img src="/assets/photos/older-texas-home.webp" alt="" width="1280" height="720"></div>
 <div class="wrap"><div class="kicker"><h2>Por qué vendernos</h2></div>
 <div class="bens">
  <article class="ben"><h3>Cierre en 7 a 14 días</h3><p>Es una venta en efectivo, así que no depende de un préstamo bancario.</p></article>
  <article class="ben"><h3>Venda tal como está, sin reparaciones</h3><p>No tiene que arreglar el techo, la cimentación ni el interior antes de hablar con nosotros.</p></article>
  <article class="ben"><h3>Pagamos todos los gastos de cierre</h3><p>Sin comisiones de agente. El saldo de su préstamo y los gravámenes se pagan del precio al cerrar.</p></article>
  <article class="ben"><h3>Gratis, sin compromiso</h3><p>Una persona real le devuelve la llamada, en español o en inglés.</p></article>
 </div></div>
</section>
<section class="alt" id="steps"><div class="wrap"><div class="kicker"><h2>De la dirección al cierre</h2><p>Tres pasos, de principio a fin.</p></div>
 <div class="steps"><div class="steps-card">
  <div class="step-i"><span class="n">1</span><h3>Envíe su dirección</h3><p>Revisamos ventas recientes, reparaciones y gravámenes.</p></div>
  <div class="step-i"><span class="n">2</span><h3>Reciba una oferta en efectivo</h3><p>Gratis, sin compromiso.</p></div>
  <div class="step-i"><span class="n">3</span><h3>Cierre y reciba su dinero</h3><p>Cierre en una compañía de títulos de Texas en 7 a 14 días. Pagamos todos los gastos de cierre.</p></div>
 </div><p><a class="btn" href="/como-funciona">Vea cómo funciona</a></p></div></div>
</section>
<section id="situations"><div class="wrap"><div class="kicker"><h2>Situaciones en las que ayudamos</h2></div><ul class="tags">{sits_list}</ul></div></section>
<section class="alt" id="areas"><div class="wrap"><div class="kicker"><h2>Dónde compramos</h2></div><ul class="tags">{metros_list}</ul></div></section>
{faq_html(core_faq)}
"""
    pages = [{
        "slug": "",
        "title": "Compramos casas en Texas en efectivo | Compramos Casas TX",
        "desc": "Compramos casas en Dallas–Fort Worth, Houston, San Antonio, Austin y el resto de Texas. Venda tal como está, sin reparaciones. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días.",
        "h1": "Venda su casa rápido por dinero en efectivo",
        "sub": "",
        "body": home_body,
        "faq": core_faq,
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
<p>Los comentarios de vendedores están en el perfil público de Google, no en esta página. Léalos en <a href="/opiniones">Opiniones</a>.</p>
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
<p>No publicamos una página por cada ciudad. Una página que solo cambia el nombre de la ciudad no le dice nada nuevo. Si su dirección está en Texas y no aparece arriba, use <a href="/oferta">el formulario</a> o llame al {PHONE}.</p>
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
        'Property: '+(data.address||''), 'Listed: '+(data.listed_with_realtor||''),
        'Situation: '+(data.situation||''), 'Timeline: '+(data.timeline||''),
        'Page: '+data.page_url].join('\n');
      var btn = form.querySelector('[type=submit]');
      if (btn) btn.disabled = true;
      fetch(ENDPOINT, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)})
        .then(function(r){
          if (!r.ok) throw new Error('bad');
          var to = data.listed_with_realtor === 'yes' ? '/gracias-listada' : '/gracias';
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
"""
    (DOCS / "assets/site-es.css").write_text(extra, encoding="utf-8")


def lint(pages):
    banned = ["el mejor", "número 1", "numero 1", "garantiz", "oficina local", "5709 vandalia", "grand prairie, tx 75052"]
    bad = []
    for page in pages:
        blob = (page["title"] + page["desc"] + page["h1"] + page["body"] + " ".join(q["a"] for q in page.get("faq") or [])).lower()
        for word in banned:
            if word in blob:
                bad.append((page["slug"] or "/", word))
    if bad:
        raise SystemExit("banned copy: " + repr(bad))


def main():
    ES = es_dict()
    pages = extra_pages(ES)
    have = {p["slug"] for p in pages}
    for page in load_landers():
        if page["slug"] in have:
            continue
        pages.append(page)
        have.add(page["slug"])
    lint(pages)
    desk, drawer = nav()
    write_site_js()
    write_css()
    urls = []
    for page in pages:
        slug = page["slug"]
        folder = DOCS if not slug else DOCS
        name = "index.html" if not slug else slug + ".html"
        (folder / name).write_text(page_html(page, desk, drawer), encoding="utf-8")
        urls.append(SITE + "/" if not slug else SITE + "/" + slug)
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
    (DOCS / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://www.compramoscasastx.com/sitemap.xml\n",
        encoding="utf-8",
    )
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        body.append(f"<url><loc>{url}</loc></url>")
    body.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(body) + "\n", encoding="utf-8")
    lines = [
        "# Compramos Casas TX",
        "",
        "> Sitio en español de Cash Home Advisors, LLC. Compramos casas en Texas tal como están, sin reparaciones. Pagamos todos los gastos de cierre y podemos cerrar en 7 a 14 días. La oferta es gratis y sin compromiso. Una persona real devuelve la llamada.",
        "",
        "Empresa legal: Cash Home Advisors, LLC",
        "Sitio: https://www.compramoscasastx.com/",
        "Sitio en inglés: https://www.cashhomeadvisors.com/",
        "Teléfono: (817) 520-8319",
        "Correo: adrian@cashhomeadvisors.com",
        "Licencia: Adrian Luna, agente de bienes raíces de Texas, TREC #675272-SA",
        "Área: Texas. Dallas–Fort Worth, Houston, San Antonio y Austin.",
        "",
        "No somos el agente del vendedor en una compra en efectivo. Compramos como principal, solos o con un inversionista socio, y lo decimos antes de la firma. El cierre es en una compañía de títulos de Texas.",
        "",
        "## Páginas",
    ]
    for url in urls:
        lines.append("- " + url)
    (DOCS / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"pages {len(pages)}")


if __name__ == "__main__":
    main()
