# Formato de los archivos

Una corrida vive en `espia/<negocio>/<AAAA-MM-DD>/`:

```
negocio.json        el negocio de la persona y la lista de competidores
datos/<area>.json   lo que trajo cada agente espía (oferta, precios, anuncios, redes, resenas, busqueda, movimientos)
sintesis.json       tus conclusiones, oportunidades y plan
cambios.json        (solo en modo vigilancia) lo genera comparar.py
informe.html        lo genera armar_informe.py
```

Reglas para todos los archivos:

- Fechas en `AAAA-MM-DD`. Números como número (`12500`, no `"$12.500"`); el texto original va en otro campo.
- `competidor` es siempre el `id` de `negocio.json`. Para el negocio de la persona se usa `"_vos"`.
- Todo dato lleva `fuente`: la URL exacta donde se vio (no la home si estaba en otra página).
- `confianza`: `alta` (lo viste en su fuente oficial), `media` (fuente de terceros o dato viejo), `baja` (inferido).

## negocio.json

```json
{
  "fecha": "2026-11-24",
  "negocio": {
    "nombre": "Café Brote",
    "rubro": "Cafetería de especialidad",
    "descripcion": "Café de especialidad y pastelería propia para llevar y para quedarse.",
    "web": "https://cafebrote.com",
    "ubicacion": "Nueva Córdoba, Córdoba, Argentina",
    "pais": "AR",
    "alcance": "local",
    "publico": "Estudiantes y oficinistas de 20 a 35 años",
    "oferta_principal": "Flat white y medialunas de masa madre",
    "precio_referencia": "Flat white $3.800",
    "moneda": "ARS",
    "redes": { "instagram": "https://www.instagram.com/cafebrote" },
    "interes": ["precios", "anuncios", "contenido"]
  },
  "competidores": [
    {
      "id": "tostado",
      "nombre": "Tostado Café",
      "tipo": "directo",
      "por_que": "Misma zona, mismo público, café de especialidad",
      "web": "https://tostadocafe.com",
      "ubicacion": "Nueva Córdoba",
      "redes": { "instagram": "https://www.instagram.com/tostadocafe", "tiktok": "", "facebook": "", "linkedin": "", "youtube": "" }
    }
  ]
}
```

`tipo`: `directo`, `indirecto` o `referente`. `alcance`: `local`, `nacional` u `online`. El `id` va en minúsculas,
sin espacios ni tildes.

## datos/<area>.json

Todas las áreas comparten esta base:

```json
{
  "area": "precios",
  "fecha": "2026-11-24",
  "resumen": "2 o 3 frases con lo más importante del área.",
  "hallazgos": [
    { "competidor": "tostado", "titulo": "Combo desayuno a $5.900", "detalle": "Flat white + medialuna, solo hasta las 11.", "fuente": "https://...", "confianza": "alta" }
  ],
  "no_encontrado": [
    { "competidor": "molienda", "que": "Lista de precios", "donde": "Web, Instagram destacadas, Google Maps (fotos de menú)" }
  ]
}
```

Y además, cada área tiene su lista propia:

### oferta → `ofertas`

```json
{ "competidor": "tostado", "propuesta_valor": "Café de origen tostado en el local", "productos": ["Café en barra", "Granos por kilo", "Cursos de barista"],
  "garantia": "", "cta_principal": "Pedí por WhatsApp", "embudo": "Instagram → link a WhatsApp → pedido",
  "tecnologia": ["Tiendanube", "Meta Pixel", "Google Analytics"], "fuente": "https://..." }
```

### precios → `precios`

```json
{ "competidor": "tostado", "producto": "Flat white 8 oz", "categoria": "Flat white", "precio": 4200, "precio_texto": "$4.200",
  "moneda": "ARS", "unidad": "taza", "condiciones": "Precio en local; en PedidosYa $4.800", "fecha": "2026-11-24", "fuente": "https://..." }
```

`categoria` es el nombre **normalizado** para comparar entre competidores ("Flat white", "Plan básico",
"Consulta inicial"). Todos los productos comparables tienen que usar exactamente la misma `categoria`. Incluí una
fila con `"competidor": "_vos"` si la persona te dio su precio.

### anuncios → `anuncios` y `bibliotecas`

```json
{ "competidor": "tostado", "plataforma": "meta", "activo_desde": "2026-08-02", "formato": "video", "gancho": "¿Tomaste café de verdad alguna vez?",
  "texto": "Primer texto del anuncio, recortado si es largo", "cta": "Enviar mensaje", "oferta": "2x1 los martes", "landing": "https://wa.me/...", "fuente": "https://www.facebook.com/ads/library/?id=..." }
```

