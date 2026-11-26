/* Conexión con Supabase.

   Con `url` y `anonKey` vacíos el portal funciona solo en modo demostración (datos de ejemplo en el
   navegador). Con los dos puestos, se entra con un enlace al correo y se ven los datos reales.

   La clave «anon» es pública por diseño (va en el navegador): lo que protege los datos son las reglas
   de seguridad por negocio (RLS) de supabase/schema.sql. Nunca poner aquí la clave «service_role».
*/
/* App de Meta de Enlaza Studio (WhatsApp, registro integrado). Mientras estén vacíos, el botón
   «Conectar mi WhatsApp» sale apagado. appId y configId son públicos (van en el navegador).
   El secreto de la app (App Secret) va SOLO en los secretos de Supabase, nunca aquí.
   configId: Facebook Login for Business → Configuraciones → la de «WhatsApp Embedded Signup».
   version: la versión vigente de la Graph API al crear la app. */
export const META = { appId: '', configId: '', version: 'v24.0' };

export const SUPABASE = {
  url: 'https://rwbgrlpelywslphswcfd.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3YmdybHBlbHl3c2xwaHN3Y2ZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTU3MTYyMzAsImV4cCI6MjExMTI5MjIzMH0.YFeuwK5lMDmiqPKoR5eyK4WP9VWKid_LrjE18P7S4Sk',
};
