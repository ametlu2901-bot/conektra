/* Enlaza Studio 3.0 — interacciones de la portada */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fino = matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Menú del celular
  const boton = $('#hamburguesa');
  const cerrar = () => { document.body.classList.remove('menu-abierto'); boton.setAttribute('aria-expanded', 'false'); };
  boton.addEventListener('click', () => boton.setAttribute('aria-expanded', String(document.body.classList.toggle('menu-abierto'))));
  $$('#menu a').forEach(a => a.addEventListener('click', cerrar));

  // Aparición al hacer scroll
  const obs = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
  }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('[data-revelar]').forEach(el => obs.observe(el));

  // Cabecera con fondo al bajar, panel que se endereza y línea del proceso
  const cab = $('#cab');
  const app = $('.app');
  const pasos = $('#pasos');
  const listaPasos = pasos ? $$('.paso', pasos) : [];
  let pendiente = false;
  const alBajar = () => {
    pendiente = false;
    cab.classList.toggle('llena', scrollY > 20);
    // ¿la cabecera está encima de una sección oscura?
    const debajo = document.elementsFromPoint(innerWidth / 2, 40).find(el => !cab.contains(el));
    cab.classList.toggle('cab--oscura', !!(debajo && debajo.closest('.sec--oscura, .final, .pie')));
    if (app && !quieto) {
      const r = app.getBoundingClientRect();
      const t = Math.min(1, Math.max(0, 1 - (r.top - innerHeight * .25) / (innerHeight * .6)));
      app.style.setProperty('--inclina', (10 * (1 - t)).toFixed(2) + 'deg');
      app.style.setProperty('--escala', (.97 + .03 * t).toFixed(4));
    }
    if (pasos) {
      const r = pasos.getBoundingClientRect();
      const avance = quieto ? 1 : Math.min(1, Math.max(0, (innerHeight * .8 - r.top) / (r.height * .7 + innerHeight * .2)));
      pasos.style.setProperty('--avance', (avance * 100).toFixed(1) + '%');
      listaPasos.forEach((p, j) => p.classList.toggle('pasado', avance >= j / (listaPasos.length - 1) - .02));
    }
  };
  addEventListener('scroll', () => { if (!pendiente) { pendiente = true; requestAnimationFrame(alBajar); } }, { passive: true });
  addEventListener('resize', alBajar);
  alBajar();

  // Actividad en vivo del panel: la última fila sube arriba como nueva
  const actividad = $('#actividad');
  if (actividad && !quieto) {
    let visible = false;
    const horas = $$('.act time', actividad).map(t => t.textContent);  // las horas quedan fijas por posición
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(actividad);
    setInterval(() => {
      if (!visible || document.hidden) return;
      const ultima = actividad.lastElementChild;
      $$('.act', actividad).forEach(a => a.classList.remove('nuevo'));
      actividad.prepend(ultima);
      ultima.classList.add('nuevo');
      $$('.act time', actividad).forEach((t, j) => { t.textContent = horas[j]; });
    }, 3200);
  }

  // Soluciones: el texto avanza y la vista fija cambia
  const items = $$('.sol__item');
  const vistas = $$('.sol__vista');
  const indice = $$('.sol__indice a');
  const activar = n => {
    items.forEach((it, j) => it.classList.toggle('activo', j === n));
    vistas.forEach((v, j) => v.classList.toggle('activo', j === n));
    indice.forEach((a, j) => a.classList.toggle('activo', j === n));
  };
  if (items.length) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) activar(+e.target.dataset.sol); }), { rootMargin: '-45% 0px -45% 0px' });
    items.forEach(it => io.observe(it));
  }

  // Campo de partículas (portada y cierre): trazos cortos que giran alrededor de un centro y esquivan el cursor
  const campo = (canvas, opts) => {
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const colores = opts.colores;
    let w, h, dpr, puntos = [], raton = { x: -9999, y: -9999 }, corriendo = false, t0 = performance.now();
    const crear = () => {
      dpr = Math.min(2, devicePixelRatio || 1);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(opts.max, (w * h) / opts.densidad));
      const cx = w / 2, cy = h * opts.centroY;
      puntos = Array.from({ length: n }, () => {
        const ang = Math.random() * Math.PI * 2;
        const rad = opts.radioMin + Math.pow(Math.random(), .8) * Math.max(w, h) * .62;
        return { ang, rad, cx, cy, vel: (Math.random() * .5 + .5) * opts.vel * (rad < 300 ? 1.4 : 1), largo: 2 + Math.random() * 4.5,
                 color: colores[Math.floor(Math.random() * colores.length)], alfa: .25 + Math.random() * .6, dx: 0, dy: 0 };
      });
    };
    const dibujar = (ahora) => {
      const dt = Math.min(50, ahora - t0); t0 = ahora;
      ctx.clearRect(0, 0, w, h);
      for (const p of puntos) {
        if (!quieto) p.ang += p.vel * dt * .00006;
        let x = p.cx + Math.cos(p.ang) * p.rad, y = p.cy + Math.sin(p.ang) * p.rad * .78;
        const ddx = x - raton.x, ddy = y - raton.y, d2 = ddx * ddx + ddy * ddy;
        const empuje = d2 < 16000 ? (1 - d2 / 16000) * 26 : 0;
        const d = Math.sqrt(d2) || 1;
        p.dx += ((ddx / d) * empuje - p.dx) * .08; p.dy += ((ddy / d) * empuje - p.dy) * .08;
        x += p.dx; y += p.dy;
        const rot = Math.atan2(y - p.cy, x - p.cx);
        ctx.strokeStyle = p.color; ctx.globalAlpha = p.alfa; ctx.lineWidth = 1.6; ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(x - Math.cos(rot) * p.largo, y - Math.sin(rot) * p.largo); ctx.lineTo(x + Math.cos(rot) * p.largo, y + Math.sin(rot) * p.largo); ctx.stroke();
      }
      ctx.globalAlpha = 1;
      if (corriendo) requestAnimationFrame(dibujar);
    };
    crear();
    addEventListener('resize', () => { crear(); if (!corriendo) dibujar(performance.now()); });
    if (fino) {
      const zona = canvas.parentElement;
      zona.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); raton.x = e.clientX - r.left; raton.y = e.clientY - r.top; });
      zona.addEventListener('pointerleave', () => { raton.x = raton.y = -9999; });
    }
    if (quieto) { dibujar(performance.now()); return; }
    new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !corriendo) { corriendo = true; t0 = performance.now(); requestAnimationFrame(dibujar); }
      else if (!e.isIntersecting) corriendo = false;
    }).observe(canvas);
  };
  campo($('#campo'), { colores: ['#167a50', '#36c98a', '#1f9e66', '#a8e6c3', '#0b1f18'], densidad: 2600, max: 520, centroY: .36, radioMin: 260, vel: 1 });
  campo($('#campo-final'), { colores: ['#36c98a', '#a8e6c3', '#1f9e66'], densidad: 3200, max: 380, centroY: .5, radioMin: 220, vel: .8 });

  // Luz que sigue al cursor en tarjetas oscuras
  if (fino) $$('.princ').forEach(el => el.addEventListener('pointermove', e => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${e.clientX - r.left}px`); el.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  // Avisos que cambian sobre la escena 3D
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

  // Barra de WhatsApp del celular: aparece al bajar y se esconde en el cierre
  const barraWa = $('#barra-wa');
  if (barraWa) {
    let enCierre = false;
    const revisar = () => {
      const mostrar = scrollY > innerHeight * .6 && !enCierre;
      barraWa.classList.toggle('visible', mostrar);
      barraWa.setAttribute('aria-hidden', String(!mostrar));
      $('a', barraWa).tabIndex = mostrar ? 0 : -1;
    };
    const io = new IntersectionObserver(es => { enCierre = es.some(e => e.isIntersecting); revisar(); }, { threshold: .05 });
    $$('.cierre, #contacto').forEach(el => io.observe(el));
    addEventListener('scroll', revisar, { passive: true });
    revisar();
  }

  // Formulario de contacto → hoja «Enlaza Studio — CRM» (y WhatsApp como respaldo)
  const form = $('#formulario');
  const cfg = window.CONEKTRA_FORM || {};
  if (form) {
    const error = $('#form-error');
    const enviar = $('button[type="submit"]', form);
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
      const resumen = (cfg.lang === 'en'
        ? [`Hi Enlaza Studio, I'm ${datos.nombre}${datos.empresa ? ` from ${datos.empresa}` : ''}.`, necesita && `I need: ${necesita}.`, datos.mensaje]
        : [`Hola Enlaza Studio, soy ${datos.nombre}${datos.empresa ? ` de ${datos.empresa}` : ''}.`, necesita && `Necesito: ${necesita}.`, datos.mensaje]
      ).filter(Boolean).join('\n');
      const enlaceWa = cfg.wa ? `https://wa.me/${cfg.wa}?text=${encodeURIComponent(resumen)}` : '';
      const listo = () => { form.hidden = true; $('#gracias').hidden = false; if (enlaceWa) $('#gracias-wa').href = enlaceWa; };
      if (!cfg.crm) { if (enlaceWa) window.open(enlaceWa, '_blank', 'noopener'); listo(); return; }
      enviar.disabled = true;
      enviar.firstChild.textContent = cfg.enviando + ' ';
      fetch(cfg.crm, { method: 'POST', mode: 'no-cors', body: new URLSearchParams(datos) })
        .then(listo)
        .catch(() => { if (enlaceWa) window.open(enlaceWa, '_blank', 'noopener'); listo(); })
        .finally(() => { enviar.disabled = false; enviar.firstChild.textContent = cfg.enviar + ' '; });
    });
  }
})();
