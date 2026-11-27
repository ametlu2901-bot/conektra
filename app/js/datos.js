/* Capa de datos del portal.

   Modo demostración: datos de ejemplo en el navegador (localStorage), con fechas relativas a hoy.
   Modo real: el negocio de quien entró, en Supabase (ver supabase/schema.sql y js/config.js).
*/
import { SUPABASE } from './config.js?v=5';

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
export const TIPOS_PAGO = [['yappy', 'Yappy'], ['banco', 'Transferencia bancaria'], ['enlace', 'Enlace de pago'], ['efectivo', 'Efectivo'], ['otro', 'Otro']];

/* Bot de WhatsApp. Los textos fijos son los mismos del servidor (supabase/functions/_compartido/bot.ts). */
export const BOT_HUMANO = 'Listo, ya le avisamos al equipo. En un momento te escribe una persona.';
export const BOT_MAX_OPCIONES = 8;
// En un negocio nuevo, las respuestas que dependen del negocio (horario, ubicación) empiezan vacías:
// el bot no se puede encender hasta llenarlas, para no mandarle a un cliente un horario inventado.
const botInicial = () => ({
  activo: false,
  saludo: '¡Hola! Gracias por escribir a {negocio}. Elige una opción y te respondemos al momento.',
  opciones: [
    { titulo: 'Precios y cotizaciones', respuesta: 'Con gusto te cotizamos. Cuéntanos qué necesitas y para qué fecha, y te respondemos con el precio.' },
    { titulo: 'Horario de atención', respuesta: '' },
    { titulo: 'Ubicación', respuesta: '' },
  ],
  pagos_en_menu: true, humano_en_menu: true,
});
const botDemo = () => ({
  ...botInicial(), activo: true,
  opciones: [
    { titulo: 'Cotizar una mudanza', respuesta: 'Con gusto. Cuéntanos qué vas a mudar, desde dónde, hacia dónde y para qué fecha. Te respondemos con el precio en minutos.' },
    { titulo: 'Zonas que cubrimos', respuesta: 'Trabajamos en toda la ciudad de Panamá, San Miguelito, Panamá Oeste y viajes al interior.' },
    { titulo: 'Horario', respuesta: 'Atendemos de lunes a sábado, de 7:00 a. m. a 6:00 p. m.' },
  ],
});
const pagosDemo = () => [
  { id: id(), tipo: 'yappy', titulo: 'Yappy', detalle: 'Busca «Acarreos Demo» en el directorio de Yappy o envía al 6000-0000.', orden: 0 },
  { id: id(), tipo: 'banco', titulo: 'Transferencia (ACH)', detalle: 'Banco General · Cuenta de ahorros 04-00-00-000000-0 · A nombre de Acarreos Demo', orden: 1 },
];

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
  ].map(([k, servicio, monto, etapa, dias], j) => ({ id: id(), numero: 120 + j, contacto_id: c(k), servicio, monto, etapa, creada: hace(dias + 2), ultimo_contacto: hace(dias, j), ganada_el: etapa === 'ganado' ? hace(dias, j) : null }));
  const cobros = [
    [1, 'Traslado de equipo', 650, en(1), 'pendiente', 3],
    [3, 'Mudanza de apartamento', 320, en(-3), 'pendiente', 1],
    [2, 'Mudanza de oficina', 1180, en(-1), 'pagado', 5],
    [5, 'Acarreo de mercancía', 230, en(6), 'pendiente', 2],
    [8, 'Anticipo traslado de mobiliario', 270, en(3), 'pendiente', 6],
    [7, 'Anticipo mudanza a Chiriquí', 500, en(-8), 'pendiente', 4],
  ].map(([k, concepto, monto, vence, estado, numero]) => ({ id: id(), numero, contacto_id: c(k), concepto, monto, vence, estado, pagado_el: estado === 'pagado' ? hace(0, 2) : null }));
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
    [9, [['in', 'Hola, ¿cuánto cobran por una mudanza a Costa del Este?', 1.2],
      ['out', '¡Hola! Gracias por escribir a Acarreos Demo. Elige una opción y te respondemos al momento.\n1. Cotizar una mudanza\n2. Zonas que cubrimos\n3. Horario\n4. Formas de pago\n5. Hablar con alguien', 1.19, 'bot'],
      ['in', '1', 1.1],
      ['out', 'Con gusto. Cuéntanos qué vas a mudar, desde dónde, hacia dónde y para qué fecha. Te respondemos con el precio en minutos.', 1.09, 'bot'],
      ['in', 'Un apartamento de 2 recámaras, de Betania a Costa del Este, el viernes 4', 0.05]], 2],
  ].map(([k, msgs, noLeidos = 0]) => ({ id: id(), contacto_id: c(k), no_leidos: noLeidos,
    mensajes: msgs.map(([dir, texto, h, origen]) => ({ dir, texto, fecha: hace(0, h), origen: origen || (dir === 'out' ? 'portal' : 'cliente'), estado: dir === 'out' ? 'leido' : undefined })) }));
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
    bot: botDemo(), pagos: pagosDemo(),
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
  // datos guardados antes de que existieran el bot y las formas de pago
  if (!D.bot || !D.pagos) { D.bot ??= botDemo(); D.pagos ??= pagosDemo(); guardar(); }
  // datos guardados antes de que los cobros tuvieran número de factura
  if (D.cobros.some(cb => !cb.numero)) { D.cobros.forEach((cb, j) => { cb.numero ??= j + 1; }); guardar(); }
  if (D.cotizaciones.some(q => q.etapa === 'ganado' && !q.ganada_el)) { D.cotizaciones.forEach(q => { if (q.etapa === 'ganado') q.ganada_el ??= q.ultimo_contacto; }); guardar(); }
  revisarSinRespuesta();
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
  // «Mira nuestro sistema» desde la página de Enlaza: /app/#demo abre la demostración directo.
  if (location.hash === '#demo') { try { localStorage.setItem(DEMO, '1'); } catch (_) {} history.replaceState(null, '', location.pathname + '#/inicio'); }
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
  const r = await cargarReal();
  if (r === 'error') return 'error';
  if (r) return 'real';
  // Si al crear la cuenta dejó el nombre del negocio (y tuvo que confirmar el correo), se crea solo.
  const meta = usuario.user_metadata || {};
  if (meta.negocio) return (await crearNegocio(meta.negocio, meta.dueno || '')) ? 'sin-negocio' : 'real';
  return 'sin-negocio';
}
/** Reintentar la carga (cuando la red falló al entrar). */
export async function reintentar() { const r = await cargarReal(); return r === 'error' ? 'error' : r ? 'real' : 'sin-negocio'; }

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
  { const r = await cargarReal(); if (r === 'error') return { error: 'No se pudo cargar tu negocio. Revisa tu conexión e inténtalo otra vez.' }; return { estado: r ? 'real' : 'sin-negocio' }; }
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
  { const r = await cargarReal(); if (r === 'error') return { error: 'No se pudo cargar tu negocio. Revisa tu conexión e inténtalo otra vez.' }; return { estado: r ? 'real' : 'sin-negocio' }; }
}
/**
 * Crear cuenta con correo y contraseña y, de una vez, su negocio. Si Supabase pide confirmar el correo,
 * devuelve { confirmar: true } (entra después de tocar el enlace del correo).
 */
