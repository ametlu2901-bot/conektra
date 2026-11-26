/* Portal Enlaza Studio — interfaz (rutas, vistas y acciones) */
import { I, LOGO } from './iconos.js?v=2';
import * as db from './datos.js?v=16';
import { metaListo, registroIntegrado } from './meta.js?v=1';

const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const esc = v => String(v ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
const dinero = n => '$' + Math.round(n).toLocaleString('en-US');
const iniciales = n => n.split(/\s+/).slice(0, 2).map(x => x[0]).join('').toUpperCase();
const digitos = tel => tel.replace(/\D/g, '');
const hace = iso => {
  const s = (Date.now() - new Date(iso)) / 1000;
  if (s < 60) return 'ahora';
  if (s < 3600) return `${Math.floor(s / 60)} min`;
  if (s < 86400) return `${Math.floor(s / 3600)} h`;
  const d = Math.floor(s / 86400); return d === 1 ? 'ayer' : `${d} días`;
};
const fechaCorta = f => new Date(f.length === 10 ? f + 'T00:00' : f).toLocaleDateString('es-PA', { day: 'numeric', month: 'short' });
const wa = (tel, texto) => `https://wa.me/${digitos(tel)}?text=${encodeURIComponent(texto)}`;

const RUTAS = [
  ['inicio', 'Inicio', 'base'], ['clientes', 'Clientes', 'crm'], ['cotizaciones', 'Cotizaciones', 'factura'], ['cobros', 'Cobros', 'pago'],
  ['conversaciones', 'Conversaciones', 'chat'], ['bot', 'Bot', 'bot'], ['reportes', 'Reportes', 'grafica'], ['automatizaciones', 'Automatizaciones', 'rayo'],
];
const ICO_ACT = { whatsapp: 'wa', web: 'web', seguimiento: 'crm', cobro: 'pago', pago: 'check', cotizacion: 'factura' };

// ---------------------------------------------------------------- avisos y diálogos
function aviso(texto) {
  const t = document.createElement('div'); t.className = 'aviso'; t.innerHTML = `${I.check}<span>${esc(texto)}</span>`;
  document.body.append(t); requestAnimationFrame(() => t.classList.add('visible'));
  setTimeout(() => { t.classList.remove('visible'); setTimeout(() => t.remove(), 400); }, 2600);
}
function dialogo(titulo, campos, enviar, boton = 'Guardar') {
  const d = document.createElement('dialog'); d.className = 'dialogo';
  d.innerHTML = `<form method="dialog"><header><h3>${esc(titulo)}</h3><button type="button" class="icono-btn" data-cerrar aria-label="Cerrar">✕</button></header>
    <div class="dialogo__campos">${campos}</div><p class="dialogo__error" role="alert"></p>
    <footer><button type="button" class="btn btn--suave" data-cerrar>Cancelar</button><button class="btn btn--tinta" value="ok">${esc(boton)}</button></footer></form>`;
  document.body.append(d); d.showModal();
  $$('[data-cerrar]', d).forEach(b => b.addEventListener('click', () => d.close()));
  d.addEventListener('close', () => d.remove());
  $('form', d).addEventListener('submit', e => {
    const datos = Object.fromEntries(new FormData(e.target));
    const error = enviar(datos);
    if (error) { e.preventDefault(); $('.dialogo__error', d).textContent = error; }
  });
  const primero = $('input, select, textarea', d); if (primero) primero.focus();
}
const campo = (etq, html) => `<label class="campo"><span>${etq}</span>${html}</label>`;
const opcionesContactos = sel => db.contactos().map(x => `<option value="${x.id}"${x.id === sel ? ' selected' : ''}>${esc(x.nombre)}</option>`).join('');

// ---------------------------------------------------------------- marco
function marco(ruta, contenido) {
  const N = db.negocio();
  const vencidos = db.resumen().vencidos.length;
  const menu = RUTAS.map(([r, t, ic]) => `<a href="#/${r}" class="${r === ruta ? 'activo' : ''}">${I[ic]}<span>${t}</span>${r === 'cobros' && vencidos ? `<b>${vencidos}</b>` : ''}</a>`).join('');
  const hora = new Date().getHours();
  const saludo = hora < 12 ? 'Buenos días' : hora < 19 ? 'Buenas tardes' : 'Buenas noches';
  return `<div class="portal">
    <aside class="lado" id="lado">
      <a class="lado__marca" href="#/inicio">${LOGO}<span>Enlaza Studio</span></a>
      <nav class="lado__menu">${menu}</nav>
      <div class="lado__pie">
        <a href="#/ajustes" class="${ruta === 'ajustes' ? 'activo' : ''}">${I.soporte}<span>Ajustes</span></a>
        <div class="lado__negocio"><span class="avatar">${iniciales(N.nombre)}</span><span><b>${esc(N.nombre)}</b><small>${!db.enModoReal() ? 'Modo demostración' : N.whatsapp_conectado ? 'WhatsApp conectado' : esc(db.correoUsuario())}</small></span></div>
      </div>
    </aside>
    <div class="principal">
      <header class="barra">
        <button class="icono-btn barra__menu" id="abrir-menu" aria-label="Menú">☰</button>
        <div><small>${saludo}${N.dueno ? `, ${esc(N.dueno.split(' ')[0])}` : ''}</small><b>${esc(N.nombre)}</b></div>
        <span class="chip"><i></i>${(f => f[0].toUpperCase() + f.slice(1))(new Date().toLocaleDateString('es-PA', { weekday: 'long', day: 'numeric', month: 'long' }))}</span>
        <label class="buscar">${I.lupa}<input id="buscar" type="search" placeholder="Buscar clientes…" autocomplete="off"></label>
        <button class="avatar avatar--btn" id="salir" title="Cerrar sesión">${iniciales(N.dueno || N.nombre)}</button>
      </header>
      ${db.enModoReal() ? '' : `<div class="demo-banda">${I.escudo}<span><b>Estás viendo una demo.</b> Los clientes, cotizaciones y cobros son de ejemplo: pruébalo con confianza, lo que cambies se queda solo en este navegador.</span>${db.hayConexion() ? '<button class="btn btn--mini btn--tinta" id="demo-crear">Crear mi cuenta</button>' : ''}</div>`}
      <main class="vista" id="vista">${contenido}</main>
    </div>
  </div>`;
}

// ---------------------------------------------------------------- vistas
const V = {};

V.inicio = () => {
  const R = db.resumen();
  const act = db.actividad().slice(0, 6).map(a => `<li class="act"><span class="act__ico act__ico--${a.tipo}">${I[ICO_ACT[a.tipo]] || I.check}</span><span class="act__txt"><b>${esc(a.titulo)}</b><small>${esc(a.detalle)}</small></span><time>${hace(a.fecha)}</time></li>`).join('');
  const tope = Math.max(...R.embudo.map(x => x[1]), 1);
  const barras = R.embudo.map(([t, v]) => `<li><span>${t}</span><i style="--v:${(v / tope).toFixed(2)}"><b>${v}</b></i></li>`).join('');
  const proximos = db.cobros().filter(cb => cb.estado !== 'pagado').slice(0, 4).map(cb => {
    const e = db.estadoCobro(cb); const x = db.contacto(cb.contacto_id);
    return `<li><span class="mini-av">${iniciales(x.nombre)}</span><span class="crece"><b>${esc(x.nombre)}</b><small>${esc(cb.concepto)}</small></span><b>${dinero(cb.monto)}</b><span class="pill pill--${e.id}">${e.texto}</span></li>`;
  }).join('');
  const rep = [`${R.clientesHoy || 0} clientes nuevos hoy`, `${R.abiertas} cotizaciones abiertas`, `${dinero(R.cobradoMes)} cobrados este mes`, `${R.venceSemana} pagos vencen esta semana`].map(x => `<li>${x}</li>`).join('');
  return `
    <div class="kpis">
      <a class="kpi" href="#/clientes"><small>Clientes nuevos (mes)</small><b>${R.clientesNuevos}</b><span>${R.clientesHoy ? `+${R.clientesHoy} hoy` : 'Sin nuevos hoy'}</span></a>
      <a class="kpi" href="#/cotizaciones"><small>Cotizaciones abiertas</small><b>${R.abiertas}</b><span>${R.porSeguir} por seguir</span></a>
      <a class="kpi" href="#/cobros"><small>Por cobrar</small><b>${dinero(R.porCobrar)}</b><span class="${R.vencidos.length ? 'rojo' : ''}">${R.vencidos.length ? `${R.vencidos.length} vencidos · ` : ''}${R.venceSemana} vencen esta semana</span></a>
      <div class="kpi"><small>Ganado (mes)</small><b>${dinero(R.ganadoMes)}</b><span>${dinero(R.cobradoMes)} ya cobrados</span></div>
    </div>
    <div class="rejilla-inicio">
      <section class="caja"><h4><span class="vivo"></span>Actividad reciente</h4><ul class="act__lista">${act}</ul></section>
      <section class="caja"><h4>Ventas del mes</h4><ul class="barras">${barras}</ul>
        <svg class="linea-graf" viewBox="0 0 200 60" preserveAspectRatio="none"><defs><linearGradient id="gA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#36c98a" stop-opacity=".35"/><stop offset="1" stop-color="#36c98a" stop-opacity="0"/></linearGradient></defs><path d="M0 48 L25 44 L50 46 L75 34 L100 37 L125 26 L150 28 L175 15 L200 10 L200 60 L0 60Z" fill="url(#gA)"/><path class="linea-graf__trazo" d="M0 48 L25 44 L50 46 L75 34 L100 37 L125 26 L150 28 L175 15 L200 10" fill="none" stroke="#1f9e66" stroke-width="2"/></svg>
      </section>
      <section class="caja"><h4>Próximos cobros <a class="ver" href="#/cobros">Ver todos</a></h4><ul class="lista-simple">${proximos || '<li class="vacio">No hay cobros pendientes.</li>'}</ul></section>
      <section class="caja caja--wa"><h4>${I.wa} Resumen del día <small>vista previa</small></h4>
        <div class="globo"><b>Resumen del día ☀️</b><ul>${rep}</ul><small>7:00 a. m. ✓✓</small></div>
        <p class="nota">Así llegará cada mañana a tu WhatsApp cuando lo conectemos.</p></section>
    </div>`;
};

V.clientes = (filtro = '') => {
  const q = filtro.toLowerCase();
  const lista = db.contactos().filter(x => !q || (x.nombre + x.telefono + x.nota + x.origen).toLowerCase().includes(q));
  const etapaDe = cid => { const qs = db.cotizaciones().filter(c => c.contacto_id === cid); return qs.length ? db.ETAPAS.find(e => e.id === qs[qs.length - 1].etapa) : null; };
  const filas = lista.map(x => { const e = etapaDe(x.id); return `<tr data-id="${x.id}"><td><span class="mini-av">${iniciales(x.nombre)}</span><span><b>${esc(x.nombre)}</b><small>${esc(x.nota)}</small></span></td>
    <td class="mono">${esc(x.telefono)}</td><td><span class="etq-origen">${esc(x.origen)}</span></td><td>${e ? `<span class="pill pill--etapa-${e.id}">${e.nombre}</span>` : '<span class="tenue">—</span>'}</td><td class="tenue">${fechaCorta(x.creado)}</td>
    <td class="acciones"><a class="icono-btn" href="${wa(x.telefono, `Hola ${x.nombre.split(' ')[0]}, `)}" target="_blank" rel="noopener" title="Escribir por WhatsApp">${I.wa}</a></td></tr>`; }).join('');
  return `<div class="cab-vista"><div><h1>Clientes</h1><p>${lista.length} ${lista.length === 1 ? 'cliente' : 'clientes'}${q ? ` para «${esc(filtro)}»` : ''}</p></div><button class="btn btn--tinta" id="nuevo-cliente">${I.mas} Nuevo cliente</button></div>
    <div class="caja caja--tabla"><table class="tabla"><thead><tr><th>Cliente</th><th>Teléfono</th><th>Origen</th><th>Etapa</th><th>Desde</th><th></th></tr></thead><tbody>${filas || '<tr><td colspan="6" class="vacio">No hay clientes que coincidan.</td></tr>'}</tbody></table></div>`;
};

V.cotizaciones = () => {
  const cols = db.ETAPAS.map(e => {
    const qs = db.cotizaciones().filter(q => q.etapa === e.id);
    const total = qs.reduce((s, q) => s + q.monto, 0);
    const tarjetas = qs.map(q => {
      const x = db.contacto(q.contacto_id); const dias = Math.floor((Date.now() - new Date(q.ultimo_contacto)) / 864e5);
      const atrasada = dias >= 2 && !['ganado', 'perdido'].includes(q.etapa);
      return `<article class="tarj" draggable="true" data-id="${q.id}"><header><small class="mono">#${q.numero}</small>${atrasada ? `<span class="pill pill--pronto">${dias} días sin respuesta</span>` : ''}</header>
        <b>${esc(x.nombre)}</b><p>${esc(q.servicio)}</p><footer><b>${dinero(q.monto)}</b>
        ${atrasada ? `<a class="btn btn--mini" href="${wa(x.telefono, `Hola ${x.nombre.split(' ')[0]}, te escribo de ${db.negocio().nombre} para saber si pudiste revisar la cotización #${q.numero} (${q.servicio}). ¿Te ayudo con algo?`)}" target="_blank" rel="noopener" data-seguir="${q.id}">${I.wa} Seguir</a>` : ''}</footer>
        <select class="tarj__mover" data-mover="${q.id}" aria-label="Mover a">${db.ETAPAS.map(o => `<option value="${o.id}"${o.id === q.etapa ? ' selected' : ''}>${o.nombre}</option>`).join('')}</select></article>`;
    }).join('');
    return `<section class="col col--${e.id}" data-etapa="${e.id}"><h3>${e.nombre}<span>${qs.length}</span></h3><small class="col__total">${dinero(total)}</small><div class="col__tarjetas">${tarjetas}</div></section>`;
  }).join('');
  return `<div class="cab-vista"><div><h1>Cotizaciones</h1><p>Arrastra cada tarjeta a su etapa. Las que llevan 2 días o más sin respuesta se marcan para darles seguimiento.</p></div><button class="btn btn--tinta" id="nueva-cot">${I.mas} Nueva cotización</button></div>
    <div class="tablero">${cols}</div>`;
};

V.cobros = () => {
  const R = db.resumen();
  const filas = db.cobros().map(cb => {
    const e = db.estadoCobro(cb); const x = db.contacto(cb.contacto_id);
    const pagos = db.textoPagos();
    const msg = `Hola ${x.nombre.split(' ')[0]}, te saluda ${db.negocio().nombre}. Te recordamos el pago de ${dinero(cb.monto)} por ${cb.concepto}, ${e.id === 'vencido' ? `que venció el ${fechaCorta(cb.vence)}` : `que vence el ${fechaCorta(cb.vence)}`}. ¡Gracias!${pagos ? `\n\n${pagos}` : ''}`;
    return `<tr><td><span class="mini-av">${iniciales(x.nombre)}</span><span><b>${esc(x.nombre)}</b><small>${esc(cb.concepto)}</small></span></td><td class="num"><b>${dinero(cb.monto)}</b></td><td class="tenue">${fechaCorta(cb.vence)}</td><td><span class="pill pill--${e.id}">${e.texto}</span></td>
      <td class="acciones">${cb.estado === 'pagado' ? '' : `<a class="btn btn--mini" href="${wa(x.telefono, msg)}" target="_blank" rel="noopener" data-recordar="${cb.id}">${I.wa} Recordar</a><button class="btn btn--mini btn--suave" data-pagado="${cb.id}">${I.check} Pagado</button>`}</td></tr>`;
  }).join('');
  return `<div class="cab-vista"><div><h1>Cobros</h1><p>Quién te debe, cuánto y desde cuándo. Envía el recordatorio con un toque.</p></div><button class="btn btn--tinta" id="nuevo-cobro">${I.mas} Nuevo cobro</button></div>
    <div class="kpis kpis--3"><div class="kpi"><small>Por cobrar</small><b>${dinero(R.porCobrar)}</b><span>${R.venceSemana} vencen esta semana</span></div>
      <div class="kpi"><small>Vencido</small><b class="${R.vencidos.length ? 'rojo' : ''}">${dinero(R.vencidos.reduce((s, cb) => s + cb.monto, 0))}</b><span>${R.vencidos.length} ${R.vencidos.length === 1 ? 'cobro' : 'cobros'}</span></div>
      <div class="kpi"><small>Cobrado este mes</small><b>${dinero(R.cobradoMes)}</b><span>Pagos registrados</span></div></div>
    <div class="caja caja--tabla"><table class="tabla"><thead><tr><th>Cliente</th><th class="num">Monto</th><th>Vence</th><th>Estado</th><th></th></tr></thead><tbody>${filas}</tbody></table></div>`;
};

V.conversaciones = (abierta) => {
  const convs = db.conversaciones();
  const real = db.enModoReal() && db.negocio().whatsapp_conectado;   // chats reales: se responde desde aquí
  if (!convs.length) {
    return `<div class="cab-vista"><div><h1>Conversaciones</h1><p>Todos los chats de WhatsApp de tu negocio en un solo lugar, conectados con tus clientes y cotizaciones.</p></div></div>
      ${real
        ? `<div class="aviso-conectar">${I.wa}<div><b>Todavía no hay conversaciones</b><p>Tu WhatsApp ya está conectado. Cuando un cliente te escriba, el chat aparecerá aquí solo.</p></div></div>`
        : `<div class="aviso-conectar">${I.wa}<div><b>Todavía no hay conversaciones</b><p>Cuando conectes el WhatsApp de tu negocio, tus chats aparecerán aquí. Mientras tanto, desde Clientes, Cotizaciones y Cobros puedes escribir por WhatsApp con un toque.</p></div><a class="btn btn--verde" href="#/ajustes">Ver cómo conectar</a></div>`}`;
  }
  const actual = convs.find(c => c.id === abierta) || convs[0];
  const lista = convs.map(c => { const x = db.contacto(c.contacto_id); const u = c.mensajes[c.mensajes.length - 1];
    const nuevos = c !== actual && c.no_leidos ? `<i class="conv__nuevos">${c.no_leidos}</i>` : '';
    return `<a href="#/conversaciones/${c.id}" class="conv${c === actual ? ' activo' : ''}"><span class="mini-av">${iniciales(x.nombre)}</span><span class="crece"><b>${esc(x.nombre)}</b><small>${u.dir === 'out' ? 'Tú: ' : ''}${esc(u.texto)}</small></span><span class="conv__lado"><time>${hace(u.fecha)}</time>${nuevos}</span></a>`; }).join('');
  const x = db.contacto(actual.contacto_id);
  const marca = m => m.dir !== 'out' ? '' : m.estado === 'fallido' ? ' <span class="msg__fallo">No se entregó</span>' : `<span class="msg__visto${m.estado === 'leido' ? ' msg__visto--leido' : ''}">${m.estado === 'enviado' && real ? ' ✓' : ' ✓✓'}</span>`;
  const msgs = actual.mensajes.map(m => `<div class="msg msg--${m.dir}">${esc(m.texto)}<small>${m.origen === 'celular' ? 'Desde tu celular · ' : ''}${new Date(m.fecha).toLocaleTimeString('es-PA', { hour: 'numeric', minute: '2-digit' })}${marca(m)}</small></div>`).join('');
  const abierto24 = !real || db.dentroDe24h(actual);
  return `<div class="cab-vista"><div><h1>Conversaciones</h1><p>Todos los chats de WhatsApp de tu negocio en un solo lugar, conectados con tus clientes y cotizaciones.</p></div></div>
    ${db.negocio().whatsapp_conectado ? '' : `<div class="aviso-conectar aviso-conectar--fino">${I.wa}<div><b>Conecta tu WhatsApp para ver tus chats reales</b><p>Estas conversaciones son de ejemplo. Sigues usando WhatsApp en tu celular y los mensajes también llegan aquí.</p></div><a class="btn btn--verde" href="#/ajustes">Ver cómo conectar</a></div>`}
    <div class="bandeja"><nav class="bandeja__lista">${lista}</nav>
      <section class="chat"><header><span class="mini-av">${iniciales(x.nombre)}</span><span class="crece"><b>${esc(x.nombre)}</b><small class="mono">${esc(x.telefono)}</small></span></header>
        <div class="chat__cuerpo">${msgs}</div>
        ${abierto24 ? '' : '<p class="chat__regla">Pasaron más de 24 horas desde su último mensaje. Por reglas de WhatsApp, lo que escribas se abrirá en tu celular.</p>'}
        <form class="chat__escribir" id="escribir"><input placeholder="${real && abierto24 ? 'Escribe un mensaje…' : 'Escribe un mensaje… (se abrirá WhatsApp)'}" name="texto" autocomplete="off" maxlength="4096"><button class="btn btn--verde btn--mini" aria-label="Enviar">${I.flecha}</button></form>
        <input type="hidden" id="chat-tel" value="${esc(x.telefono)}"><input type="hidden" id="chat-id" value="${esc(actual.id)}">
        <input type="hidden" id="chat-modo" value="${real && abierto24 ? 'api' : 'celular'}"></section>
      ${fichaCliente(x)}</div>`;
};

/** Panel derecho de la bandeja: quién es, qué cotizaciones y cobros tiene, y acciones con un toque. */
function fichaCliente(x) {
  const qs = db.cotizaciones().filter(q => q.contacto_id === x.id && q.etapa !== 'perdido').sort((a, b) => b.creada.localeCompare(a.creada));
  const cbs = db.cobros().filter(cb => cb.contacto_id === x.id && cb.estado !== 'pagado');
  const etapa = id => db.ETAPAS.find(e => e.id === id)?.nombre ?? id;
  return `<aside class="ficha-cli">
      <div class="ficha-cli__quien"><span class="avatar">${iniciales(x.nombre)}</span><b>${esc(x.nombre)}</b><small class="mono">${esc(x.telefono)}</small>
        ${x.origen ? `<span class="pill">${esc(x.origen)}</span>` : ''}</div>
      ${x.nota ? `<p class="ficha-cli__nota">${esc(x.nota)}</p>` : ''}
      <h5>Cotizaciones</h5>
      ${qs.length ? `<ul class="ficha-cli__lista">${qs.slice(0, 4).map(q => `<li><span><b>#${q.numero}</b> ${esc(q.servicio)}</span><span class="ficha-cli__dato"><b>${dinero(q.monto)}</b><span class="pill pill--etapa-${q.etapa}">${etapa(q.etapa)}</span></span></li>`).join('')}</ul>`
        : '<p class="tenue ficha-cli__vacio">Sin cotizaciones abiertas.</p>'}
      <h5>Cobros pendientes</h5>
      ${cbs.length ? `<ul class="ficha-cli__lista">${cbs.slice(0, 4).map(cb => { const e = db.estadoCobro(cb); return `<li><span>${esc(cb.concepto)}</span><span class="ficha-cli__dato"><b>${dinero(cb.monto)}</b><span class="pill${e.id === 'vencido' ? ' pill--vencido' : e.id === 'pronto' ? ' pill--pronto' : ''}">${e.texto}</span></span></li>`; }).join('')}</ul>`
        : '<p class="tenue ficha-cli__vacio">Al día: no debe nada.</p>'}
      <div class="ficha-cli__acciones">
        <button class="btn btn--tinta btn--ancho" data-cot-para="${esc(x.id)}">${I.mas} Nueva cotización</button>
        <button class="btn btn--suave btn--ancho" data-cobro-para="${esc(x.id)}">${I.mas} Nuevo cobro</button>
      </div>
    </aside>`;
}

V.reportes = () => {
  const qs = db.cotizaciones();
  const porOrigen = db.ORIGENES.map(o => [o, db.contactos().filter(x => x.origen === o).length]);
  const topeO = Math.max(...porOrigen.map(x => x[1]), 1);
  const ganadas = qs.filter(q => q.etapa === 'ganado').length, cerradas = qs.filter(q => ['ganado', 'perdido'].includes(q.etapa)).length;
  const vm = db.ventasPorMes();
  const meses = vm.map(([m]) => m[0].toUpperCase() + m.slice(1)), valores = vm.map(([, v]) => v);
  const topeM = Math.max(...valores, 1);
  return `<div class="cab-vista"><div><h1>Reportes</h1><p>Cómo va tu negocio, sin abrir una hoja de cálculo.</p></div></div>
    <div class="kpis"><div class="kpi"><small>Tasa de cierre</small><b>${cerradas ? Math.round(ganadas / cerradas * 100) : 0}%</b><span>${ganadas} de ${cerradas} cerradas</span></div>
      <div class="kpi"><small>Ticket promedio</small><b>${dinero(qs.reduce((s, q) => s + q.monto, 0) / Math.max(qs.length, 1))}</b><span>Por cotización</span></div>
      <div class="kpi"><small>Ganado este mes</small><b>${dinero(db.resumen().ganadoMes)}</b><span>Cotizaciones ganadas</span></div>
      <div class="kpi"><small>Por cobrar</small><b>${dinero(db.resumen().porCobrar)}</b><span>Pendiente</span></div></div>
    <div class="rejilla-2">
      <section class="caja"><h4>Cobrado por mes ${db.enModoReal() ? '' : '<small>meses anteriores de ejemplo</small>'}</h4><div class="columnas">${meses.map((m, j) => `<div><i style="--h:${(valores[j] / topeM * 100).toFixed(0)}%"><b>${dinero(valores[j])}</b></i><span>${m}</span></div>`).join('')}</div></section>
      <section class="caja"><h4>¿De dónde vienen tus clientes?</h4><ul class="barras barras--anchas">${porOrigen.map(([o, v]) => `<li><span>${o}</span><i style="--v:${(v / topeO).toFixed(2)}"><b>${v}</b></i></li>`).join('')}</ul></section>
    </div>`;
};

V.automatizaciones = () => {
  const N = db.negocio();
  const items = db.automatizaciones().map(a => `<article class="auto${a.activa ? ' auto--activa' : ''}"><span class="auto__ico">${I[a.canal === 'whatsapp' ? 'wa' : 'chat']}</span>
    <div class="crece"><h3>${esc(a.nombre)}</h3><p>${esc(a.detalle)}</p><small class="auto__canal">${a.canal === 'whatsapp' ? (N.whatsapp_conectado ? 'Por WhatsApp' : 'Por WhatsApp · requiere conectar tu número') : 'Por correo'}</small></div>
    <button class="interruptor" role="switch" aria-checked="${a.activa}" data-auto="${a.id}" aria-label="${esc(a.nombre)}"><i></i></button></article>`).join('');
  return `<div class="cab-vista"><div><h1>Automatizaciones</h1><p>Lo que tu negocio hace solo, mientras tú trabajas.</p></div></div><div class="autos">${items}</div>`;
};

// ---------------------------------------------------------------- bot de WhatsApp
const opcionBot = (o, i) => `<div class="bot-op">
    <span class="bot-op__num">${i + 1}</span>
    <div class="bot-op__campos">
      <input name="titulo" value="${esc(o.titulo)}" maxlength="24" placeholder="Ej.: Horario de atención" aria-label="Nombre de la opción ${i + 1}">
      <textarea name="respuesta" rows="2" maxlength="1000" placeholder="Lo que responde el bot cuando el cliente la elige" aria-label="Respuesta de la opción ${i + 1}">${esc(o.respuesta)}</textarea>
    </div>
    <button type="button" class="icono-btn" data-quitar-op="${i}" aria-label="Quitar la opción ${i + 1}">✕</button></div>`;

V.bot = () => {
  const B = db.bot(), N = db.negocio();
  const estado = !db.enModoReal() ? 'En la demostración el bot se prueba aquí, en la vista previa.'
    : !N.whatsapp_conectado ? 'Empieza a responder cuando conectes tu WhatsApp (en Ajustes).'
    : B.activo ? 'Encendido: responde a los clientes que te escriben.' : 'Apagado: no responde a nadie.';
  return `<div class="cab-vista"><div><h1>Bot de WhatsApp</h1><p>Cuando un cliente te escribe, le responde al momento con un saludo y un menú de opciones.</p></div>
      <label class="bot__encendido"><span>${B.activo ? 'Encendido' : 'Apagado'}</span><button class="interruptor" role="switch" aria-checked="${B.activo}" id="bot-activo" aria-label="Bot encendido"><i></i></button></label></div>
    <div class="bot">
      <form class="caja bot__editor" id="form-bot">
        ${campo('Saludo', `<textarea name="saludo" rows="3" maxlength="900" required>${esc(B.saludo)}</textarea>`)}
        <p class="nota">Escribe <code>{negocio}</code> y se cambia por el nombre de tu negocio.</p>
        <h4>Opciones del menú</h4>
        <div class="bot__ops" id="bot-ops">${B.opciones.map(opcionBot).join('')}</div>
        <button type="button" class="btn btn--suave" id="bot-mas"${B.opciones.length >= db.BOT_MAX_OPCIONES ? ' disabled' : ''}>${I.mas} Agregar opción</button>
        <label class="check"><input type="checkbox" name="pagos_en_menu"${B.pagos_en_menu ? ' checked' : ''}><span>Agregar <b>«Formas de pago»</b>: responde con tus <a href="#/ajustes">formas de pago</a>${db.pagos().length ? '' : ' (todavía no agregaste ninguna)'}.</span></label>
        <label class="check"><input type="checkbox" name="humano_en_menu"${B.humano_en_menu ? ' checked' : ''}><span>Agregar <b>«Hablar con alguien»</b>: el bot se calla en ese chat y te avisa.</span></label>
        <div class="bot__pie"><button class="btn btn--tinta">Guardar cambios</button><span class="nota" role="status">${estado}</span></div>
      </form>
      <aside class="bot__vista"><div class="cel" id="cel" aria-label="Vista previa del bot"></div>
        <p class="nota">Vista previa: toca «Ver opciones» y elige una, como lo haría tu cliente.</p></aside>
    </div>
    <section class="caja bot__reglas"><h4>Cómo se comporta</h4><ul>
      <li>Solo responde cuando un cliente te escribe. Nunca escribe primero.</li>
      <li>Si tú o tu equipo respondieron ese chat en las últimas 12 horas, no se mete.</li>
      <li>Muestra el menú una vez cada 12 horas por cliente. Si el cliente escribe «menú», lo vuelve a ver.</li>
      <li>Los clientes también pueden responder con el número de la opción: 1, 2, 3…</li></ul></section>`;
};

/** Lee lo que está escrito en el editor del bot (sin guardar). */
function leerBot() {
  const f = $('#form-bot');
  return {
    activo: db.bot().activo,
    saludo: $('[name=saludo]', f).value.trim(),
    opciones: $$('.bot-op', f).map(op => ({ titulo: $('[name=titulo]', op).value.trim(), respuesta: $('[name=respuesta]', op).value.trim() })),
    pagos_en_menu: $('[name=pagos_en_menu]', f).checked,
    humano_en_menu: $('[name=humano_en_menu]', f).checked,
  };
}

/** El celular de la vista previa, desde el punto de vista del cliente (sus mensajes a la derecha). */
function pintarCelular(b, paso = {}) {
  const cel = $('#cel'); if (!cel) return;
  const filas = db.filasBot(b);
  const elegida = filas.find(f => f.id === paso.elegida);
  const hora = new Date().toLocaleTimeString('es-PA', { hour: 'numeric', minute: '2-digit' });
  const burbuja = (lado, html) => `<div class="msg msg--${lado}">${html}<small>${hora}</small></div>`;
  cel.innerHTML = `<header class="cel__barra"><span class="mini-av">${iniciales(db.negocio().nombre)}</span><span><b>${esc(db.negocio().nombre)}</b><small>en línea</small></span></header>
    <div class="cel__chat">
      ${burbuja('out', 'Hola, buenas')}
      ${b.activo ? `<div class="msg msg--in msg--menu">${esc(db.saludoBot(b)).replace(/\n/g, '<br>')}<small>${hora}</small>
          ${filas.length ? `<button type="button" class="cel__ver" id="cel-ver">${I.hoja} Ver opciones</button>` : ''}</div>`
        : '<p class="cel__apagado">El bot está apagado: este mensaje lo contestas tú.</p>'}
      ${elegida ? burbuja('out', esc(elegida.titulo)) + burbuja('in', esc(elegida.respuesta).replace(/\n/g, '<br>')) : ''}
    </div>
    ${paso.lista ? `<div class="cel__hoja"><header><button type="button" class="icono-btn" id="cel-cerrar" aria-label="Cerrar">✕</button><b>Opciones</b></header>
        <ul>${filas.map(f => `<li><button type="button" data-fila="${f.id}">${esc(f.titulo)}<i></i></button></li>`).join('')}</ul></div>` : ''}`;
  const ver = $('#cel-ver'); if (ver) ver.addEventListener('click', () => pintarCelular(b, { lista: true }));
  const cerrar = $('#cel-cerrar'); if (cerrar) cerrar.addEventListener('click', () => pintarCelular(b));
  $$('[data-fila]', cel).forEach(x => x.addEventListener('click', () => pintarCelular(b, { elegida: x.dataset.fila })));
  const chat = $('.cel__chat', cel); chat.scrollTop = chat.scrollHeight;
}

V.ajustes = () => {
  const N = db.negocio();
  return `<div class="cab-vista"><div><h1>Ajustes</h1><p>Datos de tu negocio y conexiones.</p></div></div>
    <div class="rejilla-2">
      <section class="caja"><h4>Tu negocio</h4><form class="form-ajustes" id="form-negocio">
        ${campo('Nombre del negocio', `<input name="nombre" value="${esc(N.nombre)}" required>`)}${campo('Tu nombre', `<input name="dueno" value="${esc(N.dueno)}">`)}
        ${campo('Correo para el resumen diario', `<input name="correo" type="email" value="${esc(N.correo)}">`)}${campo('Teléfono', `<input name="telefono" value="${esc(N.telefono)}">`)}
        <button class="btn btn--tinta">Guardar</button></form></section>
      ${cajaWhatsApp(N)}
      <section class="caja"><h4>${I.pago} Formas de pago</h4>
        <p class="tenue">Cómo te pagan tus clientes. Salen en el bot («Formas de pago») y al final de los recordatorios de cobro.</p>
        ${db.pagos().length ? `<ul class="pagos">${db.pagos().map(p => `<li><span class="pagos__ico">${I.pago}</span><span class="crece"><b>${esc(p.titulo)}</b><small>${esc(p.detalle)}</small></span><button class="icono-btn" data-quitar-pago="${esc(p.id)}" aria-label="Quitar ${esc(p.titulo)}">✕</button></li>`).join('')}</ul>`
          : '<p class="nota">Todavía no agregaste ninguna.</p>'}
        <button class="btn btn--suave" id="nuevo-pago">${I.mas} Agregar forma de pago</button></section>
      <section class="caja"><h4>${I.enlace} API e integraciones <span class="pill pill--pronto">Próximamente</span></h4>
        <p class="tenue">Usa los datos de tu negocio en otras herramientas: tu sistema contable, tu tienda en línea, hojas de cálculo o reportes propios. Tendrás una clave de acceso y avisos automáticos (webhooks) cuando entre un cliente, cambie una cotización o se registre un pago.</p></section>
      ${db.enModoReal()
        ? `<section class="caja"><h4>${I.web} Formulario de tu página web</h4>
            <p class="tenue">Las solicitudes del formulario de tu página llegan solas a Clientes y Cotizaciones. Esta es la clave de tu formulario (te la pedimos al conectarlo):</p>
            <p><code class="mono">${esc(N.clave_formulario || '')}</code></p></section>
          <section class="caja"><h4>Tu cuenta</h4><p class="tenue">Entraste como <b>${esc(db.correoUsuario())}</b>.</p></section>`
        : `<section class="caja"><h4>Datos de demostración</h4><p class="tenue">Vuelve a cargar los datos de ejemplo. Se borra lo que hayas agregado en este navegador.</p><button class="btn btn--suave" id="reiniciar">Restablecer datos de ejemplo</button></section>`}
    </div>`;
};

/** Ajustes → WhatsApp: conectado, listo para conectar, o «muy pronto» (mientras la app de Meta no esté lista). */
function cajaWhatsApp(N) {
  if (db.enModoReal() && N.whatsapp_conectado) {
    return `<section class="caja caja--conectar"><h4>${I.wa} WhatsApp <span class="pill pill--pagado">Conectado</span></h4>
      <p>Tu número <b class="mono">${esc(N.whatsapp_numero)}</b> está conectado. Los mensajes de tus clientes llegan a <a href="#/conversaciones">Conversaciones</a> y sigues usando WhatsApp en tu celular como siempre.</p>
      <p class="nota">Los recordatorios y seguimientos usan mensajes aprobados por Meta. La aprobación de cada uno tarda de minutos a unas horas.</p></section>`;
  }
  const listo = db.enModoReal() && metaListo();
  const nota = listo ? 'Se abre una ventana de Meta. Ten tu celular a mano para escanear el código.'
    : db.enModoReal() ? 'Disponible muy pronto. Estamos completando la verificación oficial con Meta.'
    : 'En la demostración no se conecta un número real. Crea tu cuenta para conectar el tuyo.';
  return `<section class="caja caja--conectar"><h4>${I.wa} WhatsApp</h4>
    <p>Conecta el número de WhatsApp Business de tu negocio. Seguirás usándolo en tu celular como siempre, y desde aquí saldrán los recordatorios, seguimientos y el resumen diario.</p>
    <ol class="pasos-conectar"><li>Tocas «Conectar mi WhatsApp».</li><li>Entras con tu Facebook en la ventana oficial de Meta.</li><li>Escaneas un código QR con tu celular.</li><li>Listo: tus chats aparecen en Conversaciones.</li></ol>
    <button class="btn btn--verde" id="conectar-wa"${listo ? '' : ' disabled'}>${I.wa} Conectar mi WhatsApp</button>
    <p class="nota" id="nota-wa" role="status">${nota}</p></section>`;
}

// ---------------------------------------------------------------- entrada
/* La bienvenida (lado derecho de entrar): una persona de negocio mirando su celular y, a su lado, los
   avisos que le llegan con Enlaza (cliente nuevo, pago recibido, recordatorio enviado). Cercano, no técnico.
   Es decorativa: aria-hidden. */
const AVISOS = [
  ['wa', 'wa', 'Nuevo cliente por WhatsApp', 'María R. quiere cotizar para el sábado', 'ahora'],
  ['check', 'verde', 'Pago recibido', '$320 · Taller Díaz pagó con Yappy', '2 min'],
  ['reloj', 'ambar', 'Recordatorio enviado', 'A Clínica Sonrisa, por su factura de mañana', '7:00 a. m.'],
];
const escena = () => `<div class="escena">
    <span class="escena__sol"></span>
    <span class="escena__sombra"></span>
    <span class="escena__persona"><img src="img/bienvenida-persona.webp" alt="" width="357" height="900"><i class="escena__brillo"></i></span>
    ${AVISOS.map(([ic, tono, t, d, h], k) => `<div class="aviso-cel" style="--k:${k}"><span class="aviso-cel__ico aviso-cel__ico--${tono}">${I[ic]}</span><div><b>${t}</b><p>${d}</p></div><time>${h}</time></div>`).join('')}
  </div>`;

const pantallaEntrada = cuerpo => `<main class="entrar">
    <div class="entrar__caja"><a class="lado__marca" href="#/">${LOGO}<span>Enlaza Studio</span></a>${cuerpo}
      <p class="entrar__seguro">${I.escudo}<span>Tus datos están protegidos: cada negocio ve solo lo suyo.</span></p></div>
    <div class="entrar__arte" aria-hidden="true">${escena()}
      <div class="entrar__lema"><b>Tu negocio, mejor <em>conectado.</em></b><span>Clientes, cotizaciones, cobros y WhatsApp en un solo lugar.</span>
        <ul><li>${I.check} Cada cliente con su seguimiento</li><li>${I.check} Cobros que se recuerdan solos</li><li>${I.check} Hecho en Panamá</li></ul></div></div></main>`;

function entrar() {
  const real = db.hayConexion();
  document.body.innerHTML = pantallaEntrada(`
      <h1>Entra a tu negocio</h1><p>Con tu correo y tu contraseña.</p>
      ${real
        ? `<form id="form-entrar">${campo('Correo', '<input name="correo" type="email" placeholder="tu@negocio.com" required autocomplete="email">')}
            <div id="caja-clave">${campo('Contraseña', '<input name="clave" type="password" autocomplete="current-password" required>')}<a href="#" id="ir-olvide" class="entrar__olvide">¿Olvidaste tu contraseña?</a></div>
            <p class="dialogo__error" role="alert" id="error-entrar">${esc(db.errorDelEnlace)}</p>
            <button class="btn btn--tinta btn--ancho" id="boton-entrar">Entrar</button>
            <button type="button" class="btn btn--suave btn--ancho" id="usar-clave">Mejor envíame un enlace al correo</button></form>
           <div class="separador"><span>o</span></div>`
        : ''}
      <button class="btn btn--suave btn--ancho" id="demo">Ver la demostración</button>
      ${real ? '<p class="entrar__registro">¿No tienes cuenta? <a href="#" id="ir-registro">Crea tu cuenta ' + I.flecha + '</a></p>' : '<p class="nota">Por ahora el portal funciona en modo demostración con datos de ejemplo.</p>'}`);
  const irOlvide = $('#ir-olvide');
  if (irOlvide) irOlvide.addEventListener('click', e => { e.preventDefault(); olvide($('[name=correo]')?.value || ''); });
  const irRegistro = $('#ir-registro');
  if (irRegistro) irRegistro.addEventListener('click', e => { e.preventDefault(); registro(); });
  document.title = 'Entrar · Enlaza Studio';
  const form = $('#form-entrar');
  let conClave = true;
  const usarClave = $('#usar-clave');
  if (usarClave) usarClave.addEventListener('click', () => {
    conClave = !conClave;
    $('#caja-clave').hidden = !conClave;
    $('[name=clave]', form).required = conClave;
    $('#boton-entrar').textContent = conClave ? 'Entrar' : 'Enviar enlace';
    usarClave.textContent = conClave ? 'Mejor envíame un enlace al correo' : 'Entrar con contraseña';
    $('.entrar__caja h1 + p').textContent = conClave ? 'Con tu correo y tu contraseña.' : 'Te enviamos un enlace a tu correo para entrar, sin contraseña.';
    if (conClave) $('[name=clave]', form).focus();
  });
  if (form) form.addEventListener('submit', async e => {
    e.preventDefault();
    const correo = String(new FormData(form).get('correo')).trim();
    const boton = $('#boton-entrar');
    if (conClave) {
      boton.disabled = true; boton.textContent = 'Entrando…';
      const r = await db.entrarConClave(correo, String(new FormData(form).get('clave')));
      if (r.error) { $('#error-entrar').textContent = r.error; boton.disabled = false; boton.textContent = 'Entrar'; return; }
      if (r.estado === 'sin-negocio') return bienvenida();
      location.hash = '#/inicio'; render(); return;
    }
    boton.disabled = true; boton.textContent = 'Enviando…';
    const error = await db.enviarEnlace(correo);
    if (error) { $('#error-entrar').textContent = error; boton.disabled = false; boton.textContent = 'Enviar enlace'; return; }
    document.body.innerHTML = pantallaEntrada(`<h1>Revisa tu correo</h1>
      <p>Te enviamos un correo a <b>${esc(correo)}</b>. Toca el botón del correo y entrarás al portal en el navegador donde se abra.</p>
      <p class="nota">¿No llegó? Revisa la carpeta de spam o espera un minuto. Puedes cerrar esta pestaña.</p>
      <button class="btn btn--suave btn--ancho" id="otra-vez">Usar otro correo</button>`);
    $('#otra-vez').addEventListener('click', entrar);
  });
  $('#demo').addEventListener('click', async () => { await db.entrarDemo(); location.hash = '#/inicio'; render(); });
}

/** «¿Olvidaste tu contraseña?»: pide el correo y manda el enlace. */
function olvide(correoInicial = '') {
  document.body.innerHTML = pantallaEntrada(`
      <h1>Recupera tu contraseña</h1><p>Te enviamos un correo con un enlace para poner una contraseña nueva.</p>
      <form id="form-olvide">${campo('Correo', `<input name="correo" type="email" required placeholder="tu@negocio.com" autocomplete="email" value="${esc(correoInicial)}">`)}
        <p class="dialogo__error" role="alert" id="error-olvide"></p>
        <button class="btn btn--tinta btn--ancho">Enviar enlace</button></form>
      <p class="nota"><a href="#" id="volver-entrar">Volver a entrar</a></p>`);
  document.title = 'Recuperar contraseña · Enlaza Studio';
  $('#volver-entrar').addEventListener('click', e => { e.preventDefault(); entrar(); });
  const form = $('#form-olvide');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const correo = String(new FormData(form).get('correo')).trim();
    const b = $('button', form); b.disabled = true; b.textContent = 'Enviando…';
    const error = await db.olvideClave(correo);
    if (error) { $('#error-olvide').textContent = error; b.disabled = false; b.textContent = 'Enviar enlace'; return; }
    document.body.innerHTML = pantallaEntrada(`<h1>Revisa tu correo</h1>
      <p>Si <b>${esc(correo)}</b> tiene cuenta, te llegó un correo con un enlace. Tócalo <b>una sola vez</b> y podrás poner tu contraseña nueva.</p>
      <p class="nota">¿No llegó? Revisa la carpeta de spam o espera un minuto.</p>
      <button class="btn btn--suave btn--ancho" id="volver">Volver a entrar</button>`);
    $('#volver').addEventListener('click', entrar);
  });
}

