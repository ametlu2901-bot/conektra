/* Conexión con Supabase.

   Con `url` y `anonKey` vacíos el portal funciona solo en modo demostración (datos de ejemplo en el
   navegador). Con los dos puestos, se entra con un enlace al correo y se ven los datos reales.

   La clave «anon» es pública por diseño (va en el navegador): lo que protege los datos son las reglas
   de seguridad por negocio (RLS) de supabase/schema.sql. Nunca poner aquí la clave «service_role».
*/
export const SUPABASE = {
  url: 'https://rwbgrlpelywslphswcfd.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3YmdybHBlbHl3c2xwaHN3Y2ZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTU3MTYyMzAsImV4cCI6MjExMTI5MjIzMH0.YFeuwK5lMDmiqPKoR5eyK4WP9VWKid_LrjE18P7S4Sk',
};
