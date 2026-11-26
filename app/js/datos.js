/* Capa de datos del portal.

   Modo demostración: datos de ejemplo en el navegador (localStorage), con fechas relativas a hoy.
   Modo real: el negocio de quien entró, en Supabase (ver supabase/schema.sql y js/config.js).
*/
import { SUPABASE } from './config.js?v=4';

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

/* ------------------------------------------------------------------------------------------------
   Dos modos con la misma forma de datos (D):
   - «demo»: datos de ejemplo en el navegador (localStorage), como siempre.
   - «real»: el negocio del usuario en Supabase. Al entrar se carga todo en D; cada cambio se ve
     al instante en pantalla y se guarda en Supabase por detrás (si falla, se avisa y se recarga).
   ------------------------------------------------------------------------------------------------ */

/** Las automatizaciones que ofrece el portal (en la base solo se guarda cuál está activa). */
export const AUTOS = {
  'seguimiento': { nombre: 'Seguimiento de cotizaciones', detalle: 'Si un cliente no responde una cotización en 2 días, se le escribe para retomar la conversación.' },
  'cobro-antes': { nombre: 'Recordatorio antes del vencimiento', detalle: 'Un día antes de que venza un cobro, se envía un recordatorio amable.' },
  'cobro-despues': { nombre: 'Aviso de pago vencido', detalle: 'Si un cobro lleva 3 días vencido, se envía un segundo recordatorio.' },
  'resumen': { nombre: 'Resumen diario', detalle: 'Cada mañana a las 7:00 llega al dueño un resumen con clientes nuevos, cotizaciones y cobros.' },
  'resena': { nombre: 'Pedir reseña', detalle: 'Cuando una cotización pasa a «Ganado», al terminar el trabajo se le pide una reseña al cliente.' },
  'reactivar': { nombre: 'Reactivar clientes', detalle: 'A los clientes que no han vuelto en 6 meses se les envía un mensaje para recordarles que estás.' },
};
const ORDEN_AUTOS = Object.keys(AUTOS);

let D = null;
let modo = 'demo';        // 'demo' | 'real'
let sb = null;            // cliente de Supabase (solo en modo real)
let usuario = null;       // usuario de Supabase con sesión
let alFallar = () => {};  // la interfaz avisa cuando algo no se pudo guardar

export const enModoReal = () => modo === 'real';
export const hayConexion = () => !!(SUPABASE.url && SUPABASE.anonKey);
export const correoUsuario = () => usuario?.email ?? '';
export function cuandoFalle(fn) { alFallar = fn; }

const DEMO = 'conektra-portal-sesion';
const guardar = () => { if (modo !== 'demo') return; try { localStorage.setItem(CLAVE, JSON.stringify(D)); } catch (_) { /* sin almacenamiento: los cambios duran hasta recargar */ } };
function cargarDemo() {
  modo = 'demo';
  try { D = JSON.parse(localStorage.getItem(CLAVE)); } catch (_) { D = null; }
  if (!D) { D = semilla(); guardar(); }
  return D;
}
export function reiniciar() { if (modo === 'demo') { D = semilla(); guardar(); } return D; }

async function cliente() {
  if (sb) return sb;
  const { createClient } = await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/+esm');
  // Flujo «implicit»: el botón del correo sirve en cualquier navegador donde se abra (con PKCE solo
  // servía en el mismo donde se pidió). Vuelve con #access_token=…; supabase-js lo lee y lo borra
  // antes de que las rutas del portal miren la dirección.
  sb = createClient(SUPABASE.url, SUPABASE.anonKey, { auth: { flowType: 'implicit', detectSessionInUrl: true, persistSession: true } });
  return sb;
}

/**
 * Arranque: decide en qué estado está la persona.
 * - 'demo': entró a la demostración.  - 'real': tiene sesión y negocio (D ya cargado).
 * - 'sin-negocio': tiene sesión pero todavía no creó su negocio.  - 'fuera': hay que entrar.
 */