/** Después del enlace de «olvidé mi contraseña»: poner la nueva. */
function claveNueva() {
  document.body.innerHTML = pantallaEntrada(`
      <h1>Contraseña nueva</h1><p>Para <b>${esc(db.correoUsuario())}</b>.</p>
      <form id="form-clave">${campo('Contraseña nueva', '<input name="clave" type="password" required minlength="8" placeholder="Al menos 8 caracteres" autocomplete="new-password">')}
        <p class="dialogo__error" role="alert" id="error-clave"></p>
        <button class="btn btn--tinta btn--ancho">Guardar y entrar</button></form>`);
  document.title = 'Contraseña nueva · Enlaza Studio';
  const form = $('#form-clave');
  $('input', form).focus();
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const b = $('button', form); b.disabled = true; b.textContent = 'Guardando…';
    const r = await db.ponerClaveNueva(String(new FormData(form).get('clave')));
    if (r.error) { $('#error-clave').textContent = r.error; b.disabled = false; b.textContent = 'Guardar y entrar'; return; }
    if (r.estado === 'sin-negocio') return bienvenida();
    location.hash = '#/inicio'; render();
  });
}

/** Crear cuenta: correo, contraseña y el negocio, en un solo paso. */
function registro() {
  document.body.innerHTML = pantallaEntrada(`
      <h1>Crea tu cuenta</h1><p>Para ver tus clientes, cotizaciones y cobros en un solo lugar.</p>
      <form id="form-registro">
        ${campo('Nombre del negocio', '<input name="negocio" required maxlength="80" placeholder="Ej.: Acarreos Makena" autocomplete="organization">')}
        ${campo('Tu nombre', '<input name="dueno" maxlength="80" placeholder="Ej.: Amet" autocomplete="name">')}
        ${campo('Correo', '<input name="correo" type="email" required placeholder="tu@negocio.com" autocomplete="email">')}
        ${campo('Contraseña', '<input name="clave" type="password" required minlength="8" placeholder="Al menos 8 caracteres" autocomplete="new-password">')}
        <p class="dialogo__error" role="alert" id="error-registro"></p>
        <button class="btn btn--tinta btn--ancho">Crear cuenta</button></form>
      <p class="nota">¿Ya tienes cuenta? <a href="#" id="ir-entrar"><b>Entrar</b></a></p>`);
  document.title = 'Crear cuenta · Enlaza Studio';
  $('#ir-entrar').addEventListener('click', e => { e.preventDefault(); entrar(); });
  const form = $('#form-registro');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form));
    const boton = $('button', form); boton.disabled = true; boton.textContent = 'Creando…';
    const r = await db.crearCuenta({ correo: String(d.correo).trim(), clave: String(d.clave), negocio: String(d.negocio).trim(), dueno: String(d.dueno).trim() });
    if (r.error) { $('#error-registro').textContent = r.error; boton.disabled = false; boton.textContent = 'Crear cuenta'; return; }
    if (r.confirmar) {
      document.body.innerHTML = pantallaEntrada(`<h1>Confirma tu correo</h1>
        <p>Te enviamos un correo a <b>${esc(d.correo)}</b>. Toca el botón del correo y después entra con tu contraseña.</p>
        <button class="btn btn--suave btn--ancho" id="volver">Ir a entrar</button>`);
      $('#volver').addEventListener('click', entrar);
      return;
    }
    location.hash = '#/inicio'; render();
  });
}

