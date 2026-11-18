/* Capa de datos del portal.

   Hoy funciona en «modo demostración»: los datos viven en el navegador (localStorage) y se generan
   con fechas relativas a hoy. Las funciones tienen la misma forma que tendrán con Supabase
   (ver supabase/schema.sql), así que al conectar la base de datos solo cambia este archivo.
*/
const CLAVE = 'conektra-portal-demo-v1';
const DIA = 864e5;
const hoy = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const hace = (dias, horas = 0) => new Date(Date.now() - dias * DIA - horas * 36e5).toISOString();
const en = dias => new Date(hoy().getTime() + dias * DIA).toISOString().slice(0, 10);
const id = () => Math.random().toString(36).slice(2, 10);

export const ETAPAS = [
  { id: 'nuevo', nombre: 'Nuevo' }, { id: 'contactado', nombre: 'Contactado' }, { id: 'cotizado', nombre: 'Cotizado' },
  { id: 'agendado', nombre: 'Agendado' }, { id: 'ganado', nombre: 'Ganado' }, { id: 'perdido', nombre: 'Perdido' },
];
export const ORIGENES = ['WhatsApp', 'Página web', 'Google', 'Instagram', 'Referido'];

function semilla() {
  const contactos = [
    ['María Rodríguez', '6123-4567', 'WhatsApp', 'Mudanza local · San Francisco'],
    ['Taller Díaz', '6234-5678', 'Página web', 'Traslado de equipo de taller'],
    ['Clínica Sonrisa', '6345-6789', 'Google', 'Mudanza de oficina'],
    ['Rosa Martínez', '6456-7890', 'Instagram', 'Mudanza de apartamento'],
    ['Luis Pérez', '6567-8901', 'WhatsApp', 'Retiro de escombros'],
    ['Ferretería El Sol', '6678-9012', 'Referido', 'Acarreo de mercancía'],
    ['Ana González', '6789-0123', 'Página web', 'Montaje de evento'],
    ['Carlos Herrera', '6890-1234', 'Google', 'Mudanza a Chiriquí'],
    ['Restaurante La Brisa', '6901-2345', 'WhatsApp', 'Traslado de mobiliario'],
    ['Daniela Ríos', '6012-3456', 'Página web', 'Mudanza local · Costa del Este'],
  ].map(([nombre, telefono, origen, nota], j) => ({ id: id(), nombre, telefono: '+507 ' + telefono, origen, nota, creado: hace(j * 2, 2) }));
  const c = n => contactos[n].id;
  const cotizaciones = [
    [0, 'Mudanza local 2 recámaras', 380, 'nuevo', 0], [4, 'Retiro de escombros', 150, 'nuevo', 1],
    [6, 'Montaje de evento', 620, 'contactado', 2], [9, 'Mudanza local', 290, 'contactado', 1],
    [1, 'Traslado de equipo', 650, 'cotizado', 3], [3, 'Mudanza de apartamento', 320, 'cotizado', 4], [7, 'Mudanza a Chiriquí', 1450, 'cotizado', 2],
    [8, 'Traslado de mobiliario', 540, 'agendado', 1],
    [2, 'Mudanza de oficina', 1180, 'ganado', 6], [5, 'Acarreo de mercancía', 230, 'ganado', 9],
    [3, 'Bodegaje temporal', 200, 'perdido', 12],
  ].map(([k, servicio, monto, etapa, dias], j) => ({ id: id(), numero: 120 + j, contacto_id: c(k), servicio, monto, etapa, creada: hace(dias + 2), ultimo_contacto: hace(dias, j) }));
  const cobros = [
    [1, 'Traslado de equipo · factura #0410', 650, en(1), 'pendiente'],
    [3, 'Mudanza de apartamento · factura #0408', 320, en(-3), 'pendiente'],
    [2, 'Mudanza de oficina · factura #0412', 1180, en(-1), 'pagado'],
    [5, 'Acarreo de mercancía · factura #0409', 230, en(6), 'pendiente'],
    [8, 'Anticipo traslado de mobiliario', 270, en(3), 'pendiente'],
    [7, 'Anticipo mudanza a Chiriquí', 500, en(-8), 'pendiente'],
  ].map(([k, concepto, monto, vence, estado]) => ({ id: id(), contacto_id: c(k), concepto, monto, vence, estado, pagado_el: estado === 'pagado' ? hace(0, 2) : null }));
  const actividad = [
    ['seguimiento', 'Seguimiento enviado', 'Cotización #124 · sin respuesta hace 2 días', hace(0, .05)],
    ['cobro', 'Recordatorio de pago', 'Taller Díaz · vence mañana', hace(0, .2)],
    ['pago', 'Pago registrado', 'Clínica Sonrisa · factura #0412', hace(0, 2)],
    ['web', 'Formulario de la página', 'Daniela Ríos pidió precio de mudanza', hace(0, 3)],
    ['whatsapp', 'Nuevo cliente desde WhatsApp', 'María Rodríguez · Mudanza local', hace(0, 5)],
    ['cotizacion', 'Cotización enviada', 'Carlos Herrera · $1,450', hace(1, 2)],
  ].map(([tipo, titulo, detalle, fecha]) => ({ id: id(), tipo, titulo, detalle, fecha }));
  const conversaciones = [
    [0, [['in', 'Hola, buenas. ¿Cuánto cuesta una mudanza de 2 recámaras en San Francisco?', 0.4], ['out', '¡Hola María! Con gusto. ¿Para qué fecha la necesitas y a qué zona va?', 0.35], ['in', 'Para el sábado 29, vamos a Condado del Rey', 0.1]]],
    [4, [['in', 'Buenas, ¿retiran escombros en Arraiján?', 26], ['out', 'Sí, claro. ¿Cuántos sacos o metros aproximadamente?', 25.5]]],
    [1, [['out', 'Hola, te comparto la cotización #124 por $650. Cualquier duda me dices.', 50], ['out', 'Hola de nuevo 👋 ¿Pudiste revisar la cotización?', 2]]],
  ].map(([k, msgs]) => ({ id: id(), contacto_id: c(k), mensajes: msgs.map(([dir, texto, h]) => ({ dir, texto, fecha: hace(0, h) })) }));
  const automatizaciones = [
    { id: 'seguimiento', nombre: 'Seguimiento de cotizaciones', detalle: 'Si un cliente no responde una cotización en 2 días, se le escribe para retomar la conversación.', activa: true, canal: 'whatsapp' },
    { id: 'cobro-antes', nombre: 'Recordatorio antes del vencimiento', detalle: 'Un día antes de que venza un cobro, se envía un recordatorio amable.', activa: true, canal: 'whatsapp' },
    { id: 'cobro-despues', nombre: 'Aviso de pago vencido', detalle: 'Si un cobro lleva 3 días vencido, se envía un segundo recordatorio.', activa: true, canal: 'whatsapp' },
    { id: 'resumen', nombre: 'Resumen diario', detalle: 'Cada mañana a las 7:00 llega al dueño un resumen con clientes nuevos, cotizaciones y cobros.', activa: true, canal: 'correo' },
    { id: 'resena', nombre: 'Pedir reseña', detalle: 'Cuando una cotización pasa a «Ganado», al terminar el trabajo se le pide una reseña al cliente.', activa: false, canal: 'whatsapp' },
    { id: 'reactivar', nombre: 'Reactivar clientes', detalle: 'A los clientes que no han vuelto en 6 meses se les envía un mensaje para recordarles que estás.', activa: false, canal: 'whatsapp' },
  ];
  return {
    negocio: { nombre: 'Acarreos Demo', dueno: 'Amet', correo: 'hola@ejemplo.com', telefono: '+507 6000-0000', whatsapp_conectado: false },
    contactos, cotizaciones, cobros, actividad, conversaciones, automatizaciones,
  };
}

