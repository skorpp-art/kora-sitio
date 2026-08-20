# -*- coding: utf-8 -*-
"""
Genera todas las páginas HTML del sitio.

    cd "boceto silvia"
    python _build/generar.py

Las páginas resultantes son HTML estático puro: se suben tal cual y no
necesitan nada de esto para funcionar. Este script sólo hace falta para
volver a generarlas cuando se toca el marco (nav/footer) o los contenidos.
"""
import os
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

import plantilla                                     # noqa: E402
from plantilla import pagina, DOMINIO                # noqa: E402
import paginas                                       # noqa: E402
import paginas_b                                     # noqa: E402


def leer(nombre):
    with open(os.path.join(AQUI, "cuerpos", nombre), encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------
# Home: el cuerpo vive en _build/cuerpos/home.html para poder editarlo
# sin tocar Python.
# --------------------------------------------------------------------------
HOME = {
    "archivo": "index.html",
    "titulo": "KORA — Webs, chatbots y apps para PyMEs argentinas",
    "desc": "Agencia de desarrollo digital en Argentina. Diseñamos y desarrollamos webs, chatbots y apps con proceso claro, presupuesto cerrado y resultados medibles.",
    "og_titulo": "KORA — Una web que convierte visitas en clientes",
    "og_desc": "Webs, chatbots y apps para PyMEs argentinas. Proceso claro, presupuesto cerrado, resultados medibles.",
    "cuerpo": leer("home.html"),
    "extra_final": "\n" + leer("home-schema.html"),
}

AVISO_PRIVACIDAD = """
<!-- =====================================================================
     ANTES DE PUBLICAR — completar con los datos reales:

       · Razón social y CUIT (en "Quién es responsable"). El CUIT
         30-00000000-0 que aparece en el pie es de ejemplo.
       · Domicilio legal.
       · Los proveedores reales que menciona "Con quién se comparten":
         hosting, servicio de formularios y correo.

     Este texto es una base seria pero genérica, no asesoramiento legal.
     Conviene que lo revise un abogado antes de publicarlo.
     ===================================================================== -->
"""

AVISO_404 = """
<!-- =====================================================================
     Para que esta página se muestre de verdad, el servidor tiene que
     saber que es la de error 404. No alcanza con que el archivo exista:

       · Netlify y Vercel: la toman solas si está en la raíz.
       · Apache: agregar "ErrorDocument 404 /404.html" en el .htaccess.
       · Nginx: agregar "error_page 404 /404.html;" en el server.
       · Hosting compartido con cPanel: se configura en "Páginas de error".

     Importante: la respuesta tiene que seguir siendo código 404, no 200.
     ===================================================================== -->
"""

PRIVACIDAD = {
    "archivo": "privacidad.html",
    "titulo": "Política de privacidad — KORA",
    "desc": "Cómo KORA trata los datos personales que se envían por el formulario: qué se recopila, para qué, cuánto se conserva y cómo ejercer tus derechos.",
    "og_titulo": "Política de privacidad — KORA",
    "og_tipo": "article",
    "aviso": AVISO_PRIVACIDAD,
    "cuerpo": leer("privacidad.html"),
}

ERROR_404 = {
    "archivo": "404.html",
    "titulo": "Página no encontrada — KORA",
    "desc": "La página que buscabas no existe o cambió de dirección.",
    "noindex": "Las páginas de error no deben indexarse",
    "aviso": AVISO_404,
    "cuerpo": leer("404.html"),
}

PAGINAS = [
    HOME,
    paginas.SERVICIO_WEB,
    paginas.SERVICIO_CHATBOTS,
    paginas.SERVICIO_APPS,
    paginas.CASOS_LISTA,
    paginas.CASO_FERRETERIA,
    paginas.CASO_VEGA,
    paginas.CASO_NUTRI,
    paginas_b.NOSOTROS,
    paginas_b.PRECIOS,
    paginas_b.CONTACTO,
    PRIVACIDAD,
    ERROR_404,
]


def generar_paginas():
    for p in PAGINAS:
        destino = os.path.join(RAIZ, p["archivo"])
        with open(destino, "w", encoding="utf-8", newline="\n") as f:
            f.write(pagina(p, p["cuerpo"]))
        marca = "  (noindex)" if p.get("noindex") else ""
        print(f"  {p['archivo']:<32}{marca}")


def generar_sitemap():
    """Sólo las páginas indexables. Los casos de ejemplo quedan afuera."""
    hoy = date.today().isoformat()
    prioridad = {
        "index.html": "1.0",
        "servicios-web.html": "0.9",
        "servicios-chatbots.html": "0.9",
        "servicios-apps.html": "0.9",
        "precios.html": "0.8",
        "casos.html": "0.7",
        "nosotros.html": "0.7",
        "contacto.html": "0.7",
        "privacidad.html": "0.3",
    }

    urls = []
    for p in PAGINAS:
        if p.get("noindex"):
            continue
        a = p["archivo"]
        loc = f"{DOMINIO}/" if a == "index.html" else f"{DOMINIO}/{a}"
        urls.append((loc, prioridad.get(a, "0.5")))

    cuerpo = "\n".join(
        f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{hoy}</lastmod>
    <priority>{pri}</priority>
  </url>"""
        for loc, pri in urls
    )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Generado por _build/generar.py. No editar a mano.
     Los casos de ejemplo no se listan: llevan noindex hasta que sean reales. -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{cuerpo}
</urlset>
"""
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print(f"  sitemap.xml                       ({len(urls)} URLs)")


if __name__ == "__main__":
    print("Generando páginas…")
    generar_paginas()
    generar_sitemap()
    print("\nListo. Recordá revisar los marcadores pendientes:")
    print("  · dominio real en _build/plantilla.py (DOMINIO)")
    print("  · número de WhatsApp real (WHATSAPP)")
    print("  · rangos de precio en _build/paginas_b.py (buscar 'A completar')")
    print("  · fotos y nombres del equipo en NOSOTROS")
