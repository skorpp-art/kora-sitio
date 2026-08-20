# -*- coding: utf-8 -*-
"""Nosotros, Precios y Contacto."""
from plantilla import encabezado_pagina, cta_final, EMAIL, WHATSAPP, WA_TEXTO
from paginas import seccion, cabecera_seccion, faq, proceso


# --------------------------------------------------------------------------
# Formulario reutilizable
# --------------------------------------------------------------------------
def formulario():
    return f"""        <div class="form-card">
          <form class="form" id="form-contacto" data-contact-form novalidate
                action="mailto:{EMAIL}" method="post" enctype="text/plain">
            <p class="form__title">Contanos qué necesitás</p>

            <div class="field">
              <label class="field__label" for="c-nombre">Nombre y apellido <span class="field__req" aria-hidden="true">*</span></label>
              <input class="field__input" type="text" id="c-nombre" name="nombre" autocomplete="name" required aria-describedby="c-nombre-error">
              <p class="field__error" id="c-nombre-error" data-error-for="nombre"></p>
            </div>

            <div class="field-row">
              <div class="field">
                <label class="field__label" for="c-email">Email <span class="field__req" aria-hidden="true">*</span></label>
                <input class="field__input" type="email" id="c-email" name="email" autocomplete="email" required aria-describedby="c-email-error">
                <p class="field__error" id="c-email-error" data-error-for="email"></p>
              </div>
              <div class="field">
                <label class="field__label" for="c-tel">Teléfono / WhatsApp</label>
                <input class="field__input" type="tel" id="c-tel" name="telefono" autocomplete="tel" placeholder="11 0000-0000">
              </div>
            </div>

            <div class="field">
              <label class="field__label" for="c-tipo">¿Qué estás buscando?</label>
              <select class="field__input field__input--select" id="c-tipo" name="tipo">
                <option value="Web">Una web o landing page</option>
                <option value="Chatbot">Un chatbot de atención</option>
                <option value="App">Una app a medida</option>
                <option value="Rediseño">Rediseñar lo que ya tengo</option>
                <option value="No estoy seguro">Todavía no lo tengo claro</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="c-mensaje">Contanos brevemente <span class="field__req" aria-hidden="true">*</span></label>
              <textarea class="field__input field__input--area" id="c-mensaje" name="mensaje" rows="4" required aria-describedby="c-mensaje-error"
                        placeholder="Qué hace tu negocio, qué necesitás resolver y para cuándo."></textarea>
              <p class="field__error" id="c-mensaje-error" data-error-for="mensaje"></p>
            </div>

            <div class="form__honeypot" aria-hidden="true">
              <label for="c-web">No completar</label>
              <input type="text" id="c-web" name="web" tabindex="-1" autocomplete="off">
            </div>

            <button class="btn btn--accent btn--block" type="submit" data-submit>Enviar consulta</button>
            <p class="form__note">Te respondemos en menos de 24 horas hábiles. Sin spam, sin listas de correo. Al enviar aceptás nuestra <a href="privacidad.html">política de privacidad</a>.</p>
          </form>

          <div class="form-success" data-form-success hidden role="status" aria-live="polite">
            <span class="form-success__mark" aria-hidden="true">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" focusable="false">
                <path d="m4 12.5 5.5 5.5L20 7" stroke-linecap="round" stroke-linejoin="round"></path>
              </svg>
            </span>
            <p class="form-success__title">¡Listo, recibimos tu consulta!</p>
            <p class="form-success__text" data-success-text>Te escribimos a tu casilla dentro de las próximas 24 horas hábiles.</p>
            <button class="link-button" type="button" data-form-reset>Enviar otra consulta</button>
          </div>
        </div>"""


# ==========================================================================
# NOSOTROS
# ==========================================================================
AVISO_EQUIPO = """
<!-- =====================================================================
     FOTOS DEL EQUIPO — PENDIENTE

     Los integrantes de abajo están con iniciales en lugar de foto, y los
     nombres son de ejemplo. Reemplazar por las personas reales.

     Sobre las fotos: que sean fotos de verdad, sacadas el mismo día, con
     el mismo fondo y encuadre. No hace falta un estudio; con luz de
     ventana y un celular alcanza.

     Lo que NO conviene: fotos de banco de imágenes ni retratos generados
     con IA. En una agencia chica, la foto del equipo existe justamente
     para probar que atrás hay gente real. Una foto falsa consigue lo
     contrario de lo que busca.
     ===================================================================== -->
"""


