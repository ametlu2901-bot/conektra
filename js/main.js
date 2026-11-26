/* Enlaza Studio — interacciones */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Título de la portada: separa las palabras para que aparezcan una por una
  $$('.titulo-animado').forEach(h => {
    let n = 0;
    const partir = nodo => {
      [...nodo.childNodes].forEach(hijo => {
        if (hijo.nodeType === 3) {
          const frag = document.createDocumentFragment();
          hijo.textContent.split(/(\s+)/).forEach(trozo => {
            if (!trozo) return;
            if (/^\s+$/.test(trozo)) { frag.append(trozo); return; }
            const s = document.createElement('span');
            s.className = 'palabra'; s.style.setProperty('--n', n++); s.textContent = trozo;
            frag.append(s);
          });
          hijo.replaceWith(frag);
        } else if (hijo.nodeType === 1) partir(hijo);
      });
    };
    h.setAttribute('aria-label', h.textContent);
    partir(h);
  });

  // Menú del celular
  const boton = $('#hamburguesa');
  const cerrar = () => { document.body.classList.remove('menu-abierto'); boton.setAttribute('aria-expanded', 'false'); };
  boton.addEventListener('click', () => {
    const abierto = document.body.classList.toggle('menu-abierto');
    boton.setAttribute('aria-expanded', String(abierto));
  });
  $$('#menu a').forEach(a => a.addEventListener('click', cerrar));

  // Aparición al hacer scroll
  const obs = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('[data-revelar]').forEach(el => obs.observe(el));

  // Avisos que cambian en la ilustración
  const avisos = window.CONEKTRA_AVISOS || [];
  const aviso = $('#aviso');
  if (aviso && avisos.length > 1 && !quieto) {
    let n = 0;
    setInterval(() => {
      aviso.classList.add('cambiando');
      setTimeout(() => {
        n = (n + 1) % avisos.length;
        $('#aviso-titulo').textContent = avisos[n][0];
        $('#aviso-texto').textContent = avisos[n][1];
        aviso.classList.remove('cambiando');
      }, 400);
    }, 3200);
  }

  // Franja: la palabra rota, el recuadro se ajusta a su ancho y se enciende su ícono
  const pista = $('#palabras');
  if (pista) {
    const rotador = pista.parentElement;
    const palabras = $$('.rotador__palabra', pista);
    const iconos = $$('#franja-iconos .franja__ico');
    let i = 0;
    const mostrar = () => {
      const p = palabras[i];
      rotador.style.width = p.scrollWidth + 'px';
      pista.style.transform = `translateY(${-p.offsetTop}px)`;
      iconos.forEach((ic, j) => ic.classList.toggle('activo', j === i));
    };
    document.fonts && document.fonts.ready.then(mostrar);
    mostrar();
    if (!quieto) setInterval(() => { i = (i + 1) % palabras.length; mostrar(); }, 2200);
    addEventListener('resize', mostrar);
  }

  // Pasos del flujo: avanzan solos con barra de progreso; al tocar uno, se quedan quietos
  const listaPasos = $('.pasos');
  const pasos = $$('.paso');
  const cuadros = $$('.cuadro');
  if (pasos.length) {
    const DUR = 4500;
    let actual = 0, reloj, visible = false;
    listaPasos.style.setProperty('--duracion-paso', DUR / 1000 + 's');
    const contador = $('#escena-n');
    const ir = n => {
      actual = n;
      pasos.forEach((p, j) => {
        p.classList.toggle('activo', j === n); p.setAttribute('aria-pressed', String(j === n));
        const barra = $('.paso__progreso i', p);
        if (barra) { barra.style.animation = 'none'; void barra.offsetWidth; barra.style.animation = ''; }
      });
      cuadros.forEach((c, j) => c.classList.toggle('activo', j === n));
      if (contador) contador.textContent = n + 1;
    };
    const arrancar = () => {
      clearTimeout(reloj);
      if (quieto || !visible || listaPasos.classList.contains('pausado')) return;
      reloj = setTimeout(() => { ir((actual + 1) % pasos.length); arrancar(); }, DUR);
    };
    if (quieto) listaPasos.classList.add('pausado');
    pasos.forEach((p, j) => p.addEventListener('click', () => { listaPasos.classList.add('pausado'); clearTimeout(reloj); ir(j); }));
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { ir(actual); arrancar(); } else clearTimeout(reloj); }, { threshold: .3 }).observe(listaPasos);
  }

  // Celular: barra de WhatsApp que aparece al bajar y se esconde al llegar al cierre
  const barraWa = $('#barra-wa');
  if (barraWa) {
    const cierre = $('.cierre');
    let cierreVisible = false;
    if (cierre) new IntersectionObserver(([e]) => { cierreVisible = e.isIntersecting; revisarBarra(); }, { threshold: .05 }).observe(cierre);
    function revisarBarra() {
      const mostrar = scrollY > innerHeight * .5 && !cierreVisible;
      barraWa.classList.toggle('visible', mostrar);
      barraWa.setAttribute('aria-hidden', String(!mostrar));
      $('a', barraWa).tabIndex = mostrar ? 0 : -1;
    }
    addEventListener('scroll', revisarBarra, { passive: true });
    revisarBarra();
  }

  // Barra de lectura arriba y cabecera más compacta al bajar
  const lectura = $('#lectura');
  const cabecera = $('#cabecera');
  let pendienteLectura = false;
  const alBajar = () => {
    pendienteLectura = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    if (lectura) lectura.style.transform = `scaleX(${max > 0 ? Math.min(1, scrollY / max) : 0})`;
    if (cabecera) cabecera.classList.toggle('compacta', scrollY > 40);
  };
  addEventListener('scroll', () => { if (!pendienteLectura) { pendienteLectura = true; requestAnimationFrame(alBajar); } }, { passive: true });
  alBajar();

  // Solo en computadora: luz que sigue al cursor y botones magnéticos
  if (matchMedia('(hover: hover) and (pointer: fine)').matches && !quieto) {
    // Profundidad en el diagrama: cada nodo se mueve según su «capa»
    const portada = $('.portada');
    const nodosProf = $$('.diagrama .nodo');
    const nucleo = $('.diagrama .nucleo');
    if (portada && nodosProf.length) {
      portada.addEventListener('pointermove', e => {
        const r = portada.getBoundingClientRect();
        const dx = (e.clientX - r.left) / r.width - .5;
        const dy = (e.clientY - r.top) / r.height - .5;
        nodosProf.forEach(n => {
          const p = parseFloat(n.dataset.prof || 1);
          n.style.translate = `${dx * 26 * p}px ${dy * 22 * p}px`;
        });
        if (nucleo) nucleo.style.transform = `translate(-50%, -50%) perspective(600px) rotateY(${dx * 14}deg) rotateX(${-dy * 14}deg)`;
      });
      portada.addEventListener('pointerleave', () => {
        nodosProf.forEach(n => { n.style.translate = ''; });
        if (nucleo) nucleo.style.transform = '';
      });
    }
    $$('.hito__tarjeta, .pregunta, .paso, .problema, .beneficio').forEach(el => {
      el.classList.add('luz');
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--mx', `${e.clientX - r.left}px`);
        el.style.setProperty('--my', `${e.clientY - r.top}px`);
      });
    });
    $$('.hero .boton--menta, .final .boton--menta').forEach(b => {
      b.addEventListener('pointermove', e => {
        const r = b.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * .18;
        const y = (e.clientY - r.top - r.height / 2) * .28;
        b.style.transform = `translate(${x}px, ${y - 2}px)`;
      });
      b.addEventListener('pointerleave', () => { b.style.transform = ''; });
    });
  }

  // Los enlaces de servicios del pie abren su pestaña
  $$('[data-ir-tab]').forEach(a => a.addEventListener('click', () => {
    const t = document.getElementById('tab-' + a.dataset.irTab);
    if (t) setTimeout(() => t.click(), 400);
  }));

  // Formulario de contacto → hoja «Enlaza Studio — CRM» (y WhatsApp como respaldo)
  const form = $('#formulario');
  const cfg = window.CONEKTRA_FORM || {};
  if (form) {
    const error = $('#form-error');
    const boton = $('button[type="submit"]', form);
    $$('input', form).forEach(i => i.addEventListener('input', () => i.classList.remove('con-error')));
    form.addEventListener('submit', ev => {
      ev.preventDefault();
      const fd = new FormData(form);
      const dato = k => String(fd.get(k) || '').trim();
      const faltan = ['nombre', 'contacto'].filter(k => !dato(k));
      faltan.forEach(k => form.elements[k].classList.add('con-error'));
      if (faltan.length) { error.textContent = cfg.error; form.elements[faltan[0]].focus(); return; }
      error.textContent = '';
      const necesita = fd.getAll('necesita').join(', ');
      // la hoja tiene una sola columna «Contacto»: ahí van el WhatsApp y, si lo dio, el correo
      const contacto = [dato('contacto'), dato('correo')].filter(Boolean).join(' · ');
      const datos = { nombre: dato('nombre'), empresa: dato('empresa'), contacto, necesita, presupuesto: dato('presupuesto'), mensaje: dato('mensaje'), idioma: cfg.lang, web: dato('web') };
      // resumen para seguir la conversación por WhatsApp
      const resumen = (cfg.lang === 'en'
        ? [`Hi Enlaza Studio, I'm ${datos.nombre}${datos.empresa ? ` from ${datos.empresa}` : ''}.`, necesita && `I need: ${necesita}.`, datos.mensaje]
        : [`Hola Enlaza Studio, soy ${datos.nombre}${datos.empresa ? ` de ${datos.empresa}` : ''}.`, necesita && `Necesito: ${necesita}.`, datos.mensaje]
      ).filter(Boolean).join('\n');
      const enlaceWa = cfg.wa ? `https://wa.me/${cfg.wa}?text=${encodeURIComponent(resumen)}` : '';
      const listo = () => {
        form.hidden = true;
        $('#gracias').hidden = false;
        if (enlaceWa) $('#gracias-wa').href = enlaceWa;
      };
      if (!cfg.crm) { if (enlaceWa) window.open(enlaceWa, '_blank', 'noopener'); listo(); return; }
      boton.disabled = true;
      boton.firstChild.textContent = cfg.enviando + ' ';
      fetch(cfg.crm, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(datos) })
        .then(listo)
        .catch(() => { if (enlaceWa) window.open(enlaceWa, '_blank', 'noopener'); listo(); })
        .finally(() => { boton.disabled = false; boton.firstChild.textContent = cfg.enviar + ' '; });
    });
  }

  // Línea del proceso: se llena al bajar por la página y marca los pasos alcanzados
  const proceso = $('#proceso');
  if (proceso) {
    const hitos = $$('.hito', proceso);
    const vertical = () => matchMedia('(max-width: 1020px)').matches;
    let pendiente = false;
    const actualizar = () => {
      pendiente = false;
      const r = proceso.getBoundingClientRect();
      // avance: 0 cuando el proceso entra por abajo, 1 cuando llega a la mitad de la pantalla
      const avance = quieto ? 1 : Math.min(1, Math.max(0, (innerHeight * .85 - r.top) / (r.height * (vertical() ? 1 : .6) + innerHeight * .2)));
      proceso.style.setProperty('--avance', (avance * 100).toFixed(1) + '%');
      hitos.forEach((h, j) => h.classList.toggle('pasado', avance >= (hitos.length > 1 ? j / (hitos.length - 1) : 0) - .001));
    };
    const pedir = () => { if (!pendiente) { pendiente = true; requestAnimationFrame(actualizar); } };
    addEventListener('scroll', pedir, { passive: true });
    addEventListener('resize', pedir);
    actualizar();
  }

  // Pestañas de servicios: avanzan solas con barra de progreso; al tocar una, se quedan quietas
  const caja = $('.servicios');
  const tabs = $$('.pestana');
  const paneles = $$('.panel');
  const DURACION = 7000;
  let actualTab = 0, relojTab = null, visibleTab = false;
  const elegir = n => {
    actualTab = n;
    tabs.forEach((t, j) => {
      const si = j === n;
      t.classList.toggle('activa', si); t.setAttribute('aria-selected', String(si)); t.tabIndex = si ? 0 : -1;
      // reinicia la animación de la barra de progreso
      const barra = $('.pestana__progreso i', t);
      if (barra) { barra.style.animation = 'none'; void barra.offsetWidth; barra.style.animation = ''; }
    });
    paneles.forEach((p, j) => { p.classList.toggle('activo', j === n); p.hidden = j !== n; });
  };
  const arrancarTabs = () => {
    clearTimeout(relojTab);
    if (quieto || !visibleTab || caja.classList.contains('pausado')) return;
    relojTab = setTimeout(() => { elegir((actualTab + 1) % tabs.length); arrancarTabs(); }, DURACION);
  };
  const pausar = () => { caja.classList.add('pausado'); clearTimeout(relojTab); };
  if (caja) {
    caja.style.setProperty('--duracion', DURACION / 1000 + 's');
    if (quieto) caja.classList.add('pausado');
    tabs.forEach((t, j) => {
      t.addEventListener('click', () => {
        pausar(); elegir(j);
        // en celular la maqueta queda debajo de las pestañas: se lleva a la vista
        if (matchMedia('(max-width: 1020px)').matches) {
          const v = $('.vitrina');
          if (v) setTimeout(() => v.scrollIntoView({ behavior: quieto ? 'auto' : 'smooth', block: 'center' }), 120);
        }
      });
      t.addEventListener('keydown', e => {
        const d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        const k = (j + d + tabs.length) % tabs.length;
        pausar(); elegir(k); tabs[k].focus();
      });
    });
    // solo avanzan mientras la sección está en pantalla
    new IntersectionObserver(([e]) => {
      visibleTab = e.isIntersecting;
      if (visibleTab) { elegir(actualTab); arrancarTabs(); } else clearTimeout(relojTab);
    }, { threshold: .35 }).observe(caja);
    elegir(0);
  }
})();
