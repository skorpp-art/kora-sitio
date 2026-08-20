# -*- coding: utf-8 -*-
"""
Set de iconos propio de KORA.

Criterio: la silueta exterior es convencional a propósito —un navegador, un
globo de diálogo, un teléfono— porque si no, nadie reconoce qué es. La
personalidad vive adentro: núcleos azules con nodos celestes conectados,
que es el mismo lenguaje del isotipo. Duotono en vez de contorno gris, que
es lo que hace que un icono de stock se note de lejos.

Grilla de 24. Trazo 1.7. Núcleo r≈2.2, nodo r≈1.5.
"""

AZUL = "#1E3A8A"
CYAN = "#06B6D4"


def _svg(tam, cuerpo):
    return (
        '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" '
        'aria-hidden="true" focusable="false">%s</svg>' % (tam, tam, cuerpo)
    )


# --------------------------------------------------------------------------
# Servicios
# --------------------------------------------------------------------------
def web(tam=24):
    return _svg(tam, (
        '<rect x="2.35" y="4.35" width="19.3" height="15.3" rx="3.2" stroke="%(a)s" stroke-width="1.7"/>'
        '<path d="M2.35 8.9h19.3" stroke="%(a)s" stroke-width="1.7"/>'
        '<circle cx="5.5" cy="6.6" r=".85" fill="%(a)s"/>'
        '<circle cx="8.2" cy="6.6" r=".85" fill="%(a)s"/>'
        '<path d="M8.4 14.9 16 12.3M8.4 14.9 16 17.4" stroke="%(c)s" stroke-width="1.3" stroke-linecap="round"/>'
        '<circle cx="8.4" cy="14.9" r="2.2" fill="%(a)s"/>'
        '<circle cx="16.1" cy="12.2" r="1.5" fill="%(c)s"/>'
        '<circle cx="16.1" cy="17.5" r="1.5" fill="%(c)s"/>'
    ) % {"a": AZUL, "c": CYAN})


def chatbot(tam=24):
    return _svg(tam, (
        '<path d="M5.1 3.6h13.8a2.7 2.7 0 0 1 2.7 2.7v7.8a2.7 2.7 0 0 1-2.7 2.7h-6.4l-4.9 3.6v-3.6H5.1a2.7 2.7 0 0 1-2.7-2.7V6.3a2.7 2.7 0 0 1 2.7-2.7Z" '
        'stroke="%(a)s" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M7.6 10.2h8.8" stroke="%(c)s" stroke-width="1.3" stroke-linecap="round"/>'
        '<circle cx="12" cy="10.2" r="2.3" fill="%(a)s"/>'
        '<circle cx="7.5" cy="10.2" r="1.45" fill="%(c)s"/>'
        '<circle cx="16.5" cy="10.2" r="1.45" fill="%(c)s"/>'
    ) % {"a": AZUL, "c": CYAN})


def app(tam=24):
    return _svg(tam, (
        '<rect x="6.4" y="2.35" width="11.2" height="19.3" rx="2.8" stroke="%(a)s" stroke-width="1.7"/>'
        '<path d="M9.9 8.9v8.2" stroke="%(c)s" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>'
        '<circle cx="9.9" cy="8.9" r="1.35" fill="%(c)s"/>'
        '<path d="M12.7 8.9h3.1" stroke="%(a)s" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="9.9" cy="13" r="1.35" fill="%(c)s"/>'
        '<path d="M12.7 13h3.1" stroke="%(a)s" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="9.9" cy="17.1" r="1.9" fill="%(a)s"/>'
        '<path d="M12.9 17.1h2.1" stroke="%(a)s" stroke-width="1.5" stroke-linecap="round" opacity=".35"/>'
    ) % {"a": AZUL, "c": CYAN})


# --------------------------------------------------------------------------
# Propuesta de valor
# --------------------------------------------------------------------------
def proceso(tam=22):
    return _svg(tam, (
        '<path d="M4 18.4h5.6v-6.2h5.6V6h4.4" stroke="%(a)s" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="4" cy="18.4" r="1.6" fill="%(c)s"/>'
        '<circle cx="9.6" cy="12.2" r="1.4" fill="%(c)s"/>'
        '<circle cx="15.2" cy="6" r="1.4" fill="%(c)s"/>'
        '<circle cx="19.8" cy="6" r="2.3" fill="%(a)s"/>'
    ) % {"a": AZUL, "c": CYAN})


def precio(tam=22):
    return _svg(tam, (
        '<path d="M12.9 3.15h6.15a1.8 1.8 0 0 1 1.8 1.8v6.15a1.8 1.8 0 0 1-.53 1.27l-7.1 7.1a1.8 1.8 0 0 1-2.55 0l-6.15-6.15a1.8 1.8 0 0 1 0-2.55l7.1-7.1a1.8 1.8 0 0 1 1.28-.52Z" '
        'stroke="%(a)s" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="16.5" cy="7.5" r="1.75" fill="%(c)s"/>'
    ) % {"a": AZUL, "c": CYAN})


def resultados(tam=22):
    return _svg(tam, (
        '<path d="M3.4 20.6h17.2" stroke="%(a)s" stroke-width="1.5" stroke-linecap="round" opacity=".3"/>'
        '<path d="M3.9 16.8 9.3 11.4l3.3 2.9 6.4-7.2" stroke="%(a)s" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="9.3" cy="11.4" r="1.3" fill="%(c)s"/>'
        '<circle cx="19.2" cy="7" r="2.3" fill="%(c)s"/>'
    ) % {"a": AZUL, "c": CYAN})