def integrante(iniciales, nombre, rol, texto):
    return f"""        <article class="persona">
          <span class="persona__avatar" aria-hidden="true">{iniciales}</span>
          <h3 class="persona__nombre">{nombre}</h3>
          <p class="persona__rol">{rol}</p>
          <p class="persona__texto">{texto}</p>
        </article>"""


NOSOTROS = {
    "archivo": "nosotros.html",
    "titulo": "Nosotros — KORA",
    "desc": "Quiénes somos, por qué trabajamos con presupuesto cerrado y proceso fijo, y cómo es trabajar con KORA.",
    "og_titulo": "Quiénes somos — KORA",
    "aviso": AVISO_EQUIPO,
    "cuerpo": (
        encabezado_pagina(
            "Nosotros",
            "Somos chicos, y eso es parte de la propuesta.",
            "No somos una agencia con veinte personas donde tu proyecto lo termina haciendo un pasante. El que te atiende en la primera reunión es el que va a estar en el proyecto.",
            cta=False,
        )
        + seccion(
            cabecera_seccion("Por qué trabajamos así", "Tres decisiones que tomamos a propósito.")
            + """      <div class="tesis">
        <article class="tesis__item">
          <h3 class="tesis__titulo">Presupuesto cerrado, nunca por hora</h3>
          <p class="tesis__texto">Cobrar por hora te traslada a vos el riesgo de que nos equivoquemos calculando. Nos parece al revés: el riesgo del cálculo es nuestro. Vos necesitás saber cuánto vas a pagar antes de decidir, no después.</p>
          <p class="tesis__texto">La contra es que nos obliga a entender bien el problema antes de dar un número. Por eso la primera reunión es larga y hacemos preguntas incómodas.</p>
        </article>
        <article class="tesis__item">
          <h3 class="tesis__titulo">Diseñamos antes de programar</h3>
          <p class="tesis__texto">La mayoría de los proyectos que salen mal no salen mal por el código: salen mal porque nadie se puso de acuerdo en qué se estaba construyendo.</p>
          <p class="tesis__texto">Ver las pantallas terminadas antes de escribir una línea cuesta una semana más al principio y ahorra tres al final. Además te da la posibilidad real de decir “esto no era lo que pensaba” cuando cambiarlo todavía es barato.</p>
        </article>
        <article class="tesis__item">
          <h3 class="tesis__titulo">Te entregamos todo a tu nombre</h3>
          <p class="tesis__texto">Dominio, hosting, código y accesos quedan tuyos. Si mañana querés seguir con otro, podés, y no tenés que pedirnos permiso ni esperar nuestra buena voluntad.</p>
          <p class="tesis__texto">Usamos tecnologías conocidas justamente para eso: para que cualquier desarrollador pueda continuar sin arqueología.</p>
        </article>
      </div>"""
        )
        + seccion(
            cabecera_seccion("El equipo", "Quiénes vamos a estar en tu proyecto.")
            + """      <p class="aviso-demo aviso-demo--ancho">
        <span class="aviso-demo__pin" aria-hidden="true"></span>
        <span><strong>Sección en armado.</strong> Faltan las fotos y los datos reales del equipo. Los nombres de abajo son de ejemplo.</span>
      </p>"""
            + '      <div class="equipo">\n'
            + integrante("SA", "Silvia A.", "Dirección y diseño",
                         "Lleva la relación con el cliente y define la experiencia antes de que se programe nada. Es quien está en la primera reunión y en la entrega.")
            + "\n"
            + integrante("LF", "Lucas F.", "Desarrollo",
                         "Construye lo que se diseñó y se ocupa de que ande rápido, en cualquier teléfono y con mala señal. También arma las integraciones.")
            + "\n      </div>",
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Cómo trabajamos", "Cinco etapas, siempre las mismas.")
            + proceso()
            + """      <p class="nota-proceso">Ninguna etapa arranca sin que la anterior esté aprobada por vos. Si en algún punto querés frenar, frenamos: pagás lo hecho hasta ahí y te llevás los entregables.</p>"""
        )
        + seccion(
            cabecera_seccion("Con qué trabajamos", "Sin misticismo tecnológico.")
            + """      <div class="prose prose--ancho">
        <p>Elegimos herramientas conocidas y aburridas a propósito. Una tecnología de moda te deja en dos años con un sistema que nadie sabe mantener y que te obliga a rehacer todo.</p>
        <p>Trabajamos con desarrollo web estándar, bases de datos relacionales, plataformas de hosting administrado y las APIs oficiales de WhatsApp y de los medios de pago locales. Cuando un proyecto necesita algo distinto, te explicamos por qué antes de proponerlo.</p>
        <p>Y si lo que necesitás lo resuelve mejor un producto que ya existe que un desarrollo a medida, te lo decimos, aunque signifique no vender el proyecto.</p>
      </div>""",
            clase="section section--band",
        )
        + cta_final(
            "¿Charlamos?",
            "Media hora alcanza para que sepamos si podemos ayudarte y para que vos sepas cómo trabajamos.",
            boton="Agendar una charla",
        )
    ),
}