/** Si el enlace del correo falló (ya usado o vencido), el motivo para mostrarlo en la pantalla de entrar. */
export let errorDelEnlace = '';

export async function iniciar() {
  const datosUrl = new URLSearchParams(location.hash.slice(1) + '&' + location.search.slice(1));
  if (datosUrl.get('error_code') || datosUrl.get('error')) {
    errorDelEnlace = datosUrl.get('error_code') === 'otp_expired'
      ? 'Ese enlace ya se usó o venció (cada enlace sirve una sola vez). Pide uno nuevo aquí abajo.'
      : 'No se pudo entrar con ese enlace. Pide uno nuevo aquí abajo.';
    history.replaceState(null, '', location.pathname);
  }
  // Si vuelve del enlace del correo, manda el modo real (aunque antes haya visto la demostración).
  const vieneDelCorreo = location.hash.includes('access_token=') || location.search.includes('code=');
  // ¿Es el enlace de «olvidé mi contraseña»? (se lee antes de que supabase-js borre la dirección)
  const esRecuperar = /type=recovery/.test(location.hash + location.search);
  if (vieneDelCorreo) { try { localStorage.removeItem(DEMO); } catch (_) {} }
  // Solo la marca nueva ('1') cuenta: la versión anterior guardaba otra cosa con la misma clave.
  if (localStorage.getItem(DEMO) === '1') { cargarDemo(); return 'demo'; }
  try { localStorage.removeItem(DEMO); } catch (_) {}
  if (!hayConexion()) return 'fuera';
  const s = await cliente();
  const { data: { session } } = await s.auth.getSession();
  // Quitar los restos del enlace de la dirección después de entrar.
  if (vieneDelCorreo) history.replaceState(null, '', location.pathname);
  if (!session) return 'fuera';
  usuario = session.user;
  if (esRecuperar) return 'recuperar';
  return (await cargarReal()) ? 'real' : 'sin-negocio';
}

/** «Olvidé mi contraseña»: manda el correo con el enlace para poner una nueva. */
export async function olvideClave(correo) {
  const s = await cliente();
  const { error } = await s.auth.resetPasswordForEmail(correo, { redirectTo: location.origin + location.pathname });
  if (error) return error.status === 429 ? 'Se enviaron muchos correos seguidos. Espera unos minutos y vuelve a intentarlo.' : 'No se pudo enviar el correo. Revisa la dirección.';
  return null;
}

/** Poner la contraseña nueva (después del enlace del correo). Devuelve el estado para seguir. */
export async function ponerClaveNueva(clave) {
  const { error } = await sb.auth.updateUser({ password: clave });
  if (error) return { error: /least|short|weak/i.test(error.message || '') ? 'La contraseña debe tener al menos 8 caracteres.' : 'No se pudo cambiar la contraseña. Pide otro enlace.' };
  return { estado: (await cargarReal()) ? 'real' : 'sin-negocio' };
}

/** Entrar: en la demostración, al instante; con correo, se envía el enlace (devuelve el error si hubo). */
export async function entrarDemo() { try { localStorage.setItem(DEMO, '1'); } catch (_) {} cargarDemo(); }
export async function enviarEnlace(correo) {
  const s = await cliente();
  const { error } = await s.auth.signInWithOtp({ email: correo, options: { emailRedirectTo: location.origin + location.pathname } });
  return error ? (error.status === 429 ? 'Se enviaron muchos enlaces seguidos. Espera unos minutos y vuelve a intentarlo.' : 'No se pudo enviar el enlace. Revisa el correo e inténtalo otra vez.') : null;
}
/** Entrar con correo y contraseña (alternativa al enlace, para quien ya tiene contraseña). */
export async function entrarConClave(correo, clave) {
  const s = await cliente();
  const { data, error } = await s.auth.signInWithPassword({ email: correo, password: clave });
  if (error || !data.session) return { error: error?.status === 429 ? 'Demasiados intentos. Espera un minuto.' : 'Correo o contraseña incorrectos.' };
  try { localStorage.removeItem(DEMO); } catch (_) {}
  usuario = data.session.user;
  return { estado: (await cargarReal()) ? 'real' : 'sin-negocio' };
}
/**
 * Crear cuenta con correo y contraseña y, de una vez, su negocio. Si Supabase pide confirmar el correo,
 * devuelve { confirmar: true } (entra después de tocar el enlace del correo).
 */