`plataforma`: `meta`, `google`, `tiktok`, `linkedin`, `youtube`, `otra`.

```json
"bibliotecas": [ { "competidor": "tostado", "plataforma": "meta", "activos": 6, "url": "https://www.facebook.com/ads/library/?...", "verificado": true } ]
```

`activos` es la cantidad de anuncios activos que mostró la biblioteca (o `null` si no se pudo ver). `verificado`
es `false` si solo dejaste el link sin poder abrirlo.

### redes → `perfiles`

```json
{ "competidor": "tostado", "red": "instagram", "url": "https://www.instagram.com/tostadocafe", "seguidores": 18400,
  "publicaciones_por_semana": 5, "formato_principal": "reels", "temas": ["latte art", "detrás de escena", "promos"],
  "mejor_contenido": [ { "descripcion": "Reel del tostado en cámara lenta", "metrica": "210 mil vistas", "url": "https://..." } ] }
```

### resenas → `reputacion`

```json
{ "competidor": "tostado", "plataforma": "Google Maps", "nota": 4.6, "escala": 5, "cantidad": 1240,
  "elogios": ["el café", "la atención de los baristas"], "quejas": ["demora los fines de semana (muchas menciones)", "pocas mesas"],
  "fuente": "https://..." }
```

Elogios y quejas son **temas que se repiten**, resumidos con tus palabras, con una idea de cuántas veces aparecen.
Nada de nombres de quienes escribieron.

### busqueda → `busquedas`

```json
{ "consulta": "cafetería de especialidad nueva córdoba", "tipo": "google",
  "resultados": [ { "posicion": 1, "competidor": "tostado", "titulo": "Tostado Café | Café de especialidad", "url": "https://..." },
                  { "posicion": 2, "competidor": null, "titulo": "Las 10 mejores cafeterías de Córdoba - Blog", "url": "https://..." } ] }
```

`tipo`: `google`, `maps` o `ia` (respuesta de un buscador con IA). `competidor` es `null` cuando el resultado no es de
ningún competidor (o `"_vos"` si es la persona).

### movimientos → `movimientos`

```json
{ "competidor": "tostado", "fecha": "2026-10-15", "tipo": "apertura", "titulo": "Abre segundo local en Güemes",
  "detalle": "Anunciado en Instagram; búsqueda de 4 baristas en LinkedIn.", "fuente": "https://..." }
```

`tipo`: `lanzamiento`, `contratacion`, `apertura`, `cierre`, `noticia`, `cambio_web`, `cambio_precio`, `inversion`,
`alianza`, `premio`, `otro`.

## sintesis.json

```json
{
  "resumen": "3 o 4 frases para repetir en una reunión.",
  "conclusiones": ["Conclusión 1 con un número", "Conclusión 2", "Conclusión 3"],
  "competidores": [
    { "id": "tostado", "amenaza": 4, "posicionamiento": "El café 'de origen' premium de la zona",
      "fortalezas": ["Marca fuerte en Instagram"], "debilidades": ["Demoras los fines de semana"],
      "como_ganarle": "Velocidad: prometé y mostrá el tiempo de espera." }
  ],
  "oportunidades": [
    { "titulo": "Nadie ofrece suscripción de café", "evidencia": "Ninguno de los 5 tiene plan mensual (ver precios).",
      "accion": "Lanzá 'Café ilimitado' a $45.000 por mes para los oficinistas de la zona.", "competidores": ["tostado", "molienda"] }
  ],
  "angulos": [
    { "titulo": "El proceso como espectáculo", "por_que": "El reel del tostado de Tostado Café tiene 210 mil vistas; su anuncio de proceso lleva 114 días activo.",
      "ejemplo": "Reel: tu medialuna de masa madre de las 5 de la mañana al mostrador, en 15 segundos." }
  ],
  "plan": [
    { "accion": "Publicá tu precio en Google Maps y en las destacadas", "por_que": "2 de 4 competidores no lo muestran y los clientes lo piden en reseñas",
      "impacto": "alto", "esfuerzo": "bajo", "plazo": "esta semana" }
  ]
}
```

`amenaza`: 1 (casi no compite) a 5 (te está sacando clientes ahora). `impacto` y `esfuerzo`: `alto`, `medio`, `bajo`.
`plazo`: `esta semana`, `este mes`, `trimestre`.