let D = null;
const guardar = () => { try { localStorage.setItem(CLAVE, JSON.stringify(D)); } catch (_) { /* sin almacenamiento: los cambios duran hasta recargar */ } };
export function cargar() {
  try { D = JSON.parse(localStorage.getItem(CLAVE)); } catch (_) { D = null; }
  if (!D) { D = semilla(); guardar(); }
  return D;
}
export function reiniciar() { D = semilla(); guardar(); return D; }

// ---------- sesión (en Supabase: auth.signInWithOtp por correo) ----------
const SESION = 'conektra-portal-sesion';
export const sesion = {
  actual() { try { return JSON.parse(localStorage.getItem(SESION)); } catch (_) { return null; } },
  entrar(correo) { const s = { correo, desde: new Date().toISOString() }; try { localStorage.setItem(SESION, JSON.stringify(s)); } catch (_) {} return s; },
  salir() { try { localStorage.removeItem(SESION); } catch (_) {} },
};

// ---------- lecturas ----------
export const negocio = () => D.negocio;
export const contactos = () => [...D.contactos].sort((a, b) => b.creado.localeCompare(a.creado));
export const contacto = cid => D.contactos.find(x => x.id === cid);
export const cotizaciones = () => D.cotizaciones;
export const cobros = () => [...D.cobros].sort((a, b) => a.vence.localeCompare(b.vence));
export const actividad = () => [...D.actividad].sort((a, b) => b.fecha.localeCompare(a.fecha));
export const conversaciones = () => [...D.conversaciones].sort((a, b) => ultima(b).localeCompare(ultima(a)));
export const automatizaciones = () => D.automatizaciones;
const ultima = conv => conv.mensajes[conv.mensajes.length - 1].fecha;

export function estadoCobro(cb) {
  if (cb.estado === 'pagado') return { id: 'pagado', texto: 'Pagado' };
  const dias = Math.round((new Date(cb.vence + 'T00:00') - hoy()) / DIA);
  if (dias < 0) return { id: 'vencido', texto: `Vencido hace ${-dias} ${-dias === 1 ? 'día' : 'días'}`, dias };
  if (dias === 0) return { id: 'pronto', texto: 'Vence hoy', dias };
  if (dias <= 2) return { id: 'pronto', texto: dias === 1 ? 'Vence mañana' : `Vence en ${dias} días`, dias };
  return { id: 'ok', texto: `Vence en ${dias} días`, dias };
}