export async function crearCuenta({ correo, clave, negocio: nombre, dueno }) {
  const s = await cliente();
  const { data, error } = await s.auth.signUp({ email: correo, password: clave, options: { emailRedirectTo: location.origin + location.pathname } });
  if (error) {
    const m = String(error.message || '');
    if (/already registered|already exists/i.test(m)) return { error: 'Ya hay una cuenta con ese correo. Entra con tu contraseña.' };
    if (/password/i.test(m)) return { error: 'La contraseña debe tener al menos 8 caracteres.' };
    if (error.status === 429) return { error: 'Demasiados intentos seguidos. Espera unos minutos.' };
    return { error: 'No se pudo crear la cuenta. Revisa el correo e inténtalo otra vez.' };
  }
  // Con «confirmar correo» encendido, Supabase no da sesión hasta tocar el enlace (y no avisa si el correo ya existía).
  if (!data.session) return { confirmar: true };
  try { localStorage.removeItem(DEMO); } catch (_) {}
  usuario = data.session.user;
  const e = await crearNegocio(nombre, dueno);
  return e ? { error: e } : { estado: 'real' };
}
export async function salir() {
  try { localStorage.removeItem(DEMO); } catch (_) {}
  if (sb) await sb.auth.signOut();
  usuario = null; D = null; modo = 'demo';
}

/** La primera vez: crear su negocio (y quedar como dueño). */
export async function crearNegocio(nombre, dueno) {
  const { error } = await sb.rpc('crear_negocio', { p_nombre: nombre, p_dueno: dueno });
  if (error) return error.message || 'No se pudo crear el negocio.';
  return (await cargarReal()) ? null : 'No se pudo cargar el negocio.';
}

const num = v => Number(v ?? 0);
async function cargarReal() {
  const { data: m } = await sb.from('miembros').select('negocio_id').eq('user_id', usuario.id).limit(1).maybeSingle();
  if (!m) return false;
  const n = m.negocio_id;
  const [neg, con, cot, cob, act, conv, msj, aut, wa] = await Promise.all([
    sb.from('negocios').select('id, nombre, dueno, correo, telefono, clave_formulario').eq('id', n).single(),
    sb.from('contactos').select('id, nombre, telefono, origen, nota, creado').eq('negocio_id', n),
    sb.from('cotizaciones').select('id, numero, contacto_id, servicio, monto, etapa, creada, ultimo_contacto').eq('negocio_id', n),
    sb.from('cobros').select('id, contacto_id, concepto, monto, vence, estado, pagado_el').eq('negocio_id', n).neq('estado', 'anulado'),
    sb.from('actividad').select('id, tipo, titulo, detalle, fecha').eq('negocio_id', n).order('fecha', { ascending: false }).limit(100),
    sb.from('conversaciones').select('id, contacto_id').eq('negocio_id', n),
    sb.from('mensajes').select('conversacion_id, direccion, texto, fecha').eq('negocio_id', n).order('fecha').limit(2000),
    sb.from('automatizaciones').select('clave, activa, canal').eq('negocio_id', n),
    sb.rpc('whatsapp_estado'),
  ]);
  const error = [neg, con, cot, cob, act, conv, msj, aut].find(r => r.error);
  if (error) { console.error('[portal] no se pudo cargar', error.error); return false; }
  const conectado = (wa.data ?? []).some(x => x.estado === 'activa');
  D = {
    negocio: { ...neg.data, correo: neg.data.correo ?? '', telefono: neg.data.telefono ?? '', dueno: neg.data.dueno ?? '', whatsapp_conectado: conectado },
    contactos: con.data.map(x => ({ ...x, telefono: x.telefono ?? '', nota: x.nota ?? '', origen: x.origen ?? 'WhatsApp' })),
    cotizaciones: cot.data.map(q => ({ ...q, monto: num(q.monto) })),
    cobros: cob.data.map(cb => ({ ...cb, monto: num(cb.monto) })),
    actividad: act.data.map(a => ({ ...a, detalle: a.detalle ?? '' })),
    conversaciones: conv.data
      .map(c => ({ ...c, mensajes: msj.data.filter(m => m.conversacion_id === c.id).map(m => ({ dir: m.direccion, texto: m.texto ?? '', fecha: m.fecha })) }))
      .filter(c => c.mensajes.length),
    automatizaciones: ORDEN_AUTOS.map(clave => {
      const a = aut.data.find(x => x.clave === clave);
      return { id: clave, ...AUTOS[clave], activa: a ? a.activa : false, canal: a?.canal ?? (clave === 'resumen' ? 'correo' : 'whatsapp') };
    }),
  };
  modo = 'real';
  return true;
}

