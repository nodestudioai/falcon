# Agente de reseñas: qué dicen sus clientes

**Archivo:** `datos/resenas.json` · **Lista propia:** `reputacion` (una por competidor y plataforma) + `hallazgos`.

Las quejas de los clientes de la competencia son la mejor fuente de oportunidades que existe: te dicen exactamente
qué prometer.

## Qué buscar

1. **Nota y cantidad** en cada plataforma donde tenga reseñas.
2. **Elogios que se repiten:** qué es lo que más valoran (eso es lo que la persona tiene que igualar).
3. **Quejas que se repiten:** qué es lo que más molesta (eso es lo que la persona puede ganar). Indicá cuántas veces
   aparece más o menos: "demora en el envío (aparece en ~25 de las últimas 100)".
4. **Tendencia:** si las reseñas recientes son peores o mejores que las viejas.
5. **Cómo responden:** si el dueño contesta las reseñas negativas y cómo.

Leé las **más recientes** y las **más bajas** primero. Con 30 a 60 reseñas por competidor alcanza para ver los temas.

## Dónde mirar, según el rubro

- **Negocios con local:** Google Maps (la búsqueda "<competidor> <ciudad>" suele mostrar nota y cantidad; para leer
  las reseñas, Apify "Google Maps Reviews Scraper" o el navegador si está libre), TripAdvisor, Facebook.
- **E-commerce:** Mercado Libre (reputación del vendedor y preguntas), Trustpilot
  (`https://www.trustpilot.com/review/<dominio>`), Reclame Aqui (Brasil), reseñas en su tienda.
- **Software y apps:** G2, Capterra, App Store, Google Play, Product Hunt.
- **Salud y profesionales:** Doctoralia, Google Maps, Top Doctors.
- **Turismo:** Booking, Airbnb, TripAdvisor, Google.
- **Todos:** Reddit y foros (`site:reddit.com "<competidor>"`), comentarios en sus redes, "<competidor> opiniones",
  "<competidor> estafa" o "<competidor> problemas", sitios de defensa del consumidor.

## Privacidad

Resumí con tus palabras. No copies nombres ni fotos de quienes escriben, ni datos de contacto. Una cita textual
corta está bien si es muy reveladora, sin el nombre.

## Hallazgos que valen oro

- La queja que comparten varios competidores (hueco de todo el rubro).
- Un competidor con nota alta pero pocas reseñas, o con muchas reseñas pero cayendo.
- Lo que los clientes piden y nadie da ("ojalá tuvieran delivery", "no tienen turnos a la tarde").