# ==========================================================================
# PRECIOS
# ==========================================================================
AVISO_PRECIOS = """
<!-- =====================================================================
     PRECIOS — FALTAN LOS NÚMEROS

     Los rangos están como "A completar" a propósito: poner un número
     inventado sería peor que dejarlo vacío, porque es un compromiso
     comercial que después hay que sostener.

     PARA COMPLETAR: buscar en esta página los tres <span class="precio__valor">
     y reemplazar "A completar" por el rango real.

     Dos sugerencias, por si sirven:
       · Un rango ("de X a Y") funciona mejor que un "desde X" solo: el
         "desde" siempre se lee como el precio final y después decepciona.
       · Si la inflación complica publicar pesos, se puede expresar en
         dólares o en una unidad indexada y aclararlo al lado.
     ===================================================================== -->
"""


def plan(nombre, para, precio, plazo, incluye, destacado=False):
    items = "\n".join(f"          <li>{x}</li>" for x in incluye)
    clase = "plan plan--destacado" if destacado else "plan"
    etiqueta = '\n        <span class="plan__etiqueta">El más pedido</span>' if destacado else ""
    return f"""      <article class="{clase}">{etiqueta}
        <h3 class="plan__nombre">{nombre}</h3>
        <p class="plan__para">{para}</p>
        <p class="plan__precio"><span class="precio__valor">{precio}</span></p>
        <p class="plan__plazo">{plazo}</p>
        <ul class="plan__incluye">
{items}
        </ul>
        <a class="btn btn--primary btn--block" href="contacto.html">Pedir presupuesto</a>
      </article>"""


