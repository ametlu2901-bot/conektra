/* Portal Enlaza Studio — interfaz (rutas, vistas y acciones) */
import { I, LOGO } from './iconos.js?v=3';
import * as db from './datos.js?v=20';
import { metaListo, registroIntegrado } from './meta.js?v=1';

const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const esc = v => String(v ?? '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
// montos con centavos solo si los tienen ($49.99, $650): igual en pantalla que en los mensajes
const dinero = n => db.dineroTexto(n);
// iniciales: solo letras y números (el nombre puede venir del perfil de WhatsApp de cualquiera)
const iniciales = n => String(n || '').split(/\s+/).filter(Boolean).slice(0, 2).map(x => x.match(/[\p{L}\p{N}]/u)?.[0] || '').join('').toUpperCase();
const digitos = tel => String(tel || '').replace(/\D/g, '');
const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;
/** Fecha local (no UTC) en formato AAAA-MM-DD, `dias` después de hoy. */
const fechaLocal = (dias = 0) => { const d = new Date(Date.now() + dias * 864e5); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
const hace = iso => {
  const s = (Date.now() - new Date(iso)) / 1000;
  if (s < 60) return 'ahora';
  if (s < 3600) return `${Math.floor(s / 60)} min`;
  if (s < 86400) return `${Math.floor(s / 3600)} h`;
  const d = Math.floor(s / 86400); return d === 1 ? 'ayer' : `${d} días`;
};
const fechaCorta = f => new Date(f.length === 10 ? f + 'T00:00' : f).toLocaleDateString('es-PA', { day: 'numeric', month: 'short' });
// los números panameños sin código de país (7 u 8 dígitos) llevan el 507 delante
const wa = (tel, texto) => `https://wa.me/${db.waNumero(tel)}?text=${encodeURIComponent(texto)}`;

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

/** Columnas de lo cobrado por mes (solo pagos registrados). */
function graficaMeses(vm) {
  const tope = Math.max(...vm.map(([, v]) => v), 1);
  return `<div class="columnas" style="grid-template-columns: repeat(${vm.length}, minmax(0, 1fr))">${vm.map(([m, v]) => `<div><i style="--h:${Math.max(v / tope * 100, v ? 4 : 0).toFixed(0)}%">${v ? `<b>${dinero(v)}</b>` : ''}</i><span>${m[0].toUpperCase() + m.slice(1)}</span></div>`).join('')}</div>`;
}
const vacioCaja = (icono, titulo, texto) => `<div class="vacio2 vacio2--caja">${icono}<b>${titulo}</b><p>${texto}</p></div>`;

V.inicio = () => {
  const R = db.resumen(), N = db.negocio();
  const act = db.actividad().slice(0, 6).map(a => `<li class="act"><span class="act__ico act__ico--${a.tipo}">${I[ICO_ACT[a.tipo]] || I.check}</span><span class="act__txt"><b>${esc(a.titulo)}</b><small>${esc(a.detalle)}</small></span><time>${hace(a.fecha)}</time></li>`).join('');
  const proximos = db.cobros().filter(cb => cb.estado !== 'pagado').slice(0, 4).map(cb => {
    const e = db.estadoCobro(cb); const x = db.contacto(cb.contacto_id);
    return `<li><span class="mini-av">${esc(iniciales(x.nombre))}</span><span class="crece"><b>${esc(x.nombre)}</b><small><span class="mono">${db.numFactura(cb.numero)}</span> · ${esc(cb.concepto)}</small></span><b>${dinero(cb.monto)}</b><span class="pill pill--${e.id}">${e.texto}</span></li>`;
  }).join('');
  const vm = db.ventasPorMes(6), hayVentas = vm.some(([, v]) => v);
  const rep = [plural(R.clientesHoy, 'cliente nuevo hoy', 'clientes nuevos hoy'), plural(R.abiertas, 'cotización abierta', 'cotizaciones abiertas'),
    `${dinero(R.cobradoMes)} cobrados este mes`, plural(R.venceSemana, 'pago vence esta semana', 'pagos vencen esta semana')].map(x => `<li>${x}</li>`).join('');
  const autoResumen = db.automatizaciones().find(a => a.id === 'resumen');
  const notaResumen = !db.enModoReal() ? 'Así llega cada mañana a las 7:00 a tu correo.'
    : !N.correo ? 'Para recibirlo cada mañana, pon tu correo en <a href="#/ajustes">Ajustes</a>.'
    : autoResumen?.activa ? `Te llega cada mañana a las 7:00 a <b>${esc(N.correo)}</b>.`
    : 'Está apagado. Actívalo en <a href="#/automatizaciones">Automatizaciones</a> para recibirlo cada mañana.';
  return `
    <div class="kpis">
      <a class="kpi" href="#/clientes"><small>Clientes nuevos (mes)</small><b>${R.clientesNuevos}</b><span>${R.clientesHoy ? `+${R.clientesHoy} hoy` : 'Ninguno hoy'}</span></a>
      <a class="kpi" href="#/cotizaciones"><small>Cotizaciones abiertas</small><b>${R.abiertas}</b><span class="${R.porSeguir ? 'ambar' : ''}">${R.porSeguir ? plural(R.porSeguir, 'sin respuesta hace 2+ días', 'sin respuesta hace 2+ días') : 'Todas al día'}</span></a>
      <a class="kpi" href="#/cobros"><small>Por cobrar</small><b>${dinero(R.porCobrar)}</b><span class="${R.vencidos.length ? 'rojo' : ''}">${R.vencidos.length ? `${plural(R.vencidos.length, 'vencido', 'vencidos')} · ` : ''}${R.venceSemana ? plural(R.venceSemana, 'vence esta semana', 'vencen esta semana') : (R.vencidos.length ? '' : 'Nada vence esta semana')}</span></a>
      <a class="kpi" href="#/reportes"><small>Cobrado (mes)</small><b>${dinero(R.cobradoMes)}</b><span>${R.ganadoMes ? `${dinero(R.ganadoMes)} en cotizaciones ganadas` : 'Pagos registrados este mes'}</span></a>
    </div>
    <div class="rejilla-inicio">
      <section class="caja"><h4><span class="vivo"></span>Actividad reciente</h4>${act ? `<ul class="act__lista">${act}</ul>` : vacioCaja(I.rayo, 'Todavía no hay movimiento', 'Aquí verás lo que pasa en tu negocio: clientes nuevos, cotizaciones, pagos y mensajes.')}</section>
      <section class="caja"><h4>Cobrado por mes ${db.enModoReal() ? '' : '<small>meses anteriores de ejemplo</small>'}<a class="ver" href="#/reportes">Reportes</a></h4>
        ${hayVentas ? graficaMeses(vm) : vacioCaja(I.grafica, 'Sin pagos registrados', 'Cuando marques un cobro como pagado, aquí verás cuánto entra cada mes.')}</section>
      <section class="caja"><h4>Próximos cobros <a class="ver" href="#/cobros">Ver todos</a></h4><ul class="lista-simple">${proximos || '<li class="vacio">No hay cobros pendientes.</li>'}</ul></section>
      <section class="caja caja--resumen"><h4>${I.chat} Resumen del día</h4>
        <div class="globo"><b>Buenos días${N.dueno ? ', ' + esc(N.dueno.split(' ')[0]) : ''}</b><ul>${rep}</ul><small>7:00 a. m.</small></div>
        <p class="nota">${notaResumen}</p></section>
    </div>`;
};

V.clientes = (filtro = '') => {
  const q = filtro.toLowerCase();
  const lista = db.contactos().filter(x => !q || (x.nombre + x.telefono + x.nota + x.origen).toLowerCase().includes(q));
  // la etapa del cliente es la de su cotización más reciente
  const etapaDe = cid => { const qs = db.cotizaciones().filter(c => c.contacto_id === cid).sort((a, b) => a.creada.localeCompare(b.creada)); return qs.length ? db.ETAPAS.find(e => e.id === qs[qs.length - 1].etapa) : null; };
  const filas = lista.map(x => { const e = etapaDe(x.id); return `<tr data-id="${x.id}"><td><span class="mini-av">${esc(iniciales(x.nombre))}</span><span><b>${esc(x.nombre)}</b><small>${esc(x.nota)}</small></span></td>
    <td class="mono">${esc(x.telefono)}</td><td>${x.origen ? `<span class="etq-origen">${esc(x.origen)}</span>` : '<span class="tenue">—</span>'}</td><td>${e ? `<span class="pill pill--etapa-${e.id}">${e.nombre}</span>` : '<span class="tenue">—</span>'}</td><td class="tenue">${fechaCorta(x.creado)}</td>
    <td class="acciones"><button class="icono-btn" data-editar-cliente="${x.id}" title="Editar cliente" aria-label="Editar ${esc(x.nombre)}">${I.lapiz}</button><a class="icono-btn" href="${wa(x.telefono, `Hola ${x.nombre.split(' ')[0]}, `)}" target="_blank" rel="noopener" title="Escribir por WhatsApp" data-escribir="${x.id}">${I.wa}</a></td></tr>`; }).join('');
  const vacio = q ? 'No hay clientes que coincidan.' : 'Todavía no tienes clientes. Agrega el primero, o espera: los que te escriban por WhatsApp o llenen el formulario de tu página llegan solos.';
  return `<div class="cab-vista"><div><h1>Clientes</h1><p>${plural(lista.length, 'cliente', 'clientes')}${q ? ` para «${esc(filtro)}»` : ''}</p></div><button class="btn btn--tinta" id="nuevo-cliente">${I.mas} Nuevo cliente</button></div>
    <div class="caja caja--tabla"><table class="tabla"><thead><tr><th>Cliente</th><th>Teléfono</th><th>Origen</th><th>Etapa</th><th>Desde</th><th></th></tr></thead><tbody>${filas || `<tr><td colspan="6" class="vacio">${vacio}</td></tr>`}</tbody></table></div>`;
};

V.cotizaciones = () => {
  const cols = db.ETAPAS.map(e => {
    const qs = db.cotizaciones().filter(q => q.etapa === e.id);
    const total = qs.reduce((s, q) => s + q.monto, 0);
    const tarjetas = qs.map(q => {
      const x = db.contacto(q.contacto_id); const dias = Math.floor((Date.now() - new Date(q.ultimo_contacto)) / 864e5);
      const atrasada = dias >= 2 && ['contactado', 'cotizado'].includes(q.etapa);
      const porEnviar = ['nuevo', 'contactado'].includes(q.etapa);
      const nombre = x.nombre.split(' ')[0];
      // sin precio (p. ej. llegó del formulario de la página) no se puede enviar: primero ponerle precio
      const boton = porEnviar && !q.monto ? `<button class="btn btn--mini btn--suave" data-editar-cot="${q.id}">${I.lapiz} Poner precio</button>`
        : porEnviar
        ? `<a class="btn btn--mini" href="${wa(x.telefono, `Hola ${nombre}, te saluda ${db.negocio().nombre}. Te comparto la cotización #${q.numero}: ${q.servicio} por ${dinero(q.monto)}. ¿Te parece bien? Si quieres, la agendamos.`)}" target="_blank" rel="noopener" data-enviar-cot="${q.id}" title="Enviar la cotización por WhatsApp: pasa sola a Cotizado">${I.wa} Enviar</a>`
        : atrasada ? `<a class="btn btn--mini" href="${wa(x.telefono, `Hola ${nombre}, te escribo de ${db.negocio().nombre} para saber si pudiste revisar la cotización #${q.numero} (${q.servicio}). ¿Te ayudo con algo?`)}" target="_blank" rel="noopener" data-seguir="${q.id}">${I.wa} Seguir</a>` : '';
      return `<article class="tarj" draggable="true" data-id="${q.id}"><header><small class="mono">#${q.numero}</small>${atrasada ? `<span class="pill pill--pronto">${dias} días sin respuesta</span>` : ''}<button class="tarj__editar" data-editar-cot="${q.id}" title="Editar servicio y precio" aria-label="Editar cotización #${q.numero}">${I.lapiz}</button></header>
        <b>${esc(x.nombre)}</b><p>${esc(q.servicio)}</p><footer><b>${dinero(q.monto)}</b>${boton}</footer>
        <select class="tarj__mover" data-mover="${q.id}" aria-label="Mover a">${db.ETAPAS.map(o => `<option value="${o.id}"${o.id === q.etapa ? ' selected' : ''}>${o.nombre}</option>`).join('')}</select></article>`;
    }).join('');
    return `<section class="col col--${e.id}" data-etapa="${e.id}"><h3>${e.nombre}<span>${qs.length}</span></h3><small class="col__total">${dinero(total)}</small><div class="col__tarjetas">${tarjetas}</div></section>`;
  }).join('');
  const reglas = [['Le escribes', 'Contactado'], ['Le envías la cotización', 'Cotizado'], ['Registras un cobro', 'Agendado'], ['Te paga', 'Ganado'], [`${db.DIAS_PARA_PERDIDO} días sin respuesta`, 'Perdido']];
  return `<div class="cab-vista"><div><h1>Cotizaciones</h1><p>Avanzan solas de etapa. Si hace falta, arrastra la tarjeta para corregirla.</p></div><button class="btn btn--tinta" id="nueva-cot">${I.mas} Nueva cotización</button></div>
    <ol class="flujo" aria-label="Cómo avanzan solas">${reglas.map(([cuando, etapa]) => `<li><span>${cuando}</span>${I.flecha}<b>${etapa}</b></li>`).join('')}</ol>
    <div class="tablero">${cols}</div>`;
};

V.cobros = () => {
  const R = db.resumen();
  const filas = db.cobros().map(cb => {
    const e = db.estadoCobro(cb); const x = db.contacto(cb.contacto_id);
    const pagos = db.textoPagos();
    const msg = `Hola ${x.nombre.split(' ')[0]}, te saluda ${db.negocio().nombre}. Te recordamos el pago de ${dinero(cb.monto)} por ${cb.concepto} (factura ${db.numFactura(cb.numero)}), ${e.id === 'vencido' ? `que venció el ${fechaCorta(cb.vence)}` : `que vence el ${fechaCorta(cb.vence)}`}. ¡Gracias!${pagos ? `\n\n${pagos}` : ''}`;
    return `<tr><td><span class="mini-av">${esc(iniciales(x.nombre))}</span><span><b>${esc(x.nombre)}</b><small><span class="mono">${db.numFactura(cb.numero)}</span> · ${esc(cb.concepto)}</small></span></td><td class="num"><b>${dinero(cb.monto)}</b></td><td class="tenue">${fechaCorta(cb.vence)}</td><td><span class="pill pill--${e.id}">${e.texto}</span></td>
      <td class="acciones">${cb.estado === 'pagado' ? '' : `<a class="btn btn--mini" href="${wa(x.telefono, msg)}" target="_blank" rel="noopener" data-recordar="${cb.id}">${I.wa} Recordar</a><button class="btn btn--mini btn--suave" data-pagado="${cb.id}">${I.check} Pagado</button><button class="icono-btn" data-anular="${cb.id}" title="Anular cobro" aria-label="Anular factura ${db.numFactura(cb.numero)}">✕</button>`}</td></tr>`;
  }).join('');
  return `<div class="cab-vista"><div><h1>Cobros</h1><p>Quién te debe, cuánto y desde cuándo. Envía el recordatorio con un toque.</p></div><button class="btn btn--tinta" id="nuevo-cobro">${I.mas} Nuevo cobro</button></div>
    <div class="kpis kpis--3"><div class="kpi"><small>Por cobrar</small><b>${dinero(R.porCobrar)}</b><span>${R.venceSemana ? plural(R.venceSemana, 'vence esta semana', 'vencen esta semana') : 'Nada vence esta semana'}</span></div>
      <div class="kpi"><small>Vencido</small><b class="${R.vencidos.length ? 'rojo' : ''}">${dinero(R.vencidos.reduce((s, cb) => s + cb.monto, 0))}</b><span>${plural(R.vencidos.length, 'cobro', 'cobros')}</span></div>
      <div class="kpi"><small>Cobrado este mes</small><b>${dinero(R.cobradoMes)}</b><span>Pagos registrados</span></div></div>
    <div class="caja caja--tabla"><table class="tabla"><thead><tr><th>Cliente</th><th class="num">Monto</th><th>Vence</th><th>Estado</th><th></th></tr></thead><tbody>${filas || '<tr><td colspan="5" class="vacio">Todavía no tienes cobros. Crea el primero: el número de factura se pone solo.</td></tr>'}</tbody></table></div>`;
};

// ---------------------------------------------------------------- conversaciones
const COLORES_AV = ['#0f6b4a', '#2a62c9', '#a0620e', '#7a3fb8', '#b4436c', '#2f7d86'];
const colorDe = t => COLORES_AV[[...String(t)].reduce((s, c) => s + c.charCodeAt(0), 0) % COLORES_AV.length];
const avatar = (nombre, clase = '') => `<span class="av${clase ? ' ' + clase : ''}" style="--av:${colorDe(nombre)}">${esc(iniciales(nombre) || '?')}</span>`;
const horaDe = iso => new Date(iso).toLocaleTimeString('es-PA', { hour: 'numeric', minute: '2-digit' });
const mismoDia = (a, b) => a.toDateString() === b.toDateString();
function diaDe(iso) {
  const d = new Date(iso), hoyD = new Date(), ayer = new Date(Date.now() - 864e5);
  if (mismoDia(d, hoyD)) return 'Hoy';
  if (mismoDia(d, ayer)) return 'Ayer';
  const t = d.toLocaleDateString('es-PA', { weekday: 'long', day: 'numeric', month: 'long' });
  return t[0].toUpperCase() + t.slice(1);
}
function cuandoCorto(iso) {
  const d = new Date(iso);
  if (mismoDia(d, new Date())) return horaDe(iso);
  if (mismoDia(d, new Date(Date.now() - 864e5))) return 'Ayer';
  return d.toLocaleDateString('es-PA', { day: 'numeric', month: 'short' });
}
const ultimoDe = c => c.mensajes[c.mensajes.length - 1];
/** «Por responder»: el último mensaje es del cliente. */
const porResponder = c => ultimoDe(c).dir === 'in';
const QUIEN = { bot: 'Bot: ', portal: 'Tú: ', celular: 'Tú: ', automatizacion: 'Auto: ' };

function filaConversacion(c, actual) {
  const x = db.contacto(c.contacto_id), u = ultimoDe(c);
  const pre = u.dir === 'out' ? (QUIEN[u.origen] || 'Tú: ') : '';
  const nuevos = c !== actual && c.no_leidos ? `<b class="conv2__nuevos">${c.no_leidos}</b>` : '';
  const buscar = `${x.nombre} ${x.telefono} ${c.mensajes.map(m => m.texto).join(' ')}`.toLowerCase();
  return `<a href="#/conversaciones/${c.id}" class="conv2${c === actual ? ' activo' : ''}${c.no_leidos && c !== actual ? ' conv2--nuevo' : ''}"
      data-buscar="${esc(buscar)}" data-sinleer="${c.no_leidos && c !== actual ? 1 : 0}" data-responder="${porResponder(c) ? 1 : 0}">
      ${avatar(x.nombre)}
      <span class="conv2__txt"><span class="conv2__fila"><b>${esc(x.nombre)}</b><time>${cuandoCorto(u.fecha)}</time></span>
        <span class="conv2__fila"><small>${pre}${esc(u.texto.split('\n')[0])}</small>${nuevos}</span></span></a>`;
}

function burbuja(m, previo) {
  const junto = previo && previo.dir === m.dir && previo.origen === m.origen && new Date(m.fecha) - new Date(previo.fecha) < 5 * 60e3;
  const quien = m.dir !== 'out' ? '' : m.origen === 'bot' ? `<span class="burb__quien">${I.bot} Bot</span>`
    : m.origen === 'celular' ? '<span class="burb__quien">Desde tu celular</span>'
    : m.origen === 'automatizacion' ? `<span class="burb__quien">${I.rayo} Automático</span>` : '';
  const estado = m.dir !== 'out' ? ''
    : m.estado === 'fallido' ? '<span class="burb__fallo" title="Meta no entregó este mensaje">No se entregó</span>'
    : `<span class="burb__visto${m.estado === 'leido' ? ' burb__visto--leido' : ''}" title="${{ enviado: 'Enviado', entregado: 'Entregado', leido: 'Leído' }[m.estado] || 'Enviado'}">${m.estado === 'entregado' || m.estado === 'leido' ? '✓✓' : '✓'}</span>`;
  const clases = ['burb', `burb--${m.dir}`, m.origen === 'bot' ? 'burb--bot' : '', m.estado === 'fallido' ? 'burb--fallo' : '', junto ? 'burb--junto' : ''].filter(Boolean).join(' ');
  return `<div class="${clases}">${junto ? '' : quien}<p>${esc(m.texto).replace(/\n/g, '<br>')}</p><small>${horaDe(m.fecha)} ${estado}</small></div>`;
}

function hiloDe(c) {
  let html = '', dia = '';
  c.mensajes.forEach((m, j) => {
    const d = diaDe(m.fecha);
    if (d !== dia) { html += `<div class="hilo__dia"><span>${d}</span></div>`; dia = d; }
    html += burbuja(m, j && diaDe(c.mensajes[j - 1].fecha) === d ? c.mensajes[j - 1] : null);
  });
  return html;
}

/** Respuestas rápidas: las respuestas del bot y las formas de pago, para no escribir lo mismo cada vez. */
function rapidas() {
  const r = db.bot().opciones.filter(o => o.titulo && o.respuesta).map(o => [o.titulo, o.respuesta]);
  const pagos = db.textoPagos(); if (pagos) r.push(['Formas de pago', pagos]);
  return r;
}

V.conversaciones = (abierta) => {
  const convs = db.conversaciones();
  const N = db.negocio();
  const real = db.enModoReal() && N.whatsapp_conectado;   // chats reales: se responde desde aquí
  const estadoWa = N.whatsapp_conectado
    ? `<span class="cab-chat__estado cab-chat__estado--ok">${I.wa}<span>WhatsApp conectado${N.whatsapp_numero ? ` · <b class="mono">${esc(N.whatsapp_numero)}</b>` : ''}</span></span>`
    : `<span class="cab-chat__estado">${I.wa}<span><b>${db.enModoReal() ? 'WhatsApp sin conectar.' : 'Chats de ejemplo.'}</b> Conecta tu número y tus chats llegan aquí; sigues usándolo en tu celular.</span><a class="btn btn--verde btn--mini" href="#/ajustes">Conectar</a></span>`;
  if (!convs.length) {
    return `<div class="cab-chat"><h1>Conversaciones</h1>${estadoWa}</div>
      <div class="bandeja2 bandeja2--vacia"><div class="vacio2">${I.chat}<b>Todavía no hay conversaciones</b>
        <p>${real ? 'Tu WhatsApp ya está conectado. Cuando un cliente te escriba, el chat aparecerá aquí al instante.' : 'Cuando conectes el WhatsApp de tu negocio, cada chat aparecerá aquí con la ficha del cliente al lado. Mientras tanto, desde Clientes, Cotizaciones y Cobros puedes escribir por WhatsApp con un toque.'}</p></div></div>`;
  }
  const actual = convs.find(c => c.id === abierta) || convs[0];
  const x = db.contacto(actual.contacto_id);
  const sinLeer = convs.filter(c => c !== actual && c.no_leidos).length;
  const responder = convs.filter(porResponder).length;
  const abierto24 = !real || db.dentroDe24h(actual);
  const quedan = real && actual.ultimo_entrante ? Math.max(0, Math.ceil(24 - (Date.now() - new Date(actual.ultimo_entrante)) / 36e5)) : 0;

  // estado del chat: ventana de 24 h de Meta y bot de este chat
  const B = db.bot();
  const pausado = actual.bot_pausado_hasta && new Date(actual.bot_pausado_hasta) > new Date();
  const chips = [];
  if (real) chips.push(abierto24 ? `<span class="chip2 chip2--ok" title="Por reglas de WhatsApp, puedes escribir libremente hasta 24 h después del último mensaje del cliente">${I.reloj} Puedes responder · quedan ${quedan} h</span>`
    : `<span class="chip2 chip2--aviso" title="Pasaron más de 24 h desde su último mensaje">${I.reloj} Ventana cerrada · responde desde tu celular</span>`);
  if (B.activo) chips.push(`<button class="chip2 chip2--btn${pausado ? ' chip2--pausa' : ''}" data-pausar-bot="${actual.id}" data-pausado="${pausado ? 1 : 0}" title="${pausado ? 'El bot no responde en este chat hasta ' + horaDe(actual.bot_pausado_hasta) : 'El bot responde en este chat. Tócalo para pausarlo 12 h y atender tú'}">${I.bot} ${pausado ? 'Bot pausado · reanudar' : 'Bot activo · pausar'}</button>`);

  const r = rapidas();
  return `<div class="cab-chat"><h1>Conversaciones</h1>${estadoWa}</div>
    <div class="bandeja2">
      <nav class="lista2" aria-label="Conversaciones">
        <div class="lista2__cab">
          <label class="lista2__buscar">${I.lupa}<input id="buscar-chat" type="search" placeholder="Buscar chat o mensaje" autocomplete="off"></label>
          <div class="lista2__tabs" role="tablist">
            <button role="tab" aria-selected="true" data-filtro="todos">Todos <span>${convs.length}</span></button>
            <button role="tab" aria-selected="false" data-filtro="sinleer">Sin leer <span>${sinLeer}</span></button>
            <button role="tab" aria-selected="false" data-filtro="responder" title="El último mensaje es del cliente">Pendientes <span>${responder}</span></button>
          </div>
        </div>
        <div class="lista2__items" id="lista-chats">${convs.map(c => filaConversacion(c, actual)).join('')}<p class="lista2__nada" hidden>No hay chats que coincidan.</p></div>
      </nav>
      <section class="chat2">
        <header class="chat2__cab">${avatar(x.nombre, 'av--md')}
          <span class="chat2__quien"><b>${esc(x.nombre)}</b><small class="mono">${esc(x.telefono)}</small></span>
          <span class="chat2__chips">${chips.join('')}</span></header>
        <div class="chat2__hilo" id="hilo">${hiloDe(actual)}</div>
        <form class="chat2__escribir" id="escribir">
          ${r.length ? `<details class="rapidas"><summary title="Respuestas rápidas">${I.rayo}<span>Rápidas</span></summary>
            <div class="rapidas__menu">${r.map(([t, txt], j) => `<button type="button" data-rapida="${j}"><b>${esc(t)}</b><small>${esc(txt.split('\n')[0])}</small></button>`).join('')}</div></details>` : ''}
          <textarea name="texto" rows="1" maxlength="4096" placeholder="${real && abierto24 ? 'Escribe un mensaje… (Enter para enviar)' : 'Escribe un mensaje… se abrirá WhatsApp'}" aria-label="Mensaje"></textarea>
          <button class="chat2__enviar" aria-label="Enviar">${I.flecha}</button>
        </form>
        <input type="hidden" id="chat-tel" value="${esc(x.telefono)}"><input type="hidden" id="chat-id" value="${esc(actual.id)}"><input type="hidden" id="chat-contacto" value="${esc(x.id)}">
        <input type="hidden" id="chat-modo" value="${real && abierto24 ? 'api' : 'celular'}">
      </section>
      ${fichaCliente(x)}</div>`;
};

/** Panel derecho de la bandeja: quién es, qué cotizaciones y cobros tiene, y acciones con un toque. */
function fichaCliente(x) {
  const qs = db.cotizaciones().filter(q => q.contacto_id === x.id && !['perdido', 'ganado'].includes(q.etapa)).sort((a, b) => b.creada.localeCompare(a.creada));
  const cbs = db.cobros().filter(cb => cb.contacto_id === x.id && cb.estado !== 'pagado');
  const pagado = db.cobros().filter(cb => cb.contacto_id === x.id && cb.estado === 'pagado').reduce((s, cb) => s + cb.monto, 0);
  const etapa = id => db.ETAPAS.find(e => e.id === id)?.nombre ?? id;
  return `<aside class="ficha2">
      <div class="ficha2__quien">${avatar(x.nombre, 'av--lg')}<b>${esc(x.nombre)}</b><small class="mono">${esc(x.telefono)}</small></div>
      <dl class="ficha2__datos">
        <div><dt>Origen</dt><dd>${esc(x.origen || '—')}</dd></div>
        <div><dt>Cliente desde</dt><dd>${x.creado ? new Date(x.creado).toLocaleDateString('es-PA', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'}</dd></div>
        <div><dt>Te ha pagado</dt><dd>${dinero(pagado)}</dd></div>
      </dl>
      ${x.nota ? `<p class="ficha2__nota">${esc(x.nota)}</p>` : ''}
      <h5>Cotizaciones abiertas <span>${qs.length}</span></h5>
      ${qs.length ? `<ul class="ficha2__lista">${qs.slice(0, 4).map(q => `<li><span class="ficha2__fila"><b class="mono">#${q.numero}</b><span class="pill pill--etapa-${q.etapa}">${etapa(q.etapa)}</span></span><span class="ficha2__fila"><span>${esc(q.servicio)}</span><b>${dinero(q.monto)}</b></span></li>`).join('')}</ul>`
        : '<p class="ficha2__vacio">Sin cotizaciones abiertas.</p>'}
      <h5>Cobros pendientes <span>${cbs.length}</span></h5>
      ${cbs.length ? `<ul class="ficha2__lista">${cbs.slice(0, 4).map(cb => { const e = db.estadoCobro(cb); return `<li><span class="ficha2__fila"><b class="mono">${db.numFactura(cb.numero)}</b><span class="pill${e.id === 'vencido' ? ' pill--vencido' : e.id === 'pronto' ? ' pill--pronto' : ''}">${e.texto}</span></span><span class="ficha2__fila"><span>${esc(cb.concepto)}</span><b>${dinero(cb.monto)}</b></span></li>`; }).join('')}</ul>`
        : '<p class="ficha2__vacio">Al día: no debe nada.</p>'}
      <div class="ficha2__acciones">
        <button class="btn btn--tinta btn--ancho" data-cot-para="${esc(x.id)}">${I.mas} Nueva cotización</button>
        <button class="btn btn--suave btn--ancho" data-cobro-para="${esc(x.id)}">${I.mas} Nuevo cobro</button>
      </div>
    </aside>`;
}

let periodoReporte = 'mes';
V.reportes = () => {
  const R = db.reporte(periodoReporte);
  const nombreP = db.PERIODOS.find(p => p[0] === periodoReporte)[1].toLowerCase();
  const vm = db.ventasPorMes(['anio', 'todo'].includes(periodoReporte) ? 12 : 6), hayVentas = vm.some(([, v]) => v);
  const topeO = Math.max(...R.origenes.map(o => o.clientes), 1);
  const totalO = R.origenes.reduce((s, o) => s + o.clientes, 0) || 1;
  const origenes = R.origenes.map(o => `<li><span class="rep-or__nombre">${esc(o.origen)}</span>
      <span class="rep-or__barra"><i style="--v:${(o.clientes / topeO).toFixed(2)}"></i></span>
      <span class="rep-or__num"><b>${o.clientes}</b> <small>${Math.round(o.clientes / totalO * 100)}%</small></span>
      <span class="rep-or__dinero">${o.cobrado ? dinero(o.cobrado) : '—'}</span></li>`).join('');
  const topeE = Math.max(...R.etapas.map(e => e.cantidad), 1);
  const etapas = R.etapas.map(e => `<li><span><span class="punto punto--${e.id}"></span>${e.nombre}</span><span class="rep-et__barra"><i style="--v:${(e.cantidad / topeE).toFixed(2)}"></i></span><b>${e.cantidad}</b><span class="tenue">${dinero(e.monto)}</span></li>`).join('');
  const mejores = R.mejores.map((m, j) => `<li><span class="rep-pos">${j + 1}</span><span class="mini-av">${esc(iniciales(m.cliente.nombre))}</span><span class="crece"><b>${esc(m.cliente.nombre)}</b><small>${esc(m.cliente.origen || '')}</small></span><b>${dinero(m.total)}</b></li>`).join('');
  return `<div class="cab-vista"><div><h1>Reportes</h1><p>Cómo va tu negocio, con lo que tú registras: cobros, cotizaciones y clientes.</p></div>
      <div class="periodos" role="tablist" aria-label="Periodo">${db.PERIODOS.map(([id, t]) => `<button role="tab" aria-selected="${id === periodoReporte}" data-periodo="${id}">${t}</button>`).join('')}</div></div>
    <div class="kpis">
      <div class="kpi"><small>Cobrado</small><b>${dinero(R.cobrado)}</b><span>${R.pagos ? plural(R.pagos, 'pago registrado', 'pagos registrados') : 'Sin pagos en ' + nombreP}</span></div>
      <div class="kpi"><small>Ventas ganadas</small><b>${dinero(R.ganado)}</b><span>${R.ganadas ? plural(R.ganadas, 'cotización ganada', 'cotizaciones ganadas') : 'Ninguna ganada en ' + nombreP}</span></div>
      <div class="kpi"><small>Tasa de cierre</small><b>${R.tasa === null ? '—' : R.tasa + '%'}</b><span>${R.tasa === null ? 'Aún no hay cotizaciones cerradas' : `${R.ganadas} ${R.ganadas === 1 ? 'ganada' : 'ganadas'} · ${R.perdidas} ${R.perdidas === 1 ? 'perdida' : 'perdidas'}`}</span></div>
      <div class="kpi"><small>Ticket promedio</small><b>${R.ticket === null ? '—' : dinero(R.ticket)}</b><span>${R.ticket === null ? 'Se calcula con ventas ganadas' : 'Por venta ganada'}</span></div>
    </div>
    <div class="rejilla-2">
      <section class="caja"><h4>Cobrado por mes ${db.enModoReal() ? '' : '<small>meses anteriores de ejemplo</small>'}</h4>
        ${hayVentas ? graficaMeses(vm) : vacioCaja(I.grafica, 'Todavía no hay pagos registrados', 'Cuando marques un cobro como pagado, aquí verás cuánto entra cada mes.')}</section>
      <section class="caja"><h4>¿De dónde vienen tus clientes? <small>${plural(R.clientesNuevos, 'cliente nuevo', 'clientes nuevos')} · ${nombreP}</small></h4>
        ${origenes ? `<ul class="rep-or"><li class="rep-or__cab"><span>Origen</span><span></span><span>Clientes</span><span>Cobrado</span></li>${origenes}</ul>
          <p class="nota">Según el origen de cada cliente. Los que te escriben por WhatsApp o llenan el formulario de tu página se marcan solos; a los demás se lo pones al agregarlos.</p>`
          : vacioCaja(I.crm, 'Sin clientes nuevos en ' + nombreP, 'Cuando agregues clientes (o te escriban por WhatsApp o tu página), aquí verás de dónde llegan y cuánto te dejan.')}</section>
      <section class="caja"><h4>Cotizaciones por etapa <small>ahora</small><a class="ver" href="#/cotizaciones">Tablero</a></h4>
        ${R.etapas.some(e => e.cantidad) ? `<ul class="rep-et">${etapas}</ul>` : vacioCaja(I.factura, 'Sin cotizaciones', 'Crea tu primera cotización y aquí verás cuántas tienes en cada etapa y por cuánto.')}</section>
      <section class="caja"><h4>Mejores clientes <small>${nombreP}</small></h4>
        ${mejores ? `<ul class="lista-simple rep-mejores">${mejores}</ul>` : vacioCaja(I.estrella, 'Todavía sin pagos', 'Aquí aparecen los clientes que más te han pagado en el periodo.')}</section>
    </div>`;
};

V.automatizaciones = () => {
  const N = db.negocio(), real = db.enModoReal();
  const items = db.automatizaciones().map(a => {
    const pronto = ['resena', 'reactivar'].includes(a.id);
    const faltaWa = real && a.canal === 'whatsapp' && !N.whatsapp_conectado;
    const faltaCorreo = real && a.canal === 'correo' && !N.correo;
    const bloqueada = pronto || faltaWa;
    const activa = a.activa && !bloqueada;
    const estado = pronto ? '<span class="pill pill--pronto">Próximamente</span>'
      : faltaWa ? `<span class="auto__falta">${I.wa} Requiere <a href="#/ajustes">conectar tu WhatsApp</a></span>`
      : faltaCorreo ? `<span class="auto__falta">Pon tu correo en <a href="#/ajustes">Ajustes</a> para recibirlo</span>`
      : a.canal === 'whatsapp' ? 'Por WhatsApp, con mensajes aprobados por Meta' : `Por correo${N.correo ? ' a ' + esc(N.correo) : ''}`;
    return `<article class="auto${activa ? ' auto--activa' : ''}${bloqueada ? ' auto--bloq' : ''}"><span class="auto__ico">${I[a.canal === 'whatsapp' ? 'wa' : 'chat']}</span>
      <div class="crece"><h3>${esc(a.nombre)}</h3><p>${esc(a.detalle)}</p><small class="auto__canal">${estado}</small></div>
      <button class="interruptor" role="switch" aria-checked="${activa}" data-auto="${a.id}" aria-label="${esc(a.nombre)}"${bloqueada ? ' disabled' : ''}><i></i></button></article>`;
  }).join('');
  return `<div class="cab-vista"><div><h1>Automatizaciones</h1><p>Lo que tu negocio hace solo, mientras tú trabajas. Se revisan cada hora y cada aviso se envía una sola vez.</p></div></div><div class="autos">${items}</div>`;
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
      <section class="caja"><h4>${I.pago} Cobros en línea <span class="pill pill--pronto">Próximamente</span></h4>
        <p class="tenue">Con TiloPay, cada factura tendrá su enlace de pago: tu cliente paga con tarjeta desde WhatsApp y el cobro se marca como pagado solo.</p></section>
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
  // En Conversaciones la pantalla no se desplaza: la bandeja llena el alto disponible.
  document.body.classList.toggle('en-chat', vista === 'conversaciones' && !!$('.bandeja2:not(.bandeja2--vacia)'));
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

  const camposCliente = (x = {}) => {
    const origenes = [...new Set([...db.ORIGENES, ...(x.origen ? [x.origen] : [])])];
    return campo('Nombre', `<input name="nombre" required value="${esc(x.nombre || '')}">`) + campo('Teléfono (WhatsApp)', `<input name="telefono" placeholder="6000-0000" required value="${esc(x.telefono || '')}">`) +
      campo('¿Cómo llegó?', `<select name="origen">${origenes.map(o => `<option${o === x.origen ? ' selected' : ''}>${esc(o)}</option>`).join('')}</select>`) + campo('Qué necesita', `<input name="nota" placeholder="Ej.: mudanza local" value="${esc(x.nota || '')}">`);
  };
  const validoCliente = d => (!d.nombre.trim() || digitos(d.telefono).length < 7) ? 'Escribe el nombre y un teléfono válido.' : null;
  const nuevoCliente = $('#nuevo-cliente');
  if (nuevoCliente) nuevoCliente.addEventListener('click', () => dialogo('Nuevo cliente', camposCliente(),
    d => { const mal = validoCliente(d); if (mal) return mal; const r = db.crearContacto({ ...d, nombre: d.nombre.trim() }); if (r.error) return r.error; aviso('Cliente agregado'); render(); }));
  $$('[data-editar-cliente]').forEach(b => b.addEventListener('click', () => {
    const x = db.contacto(b.dataset.editarCliente);
    dialogo('Editar cliente', camposCliente(x), d => { const mal = validoCliente(d); if (mal) return mal; const r = db.editarContacto(x.id, { ...d, nombre: d.nombre.trim() }); if (r.error) return r.error; aviso('Cliente actualizado'); render(); });
  }));
  $$('[data-editar-cot]').forEach(b => b.addEventListener('click', e => {
    e.stopPropagation();
    const q = db.cotizaciones().find(x => x.id === b.dataset.editarCot); if (!q) return;
    dialogo(`Cotización #${q.numero}`, campo('Servicio', `<input name="servicio" required value="${esc(q.servicio)}">`) + campo('Monto ($)', `<input name="monto" type="number" min="0" step="0.01" required value="${q.monto || ''}">`),
      d => { if (!d.servicio.trim() || !(+d.monto > 0)) return 'Escribe el servicio y un monto mayor a cero.'; db.editarCotizacion(q.id, { servicio: d.servicio.trim(), monto: +d.monto }); aviso('Cotización actualizada'); render(); });
  }));
  $$('[data-anular]').forEach(b => b.addEventListener('click', () => {
    const cb = db.cobros().find(x => x.id === b.dataset.anular); if (!cb) return;
    dialogo(`Anular factura ${db.numFactura(cb.numero)}`, `<p>Se quita de tus cobros (${esc(cb.concepto)} · ${dinero(cb.monto)}). El número ${db.numFactura(cb.numero)} no se vuelve a usar, para que tus facturas sigan en orden.</p>`,
      () => { db.anularCobro(cb.id); aviso('Cobro anulado'); render(); }, 'Anular');
  }));

  const sinClientes = () => { if (db.contactos().length) return false; aviso('Primero agrega un cliente'); location.hash = '#/clientes'; return true; };
  const abrirCot = sel => !sinClientes() && dialogo('Nueva cotización',
    campo('Cliente', `<select name="contacto_id">${opcionesContactos(sel)}</select>`) + campo('Servicio', '<input name="servicio" required placeholder="Ej.: mudanza de 2 recámaras">') + campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>'),
    d => { if (!d.servicio.trim() || !(+d.monto > 0)) return 'Escribe el servicio y un monto mayor a cero.'; db.crearCotizacion(d); aviso('Cotización creada'); render(); });
  const abrirCobro = sel => !sinClientes() && dialogo('Nuevo cobro',
    `<p class="dialogo__numero">Factura <b class="mono">${db.numFactura(db.siguienteFactura())}</b><span>El número se pone solo y sigue en orden.</span></p>` +
    campo('Cliente', `<select name="contacto_id">${opcionesContactos(sel)}</select>`) + campo('Concepto', '<input name="concepto" required placeholder="Ej.: mudanza del sábado">') +
    campo('Monto ($)', '<input name="monto" type="number" min="0" step="0.01" required>') + campo('Vence', `<input name="vence" type="date" required value="${fechaLocal(7)}">`),
    d => { if (!d.concepto.trim() || !(+d.monto > 0) || !d.vence) return 'Completa el concepto, el monto y la fecha.'; db.crearCobro(d); aviso('Cobro agregado'); render(); });
  const nuevaCot = $('#nueva-cot'); if (nuevaCot) nuevaCot.addEventListener('click', () => abrirCot());
  const nuevoCobro = $('#nuevo-cobro'); if (nuevoCobro) nuevoCobro.addEventListener('click', () => abrirCobro());
  $$('[data-cot-para]').forEach(b => b.addEventListener('click', () => abrirCot(b.dataset.cotPara)));
  $$('[data-cobro-para]').forEach(b => b.addEventListener('click', () => abrirCobro(b.dataset.cobroPara)));

  $$('[data-pagado]').forEach(b => b.addEventListener('click', () => { const movio = db.marcarPagado(b.dataset.pagado); aviso(movio ? 'Pago registrado: su cotización pasó a Ganado' : 'Pago registrado'); render(); }));
  $$('[data-periodo]').forEach(b => b.addEventListener('click', () => { periodoReporte = b.dataset.periodo; render(); }));
  $$('[data-recordar]').forEach(a => a.addEventListener('click', () => { db.marcarRecordatorio(a.dataset.recordar); setTimeout(() => { aviso('Recordatorio registrado'); render(); }, 300); }));
  $$('[data-seguir]').forEach(a => a.addEventListener('click', () => { db.marcarSeguimiento(a.dataset.seguir); setTimeout(() => { aviso('Seguimiento registrado'); render(); }, 300); }));
  $$('[data-enviar-cot]').forEach(a => a.addEventListener('click', () => { db.enviarCotizacion(a.dataset.enviarCot); setTimeout(() => { aviso('Cotización enviada: pasó a Cotizado'); render(); }, 300); }));
  $$('[data-escribir]').forEach(a => a.addEventListener('click', () => { if (db.escribioCliente(a.dataset.escribir)) setTimeout(() => { aviso('Su cotización pasó a Contactado'); render(); }, 300); }));
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

  // ---- bandeja: escribir, respuestas rápidas, buscar, filtrar y pausar el bot del chat
  const escribir = $('#escribir');
  if (escribir) {
    const campoTexto = $('textarea', escribir);
    const crecer = () => { campoTexto.style.height = 'auto'; campoTexto.style.height = Math.min(campoTexto.scrollHeight, 160) + 'px'; };
    campoTexto.addEventListener('input', crecer);
    // Enter envía; Shift + Enter hace salto de línea
    campoTexto.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); escribir.requestSubmit(); } });
    $$('[data-rapida]', escribir).forEach(b => b.addEventListener('click', () => {
      campoTexto.value = rapidas()[+b.dataset.rapida][1]; crecer(); campoTexto.focus();
      b.closest('details').open = false;
    }));
    escribir.addEventListener('submit', async e => {
      e.preventDefault();
      const texto = campoTexto.value.trim();
      if (!texto) return;
      // Demostración, sin conectar o fuera de las 24 h: se abre WhatsApp en el celular con el mensaje escrito.
      if ($('#chat-modo').value !== 'api') {
        window.open(wa($('#chat-tel').value, texto), '_blank', 'noopener');
        campoTexto.value = ''; crecer();
        if (db.escribioCliente($('#chat-contacto').value)) { aviso('Su cotización pasó a Contactado'); render(); }
        return;
      }
      const boton = $('.chat2__enviar', escribir); boton.disabled = true; campoTexto.disabled = true;
      const r = await db.enviarMensaje($('#chat-id').value, texto);
      if (r.error) {
        aviso(r.error); boton.disabled = false; campoTexto.disabled = false;
        if (r.fuera24h) window.open(wa($('#chat-tel').value, texto), '_blank', 'noopener');
        return;
      }
      // solo si de verdad salió: su cotización pasa a Contactado
      db.escribioCliente($('#chat-contacto').value);
      render();
    });
  }
  const hilo = $('#hilo'); if (hilo) hilo.scrollTop = hilo.scrollHeight;
  const chatId = $('#chat-id'); if (chatId && db.enModoReal()) db.leerConversacion(chatId.value);
  const buscarChat = $('#buscar-chat');
  if (buscarChat) {
    let filtro = 'todos';
    const aplicar = () => {
      const q = buscarChat.value.trim().toLowerCase();
      let vistos = 0;
      $$('#lista-chats .conv2').forEach(a => {
        const ok = (!q || a.dataset.buscar.includes(q)) && (filtro === 'todos' || (filtro === 'sinleer' && a.dataset.sinleer === '1') || (filtro === 'responder' && a.dataset.responder === '1'));
        a.hidden = !ok; if (ok) vistos++;
      });
      $('.lista2__nada').hidden = vistos > 0;
    };
    buscarChat.addEventListener('input', aplicar);
    $$('[data-filtro]').forEach(b => b.addEventListener('click', () => {
      filtro = b.dataset.filtro;
      $$('[data-filtro]').forEach(x => x.setAttribute('aria-selected', String(x === b)));
      aplicar();
    }));
  }
  $$('[data-pausar-bot]').forEach(b => b.addEventListener('click', () => {
    const pausar = b.dataset.pausado !== '1';
    db.pausarBot(b.dataset.pausarBot, pausar);
    aviso(pausar ? 'Bot pausado 12 h en este chat: atiendes tú' : 'El bot vuelve a responder en este chat');
    render();
  }));

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
      const completo = x => x.saludo && x.opciones.length && !x.opciones.some(o => !o.titulo || !o.respuesta);
      // no se enciende con respuestas vacías: el cliente recibiría un mensaje a medias
      if (!db.bot().activo && !completo(b)) return aviso('Completa el saludo y la respuesta de cada opción antes de encender el bot');
      const guardado = db.guardarBot({ ...(completo(b) ? b : db.bot()), activo: !db.bot().activo });
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