/** Guarda en Supabase por detrás; si falla, avisa y vuelve a cargar lo que de verdad quedó guardado. */
function enSupabase(promesa) {
  if (modo !== 'real') return;
  Promise.resolve(promesa).then(r => { if (r?.error) throw r.error; }).catch(async e => {
    console.error('[portal] no se guardó', e);
    await cargarReal();
    alFallar('No se pudo guardar el cambio. Revisa tu conexión e inténtalo otra vez.');
  });
}
const nid = () => D.negocio.id;
const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : id());

// ---------- sesión (para saber si se muestra el portal) ----------
export const sesion = { actual: () => (modo === 'demo' ? localStorage.getItem(DEMO) === '1' && !!D : !!usuario && !!D) };

// ---------- lecturas ----------
export const negocio = () => D.negocio;
export const contactos = () => [...D.contactos].sort((a, b) => b.creado.localeCompare(a.creado));
export const contacto = cid => D.contactos.find(x => x.id === cid) || { id: cid, nombre: 'Cliente', telefono: '', nota: '', origen: '' };
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

/** Lo cobrado en los últimos 6 meses (en la demostración, los meses anteriores son de ejemplo). */
export function ventasPorMes() {
  const meses = [];
  for (let k = 5; k >= 0; k--) {
    const d = new Date(hoy().getFullYear(), hoy().getMonth() - k, 1);
    const desde = d.toISOString(), hasta = new Date(d.getFullYear(), d.getMonth() + 1, 1).toISOString();
    const total = D.cobros.filter(cb => cb.estado === 'pagado' && cb.pagado_el >= desde && cb.pagado_el < hasta).reduce((s, cb) => s + cb.monto, 0);
    meses.push([d.toLocaleDateString('es-PA', { month: 'short' }).replace('.', ''), total]);
  }
  if (modo === 'demo') [2100, 2650, 2400, 3300, 3900].forEach((v, j) => { meses[j][1] = v; });
  return meses;
}

// ---------- escrituras (en pantalla al instante; en Supabase por detrás) ----------
function registrar(tipo, titulo, detalle) {
  const a = { id: uuid(), tipo, titulo, detalle, fecha: new Date().toISOString() };
  D.actividad.push(a);
  enSupabase(sb?.from('actividad').insert({ id: a.id, negocio_id: nid(), tipo, titulo, detalle }));
}