export async function crearCuenta({ correo, clave, negocio: nombre, dueno }) {
  const s = await cliente();
  const { data, error } = await s.auth.signUp({ email: correo, password: clave, options: { emailRedirectTo: location.origin + location.pathname, data: { negocio: nombre, dueno } } });
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
  if (canal) { await sb.removeChannel(canal); canal = null; }
  if (sb) await sb.auth.signOut();
  usuario = null; D = null; modo = 'demo';
}

/** La primera vez: crear su negocio (y quedar como dueño). */
export async function crearNegocio(nombre, dueno) {
  const { error } = await sb.rpc('crear_negocio', { p_nombre: nombre, p_dueno: dueno });
  if (error) return error.message || 'No se pudo crear el negocio.';
  return (await cargarReal()) === true ? null : 'No se pudo cargar el negocio.';
}

const num = v => Number(v ?? 0);
/** Carga el negocio. Devuelve true, false (no tiene negocio) o 'error' (falló la red: no es lo mismo que no tener negocio). */
async function cargarReal() {
  const { data: m, error: errM } = await sb.from('miembros').select('negocio_id').eq('user_id', usuario.id).limit(1).maybeSingle();
  if (errM) { console.error('[portal] no se pudo cargar', errM); return 'error'; }
  if (!m) return false;
  const n = m.negocio_id;
  const [neg, con, cot, cob, act, conv, msj, aut, wa, bot, pagos] = await Promise.all([
    sb.from('negocios').select('id, nombre, dueno, correo, telefono, clave_formulario, ultima_cotizacion, ultimo_cobro').eq('id', n).single(),
    sb.from('contactos').select('id, nombre, telefono, origen, nota, creado').eq('negocio_id', n),
    sb.from('cotizaciones').select('id, numero, contacto_id, servicio, monto, etapa, creada, ultimo_contacto, ganada_el').eq('negocio_id', n).order('creada'),
    sb.from('cobros').select('id, numero, contacto_id, concepto, monto, vence, estado, pagado_el').eq('negocio_id', n).neq('estado', 'anulado'),
    sb.from('actividad').select('id, tipo, titulo, detalle, fecha').eq('negocio_id', n).order('fecha', { ascending: false }).limit(100),
    sb.from('conversaciones').select('id, contacto_id, ultimo_entrante, no_leidos, bot_pausado_hasta').eq('negocio_id', n),
    // los 2000 mensajes MÁS NUEVOS (se piden al revés y se dan vuelta)
    sb.from('mensajes').select('conversacion_id, direccion, origen, tipo, texto, estado, fecha').eq('negocio_id', n).order('fecha', { ascending: false }).limit(2000),
    sb.from('automatizaciones').select('clave, activa, canal').eq('negocio_id', n),
    sb.rpc('whatsapp_estado'),
    // bot y formas de pago: si la base todavía no tiene esas tablas, el portal sigue funcionando sin ellos
    sb.from('bots').select('activo, saludo, opciones, pagos_en_menu, humano_en_menu').eq('negocio_id', n).maybeSingle(),
    sb.from('metodos_pago').select('id, tipo, titulo, detalle, orden').eq('negocio_id', n).order('orden'),
  ]);
  const error = [neg, con, cot, cob, act, conv, msj, aut].find(r => r.error);
  if (error) { console.error('[portal] no se pudo cargar', error.error); return 'error'; }
  msj.data.reverse();
  const conexion = (wa.data ?? []).find(x => x.estado === 'activa');
  D = {
    negocio: { ...neg.data, correo: neg.data.correo ?? '', telefono: neg.data.telefono ?? '', dueno: neg.data.dueno ?? '',
      whatsapp_conectado: !!conexion, whatsapp_numero: conexion?.numero_visible ?? '' },
    contactos: con.data.map(x => ({ ...x, telefono: x.telefono ?? '', nota: x.nota ?? '', origen: x.origen ?? 'WhatsApp' })),
    cotizaciones: cot.data.map(q => ({ ...q, monto: num(q.monto), ganada_el: q.ganada_el ?? (q.etapa === 'ganado' ? q.ultimo_contacto : null) })),
    cobros: cob.data.map(cb => ({ ...cb, monto: num(cb.monto) })),
    actividad: act.data.map(a => ({ ...a, detalle: a.detalle ?? '' })),
    conversaciones: conv.data
      .map(c => ({ ...c, no_leidos: c.no_leidos ?? 0,
        mensajes: msj.data.filter(m => m.conversacion_id === c.id).map(m => ({ dir: m.direccion, origen: m.origen, tipo: m.tipo, estado: m.estado, texto: m.texto ?? '', fecha: m.fecha })) }))
      .filter(c => c.mensajes.length),
    bot: bot.data ? { ...botInicial(), ...bot.data, opciones: Array.isArray(bot.data.opciones) ? bot.data.opciones : [] } : botInicial(),
    pagos: pagos.error ? [] : pagos.data,
    automatizaciones: ORDEN_AUTOS.map(clave => {
      const a = aut.data.find(x => x.clave === clave);
      return { id: clave, ...AUTOS[clave], activa: a ? a.activa : false, canal: a?.canal ?? (clave === 'resumen' ? 'correo' : 'whatsapp') };
    }),
  };
  modo = 'real';
  // (la regla de «15 días sin respuesta → Perdido» la aplica el servidor cada hora; aquí solo en la demostración)
  escucharCambios();
  return true;
}

