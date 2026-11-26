/* «Conectar mi WhatsApp»: el registro integrado de Meta (Embedded Signup) con coexistencia.

   Abre la ventana oficial de Meta. El dueño entra con su Facebook, elige su portafolio y su número y, si ya
   usa la app WhatsApp Business, escanea un código QR con su celular (sigue usando la app como siempre).
   Al terminar, Meta entrega al navegador:
     • un `code` de un solo uso (en la respuesta de FB.login), que el servidor cambia por el token;
     • `waba_id` y `phone_number_id` (en un mensaje «WA_EMBEDDED_SIGNUP» de la ventana).
   Aquí solo se juntan esos datos; el token nunca pasa por el navegador.
*/
import { META } from './config.js?v=5';

export const metaListo = () => !!(META.appId && META.configId);

let sdk = null;
function cargarSdk() {
  if (sdk) return sdk;
  sdk = new Promise((ok, mal) => {
    window.fbAsyncInit = () => {
      window.FB.init({ appId: META.appId, autoLogAppEvents: true, xfbml: false, version: META.version });
      ok(window.FB);
    };
    const s = document.createElement('script');
    s.src = 'https://connect.facebook.net/es_LA/sdk.js'; s.async = true; s.defer = true; s.crossOrigin = 'anonymous';
    s.onerror = () => { sdk = null; mal(new Error('No se pudo abrir la ventana de Meta. Revisa tu conexión o desactiva el bloqueador de anuncios para esta página.')); };
    document.head.append(s);
  });
  return sdk;
}

const deFacebook = origen => { try { return /(^|\.)facebook\.com$/.test(new URL(origen).hostname); } catch (_) { return false; } };

/**
 * Abre el registro integrado y espera a que termine.
 * Devuelve { code, waba_id, phone_number_id, coexistencia } o lanza un Error con el motivo para mostrarlo.
 */
export async function registroIntegrado() {
  const FB = await cargarSdk();
  return new Promise((ok, mal) => {
    let code = null, sesion = null, listo = false, espera = 0;
    const terminar = (error, datos) => {
      if (listo) return;
      listo = true; clearTimeout(espera); removeEventListener('message', oir);
      error ? mal(new Error(error)) : ok(datos);
    };
    const intentar = () => { if (code && sesion) terminar(null, { code, ...sesion }); };

    function oir(ev) {
      if (!deFacebook(ev.origin)) return;
      let d; try { d = typeof ev.data === 'string' ? JSON.parse(ev.data) : ev.data; } catch (_) { return; }
      if (d?.type !== 'WA_EMBEDDED_SIGNUP') return;
      const ev2 = String(d.event || '');
      if (ev2.startsWith('FINISH')) {
        if (!d.data?.phone_number_id) return terminar('Se creó la cuenta de WhatsApp, pero no se eligió un número. Vuelve a intentarlo y elige tu número.');
        // FINISH_WHATSAPP_BUSINESS_APP_ONBOARDING = número que ya está en la app (coexistencia); FINISH = número nuevo solo para la API.
        sesion = { waba_id: d.data.waba_id, phone_number_id: d.data.phone_number_id, coexistencia: ev2 === 'FINISH_WHATSAPP_BUSINESS_APP_ONBOARDING' };
        intentar();
      } else if (ev2 === 'CANCEL') {
        terminar(d.data?.error_message ? `Meta dice: ${d.data.error_message}` : 'Cerraste la ventana de Meta antes de terminar. Puedes intentarlo otra vez cuando quieras.');
      } else if (ev2 === 'ERROR') {
        terminar(`Meta no pudo terminar: ${d.data?.error_message || 'error desconocido'}.`);
      }
    }
    addEventListener('message', oir);

    // El callback de FB.login no puede ser async (el SDK lo rechaza).
    FB.login(r => {
      if (!r?.authResponse?.code) return terminar('Cerraste la ventana de Meta antes de terminar. Puedes intentarlo otra vez cuando quieras.');
      code = r.authResponse.code;
      intentar();
      // El aviso con el número a veces llega un instante después de cerrar la ventana.
      espera = setTimeout(() => terminar('Meta no confirmó qué número se conectó. Inténtalo otra vez.'), 10000);
    }, {
      config_id: META.configId,
      response_type: 'code',
      override_default_response_type: true,
      extras: { setup: {}, featureType: 'whatsapp_business_app_onboarding', sessionInfoVersion: '3' },
    });
  });
}