PRECIOS = {
    "archivo": "precios.html",
    "titulo": "Precios y cómo cobramos — KORA",
    "desc": "Cómo cobramos en KORA: presupuesto cerrado antes de arrancar, nunca por hora. Qué mueve el precio, qué está incluido y cómo son los pagos.",
    "og_titulo": "Cómo cobramos — KORA",
    "aviso": AVISO_PRECIOS,
    "cuerpo": (
        encabezado_pagina(
            "Precios",
            "Cuánto sale, explicado sin vueltas.",
            "Casi ninguna agencia publica precios. Nosotros preferimos que sepas de entrada si estamos en el mismo rango, en vez de que los dos perdamos una reunión para descubrir que no.",
            cta=False,
        )
        + seccion(
            cabecera_seccion("El modelo", "Presupuesto cerrado, nunca por hora.")
            + """      <div class="prose prose--ancho">
        <p>Después de la primera reunión te pasamos un número cerrado y una fecha. Ese número no se mueve, salvo que vos pidas agregar algo que no estaba en el alcance — y en ese caso lo cotizamos aparte antes de hacerlo, nunca al final.</p>
        <p>Si nos equivocamos calculando, el problema es nuestro y lo absorbemos. Nos parece que el riesgo del cálculo tiene que estar del lado del que hace el cálculo.</p>
      </div>"""
        )
        + seccion(
            cabecera_seccion("Rangos", "Tres formas de arrancar.")
            + '      <div class="planes">\n'
            + plan("Landing", "Una página para presentar un servicio o una campaña puntual.",
                   "A completar", "3 semanas",
                   ["Una página, diseño propio", "Textos escritos con vos", "Formulario con aviso por mail y WhatsApp",
                    "Preparada para Google", "Panel para editar textos", "30 días de soporte"])
            + "\n"
            + plan("Sitio institucional", "El sitio completo de tu empresa, con servicios, casos y contacto.",
                   "A completar", "4 a 5 semanas",
                   ["Hasta 6 páginas", "Todo lo de Landing", "Sección de casos o portfolio",
                    "Preguntas frecuentes", "Blog opcional", "Capacitación al equipo"], destacado=True)
            + "\n"
            + plan("Tienda, chatbot o app", "Cuando hay operación atrás: stock, pagos, usuarios o automatización.",
                   "A completar", "8 a 12 semanas",
                   ["Alcance definido con vos", "Se puede hacer por etapas", "Integraciones con lo que ya usás",
                    "Pagos y facturación", "Panel de administración", "Código y datos a tu nombre"])
            + "\n      </div>"
            + """      <p class="planes__nota">Los rangos orientan. El número final sale de la primera reunión y queda cerrado por escrito.</p>""",
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Qué mueve el precio", "Para arriba y para abajo.")
            + """      <div class="split">
        <div class="split__col split__col--no">
          <h3 class="split__titulo">Lo sube</h3>
          <ul class="lista-marca lista-marca--sube">
            <li>Integraciones con sistemas de gestión propios o viejos.</li>
            <li>Muchos productos con variantes, stock por sucursal o precios por lista.</li>
            <li>Usuarios con permisos distintos y necesidad de auditoría.</li>
            <li>Contenido que tenemos que producir nosotros: textos, fotos, video.</li>
            <li>Plazos comprimidos que obligan a reordenar otros proyectos.</li>
          </ul>
        </div>
        <div class="split__col split__col--si">
          <h3 class="split__titulo">Lo baja</h3>
          <ul class="lista-marca lista-marca--baja">
            <li>Tener los textos y las fotos listos antes de arrancar.</li>
            <li>Una sola persona que decide y aprueba, en vez de un comité.</li>
            <li>Aceptar un alcance por etapas en lugar de todo junto.</li>
            <li>Reutilizar la identidad de marca que ya tenés.</li>
            <li>Flexibilidad en la fecha de entrega.</li>
          </ul>
        </div>
      </div>"""
        )
        + seccion(
            cabecera_seccion("Siempre incluido", "Sin costo extra, en cualquier proyecto.")
            + """      <div class="prose prose--ancho">
        <ul>
          <li>Diseño propio: nunca una plantilla comprada y rellenada.</li>
          <li>Optimización de velocidad y funcionamiento en celular.</li>
          <li>Preparación para buscadores: estructura, títulos, sitemap y datos estructurados.</li>
          <li>Capacitación grabada para que puedas editar contenidos.</li>
          <li>Treinta días de soporte después del lanzamiento.</li>
          <li>Dominio, hosting, código y accesos a tu nombre.</li>
        </ul>
        <h3>Lo que se cotiza aparte</h3>
        <ul>
          <li>Producción de fotos o video.</li>
          <li>Campañas de publicidad y su gestión.</li>
          <li>Trabajo sostenido de posicionamiento en buscadores.</li>
          <li>Mantenimiento mensual después de los primeros 30 días.</li>
          <li>Licencias de terceros: medios de pago, WhatsApp API, servicios de correo.</li>
        </ul>
      </div>""",
            clase="section section--band",
        )
        + seccion(
            cabecera_seccion("Preguntas frecuentes", "Sobre plata.")
            + faq(
                [
                    ("¿Cómo son los pagos?", [
                        "En general un anticipo para arrancar y el resto contra entregas parciales, atado a las etapas del proceso. En proyectos largos se divide en más pagos.",
                        "El esquema exacto va en la propuesta y se acuerda antes de firmar.",
                    ]),
                    ("¿Hay costos mensuales después?", [
                        "Hosting y dominio sí, y en proyectos con app o chatbot se suman los servicios de terceros. Son costos tuyos, contratados a tu nombre, no un recargo nuestro.",
                        "Te los detallamos en la propuesta con el número estimado, para que no aparezcan de sorpresa.",
                    ]),
                    ("¿Qué pasa si a mitad de camino quiero agregar algo?", [
                        "Lo cotizamos aparte y decidís vos si va ahora o en una segunda etapa. Nunca se agrega trabajo y se factura después sin avisar.",
                    ]),
                    ("¿Y si quiero frenar el proyecto?", [
                        "Pagás lo hecho hasta la etapa aprobada y te llevás todos los entregables: diseños, código y accesos.",
                        "No hay penalidad ni retención de material.",
                    ]),
                    ("¿Hacen descuentos?", [
                        "No hacemos descuentos por regatear, porque el precio ya sale calculado sin colchón. Lo que sí hacemos es ajustar el alcance: si el presupuesto no alcanza, buscamos juntos qué sacar o qué dejar para una segunda etapa.",
                    ]),
                ]
            )
        )
        + cta_final(
            "¿Entramos en tu presupuesto?",
            "Contanos qué necesitás y en 48 horas tenés un número cerrado. Si no llegamos, te lo decimos igual.",
        )
    ),
}


