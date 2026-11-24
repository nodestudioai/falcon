#!/usr/bin/env python3
"""Valida una corrida del espía y arma informe.html.

Uso:
    python armar_informe.py espia/<negocio>/<fecha> --validar     solo revisa los datos
    python armar_informe.py espia/<negocio>/<fecha>               revisa y arma informe.html
    python armar_informe.py <carpeta> --salida otro.html          con otro nombre
    python armar_informe.py <carpeta> --forzar                    arma aunque haya errores

La carpeta tiene negocio.json, datos/<area>.json, sintesis.json y, opcional, cambios.json.
Si un área se partió en varios archivos (precios-1.json, precios-2.json) los junta.
"""
import html as htmllib
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AQUI = Path(__file__).resolve().parent
PLANTILLA = AQUI.parent / "plantilla" / "informe.html"
AREAS = ["oferta", "precios", "anuncios", "redes", "resenas", "busqueda", "movimientos"]
LISTAS = {  # área -> listas propias que llevan competidor + fuente
    "oferta": ["ofertas"],
    "precios": ["precios"],
    "anuncios": ["anuncios", "bibliotecas"],
    "redes": ["perfiles"],
    "resenas": ["reputacion"],
    "busqueda": ["busquedas"],
    "movimientos": ["movimientos"],
}
CAMPO_FUENTE = {"perfiles": "url", "bibliotecas": "url"}
NUMEROS = {"precios": ["precio"], "reputacion": ["nota", "cantidad"], "perfiles": ["seguidores", "publicaciones_por_semana"],
           "bibliotecas": ["activos"]}


def leer_json(ruta):
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"ERROR: {ruta} no es JSON válido (línea {e.lineno}, columna {e.colno}): {e.msg}")


def cargar_corrida(carpeta):
    carpeta = Path(carpeta)
    if not (carpeta / "negocio.json").exists():
        raise SystemExit(f"ERROR: no encuentro {carpeta / 'negocio.json'}")
    negocio = leer_json(carpeta / "negocio.json")
    areas = {}
    for archivo in sorted((carpeta / "datos").glob("*.json")) if (carpeta / "datos").exists() else []:
        datos = leer_json(archivo)
        area = datos.get("area") or archivo.stem.split("-")[0]
        if area not in areas:
            areas[area] = datos
            continue
        destino = areas[area]  # área partida en varios archivos: se juntan las listas
        for k, v in datos.items():
            if isinstance(v, list):
                destino.setdefault(k, []).extend(v)
            elif k == "resumen" and v:
                destino["resumen"] = (destino.get("resumen", "") + " " + v).strip()
    sintesis = leer_json(carpeta / "sintesis.json") if (carpeta / "sintesis.json").exists() else None
    cambios = leer_json(carpeta / "cambios.json") if (carpeta / "cambios.json").exists() else None
    return {"negocio": negocio, "areas": areas, "sintesis": sintesis, "cambios": cambios}


def es_url(v):
    return isinstance(v, str) and v.startswith(("http://", "https://"))


