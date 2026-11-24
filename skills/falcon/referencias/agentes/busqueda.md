# Agente de búsqueda: dónde los encuentra el cliente

**Archivo:** `datos/busqueda.json` · **Lista propia:** `busquedas` (una por consulta) + `hallazgos`.

## Qué hacer

1. **Pensá como cliente.** Armá de 6 a 10 búsquedas que haría alguien que quiere comprar lo que vende la persona,
   mezclando:
   - genéricas: "<rubro> en <ciudad>", "mejor <producto> <ciudad>";
   - de problema: "cómo <problema que resuelve>", "<necesidad> urgente";
   - de precio: "<producto> precio", "<producto> barato";
   - de comparación: "<competidor grande> alternativas", "<competidor> vs <competidor>";
   - de marca: el nombre de cada competidor (para ver qué aparece alrededor: reseñas, quejas, notas).
   Si el negocio es local, agregá la ciudad o el barrio.
2. **Anotá quién aparece.** Para cada búsqueda, los primeros 5 a 10 resultados con su posición, y en `competidor` a
   quién pertenece (`null` si no es de nadie de la lista, `"_vos"` si es la persona). Marcá en `hallazgos` los
   resultados patrocinados que veas.
3. **Google Maps** (si es local): para "<rubro> cerca de <zona>", quién sale en el mapa, con nota y cantidad de
   reseñas. Va como búsqueda con `"tipo": "maps"`.
4. **Buscadores con IA:** si podés, hacé 2 o 3 preguntas como las haría un cliente a un asistente ("¿qué
   <rubro> me recomendás en <ciudad>?") y anotá a quién nombra la respuesta (`"tipo": "ia"`).
5. **Su contenido para buscadores:** si tienen blog o guías, sobre qué escriben y cada cuánto. `site:<dominio>`
   da una idea del tamaño del sitio; `<dominio>/sitemap.xml` lista sus páginas. Páginas por ciudad o por servicio
   = están trabajando el SEO en serio.
6. **Directorios y listados:** "las 10 mejores <rubro> en <ciudad>", directorios del rubro, marketplaces. Quién
   está y quién no.

## Hallazgos que valen oro

- Una búsqueda con mucha intención de compra donde ningún competidor aparece arriba.
- El competidor que aparece en todas (y qué página usa para eso).
- Listados de "los mejores" donde la persona podría pedir aparecer.
- La persona no aparece en ninguna búsqueda de su propia ciudad.
