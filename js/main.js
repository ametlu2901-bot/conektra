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

  // Pestañas de servicios
  const tabs = $$('.pestana');
  const paneles = $$('.panel');
  const elegir = n => {
    tabs.forEach((t, j) => { t.classList.toggle('activa', j === n); t.setAttribute('aria-selected', String(j === n)); t.tabIndex = j === n ? 0 : -1; });
    paneles.forEach((p, j) => { p.classList.toggle('activo', j === n); p.hidden = j !== n; });
  };
  tabs.forEach((t, j) => {
    t.addEventListener('click', () => elegir(j));
    t.addEventListener('keydown', e => {
      const d = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      const k = (j + d + tabs.length) % tabs.length;
      elegir(k); tabs[k].focus();
    });
  });
  elegir(0);
})();
