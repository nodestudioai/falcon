#!/usr/bin/env python3
"""Huella de una web: redes sociales, tecnología y píxeles de anuncios.

Uso:
    python huella.py https://competidor.com [https://otro.com ...] [--json]

Lee solo la página que le pasás (una petición por URL) y busca en el HTML:
- links a Instagram, TikTok, Facebook, LinkedIn, YouTube, X, WhatsApp, Pinterest, Threads;
- la plataforma (Shopify, Tiendanube, WordPress, Wix...) y herramientas (Meta Pixel, Google Ads, HubSpot...).

Solo usa la biblioteca estándar de Python.
"""
import json
import re
import sys
import ssl
import urllib.request

try:  # certificados de certifi si está instalado (Python en Windows a veces no encuentra los del sistema)
    import certifi
    CONTEXTO = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXTO = ssl.create_default_context()
from urllib.parse import urljoin, urlparse

if hasattr(sys.stdout, "reconfigure"):  # consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AGENTE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

REDES = {
    "instagram": r"https?://(?:www\.)?instagram\.com/(?!p/|reel/|explore/|accounts/)[A-Za-z0-9_.]+/?",
    "tiktok": r"https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.]+/?",
    "facebook": r"https?://(?:www\.|es-la\.|m\.)?facebook\.com/(?!sharer|share|plugins|tr\b|dialog)[A-Za-z0-9_.\-]+/?",
    "linkedin": r"https?://(?:[a-z]{2,3}\.)?linkedin\.com/(?:company|in|school)/[A-Za-z0-9_\-%.]+/?",
    "youtube": r"https?://(?:www\.)?youtube\.com/(?:@[A-Za-z0-9_.\-]+|channel/[A-Za-z0-9_\-]+|c/[A-Za-z0-9_\-]+|user/[A-Za-z0-9_\-]+)/?",
    "x": r"https?://(?:www\.)?(?:twitter|x)\.com/(?!intent|share|home)[A-Za-z0-9_]+/?",
    "whatsapp": r"https?://(?:api\.whatsapp\.com/send\?phone=\d+|wa\.me/\d+|wa\.link/[A-Za-z0-9]+)",
    "pinterest": r"https?://(?:[a-z]{2}\.)?pinterest\.[a-z.]+/[A-Za-z0-9_\-]+/?",
    "threads": r"https?://(?:www\.)?threads\.(?:net|com)/@[A-Za-z0-9_.]+/?",
}

