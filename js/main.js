/* Integrafy — interacciones */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;

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
  const avisos = window.INTEGRAFY_AVISOS || [];
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

  // Lista de palabras que va pasando
  const pista = $('#palabras');
  if (pista) {
    const items = $$('li', pista);
    const alto = () => items[0].getBoundingClientRect().height;
    let i = 0;
    const mostrar = () => {
      items.forEach((li, j) => li.classList.toggle('activa', j === i));
      pista.style.transform = `translateY(${(2 - i) * alto()}px)`;
    };
    mostrar();
    if (!quieto) setInterval(() => { i = (i + 1) % items.length; mostrar(); }, 2000);
    addEventListener('resize', mostrar);
  }

  // Pasos del flujo (se avanzan solos y también al tocarlos)
  const pasos = $$('.paso');
  const cuadros = $$('.cuadro');
  if (pasos.length) {
    let actual = 0, reloj;
    const ir = n => {
      actual = n;
      pasos.forEach((p, j) => { p.classList.toggle('activo', j === n); p.setAttribute('aria-pressed', String(j === n)); });
      cuadros.forEach((c, j) => c.classList.toggle('activo', j === n));
    };
    const arrancar = () => { clearInterval(reloj); if (!quieto) reloj = setInterval(() => ir((actual + 1) % pasos.length), 4000); };
    pasos.forEach((p, j) => p.addEventListener('click', () => { ir(j); arrancar(); }));
    arrancar();
  }

  // Formulario de contacto → hoja «Integrafy — CRM» (y WhatsApp como respaldo)
  const form = $('#formulario');
  const cfg = window.INTEGRAFY_FORM || {};
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
      const datos = { nombre: dato('nombre'), empresa: dato('empresa'), contacto: dato('contacto'), necesita, presupuesto: dato('presupuesto'), mensaje: dato('mensaje'), idioma: cfg.lang, web: dato('web') };
      // resumen para seguir la conversación por WhatsApp
      const resumen = (cfg.lang === 'en'
        ? [`Hi Integrafy, I'm ${datos.nombre}${datos.empresa ? ` from ${datos.empresa}` : ''}.`, necesita && `I need: ${necesita}.`, datos.mensaje]
        : [`Hola Integrafy, soy ${datos.nombre}${datos.empresa ? ` de ${datos.empresa}` : ''}.`, necesita && `Necesito: ${necesita}.`, datos.mensaje]
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
      t.addEventListener('click', () => { pausar(); elegir(j); });
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
