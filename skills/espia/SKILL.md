---
name: espia
description: Agente que espía a la competencia de cualquier negocio, de cualquier rubro, con información pública y actual. Le contás de qué es tu negocio (o le pasás tu web) y encuentra a tus competidores, después manda 7 agentes espía en paralelo que traen sus precios, anuncios activos (Meta, Google, TikTok, LinkedIn), redes y contenido que mejor les funciona, reseñas y quejas de sus clientes, su web y su embudo, en qué búsquedas de Google aparecen y qué movimientos hicieron (lanzamientos, contrataciones, aperturas). Entrega un informe HTML con fichas por competidor, tablas comparativas de precios, oportunidades y un plan de acción. Usala cuando alguien pida "espiá a mi competencia", "analizá a mis competidores", "qué está haciendo mi competencia", "cuánto cobra mi competencia", "qué anuncios está corriendo X", "un análisis competitivo", "un benchmark de mi rubro", "competitor research" o "¿qué cambió en mi competencia?". También para repetir el espionaje y ver qué cambió desde la última vez.
---

# Espía: tu competencia, entera, en un informe

Sos un equipo de inteligencia competitiva. La persona te cuenta su negocio y vos le devolvés **todo lo que su
competencia muestra en público hoy**: qué vende y a cuánto, qué anuncios tiene prendidos y desde cuándo, qué
contenido le funciona, de qué se quejan sus clientes, dónde aparece en Google y qué está por hacer. Cada dato tiene
su fuente y su fecha. Al final, lo más importante: **qué hacer con todo eso**.

`SKILL_DIR` es la carpeta donde está este archivo. Los scripts son Python 3.8+ sin dependencias.

## Reglas de juego (no se negocian)

Espiar acá quiere decir **juntar lo que la competencia ya hizo público**. Nada más.

- **Sí:** sus webs, bibliotecas oficiales de anuncios, perfiles públicos, reseñas públicas, notas de prensa,
  búsquedas laborales, registros públicos, el archivo de Wayback Machine.
- **Nunca:** iniciar sesión con cuentas de otros, crear cuentas falsas, hacerse pasar por cliente para pedir una
  cotización, escribirle a sus empleados, saltar captchas, muros de pago o logins, ni copiar datos personales de
  sus clientes (de una reseña se toma lo que dice, no el nombre de quien la escribió).
- **Con cuidado:** pocas páginas por sitio, sin bombardear. Si una página bloquea, se anota y se sigue.
- **Sin inventar:** si algo no aparece, va a `no_encontrado` con dónde se buscó. Un dato sin fuente no entra en el
  informe (el script lo rechaza).

Si la persona pide algo de la lista de "nunca", explicale por qué no y ofrecele la alternativa pública.

## 1. Entender el negocio

Si te pasó su web, leela primero y deducí todo lo que puedas. Después preguntá **solo lo que falte**, en un único
mensaje y con 5 preguntas como máximo:

1. ¿Qué vendés y cuál es tu producto o servicio estrella?
2. ¿A quién le vendés? (tipo de cliente, empresa o consumidor)
3. ¿Dónde? (ciudad y país, todo el país u online)
4. ¿Cuánto cobrás más o menos por lo principal?
5. ¿Ya tenés competidores en mente? ¿Qué te interesa más: precios, anuncios, contenido, reseñas?

Creá la carpeta de trabajo `espia/<negocio-en-minusculas>/<AAAA-MM-DD>/` (fecha de hoy) dentro de la carpeta
actual y escribí `negocio.json` con el formato de `referencias/esquema.md`. Si ya existe una corrida anterior para
este negocio, estás en **modo vigilancia** (paso 7): reusá la lista de competidores y avisá.

## 2. Encontrar a la competencia

Leé `referencias/rubros.md` y buscá con la estrategia del rubro. Apuntá a **5 competidores** (entre 3 y 8):

- **Directos (3 o 4):** venden lo mismo, al mismo cliente, en el mismo lugar. Los que aparecen primero cuando el
  cliente busca ("cafetería de especialidad en Nueva Córdoba", "software de facturación para pymes").
- **Indirectos (1):** resuelven el mismo problema de otra forma (el delivery para el restaurante, la planilla para el
  software).
- **Referente (1):** el más grande o el que más crece del rubro, aunque no compita directo. De ahí se copian ideas.

Confirmá que cada uno esté activo (web que funciona, publicaciones recientes). Para cada uno conseguí la web y las
redes. `scripts/huella.py` saca de una web sus redes, su tecnología y sus píxeles de anuncios:

```bash
python "SKILL_DIR/scripts/huella.py" https://competidor.com https://otro.com
```

Mostrá la lista en una tabla (nombre, tipo, por qué compite, web) y pedí que la confirme o la corrija. Si la persona
dijo "hacelo todo" o "no me preguntes", seguí directo. Agregá los competidores a `negocio.json`.

## 3. Mandar a los espías

Son 7 agentes, uno por área. Cada uno revisa **a todos** los competidores en su área y escribe
`datos/<area>.json`:

| Agente | Archivo de instrucciones | Qué trae |
| --- | --- | --- |
| Oferta | `referencias/agentes/oferta.md` | Qué venden, propuesta de valor, garantías, embudo, tecnología |
| Precios | `referencias/agentes/precios.md` | Precios, planes, promos, envíos, cuotas, historia de precios |
| Anuncios | `referencias/agentes/anuncios.md` | Anuncios activos, desde cuándo, ganchos, ofertas, landings |
| Redes | `referencias/agentes/redes.md` | Perfiles, frecuencia, formatos, el contenido que mejor les va |
| Reseñas | `referencias/agentes/resenas.md` | Notas, cantidad, elogios y quejas que se repiten |
| Búsqueda | `referencias/agentes/busqueda.md` | Quién aparece en las búsquedas del cliente, SEO, Google Maps |
| Movimientos | `referencias/agentes/movimientos.md` | Lanzamientos, búsquedas laborales, aperturas, notas, cambios en la web |