# ==========================================================================
# CONTACTO
# ==========================================================================
CONTACTO = {
    "archivo": "contacto.html",
    "titulo": "Contacto — KORA",
    "desc": "Escribinos y te respondemos en menos de 24 horas hábiles con una propuesta concreta. Por formulario, mail o WhatsApp.",
    "og_titulo": "Hablemos de tu proyecto — KORA",
    "cuerpo": (
        encabezado_pagina(
            "Contacto",
            "Contanos qué necesitás.",
            "Te respondemos en menos de 24 horas hábiles. No hay secretaria filtrando ni cadena de correos: te contesta la persona que va a estar en tu proyecto.",
            cta=False,
        )
        + f"""
    <section class="section" data-reveal>
      <div class="contacto-grid">
        <div class="contacto-info">
          <h2 class="contacto-info__titulo">Qué pasa después de que escribís</h2>
          <ol class="pasos-contacto">
            <li>
              <span class="pasos-contacto__n">1</span>
              <div>
                <h3>Te respondemos en 24 h hábiles</h3>
                <p>Con preguntas concretas si falta información, o directamente proponiendo una charla.</p>
              </div>
            </li>
            <li>
              <span class="pasos-contacto__n">2</span>
              <div>
                <h3>Charlamos 45 minutos</h3>
                <p>Por videollamada o presencial. Salís de ahí con el problema escrito, hagamos negocio o no.</p>
              </div>
            </li>
            <li>
              <span class="pasos-contacto__n">3</span>
              <div>
                <h3>Te pasamos la propuesta en 48 h</h3>
                <p>Alcance, fecha y precio cerrado. Vale 15 días y no tiene letra chica.</p>
              </div>
            </li>
          </ol>

          <h2 class="contacto-info__titulo">Si preferís, escribinos directo</h2>
          <ul class="channels channels--claro">
            <li>
              <a class="channel channel--wa" href="https://wa.me/{WHATSAPP}?text={WA_TEXTO}" target="_blank" rel="noopener">
                <span class="channel__icon" aria-hidden="true">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" focusable="false"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.82 9.82 0 0 1 6.988 2.896 9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.885-9.885 9.885M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.359.101 11.943c0 2.096.549 4.142 1.593 5.945L0 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.582 0 11.941-5.359 11.944-11.945a11.87 11.87 0 0 0-3.487-8.4"/></svg>
                </span>
                <span class="channel__body">
                  <span class="channel__label">WhatsApp</span>
                  <span class="channel__meta">Lun a vie de 9 a 18 h</span>
                </span>
              </a>
            </li>
            <li>
              <a class="channel" href="mailto:{EMAIL}?subject=Consulta%20desde%20la%20web">
                <span class="channel__icon" aria-hidden="true">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" focusable="false">
                    <rect x="2.5" y="5" width="19" height="14" rx="2.5"></rect>
                    <path d="m3 7 9 6 9-6" stroke-linecap="round" stroke-linejoin="round"></path>
                  </svg>
                </span>
                <span class="channel__body">
                  <span class="channel__label">{EMAIL}</span>
                  <span class="channel__meta">Respondemos en menos de 24 h</span>
                </span>
              </a>
            </li>
          </ul>

          <div class="ayuda-brief">
            <h3>Nos ayuda mucho si nos contás…</h3>
            <ul>
              <li>Qué hace tu negocio y a quién le vendés.</li>
              <li>Qué problema concreto querés resolver.</li>
              <li>Si tenés una fecha límite y por qué.</li>
              <li>Con qué presupuesto estás manejándote, aunque sea aproximado.</li>
            </ul>
            <p>Con eso la primera respuesta ya es útil en vez de ser otra pregunta.</p>
          </div>
        </div>

{formulario()}
      </div>
    </section>"""
    ),
}