def validar(corrida):
    errores, avisos = [], []
    neg = corrida["negocio"]
    comps = neg.get("competidores") or []
    if not neg.get("negocio", {}).get("nombre"):
        errores.append("negocio.json: falta negocio.nombre")
    if not neg.get("fecha"):
        errores.append("negocio.json: falta fecha")
    if not comps:
        errores.append("negocio.json: no hay competidores")
    ids = set()
    for c in comps:
        if not c.get("id") or not c.get("nombre"):
            errores.append(f"negocio.json: competidor sin id o nombre: {c}")
        elif c["id"] in ids:
            errores.append(f"negocio.json: id repetido: {c['id']}")
        ids.add(c.get("id"))
        if c.get("tipo") not in ("directo", "indirecto", "referente"):
            avisos.append(f"negocio.json: {c.get('id')} tiene tipo '{c.get('tipo')}' (directo, indirecto o referente)")
    validos = ids | {"_vos"}

    for area in AREAS:
        if area not in corrida["areas"]:
            avisos.append(f"datos/{area}.json: falta (esa sección no va a salir en el informe)")
    for area, datos in corrida["areas"].items():
        if area not in AREAS:
            avisos.append(f"datos: área desconocida '{area}' (se ignora)")
            continue
        for i, h in enumerate(datos.get("hallazgos") or []):
            donde = f"datos/{area}.json hallazgos[{i}]"
            if h.get("competidor") not in validos:
                errores.append(f"{donde}: competidor '{h.get('competidor')}' no está en negocio.json")
            if not es_url(h.get("fuente")):
                errores.append(f"{donde}: falta fuente (URL) en “{str(h.get('titulo'))[:60]}”")
        for lista in LISTAS[area]:
            for i, f in enumerate(datos.get(lista) or []):
                donde = f"datos/{area}.json {lista}[{i}]"
                if lista == "busquedas":
                    if not f.get("consulta"):
                        errores.append(f"{donde}: falta consulta")
                    for j, r in enumerate(f.get("resultados") or []):
                        if r.get("competidor") not in validos | {None}:
                            errores.append(f"{donde}.resultados[{j}]: competidor '{r.get('competidor')}' no existe")
                    continue
                if f.get("competidor") not in validos:
                    errores.append(f"{donde}: competidor '{f.get('competidor')}' no está en negocio.json")
                campo = CAMPO_FUENTE.get(lista, "fuente")
                if not es_url(f.get(campo)):
                    errores.append(f"{donde}: falta {campo} (URL)")
                for n in NUMEROS.get(lista, []):
                    v = f.get(n)
                    if v is not None and not isinstance(v, (int, float)):
                        errores.append(f"{donde}: '{n}' tiene que ser número, no {v!r}")
                if lista == "anuncios" and not f.get("activo_desde"):
                    avisos.append(f"{donde}: sin activo_desde (es lo que dice si el anuncio funciona)")

    s = corrida["sintesis"]
    if s is None:
        avisos.append("sintesis.json: falta (el informe sale sin conclusiones ni plan)")
    else:
        for c in s.get("competidores") or []:
            if c.get("id") not in ids:
                errores.append(f"sintesis.json: competidor '{c.get('id')}' no está en negocio.json")
            a = c.get("amenaza")
            if a is not None and a not in (1, 2, 3, 4, 5):
                errores.append(f"sintesis.json: amenaza de {c.get('id')} tiene que ser 1 a 5")
        for i, o in enumerate(s.get("oportunidades") or []):
            if not o.get("evidencia"):
                errores.append(f"sintesis.json oportunidades[{i}]: sin evidencia no es oportunidad")
        if not s.get("plan"):
            avisos.append("sintesis.json: falta plan de acción")
    return errores, avisos


def contar(corrida):
    fuentes, datos = set(), 0
    for area, d in corrida["areas"].items():
        for h in d.get("hallazgos") or []:
            datos += 1
            fuentes.add(h.get("fuente"))
        for lista in LISTAS.get(area, []):
            for f in d.get(lista) or []:
                datos += 1
                fuentes.add(f.get(CAMPO_FUENTE.get(lista, "fuente")))
                for r in f.get("resultados") or []:
                    fuentes.add(r.get("url"))
    fuentes.discard(None)
    return datos, len(fuentes)


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("--"):
        print(__doc__)
        sys.exit(1)
    carpeta = Path(args[0])
    corrida = cargar_corrida(carpeta)
    errores, avisos = validar(corrida)
    datos, fuentes = contar(corrida)

    print(f"{corrida['negocio'].get('negocio', {}).get('nombre', '?')}: {len(corrida['negocio'].get('competidores', []))} competidores, "
          f"{len(corrida['areas'])} áreas, {datos} datos, {fuentes} fuentes")
    for a in avisos:
        print("  aviso: " + a)
    for e in errores:
        print("  ERROR: " + e)

    if "--validar" in args:
        print("Todo en orden." if not errores else f"{len(errores)} errores para corregir.")
        sys.exit(1 if errores else 0)
    if errores and "--forzar" not in args:
        print(f"No armo el informe: hay {len(errores)} errores. Corregilos o usá --forzar.")
        sys.exit(1)

    salida = carpeta / (args[args.index("--salida") + 1] if "--salida" in args else "informe.html")
    paquete = dict(corrida, estadisticas={"datos": datos, "fuentes": fuentes})
    incrustado = json.dumps(paquete, ensure_ascii=False).replace("</", "<\\/")
    html = PLANTILLA.read_text(encoding="utf-8")
    if "/*__DATOS__*/null" not in html:
        raise SystemExit("ERROR: la plantilla no tiene el marcador /*__DATOS__*/null")
    html = html.replace("/*__DATOS__*/null", incrustado, 1)
    titulo = f"Espía · {corrida['negocio'].get('negocio', {}).get('nombre', '')} · {corrida['negocio'].get('fecha', '')}"
    html = html.replace("<title>Espía</title>", f"<title>{htmllib.escape(titulo)}</title>", 1)
    salida.write_text(html, encoding="utf-8")
    print(f"Listo: {salida.resolve()}")


if __name__ == "__main__":
    main()