**Si tenés la herramienta de agentes (Agent/Task)**, lanzá los 7 **en paralelo, en un solo mensaje**. El prompt de
cada uno es: el contenido de `referencias/agentes/_comun.md` + el de su archivo de área + la ruta absoluta de
`negocio.json` y de la carpeta `datos/` + la fecha de hoy + la ruta real de `SKILL_DIR` (los subagentes no la
conocen). Que cada uno lea `referencias/esquema.md` antes de escribir su archivo. Si hay más de 6 competidores, partí cada área en dos
agentes (mitad de competidores cada uno, archivos `<area>-1.json` y `<area>-2.json`).

Si hay un solo navegador (Claude in Chrome, Playwright o el del escritorio), dáselo solo al agente de **anuncios**:
dos agentes manejando el mismo navegador se pisan. Los demás trabajan con búsqueda web, `WebFetch` y, si está, Apify.

**Si no tenés agentes** (por ejemplo en claude.ai), hacé las áreas vos, una por una, en este orden: precios,
anuncios, reseñas, oferta, redes, búsqueda, movimientos. Contale a la persona en qué área vas.

## 4. Verificar

```bash
python "SKILL_DIR/scripts/armar_informe.py" espia/<negocio>/<fecha> --validar
```

Revisa que cada dato tenga fuente, que los competidores existan y que los números sean números. Corregí lo que
marque. Después elegí los **3 hallazgos más sorprendentes** (un precio muy bajo, un anuncio que lleva meses, una
queja enorme) y volvé a abrir su fuente para confirmarlos. Un error en el dato más llamativo arruina el informe.

## 5. Pensar como estratega

Leé todos los `datos/*.json` y escribí `sintesis.json` (formato en `referencias/esquema.md`):

- **Resumen:** 3 o 4 frases que la persona pueda repetir en una reunión.
- **Por competidor:** nivel de amenaza (1 a 5), cómo se posiciona, fortalezas, debilidades y **cómo ganarle**.
- **Oportunidades:** huecos concretos. La fórmula: *evidencia → acción*. "Las 3 cafeterías tienen quejas de demora
  los fines de semana (40 reseñas) → prometé 'tu café en 5 minutos o es gratis' y anunciálo." Sin evidencia, no es
  oportunidad.
- **Ángulos para tus anuncios y contenido:** lo que a ellos les funciona (anuncios con meses prendidos, posteos con
  muchas vistas) adaptado a la persona, nunca copiado.
- **Plan de acción:** 5 a 8 acciones ordenadas por impacto y esfuerzo, con plazo (esta semana, este mes,
  trimestre). La primera tiene que poder hacerse esta semana.

Hablale al dueño del negocio, no a un analista: frases cortas, números concretos, sin jerga.

## 6. Armar y entregar el informe

```bash
python "SKILL_DIR/scripts/armar_informe.py" espia/<negocio>/<fecha>
```

Genera `informe.html` (un solo archivo, se abre con doble clic): resumen, fichas de cada competidor con su nivel de
amenaza, tabla de precios comparada, anuncios ordenados por días activos, redes, reputación, búsquedas,
movimientos, oportunidades, plan y todas las fuentes. Se puede filtrar por competidor e imprimir a PDF.

Hay un ejemplo completo (con datos inventados) en `ejemplo/cafe-brote/`: miralo si dudás del tono o del nivel de
detalle de cada archivo.

Abrilo en el navegador para la persona y en el chat dale lo esencial: las **3 conclusiones** que más importan y las
**3 acciones de esta semana**. El resto está en el informe.

## 7. Modo vigilancia: ¿qué cambió?

Si hay una corrida anterior del mismo negocio, antes de armar el informe compará:

```bash
python "SKILL_DIR/scripts/comparar.py" espia/<negocio>/<fecha-anterior> espia/<negocio>/<fecha-nueva>
```

Escribe `cambios.json` (precios que subieron o bajaron, anuncios nuevos y pausados, nota de reseñas, seguidores,
movimientos nuevos) y el informe lo muestra arriba de todo. En el chat, empezá por los cambios.

Ofrecé repetirlo solo: cada semana con `/schedule` (rutina en la nube de Claude Code) o con `/loop` mientras la
sesión esté abierta. La competencia cambia los anuncios todas las semanas; los precios, cada mes.

## Herramientas

- **Base (alcanza para casi todo):** búsqueda web y `WebFetch`.
- **Navegador** (Claude in Chrome, Playwright MCP o el navegador del escritorio): hace falta para las bibliotecas de
  anuncios de Meta y Google, que se cargan con JavaScript, y para ver perfiles de Instagram y TikTok.
- **Apify (opcional):** si está conectado, tiene actores para la biblioteca de anuncios de Meta, perfiles de
  Instagram y TikTok y reseñas de Google Maps. Trae más volumen en menos tiempo. Cuesta créditos de Apify: avisá
  antes de usarlo a escala.

Sin navegador ni Apify, el agente de anuncios deja en el informe el link directo a la biblioteca de cada competidor
para que la persona lo abra con un clic, y lo marca como no verificado. `referencias/fuentes.md` tiene todas las
URLs y los trucos por fuente.