/** La primera vez que entra alguien con correo: crea su negocio. */
function bienvenida() {
  document.body.innerHTML = pantallaEntrada(`
      <h1>Bienvenido</h1><p>Entraste como <b>${esc(db.correoUsuario())}</b>. Ahora crea tu negocio: es lo que verás en tu portal.</p>
      <form id="form-negocio-nuevo">${campo('Nombre del negocio', '<input name="nombre" required maxlength="80" placeholder="Ej.: Acarreos Makena" autocomplete="organization">')}
        ${campo('Tu nombre', '<input name="dueno" maxlength="80" placeholder="Ej.: Amet" autocomplete="name">')}
        <p class="dialogo__error" role="alert" id="error-negocio"></p>
        <button class="btn btn--tinta btn--ancho">Crear mi negocio</button></form>
      <button class="btn btn--suave btn--ancho" id="salir-bienvenida">Usar otro correo</button>`);
  document.title = 'Bienvenido · Enlaza Studio';
  const form = $('#form-negocio-nuevo');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form));
    const boton = $('button', form); boton.disabled = true; boton.textContent = 'Creando…';
    const error = await db.crearNegocio(String(d.nombre).trim(), String(d.dueno).trim());
    if (error) { $('#error-negocio').textContent = error; boton.disabled = false; boton.textContent = 'Crear mi negocio'; return; }
    location.hash = '#/inicio'; render();
  });
  $('#salir-bienvenida').addEventListener('click', async () => { await db.salir(); entrar(); });
}

