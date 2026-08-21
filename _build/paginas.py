# -*- coding: utf-8 -*-
"""
Contenido de cada página. El marco (nav, footer, cabecera) sale de plantilla.py.

Para editar textos, se toca acá y se corre:  python _build/generar.py
"""
from plantilla import encabezado_pagina, cta_final, WHATSAPP


# --------------------------------------------------------------------------
# Helpers de contenido
# --------------------------------------------------------------------------
def seccion(contenido, clase="section", extra=""):
    return f'\n    <section class="{clase}" data-reveal{extra}>\n{contenido}\n    </section>'


def cabecera_seccion(eyebrow, titulo):
    return f"""      <header class="section__head">
        <span class="eyebrow">{eyebrow}</span>
        <h2 class="section__title">{titulo}</h2>
      </header>"""


def para_quien(si_lista, no_lista):
    si = "\n".join(f"          <li>{x}</li>" for x in si_lista)
    no = "\n".join(f"          <li>{x}</li>" for x in no_lista)
    return f"""      <div class="split">
        <div class="split__col split__col--si">
          <h3 class="split__titulo">Es para vos si…</h3>
          <ul class="lista-marca lista-marca--si">
{si}
          </ul>
        </div>
        <div class="split__col split__col--no">
          <h3 class="split__titulo">No es para vos si…</h3>
          <ul class="lista-marca lista-marca--no">
{no}
          </ul>
        </div>
      </div>"""


def entregables(items):
    filas = "\n".join(
        f"""        <div class="entregable">
          <h3 class="entregable__titulo">{t}</h3>
          <p class="entregable__texto">{d}</p>
        </div>"""
        for t, d in items
    )
    return f'      <div class="entregables">\n{filas}\n      </div>'


def faq(items):
    bloques = []
    for i, (q, a) in enumerate(items, 1):
        cuerpo = "\n".join(f"              <p>{p}</p>" for p in a)
        bloques.append(f"""        <div class="faq__item">
          <h3 class="faq__q">
            <button class="faq__trigger" type="button" aria-expanded="false" aria-controls="faq-{i}" id="faq-{i}-btn">
              <span>{q}</span>
              <span class="faq__icon" aria-hidden="true"></span>
            </button>
          </h3>
          <div class="faq__panel" id="faq-{i}" role="region" aria-labelledby="faq-{i}-btn">
            <div class="faq__body">
{cuerpo}
            </div>
          </div>
        </div>""")
    return '      <div class="faq">\n' + "\n".join(bloques) + "\n      </div>"


def mini_casos(casos):
    tarjetas = "\n".join(
        f"""        <a class="mini-caso" href="{a}">
          <span class="mini-caso__industria">{ind}</span>
          <span class="mini-caso__nombre">{nom}</span>
          <span class="mini-caso__metrica">{met} <em>{lab}</em></span>
          <span class="mini-caso__link">Ver el caso <span aria-hidden="true">&rarr;</span></span>
        </a>"""
        for a, ind, nom, met, lab in casos
    )
    return f'      <div class="mini-casos">\n{tarjetas}\n      </div>'


PROCESO = [
    ("1", "Brief", "Entendemos tu negocio, objetivos y público."),
    ("2", "Propuesta", "Alcance y presupuesto cerrado, sin sorpresas."),
    ("3", "Diseño", "Definimos la experiencia antes de programar nada."),
    ("4", "Desarrollo", "Construimos con avances visibles cada semana."),
    ("5", "Entrega", "Lanzamos, medimos y acompañamos el resultado."),
]


def proceso(detalle=None):
    detalle = detalle or {}
    pasos = "\n".join(
        f"""        <li class="steps__item">
          <span class="steps__n">{n}</span>
          <h3 class="steps__title">{t}</h3>
          <p class="steps__text">{detalle.get(n, d)}</p>
        </li>"""
        for n, t, d in PROCESO
    )
    return f'      <ol class="steps">\n{pasos}\n      </ol>'


