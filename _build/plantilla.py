# -*- coding: utf-8 -*-
"""
Marco compartido de todas las páginas de KORA.

Acá viven la cabecera, la navegación, el pie y el botón flotante. Se escriben
una sola vez y el generador los inserta en cada página. Si hay que tocar un
link del menú o del footer, se toca acá y se corren de nuevo los generadores:

    python _build/generar.py

Las páginas que salen son HTML estático puro: no necesitan este script para
funcionar en el servidor, sólo para volver a generarse.

Sistema visual: "Pizarra GSAP" (lienzo casi negro, crema, verde de marca,
Inter Tight). Todo vive en kora.css + kora.js, una sola hoja y un solo
script para las trece páginas.
"""
import math

DOMINIO = "https://kora.com.ar"        # ← cambiar por el dominio real
EMAIL = "hola@kora.com.ar"
WHATSAPP = "5491100000000"             # ← cambiar por el número real
WA_TEXTO = "Hola%20KORA%2C%20quiero%20consultar%20por%20un%20proyecto."

# Colores del sistema que se necesitan del lado de Python (el SVG del
# isotipo lleva los suyos inline). El resto vive en kora.css.
CREMA = "#fffce1"
VERDE = "#0AE448"
LIENZO = "#0e100f"


# --------------------------------------------------------------------------
# Isotipo
# Un núcleo dominante con tres nodos alrededor: KORA ("tu núcleo digital",
# como dice el pie) con sus tres servicios colgando de él.
#
# El dibujo anterior eran tres circunferencias finas superpuestas. A 32px
# los trazos se fundían entre sí y quedaba una mancha ilegible — el logo
# pasaba desapercibido justo en el único tamaño en que la gente lo ve.
# Este tiene cuatro formas sólidas separadas por aire, que es lo que
# aguanta el tamaño chico.
#
# El núcleo mide más del doble que cada nodo a propósito: si los cuatro
# círculos fueran parecidos, el dibujo diría "cuatro cosas" en vez de
# "una cosa con tres ramas".
#
# La geometría se calcula, no se escribe a mano, así la simetría es
# exacta y cambiar una medida no obliga a recalcular las otras.
# --------------------------------------------------------------------------
CENTRO = 64.0
ANGULOS_NODOS = (-90.0, 30.0, 150.0)   # uno arriba y dos abajo: apoya mejor
DIST_NODO = 54.0
R_NODO = 12.0
R_NUCLEO = 25.0
GROSOR_RADIO = 9.0
DESPLAZAMIENTO_Y = 13.5   # centra ópticamente el conjunto dentro del viewBox


def _nodo_xy(grados):
    rad = math.radians(grados)
    return (CENTRO + DIST_NODO * math.cos(rad), CENTRO + DIST_NODO * math.sin(rad))


def isotipo(tam, radio=CREMA, nucleo=VERDE, nodo=VERDE, clase=""):
    cls = ' class="%s"' % clase if clase else ""
    coords = [_nodo_xy(a) for a in ANGULOS_NODOS]

    radios = "\n".join(
        f'              <line class="iso__radio" x1="{CENTRO:.0f}" y1="{CENTRO:.0f}"'
        f' x2="{x:.2f}" y2="{y:.2f}"></line>'
        for x, y in coords
    )
    nodos = "\n".join(
        f'            <circle class="iso__nodo" cx="{x:.2f}" cy="{y:.2f}"'
        f' r="{R_NODO:.0f}" fill="{nodo}"></circle>'
        for x, y in coords
    )

    return f"""<svg{cls} width="{tam}" height="{tam}" viewBox="0 0 128 128" aria-hidden="true" focusable="false">
          <g transform="translate(0 {DESPLAZAMIENTO_Y})">
            <g stroke="{radio}" stroke-width="{GROSOR_RADIO:.0f}" stroke-linecap="round">
{radios}
            </g>
{nodos}
            <circle class="iso__nucleo" cx="{CENTRO:.0f}" cy="{CENTRO:.0f}" r="{R_NUCLEO:.0f}" fill="{nucleo}"></circle>
          </g>
        </svg>"""


ICONO_WA = """<svg class="wa-fab__icon" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.885-9.885 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.943c0 2.096.549 4.142 1.593 5.945L0 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.582 0 11.941-5.359 11.944-11.945a11.87 11.87 0 0 0-3.487-8.4"/>
    </svg>"""