// ---------- tiempo real: cuando entra un mensaje (o algo nuevo en la actividad) se recarga solo ----------
let canal = null, alCambiar = () => {}, recarga = 0;
export function cuandoCambie(fn) { alCambiar = fn; }
function escucharCambios() {
  if (canal || modo !== 'real') return;
  const filtro = { schema: 'public', filter: `negocio_id=eq.${nid()}` };
  const recargar = () => { clearTimeout(recarga); recarga = setTimeout(async () => { if (modo === 'real' && (await cargarReal()) === true) alCambiar(); }, 400); };
  canal = sb.channel('negocio-' + nid())
    .on('postgres_changes', { event: '*', table: 'mensajes', ...filtro }, recargar)
    .on('postgres_changes', { event: 'INSERT', table: 'actividad', ...filtro }, recargar)
    .subscribe();
}

// ---------- WhatsApp (funciones del servidor: el token de Meta nunca llega al navegador) ----------
async function llamar(funcion, cuerpo) {
  const { data, error } = await sb.functions.invoke(funcion, { body: cuerpo });
  if (!error) return data ?? {};
  try { return await error.context.json(); } catch (_) { return { error: 'No se pudo hablar con el servidor. Revisa tu conexión.' }; }
}

/** Después de la ventana de Meta: el servidor guarda la conexión, suscribe el webhook y crea las plantillas. */
export async function conectarWhatsApp({ code, waba_id, phone_number_id, coexistencia }) {
  const r = await llamar('whatsapp-conectar', { negocio_id: nid(), code, waba_id, phone_number_id, coexistencia });
  if (!r.ok) return { error: 'No se pudo conectar tu número. Inténtalo otra vez en un momento.' };
  await cargarReal();
  return { numero: r.numero };
}