AVISO_DEMO = """
<!-- =====================================================================
     CASO DE EJEMPLO — NO ES UN CLIENTE REAL

     El cliente, las cifras, los plazos y la cita de esta página son
     inventados. Sirven para que la sección exista y se vea terminada
     mientras se consiguen casos de verdad.

     Por eso la página lleva "noindex": mientras el contenido sea ficticio
     no conviene que Google lo indexe ni que aparezca en búsquedas como si
     fuera un resultado real.

     AL REEMPLAZARLO POR UN CASO REAL:
       1. Cambiar todos los textos y números por los verdaderos.
       2. Pedirle al cliente permiso por escrito para publicarlo.
       3. Borrar la línea <meta name="robots" content="noindex, follow">
          de esta página y sumarla al sitemap.xml.
       4. Sacar el cartel "Caso de ejemplo" del encabezado.
     ===================================================================== -->
"""


def cartel_demo():
    return """      <p class="aviso-demo">
        <span class="aviso-demo__pin" aria-hidden="true"></span>
        <span><strong>Caso de ejemplo.</strong> Cliente y cifras ficticios, para mostrar el formato. Los casos reales se publican con autorización del cliente.</span>
      </p>"""


# ==========================================================================
# SERVICIOS
# ==========================================================================
SERVICIO_WEB = {
    "archivo": "servicios-web.html",
    "titulo": "Desarrollo web para PyMEs — KORA",
    "desc": "Diseñamos y desarrollamos sitios y landing pages pensadas para convertir visitas en consultas. Presupuesto cerrado, entrega en 3 a 5 semanas.",
    "og_titulo": "Desarrollo web que convierte — KORA",
    "cuerpo": (
        encabezado_pagina(
            "Desarrollo web",
            "Una web que trabaja para vos, no un folleto lindo.",
            "La mayoría de las webs de PyMEs se hicieron una vez, hace años, y nadie volvió a tocarlas. Se ven bien y no traen un solo cliente. Nosotros diseñamos para que el visitante haga algo: escribir, llamar, comprar.",
        )
        + seccion(
            cabecera_seccion("A quién le sirve", "Antes de que pierdas tiempo.")
            + para_quien(
                [
                    "Tenés un negocio andando y la web no acompaña.",
                    "Vendés por WhatsApp y se te escapan pedidos fuera de horario.",
                    "Querés dejar de explicar lo mismo por teléfono diez veces por día.",
                    "Necesitás algo que puedas actualizar vos sin depender de nadie.",
                ],
                [
                    "Buscás lo más barato del mercado.",
                    "Querés la web para la semana que viene.",
                    "No tenés todavía claro qué vendés ni a quién.",
                    "Esperás que la web sola resuelva un problema comercial de fondo.",
                ],
            )
        )
        + seccion(
            cabecera_seccion("Qué incluye", "Todo lo que entra en el precio cerrado.")
            + entregables(
                [
                    ("Diseño propio", "Nada de plantillas recicladas. Se diseña sobre tu marca, tus colores y tus fotos."),
                    ("Textos que venden", "Si no los tenés, los escribimos nosotros después de entrevistarte."),
                    ("Rápida de verdad", "Optimizada para que cargue en menos de dos segundos, también con datos móviles."),
                    ("Pensada para el celular", "Se diseña primero para el teléfono, que es por donde entra la mayoría."),
                    ("Encontrable en Google", "Títulos, descripciones, datos estructurados y sitemap desde el día uno."),
                    ("Formularios que llegan", "Con aviso por mail y por WhatsApp, para que no se pierda ninguna consulta."),
                    ("Panel para editar", "Cambiás textos, precios y fotos vos, sin llamarnos."),
                    ("Todo a tu nombre", "Dominio, hosting y accesos quedan tuyos. No secuestramos nada."),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Cómo trabajamos", "Cinco etapas, siempre las mismas.")
            + proceso(
                {
                    "1": "Una reunión de 45 minutos. Salís con el problema escrito en una hoja.",
                    "2": "Alcance, fecha y precio cerrado. La propuesta vale 15 días.",
                    "3": "Ves las pantallas terminadas antes de que se programe nada. Dos rondas de cambios incluidas.",
                    "4": "Entorno de prueba online desde la primera semana para que lo veas crecer.",
                    "5": "Puesta en producción, capacitación y 30 días de soporte.",
                }
            ),
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Resultados", "Webs que hicimos y qué movieron.")
            + mini_casos(
                [
                    ("caso-ferreteria-del-sur.html", "Retail", "Ferretería Del Sur", "+40%", "pedidos mensuales"),
                    ("caso-estudio-vega.html", "Servicios profesionales", "Estudio Contable Vega", "3.2x", "más consultas"),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Preguntas frecuentes", "Sobre desarrollo web.")
            + faq(
                [
                    ("¿Cuánto tarda una web?", [
                        "Una landing o un sitio institucional está listo en <strong>3 a 5 semanas</strong>. Una tienda online, entre 8 y 12.",
                        "Lo que más demora no es programar: son los textos y las fotos. Si eso lo tenés resuelto, se acorta.",
                    ]),
                    ("¿Puedo editarla yo después?", [
                        "Sí. Te dejamos un panel para cambiar textos, precios, fotos y publicaciones, y una capacitación grabada de una hora.",
                        "Lo que no toques vos, lo podemos mantener nosotros con un acuerdo aparte.",
                    ]),
                    ("¿Sirve para aparecer en Google?", [
                        "La web sale preparada: estructura correcta, velocidad, títulos y descripciones únicos, datos estructurados y sitemap.",
                        "Ahora bien, seamos honestos: eso es la base, no un puesto garantizado. Posicionarse para términos competidos es un trabajo sostenido de contenido que se acuerda por separado.",
                    ]),
                    ("¿Y si ya tengo una web?", [
                        "Miramos qué se puede aprovechar. A veces conviene rehacerla y a veces alcanza con corregir la estructura y los textos.",
                        "Te lo decimos derecho, aunque implique un trabajo más chico para nosotros.",
                    ]),
                ]
            ),
            clase="section section--band",
        )
        + cta_final(
            "¿Arrancamos con tu web?",
            "Contanos qué necesitás y en 48 horas tenés una propuesta con alcance, fecha y precio cerrado.",
        )
    ),
}

SERVICIO_CHATBOTS = {
    "archivo": "servicios-chatbots.html",
    "titulo": "Chatbots para atención automática — KORA",
    "desc": "Chatbots para WhatsApp y web que responden consultas, califican clientes y agendan ventas las 24 horas. Integrados con tu operación.",
    "og_titulo": "Chatbots que atienden 24/7 — KORA",
    "cuerpo": (
        encabezado_pagina(
            "Chatbots",
            "El 60% de las consultas llegan cuando ya cerraste.",
            "Y la mayoría no vuelve al día siguiente: escribe al que le contesta primero. Un chatbot bien armado responde en segundos, filtra lo que no sirve y te deja la conversación lista para cerrar.",
        )
        + seccion(
            cabecera_seccion("A quién le sirve", "Antes de perder otra consulta fuera de horario.")
            + para_quien(
                [
                    "Te llegan muchas consultas repetidas: precios, horarios, stock, envíos.",
                    "Perdés ventas fuera del horario comercial o los fines de semana.",
                    "Alguien del equipo pasa el día entero contestando WhatsApp.",
                    "Querés saber cuántas consultas entran y de qué son.",
                ],
                [
                    "Recibís dos o tres consultas por semana: no justifica la inversión.",
                    "Tu venta es 100% consultiva y cada caso es distinto.",
                    "Buscás un robot que reemplace a todo el equipo. No es eso.",
                    "No tenés a nadie que pueda retomar la conversación cuando el bot la derive.",
                ],
            )
        )
        + seccion(
            cabecera_seccion("Qué incluye", "Lo que incluye tu chatbot, sin sorpresas después.")
            + entregables(
                [
                    ("En WhatsApp y en la web", "El mismo bot atendiendo en los dos canales, con la misma información."),
                    ("Guion armado con vos", "Relevamos las preguntas que ya te hacen y armamos las respuestas juntos."),
                    ("Derivación a una persona", "Cuando la consulta se complica, pasa a un humano sin que el cliente lo note."),
                    ("Califica antes de derivar", "Te llega la conversación con el presupuesto, la zona y la urgencia ya preguntados."),
                    ("Conectado a tu sistema", "Puede consultar stock, precios o turnos si tenés dónde consultarlos."),
                    ("Panel de conversaciones", "Ves todo lo que se habló, qué se preguntó más y qué no supo responder."),
                    ("Horarios y respaldo", "Fuera de hora avisa cuándo van a responder, en vez de dejar en visto."),
                    ("Ajustes del primer mes", "Los primeros treinta días afinamos las respuestas con casos reales."),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Cómo trabajamos", "Mismo proceso de siempre, aplicado a tu chatbot.")
            + proceso(
                {
                    "1": "Revisamos tus conversaciones reales para ver qué se pregunta de verdad.",
                    "2": "Alcance, canales, integraciones y precio cerrado.",
                    "3": "Diseñamos el guion completo y lo aprobás antes de que se programe.",
                    "4": "Lo armamos y lo probás vos mismo desde tu teléfono.",
                    "5": "Sale en vivo y durante 30 días ajustamos con casos reales.",
                }
            ),
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Resultados", "Un caso con chatbot adentro.")
            + mini_casos(
                [
                    ("caso-ferreteria-del-sur.html", "Retail", "Ferretería Del Sur", "+40%", "pedidos mensuales"),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Preguntas frecuentes", "Sobre chatbots.")
            + faq(
                [
                    ("¿Es un bot con inteligencia artificial?", [
                        "Depende de lo que necesites, y te lo decimos sin vender humo.",
                        "Para preguntas repetidas y acotadas, un bot por reglas es más barato, más rápido y no se inventa respuestas. Cuando hace falta entender consultas abiertas, sumamos un modelo de lenguaje con tu información como fuente y límites claros para que no improvise.",
                    ]),
                    ("¿Le va a hablar mal a mis clientes?", [
                        "Ese es el miedo razonable y por eso el guion se aprueba antes. El bot no sale a improvisar: responde lo que definimos y, ante cualquier cosa que no reconoce, deriva a una persona en vez de arriesgar.",
                    ]),
                    ("¿Necesito una línea de WhatsApp aparte?", [
                        "Sí, conviene una línea dedicada con WhatsApp Business API. Te ayudamos con el trámite de verificación de la empresa, que suele tardar unos días.",
                        "Tu número personal puede seguir funcionando aparte.",
                    ]),
                    ("¿Qué pasa si el bot no sabe algo?", [
                        "Deriva a una persona y te deja la conversación con el contexto completo. Además queda registrado como pregunta sin responder para que la sumemos al guion.",
                        "Un bot bien mantenido mejora todos los meses.",
                    ]),
                ]
            ),
            clase="section section--band",
        )
        + cta_final(
            "¿Cuántas consultas estás perdiendo?",
            "Contanos cuántos mensajes recibís por semana y te decimos si un chatbot te conviene o no.",
            boton="Quiero dejar de perderlas",
        )
    ),
}

SERVICIO_APPS = {
    "archivo": "servicios-apps.html",
    "titulo": "Apps y software a medida — KORA",
    "desc": "Aplicaciones y sistemas a medida para gestionar tu operación o llegar a tus clientes. Cuando el Excel y las planillas compartidas ya no alcanzan.",
    "og_titulo": "Apps a medida para tu operación — KORA",
    "cuerpo": (
        encabezado_pagina(
            "Apps a medida",
            "Cuando el Excel ya no da más.",
            "Casi todas las PyMEs llegan a un punto donde la operación vive en cinco planillas, un grupo de WhatsApp y la cabeza de una persona. Ahí es donde conviene un sistema propio, hecho a la medida de cómo trabajás.",
        )
        + seccion(
            cabecera_seccion("A quién le sirve", "Antes de que el Excel se rompa del todo.")
            + para_quien(
                [
                    "Tu operación depende de planillas que se pisan entre sí.",
                    "Cargás la misma información en tres lugares distintos.",
                    "Necesitás que tu equipo trabaje desde el celular, en la calle o en el depósito.",
                    "Probaste un software enlatado y te obliga a trabajar como no trabajás.",
                ],
                [
                    "Un sistema de los que ya existen te resuelve el 90%: te conviene ese.",
                    "Todavía estás definiendo cómo funciona el proceso.",
                    "Necesitás algo funcionando el mes que viene.",
                    "Nadie del equipo va a poder dedicarle tiempo a probarlo.",
                ],
            )
        )
        + seccion(
            cabecera_seccion("Qué incluye", "Lo que incluye tu sistema, de punta a punta.")
            + entregables(
                [
                    ("Relevamiento en tu lugar", "Vamos, miramos cómo trabajan hoy y anotamos. No se diseña de memoria."),
                    ("Funciona en el celular", "Se usa desde el teléfono, la tablet o la computadora, con la misma cuenta."),
                    ("Anda sin señal", "Si el depósito no tiene datos, sigue funcionando y sincroniza después."),
                    ("Usuarios y permisos", "Cada uno ve lo suyo. El dueño ve todo."),
                    ("Conectada a lo que ya usás", "Facturación, medios de pago, planillas o el sistema de gestión que tengas."),
                    ("Reportes de verdad", "Los números que mirás para decidir, no un tablero lleno de gráficos inútiles."),
                    ("Capacitación al equipo", "Formamos a quien la va a usar, no sólo a quien la contrató."),
                    ("Código y datos tuyos", "Te entregamos el código y la base. No quedás atado a nosotros."),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Cómo trabajamos", "Mismas cinco etapas, ahora para tu sistema.")
            + proceso(
                {
                    "1": "Relevamiento en tu lugar de trabajo, con la gente que lo va a usar.",
                    "2": "Alcance por etapas y precio cerrado por cada una.",
                    "3": "Prototipo navegable que probás antes de que exista una línea de código.",
                    "4": "Entregas cada dos semanas, usables, no demos.",
                    "5": "Puesta en marcha, capacitación y acompañamiento del primer mes real.",
                }
            ),
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Resultados", "Una app que cambió una operación.")
            + mini_casos(
                [
                    ("caso-nutri-delivery.html", "Alimentos", "Nutrí Delivery", "-60%", "tiempo por pedido"),
                ]
            )
        )
        + seccion(
            cabecera_seccion("Preguntas frecuentes", "Sobre apps a medida.")
            + faq(
                [
                    ("¿Va a estar en la App Store?", [
                        "Depende de para quién sea. Si es para tu equipo interno, casi siempre conviene una app web que se instala en el teléfono sin pasar por las tiendas: más barata, y las actualizaciones son inmediatas.",
                        "Si es para tus clientes finales y necesitás notificaciones o cámara, ahí sí publicamos en App Store y Google Play, con el trámite incluido.",
                    ]),
                    ("¿Cuánto cuesta mantenerla?", [
                        "Hay un costo de infraestructura mensual, que en proyectos de este tamaño suele ser bajo, y un mantenimiento opcional para mejoras y soporte.",
                        "Los dos números te los damos en la propuesta, antes de arrancar. No aparecen después.",
                    ]),
                    ("¿Se puede hacer por partes?", [
                        "Es lo que recomendamos. Arrancamos por lo que más duele, lo ponés a andar, y recién después seguimos con el resto.",
                        "Cada etapa tiene su propio precio cerrado y podés frenar cuando quieras.",
                    ]),
                    ("¿Qué pasa si mañana no trabajamos más juntos?", [
                        "Te entregamos el código fuente, la base de datos y la documentación. Cualquier desarrollador puede seguir.",
                        "Usamos tecnologías conocidas justamente por eso: para que no dependas de nosotros.",
                    ]),
                ]
            ),
            clase="section section--band",
        )
        + cta_final(
            "Contanos cómo trabajás hoy.",
            "Con media hora de charla ya podemos decirte si conviene un sistema a medida o si te sirve algo que ya existe.",
            boton="Contarles cómo trabajo",
        )
    ),
}


# ==========================================================================
# CASOS
# ==========================================================================
def caso(archivo, industria, nombre, metrica, metrica_label, resumen,
         problema, decisiones, solucion, resultados, cita, autor, cargo,
         servicios, imagen, alt):
    filas_res = "\n".join(
        f"""        <div class="resultado">
          <p class="resultado__valor">{v}</p>
          <p class="resultado__label">{l}</p>
        </div>"""
        for v, l in resultados
    )
    lista_serv = "\n".join(f'          <li><a href="{a}">{t}</a></li>' for a, t in servicios)
    bloques_dec = "\n".join(
        f"""        <div class="decision">
          <h3 class="decision__titulo">{t}</h3>
          <p class="decision__texto">{d}</p>
        </div>"""
        for t, d in decisiones
    )

    cuerpo = f"""
    <section class="caso-hero">
      <div class="caso-hero__inner">
{cartel_demo()}
        <span class="eyebrow">{industria}</span>
        <h1 class="caso-hero__titulo">{nombre}</h1>
        <p class="caso-hero__resumen">{resumen}</p>
        <p class="caso-hero__metrica"><span>{metrica}</span> {metrica_label}</p>
      </div>
      <figure class="caso-hero__figura">
        <img src="img/{imagen}" alt="{alt}" width="800" height="560" loading="eager">
      </figure>
    </section>

    <section class="section" data-reveal>
      <div class="caso-cuerpo">
        <div class="prose">
          <h2>El problema</h2>
          {problema}

          <h2>Qué decidimos y por qué</h2>
          <p>Acá está el criterio, que es lo que más se parece a lo que haríamos con tu proyecto:</p>
        </div>
{bloques_dec}
        <div class="prose">
          <h2>La solución</h2>
          {solucion}
        </div>
      </div>
    </section>

    <section class="section section--band" data-reveal>
      <div class="section__inner">
{cabecera_seccion("Resultados", "Qué se movió, con qué medida.")}
        <div class="resultados">
{filas_res}
        </div>
        <p class="resultados__nota">Cifras de ejemplo. En un caso real acá va de dónde sale cada número y en qué período se midió.</p>

        <figure class="cita-caso">
          <blockquote>{cita}</blockquote>
          <figcaption><strong>{autor}</strong> · {cargo}</figcaption>
        </figure>
      </div>
    </section>

    <section class="section" data-reveal>
      <div class="caso-pie">
        <div>
          <h2 class="caso-pie__titulo">Servicios que usamos</h2>
          <ul class="caso-pie__servicios">
{lista_serv}
          </ul>
        </div>
        <a class="link-underline" href="casos.html">Ver todos los casos</a>
      </div>
    </section>
""" + cta_final(
        "¿Tenés un problema parecido?",
        "Contanos en qué estás y te decimos si podemos ayudarte, con una propuesta concreta en 48 horas.",
        boton="Contarles mi caso",
    )

    return {
        "archivo": archivo,
        "titulo": f"{nombre} — Caso de ejemplo — KORA",
        "desc": f"{resumen}",
        "noindex": "Caso de ejemplo con datos ficticios: no debe indexarse hasta ser reemplazado por un caso real. Ver el aviso al inicio del body.",
        "aviso": AVISO_DEMO,
        "og_tipo": "article",
        "cuerpo": cuerpo,
    }


CASO_FERRETERIA = caso(
    "caso-ferreteria-del-sur.html", "Retail", "Ferretería Del Sur",
    "+40%", "pedidos mensuales",
    "Una ferretería de barrio que vendía sólo por WhatsApp pasó a tener catálogo online con carrito y un chatbot que atiende de noche.",
    """<p>Del Sur vende ferretería y sanitarios en el conurbano desde hace más de veinte años. Toda la venta que no era mostrador pasaba por un único WhatsApp que atendía la dueña.</p>
          <p>El problema no era la falta de consultas: eran demasiadas y desordenadas. Cada pedido implicaba tres o cuatro idas y vueltas para confirmar si había stock, cuánto salía y cómo se pagaba. Las consultas que entraban después de las 19 se contestaban al otro día, y para entonces buena parte ya había comprado en otro lado.</p>""",
    [
        ("Catálogo antes que tienda completa", "No arrancamos por el carrito. Primero pusimos el catálogo con precios y stock visibles, porque la mitad de los mensajes eran justamente para preguntar eso. Bajó el volumen de consultas antes de vender un solo producto online."),
        ("Stock por sucursal, no total", "Mostrar un stock general hubiera generado pedidos imposibles de cumplir. Se muestra por sucursal, aunque sea más difícil de mantener: es peor prometer y fallar que mostrar menos."),
        ("El chatbot atiende, no vende", "Se limitó a responder precio, stock, horarios y envíos, y a derivar todo lo demás. Un bot que intenta cerrar ventas complejas de ferretería iba a dar respuestas equivocadas."),
    ],
    """<p>Un catálogo de 120 productos con búsqueda, filtros y stock por sucursal, carrito con retiro en local o envío, y un chatbot en la web y en WhatsApp que responde las cuatro preguntas de siempre y deriva el resto con el contexto ya cargado.</p>
          <p>La carga de productos quedó en manos del equipo, con un panel simple y una capacitación de una hora.</p>""",
    [("+40%", "pedidos mensuales"), ("-65%", "consultas repetidas"), ("3 sem.", "de desarrollo"), ("24/7", "atención automática")],
    "Antes vivíamos contestando lo mismo todo el día. Ahora el que pregunta el precio lo ve en la web, y el que escribe de noche recibe respuesta igual.",
    "Marina Gómez", "Dueña, Ferretería Del Sur",
    [("servicios-web.html", "Desarrollo web"), ("servicios-chatbots.html", "Chatbots")],
    "case-ferreteria.svg",
    "Tienda online de Ferretería Del Sur: catálogo de productos con buscador, filtros, carrito y el widget del chatbot de atención.",
)

CASO_VEGA = caso(
    "caso-estudio-vega.html", "Servicios profesionales", "Estudio Contable Vega",
    "3.2x", "más consultas",
    "Un estudio contable con una web de 2015 que no generaba una sola consulta pasó a recibir pedidos calificados todas las semanas.",
    """<p>El estudio Vega atiende monotributistas y PyMEs. Su web era de 2015: tres pestañas, un listado de servicios en viñetas y un formulario que nadie completaba.</p>
          <p>El problema real no era el diseño viejo, era que la web no decía nada que un contador cualquiera no dijera. No había motivo para elegirlos a ellos, y la gente que entraba se iba a pedir recomendaciones a un conocido.</p>""",
    [
        ("Menos servicios, más específicos", "La web listaba catorce servicios. Los redujimos a tres, los que efectivamente querían vender. Listar todo es la forma más rápida de no ser recordado por nada."),
        ("Casos en vez de adjetivos", "Reemplazamos “atención personalizada y profesional” por situaciones concretas: qué hacer si te pasaron a responsable inscripto, cómo ordenar la contabilidad atrasada. La gente busca su problema, no tu rubro."),
        ("Formulario que califica", "Pasamos de un campo de mensaje libre a cuatro preguntas cortas. Entran menos consultas pero llegan listas para presupuestar, y el estudio dejó de perder horas en llamadas que no iban a ningún lado."),
    ],
    """<p>Una landing con foco en tres servicios, textos escritos a partir de dos entrevistas con los socios, casos de situaciones reales y un formulario de cuatro preguntas que llega por mail y por WhatsApp.</p>
          <p>Se sumaron datos estructurados y fichas por servicio para que cada uno pueda encontrarse por separado en Google.</p>""",
    [("3.2x", "más consultas"), ("+80%", "consultas calificadas"), ("4 sem.", "de desarrollo"), ("2 min", "para completar el formulario")],
    "Dejamos de recibir mensajes de dos palabras. Ahora llega la consulta con el contexto y ya sabemos si podemos ayudar antes de llamar.",
    "Roberto Vega", "Socio, Estudio Contable Vega",
    [("servicios-web.html", "Desarrollo web")],
    "case-vega.svg",
    "Landing page del Estudio Contable Vega: titular, llamado a la acción, gráfico de consultas mensuales en crecimiento y tarjetas de servicios.",
)

CASO_NUTRI = caso(
    "caso-nutri-delivery.html", "Alimentos", "Nutrí Delivery",
    "-60%", "tiempo por pedido",
    "Una cocina de viandas saludables que tomaba pedidos por teléfono pasó a una app propia con seguimiento y pagos integrados.",
    """<p>Nutrí prepara y reparte viandas semanales. Los pedidos se tomaban por teléfono y WhatsApp, se anotaban en un cuaderno y se pasaban a una planilla para armar las rutas de reparto.</p>
          <p>Con 40 pedidos por semana funcionaba. Con 150 se rompió: pedidos mal anotados, viandas que llegaban al domicilio equivocado y una persona dedicada full time a copiar información de un lado a otro.</p>""",
    [
        ("App web, no app de tienda", "No publicamos en App Store ni en Google Play. Una app web instalable evitó el trámite de las tiendas y permitió actualizar el mismo día, que era lo que hacía falta en las primeras semanas."),
        ("Primero el pedido, después el seguimiento", "La primera entrega resolvió sólo la toma de pedidos, que era donde se perdía plata. El seguimiento del reparto llegó recién en la segunda etapa, ya con la operación estabilizada."),
        ("Funciona sin señal", "Los repartidores pierden datos en varias zonas. La app guarda las entregas en el teléfono y sincroniza cuando vuelve la señal, en vez de pedirles que anoten en papel."),
    ],
    """<p>Una app de pedidos con menú semanal, suscripción, pagos integrados y confirmación automática, más una vista para repartidores con la ruta del día y el estado de cada entrega.</p>
          <p>Del lado de la cocina, un panel que arma la lista de producción del día a partir de los pedidos cerrados.</p>""",
    [("-60%", "tiempo por pedido"), ("-90%", "errores de reparto"), ("10 sem.", "en dos etapas"), ("150+", "pedidos semanales")],
    "Sacamos a una persona de copiar pedidos y la pusimos a producir. Eso solo ya pagó el desarrollo.",
    "Lucía Paz", "Fundadora, Nutrí Delivery",
    [("servicios-apps.html", "Apps a medida")],
    "case-nutri.svg",
    "App de Nutrí Delivery: pantalla de pedido con ítems y total, y pantalla de seguimiento del envío en el mapa con tiempo estimado.",
)


# --------------------------------------------------------------------------
# Listado de casos
# --------------------------------------------------------------------------
CASOS_LISTA = {
    "archivo": "casos.html",
    "titulo": "Casos — KORA",
    "desc": "Proyectos de KORA con el problema, la decisión de diseño y el resultado de cada uno.",
    "cuerpo": (
        encabezado_pagina(
            "Casos",
            "Cada caso, con el problema, la decisión y el resultado.",
            "Nada de antes/después con filtro. Contamos qué pasaba, qué decidimos y por qué, y qué se movió después — con números.",
            cta=False,
        )
        + seccion(
            """      <p class="aviso-demo aviso-demo--ancho">
        <span class="aviso-demo__pin" aria-hidden="true"></span>
        <span><strong>Casos de ejemplo.</strong> Estamos armando esta sección con clientes reales. Mientras tanto, los tres de abajo muestran el formato y el nivel de detalle con el que documentamos cada proyecto.</span>
      </p>"""
            + """      <div class="cases">
        <article class="case">
          <div class="case__shot">
            <img src="img/case-ferreteria.svg" alt="Tienda online de Ferretería Del Sur con catálogo, carrito y chatbot." loading="lazy" width="800" height="560">
          </div>
          <div class="case__body">
            <div>
              <span class="case__industry">Retail</span>
              <h2 class="case__name">Ferretería Del Sur</h2>
            </div>
            <p class="case__text">Vendían sólo por WhatsApp y perdían pedidos fuera de horario. Catálogo con stock por sucursal y chatbot de atención.</p>
            <div class="case__footer">
              <p class="case__metric"><span class="case__metric-value">+40%</span> <span class="case__metric-label">pedidos mensuales</span></p>
              <a class="case__link" href="caso-ferreteria-del-sur.html">Ver caso completo <span aria-hidden="true">&rarr;</span></a>
            </div>
          </div>
        </article>

        <article class="case">
          <div class="case__shot">
            <img src="img/case-vega.svg" alt="Landing del Estudio Contable Vega con gráfico de consultas en alza." loading="lazy" width="800" height="560">
          </div>
          <div class="case__body">
            <div>
              <span class="case__industry">Servicios profesionales</span>
              <h2 class="case__name">Estudio Contable Vega</h2>
            </div>
            <p class="case__text">Web desactualizada y cero consultas nuevas. Landing enfocada en tres servicios con formulario que califica.</p>
            <div class="case__footer">
              <p class="case__metric"><span class="case__metric-value">3.2x</span> <span class="case__metric-label">más consultas</span></p>
              <a class="case__link" href="caso-estudio-vega.html">Ver caso completo <span aria-hidden="true">&rarr;</span></a>
            </div>
          </div>
        </article>

        <article class="case">
          <div class="case__shot">
            <img src="img/case-nutri.svg" alt="App de Nutrí Delivery con pedido y seguimiento del reparto." loading="lazy" width="800" height="560">
          </div>
          <div class="case__body">
            <div>
              <span class="case__industry">Alimentos</span>
              <h2 class="case__name">Nutrí Delivery</h2>
            </div>
            <p class="case__text">Pedidos por teléfono anotados en un cuaderno. App propia con menú semanal, pagos y seguimiento de reparto.</p>
            <div class="case__footer">
              <p class="case__metric"><span class="case__metric-value">-60%</span> <span class="case__metric-label">tiempo por pedido</span></p>
              <a class="case__link" href="caso-nutri-delivery.html">Ver caso completo <span aria-hidden="true">&rarr;</span></a>
            </div>
          </div>
        </article>
      </div>"""
        )
        + cta_final(
            "¿Querés ser el próximo?",
            "Contanos tu problema y te decimos con qué lo resolveríamos, sin vueltas.",
            boton="Quiero ser el próximo",
        )
    ),
}
