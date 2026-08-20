/* ==========================================================================
   KORA — Home
   Comportamiento de la página: constelaciones animadas, marquee, barra de
   progreso, apariciones al scroll, contadores, demo del chatbot,
   formulario, tooltips y transiciones de página.

   Todo es progresivo: sin JS la página se ve completa y estática.
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------------------
     CONFIGURACIÓN — lo único que hay que tocar para poner el sitio en producción
     ------------------------------------------------------------------------

     FORM_ENDPOINT
       URL del servicio que recibe el formulario (Formspree, Web3Forms,
       una función serverless propia, etc.). Si queda vacío, el formulario
       abre el cliente de mail del visitante con la consulta ya redactada,
       así funciona igual desde el día uno.

     CONTACT_EMAIL
       Casilla a la que llegan las consultas cuando se usa el modo mail.

     El número de WhatsApp NO está acá: vive en los href de index.html
     (botón flotante, tarjeta de contacto y footer). Buscá "5491100000000"
     y reemplazá los tres por el número real, en formato internacional
     sin +, sin espacios y sin guiones.
     ---------------------------------------------------------------------- */
  var FORM_ENDPOINT = '';
  var CONTACT_EMAIL = 'hola@kora.com.ar';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------------
     1. Transiciones de página
     Dos capas. Donde el navegador soporta View Transitions entre documentos
     (@view-transition en styles.css), lo maneja él. Donde no, usamos un
     velo del color del fondo: se funde al entrar y vuelve a aparecer antes
     de saltar a la página siguiente. En ningún caso se ve el flash blanco.
     ------------------------------------------------------------------------ */
  function initPageTransitions() {
    var veil = document.querySelector('[data-veil]');
    if (!veil || reduceMotion) return;

    // Entrada
    veil.classList.add('page-veil--enter');

    function clearEnter() { veil.classList.remove('page-veil--enter'); }
    veil.addEventListener('animationend', clearEnter, { once: true });
    // Red de seguridad: si la animación no llega a correr (pestaña en segundo
    // plano, motor con animaciones frenadas), igual sacamos el velo. Nunca
    // puede quedar una capa opaca tapando la página.
    setTimeout(clearEnter, 600);

    // Si el navegador ya hace la transición nativa, no duplicamos el efecto.
    var nativeCrossDoc = typeof window.CSSViewTransitionRule === 'function';

    document.addEventListener('click', function (e) {
      if (nativeCrossDoc) return;
      if (e.defaultPrevented || e.button !== 0) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var link = e.target.closest('a');
      if (!link || link.hasAttribute('download')) return;
      if (link.target && link.target !== '_self') return;

      var href = link.getAttribute('href');
      if (!href || href.charAt(0) === '#') return;

      var url;
      try { url = new URL(link.href, location.href); } catch (err) { return; }

      // mailto:, tel:, whatsapp y cualquier otro dominio salen sin velo
      if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
      if (url.origin !== location.origin) return;
      // Ancla dentro de la misma página
      if (url.pathname === location.pathname && url.search === location.search) return;

      e.preventDefault();
      veil.classList.remove('page-veil--enter');
      veil.classList.add('page-veil--leave');
      setTimeout(function () { location.href = url.href; }, 220);
    });

    // Al volver con el botón "atrás" la página sale de la caché con el velo
    // puesto; hay que sacárselo.
    window.addEventListener('pageshow', function (e) {
      if (e.persisted) veil.className = 'page-veil';
    });
  }

  /* ------------------------------------------------------------------------
     2. Botones: onda al hacer click
     El resto del feedback (levantarse al hover, hundirse al apretar) es CSS.
     ------------------------------------------------------------------------ */
  function initButtons() {
    if (reduceMotion) return;

    // Entrada del botón flotante de WhatsApp. Se apaga sola al terminar
    // (o por reloj) para que el estado en reposo sea siempre "visible".
    var fab = document.querySelector('[data-wa-fab]');
    if (fab) {
      fab.classList.add('is-entering');
      function settleFab() { fab.classList.remove('is-entering'); }
      fab.addEventListener('animationend', settleFab, { once: true });
      setTimeout(settleFab, 1400);
    }

    document.addEventListener('pointerdown', function (e) {
      var btn = e.target.closest('.btn');
      if (!btn) return;

      var rect = btn.getBoundingClientRect();
      // Radio suficiente para cubrir el botón desde donde se apretó
      var radius = Math.max(
        Math.hypot(e.clientX - rect.left, e.clientY - rect.top),
        Math.hypot(e.clientX - rect.right, e.clientY - rect.top),
        Math.hypot(e.clientX - rect.left, e.clientY - rect.bottom),
        Math.hypot(e.clientX - rect.right, e.clientY - rect.bottom)
      );

      var ripple = document.createElement('span');
      ripple.className = 'btn__ripple';
      ripple.style.width = ripple.style.height = radius * 2 + 'px';
      ripple.style.left = (e.clientX - rect.left - radius) + 'px';
      ripple.style.top = (e.clientY - rect.top - radius) + 'px';

      btn.appendChild(ripple);
      ripple.addEventListener('animationend', function () { ripple.remove(); }, { once: true });
    });
  }

  /* ------------------------------------------------------------------------
     3. Navegación mobile
     La animación de apertura es CSS; acá sólo manejamos el estado.
     ------------------------------------------------------------------------ */
  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var menu = document.getElementById('nav-menu');
    if (!toggle || !menu) return;

    function setOpen(open) {
      menu.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    }

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });

    // Click fuera del menú
    document.addEventListener('click', function (e) {
      if (!menu.classList.contains('is-open')) return;
      if (e.target.closest('.nav__inner')) return;
      setOpen(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    window.matchMedia('(min-width: 901px)').addEventListener('change', function (e) {
      if (e.matches) setOpen(false);
      cerrarSubmenus();
    });

    /* --- Submenú de Servicios ---------------------------------------------
       En escritorio se abre al pasar el mouse y también con teclado; en
       mobile se despliega dentro del menú. El estado lo lleva aria-expanded
       en todos los casos, así el lector de pantalla lo anuncia igual. */
    var escritorio = window.matchMedia('(min-width: 901px)');
    var disparadores = Array.prototype.slice.call(document.querySelectorAll('[data-submenu]'));

    function cerrarSubmenus(excepto) {
      disparadores.forEach(function (d) {
        if (d === excepto) return;
        d.setAttribute('aria-expanded', 'false');
        var sub = document.getElementById(d.getAttribute('aria-controls'));
        if (sub) sub.classList.remove('is-open');
      });
    }

    disparadores.forEach(function (disparador) {
      var sub = document.getElementById(disparador.getAttribute('aria-controls'));
      if (!sub) return;
      var contenedor = disparador.closest('.nav__item');
      var salida = null;

      function abrir(estado) {
        clearTimeout(salida);
        if (estado) cerrarSubmenus(disparador);
        disparador.setAttribute('aria-expanded', String(estado));
        sub.classList.toggle('is-open', estado);
      }

      disparador.addEventListener('click', function () {
        abrir(disparador.getAttribute('aria-expanded') !== 'true');
      });

      // Hover sólo en escritorio, con un respiro al salir para que no se
      // cierre mientras el mouse cruza el hueco hacia el panel.
      contenedor.addEventListener('mouseenter', function () {
        if (escritorio.matches) abrir(true);
      });
      contenedor.addEventListener('mouseleave', function () {
        if (!escritorio.matches) return;
        salida = setTimeout(function () { abrir(false); }, 160);
      });

      // Al salir del submenú con el tabulador, se cierra
      contenedor.addEventListener('focusout', function (e) {
        if (!escritorio.matches) return;
        if (contenedor.contains(e.relatedTarget)) return;
        abrir(false);
      });

      sub.addEventListener('click', function (e) {
        if (e.target.closest('a')) abrir(false);
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') cerrarSubmenus();
    });

    document.addEventListener('click', function (e) {
      if (!e.target.closest('.nav__item--tiene-submenu')) cerrarSubmenus();
    });
  }

  /* ------------------------------------------------------------------------
     4. Tooltips
     Cualquier elemento con [data-tooltip] recibe uno. Aparece al hover y
     también al llegar con el teclado, y se cierra con Escape.
     ------------------------------------------------------------------------ */
  var tooltipSeq = 0;

  function initTooltips() {
    var triggers = Array.prototype.slice.call(document.querySelectorAll('[data-tooltip]'));

    triggers.forEach(function (trigger) {
      var text = trigger.getAttribute('data-tooltip');
      if (!text) return;

      var tip = document.createElement('span');
      tip.className = 'tooltip';
      tip.setAttribute('role', 'tooltip');
      tip.id = 'tooltip-' + (++tooltipSeq);
      tip.textContent = text;
      document.body.appendChild(tip);

      trigger.classList.add('has-tooltip');
      trigger.setAttribute('aria-describedby', tip.id);
      if (!trigger.hasAttribute('tabindex')) trigger.setAttribute('tabindex', '0');

      var MARGIN = 10;   // separación respecto del elemento
      var EDGE = 12;     // aire mínimo contra el borde de la pantalla

      function place() {
        var anchor = trigger.getBoundingClientRect();
        // offsetWidth/Height y no getBoundingClientRect: el tooltip está
        // escalado a 0.97 mientras está oculto y mediría de menos.
        var w = tip.offsetWidth;
        var h = tip.offsetHeight;

        // Arriba si entra; si no, abajo.
        var below = anchor.top - h - MARGIN < EDGE;
        tip.classList.toggle('tooltip--below', below);
        tip.style.top = (below ? anchor.bottom + MARGIN : anchor.top - h - MARGIN) + 'px';

        // Centrado sobre el elemento, sin salirse de la pantalla
        var center = anchor.left + anchor.width / 2;
        var half = w / 2;
        var min = EDGE + half;
        var max = window.innerWidth - EDGE - half;
        var left = max < min ? window.innerWidth / 2 : Math.min(Math.max(center, min), max);
        tip.style.left = left + 'px';

        // El piquito sigue apuntando al elemento aunque el globo se haya
        // corrido, sin llegar a salirse de las esquinas redondeadas.
        var arrow = Math.min(Math.max(center - left + half, 14), w - 14);
        tip.style.setProperty('--tip-arrow', arrow + 'px');
      }

      function show() {
        place();
        tip.classList.add('is-visible');
      }
      function hide() {
        tip.classList.remove('is-visible');
      }

      trigger.addEventListener('mouseenter', show);
      trigger.addEventListener('mouseleave', hide);
      trigger.addEventListener('focus', show);
      trigger.addEventListener('blur', hide);
      trigger.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') hide();
      });

      // Al scrollear el globo quedaría flotando lejos del elemento
      window.addEventListener('scroll', hide, { passive: true });
      window.addEventListener('resize', hide, { passive: true });
    });
  }

  /* ------------------------------------------------------------------------
     4b. Hero: entrada escalonada y titular rotativo
     El titular alterna entre los tres servicios revelando línea por línea.
     Sin JS se ve el primero fijo, que ya es una frase completa y correcta.
     ------------------------------------------------------------------------ */
  var ROTACION_MS = 3600;
  var SALIDA_MS = 640;

  function initHero() {
    var hero = document.querySelector('[data-hero]');

    // --- Entrada escalonada ---
    // El estado oculto va como estilo en línea y lo saca este mismo código.
    // Así, si las transiciones no llegan a correr, al borrar el estilo el
    // elemento queda visible igual: el hero no puede quedar en blanco.
    if (hero && !reduceMotion) {
      var partes = Array.prototype.slice.call(hero.querySelectorAll('.hero__reveal'));

      partes.forEach(function (el, i) {
        var t = 'opacity 760ms var(--ease-out) ' + i * 90 + 'ms, ' +
                'transform 760ms var(--ease-out) ' + i * 90 + 'ms';
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = t;
      });

      var mostrar = function () {
        partes.forEach(function (el) {
          el.style.opacity = '';
          el.style.transform = '';
        });
      };

      requestAnimationFrame(function () { requestAnimationFrame(mostrar); });
      setTimeout(mostrar, 1200);                       // red de seguridad
      setTimeout(function () {                          // limpieza al terminar
        partes.forEach(function (el) { el.style.transition = ''; });
      }, 2600);
    }

    // --- Rotador ---
    var rot = document.querySelector('[data-rotador]');
    if (!rot || reduceMotion) return;

    var items = Array.prototype.slice.call(rot.querySelectorAll('.rotador__item'));
    if (items.length < 2) return;

    // La altura del bloque la resuelve el grid con el ítem más alto (ver
    // .js-rotador en styles.css). No se mide nada por JS a propósito: medir
    // antes de que carguen las tipografías dejaba el bloque con la altura
    // equivocada y un hueco enorme debajo del titular.
    rot.classList.add('js-rotador');

    // El bento del hero comparte reloj con el titular: la tarjeta que pasa
    // al lugar grande es la del servicio que el titular está nombrando.
    // Un solo intervalo para los dos, así no pueden desfasarse nunca.
    var LUGARES = ['is-grande', 'is-chica-1', 'is-chica-2'];
    var tarjetas = Array.prototype.slice.call(
      document.querySelectorAll('[data-bento] [data-bento-card]')
    );

    function acomodarBento(activa) {
      tarjetas.forEach(function (card, i) {
        // La activa va al grande; el resto ocupa los chicos en orden.
        var pos = (i - activa + tarjetas.length) % tarjetas.length;
        LUGARES.forEach(function (l) { card.classList.remove(l); });
        card.classList.add(LUGARES[pos] || LUGARES[LUGARES.length - 1]);
      });
    }

    var actual = 0;
    if (tarjetas.length) acomodarBento(actual);

    setInterval(function () {
      var saliendo = items[actual];
      actual = (actual + 1) % items.length;

      saliendo.classList.remove('is-activa');
      saliendo.classList.add('is-saliendo');
      items[actual].classList.add('is-activa');

      if (tarjetas.length) acomodarBento(actual % tarjetas.length);

      // Al desmontar la salida hay que apagar la transición, si no el ítem
      // que ya se fue vuelve deslizándose a su posición de espera y se ve.
      setTimeout(function () {
        saliendo.classList.add('sin-transicion');
        saliendo.classList.remove('is-saliendo');
        void saliendo.offsetHeight;
        saliendo.classList.remove('sin-transicion');
      }, SALIDA_MS);
    }, ROTACION_MS);
  }

  /* ------------------------------------------------------------------------
     5. Constelaciones
     El mismo motivo de puntos y líneas del hero, repetido en toda la
     landing. Las formas se declaran acá y se dibujan sobre cualquier
     elemento con [data-net-gen]; después el animador las mueve junto con
     las dos constelaciones que ya venían en el HTML.

     Cada forma: nodos [x, y, radio, esNodoPrincipal] sobre un lienzo
     de 400×400, y aristas [índiceA, índiceB].
     ------------------------------------------------------------------------ */
  var NET_SHAPES = {
    arc: {
      nodes: [[40, 60, 4, 0], [160, 120, 5, 1], [300, 50, 4, 0], [240, 220, 5, 1], [120, 300, 4, 0], [330, 320, 4, 0]],
      edges: [[0, 1], [1, 2], [1, 4], [2, 3], [3, 5], [3, 4]]
    },
    fan: {
      nodes: [[200, 40, 5, 1], [60, 160, 4, 0], [340, 150, 4, 0], [150, 320, 4, 0], [280, 300, 5, 1]],
      edges: [[0, 1], [0, 2], [1, 3], [2, 4], [3, 4]]
    },
    chain: {
      nodes: [[50, 320, 4, 0], [140, 220, 5, 1], [250, 260, 4, 0], [340, 150, 5, 1], [300, 40, 4, 0]],
      edges: [[0, 1], [1, 2], [2, 3], [3, 4], [1, 3]]
    },
    cluster: {
      nodes: [[200, 200, 6, 1], [90, 110, 4, 0], [310, 120, 4, 0], [120, 310, 4, 0], [300, 300, 4, 0]],
      edges: [[0, 1], [0, 2], [0, 3], [0, 4]]
    },
    zig: {
      nodes: [[40, 120, 4, 0], [150, 60, 5, 1], [250, 180, 5, 1], [360, 110, 4, 0], [200, 320, 4, 0]],
      edges: [[0, 1], [1, 2], [2, 3], [2, 4]]
    },
    wide: {
      nodes: [[60, 200, 4, 0], [180, 90, 5, 1], [300, 200, 4, 0], [180, 310, 5, 1], [380, 300, 4, 0]],
      edges: [[0, 1], [1, 2], [2, 3], [3, 0], [2, 4]]
    }
  };

  var NET_TONES = {
    light: { line: '#E5E7EB', hub: '#1E3A8A', dot: '#06B6D4' },
    dark:  { line: 'rgba(255,255,255,0.7)', hub: '#FFFFFF', dot: '#06B6D4' }
  };

  var SVG_NS = 'http://www.w3.org/2000/svg';

  function buildNets() {
    var hosts = Array.prototype.slice.call(document.querySelectorAll('[data-net-gen]'));

    hosts.forEach(function (host) {
      var shape = NET_SHAPES[host.dataset.netGen];
      if (!shape) return;

      var tone = NET_TONES[host.dataset.netTone] || NET_TONES.light;
      var size = parseInt(host.dataset.netSize, 10) || 360;

      if (host.dataset.netTone === 'dark') host.classList.add('net-deco--dark');

      var svg = document.createElementNS(SVG_NS, 'svg');
      svg.setAttribute('width', size);
      svg.setAttribute('height', size);
      svg.setAttribute('viewBox', '0 0 400 400');
      svg.setAttribute('data-net', '');
      svg.setAttribute('aria-hidden', 'true');
      svg.setAttribute('focusable', 'false');

      var group = document.createElementNS(SVG_NS, 'g');
      group.setAttribute('stroke', tone.line);
      group.setAttribute('stroke-width', '1');

      shape.edges.forEach(function (edge) {
        var a = shape.nodes[edge[0]];
        var b = shape.nodes[edge[1]];
        var line = document.createElementNS(SVG_NS, 'line');
        line.setAttribute('data-a', edge[0]);
        line.setAttribute('data-b', edge[1]);
        line.setAttribute('x1', a[0]);
        line.setAttribute('y1', a[1]);
        line.setAttribute('x2', b[0]);
        line.setAttribute('y2', b[1]);
        group.appendChild(line);
      });
      svg.appendChild(group);

      shape.nodes.forEach(function (node, i) {
        var dot = document.createElementNS(SVG_NS, 'circle');
        dot.setAttribute('data-i', i);
        dot.setAttribute('cx', node[0]);
        dot.setAttribute('cy', node[1]);
        dot.setAttribute('r', node[2]);
        dot.setAttribute('fill', node[3] ? tone.hub : tone.dot);
        svg.appendChild(dot);
      });

      host.appendChild(svg);
    });
  }

  /* Anima todas las constelaciones de la página, generadas o no.
     Cada nodo flota con su propio seno/coseno y cada línea sigue a los
     dos nodos que conecta. Las que están fuera de pantalla se saltean. */
  function initNets() {
    var svgs = Array.prototype.slice.call(document.querySelectorAll('[data-net]'));
    if (!svgs.length || reduceMotion) return;

    var nets = svgs.map(function (svg) {
      var dots = Array.prototype.slice.call(svg.querySelectorAll('circle[data-i]'));
      return {
        el: svg,
        visible: true,
        lines: Array.prototype.slice.call(svg.querySelectorAll('line[data-a]')),
        base: dots.map(function (d) {
          return {
            el: d,
            x: parseFloat(d.getAttribute('cx')),
            y: parseFloat(d.getAttribute('cy')),
            ax: 7 + Math.random() * 6,          // amplitud horizontal
            ay: 6 + Math.random() * 7,          // amplitud vertical
            px: Math.random() * Math.PI * 2,    // fase
            py: Math.random() * Math.PI * 2,
            sx: 0.22 + Math.random() * 0.18,    // velocidad
            sy: 0.20 + Math.random() * 0.18
          };
        })
      };
    });

    // No gastar frames en constelaciones que no se ven.
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          var net = nets.find(function (n) { return n.el === entry.target; });
          if (net) net.visible = entry.isIntersecting;
        });
      }, { rootMargin: '120px' });
      nets.forEach(function (net) {
        net.visible = false;
        io.observe(net.el);
      });
    }

    function tick(t) {
      var s = t / 1000;

      nets.forEach(function (net) {
        if (!net.visible) return;

        var pos = net.base.map(function (n) {
          return {
            x: n.x + Math.sin(s * n.sx + n.px) * n.ax,
            y: n.y + Math.cos(s * n.sy + n.py) * n.ay
          };
        });

        net.base.forEach(function (n, i) {
          n.el.setAttribute('cx', pos[i].x.toFixed(2));
          n.el.setAttribute('cy', pos[i].y.toFixed(2));
        });

        net.lines.forEach(function (l) {
          var a = pos[+l.dataset.a];
          var b = pos[+l.dataset.b];
          if (!a || !b) return;
          l.setAttribute('x1', a.x.toFixed(2));
          l.setAttribute('y1', a.y.toFixed(2));
          l.setAttribute('x2', b.x.toFixed(2));
          l.setAttribute('y2', b.y.toFixed(2));
        });
      });

      requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  /* ------------------------------------------------------------------------
     6. Marquee infinito
     Se frena al pasar el mouse por encima para poder leerlo.
     ------------------------------------------------------------------------ */
  function initMarquee() {
    var band = document.querySelector('.marquee');
    var track = document.querySelector('[data-marquee]');
    var group = document.querySelector('[data-marquee-group]');
    if (!band || !track || !group || reduceMotion) return;

    var clone = group.cloneNode(true);
    clone.removeAttribute('data-marquee-group');
    clone.setAttribute('aria-hidden', 'true');
    track.appendChild(clone);

    var SPEED = 21;           // px por segundo
    var x = 0;
    var last = null;
    var paused = false;

    band.addEventListener('mouseenter', function () { paused = true; });
    band.addEventListener('mouseleave', function () { paused = false; });

    function step(now) {
      if (last === null) last = now;
      var dt = Math.min((now - last) / 1000, 0.1);
      last = now;

      if (!paused) {
        x -= SPEED * dt;
        var half = track.scrollWidth / 2;
        if (half && -x >= half) x += half;
        track.style.transform = 'translateX(' + x.toFixed(2) + 'px)';
      }

      requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  /* ------------------------------------------------------------------------
     7. Barra de progreso de scroll + sombra de la barra de navegación
     ------------------------------------------------------------------------ */
  function initProgress() {
    var bar = document.querySelector('[data-progress]');
    var nav = document.querySelector('.nav');
    if (!bar && !nav) return;

    var ticking = false;

    function update() {
      if (bar) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
      }
      if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 12);
      ticking = false;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
  }

  /* ------------------------------------------------------------------------
     8. Apariciones al scroll
     Dentro de cada [data-reveal] buscamos los bloques de contenido y los
     hacemos entrar escalonados, no la sección entera de una. Si no hay
     bloques reconocibles, se anima el contenedor.

     Las clases las pone JS, así que sin JS no queda nada escondido.
     ------------------------------------------------------------------------ */
  var REVEAL_ITEMS = [
    '.section__head', '.value', '.card', '.stats__cell',
    '.steps__item', '.case', '.quote', '.cta__copy', '.form-card'
  ].join(', ');

  var STAGGER_MS = 70;
  var STAGGER_MAX = 5;   // a partir del sexto no sumamos más demora

  function initReveal() {
    var groups = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
    if (!groups.length || reduceMotion || !('IntersectionObserver' in window)) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px' });

    groups.forEach(function (group) {
      var items = Array.prototype.slice.call(group.querySelectorAll(REVEAL_ITEMS));
      if (!items.length) items = [group];

      items.forEach(function (item, i) {
        item.classList.add('reveal');
        item.style.setProperty('--reveal-delay', Math.min(i, STAGGER_MAX) * STAGGER_MS + 'ms');
        io.observe(item);
      });
    });
  }

  /* ------------------------------------------------------------------------
     9. Contadores animados
     ------------------------------------------------------------------------ */
  function initCounters() {
    var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
    if (!counters.length || reduceMotion || !('IntersectionObserver' in window)) return;

    function format(el, value) {
      var target = parseFloat(el.dataset.count) || 0;
      var decimals = target % 1 !== 0 ? 1 : 0;
      return (el.dataset.prefix || '') + value.toFixed(decimals) + (el.dataset.suffix || '');
    }

    function write(el, value) { el.textContent = format(el, value); }

    counters.forEach(function (el) { write(el, 0); });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        io.unobserve(el);

        var target = parseFloat(el.dataset.count) || 0;
        var t0 = performance.now();

        (function run(now) {
          var p = Math.min((now - t0) / 1400, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          write(el, target * eased);
          if (p < 1) requestAnimationFrame(run);
        })(t0);
      });
    }, { threshold: 0.4 });

    counters.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------------------------
     10. Demo del chatbot
     ------------------------------------------------------------------------ */
  var CHAT_SCRIPT = [
    { role: 'user', text: 'Hola, ¿hacen tiendas online?' },
    { role: 'bot',  text: 'Sí. ¿Cuántos productos manejás?' },
    { role: 'user', text: 'Unos 120, con stock por sucursal.' },
    { role: 'bot',  text: 'Perfecto. Te armo una propuesta con catálogo, stock y pagos. ¿Te la paso hoy?' }
  ];

  function initChat() {
    var log = document.querySelector('[data-chat-log]');
    if (!log) return;

    function append(i) {
      var msg = CHAT_SCRIPT[i];
      var row = document.createElement('li');
      row.className = 'chat__row chat__row--' + msg.role;

      var bubble = document.createElement('div');
      bubble.className = 'chat__bubble';
      bubble.textContent = msg.text;

      row.appendChild(bubble);
      log.appendChild(row);
    }

    var count = 1;
    append(0);

    if (reduceMotion) {
      // Sin animación: se muestra la conversación completa de una vez.
      for (var i = 1; i < CHAT_SCRIPT.length; i++) append(i);
      return;
    }

    setInterval(function () {
      if (count >= CHAT_SCRIPT.length) {
        log.textContent = '';
        count = 1;
        append(0);
      } else {
        append(count);
        count += 1;
      }
    }, 1900);
  }

  /* ------------------------------------------------------------------------
     11. Preguntas frecuentes (acordeón)
     Mejora progresiva: el HTML viene con todas las respuestas a la vista.
     Recién cuando este código corre se pliegan y el bloque pasa a ser un
     acordeón. Sin JS, la sección se lee entera igual.
     ------------------------------------------------------------------------ */
  function initFaq() {
    var faq = document.querySelector('.faq');
    if (!faq) return;

    var items = Array.prototype.slice.call(faq.querySelectorAll('.faq__item'));
    if (!items.length) return;

    // is-initing apaga la transición mientras se pliegan por primera vez,
    // así al cargar la página no se ve el acordeón cerrándose solo.
    faq.classList.add('js-accordion', 'is-initing');

    var abiertos = items.map(function (item) {
      var trigger = item.querySelector('.faq__trigger');
      var panel = item.querySelector('.faq__panel');
      if (!trigger || !panel) return null;

      var timerCierre = null;

      function abrir() {
        clearTimeout(timerCierre);
        panel.hidden = false;
        panel.style.height = '0px';
        void panel.offsetHeight;                 // reflow: da el punto de partida
        panel.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
        panel.style.height = panel.firstElementChild.offsetHeight + 'px';
      }

      // El alto siempre está en px explícitos (nunca en "auto"), así que se
      // puede animar a cero directo. El estado ARIA cambia acá y no dentro
      // de un requestAnimationFrame: es estado, no animación, y tiene que
      // quedar aplicado ya. El hidden llega al final del plegado, por reloj.
      function cerrar() {
        clearTimeout(timerCierre);
        panel.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
        panel.style.height = '0px';
        timerCierre = setTimeout(function () { panel.hidden = true; }, 340);
      }

      // Estado inicial: cerrado del todo, sin animación
      panel.style.height = '0px';
      panel.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');

      trigger.addEventListener('click', function () {
        var estaAbierto = trigger.getAttribute('aria-expanded') === 'true';
        if (estaAbierto) {
          cerrar();
          return;
        }
        // Acordeón: se cierra el que estuviera abierto
        abiertos.forEach(function (otro) {
          if (otro && otro.trigger !== trigger && otro.trigger.getAttribute('aria-expanded') === 'true') {
            otro.cerrar();
          }
        });
        abrir();
      });

      // Si el contenido cambia de alto (resize, fuentes que cargan tarde),
      // el panel abierto se reajusta solo.
      if ('ResizeObserver' in window) {
        new ResizeObserver(function () {
          if (trigger.getAttribute('aria-expanded') === 'true') {
            panel.style.height = panel.firstElementChild.offsetHeight + 'px';
          }
        }).observe(panel.firstElementChild);
      }

      return { trigger: trigger, cerrar: cerrar };
    });

    void faq.offsetHeight;              // forzar reflow antes de reactivar
    faq.classList.remove('is-initing');

    // Si se llega con un enlace directo a una pregunta, se abre sola
    if (location.hash) {
      var destino = faq.querySelector('.faq__trigger[aria-controls="' + location.hash.slice(1) + '"]');
      if (destino) destino.click();
    }
  }

  /* ------------------------------------------------------------------------
     12. Formulario de contacto
     Valida en el navegador y envía. Si hay FORM_ENDPOINT configurado se
     manda por fetch; si no, se arma un mail con los datos y se abre el
     cliente de correo del visitante.
     ------------------------------------------------------------------------ */
  var RULES = {
    nombre: function (v) {
      if (!v) return 'Contanos cómo te llamás.';
      if (v.length < 2) return 'El nombre parece muy corto.';
      return '';
    },
    email: function (v) {
      if (!v) return 'Necesitamos un email para poder responderte.';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Revisá el email, parece que falta algo.';
      return '';
    },
    mensaje: function (v) {
      if (!v) return 'Escribinos un par de líneas sobre el proyecto.';
      if (v.length < 10) return 'Contanos un poco más para poder ayudarte.';
      return '';
    }
  };

  function initContactForm() {
    var form = document.querySelector('[data-contact-form]');
    if (!form) return;

    var success = document.querySelector('[data-form-success]');
    var successText = document.querySelector('[data-success-text]');
    var submit = form.querySelector('[data-submit]');
    var resetBtn = document.querySelector('[data-form-reset]');

    function errorSlot(name) {
      return form.querySelector('[data-error-for="' + name + '"]');
    }

    function setError(name, message) {
      var input = form.elements[name];
      var slot = errorSlot(name);
      if (slot) slot.textContent = message;
      if (input) {
        if (message) input.setAttribute('aria-invalid', 'true');
        else input.removeAttribute('aria-invalid');
      }
    }

    function validate() {
      var firstBad = null;

      Object.keys(RULES).forEach(function (name) {
        var input = form.elements[name];
        if (!input) return;
        var message = RULES[name](input.value.trim());
        setError(name, message);
        if (message && !firstBad) firstBad = input;
      });

      return firstBad;
    }

    // Limpiar el error apenas la persona corrige el campo
    Object.keys(RULES).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      input.addEventListener('input', function () {
        if (input.getAttribute('aria-invalid') === 'true') setError(name, '');
      });
      input.addEventListener('blur', function () {
        if (input.value.trim()) setError(name, RULES[name](input.value.trim()));
      });
    });

    function collect() {
      return {
        nombre: form.elements.nombre.value.trim(),
        email: form.elements.email.value.trim(),
        telefono: form.elements.telefono.value.trim(),
        tipo: form.elements.tipo.value,
        mensaje: form.elements.mensaje.value.trim()
      };
    }

    function showSuccess(message) {
      if (successText && message) successText.textContent = message;
      form.hidden = true;
      if (success) {
        success.hidden = false;
        success.scrollIntoView({ block: 'nearest', behavior: reduceMotion ? 'auto' : 'smooth' });
      }
    }

    function sendByMail(data) {
      var body = [
        'Nombre: ' + data.nombre,
        'Email: ' + data.email,
        'Teléfono: ' + (data.telefono || '—'),
        'Necesita: ' + data.tipo,
        '',
        data.mensaje
      ].join('\n');

      window.location.href = 'mailto:' + CONTACT_EMAIL +
        '?subject=' + encodeURIComponent('Consulta web — ' + data.nombre) +
        '&body=' + encodeURIComponent(body);

      showSuccess('Te abrimos el mail con la consulta ya redactada. Dale a enviar y te respondemos dentro de las 24 horas hábiles.');
    }

    function sendByFetch(data) {
      submit.setAttribute('aria-busy', 'true');
      submit.textContent = 'Enviando…';

      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          showSuccess('Te escribimos a ' + data.email + ' dentro de las próximas 24 horas hábiles.');
        })
        .catch(function () {
          setError('mensaje', 'No pudimos enviar la consulta. Probá de nuevo o escribinos a ' + CONTACT_EMAIL + '.');
        })
        .finally(function () {
          submit.removeAttribute('aria-busy');
          submit.textContent = 'Enviar consulta';
        });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      // Si el honeypot vino completo es un bot: no enviamos nada.
      if (form.elements.web && form.elements.web.value) {
        showSuccess('Gracias por tu mensaje.');
        return;
      }

      var firstBad = validate();
      if (firstBad) {
        firstBad.focus();
        return;
      }

      var data = collect();
      if (FORM_ENDPOINT) sendByFetch(data);
      else sendByMail(data);
    });

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        form.reset();
        Object.keys(RULES).forEach(function (name) { setError(name, ''); });
        if (success) success.hidden = true;
        form.hidden = false;
        form.elements.nombre.focus();
      });
    }
  }

  /* ------------------------------------------------------------------------
     Arranque
     ------------------------------------------------------------------------ */
  /* ==========================================================================
     GSAP + ScrollTrigger — capa de animación adicional
     Los cuatro bloques de acá abajo son aparte del sistema de reveal de
     siempre (initReveal, más arriba), que sigue intacto y sigue siendo la
     garantía de fondo: TODO el contenido del sitio se ve completo aunque
     JS no corra. Estos cuatro son mejoras que se SUMAN encima cuando GSAP
     está disponible, nunca un reemplazo de esa garantía.

     Por eso el patrón se repite en los cuatro: el estado "oculto" antes de
     animar lo pone GSAP por JS (gsap.set(...)), nunca una clase o regla
     CSS. Si vendor/gsap/*.js no llega a cargar —bloqueado, caído, lo que
     sea— cada función corta en la primera línea y el contenido queda
     exactamente como está en el HTML: visible.
     ========================================================================== */
  var GSAP_OK = !!(window.gsap && window.ScrollTrigger) && !reduceMotion;
  if (GSAP_OK) gsap.registerPlugin(ScrollTrigger);

  /* --------------------------------------------------------------------------
     A. La marca se dibuja al cargar
     Los tres anillos del isotipo (arriba a la izquierda, en todas las
     páginas) se trazan con stroke-dashoffset y después aparecen el núcleo
     y los tres nodos, escalonados. Es la idea del brief ("el logo se
     construye") adaptada a la geometría real de la marca — que son tres
     circunferencias superpuestas, no líneas rectas a tres puntos.
     -------------------------------------------------------------------------- */
  function initMarcaAnimada() {
    if (!GSAP_OK) return;
    var marca = document.querySelector('svg.nav__mark');
    if (!marca) return;

    var anillos = marca.querySelectorAll('g g circle');
    var relleno = marca.querySelectorAll(':scope > g > circle');
    if (!anillos.length) return;

    var tl = gsap.timeline({ delay: 0.15 });

    anillos.forEach(function (c, i) {
      var largo = c.getTotalLength();
      gsap.set(c, { strokeDasharray: largo, strokeDashoffset: largo });
      tl.to(c, { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' },
        i * 0.12);
    });

    gsap.set(relleno, { opacity: 0, scale: 0.4, transformOrigin: 'center' });
    tl.to(relleno, {
      opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)', stagger: 0.08,
    }, 0.35);
  }

  /* --------------------------------------------------------------------------
     B. Títulos con máscara
     Los títulos principales (no el del hero del home, que ya tiene su
     propio rotador) entran con un barrido de abajo hacia arriba en vez de
     un simple fundido. clip-path: inset(100% 0 0 0) -> inset(0% 0 0 0).
     -------------------------------------------------------------------------- */
  function initTitulosGSAP() {
    if (!GSAP_OK) return;
    var titulos = document.querySelectorAll(
      '.section__title, .cta__title, .page-hero__title, .caso-hero__titulo'
    );
    titulos.forEach(function (el) {
      gsap.set(el, { clipPath: 'inset(100% 0 0 0)' });
      gsap.to(el, {
        clipPath: 'inset(0% 0 0 0)',
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 85%', once: true },
      });
    });
  }

  /* --------------------------------------------------------------------------
     C. Proceso: se arma en secuencia
     Es la sección que el brief marca como la más importante. La línea que
     conecta los cinco pasos se dibuja de izquierda a derecha con scaleX,
     y cada paso aparece justo cuando la línea llega a su altura — da la
     sensación de que se va construyendo, no de que aparece todo junto.
     -------------------------------------------------------------------------- */
  function initProcesoGSAP() {
    if (!GSAP_OK) return;
    var linea = document.querySelector('.steps');
    var pasos = document.querySelectorAll('.steps__item');
    if (!linea || !pasos.length) return;

    gsap.set(linea, { '--linea-avance': 0 });
    gsap.set(pasos, { opacity: 0, y: 16 });

    var tl = gsap.timeline({
      scrollTrigger: { trigger: linea, start: 'top 75%', once: true },
    });
    tl.to(linea, { '--linea-avance': 1, duration: 1.1, ease: 'power1.inOut' }, 0);
    pasos.forEach(function (paso, i) {
      tl.to(paso, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' },
        (i / Math.max(pasos.length - 1, 1)) * 1.1 * 0.82);
    });
  }

  /* --------------------------------------------------------------------------
     D. Tarjetas con inclinación 3D
     Las tarjetas de servicio siguen apenas el mouse en perspectiva. Nada
     de esto reemplaza el hover ya existente (borde celeste, ícono que
     gira) — se suma. quickTo interpola con inercia en vez de saltar al
     valor nuevo en cada evento, que es lo que da la sensación de resorte.
     -------------------------------------------------------------------------- */
  function initTiltCards() {
    if (!GSAP_OK) return;
    var tarjetas = document.querySelectorAll('.card');
    var TOPE = 6; // grados máximos — sutil, no un efecto de feria

    tarjetas.forEach(function (card) {
      var qx = gsap.quickTo(card, 'rotateX', { duration: 0.4, ease: 'power3' });
      var qy = gsap.quickTo(card, 'rotateY', { duration: 0.4, ease: 'power3' });
      gsap.set(card, { transformPerspective: 900, transformStyle: 'preserve-3d' });

      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width;   // 0..1
        var py = (e.clientY - r.top) / r.height;
        qy(((px - 0.5) * 2) * TOPE);
        qx(-((py - 0.5) * 2) * TOPE);
      });
      card.addEventListener('mouseleave', function () {
        qx(0);
        qy(0);
      });
    });
  }

  function init() {
    initPageTransitions();
    initButtons();
    initNav();
    initTooltips();
    initHero();
    buildNets();
    initNets();
    initMarquee();
    initProgress();
    initReveal();
    initCounters();
    initChat();
    initFaq();
    initContactForm();
    initMarcaAnimada();
    initTitulosGSAP();
    initProcesoGSAP();
    initTiltCards();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
