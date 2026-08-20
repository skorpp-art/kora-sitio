/* ==========================================================================
   KORA — Sistema "Pizarra GSAP"
   Comportamiento de todo el sitio: rotador del titular, reveals y línea de
   proceso con GSAP, contadores, acordeón FAQ, formulario, tooltips, nav y
   transiciones de página.

   Cada función arranca comprobando que su elemento exista, así el mismo
   archivo sirve al home y a las páginas interiores sin errores: lo que no
   está en la página, simplemente no se inicializa.

   Todo es progresivo: sin JS la página se ve completa y estática.
   Ningún estado oculto vive en CSS para contenido — los pone este archivo
   (o GSAP) sólo cuando existe capacidad de mostrarlos de nuevo.
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------------------
     CONFIGURACIÓN — ver la nota equivalente en script.js
     FORM_ENDPOINT vacío = el formulario abre el cliente de mail con la
     consulta redactada. El número de WhatsApp vive en los href de index.html.
     ---------------------------------------------------------------------- */
  var FORM_ENDPOINT = '';
  var CONTACT_EMAIL = 'hola@kora.com.ar';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------------------------------------------------
     1. Transiciones de página (velo del color del lienzo)
     ------------------------------------------------------------------------ */
  function initPageTransitions() {
    var veil = document.querySelector('[data-veil]');
    if (!veil || reduceMotion) return;

    veil.classList.add('page-veil--enter');

    function clearEnter() { veil.classList.remove('page-veil--enter'); }
    veil.addEventListener('animationend', clearEnter, { once: true });
    setTimeout(clearEnter, 700);

    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

      var link = e.target.closest('a');
      if (!link || link.hasAttribute('download')) return;
      if (link.target && link.target !== '_self') return;

      var href = link.getAttribute('href');
      if (!href || href.charAt(0) === '#') return;

      var url;
      try { url = new URL(link.href, location.href); } catch (err) { return; }

      if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname && url.search === location.search) return;

      e.preventDefault();
      veil.classList.remove('page-veil--enter');
      veil.classList.add('page-veil--leave');
      setTimeout(function () { location.href = url.href; }, 220);
    });

    window.addEventListener('pageshow', function (e) {
      if (e.persisted) veil.className = 'page-veil';
    });
  }

  /* ------------------------------------------------------------------------
     2. Navegación mobile + submenú de Servicios
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

    var escritorio = window.matchMedia('(min-width: 901px)');
    escritorio.addEventListener('change', function (e) {
      if (e.matches) { setOpen(false); cerrarSubmenus(); }
    });

    /* --- Submenú: hover en escritorio, click en mobile --- */
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

      contenedor.addEventListener('mouseenter', function () {
        if (escritorio.matches) abrir(true);
      });
      contenedor.addEventListener('mouseleave', function () {
        if (!escritorio.matches) return;
        salida = setTimeout(function () { abrir(false); }, 160);
      });
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
     3. Tooltips ([data-tooltip])
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

      var MARGIN = 10;
      var EDGE = 12;

      function place() {
        var anchor = trigger.getBoundingClientRect();
        var w = tip.offsetWidth;
        var h = tip.offsetHeight;

        var below = anchor.top - h - MARGIN < EDGE;
        tip.classList.toggle('tooltip--below', below);
        tip.style.top = (below ? anchor.bottom + MARGIN : anchor.top - h - MARGIN) + 'px';

        var center = anchor.left + anchor.width / 2;
        var half = w / 2;
        var min = EDGE + half;
        var max = window.innerWidth - EDGE - half;
        var left = max < min ? window.innerWidth / 2 : Math.min(Math.max(center, min), max);
        tip.style.left = left + 'px';

        var arrow = Math.min(Math.max(center - left + half, 14), w - 14);
        tip.style.setProperty('--tip-arrow', arrow + 'px');
      }

      function show() { place(); tip.classList.add('is-visible'); }
      function hide() { tip.classList.remove('is-visible'); }

      trigger.addEventListener('mouseenter', show);
      trigger.addEventListener('mouseleave', hide);
      trigger.addEventListener('focus', show);
      trigger.addEventListener('blur', hide);
      trigger.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') hide();
      });

      window.addEventListener('scroll', hide, { passive: true });
      window.addEventListener('resize', hide, { passive: true });
    });
  }

  /* ------------------------------------------------------------------------
     4. Rotador del titular
     Las dos líneas de cada variante (palabra + resto de la frase) entran
     desde abajo con máscara; la palabra toma el color de su categoría por
     CSS (data-service). Sin JS se ve la primera variante.
     ------------------------------------------------------------------------ */
  var ROTACION_MS = 3600;
  var SALIDA_MS = 700;

  function initRotador() {
    var rot = document.querySelector('[data-rotador]');
    if (!rot || reduceMotion) return;

    var items = Array.prototype.slice.call(rot.querySelectorAll('.rotador__item'));
    if (items.length < 2) return;

    rot.classList.add('js-rotador');

    var actual = 0;

    setInterval(function () {
      var saliendo = items[actual];
      actual = (actual + 1) % items.length;

      saliendo.classList.remove('is-activa');
      saliendo.classList.add('is-saliendo');
      items[actual].classList.add('is-activa');

      setTimeout(function () {
        saliendo.classList.add('sin-transicion');
        saliendo.classList.remove('is-saliendo');
        void saliendo.offsetHeight;
        saliendo.classList.remove('sin-transicion');
      }, SALIDA_MS);
    }, ROTACION_MS);
  }

  /* ------------------------------------------------------------------------
     5. Barra de progreso + borde del nav al scrollear
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
     6. Contadores animados
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
     7. Preguntas frecuentes (acordeón, mejora progresiva)
     ------------------------------------------------------------------------ */
  function initFaq() {
    var faq = document.querySelector('.faq');
    if (!faq) return;

    var items = Array.prototype.slice.call(faq.querySelectorAll('.faq__item'));
    if (!items.length) return;

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
        void panel.offsetHeight;
        panel.classList.add('is-open');
        trigger.setAttribute('aria-expanded', 'true');
        panel.style.height = panel.firstElementChild.offsetHeight + 'px';
      }

      function cerrar() {
        clearTimeout(timerCierre);
        panel.classList.remove('is-open');
        trigger.setAttribute('aria-expanded', 'false');
        panel.style.height = '0px';
        timerCierre = setTimeout(function () { panel.hidden = true; }, 340);
      }

      panel.style.height = '0px';
      panel.hidden = true;
      trigger.setAttribute('aria-expanded', 'false');

      trigger.addEventListener('click', function () {
        var estaAbierto = trigger.getAttribute('aria-expanded') === 'true';
        if (estaAbierto) {
          cerrar();
          return;
        }
        abiertos.forEach(function (otro) {
          if (otro && otro.trigger !== trigger && otro.trigger.getAttribute('aria-expanded') === 'true') {
            otro.cerrar();
          }
        });
        abrir();
      });

      if ('ResizeObserver' in window) {
        new ResizeObserver(function () {
          if (trigger.getAttribute('aria-expanded') === 'true') {
            panel.style.height = panel.firstElementChild.offsetHeight + 'px';
          }
        }).observe(panel.firstElementChild);
      }

      return { trigger: trigger, cerrar: cerrar };
    });

    void faq.offsetHeight;
    faq.classList.remove('is-initing');

    if (location.hash) {
      var destino = faq.querySelector('.faq__trigger[aria-controls="' + location.hash.slice(1) + '"]');
      if (destino) destino.click();
    }
  }

  /* ------------------------------------------------------------------------
     8. Formulario de contacto
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
     9. Campo de puntos — el halo verde sigue al cursor
     No depende de GSAP: es sólo una custom property (--mx/--my) que la
     máscara radial de .dotfield::after ya sabe leer. Sin este script el
     fondo queda con la grilla tenue fija, nunca rota.
     ------------------------------------------------------------------------ */
  function initCampoPuntos() {
    var campo = document.querySelector('[data-dotfield]');
    if (!campo || reduceMotion) return;
    if (window.matchMedia('(hover: none)').matches) return;

    var activo = false;
    var mx = 0;
    var my = 0;
    var pintarProgramado = false;

    function pintar() {
      campo.style.setProperty('--mx', mx + 'px');
      campo.style.setProperty('--my', my + 'px');
      pintarProgramado = false;
    }

    window.addEventListener('mousemove', function (e) {
      mx = e.clientX;
      my = e.clientY;
      if (!activo) {
        activo = true;
        campo.classList.add('is-active');
      }
      if (!pintarProgramado) {
        pintarProgramado = true;
        requestAnimationFrame(pintar);
      }
    }, { passive: true });

    document.addEventListener('mouseleave', function () {
      activo = false;
      campo.classList.remove('is-active');
    });
  }

  /* ------------------------------------------------------------------------
     10. Entrada del botón flotante de WhatsApp
     ------------------------------------------------------------------------ */
  function initFab() {
    if (reduceMotion) return;
    var fab = document.querySelector('[data-wa-fab]');
    if (!fab) return;
    fab.classList.add('is-entering');
    function settle() { fab.classList.remove('is-entering'); }
    fab.addEventListener('animationend', settle, { once: true });
    setTimeout(settle, 1600);
  }

  /* ==========================================================================
     Capa GSAP — mejoras que se SUMAN cuando vendor/gsap cargó.
     El estado inicial oculto lo pone GSAP por JS, nunca CSS: sin GSAP el
     contenido queda exactamente como está en el HTML: visible.
     NUNCA se anima con GSAP una propiedad que también tenga transición CSS
     en el mismo elemento.
     ========================================================================== */
  var GSAP_OK = !!(window.gsap && window.ScrollTrigger) && !reduceMotion;
  if (GSAP_OK) gsap.registerPlugin(ScrollTrigger);

  /* A. La marca se dibuja al cargar (tres anillos trazados + núcleo) */
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
      tl.to(c, { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' }, i * 0.12);
    });

    gsap.set(relleno, { opacity: 0, scale: 0.4, transformOrigin: 'center' });
    tl.to(relleno, {
      opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)', stagger: 0.08
    }, 0.35);
  }

  /* B. Entrada del hero: línea fija con máscara + bloques escalonados.
     El rotador NO se anima acá: sus líneas ya tienen transición CSS. */
  function initHeroIntro() {
    if (!GSAP_OK) return;
    var hero = document.querySelector('[data-hero]');
    if (!hero) return;

    var tl = gsap.timeline({ delay: 0.1, defaults: { ease: 'power4.out' } });

    var estatica = hero.querySelector('.hero__line--static');
    if (estatica) tl.from(estatica, { yPercent: 115, duration: 0.9 });

    tl.from(hero.querySelectorAll('.hero__fade'), {
      autoAlpha: 0, y: 26, duration: 0.7, ease: 'power3.out', stagger: 0.09
    }, estatica ? '-=0.45' : 0);
  }

  /* C. Formas flotando.
     Antes era un vaivén de un solo eje: los dos ejes compartían duración,
     así que todas las formas iban y volvían por la misma diagonal y al
     mismo tiempo, y el bucle se notaba. Ahora x e y tienen períodos
     distintos y primos entre sí, con lo cual el recorrido es una figura
     que tarda muchísimo en repetirse — se lee como deriva, no como loop.

     Ojo con el selector: antes decía '.hero__shape, [data-float]', que
     agarraba al contenedor Y a su hijo, y el movimiento se sumaba dos
     veces. Ahora el contenedor queda libre para el parallax de abajo y
     acá sólo se mueve el hijo. */
  function initFloaters() {
    if (!GSAP_OK) return;
    var formas = gsap.utils.toArray('[data-float]');
    if (!formas.length) return;

    formas.forEach(function (forma, i) {
      var signo = i % 2 ? -1 : 1;

      gsap.to(forma, {
        y: signo * 24,
        duration: 3.1 + i * 0.43,
        ease: 'sine.inOut', yoyo: true, repeat: -1
      });
      gsap.to(forma, {
        x: signo * -15,
        duration: 4.7 + i * 0.61,
        ease: 'sine.inOut', yoyo: true, repeat: -1
      });
    });

    /* El molinete y el anillo giran despacio y sin parar: son las dos
       formas con estructura interna, las únicas donde el giro se ve. */
    gsap.utils.toArray('.hero__shape--pin [data-float], .hero__shape--ring [data-float]')
      .forEach(function (forma, i) {
        gsap.to(forma, {
          rotation: i ? -360 : 360,
          duration: 44 + i * 15,
          ease: 'none',
          repeat: -1
        });
      });
  }

  /* C2. Las formas del hero siguen al mouse en profundidad
     Cada una se corre distinto (las de más adelante, más), así el bloque
     de formas se abre en capas cuando movés el cursor. Se le pone al
     CONTENEDOR, no al hijo: el hijo ya está ocupado con la deriva de
     arriba y pisarle el transform sería pelearse por la misma matriz. */
  function initParallaxHero() {
    if (!GSAP_OK) return;
    if (window.matchMedia('(hover: none)').matches) return;

    var capas = gsap.utils.toArray('.hero__shape');
    if (!capas.length) return;

    var motores = capas.map(function (capa, i) {
      return {
        x: gsap.quickTo(capa, 'x', { duration: 0.9, ease: 'power3' }),
        y: gsap.quickTo(capa, 'y', { duration: 0.9, ease: 'power3' }),
        profundidad: (i + 1) * 10
      };
    });

    window.addEventListener('mousemove', function (e) {
      var cx = (e.clientX / window.innerWidth - 0.5) * 2;   // -1..1
      var cy = (e.clientY / window.innerHeight - 0.5) * 2;
      motores.forEach(function (m) {
        m.x(-cx * m.profundidad);
        m.y(-cy * m.profundidad);
      });
    }, { passive: true });
  }

  /* C3. Las formas de servicio se transforman al scrollear
     Cada una deja de ser una esfera y toma la silueta de lo que vende:
     la web se aplasta en una pantalla, el chatbot pierde una esquina y
     queda como globo de diálogo, y el cuadrado de apps se estira a
     telefono con su icono al lado.

     Va con scrub: el avance está atado a la posición del scroll, no a un
     reloj. Es la diferencia entre una animación que le pasa al visitante
     y una que el visitante siente que maneja él.

     Los border-radius van en fromTo y con los cuatro valores escritos a
     mano en los dos extremos. Si el inicio fuera '50%' (un solo valor) y
     el final cuatro, GSAP no tendría cómo emparejarlos y saltaría en vez
     de interpolar. */
  function initMorphServicios() {
    if (!GSAP_OK) return;

    function alScroll(el) {
      /* El recorrido es corto a propósito: la forma entra por abajo (92%)
         y termina de transformarse cuando llegó al 62% de la pantalla, o
         sea en unos 220px de scroll en vez de los ~490px que daba usar
         bottom como final. Repartida en medio viewport la transformación
         avanza tan de a poco que no se percibe; concentrada acá se ve.
         Después la forma sigue subiendo ya transformada, que es cuando
         se la puede mirar.

         scrub bajo (0.25) para que siga al scroll casi sin inercia: con
         0.6 el dibujo llegaba tarde y tapaba lo poco que se notaba. */
      return { trigger: el, start: 'top 92%', end: 'top 62%', scrub: 0.25 };
    }

    var web = document.querySelector('.shape-orb--web');
    if (web) {
      gsap.fromTo(web,
        { borderRadius: '50% 50% 50% 50%' },
        {
          borderRadius: '14% 14% 14% 14%',
          scaleX: 1.32, scaleY: 0.66,
          ease: 'none', scrollTrigger: alScroll(web)
        });
    }

    var chat = document.querySelector('.shape-orb--chat');
    if (chat) {
      gsap.fromTo(chat,
        { borderRadius: '50% 50% 50% 50%' },
        {
          borderRadius: '50% 50% 6% 50%',
          rotation: -12,
          ease: 'none', scrollTrigger: alScroll(chat)
        });
    }

    var duo = document.querySelector('.shape-duo');
    if (duo) {
      var cuadrado = duo.querySelector('.shape-duo__sq');
      var punto = duo.querySelector('.shape-duo__dot');
      if (cuadrado) {
        gsap.fromTo(cuadrado,
          { borderRadius: '22%' },
          {
            borderRadius: '26%',
            scaleX: 0.6, scaleY: 1.36,
            ease: 'none', scrollTrigger: alScroll(duo)
          });
      }
      if (punto) {
        gsap.to(punto, {
          x: 10, y: -4, scale: 0.62,
          ease: 'none', scrollTrigger: alScroll(duo)
        });
      }
    }
  }

  /* D. Reveals al scroll.
     En el home [data-reveal] va sobre bloques chicos; en las páginas
     interiores lo genera _build/ sobre la <section> entera. Si adentro hay
     bloques reconocibles entran escalonados —que se vea que la sección se
     arma— y si no, entra el elemento solo.

     .steps__item queda deliberadamente afuera de la lista: de esos se
     ocupa initProceso(), y animar el mismo elemento desde dos lugares
     distintos es la forma más rápida de que uno pise al otro. */
  var REVEAL_ITEMS = [
    '.section__head', '.split__col', '.entregable', '.mini-caso',
    '.faq__item', '.case', '.plan', '.persona', '.tesis__item',
    '.decision', '.resultado', '.cita-caso', '.prose',
    '.contacto-info', '.form-card'
  ].join(', ');

  function initReveals() {
    if (!GSAP_OK) return;

    gsap.utils.toArray('[data-reveal]').forEach(function (el) {
      var hijos = el.querySelectorAll(REVEAL_ITEMS);
      var objetivo = hijos.length ? hijos : el;

      gsap.from(objetivo, {
        autoAlpha: 0,
        y: 30,
        duration: 0.75,
        ease: 'power3.out',
        stagger: hijos.length ? 0.08 : 0,
        scrollTrigger: { trigger: el, start: 'top 84%', once: true }
      });
    });
  }

  /* E. Proceso: la línea verde se dibuja y los pasos aparecen a su ritmo */
  function initProceso() {
    if (!GSAP_OK) return;
    var linea = document.querySelector('.steps');
    var pasos = document.querySelectorAll('.steps__item');
    if (!linea || !pasos.length) return;

    gsap.set(linea, { '--avance': 0 });
    gsap.set(pasos, { autoAlpha: 0, y: 18 });

    var tl = gsap.timeline({
      scrollTrigger: { trigger: linea, start: 'top 76%', once: true }
    });
    tl.to(linea, { '--avance': 1, duration: 1.15, ease: 'power1.inOut' }, 0);
    pasos.forEach(function (paso, i) {
      tl.to(paso, { autoAlpha: 1, y: 0, duration: 0.45, ease: 'power2.out' },
        (i / Math.max(pasos.length - 1, 1)) * 1.15 * 0.82);
    });
  }

  /* F. Manifiesto: palabras clave se encienden al entrar */
  function initManifesto() {
    if (!GSAP_OK) return;
    var manifiesto = document.querySelector('.manifesto');
    if (!manifiesto) return;

    gsap.from(manifiesto, {
      autoAlpha: 0,
      y: 36,
      duration: 0.85,
      ease: 'power3.out',
      scrollTrigger: { trigger: manifiesto, start: 'top 82%', once: true }
    });
  }

  function init() {
    initPageTransitions();
    initNav();
    initTooltips();
    initRotador();
    initProgress();
    initCounters();
    initFaq();
    initContactForm();
    initCampoPuntos();
    initFab();
    initMarcaAnimada();
    initHeroIntro();
    initFloaters();
    initParallaxHero();
    initMorphServicios();

    /* ScrollTrigger toma las medidas cuando se crea cada disparador. Si
       después entra una imagen sin alto declarado, el layout se corre y
       todos los disparadores de más abajo quedan apuntando al lugar
       equivocado — el efecto arranca antes de tiempo o directamente sale
       ya terminado. Un refresh cuando la página terminó de cargar los
       vuelve a medir con todo ya asentado. */
    if (GSAP_OK) {
      window.addEventListener('load', function () { ScrollTrigger.refresh(); });
    }
    initReveals();
    initProceso();
    initManifesto();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
