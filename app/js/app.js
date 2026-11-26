/* Portal Enlaza Studio — interfaz (rutas, vistas y acciones) */
import { I, LOGO } from './iconos.js';
import * as db from './datos.js';

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
  ['conversaciones', 'Conversaciones', 'chat'], ['reportes', 'Reportes', 'grafica'], ['automatizaciones', 'Automatizaciones', 'rayo'],
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
        <div class="lado__negocio"><span class="avatar">${iniciales(N.nombre)}</span><span><b>${esc(N.nombre)}</b><small>${N.whatsapp_conectado ? 'WhatsApp conectado' : 'Modo demostración'}</small></span></div>
      </div>
    </aside>
    <div class="principal">
      <header class="barra">
        <button class="icono-btn barra__menu" id="abrir-menu" aria-label="Menú">☰</button>
        <div><small>${saludo}, ${esc(N.dueno)}</small><b>${esc(N.nombre)}</b></div>
        <span class="chip"><i></i>${(f => f[0].toUpperCase() + f.slice(1))(new Date().toLocaleDateString('es-PA', { weekday: 'long', day: 'numeric', month: 'long' }))}</span>
        <label class="buscar">${I.lupa}<input id="buscar" type="search" placeholder="Buscar clientes…" autocomplete="off"></label>
        <button class="avatar avatar--btn" id="salir" title="Cerrar sesión">${iniciales(N.dueno)}</button>
      </header>
      ${N.whatsapp_conectado ? '' : `<div class="demo-banda">${I.escudo}<span><b>Modo demostración.</b> Los datos son de ejemplo y se guardan solo en este navegador. Cuando conectemos tu cuenta, aquí verás tu negocio real.</span></div>`}
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
    const msg = `Hola ${x.nombre.split(' ')[0]}, te saluda ${db.negocio().nombre}. Te recordamos el pago de ${dinero(cb.monto)} por ${cb.concepto}, ${e.id === 'vencido' ? `que venció el ${fechaCorta(cb.vence)}` : `que vence el ${fechaCorta(cb.vence)}`}. ¡Gracias!`;
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
  const actual = convs.find(c => c.id === abierta) || convs[0];
  const lista = convs.map(c => { const x = db.contacto(c.contacto_id); const u = c.mensajes[c.mensajes.length - 1];
    return `<a href="#/conversaciones/${c.id}" class="conv${c === actual ? ' activo' : ''}"><span class="mini-av">${iniciales(x.nombre)}</span><span class="crece"><b>${esc(x.nombre)}</b><small>${u.dir === 'out' ? 'Tú: ' : ''}${esc(u.texto)}</small></span><time>${hace(u.fecha)}</time></a>`; }).join('');
  const x = db.contacto(actual.contacto_id);
  const msgs = actual.mensajes.map(m => `<div class="msg msg--${m.dir}">${esc(m.texto)}<small>${new Date(m.fecha).toLocaleTimeString('es-PA', { hour: 'numeric', minute: '2-digit' })}${m.dir === 'out' ? ' ✓✓' : ''}</small></div>`).join('');
  return `<div class="cab-vista"><div><h1>Conversaciones</h1><p>Todos los chats de WhatsApp de tu negocio en un solo lugar, conectados con tus clientes y cotizaciones.</p></div></div>
    <div class="aviso-conectar">${I.wa}<div><b>Conecta tu WhatsApp para ver tus chats reales</b><p>Estas conversaciones son de ejemplo. Al conectar tu número seguirás usando WhatsApp en tu celular y los mensajes también llegarán aquí.</p></div><a class="btn btn--verde" href="#/ajustes">Ver cómo conectar</a></div>
    <div class="bandeja"><nav class="bandeja__lista">${lista}</nav>
      <section class="chat"><header><span class="mini-av">${iniciales(x.nombre)}</span><span class="crece"><b>${esc(x.nombre)}</b><small class="mono">${esc(x.telefono)}</small></span></header>
        <div class="chat__cuerpo">${msgs}</div>
        <form class="chat__escribir" id="escribir"><input placeholder="Escribe un mensaje… (se abrirá WhatsApp)" name="texto" autocomplete="off"><button class="btn btn--verde btn--mini">${I.flecha}</button></form>
        <input type="hidden" id="chat-tel" value="${esc(x.telefono)}"></section></div>`;
};

