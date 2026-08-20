# -*- coding: utf-8 -*-
"""
Genera img/cta-halftone.jpg — el fondo de puntos del CTA final.

Es la adaptación del motivo de firma de la referencia Caldera ("halftone
dot pattern... the system's most recognizable motif"): una imagen de
semitono que se funde de vacío a sólido en una esquina. La de la
referencia va de violeta a naranja; esta va de azul KORA a celeste, y
se genera una sola vez porque .cta usa la misma clase en el home y en
las 8 páginas que llaman a cta_final() — no hace falta regenerarla salvo
que se quieran otros focos/colores.

    cd "boceto silvia"
    python _build/generar_halftone.py
"""
import math
import random

from PIL import Image, ImageDraw

random.seed(11)

W, H = 1800, 900
BASE = (30, 58, 138)     # #1E3A8A azul KORA — el "fondo violeta" de la referencia
DOT = (6, 182, 212)      # #06B6D4 celeste — el "naranja" de la referencia
DOT_APAGADO = (14, 116, 144)   # celeste apagado, para las zonas de baja densidad

# Focos gaussianos: (x, y, sigma, peso). Sigma chico = mancha compacta,
# sigma grande = mancha difusa. Sumarlos da la variación orgánica de
# manchas que tiene un halftone real, en vez de un degradado mecánico.
FOCOS = [
    (W * 0.88, H * 0.20, 340, 1.15),   # el foco dominante, arriba a la derecha
    (W * 0.60, H * 0.65, 260, 0.85),
    (W * 0.22, H * 0.78, 200, 0.65),
]

CELDA = 16
UMBRAL = 0.05             # por debajo de esto no se dibuja nada: aire real


def campo(x, y):
    v = 0.0
    for fx, fy, sigma, peso in FOCOS:
        dist2 = (x - fx) ** 2 + (y - fy) ** 2
        v += peso * math.exp(-dist2 / (2 * sigma * sigma))
    return v


def generar(destino='img/cta-halftone.jpg'):
    # Calibrar el rango real del campo muestreando la grilla, en vez de
    # adivinar constantes de normalización a ciegas.
    muestras = [campo(x, y) for y in range(0, H, 30) for x in range(0, W, 30)]
    vmin, vmax = min(muestras), max(muestras)

    img = Image.new('RGB', (W, H), BASE)
    d = ImageDraw.Draw(img)
    max_r = CELDA * 0.58

    for gy in range(0, H + CELDA, CELDA):
        for gx in range(0, W + CELDA, CELDA):
            t = (campo(gx, gy) - vmin) / (vmax - vmin)
            t = max(0.0, t) ** 1.6          # curva: más aire en las zonas bajas
            if t <= UMBRAL:
                continue
            jx = gx + random.uniform(-2, 2)
            jy = gy + random.uniform(-2, 2)
            r = max_r * t
            color = DOT if t > 0.45 else DOT_APAGADO
            d.ellipse([jx - r, jy - r, jx + r, jy + r], fill=color)

    img.save(destino, 'JPEG', quality=88, optimize=True)
    print(f'{destino} listo — {W}x{H}')


if __name__ == '__main__':
    generar()
