# Agente de anuncios: qué publicidad tienen prendida

**Archivo:** `datos/anuncios.json` · **Listas propias:** `anuncios` (uno por anuncio) y `bibliotecas` (una por
competidor y plataforma) + `hallazgos`.

Sos el único agente que puede usar el navegador. Las bibliotecas de anuncios se cargan con JavaScript: con
`WebFetch` solo no se ven.

## La regla de oro

**Un anuncio que lleva mucho tiempo prendido es un anuncio que funciona.** Nadie paga meses por algo que no vende.
Por eso la fecha `activo_desde` es lo más importante de cada anuncio. Ordená lo que juntes por antigüedad y mirá con
lupa los que llevan más de 30 días.

## Dónde mirar

1. **Meta (Facebook e Instagram).** Biblioteca de anuncios:
   `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=<PAIS>&q=<nombre>&search_type=keyword_unordered&media_type=all`
   Buscá por el nombre de la página, elegí la página correcta y quedate con su vista (`view_all_page_id=...`). Cada
   anuncio muestra "Comenzó a circular el…", las plataformas y cuántas versiones tiene. `<PAIS>` es el código de
   `negocio.pais` (AR, MX, ES, CO, CL, US…); si venden a varios países, `ALL`.
2. **Google (búsqueda, YouTube, Display).** Centro de transparencia:
   `https://adstransparency.google.com/?region=<PAIS>&domain=<dominio>` o buscando el anunciante por nombre.
   Muestra los anuncios con fecha de primera y última vez visto.
3. **TikTok.** Biblioteca de anuncios `https://library.tiktok.com/ads` (solo anuncios mostrados en Europa) y el
   Creative Center de anuncios destacados del rubro `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/es`.
4. **LinkedIn** (si es B2B): `https://www.linkedin.com/ad-library/search?accountOwner=<nombre>`.
5. **Señales indirectas.** Si `huella.py` o el agente de oferta encontró píxel de Meta, TikTok o Google Ads en su
   web, están invirtiendo o por invertir. Si al buscar "<rubro> <ciudad>" en Google aparece un resultado
   "Patrocinado" de un competidor, anotalo con la consulta.

## Qué anotar de cada anuncio

Plataforma, `activo_desde`, formato (imagen, video, carrusel, texto), **el gancho** (la primera frase o lo primero
que se ve/escucha), el texto (recortado), el botón (`cta`), la oferta (descuento, envío gratis, prueba gratis) y a
dónde lleva (`landing`: web, WhatsApp, formulario). La `fuente` es el link del anuncio en la biblioteca (o el de la
página del anunciante si el anuncio no tiene link propio).

Si un competidor tiene muchos, quedate con los 5 a 8 más antiguos y con los más nuevos (los nuevos muestran qué
están probando ahora). En `bibliotecas` anotá cuántos activos tiene en total cada plataforma.

## Si no podés abrir las bibliotecas

Sin navegador ni Apify, cargá igual en `bibliotecas` una fila por competidor con el link armado, `activos: null` y
`verificado: false`, y avisá en `resumen`. El informe le muestra a la persona el botón para abrirlo.

Con Apify: buscá un actor de "Facebook Ads Library" (`search-actors`), corré un lote con las páginas de los
competidores y tomá de cada anuncio la fecha de inicio, el texto, el formato y el link.

## Hallazgos que valen oro

- El anuncio más viejo de cada uno (y qué promete).
- Ofertas repetidas en varios competidores: así se está comprando en ese rubro.
- Un competidor que invierte fuerte (muchos anuncios, muchas versiones del mismo) contra otros que no anuncian nada.
- A dónde mandan el tráfico: si todos mandan a WhatsApp, el rubro vende conversando.
