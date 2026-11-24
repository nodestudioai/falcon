# Agente de redes: qué contenido les funciona

**Archivo:** `datos/redes.json` · **Lista propia:** `perfiles` (uno por competidor y red) + `hallazgos`.

## Qué buscar

Para cada red donde esté cada competidor (Instagram, TikTok, YouTube, Facebook, LinkedIn, X):

1. **Tamaño:** seguidores (número exacto o aproximado, `12400` y no "12,4 mil").
2. **Ritmo:** cuántas publicaciones por semana en el último mes (`publicaciones_por_semana`).
3. **Formato principal:** reels, carruseles, fotos, videos largos, shorts, lives.
4. **Temas que repiten:** detrás de escena, tips, testimonios, promos, humor, tendencias, el dueño a cámara.
5. **Lo que mejor les va:** de 2 a 4 publicaciones con más vistas, likes o comentarios de los últimos 3 meses, con
   su métrica y su link, en `mejor_contenido`. Describí qué tiene: el gancho, el formato, de qué habla.
6. **Señales extra:** colaboraciones con influencers, sorteos, contenido en vivo, si responden comentarios, links en
   bio (a dónde mandan).

## Dónde mirar

- Los links de redes están en `negocio.json` (los sacó `huella.py` de la web). Si falta alguno, buscá
  "<competidor> instagram" o "<competidor> tiktok".
- Instagram y TikTok muestran poco sin sesión. Probá en este orden: búsqueda web (los resultados suelen mostrar
  seguidores y publicaciones recientes), `WebFetch` del perfil, Apify (actores de "Instagram Profile Scraper",
  "TikTok Profile Scraper", con lotes chicos), y por último el navegador solo si el agente de anuncios no lo está
  usando.
- YouTube y LinkedIn de empresa se ven bien con `WebFetch` o búsqueda.
- No inicies sesión nunca. Si algo no se ve, va a `no_encontrado`.

## Hallazgos que valen oro

- Un formato que les explota y la persona no usa.
- Un competidor chico con poco presupuesto que crece más rápido que el grande (y por qué).
- Preguntas que se repiten en sus comentarios: son contenido listo para la persona.
- Una red donde nadie del rubro está presente: territorio libre.