/** Ventana de 24 h de Meta: dentro de ella se responde con texto libre; fuera, solo con plantilla aprobada. */
export const dentroDe24h = conv => !!conv.ultimo_entrante && Date.now() - new Date(conv.ultimo_entrante) < 24 * 36e5;

/** Responder desde la bandeja (sale por el WhatsApp del negocio). */
export async function enviarMensaje(conversacion_id, texto) {
  const r = await llamar('whatsapp-enviar', { conversacion_id, texto });
  if (r.requiere_plantilla) return { error: 'Pasaron más de 24 horas desde su último mensaje. Por reglas de WhatsApp, escríbele desde tu celular.', fuera24h: true };
  if (!r.ok) return { error: 'No se pudo enviar el mensaje. Inténtalo otra vez.' };
  const conv = D.conversaciones.find(c => c.id === conversacion_id);
  if (conv) conv.mensajes.push({ dir: 'out', origen: 'portal', estado: 'enviado', texto, fecha: new Date().toISOString() });
  return { ok: true };
}

/** Pausar (12 h) o reanudar el bot en un chat: para atender tú sin que el bot se meta. */
export function pausarBot(cid, pausar) {
  const conv = D.conversaciones.find(c => c.id === cid); if (!conv) return;
  conv.bot_pausado_hasta = pausar ? new Date(Date.now() + 12 * 36e5).toISOString() : null;
  enSupabase(sb?.from('conversaciones').update({ bot_pausado_hasta: conv.bot_pausado_hasta }).eq('id', cid));
  guardar();
}

/** Al abrir un chat: ya no está «sin leer». */
export function leerConversacion(cid) {
  const conv = D.conversaciones.find(c => c.id === cid);
  if (!conv || !conv.no_leidos) return;
  conv.no_leidos = 0;
  enSupabase(sb.from('conversaciones').update({ no_leidos: 0 }).eq('id', cid));
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
/** Teléfono para WhatsApp: solo dígitos; los números panameños de 7 u 8 dígitos llevan el 507 delante. */
export function waNumero(tel) {
  const d = String(tel ?? '').replace(/\D/g, '');
  return d.length === 7 || d.length === 8 ? '507' + d : d;
}
/** ¿Ya hay un cliente con ese teléfono? (para no duplicarlo) */
export const clientePorTelefono = (tel, menos) => { const w = waNumero(tel); return w ? D.contactos.find(x => x.id !== menos && waNumero(x.telefono) === w) : null; };
export const cotizaciones = () => D.cotizaciones;
export const cobros = () => [...D.cobros].sort((a, b) => a.vence.localeCompare(b.vence));
export const actividad = () => [...D.actividad].sort((a, b) => b.fecha.localeCompare(a.fecha));
export const conversaciones = () => [...D.conversaciones].sort((a, b) => ultima(b).localeCompare(ultima(a)));
export const automatizaciones = () => D.automatizaciones;
export const bot = () => D.bot;
export const pagos = () => D.pagos;
/** Las formas de pago en un texto para WhatsApp (bot y recordatorios de cobro). Vacío si no hay. */
export const textoPagos = () => D.pagos.length ? 'Formas de pago:\n' + D.pagos.map(p => `• ${p.titulo}: ${p.detalle}`).join('\n') : '';
/** Las filas del menú del bot, en el mismo orden que las ve el cliente (igual que en el servidor). */
export function filasBot(b = D.bot) {
  const filas = b.opciones.filter(o => o.titulo && o.respuesta).slice(0, BOT_MAX_OPCIONES).map((o, i) => ({ id: `op-${i}`, titulo: o.titulo.slice(0, 24), respuesta: o.respuesta }));
  if (b.pagos_en_menu && D.pagos.length) filas.push({ id: 'pagos', titulo: 'Formas de pago', respuesta: textoPagos() });
  if (b.humano_en_menu) filas.push({ id: 'humano', titulo: 'Hablar con alguien', respuesta: BOT_HUMANO });
  return filas;
}
export const saludoBot = (b = D.bot) => (b.saludo || '¡Hola! ¿En qué te ayudamos?').replaceAll('{negocio}', D.negocio.nombre);
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
  // «por seguir» = lo mismo que el tablero marca como «X días sin respuesta»
  const porSeguir = abiertas.filter(q => ['contactado', 'cotizado'].includes(q.etapa) && Date.now() - new Date(q.ultimo_contacto) >= 2 * DIA);
  const pendientes = D.cobros.filter(cb => cb.estado !== 'pagado');
  const semana = pendientes.filter(cb => { const e = estadoCobro(cb); return e.dias >= 0 && e.dias <= 7; });
  return {
    clientesNuevos: D.contactos.filter(x => x.creado >= inicioMes).length,
    clientesHoy: D.contactos.filter(x => x.creado >= inicioHoy).length,
    abiertas: abiertas.length, porSeguir: porSeguir.length,
    porCobrar: pendientes.reduce((s, cb) => s + cb.monto, 0), venceSemana: semana.length,
    vencidos: pendientes.filter(cb => estadoCobro(cb).id === 'vencido'),
    cobradoMes: D.cobros.filter(cb => cb.estado === 'pagado' && cb.pagado_el >= inicioMes).reduce((s, cb) => s + cb.monto, 0),
    ganadoMes: D.cotizaciones.filter(q => q.etapa === 'ganado' && (q.ganada_el || '') >= inicioMes).reduce((s, q) => s + q.monto, 0),
    nuevasMes: D.cotizaciones.filter(q => q.creada >= inicioMes).length,
  };
}