// ---------------------------------------------------------------- render y eventos
function render() {
  const [, ruta = 'inicio', extra] = location.hash.split('/');
  const vista = V[ruta] ? ruta : 'inicio';
  document.body.innerHTML = marco(vista, V[vista](extra ? decodeURIComponent(extra) : undefined));
  document.title = `${RUTAS.find(r => r[0] === vista)?.[1] || 'Ajustes'} · Enlaza Studio`;
  enlazar(vista);
}

function enlazar(vista) {
  $('#abrir-menu').addEventListener('click', () => document.body.classList.toggle('menu-abierto'));
  $$('.lado a').forEach(a => a.addEventListener('click', () => document.body.classList.remove('menu-abierto')));
  $('#salir').addEventListener('click', async () => { await db.salir(); location.hash = ''; entrar(); });
  const demoCrear = $('#demo-crear');
  if (demoCrear) demoCrear.addEventListener('click', async () => { await db.salir(); location.hash = ''; registro(); });
  const buscar = $('#buscar');
  buscar.addEventListener('keydown', e => { if (e.key === 'Enter') location.hash = '#/clientes/' + encodeURIComponent(buscar.value.trim()); });
  if (vista === 'clientes') { const [, , f] = location.hash.split('/'); if (f) buscar.value = decodeURIComponent(f); }

  const nuevoCliente = $('#nuevo-cliente');
  if (nuevoCliente) nuevoCliente.addEventListener('click', () => dialogo('Nuevo cliente',
    campo('Nombre', '<input name="nombre" required>') + campo('Teléfono (WhatsApp)', '<input name="telefono" placeholder="+507 6000-0000" required>') +
    campo('Origen', `<select name="origen">${db.ORIGENES.map(o => `<option>${o}</option>`).join('')}</select>`) + campo('Qué necesita', '<input name="nota" placeholder="Ej.: mudanza local">'),
    d => { if (!d.nombre.trim() || digitos(d.telefono).length < 7) return 'Escribe el nombre y un teléfono válido.'; db.crearContacto(d); aviso('Cliente agregado'); render(); }));

  const sinClientes = () => { if (db.contactos().length) return false; aviso('Primero agrega un cliente'); location.hash = '#/clientes'; return true; };
  const abrirCot = sel => !sinClientes() && dialogo('Nueva cotización',
    campo('Cliente', `<select name="contacto_id">${opcionesContactos(sel)}</select>`) + campo('Servicio', '<input name="servicio" required placeholder="Ej.: mudanza de 2 recámaras">') + campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>'),
    d => { if (!d.servicio.trim() || !(+d.monto > 0)) return 'Escribe el servicio y un monto mayor a cero.'; db.crearCotizacion(d); aviso('Cotización creada'); render(); });
  const abrirCobro = sel => !sinClientes() && dialogo('Nuevo cobro',
    campo('Cliente', `<select name="contacto_id">${opcionesContactos(sel)}</select>`) + campo('Concepto', '<input name="concepto" required placeholder="Ej.: factura #0413">') +
    campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>') + campo('Vence', `<input name="vence" type="date" required value="${new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10)}">`),
    d => { if (!d.concepto.trim() || !(+d.monto > 0) || !d.vence) return 'Completa el concepto, el monto y la fecha.'; db.crearCobro(d); aviso('Cobro agregado'); render(); });
  const nuevaCot = $('#nueva-cot'); if (nuevaCot) nuevaCot.addEventListener('click', () => abrirCot());
  const nuevoCobro = $('#nuevo-cobro'); if (nuevoCobro) nuevoCobro.addEventListener('click', () => abrirCobro());
  $$('[data-cot-para]').forEach(b => b.addEventListener('click', () => abrirCot(b.dataset.cotPara)));
  $$('[data-cobro-para]').forEach(b => b.addEventListener('click', () => abrirCobro(b.dataset.cobroPara)));

  $$('[data-pagado]').forEach(b => b.addEventListener('click', () => { db.marcarPagado(b.dataset.pagado); aviso('Pago registrado'); render(); }));
  $$('[data-recordar]').forEach(a => a.addEventListener('click', () => { db.marcarRecordatorio(a.dataset.recordar); setTimeout(() => { aviso('Recordatorio registrado'); render(); }, 300); }));
  $$('[data-seguir]').forEach(a => a.addEventListener('click', () => { db.marcarSeguimiento(a.dataset.seguir); setTimeout(() => { aviso('Seguimiento registrado'); render(); }, 300); }));
  $$('[data-auto]').forEach(b => b.addEventListener('click', () => { const a = db.alternarAutomatizacion(b.dataset.auto); aviso(`${a.nombre}: ${a.activa ? 'activada' : 'pausada'}`); render(); }));

  // tablero: arrastrar y soltar (computadora) y selector «Mover a» (celular)
  $$('.tarj').forEach(t => t.addEventListener('dragstart', e => { e.dataTransfer.setData('text/plain', t.dataset.id); t.classList.add('arrastrando'); }));
  $$('.tarj').forEach(t => t.addEventListener('dragend', () => t.classList.remove('arrastrando')));
  $$('.col').forEach(col => {
    col.addEventListener('dragover', e => { e.preventDefault(); col.classList.add('encima'); });
    col.addEventListener('dragleave', () => col.classList.remove('encima'));
    col.addEventListener('drop', e => { e.preventDefault(); db.moverCotizacion(e.dataTransfer.getData('text/plain'), col.dataset.etapa); render(); });
  });
  $$('[data-mover]').forEach(s => s.addEventListener('change', () => { db.moverCotizacion(s.dataset.mover, s.value); aviso('Cotización movida'); render(); }));

  const escribir = $('#escribir');
  if (escribir) escribir.addEventListener('submit', async e => {
    e.preventDefault();
    const campoTexto = $('input', escribir), texto = campoTexto.value.trim();
    if (!texto) return;
    // Demostración, sin conectar o fuera de las 24 h: se abre WhatsApp en el celular con el mensaje escrito.
    if ($('#chat-modo').value !== 'api') { window.open(wa($('#chat-tel').value, texto), '_blank', 'noopener'); return; }
    const boton = $('button', escribir); boton.disabled = true; campoTexto.disabled = true;
    const r = await db.enviarMensaje($('#chat-id').value, texto);
    if (r.error) {
      aviso(r.error); boton.disabled = false; campoTexto.disabled = false;
      if (r.fuera24h) window.open(wa($('#chat-tel').value, texto), '_blank', 'noopener');
      return;
    }
    render();
  });
  const chat = $('.chat__cuerpo'); if (chat) chat.scrollTop = chat.scrollHeight;
  const chatId = $('#chat-id'); if (chatId && db.enModoReal()) db.leerConversacion(chatId.value);

  const conectarWa = $('#conectar-wa');
  if (conectarWa && !conectarWa.disabled) conectarWa.addEventListener('click', async () => {
    const nota = $('#nota-wa');
    conectarWa.disabled = true; nota.textContent = 'Sigue los pasos en la ventana de Meta…';
    try {
      const datos = await registroIntegrado();
      nota.textContent = 'Conectando tu número… (puede tardar unos segundos)';
      const r = await db.conectarWhatsApp(datos);
      if (r.error) throw new Error(r.error);
      aviso(`WhatsApp conectado: ${r.numero}`); render();
    } catch (e) {
      nota.textContent = e.message; conectarWa.disabled = false;
    }
  });

  // ---- bot de WhatsApp
  const formBot = $('#form-bot');
  if (formBot) {
    let paso = {};
    const vista = () => pintarCelular(leerBot(), paso);
    const ops = () => { const b = leerBot(); $('#bot-ops').innerHTML = b.opciones.map(opcionBot).join(''); $('#bot-mas').disabled = b.opciones.length >= db.BOT_MAX_OPCIONES; vista(); };
    formBot.addEventListener('input', () => { paso = {}; vista(); });
    $('#bot-mas').addEventListener('click', () => {
      const b = leerBot(); if (b.opciones.length >= db.BOT_MAX_OPCIONES) return;
      $('#bot-ops').insertAdjacentHTML('beforeend', opcionBot({ titulo: '', respuesta: '' }, b.opciones.length));
      $('#bot-mas').disabled = b.opciones.length + 1 >= db.BOT_MAX_OPCIONES;
      $$('.bot-op [name=titulo]').at(-1).focus(); vista();
    });
    $('#bot-ops').addEventListener('click', e => {
      const q = e.target.closest('[data-quitar-op]'); if (!q) return;
      q.closest('.bot-op').remove(); ops();
    });
    const limpio = b => ({ ...b, opciones: b.opciones.filter(o => o.titulo || o.respuesta) });
    formBot.addEventListener('submit', e => {
      e.preventDefault();
      const b = limpio(leerBot());
      if (!b.saludo) return aviso('Escribe el saludo del bot');
      if (b.opciones.some(o => !o.titulo || !o.respuesta)) return aviso('Cada opción necesita un nombre y una respuesta');
      db.guardarBot(b); aviso('Bot guardado'); render();
    });
    $('#bot-activo').addEventListener('click', () => {
      const b = limpio(leerBot());
      const completo = b.saludo && !b.opciones.some(o => !o.titulo || !o.respuesta);
      const guardado = db.guardarBot({ ...(completo ? b : db.bot()), activo: !db.bot().activo });
      aviso(guardado.activo ? 'Bot encendido' : 'Bot apagado'); render();
    });
    vista();
  }

  // ---- formas de pago
  const nuevoPago = $('#nuevo-pago');
  if (nuevoPago) nuevoPago.addEventListener('click', () => dialogo('Nueva forma de pago',
    campo('Tipo', `<select name="tipo">${db.TIPOS_PAGO.map(([v, t]) => `<option value="${v}">${t}</option>`).join('')}</select>`) +
    campo('Nombre', '<input name="titulo" maxlength="40" placeholder="Ej.: Yappy (si lo dejas vacío, se usa el tipo)">') +
    campo('Lo que ve el cliente', '<textarea name="detalle" rows="3" maxlength="300" required placeholder="Ej.: Busca «Mi Negocio» en el directorio de Yappy o envía al 6000-0000"></textarea>') +
    '<p class="nota">Solo datos para compartir: número de Yappy, cuenta para transferencias o un enlace de pago. Nunca tarjetas ni claves.</p>',
    d => {
      if (!d.detalle.trim()) return 'Escribe lo que verá el cliente.';
      db.agregarPago({ tipo: d.tipo, titulo: d.titulo.trim() || db.TIPOS_PAGO.find(t => t[0] === d.tipo)[1], detalle: d.detalle.trim() });
      aviso('Forma de pago agregada'); render();
    }, 'Agregar'));
  $$('[data-quitar-pago]').forEach(b => b.addEventListener('click', () => { db.quitarPago(b.dataset.quitarPago); aviso('Forma de pago quitada'); render(); }));

  const formN = $('#form-negocio');
  if (formN) formN.addEventListener('submit', e => { e.preventDefault(); db.actualizarNegocio(Object.fromEntries(new FormData(formN))); aviso('Datos guardados'); render(); });
  const rein = $('#reiniciar');
  if (rein) rein.addEventListener('click', () => { db.reiniciar(); aviso('Datos de ejemplo restablecidos'); location.hash = '#/inicio'; render(); });
}

async function arrancar() {
  // Si algo no se pudo guardar en Supabase, se avisa y se muestra lo que de verdad quedó.
  db.cuandoFalle(texto => { aviso(texto); if (db.sesion.actual()) render(); });
  // Llegó un mensaje (tiempo real): se vuelve a dibujar sin perder lo que estaba escribiendo.
  db.cuandoCambie(() => {
    if (!db.sesion.actual() || document.querySelector('dialog[open]')) return;
    const campo = $('#escribir input'), borrador = campo?.value ?? '', enfocado = document.activeElement === campo;
    render();
    const nuevo = $('#escribir input');
    if (nuevo && borrador) nuevo.value = borrador;
    if (nuevo && enfocado) nuevo.focus();
  });
  let estado = 'fuera';
  try { estado = await db.iniciar(); } catch (e) { console.error('[portal] no se pudo iniciar', e); }
  if (estado === 'fuera') return entrar();
  if (estado === 'recuperar') return claveNueva();
  if (estado === 'sin-negocio') return bienvenida();
  if (!location.hash || location.hash === '#/') location.hash = '#/inicio';
  render();
}
addEventListener('hashchange', () => { if (db.sesion.actual()) render(); });
arrancar();