V.reportes = () => {
  const qs = db.cotizaciones();
  const porOrigen = db.ORIGENES.map(o => [o, db.contactos().filter(x => x.origen === o).length]);
  const topeO = Math.max(...porOrigen.map(x => x[1]), 1);
  const ganadas = qs.filter(q => q.etapa === 'ganado').length, cerradas = qs.filter(q => ['ganado', 'perdido'].includes(q.etapa)).length;
  const meses = ['Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov'], valores = [2100, 2650, 2400, 3300, 3900, db.resumen().ganadoMes];
  const topeM = Math.max(...valores);
  return `<div class="cab-vista"><div><h1>Reportes</h1><p>Cómo va tu negocio, sin abrir una hoja de cálculo.</p></div></div>
    <div class="kpis"><div class="kpi"><small>Tasa de cierre</small><b>${cerradas ? Math.round(ganadas / cerradas * 100) : 0}%</b><span>${ganadas} de ${cerradas} cerradas</span></div>
      <div class="kpi"><small>Ticket promedio</small><b>${dinero(qs.reduce((s, q) => s + q.monto, 0) / Math.max(qs.length, 1))}</b><span>Por cotización</span></div>
      <div class="kpi"><small>Ganado este mes</small><b>${dinero(db.resumen().ganadoMes)}</b><span>Cotizaciones ganadas</span></div>
      <div class="kpi"><small>Por cobrar</small><b>${dinero(db.resumen().porCobrar)}</b><span>Pendiente</span></div></div>
    <div class="rejilla-2">
      <section class="caja"><h4>Ventas por mes <small>meses anteriores de ejemplo</small></h4><div class="columnas">${meses.map((m, j) => `<div><i style="--h:${(valores[j] / topeM * 100).toFixed(0)}%"><b>${dinero(valores[j])}</b></i><span>${m}</span></div>`).join('')}</div></section>
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

V.ajustes = () => {
  const N = db.negocio();
  return `<div class="cab-vista"><div><h1>Ajustes</h1><p>Datos de tu negocio y conexiones.</p></div></div>
    <div class="rejilla-2">
      <section class="caja"><h4>Tu negocio</h4><form class="form-ajustes" id="form-negocio">
        ${campo('Nombre del negocio', `<input name="nombre" value="${esc(N.nombre)}" required>`)}${campo('Tu nombre', `<input name="dueno" value="${esc(N.dueno)}">`)}
        ${campo('Correo para el resumen diario', `<input name="correo" type="email" value="${esc(N.correo)}">`)}${campo('Teléfono', `<input name="telefono" value="${esc(N.telefono)}">`)}
        <button class="btn btn--tinta">Guardar</button></form></section>
      <section class="caja caja--conectar"><h4>${I.wa} WhatsApp</h4>
        <p>Conecta el número de WhatsApp Business de tu negocio. Seguirás usándolo en tu celular como siempre, y desde aquí saldrán los recordatorios, seguimientos y el resumen diario.</p>
        <ol class="pasos-conectar"><li>Tocas «Conectar mi WhatsApp».</li><li>Entras con tu Facebook en la ventana oficial de Meta.</li><li>Escaneas un código QR con tu celular.</li><li>Listo: tus chats aparecen en Conversaciones.</li></ol>
        <button class="btn btn--verde" disabled title="Disponible cuando Enlaza Studio complete su verificación con Meta">${I.wa} Conectar mi WhatsApp</button>
        <p class="nota">Disponible muy pronto. Estamos completando la verificación oficial con Meta.</p></section>
      <section class="caja"><h4>${I.enlace} API e integraciones <span class="pill pill--pronto">Próximamente</span></h4>
        <p class="tenue">Usa los datos de tu negocio en otras herramientas: tu sistema contable, tu tienda en línea, hojas de cálculo o reportes propios. Tendrás una clave de acceso y avisos automáticos (webhooks) cuando entre un cliente, cambie una cotización o se registre un pago.</p></section>
      <section class="caja"><h4>Datos de demostración</h4><p class="tenue">Vuelve a cargar los datos de ejemplo. Se borra lo que hayas agregado en este navegador.</p><button class="btn btn--suave" id="reiniciar">Restablecer datos de ejemplo</button></section>
    </div>`;
};

// ---------------------------------------------------------------- entrada
function entrar() {
  document.body.innerHTML = `<main class="entrar">
    <div class="entrar__caja"><a class="lado__marca" href="#/">${LOGO}<span>Enlaza Studio</span></a>
      <h1>Entra a tu negocio</h1><p>Te enviaremos un enlace a tu correo para entrar, sin contraseñas.</p>
      <form id="form-entrar">${campo('Correo', '<input name="correo" type="email" placeholder="tu@negocio.com" required autocomplete="email">')}
        <button class="btn btn--tinta btn--ancho">Enviar enlace</button></form>
      <div class="separador"><span>o</span></div>
      <button class="btn btn--suave btn--ancho" id="demo">Ver la demostración</button>
      <p class="nota">Por ahora el portal funciona en modo demostración con datos de ejemplo.</p></div>
    <div class="entrar__arte" aria-hidden="true"><div><b>Tu negocio, mejor conectado.</b><span>Clientes, cotizaciones, cobros y WhatsApp en un solo lugar.</span></div></div></main>`;
  const ir = correo => { db.sesion.entrar(correo); location.hash = '#/inicio'; arrancar(); };
  $('#form-entrar').addEventListener('submit', e => { e.preventDefault(); ir(new FormData(e.target).get('correo')); });
  $('#demo').addEventListener('click', () => ir('demo@conektra'));
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
  $('#salir').addEventListener('click', () => { db.sesion.salir(); location.hash = ''; entrar(); });
  const buscar = $('#buscar');
  buscar.addEventListener('keydown', e => { if (e.key === 'Enter') location.hash = '#/clientes/' + encodeURIComponent(buscar.value.trim()); });
  if (vista === 'clientes') { const [, , f] = location.hash.split('/'); if (f) buscar.value = decodeURIComponent(f); }

  const nuevoCliente = $('#nuevo-cliente');
  if (nuevoCliente) nuevoCliente.addEventListener('click', () => dialogo('Nuevo cliente',
    campo('Nombre', '<input name="nombre" required>') + campo('Teléfono (WhatsApp)', '<input name="telefono" placeholder="+507 6000-0000" required>') +
    campo('Origen', `<select name="origen">${db.ORIGENES.map(o => `<option>${o}</option>`).join('')}</select>`) + campo('Qué necesita', '<input name="nota" placeholder="Ej.: mudanza local">'),
    d => { if (!d.nombre.trim() || digitos(d.telefono).length < 7) return 'Escribe el nombre y un teléfono válido.'; db.crearContacto(d); aviso('Cliente agregado'); render(); }));

  const nuevaCot = $('#nueva-cot');
  if (nuevaCot) nuevaCot.addEventListener('click', () => dialogo('Nueva cotización',
    campo('Cliente', `<select name="contacto_id">${opcionesContactos()}</select>`) + campo('Servicio', '<input name="servicio" required placeholder="Ej.: mudanza de 2 recámaras">') + campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>'),
    d => { if (!d.servicio.trim() || !(+d.monto > 0)) return 'Escribe el servicio y un monto mayor a cero.'; db.crearCotizacion(d); aviso('Cotización creada'); render(); }));

  const nuevoCobro = $('#nuevo-cobro');
  if (nuevoCobro) nuevoCobro.addEventListener('click', () => dialogo('Nuevo cobro',
    campo('Cliente', `<select name="contacto_id">${opcionesContactos()}</select>`) + campo('Concepto', '<input name="concepto" required placeholder="Ej.: factura #0413">') +
    campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>') + campo('Vence', `<input name="vence" type="date" required value="${new Date(Date.now() + 7 * 864e5).toISOString().slice(0, 10)}">`),
    d => { if (!d.concepto.trim() || !(+d.monto > 0) || !d.vence) return 'Completa el concepto, el monto y la fecha.'; db.crearCobro(d); aviso('Cobro agregado'); render(); }));

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
  if (escribir) escribir.addEventListener('submit', e => { e.preventDefault(); const texto = new FormData(escribir).get('texto'); if (texto) window.open(wa($('#chat-tel').value, texto), '_blank', 'noopener'); });
  const chat = $('.chat__cuerpo'); if (chat) chat.scrollTop = chat.scrollHeight;

  const formN = $('#form-negocio');
  if (formN) formN.addEventListener('submit', e => { e.preventDefault(); db.actualizarNegocio(Object.fromEntries(new FormData(formN))); aviso('Datos guardados'); render(); });
  const rein = $('#reiniciar');
  if (rein) rein.addEventListener('click', () => { db.reiniciar(); aviso('Datos de ejemplo restablecidos'); location.hash = '#/inicio'; render(); });
}

function arrancar() {
  db.cargar();
  if (!db.sesion.actual()) { entrar(); return; }
  render();
}
addEventListener('hashchange', () => { if (db.sesion.actual()) render(); });
arrancar();