# --------------------------------------------------------------------------
# Cabecera
# --------------------------------------------------------------------------
def cabeza(p):
    """p: dict con archivo, titulo, desc, og_titulo, og_desc, noindex, aviso."""
    url = f"{DOMINIO}/{p['archivo']}" if p["archivo"] != "index.html" else f"{DOMINIO}/"

    if p.get("noindex"):
        robots = f'\n  <!-- {p["noindex"]} -->\n  <meta name="robots" content="noindex, follow">'
    else:
        robots = '\n  <meta name="robots" content="index, follow">'

    canonical = "" if p.get("noindex") else f'\n  <link rel="canonical" href="{url}">'

    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['titulo']}</title>
  <meta name="description" content="{p['desc']}">
  <meta name="theme-color" content="{LIENZO}">{robots}{canonical}

  <meta property="og:type" content="{p.get('og_tipo', 'website')}">
  <meta property="og:site_name" content="KORA">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{p.get('og_titulo', p['titulo'])}">
  <meta property="og:description" content="{p.get('og_desc', p['desc'])}">
  <meta property="og:image" content="{DOMINIO}/img/og-kora.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_AR">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{p.get('og_titulo', p['titulo'])}">
  <meta name="twitter:description" content="{p.get('og_desc', p['desc'])}">
  <meta name="twitter:image" content="{DOMINIO}/img/og-kora.png">

  <link rel="icon" href="kora-icon-transparent.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!-- Inter Tight: sustituto libre de Mori, la sans humanista de una sola
       familia (400/500/600) que pide el sistema "pizarra GSAP". -->
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="kora.css">
</head>
<body>
{p.get('aviso', '')}
  <div class="dotfield" data-dotfield aria-hidden="true"></div>
  <div class="page-veil" data-veil aria-hidden="true"></div>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <div class="scroll-progress" data-progress aria-hidden="true"></div>

  <!-- ============ FRANJA DE ANUNCIO ============ -->
  <p class="announce">Agencia de desarrollo digital — Buenos Aires, Argentina</p>
"""


# --------------------------------------------------------------------------
# Navegación
# --------------------------------------------------------------------------
SERVICIOS = [
    ("servicios-web.html", "Desarrollo web", "Sitios y landings que convierten"),
    ("servicios-chatbots.html", "Chatbots", "Atención automática 24/7"),
    ("servicios-apps.html", "Apps a medida", "Software para tu operación"),
]


def navegacion(actual):
    def activo(archivo):
        return ' aria-current="page"' if archivo == actual else ""

    en_servicios = actual in [s[0] for s in SERVICIOS]
    items = "\n".join(
        f"""            <li><a href="{a}"{activo(a)}>
              <span class="submenu__titulo">{t}</span>
              <span class="submenu__desc">{d}</span>
            </a></li>"""
        for a, t, d in SERVICIOS
    )

    return f"""
  <!-- ============ NAVBAR ============ -->
  <header class="nav">
    <div class="nav__inner">
      <a class="nav__brand" href="index.html" aria-label="KORA — inicio">
        {isotipo(40, clase='nav__mark')}
        <span class="nav__wordmark">KORA</span>
      </a>

      <button class="nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="nav-menu" aria-label="Abrir menú">
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
      </button>

      <nav class="nav__menu" id="nav-menu" aria-label="Navegación principal">
        <ul class="nav__links">
          <li class="nav__item nav__item--tiene-submenu">
            <button class="nav__disparador" type="button" data-submenu aria-expanded="false" aria-controls="submenu-servicios"{' data-activo' if en_servicios else ''}>
              Servicios
              <span class="nav__chevron" aria-hidden="true"></span>
            </button>
            <ul class="submenu" id="submenu-servicios">
{items}
            </ul>
          </li>
          <li class="nav__item"><a href="casos.html"{activo('casos.html')}>Casos</a></li>
          <li class="nav__item"><a href="nosotros.html"{activo('nosotros.html')}>Nosotros</a></li>
          <li class="nav__item"><a href="precios.html"{activo('precios.html')}>Precios</a></li>
        </ul>
        <a class="pill pill--sm nav__cta" href="contacto.html">Hablemos</a>
      </nav>
    </div>
  </header>