/** Falló la red al cargar el negocio: no es lo mismo que no tener negocio. */
function errorDeCarga() {
  document.body.innerHTML = `<main class="error-carga"><div class="vacio2">${I.escudo}<b>No se pudo cargar tu negocio</b>
    <p>Parece un problema de conexión. Tus datos están bien guardados.</p><button class="btn btn--tinta" id="reintentar">Reintentar</button></div></main>`;
  $('#reintentar').addEventListener('click', async () => {
    const r = await db.reintentar();
    if (r === 'error') return aviso('Todavía sin conexión. Inténtalo en un momento.');
    if (r === 'sin-negocio') return bienvenida();
    if (!location.hash || location.hash === '#/') location.hash = '#/inicio';
    render();
  });
}

async function arrancar() {
  // Si algo no se pudo guardar en Supabase, se avisa y se muestra lo que de verdad quedó.
  db.cuandoFalle(texto => { aviso(texto); if (db.sesion.actual()) render(); });
  // Llegó un mensaje (tiempo real): se vuelve a dibujar sin perder lo que estaba escribiendo.
  // Cuando la base pone el número definitivo de una cotización o factura, se vuelve a dibujar.
  db.cuandoNumere(() => { if (db.sesion.actual() && !document.querySelector('dialog[open]')) render(); });
  db.cuandoCambie(() => {
    if (!db.sesion.actual() || document.querySelector('dialog[open]')) return;
    // en el editor del bot y en Ajustes no se vuelve a dibujar: borraría lo que está escribiendo
    if (['bot', 'ajustes'].includes(location.hash.split('/')[1])) return;
    const campo = $('#escribir textarea'), borrador = campo?.value ?? '', enfocado = document.activeElement === campo;
    render();
    const nuevo = $('#escribir textarea');
    if (nuevo && borrador) nuevo.value = borrador;
    if (nuevo && enfocado) nuevo.focus();
  });
  let estado = 'fuera';
  try { estado = await db.iniciar(); } catch (e) { console.error('[portal] no se pudo iniciar', e); }
  if (estado === 'fuera') return entrar();
  if (estado === 'error') return errorDeCarga();
  if (estado === 'recuperar') return claveNueva();
  if (estado === 'sin-negocio') return bienvenida();
  if (!location.hash || location.hash === '#/') location.hash = '#/inicio';
  render();
}
addEventListener('hashchange', () => { if (db.sesion.actual()) render(); });
arrancar();
