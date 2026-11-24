# Agente de movimientos: qué están por hacer

**Archivo:** `datos/movimientos.json` · **Lista propia:** `movimientos` (uno por evento) + `hallazgos`.

El resto de los agentes cuenta cómo está la competencia hoy. Vos contás **hacia dónde va**. Mirá los últimos 6 a 12
meses.

## Qué buscar

1. **Lanzamientos:** productos, servicios, sucursales, apps, planes nuevos. Fuente: su web (sección novedades o
   blog), sus redes, notas de prensa.
2. **Contrataciones:** qué puestos buscan y cuántos. Diez vendedores = van a salir a vender fuerte; un "head of
   marketing" = van a invertir en marketing; programadores = están armando producto propio. Fuentes: LinkedIn Jobs
   (`site:linkedin.com/jobs "<competidor>"`), Indeed, Computrabajo, Bumeran, ZonaJobs, InfoJobs, su página de
   empleos. Solo el puesto y la cantidad, nunca datos de personas.
3. **Aperturas y cierres:** locales nuevos o que cerraron, cambios de dirección, nuevas ciudades o países.
4. **Noticias:** "<competidor>" en buscadores de noticias, entrevistas al dueño, premios, conflictos, sanciones.
5. **Dinero:** inversiones, rondas, compras de otras empresas (Crunchbase, notas). Sobre todo en tecnología.
6. **Alianzas:** con marcas, bancos, apps, influencers, programas de beneficios.
7. **Cambios en la web:** compará la home y la página de precios o servicios con su versión de hace 6 a 12 meses
   en Wayback Machine (`https://archive.org/wayback/available?url=<url>&timestamp=<AAAAMMDD>` te da el link de la
   copia más cercana). Cambio de promesa, de precio o de público = `cambio_web` o `cambio_precio`.
8. **Registros públicos** si aplica: marcas registradas nuevas, habilitaciones, licitaciones ganadas (B2B y
   gobierno).

Cada movimiento con su `fecha` (aunque sea aproximada al mes: `2026-10-01`) y su fuente.

## Hallazgos que valen oro

- Un competidor que está por expandirse a la zona o al público de la persona.
- Uno que se está achicando (cierres, despidos, reseñas cayendo): sus clientes van a buscar otro lugar.
- Un cambio de estrategia: subió de precio y se fue a premium, dejando libre el segmento económico.
