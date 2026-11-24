# Agente de precios: cuánto cobra cada uno

**Archivo:** `datos/precios.json` · **Lista propia:** `precios` (una fila por producto y competidor) + `hallazgos`.

## Qué buscar

1. **Los mismos productos en todos.** Primero mirá qué vende la persona (`oferta_principal`, `precio_referencia`) y
   elegí de 3 a 6 productos o servicios **comparables** que tengan casi todos. Usá exactamente la misma `categoria`
   para cada uno en todos los competidores, así la tabla los compara. Ejemplos: "Flat white", "Plan mensual",
   "Corte de pelo", "Consulta inicial", "Envío a domicilio", "Hora de consultoría".
2. **Precio y condiciones.** Precio final con impuestos si se ve, moneda, unidad (por mes, por hora, por kilo, por
   persona), y en `condiciones` todo lo que cambia el precio: cuotas sin interés, descuento por transferencia,
   precio distinto en apps de delivery, mínimo de compra, precio de lista contra precio de oferta.
3. **Planes y escalones.** Si tienen planes (básico, pro, empresa), cargá cada uno como fila con `categoria` propia.
4. **Promos activas.** 2x1, descuentos de temporada, cupón de primera compra, envío gratis desde X. Van a
   `hallazgos` con su vigencia.
5. **Historia del precio.** Si tienen página de precios, buscá una versión vieja en Wayback Machine
   (`https://web.archive.org/web/2025/<url-de-precios>`, o la API `https://archive.org/wayback/available?url=<url>&timestamp=<AAAAMMDD>`).
   Si subieron o bajaron, es un hallazgo: "subió 18% desde marzo".
6. **El precio de la persona.** Si `negocio.json` tiene precio de referencia, cargalo como fila con
   `"competidor": "_vos"` y la misma `categoria`.

## Dónde mirar, por orden

1. Página de precios, tienda online o menú en la web.
2. Marketplaces y apps: Mercado Libre, Amazon, Tiendanube, PedidosYa, Rappi, Uber Eats, Booking, Airbnb, Doctoralia,
   App Store y Google Play (precios de suscripción). Ahí casi siempre está el precio aunque la web no lo muestre.
3. Google Shopping o la búsqueda "<competidor> precio <producto>".
4. Fotos del menú o la lista de precios en Google Maps y destacadas de Instagram (con navegador).
5. Notas, comparadores y reseñas que mencionen precios (confianza media, con fecha).

## Si no publican precios

Es un dato en sí: "no publica precios, pide escribir por WhatsApp". Va a `hallazgos`. Si en reseñas o foros
aparece un precio, cargalo con `confianza: "media"` y la fecha del comentario. **Nunca** pidas una cotización
haciéndote pasar por cliente.

`precio` siempre como número (sin puntos de miles ni signo). Si es un rango, poné el mínimo en `precio` y el rango en
`precio_texto`.