export function crearContacto({ nombre, telefono, origen, nota }) {
  const x = { id: uuid(), nombre, telefono, origen, nota, creado: new Date().toISOString() };
  D.contactos.push(x);
  const digitos = String(telefono).replace(/\D/g, '');
  const wa_id = digitos.length === 8 ? '507' + digitos : digitos || null;
  enSupabase(sb?.from('contactos').insert({ id: x.id, negocio_id: nid(), nombre, telefono, wa_id, origen, nota }));
  registrar(origen === 'WhatsApp' ? 'whatsapp' : 'web', 'Nuevo cliente', `${nombre} · ${origen}`); guardar(); return x;
}
export function crearCotizacion({ contacto_id, servicio, monto }) {
  const q = { id: uuid(), numero: Math.max(119, ...D.cotizaciones.map(x => x.numero)) + 1, contacto_id, servicio, monto: +monto || 0, etapa: 'nuevo', creada: new Date().toISOString(), ultimo_contacto: new Date().toISOString() };
  D.cotizaciones.push(q);
  // El número lo pone la base de datos: se actualiza en pantalla cuando responde.
  if (modo === 'real') {
    sb.from('cotizaciones').insert({ id: q.id, negocio_id: nid(), contacto_id, servicio, monto: q.monto }).select('numero').single()
      .then(({ data, error }) => { if (error) throw error; q.numero = data.numero; })
      .catch(() => enSupabase(Promise.reject(new Error('cotización'))));
  }
  registrar('cotizacion', 'Nueva cotización', `${contacto(contacto_id).nombre} · ${servicio}`); guardar(); return q;
}
export function moverCotizacion(qid, etapa) {
  const q = D.cotizaciones.find(x => x.id === qid); if (!q || q.etapa === etapa) return;
  q.etapa = etapa; q.ultimo_contacto = new Date().toISOString();
  enSupabase(sb?.from('cotizaciones').update({ etapa, ultimo_contacto: q.ultimo_contacto }).eq('id', qid));
  const nombre = ETAPAS.find(e => e.id === etapa).nombre;
  registrar(etapa === 'ganado' ? 'pago' : 'cotizacion', `Cotización #${q.numero} → ${nombre}`, `${contacto(q.contacto_id).nombre} · ${q.servicio}`); guardar();
}
export function marcarSeguimiento(qid) {
  const q = D.cotizaciones.find(x => x.id === qid); q.ultimo_contacto = new Date().toISOString();
  enSupabase(sb?.from('cotizaciones').update({ ultimo_contacto: q.ultimo_contacto }).eq('id', qid));
  registrar('seguimiento', 'Seguimiento enviado', `Cotización #${q.numero} · ${contacto(q.contacto_id).nombre}`); guardar();
}
export function crearCobro({ contacto_id, concepto, monto, vence }) {
  const cb = { id: uuid(), contacto_id, concepto, monto: +monto || 0, vence, estado: 'pendiente', pagado_el: null };
  D.cobros.push(cb);
  enSupabase(sb?.from('cobros').insert({ id: cb.id, negocio_id: nid(), contacto_id, concepto, monto: cb.monto, vence }));
  registrar('cobro', 'Nuevo cobro', `${contacto(contacto_id).nombre} · $${cb.monto}`); guardar(); return cb;
}
export function marcarPagado(cid) {
  const cb = D.cobros.find(x => x.id === cid); cb.estado = 'pagado'; cb.pagado_el = new Date().toISOString();
  enSupabase(sb?.from('cobros').update({ estado: 'pagado', pagado_el: cb.pagado_el }).eq('id', cid));
  registrar('pago', 'Pago registrado', `${contacto(cb.contacto_id).nombre} · $${cb.monto}`); guardar();
}
export function marcarRecordatorio(cid) {
  const cb = D.cobros.find(x => x.id === cid);
  registrar('cobro', 'Recordatorio de pago', `${contacto(cb.contacto_id).nombre} · ${estadoCobro(cb).texto.toLowerCase()}`); guardar();
}
export function alternarAutomatizacion(aid) {
  const a = D.automatizaciones.find(x => x.id === aid); a.activa = !a.activa;
  enSupabase(sb?.from('automatizaciones').upsert({ negocio_id: nid(), clave: aid, activa: a.activa, canal: a.canal }));
  guardar(); return a;
}
export function actualizarNegocio(campos) {
  Object.assign(D.negocio, campos);
  const { nombre, dueno, correo, telefono } = D.negocio;
  enSupabase(sb?.from('negocios').update({ nombre, dueno, correo, telefono }).eq('id', nid()));
  guardar();
}