/* ---------- reportes: todo sale de lo que el negocio registró (nada inventado) ---------- */
export const PERIODOS = [['mes', 'Este mes'], ['3m', 'Últimos 3 meses'], ['anio', 'Este año'], ['todo', 'Todo']];
function desdePeriodo(p) {
  const h = hoy();
  if (p === 'mes') return new Date(h.getFullYear(), h.getMonth(), 1);
  if (p === '3m') return new Date(h.getFullYear(), h.getMonth() - 2, 1);
  if (p === 'anio') return new Date(h.getFullYear(), 0, 1);
  return new Date(0);
}
export function reporte(periodo = 'mes') {
  const desde = desdePeriodo(periodo).toISOString();
  const pagados = D.cobros.filter(cb => cb.estado === 'pagado' && (cb.pagado_el || '') >= desde);
  const ganadas = D.cotizaciones.filter(q => q.etapa === 'ganado' && (q.ganada_el || '') >= desde);
  const perdidas = D.cotizaciones.filter(q => q.etapa === 'perdido' && q.ultimo_contacto >= desde);
  const conMonto = ganadas.filter(q => q.monto > 0);
  const pendientes = D.cobros.filter(cb => cb.estado !== 'pagado');
  // de dónde vienen: clientes que llegaron en el periodo, agrupados por el origen que se registró
  const nuevos = D.contactos.filter(x => (x.creado || '') >= desde);
  const grupos = {};
  for (const x of nuevos) { const o = (x.origen || '').trim() || 'Sin origen'; (grupos[o] ??= { origen: o, clientes: 0, cobrado: 0 }).clientes++; }
  for (const cb of pagados) { const x = D.contactos.find(c => c.id === cb.contacto_id); const o = (x?.origen || '').trim() || 'Sin origen'; if (grupos[o]) grupos[o].cobrado += cb.monto; }
  const origenes = Object.values(grupos).sort((a, b) => b.clientes - a.clientes);
  // mejores clientes: los que más pagaron en el periodo
  const porCliente = {};
  for (const cb of pagados) porCliente[cb.contacto_id] = (porCliente[cb.contacto_id] || 0) + cb.monto;
  const mejores = Object.entries(porCliente).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([cid, total]) => ({ cliente: contacto(cid), total }));
  return {
    cobrado: pagados.reduce((s, cb) => s + cb.monto, 0), pagos: pagados.length,
    ganado: ganadas.reduce((s, q) => s + q.monto, 0), ganadas: ganadas.length, perdidas: perdidas.length,
    tasa: ganadas.length + perdidas.length ? Math.round(ganadas.length / (ganadas.length + perdidas.length) * 100) : null,
    ticket: conMonto.length ? conMonto.reduce((s, q) => s + q.monto, 0) / conMonto.length : null,
    porCobrar: pendientes.reduce((s, cb) => s + cb.monto, 0), pendientes: pendientes.length,
    vencido: pendientes.filter(cb => estadoCobro(cb).id === 'vencido').reduce((s, cb) => s + cb.monto, 0),
    clientesNuevos: nuevos.length, origenes, mejores,
    etapas: ETAPAS.map(e => { const qs = D.cotizaciones.filter(q => q.etapa === e.id); return { ...e, cantidad: qs.length, monto: qs.reduce((s, q) => s + q.monto, 0) }; }),
  };
}

/** Lo cobrado mes a mes (los últimos `n` meses). Solo pagos registrados: nada de ejemplo en un negocio real. */
export function ventasPorMes(n = 6) {
  const meses = [];
  for (let k = n - 1; k >= 0; k--) {
    const d = new Date(hoy().getFullYear(), hoy().getMonth() - k, 1);
    const desde = d.toISOString(), hasta = new Date(d.getFullYear(), d.getMonth() + 1, 1).toISOString();
    const total = D.cobros.filter(cb => cb.estado === 'pagado' && cb.pagado_el >= desde && cb.pagado_el < hasta).reduce((s, cb) => s + cb.monto, 0);
    meses.push([d.toLocaleDateString('es-PA', { month: 'short' }).replace('.', ''), total]);
  }
  // En la demostración los meses anteriores llevan cifras de ejemplo (la pantalla lo avisa).
  if (modo === 'demo') [2100, 2650, 2400, 3300, 3900, 4200, 3700, 4500, 5100, 4800, 5600].slice(-(n - 1)).forEach((v, j) => { meses[j][1] = v; });
  return meses;
}

