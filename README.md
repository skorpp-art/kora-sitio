# KORA — sitio

Sitio estático de KORA, agencia de desarrollo digital para PyMEs argentinas.
Trece páginas de HTML puro: se suben tal cual y no necesitan build en el
servidor.

## Cómo está armado

| Archivo | Qué es |
| --- | --- |
| `kora.css` | Sistema visual completo — una sola hoja para las trece páginas |
| `kora.js` | Todo el comportamiento: navegación, FAQ, formulario, animaciones |
| `vendor/gsap/` | GSAP + ScrollTrigger self-hosteados (no CDN) |
| `_build/` | Generador de las páginas |
| `vercel.json` | Config del deploy. Manda `X-Robots-Tag: noindex` en todo el sitio, porque mientras los casos sean ficticios no conviene que Google los indexe. **Sacar esa cabecera antes de salir a producción de verdad.** |

Las páginas HTML de la raíz **se generan**, no se editan a mano:

```bash
python _build/generar.py
```

Eso vuelve a escribir las trece páginas y el `sitemap.xml` a partir de
`_build/plantilla.py` (nav, pie, cabecera) y `_build/paginas*.py`
(contenido). Si editás un `.html` de la raíz, el próximo generador te lo
pisa.

## Dos reglas que conviene no romper

**Todo visible sin JavaScript.** Ningún estado oculto vive en CSS: los pone
`kora.js` en tiempo de ejecución, y cada función que usa GSAP arranca con
`if (!GSAP_OK) return;`. Si GSAP no carga, la página se ve entera igual.
Está probado bloqueando los archivos, no asumido.

**Nada servido por terceros.** GSAP va self-hosteado en `vendor/`. La única
excepción es Inter Tight, que viene de Google Fonts.

## Antes de usarlo en producción

Este repo todavía tiene datos de ejemplo:

- Número de WhatsApp de prueba (`5491100000000`) en `_build/plantilla.py`
- CUIT de ejemplo (`30-00000000-0`) en el pie
- Los tres casos de éxito son **ficticios** — llevan `noindex` y un cartel
  que lo aclara
- Los rangos de precio dicen "A completar" (`_build/paginas_b.py`)
- El dominio de las etiquetas canónicas y Open Graph es `kora.com.ar`
- La política de privacidad es una base genérica, no asesoramiento legal