TECNOLOGIA = {
    # Plataformas
    "Shopify": [r"cdn\.shopify\.com", r"Shopify\.theme"],
    "Tiendanube": [r"tiendanube", r"nuvemshop", r"d26lpennugtm8s\.cloudfront\.net"],
    "WooCommerce": [r"woocommerce"],
    "WordPress": [r"wp-content/", r"wp-includes/"],
    "Wix": [r"static\.wixstatic\.com", r"wix\.com"],
    "Webflow": [r"webflow\.(?:com|io)", r"data-wf-site"],
    "Squarespace": [r"squarespace"],
    "VTEX": [r"vtex(?:assets|img|commercestable)?\."],
    "Magento": [r"Mage\.Cookies", r"/static/version\d+/frontend/", r"x-magento"],
    "PrestaShop": [r"prestashop"],
    "Framer": [r"framerusercontent\.com", r"framer\.com/m/"],
    "Hotmart": [r"hotmart"],
    "Kajabi": [r"kajabi"],
    "Empretienda": [r"empretienda"],
    # Publicidad y medición
    "Meta Pixel": [r"connect\.facebook\.net/[^\"']*fbevents\.js", r"fbq\(\s*['\"]init"],
    "TikTok Pixel": [r"analytics\.tiktok\.com", r"ttq\.load"],
    "Google Ads": [r"googleadservices\.com", r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]AW-"],
    "Google Analytics": [r"google-analytics\.com", r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-", r"googletagmanager\.com/gtag/js\?id=G-"],
    "Google Tag Manager": [r"googletagmanager\.com/gtm\.js", r"GTM-[A-Z0-9]{4,}"],
    "LinkedIn Insight": [r"snap\.licdn\.com", r"_linkedin_partner_id"],
    "Pinterest Tag": [r"pintrk\("],
    "Hotjar": [r"hotjar\.com"],
    "Microsoft Clarity": [r"clarity\.ms"],
    # Ventas y contacto
    "HubSpot": [r"js\.hs-scripts\.com", r"hubspot"],
    "Klaviyo": [r"klaviyo"],
    "Mailchimp": [r"mailchimp", r"list-manage\.com"],
    "ActiveCampaign": [r"activehosted\.com", r"activecampaign"],
    "Intercom": [r"widget\.intercom\.io", r"intercomSettings"],
    "Zendesk": [r"zdassets\.com", r"zendesk"],
    "Tidio": [r"tidio"],
    "Crisp": [r"client\.crisp\.chat"],
    "Botón de WhatsApp": [r"wa\.me/", r"api\.whatsapp\.com"],
    "Calendly": [r"calendly\.com"],
    "AgendaPro": [r"agendapro"],
    "Typeform": [r"typeform\.com"],
    # Pagos
    "Mercado Pago": [r"mercadopago", r"mercadolibre\.com/jms"],
    "Stripe": [r"js\.stripe\.com"],
    "PayPal": [r"paypal\.com/sdk", r"paypalobjects"],
}


def bajar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept-Language": "es,en;q=0.8"})
    with urllib.request.urlopen(pedido, timeout=20, context=CONTEXTO) as r:
        crudo = r.read(3_000_000)
        juego = r.headers.get_content_charset() or "utf-8"
        return r.geturl(), crudo.decode(juego, errors="replace")


def limpiar(link):
    link = link.split("?")[0] if "whatsapp.com/send" not in link else link
    return link.rstrip("/").replace("http://", "https://")


def huella(url):
    if not url.startswith("http"):
        url = "https://" + url
    resultado = {"url": url, "redes": {}, "tecnologia": [], "titulo": "", "descripcion": "", "error": None}
    try:
        final, html = bajar(url)
    except Exception as e:  # noqa: BLE001
        resultado["error"] = f"No se pudo leer: {e}"
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            resultado["error"] += " (instalá certifi: pip install certifi, o leé la página con WebFetch)"
        return resultado
    resultado["url"] = final

    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m:
        resultado["titulo"] = re.sub(r"\s+", " ", m.group(1)).strip()[:200]
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, re.I)
    if m:
        resultado["descripcion"] = m.group(1).strip()[:300]

    texto = html.replace("\\/", "/")
    for red, patron in REDES.items():
        vistos = []
        for link in re.findall(patron, texto, re.I):
            link = limpiar(link)
            if link not in vistos:
                vistos.append(link)
        if vistos:
            resultado["redes"][red] = vistos[:3]

    for nombre, patrones in TECNOLOGIA.items():
        if any(re.search(p, texto, re.I) for p in patrones):
            resultado["tecnologia"].append(nombre)

    anuncios = [t for t in ("Meta Pixel", "TikTok Pixel", "Google Ads", "LinkedIn Insight", "Pinterest Tag") if t in resultado["tecnologia"]]
    resultado["invierte_en_anuncios"] = bool(anuncios)
    resultado["dominio"] = urlparse(final).netloc.replace("www.", "")
    return resultado


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(1)
    resultados = [huella(u) for u in args]
    if "--json" in sys.argv:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
        return
    for r in resultados:
        print(f"\n=== {r['url']}")
        if r["error"]:
            print("  " + r["error"])
            continue
        if r["titulo"]:
            print(f"  Título: {r['titulo']}")
        if r["descripcion"]:
            print(f"  Descripción: {r['descripcion']}")
        print("  Redes:" if r["redes"] else "  Redes: no se encontraron links en esta página")
        for red, links in r["redes"].items():
            print(f"    {red}: {', '.join(links)}")
        print(f"  Tecnología: {', '.join(r['tecnologia']) or 'nada reconocible (puede cargarse con JavaScript)'}")
        print(f"  Píxeles de anuncios: {'sí' if r['invierte_en_anuncios'] else 'no se ven'}")


if __name__ == "__main__":
    main()
