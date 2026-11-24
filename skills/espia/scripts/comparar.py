#!/usr/bin/env python3
"""Compara dos corridas del espía y escribe cambios.json en la más nueva.

Uso:
    python comparar.py espia/<negocio>/<fecha-anterior> espia/<negocio>/<fecha-nueva>

Detecta: competidores nuevos, precios que subieron o bajaron, productos nuevos o retirados, anuncios nuevos y
pausados, cambios de nota y cantidad de reseñas, cambios de seguidores y movimientos nuevos.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # consola de Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))
from armar_informe import cargar_corrida  # noqa: E402


PLAT = {"meta": "Meta", "google": "Google", "tiktok": "TikTok", "linkedin": "LinkedIn", "youtube": "YouTube"}
RED = {"instagram": "Instagram", "tiktok": "TikTok", "youtube": "YouTube", "facebook": "Facebook", "linkedin": "LinkedIn", "x": "X"}


def clave_texto(t):
    return " ".join(str(t or "").lower().split())[:80]


def indexar(filas, clave):
    salida = {}
    for f in filas:
        k = clave(f)
        if k and k not in salida:
            salida[k] = f
    return salida


def lista(corrida, area, campo):
    return (corrida["areas"].get(area) or {}).get(campo) or []


def pct(antes, despues):
    if not antes:
        return None
    return round((despues - antes) / antes * 100, 1)


def comparar(vieja, nueva):
    nombres = {c["id"]: c.get("nombre", c["id"]) for c in nueva["negocio"].get("competidores", [])}
    nombres["_vos"] = "Vos"
    items = []

    def agregar(tipo, competidor, texto, antes=None, despues=None, importancia="media"):
        items.append({"tipo": tipo, "competidor": competidor, "texto": texto, "antes": antes, "despues": despues,
                      "importancia": importancia})

    viejos_ids = {c["id"] for c in vieja["negocio"].get("competidores", [])}
    for c in nueva["negocio"].get("competidores", []):
        if c["id"] not in viejos_ids:
            agregar("competidor", c["id"], f"Nuevo competidor en el radar: {c.get('nombre', c['id'])}")

    # Precios
    clave_p = lambda f: (f.get("competidor"), clave_texto(f.get("categoria") or f.get("producto")))
    p_viejo = indexar(lista(vieja, "precios", "precios"), clave_p)
    p_nuevo = indexar(lista(nueva, "precios", "precios"), clave_p)
    for k, f in p_nuevo.items():
        nombre = f.get("categoria") or f.get("producto")
        if k not in p_viejo:
            if any(kv[0] == k[0] for kv in p_viejo):
                agregar("precio_nuevo", k[0], f"{nombres.get(k[0], k[0])} agregó {nombre}: {f.get('precio_texto') or f.get('precio')}")
            continue
        a, d = p_viejo[k].get("precio"), f.get("precio")
        if isinstance(a, (int, float)) and isinstance(d, (int, float)) and a != d:
            cambio = pct(a, d)
            verbo = "subió" if d > a else "bajó"
            imp = "alta" if cambio is not None and abs(cambio) >= 10 else "media"
            agregar("precio", k[0], f"{nombres.get(k[0], k[0])} {verbo} {nombre} un {str(abs(cambio)).replace('.', ',')}%", a, d, imp)
    for k, f in p_viejo.items():
        if k not in p_nuevo and any(kv[0] == k[0] for kv in p_nuevo):
            agregar("precio_retirado", k[0], f"{nombres.get(k[0], k[0])} ya no muestra {f.get('categoria') or f.get('producto')}")

    # Anuncios
    clave_a = lambda f: (f.get("competidor"), f.get("plataforma"), clave_texto(f.get("gancho") or f.get("texto")))
    a_viejo = indexar(lista(vieja, "anuncios", "anuncios"), clave_a)
    a_nuevo = indexar(lista(nueva, "anuncios", "anuncios"), clave_a)
    for k, f in a_nuevo.items():
        if k not in a_viejo:
            gancho = f.get("gancho") or f.get("texto") or "sin texto"
            agregar("anuncio_nuevo", k[0], f"{nombres.get(k[0], k[0])} prendió un anuncio nuevo en {PLAT.get(k[1], k[1])}: “{gancho[:90]}”",
                    importancia="alta")
    for k, f in a_viejo.items():
        if k not in a_nuevo:
            gancho = f.get("gancho") or f.get("texto") or "sin texto"
            agregar("anuncio_pausado", k[0], f"{nombres.get(k[0], k[0])} apagó el anuncio “{gancho[:90]}”")

    b_viejo = indexar(lista(vieja, "anuncios", "bibliotecas"), lambda f: (f.get("competidor"), f.get("plataforma")))
    for f in lista(nueva, "anuncios", "bibliotecas"):
        k = (f.get("competidor"), f.get("plataforma"))
        a, d = (b_viejo.get(k) or {}).get("activos"), f.get("activos")
        if isinstance(a, int) and isinstance(d, int) and a != d:
            agregar("anuncios_cantidad", k[0], f"{nombres.get(k[0], k[0])} pasó de {a} a {d} anuncios activos en {PLAT.get(k[1], k[1])}",
                    a, d, "alta" if abs(d - a) >= 3 else "media")

    # Reseñas
    r_viejo = indexar(lista(vieja, "resenas", "reputacion"), lambda f: (f.get("competidor"), clave_texto(f.get("plataforma"))))
    for f in lista(nueva, "resenas", "reputacion"):
        k = (f.get("competidor"), clave_texto(f.get("plataforma")))
        v = r_viejo.get(k)
        if not v:
            continue
        a, d = v.get("nota"), f.get("nota")
        if isinstance(a, (int, float)) and isinstance(d, (int, float)) and round(a, 1) != round(d, 1):
            verbo = "subió" if d > a else "bajó"
            agregar("reputacion", k[0], f"La nota de {nombres.get(k[0], k[0])} en {f.get('plataforma')} {verbo} de {a} a {d}",
                    a, d, "alta" if abs(d - a) >= 0.2 else "media")
        ca, cd = v.get("cantidad"), f.get("cantidad")
        if isinstance(ca, int) and isinstance(cd, int) and cd - ca >= 10:
            agregar("resenas_nuevas", k[0], f"{nombres.get(k[0], k[0])} sumó {cd - ca} reseñas en {f.get('plataforma')}", ca, cd, "baja")

    # Seguidores
    s_viejo = indexar(lista(vieja, "redes", "perfiles"), lambda f: (f.get("competidor"), f.get("red")))
    for f in lista(nueva, "redes", "perfiles"):
        k = (f.get("competidor"), f.get("red"))
        a, d = (s_viejo.get(k) or {}).get("seguidores"), f.get("seguidores")
        if isinstance(a, int) and isinstance(d, int) and a and abs(d - a) / a >= 0.02:
            cambio = pct(a, d)
            agregar("seguidores", k[0], f"{nombres.get(k[0], k[0])} {'ganó' if d > a else 'perdió'} {abs(d - a):,} seguidores en {RED.get(k[1], k[1])} ({cambio:+}%)".replace(",", "."),
                    a, d, "alta" if abs(cambio) >= 10 else "baja")

    # Movimientos
    m_viejo = indexar(lista(vieja, "movimientos", "movimientos"), lambda f: (f.get("competidor"), clave_texto(f.get("titulo"))))
    for f in lista(nueva, "movimientos", "movimientos"):
        k = (f.get("competidor"), clave_texto(f.get("titulo")))
        if k not in m_viejo:
            agregar("movimiento", k[0], f"{nombres.get(k[0], k[0])}: {f.get('titulo')}", importancia="alta")

    orden = {"alta": 0, "media": 1, "baja": 2}
    items.sort(key=lambda i: orden.get(i["importancia"], 1))
    return {"desde": vieja["negocio"].get("fecha"), "hasta": nueva["negocio"].get("fecha"), "items": items}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    vieja, nueva = Path(sys.argv[1]), Path(sys.argv[2])
    cambios = comparar(cargar_corrida(vieja), cargar_corrida(nueva))
    destino = nueva / "cambios.json"
    destino.write_text(json.dumps(cambios, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(cambios['items'])} cambios desde {cambios['desde']} → {destino}")
    for i in cambios["items"]:
        marca = "!!" if i["importancia"] == "alta" else " -"
        print(f" {marca} {i['texto']}")


if __name__ == "__main__":
    main()
