# Fuentes públicas y cómo leerlas

Todas son públicas y gratuitas. Las que dicen **navegador** se cargan con JavaScript: con `WebFetch` se ven vacías.

## Anuncios

| Fuente | URL | Cómo |
| --- | --- | --- |
| Biblioteca de anuncios de Meta | `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<PAIS>&q=<nombre>&search_type=keyword_unordered&media_type=all` | **Navegador** o Apify. Muestra fecha de inicio, plataformas y versiones de cada anuncio |
| Centro de transparencia de Google Ads | `https://adstransparency.google.com/?region=<PAIS>&domain=<dominio>` | **Navegador**. Búsqueda, YouTube y Display, con primera y última vez visto |
| Biblioteca de anuncios de TikTok | `https://library.tiktok.com/ads` | **Navegador**. Solo anuncios mostrados en Europa |
| TikTok Creative Center (anuncios destacados por rubro) | `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/es` | **Navegador**. Sirve para ver qué funciona en el rubro |
| Biblioteca de anuncios de LinkedIn | `https://www.linkedin.com/ad-library/search?accountOwner=<nombre>` | `WebFetch` o navegador |

## Web, oferta y tecnología

| Fuente | Cómo |
| --- | --- |
| Su web | `WebFetch` de home, servicios, precios, nosotros, preguntas frecuentes |
| HTML crudo | `curl -sL -A "Mozilla/5.0" <url>` o `scripts/huella.py <url>` |
| Mapa del sitio | `<dominio>/sitemap.xml` (y `sitemap_index.xml`): todas sus páginas, a veces con fecha |
| Wayback Machine | `https://archive.org/wayback/available?url=<url>&timestamp=<AAAAMMDD>` devuelve la copia más cercana; después `WebFetch` de esa copia. Sirve para ver precios y promesas de hace meses |

`huella.py` detecta: Shopify, Tiendanube, WooCommerce, WordPress, Wix, Webflow, Squarespace, VTEX, Magento,
Hotmart, Kajabi, Meta Pixel, TikTok Pixel, Google Ads, Google Analytics, Google Tag Manager, Hotjar, Clarity,
HubSpot, Klaviyo, Mailchimp, Intercom, WhatsApp, Calendly, Mercado Pago, Stripe, PayPal y más.

## Precios

Su web y tienda, Mercado Libre, Amazon, Google Shopping, apps de delivery (PedidosYa, Rappi, Uber Eats), Booking y
Airbnb, App Store y Google Play, Doctoralia, portales inmobiliarios. Fotos de menú en Google Maps (navegador).

## Redes

| Red | Cómo |
| --- | --- |
| Instagram | Búsqueda web del perfil (los resultados muestran seguidores y posteos), `WebFetch` del perfil, Apify "Instagram Profile Scraper" o navegador. Sin sesión se ve poco |
| TikTok | `WebFetch` de `https://www.tiktok.com/@<usuario>`, Apify "TikTok Profile Scraper" o navegador |
| YouTube | `WebFetch` del canal y de `/videos`; la búsqueda muestra suscriptores |
| LinkedIn de empresa | `WebFetch` de `https://www.linkedin.com/company/<usuario>` (seguidores, empleados, publicaciones) |
| Facebook | Página pública con navegador; la biblioteca de anuncios muestra también datos de la página |

## Reseñas

Google Maps (búsqueda web para nota y cantidad; Apify "Google Maps Reviews Scraper" o navegador para leerlas),
Trustpilot (`https://www.trustpilot.com/review/<dominio>`), Mercado Libre, TripAdvisor, Booking, G2, Capterra,
App Store, Google Play, Doctoralia, Reclame Aqui, Reddit (`site:reddit.com "<nombre>"`), foros del rubro.

## Movimientos

Noticias (buscador, "<nombre>" con el año), LinkedIn Jobs (`site:linkedin.com/jobs "<nombre>"`), Indeed,
Computrabajo, Bumeran, ZonaJobs, InfoJobs, su página de empleos, Crunchbase, sus redes (anuncios de aperturas),
registros de marcas del país, portales de licitaciones públicas.

## Apify (opcional)

Si el MCP de Apify está conectado: `search-actors` con lo que necesitás ("facebook ads library", "instagram profile",
"tiktok profile", "google maps reviews"), elegí el actor con más usuarios y buena nota, leé el esquema con
`fetch-actor-details` y corré lotes chicos (los competidores juntos en una sola corrida). Cada corrida gasta créditos.