"""


# --------------------------------------------------------------------------
# Pie
# El color de cada columna es clasificación, no decoración: verde para lo
# que se vende, rosa para la compañía, lila para los canales de contacto.
# --------------------------------------------------------------------------
def pie():
    return f"""
  <!-- ============ FOOTER ============ -->
  <footer class="footer">
    <div class="wrap">
      <div class="footer__grid">
        <div>
          <div class="footer__brand">
            {isotipo(34)}
            <span class="footer__wordmark">KORA</span>
          </div>
          <p class="footer__about">Tu núcleo digital: web, chatbots y apps. Agencia de desarrollo para PyMEs argentinas, con proceso claro y resultados medibles.</p>
        </div>

        <nav class="footer__col footer__col--green" aria-labelledby="f-servicios">
          <p class="footer__heading" id="f-servicios">Servicios</p>
          <ul class="footer__list">
            <li><a href="servicios-web.html">Desarrollo web</a></li>
            <li><a href="servicios-chatbots.html">Chatbots</a></li>
            <li><a href="servicios-apps.html">Apps a medida</a></li>
            <li><a href="precios.html">Precios</a></li>
          </ul>
        </nav>

        <nav class="footer__col footer__col--pink" aria-labelledby="f-compania">
          <p class="footer__heading" id="f-compania">Compañía</p>
          <ul class="footer__list">
            <li><a href="nosotros.html">Nosotros</a></li>
            <li><a href="casos.html">Casos</a></li>
            <li><a href="index.html#faq">Preguntas frecuentes</a></li>
            <li><a href="contacto.html">Contacto</a></li>
            <li><a href="privacidad.html">Política de privacidad</a></li>
          </ul>
        </nav>

        <nav class="footer__col footer__col--lila" aria-labelledby="f-contacto">
          <p class="footer__heading" id="f-contacto">Contacto</p>
          <ul class="footer__list">
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></li>
          </ul>
        </nav>
      </div>

      <div class="footer__legal">
        <p>© 2026 KORA. Todos los derechos reservados. CUIT 30-00000000-0.</p>
        <p>Buenos Aires, Argentina</p>
      </div>
    </div>
  </footer>

  <a class="wa-fab" href="https://wa.me/{WHATSAPP}?text={WA_TEXTO}"
     target="_blank" rel="noopener" data-wa-fab aria-label="Escribinos por WhatsApp">
    {ICONO_WA}
    <span class="wa-fab__label">Hablemos por WhatsApp</span>
  </a>
"""


def cierre(extra=""):
    return f"""{extra}
  <!-- GSAP self-hosteado (vendor/gsap/), no CDN — mismo criterio que todo
       lo demás: nada que dependa de que un tercero siga sirviendo el
       archivo. Va antes de kora.js porque kora.js lo usa si está
       disponible, pero la página entera se ve completa igual si estos dos
       archivos no cargaran (ver la guarda `if (!GSAP_OK) return;` al
       principio de cada función que los usa). -->
  <script src="vendor/gsap/gsap.min.js" defer></script>
  <script src="vendor/gsap/ScrollTrigger.min.js" defer></script>
  <script src="kora.js" defer></script>
</body>
</html>
"""


def pagina(p, cuerpo):
    """Arma la página completa."""
    return (
        cabeza(p)
        + navegacion(p["archivo"])
        + '\n  <main id="contenido">\n'
        + cuerpo
        + "\n  </main>\n"
        + pie()
        + cierre(p.get("extra_final", ""))
    )


# --------------------------------------------------------------------------
# Piezas reutilizables de contenido
# --------------------------------------------------------------------------
def cta_final(titulo, texto, boton="Empezar un proyecto"):
    return f"""
    <section class="cta">
      <div class="cta__inner">
        <div class="cta__copy">
          <h2 class="cta__title">{titulo}</h2>
          <p class="cta__text">{texto}</p>
          <div class="cta__acciones">
            <a class="btn btn--accent btn--xl" href="contacto.html">{boton}</a>
            <a class="cta__mail" href="https://wa.me/{WHATSAPP}?text={WA_TEXTO}" target="_blank" rel="noopener">o escribinos por WhatsApp</a>
          </div>
        </div>
      </div>
    </section>"""


def encabezado_pagina(eyebrow, titulo, bajada, cta=True):
    boton = (
        '\n        <div class="page-hero__acciones">'
        '\n          <a class="btn btn--accent btn--lg" href="contacto.html">Pedir presupuesto</a>'
        '\n          <a class="link-underline" href="casos.html">Ver casos</a>'
        "\n        </div>"
        if cta
        else ""
    )
    return f"""
    <section class="page-hero">
      <div class="page-hero__inner">
        <span class="eyebrow">{eyebrow}</span>
        <h1 class="page-hero__title">{titulo}</h1>
        <p class="page-hero__lede">{bajada}</p>{boton}
      </div>
    </section>"""