// ---------- etapas automáticas: las cotizaciones avanzan solas (nunca retroceden) ----------
//   le escribes → Contactado · le envías la cotización → Cotizado · registras un cobro → Agendado
//   te paga → Ganado · 15 días sin respuesta → Perdido. Siempre se pueden mover a mano.
// El servidor hace lo mismo con «le escribes» cuando el mensaje sale por la API o desde el celular.
export const DIAS_PARA_PERDIDO = 15;
const AVANCE = ['nuevo', 'contactado', 'cotizado', 'agendado', 'ganado'];
const nombreEtapa = id => ETAPAS.find(e => e.id === id)?.nombre ?? id;
function moverSola(q, etapa, motivo, tocar = true) {
  q.etapa = etapa;
  if (tocar) q.ultimo_contacto = new Date().toISOString();
  q.ganada_el = etapa === 'ganado' ? new Date().toISOString() : null;
  enSupabase(sb?.from('cotizaciones').update({ etapa, ultimo_contacto: q.ultimo_contacto, ganada_el: q.ganada_el }).eq('id', q.id));
  registrar(etapa === 'ganado' ? 'pago' : 'cotizacion', `Cotización #${q.numero} pasó sola a ${nombreEtapa(etapa)}`, `${contacto(q.contacto_id).nombre} · ${motivo}`);
}
/** Lleva a «etapa» las cotizaciones abiertas del cliente que van antes (todas, o solo la más reciente). */
function avanzarCliente(contacto_id, etapa, motivo, todas = false) {
  const pos = AVANCE.indexOf(etapa);
  const atras = D.cotizaciones.filter(q => q.contacto_id === contacto_id && q.etapa !== 'perdido' && AVANCE.indexOf(q.etapa) < pos)
    .sort((a, b) => b.creada.localeCompare(a.creada));
  (todas ? atras : atras.slice(0, 1)).forEach(q => moverSola(q, etapa, motivo));
  return atras.length > 0;
}
/** Le escribiste por WhatsApp: sus cotizaciones en «Nuevo» pasan a «Contactado». */
export function escribioCliente(contacto_id) {
  const movio = avanzarCliente(contacto_id, 'contactado', 'le escribiste por WhatsApp', true);
  if (movio) guardar();
  return movio;
}
/** Le enviaste la cotización: pasa a «Cotizado» (si ya iba más adelante, solo cuenta como contacto). */
export function enviarCotizacion(qid) {
  const q = D.cotizaciones.find(x => x.id === qid); if (!q) return;
  if (AVANCE.indexOf(q.etapa) < AVANCE.indexOf('cotizado') && q.etapa !== 'perdido') moverSola(q, 'cotizado', 'le enviaste la cotización');
  else { q.ultimo_contacto = new Date().toISOString(); enSupabase(sb?.from('cotizaciones').update({ ultimo_contacto: q.ultimo_contacto }).eq('id', qid)); }
  guardar();
}
/** Al cargar la demostración: las que llevan 15 días sin respuesta pasan a «Perdido» (en un negocio real lo hace el servidor). */
function revisarSinRespuesta() {
  const limite = Date.now() - DIAS_PARA_PERDIDO * DIA;
  const viejas = D.cotizaciones.filter(q => ['contactado', 'cotizado'].includes(q.etapa) && new Date(q.ultimo_contacto).getTime() < limite);
  viejas.forEach(q => moverSola(q, 'perdido', `${Math.floor((Date.now() - new Date(q.ultimo_contacto)) / DIA)} días sin respuesta`, false));
  if (viejas.length) guardar();
}

// ---------- escrituras (en pantalla al instante; en Supabase por detrás) ----------
function registrar(tipo, titulo, detalle) {
  const a = { id: uuid(), tipo, titulo, detalle, fecha: new Date().toISOString() };
  D.actividad.push(a);
  enSupabase(sb?.from('actividad').insert({ id: a.id, negocio_id: nid(), tipo, titulo, detalle }));
}