export function resumen() {
  const inicioHoy = hoy().toISOString();
  const inicioMes = new Date(hoy().getFullYear(), hoy().getMonth(), 1).toISOString();
  const abiertas = D.cotizaciones.filter(q => !['ganado', 'perdido'].includes(q.etapa));
  const porSeguir = abiertas.filter(q => Date.now() - new Date(q.ultimo_contacto) > 2 * DIA);
  const pendientes = D.cobros.filter(cb => cb.estado !== 'pagado');
  const semana = pendientes.filter(cb => { const e = estadoCobro(cb); return e.dias >= 0 && e.dias <= 7; });
  return {
    clientesNuevos: D.contactos.filter(x => x.creado >= inicioMes).length,
    clientesHoy: D.contactos.filter(x => x.creado >= inicioHoy).length,
    abiertas: abiertas.length, porSeguir: porSeguir.length,
    porCobrar: pendientes.reduce((s, cb) => s + cb.monto, 0), venceSemana: semana.length,
    vencidos: pendientes.filter(cb => estadoCobro(cb).id === 'vencido'),
    cobradoMes: D.cobros.filter(cb => cb.estado === 'pagado' && cb.pagado_el >= inicioMes).reduce((s, cb) => s + cb.monto, 0),
    ganadoMes: D.cotizaciones.filter(q => q.etapa === 'ganado').reduce((s, q) => s + q.monto, 0),
    embudo: [['Nuevos', D.cotizaciones.length], ['Cotizados', D.cotizaciones.filter(q => ['cotizado', 'agendado', 'ganado'].includes(q.etapa)).length], ['Ganados', D.cotizaciones.filter(q => q.etapa === 'ganado').length]],
  };
}

// ---------- escrituras ----------
function registrar(tipo, titulo, detalle) { D.actividad.push({ id: id(), tipo, titulo, detalle, fecha: new Date().toISOString() }); }

export function crearContacto({ nombre, telefono, origen, nota }) {
  const x = { id: id(), nombre, telefono, origen, nota, creado: new Date().toISOString() };
  D.contactos.push(x); registrar(origen === 'WhatsApp' ? 'whatsapp' : 'web', 'Nuevo cliente', `${nombre} · ${origen}`); guardar(); return x;
}
export function crearCotizacion({ contacto_id, servicio, monto }) {
  const q = { id: id(), numero: Math.max(119, ...D.cotizaciones.map(x => x.numero)) + 1, contacto_id, servicio, monto: +monto || 0, etapa: 'nuevo', creada: new Date().toISOString(), ultimo_contacto: new Date().toISOString() };
  D.cotizaciones.push(q); registrar('cotizacion', 'Nueva cotización', `${contacto(contacto_id).nombre} · ${servicio}`); guardar(); return q;
}
export function moverCotizacion(qid, etapa) {
  const q = D.cotizaciones.find(x => x.id === qid); if (!q || q.etapa === etapa) return;
  q.etapa = etapa; q.ultimo_contacto = new Date().toISOString();
  const nombre = ETAPAS.find(e => e.id === etapa).nombre;
  registrar(etapa === 'ganado' ? 'pago' : 'cotizacion', `Cotización #${q.numero} → ${nombre}`, `${contacto(q.contacto_id).nombre} · ${q.servicio}`); guardar();
}
export function marcarSeguimiento(qid) {
  const q = D.cotizaciones.find(x => x.id === qid); q.ultimo_contacto = new Date().toISOString();
  registrar('seguimiento', 'Seguimiento enviado', `Cotización #${q.numero} · ${contacto(q.contacto_id).nombre}`); guardar();
}
export function crearCobro({ contacto_id, concepto, monto, vence }) {
  const cb = { id: id(), contacto_id, concepto, monto: +monto || 0, vence, estado: 'pendiente', pagado_el: null };
  D.cobros.push(cb); registrar('cobro', 'Nuevo cobro', `${contacto(contacto_id).nombre} · $${cb.monto}`); guardar(); return cb;
}
export function marcarPagado(cid) {
  const cb = D.cobros.find(x => x.id === cid); cb.estado = 'pagado'; cb.pagado_el = new Date().toISOString();
  registrar('pago', 'Pago registrado', `${contacto(cb.contacto_id).nombre} · $${cb.monto}`); guardar();
}
export function marcarRecordatorio(cid) {
  const cb = D.cobros.find(x => x.id === cid);
  registrar('cobro', 'Recordatorio de pago', `${contacto(cb.contacto_id).nombre} · ${estadoCobro(cb).texto.toLowerCase()}`); guardar();
}
export function alternarAutomatizacion(aid) { const a = D.automatizaciones.find(x => x.id === aid); a.activa = !a.activa; guardar(); return a; }
export function actualizarNegocio(campos) { Object.assign(D.negocio, campos); guardar(); }