/** Crear cliente. Devuelve el cliente, o { error } si ya existe uno con ese teléfono. */
export function crearContacto({ nombre, telefono, origen, nota }) {
  const ya = clientePorTelefono(telefono);
  if (ya) return { error: `Ya tienes a ${ya.nombre} con ese teléfono.` };
  const x = { id: uuid(), nombre, telefono, origen, nota, creado: new Date().toISOString() };
  D.contactos.push(x);
  const wa_id = waNumero(telefono) || null;
  const anotar = () => registrar(origen === 'WhatsApp' ? 'whatsapp' : 'web', 'Nuevo cliente', `${nombre} · ${origen}`);
  if (modo === 'real') {
    // la actividad se anota solo si el cliente de verdad quedó guardado
    sb.from('contactos').insert({ id: x.id, negocio_id: nid(), nombre, telefono, wa_id, origen, nota })
      .then(({ error }) => { if (error) throw error; anotar(); })
      .catch(e => enSupabase(Promise.reject(e)));
  } else anotar();
  guardar(); return x;
}
export function editarContacto(cid, { nombre, telefono, origen, nota }) {
  const x = D.contactos.find(c => c.id === cid); if (!x) return {};
  const ya = clientePorTelefono(telefono, cid);
  if (ya) return { error: `Ya tienes a ${ya.nombre} con ese teléfono.` };
  Object.assign(x, { nombre, telefono, origen, nota });
  enSupabase(sb?.from('contactos').update({ nombre, telefono, wa_id: waNumero(telefono) || null, origen, nota }).eq('id', cid));
  guardar(); return x;
}
/** Avisa a la pantalla cuando la base asigna el número definitivo (cotización o factura). */
let alNumerar = () => {};
export function cuandoNumere(fn) { alNumerar = fn; }
export function crearCotizacion({ contacto_id, servicio, monto }) {
  // Número provisional (el siguiente del negocio); el definitivo lo pone la base y se actualiza al responder.
  const base = modo === 'real' ? (D.negocio.ultima_cotizacion || 0) : 119;
  const q = { id: uuid(), numero: Math.max(base, ...D.cotizaciones.map(x => x.numero || 0)) + 1, contacto_id, servicio, monto: +monto || 0, etapa: 'nuevo', creada: new Date().toISOString(), ultimo_contacto: new Date().toISOString(), ganada_el: null };
  D.cotizaciones.push(q);
  if (modo === 'real') {
    sb.from('cotizaciones').insert({ id: q.id, negocio_id: nid(), contacto_id, servicio, monto: q.monto }).select('numero').single()
      .then(({ data, error }) => {
        if (error) throw error;
        const cambio = q.numero !== data.numero; q.numero = data.numero; D.negocio.ultima_cotizacion = Math.max(D.negocio.ultima_cotizacion || 0, data.numero);
        registrar('cotizacion', `Nueva cotización #${q.numero}`, `${contacto(contacto_id).nombre} · ${servicio}`);
        if (cambio) alNumerar();
      })
      .catch(e => enSupabase(Promise.reject(e)));
  } else registrar('cotizacion', `Nueva cotización #${q.numero}`, `${contacto(contacto_id).nombre} · ${servicio}`);
  guardar(); return q;
}
export function editarCotizacion(qid, { servicio, monto }) {
  const q = D.cotizaciones.find(x => x.id === qid); if (!q) return;
  q.servicio = servicio; q.monto = +monto || 0;
  enSupabase(sb?.from('cotizaciones').update({ servicio, monto: q.monto }).eq('id', qid));
  guardar();
}
export function moverCotizacion(qid, etapa) {
  const q = D.cotizaciones.find(x => x.id === qid); if (!q || q.etapa === etapa) return;
  q.etapa = etapa; q.ultimo_contacto = new Date().toISOString();
  q.ganada_el = etapa === 'ganado' ? new Date().toISOString() : null;
  enSupabase(sb?.from('cotizaciones').update({ etapa, ultimo_contacto: q.ultimo_contacto, ganada_el: q.ganada_el }).eq('id', qid));
  const nombre = ETAPAS.find(e => e.id === etapa).nombre;
  registrar(etapa === 'ganado' ? 'pago' : 'cotizacion', `Cotización #${q.numero} → ${nombre}`, `${contacto(q.contacto_id).nombre} · ${q.servicio}`); guardar();
}
export function marcarSeguimiento(qid) {
  const q = D.cotizaciones.find(x => x.id === qid); q.ultimo_contacto = new Date().toISOString();
  enSupabase(sb?.from('cotizaciones').update({ ultimo_contacto: q.ultimo_contacto }).eq('id', qid));
  registrar('seguimiento', 'Seguimiento enviado', `Cotización #${q.numero} · ${contacto(q.contacto_id).nombre}`); guardar();
}
/** Número de factura para mostrar: #0001, #0002… (cada negocio cuenta desde el 1, sin fin). */
export const numFactura = n => n ? '#' + String(n).padStart(4, '0') : '#…';
// el contador del negocio (incluye facturas anuladas, que no se muestran pero sí gastaron su número)
export const siguienteFactura = () => Math.max(D.negocio.ultimo_cobro || 0, ...D.cobros.map(cb => cb.numero || 0)) + 1;
export function crearCobro({ contacto_id, concepto, monto, vence }) {
  const cb = { id: uuid(), numero: siguienteFactura(), contacto_id, concepto, monto: +monto || 0, vence, estado: 'pendiente', pagado_el: null };
  D.cobros.push(cb);
  D.negocio.ultimo_cobro = Math.max(D.negocio.ultimo_cobro || 0, cb.numero);
  const anotar = () => registrar('cobro', `Nuevo cobro · factura ${numFactura(cb.numero)}`, `${contacto(contacto_id).nombre} · ${dineroTexto(cb.monto)}`);
  // En la base el número lo pone el servidor (así dos personas nunca sacan el mismo); se actualiza al responder.
  if (modo === 'real') {
    sb.from('cobros').insert({ id: cb.id, negocio_id: nid(), contacto_id, concepto, monto: cb.monto, vence }).select('numero').single()
      .then(({ data, error }) => {
        if (error) throw error;
        const cambio = cb.numero !== data.numero; cb.numero = data.numero; D.negocio.ultimo_cobro = Math.max(D.negocio.ultimo_cobro || 0, data.numero);
        anotar(); if (cambio) alNumerar();
      })
      .catch(e => enSupabase(Promise.reject(e)));
  } else anotar();
  avanzarCliente(contacto_id, 'agendado', 'registraste un cobro');
  guardar(); return cb;
}
/** Marcar pagado. Devuelve true si además una cotización del cliente pasó sola a «Ganado». */
export function marcarPagado(cid) {
  const cb = D.cobros.find(x => x.id === cid); cb.estado = 'pagado'; cb.pagado_el = new Date().toISOString();
  enSupabase(sb?.from('cobros').update({ estado: 'pagado', pagado_el: cb.pagado_el }).eq('id', cid));
  registrar('pago', `Pago registrado · factura ${numFactura(cb.numero)}`, `${contacto(cb.contacto_id).nombre} · ${dineroTexto(cb.monto)}`);
  const movio = avanzarCliente(cb.contacto_id, 'ganado', `pagó ${dineroTexto(cb.monto)}`);
  guardar(); return movio;
}
/** Anular un cobro (error de tipeo, se canceló el trabajo). Su número de factura no se vuelve a usar. */
export function anularCobro(cid) {
  const cb = D.cobros.find(x => x.id === cid); if (!cb) return;
  D.cobros = D.cobros.filter(x => x.id !== cid);
  D.negocio.ultimo_cobro = Math.max(D.negocio.ultimo_cobro || 0, cb.numero || 0);
  enSupabase(sb?.from('cobros').update({ estado: 'anulado' }).eq('id', cid));
  registrar('cobro', `Cobro anulado · factura ${numFactura(cb.numero)}`, `${contacto(cb.contacto_id).nombre} · ${dineroTexto(cb.monto)}`);
  guardar();
}
/** Montos para textos: con centavos solo si los tiene ($49.99, $650). */
export const dineroTexto = n => '$' + Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: Number.isInteger(+n) ? 0 : 2, maximumFractionDigits: 2 });
export function marcarRecordatorio(cid) {
  const cb = D.cobros.find(x => x.id === cid);
  registrar('cobro', 'Recordatorio de pago', `${contacto(cb.contacto_id).nombre} · ${estadoCobro(cb).texto.toLowerCase()}`); guardar();
}
export function alternarAutomatizacion(aid) {
  const a = D.automatizaciones.find(x => x.id === aid); a.activa = !a.activa;
  enSupabase(sb?.from('automatizaciones').upsert({ negocio_id: nid(), clave: aid, activa: a.activa, canal: a.canal }));
  guardar(); return a;
}
export function guardarBot(b) {
  D.bot = { activo: !!b.activo, saludo: b.saludo, opciones: b.opciones.slice(0, BOT_MAX_OPCIONES), pagos_en_menu: !!b.pagos_en_menu, humano_en_menu: !!b.humano_en_menu };
  enSupabase(sb?.from('bots').upsert({ negocio_id: nid(), ...D.bot, actualizado: new Date().toISOString() }));
  guardar(); return D.bot;
}
export function agregarPago({ tipo, titulo, detalle }) {
  const p = { id: uuid(), tipo, titulo, detalle, orden: D.pagos.length };
  D.pagos.push(p);
  enSupabase(sb?.from('metodos_pago').insert({ ...p, negocio_id: nid() }));
  guardar(); return p;
}
export function quitarPago(pid) {
  D.pagos = D.pagos.filter(p => p.id !== pid);
  enSupabase(sb?.from('metodos_pago').delete().eq('id', pid));
  guardar();
}
export function actualizarNegocio(campos) {
  Object.assign(D.negocio, campos);
  const { nombre, dueno, correo, telefono } = D.negocio;
  enSupabase(sb?.from('negocios').update({ nombre, dueno, correo, telefono }).eq('id', nid()));
  guardar();
}
