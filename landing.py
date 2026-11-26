"""Páginas de servicio de Enlaza Studio pensadas para Google (español, Panamá).

Cada página apunta a una búsqueda concreta: su <title>, su H1 y sus H2 llevan las palabras
que la gente escribe en Google. Usan el diseño 3.0 (css/v3.css, js/v3.js) y las mismas
vistas de producto de la portada (inicio._vis).

Regla: no prometer lo que no está probado. Lo que depende del proyecto se dice así.
"""
import json
import os

import inicio
import textos3
from iconos import I

FECHA = "2026-11-26"

# clave → (ruta, vista de la portada que la ilustra)
PAGINAS = {
    "web": dict(
        ruta="paginas-web-panama/", vista="atrae", menu="Páginas web",
        titulo="Páginas web en Panamá para pequeños negocios | Enlaza Studio",
        meta="Diseño de páginas web en Panamá para pequeños negocios: rápidas en celular, listas para Google y Google Maps, con botón de WhatsApp y formulario de cotización. Diagnóstico gratis.",
        etq="Páginas web · Panamá",
        h1="Páginas web en Panamá que te traen clientes por WhatsApp",
        lead="Diseño web en Panamá para pequeños negocios: creamos la página web de tu negocio para que aparezca en Google, cargue rápido en el celular y lleve a cada persona directo a tu WhatsApp o a un formulario de cotización.",
        dolor_h2="¿Tu negocio no aparece en Google?",
        dolor=["No tienes página web, o la que tienes no te trae clientes.",
               "Cuando buscan lo que haces en Panamá, sale la competencia.",
               "Te escriben por WhatsApp sin datos y pierdes tiempo preguntando lo mismo."],
        incluye_h2="Qué incluye tu página web",
        incluye=[("Diseño a la medida", "Hecha para tu marca y tus servicios, no una plantilla genérica."),
                 ("Pensada para celular", "La mayoría de tus clientes te va a ver desde el teléfono."),
                 ("Lista para Google", "Títulos, descripciones, mapa del sitio y Search Console configurados."),
                 ("Google Maps y perfil de empresa", "Te ayudamos a que tu negocio salga en el mapa de tu zona."),
                 ("Botón de WhatsApp", "Cada visita puede escribirte con un toque, con un mensaje ya listo."),
                 ("Formulario de cotización", "Las solicitudes llegan ordenadas a una hoja de Google, no sueltas.")],
        pasos_h2="Cómo hacemos tu página web",
        faq_h2="Preguntas frecuentes sobre páginas web",
        faq=[("¿Cuánto cuesta una página web en Panamá?", "Depende de cuántas secciones y funciones lleve. Después del diagnóstico gratis te enviamos una propuesta con precio cerrado antes de empezar."),
             ("¿Cuánto tarda?", "Te damos el tiempo exacto en la propuesta. Trabajamos por etapas y puedes ver los avances en tu celular."),
             ("¿Incluye dominio propio?", "Sí, te ayudamos a comprar y conectar tu dominio (por ejemplo, tunegocio.com) a tu nombre."),
             ("¿Me garantizan el primer lugar en Google?", "Nadie puede garantizarlo con honestidad. Dejamos tu página técnicamente lista y con textos pensados para lo que buscan tus clientes en Panamá.")],
        servicio="Diseño de páginas web",
    ),
    "crm": dict(
        ruta="crm-whatsapp/", vista="vende", menu="CRM para WhatsApp",
        titulo="CRM para WhatsApp: seguimiento de clientes y cotizaciones | Enlaza Studio",
        meta="CRM para negocios que venden por WhatsApp en Panamá: cada cliente con su etapa, recordatorios de seguimiento automáticos y cotizaciones que no se quedan sin respuesta.",
        etq="CRM · Seguimiento de clientes",
        h1="CRM para WhatsApp: ninguna cotización sin seguimiento",
        lead="Un CRM sencillo para negocios que atienden por WhatsApp, para el seguimiento de clientes y cotizaciones. Cada cliente entra a un tablero con su etapa y el sistema te recuerda a quién responder antes de que se enfríe.",
        dolor_h2="¿Se te escapan clientes en el chat?",
        dolor=["Tus clientes están repartidos entre chats, libretas y hojas sueltas.",
               "Envías cotizaciones y se te olvida darles seguimiento.",
               "No sabes cuántas ventas cierras al mes ni dónde se pierden."],
        incluye_h2="Qué incluye tu CRM",
        incluye=[("Etapas a tu manera", "Nuevo, cotizado, ganado… las etapas que de verdad usa tu negocio."),
                 ("Entrada automática", "Las solicitudes de tu página y tu formulario llegan solas, con sus datos."),
                 ("Recordatorios de seguimiento", "Te avisa qué cotizaciones llevan días sin respuesta."),
                 ("Clientes antiguos", "Mensajes para que vuelvan quienes no te escriben hace meses."),
                 ("Historial por cliente", "Qué pidió, cuánto se cotizó y en qué quedó, en un solo lugar."),
                 ("Reportes claros", "Cuántos clientes entran, cuántos cierras y cuánto vendes.")],
        pasos_h2="Cómo armamos tu CRM",
        faq_h2="Preguntas frecuentes sobre el CRM",
        faq=[("¿Qué es un CRM?", "Es un sistema para ordenar a tus clientes: quién te escribió, qué le cotizaste y qué falta para cerrar la venta."),
             ("¿Funciona con mi WhatsApp de siempre?", "Sí. Puedes seguir atendiendo desde tu WhatsApp Business. Si quieres automatizar mensajes, lo hacemos con la API oficial de Meta, nunca con bots no oficiales."),
             ("¿Tengo que pagar licencias caras?", "Casi nunca. Muchas veces empezamos con herramientas que ya usas, como Google Sheets, y crecemos cuando haga falta."),
             ("¿Lo puede usar mi equipo?", "Sí. Cada persona ve sus clientes y tú ves el total del negocio.")],
        servicio="CRM para WhatsApp",
    ),
    "cobros": dict(
        ruta="cobros-por-whatsapp/", vista="cobra", menu="Cobros por WhatsApp",
        titulo="Recordatorios de cobro por WhatsApp: cobranza automática | Enlaza Studio",
        meta="Cobranza automática por WhatsApp para negocios en Panamá: recordatorios de pago antes y después del vencimiento y una lista al día de quién te debe y cuánto.",
        etq="Cobranza · Cuentas por cobrar",
        h1="Recordatorios de cobro por WhatsApp para cobrar a tiempo",
        lead="El sistema le recuerda a cada cliente su pago por WhatsApp antes y después del vencimiento, y tú ves en una sola lista quién te debe, cuánto y desde cuándo.",
        dolor_h2="¿Te cuesta cobrar sin perseguir a nadie?",
        dolor=["Tienes que acordarte de escribirle a cada cliente que te debe.",
               "Te da pena cobrar y los pagos se atrasan semanas.",
               "No tienes claro cuánto te deben en total."],
        incluye_h2="Qué incluye la cobranza automática",
        incluye=[("Recordatorios de pago", "Mensajes amables antes de la fecha y avisos cuando ya venció."),
                 ("Cuentas por cobrar", "Quién debe, cuánto y desde cuándo, siempre al día."),
                 ("Aviso cuando pagan", "Marcas el pago y el cliente sale de la lista de pendientes."),
                 ("Tus formas de pago", "El mensaje indica cómo pagarte: transferencia, Yappy o lo que uses."),
                 ("Mensajes con tu tono", "Escribimos los recordatorios contigo para que suenen a tu negocio."),
                 ("Resumen semanal", "Cuánto cobraste y qué vence en los próximos días.")],
        pasos_h2="Cómo activamos tu cobranza",
        faq_h2="Preguntas frecuentes sobre la cobranza",
        faq=[("¿Los mensajes salen de mi número?", "Sí, la idea es que tus clientes reciban el recordatorio de tu propio WhatsApp, usando la API oficial de Meta."),
             ("¿Puedo cobrar con Yappy o transferencia?", "Sí. El recordatorio indica cómo pagarte. La conexión directa con plataformas de pago se evalúa según el proyecto."),
             ("¿Y si un cliente se molesta?", "Los mensajes los escribimos contigo, con un tono amable, y tú decides cuándo y cuántas veces se envían."),
             ("¿Sirve si cobro a crédito o por cuotas?", "Sí. Registramos cada pago con su fecha y el sistema avisa cuota por cuota.")],
        servicio="Cobranza automática por WhatsApp",
    ),
    "erp": dict(
        ruta="automatizacion-whatsapp/", vista="controla", menu="Automatización de WhatsApp",
        titulo="Automatización de WhatsApp Business en Panamá: WhatsApp automatizado | Enlaza Studio",
        meta="Automatización de WhatsApp Business para negocios en Panamá con la API oficial de Meta: mensajes automáticos, seguimientos, recordatorios y un reporte diario de tu negocio.",
        etq="Automatización · WhatsApp Business",
        h1="Automatización de WhatsApp Business para tu negocio",
        lead="Automatizamos lo que hoy haces a mano en WhatsApp: seguimientos, recordatorios, avisos y un resumen diario de tu negocio, con la API oficial de Meta y tu propio número.",
        dolor_h2="¿Pasas el día contestando lo mismo?",
        dolor=["Respondes las mismas preguntas una y otra vez.",
               "Se te olvidan seguimientos y recordatorios importantes.",
               "Para saber cómo va el negocio tienes que preguntar o revisar todo a mano."],
        incluye_h2="Qué podemos automatizar",
        incluye=[("Mensajes automáticos", "Respuestas a preguntas frecuentes y mensajes fuera de horario."),
                 ("Seguimientos", "Recordatorios a clientes que no respondieron una cotización."),
                 ("Recordatorios de cita y pago", "Avisos antes de una cita o de un vencimiento."),
                 ("Reporte diario", "Un resumen a tu WhatsApp cada mañana con ventas, cobros y pendientes."),
                 ("Alertas", "Te avisa cuando algo se sale de lo normal."),
                 ("API oficial de Meta", "Sin bots no oficiales que ponen en riesgo tu número.")],
        pasos_h2="Cómo automatizamos tu WhatsApp",
        faq_h2="Preguntas frecuentes sobre automatizar WhatsApp",
        faq=[("¿Es un chatbot?", "Puede incluir respuestas automáticas, pero no buscamos reemplazarte: automatizamos lo repetitivo para que tú atiendas lo importante."),
             ("¿Puedo seguir usando WhatsApp en mi celular?", "Sí. Con la coexistencia de Meta puedes seguir usando la app de WhatsApp Business y automatizar a la vez. Lo revisamos en el diagnóstico para tu caso."),
             ("¿Me pueden bloquear el número?", "Usamos solo la API oficial de Meta y sus reglas, que es lo que protege tu número. Nunca usamos bots no oficiales."),
             ("¿Cuánto cuesta enviar mensajes?", "Meta cobra algunos tipos de mensajes según su tarifa. Te lo explicamos con números claros en la propuesta.")],
        servicio="Automatización de WhatsApp Business",
    ),
    "api": dict(
        ruta="integraciones/", vista="conecta", menu="Integraciones",
        titulo="Integraciones de WhatsApp, Google Sheets y tus herramientas | Enlaza Studio",
        meta="Conectamos WhatsApp, tu página web, Google Sheets, Gmail y Calendar para que no copies datos a mano. Factura electrónica DGI y pagos según proyecto. Negocios en Panamá.",
        etq="Integraciones · Conexiones",
        h1="Integraciones con WhatsApp, Google Sheets y tus herramientas",
        lead="Unimos las herramientas que ya usas para que la información pase sola de una a otra: tu página, tu WhatsApp, tus hojas de cálculo, tu correo y tu agenda.",
        dolor_h2="¿Copias los mismos datos en varios lados?",
        dolor=["Pasas datos del chat a una hoja y de la hoja al correo.",
               "Cada herramienta tiene una parte de la información y ninguna el total.",
               "Un error al copiar te cuesta una venta o un cobro."],
        incluye_h2="Qué podemos conectar",
        incluye=[("WhatsApp", "Mensajes y avisos conectados con tus clientes y tus cobros."),
                 ("Página web y formularios", "Cada solicitud llega sola a donde la necesitas."),
                 ("Google Sheets", "Tus datos ordenados en hojas que ya sabes usar."),
                 ("Gmail y Calendar", "Correos y citas que se crean sin escribirlos dos veces."),
                 ("Factura electrónica DGI", "Se evalúa según tu proyecto y tu proveedor de facturación."),
                 ("Pagos (Yappy, PágueloFácil y otros)", "Se evalúan según lo que permite cada plataforma.")],
        pasos_h2="Cómo conectamos tus herramientas",
        faq_h2="Preguntas frecuentes sobre integraciones",
        faq=[("¿Tengo que cambiar las herramientas que uso?", "Casi nunca. Primero conectamos lo que ya tienes. Si algo no da para más, te lo decimos."),
             ("¿Pueden conectar la factura electrónica de la DGI?", "Se evalúa según el proyecto. Antes de prometerlo revisamos qué permite tu proveedor y lo probamos contigo."),
             ("¿Mis datos quedan seguros?", "Tus datos quedan en tus propias cuentas, con los permisos mínimos y todo documentado."),
             ("¿Qué pasa si una herramienta cambia?", "Seguimos contigo con soporte: si algo cambia, lo ajustamos.")],
        servicio="Integraciones de sistemas",
    ),
    "conectar": dict(
        ruta="conectar-whatsapp/", vista="conecta", menu="Conectar WhatsApp a tu sistema",
        titulo="Conectar WhatsApp a tu sistema, CRM o Google Sheets | Enlaza Studio",
        meta="Conectamos tu WhatsApp con tu sistema, tu CRM, tu página web o Google Sheets para que cada cliente y cada mensaje quede registrado solo. Para negocios en Panamá.",
        etq="Integración · WhatsApp",
        h1="Conectar WhatsApp a tu sistema, sin copiar nada a mano",
        lead="Unimos tu WhatsApp con el sistema que ya usas (un CRM, una hoja de Google, tu página web o tu propio programa) para que cada cliente, cotización y pago quede registrado sin que nadie lo copie.",
        dolor_h2="¿Tu WhatsApp está desconectado del resto?",
        dolor=["Lo que hablas por WhatsApp no queda en ningún sistema.",
               "Copias a mano nombres, pedidos y pagos del chat a una hoja.",
               "Si alguien de tu equipo falta, nadie sabe qué se habló con el cliente."],
        incluye_h2="Qué conectamos con tu WhatsApp",
        incluye=[("Tu CRM o sistema", "Cada conversación nueva crea o actualiza al cliente en tu sistema."),
                 ("Google Sheets", "Los datos del cliente y del pedido se guardan solos en tu hoja."),
                 ("Tu página web", "El formulario y el botón de WhatsApp alimentan el mismo registro."),
                 ("Avisos automáticos", "Tu sistema puede enviar mensajes de WhatsApp: confirmaciones, recordatorios y cobros."),
                 ("API oficial de Meta", "La conexión se hace con la API oficial de WhatsApp Business, a nombre de tu negocio."),
                 ("Tu propio programa", "Si ya tienes un sistema, lo conectamos por API o webhooks según lo que permita.")],
        pasos_h2="Cómo conectamos WhatsApp a tu sistema",
        faq_h2="Preguntas frecuentes sobre conectar WhatsApp",
        faq=[("¿Se puede conectar WhatsApp a cualquier sistema?", "A casi cualquiera que permita recibir o enviar datos (API, webhooks o una hoja de cálculo). En el diagnóstico revisamos el tuyo y te decimos qué es posible."),
             ("¿Necesito la API de WhatsApp Business?", "Para enviar y recibir mensajes de forma automática, sí. Te ayudamos a activarla a nombre de tu negocio; el número y la cuenta siguen siendo tuyos."),
             ("¿Puedo seguir usando WhatsApp en mi celular?", "En muchos casos sí, con la coexistencia que ofrece Meta. Lo revisamos para tu número en el diagnóstico."),
             ("¿Qué pasa con mis chats anteriores?", "Siguen en tu WhatsApp. La conexión registra lo que pasa desde que se activa.")],
        servicio="Integración de WhatsApp con sistemas",
    ),
    "chatbot": dict(
        ruta="chatbot-whatsapp/", vista="vende", menu="Chatbot y WhatsApp automatizado",
        titulo="WhatsApp automatizado y chatbot para negocios en Panamá | Enlaza Studio",
        meta="WhatsApp automatizado para tu negocio: respuestas automáticas, preguntas frecuentes, toma de datos y seguimiento, con la API oficial de Meta. Sin bots que pongan en riesgo tu número.",
        etq="Chatbot · WhatsApp automatizado",
        h1="WhatsApp automatizado: un chatbot que atiende mientras trabajas",
        lead="Un bot de WhatsApp con respuestas automáticas, hecho con la API oficial: configuramos tu WhatsApp para que tus clientes reciban información al instante, dejen sus datos y tú solo atiendas lo que de verdad necesita una persona.",
        dolor_h2="¿Pierdes clientes por no contestar a tiempo?",
        dolor=["Te escriben de noche o en fin de semana y respondes tarde.",
               "Contestas las mismas preguntas de precio, horario y ubicación todo el día.",
               "El cliente se va con quien le respondió primero."],
        incluye_h2="Qué hace tu WhatsApp automatizado",
        incluye=[("Respuesta inmediata", "Saluda y orienta al cliente en segundos, a cualquier hora."),
                 ("Preguntas frecuentes", "Precios de referencia, horarios, ubicación y servicios, escritos contigo."),
                 ("Toma de datos", "Pide nombre, qué necesita y dónde, y lo guarda en tu sistema."),
                 ("Pase a una persona", "Cuando el cliente lo necesita, la conversación pasa a ti o a tu equipo."),
                 ("Seguimiento", "Si el cliente no responde una cotización, el sistema le recuerda."),
                 ("Número seguro", "Solo con la API oficial de Meta: nada de bots no oficiales que bloquean números.")],
        pasos_h2="Cómo armamos tu chatbot de WhatsApp",
        faq_h2="Preguntas frecuentes sobre el chatbot de WhatsApp",
        faq=[("¿El chatbot reemplaza a mi equipo?", "No. Se encarga de lo repetitivo y de no dejar a nadie esperando; las ventas y los casos especiales los atienden ustedes."),
             ("¿Me pueden bloquear el número?", "Usamos solo la API oficial de WhatsApp Business de Meta y sus reglas, que es lo que protege tu número."),
             ("¿Puede usar inteligencia artificial?", "Se puede evaluar según tu caso. Muchas veces unas respuestas bien pensadas resuelven la mayoría de las preguntas."),
             ("¿Cuánto cuesta?", "Depende de lo que automatices. Después del diagnóstico gratis te damos un precio cerrado; aparte, Meta cobra algunos mensajes según su tarifa.")],
        servicio="Chatbot de WhatsApp",
    ),
    "wabapi": dict(
        ruta="whatsapp-business-api/", vista="controla", menu="WhatsApp Business API",
        titulo="WhatsApp Business API en Panamá: activación y automatización | Enlaza Studio",
        meta="Te ayudamos a activar la API oficial de WhatsApp Business (Meta) a nombre de tu negocio y a usarla para automatizar mensajes, cobros y seguimiento. Negocios en Panamá.",
        etq="WhatsApp Business API · Meta",
        h1="WhatsApp Business API para tu negocio en Panamá",
        lead="La API oficial de WhatsApp Business es lo que permite automatizar mensajes de forma segura. Te ayudamos a activarla a nombre de tu negocio y la conectamos con tus clientes, tus cobros y tus reportes.",
        dolor_h2="¿WhatsApp Business ya se te quedó corto?",
        dolor=["La app de WhatsApp Business no te deja automatizar lo que necesitas.",
               "Varias personas atienden el mismo número y se pierde el orden.",
               "Quieres mandar recordatorios y avisos sin hacerlo uno por uno."],
        incluye_h2="Qué incluye la activación de la API",
        incluye=[("Cuenta a tu nombre", "El portafolio de Meta, el número y la cuenta de WhatsApp son de tu negocio."),
                 ("Verificación del negocio", "Te guiamos en la verificación con Meta y en el nombre que verán tus clientes."),
                 ("Plantillas de mensajes", "Preparamos y enviamos a aprobación tus mensajes de recordatorio, cobro y seguimiento."),
                 ("Coexistencia", "Cuando aplica, puedes seguir usando la app en tu celular junto a la API."),
                 ("Conexión con tu sistema", "Los mensajes quedan registrados en tu CRM, tu hoja o tu panel."),
                 ("Costos claros", "Te explicamos la tarifa de Meta por mensaje antes de empezar.")],
        pasos_h2="Cómo activamos tu WhatsApp Business API",
        faq_h2="Preguntas frecuentes sobre WhatsApp Business API",
        faq=[("¿Qué diferencia hay con la app de WhatsApp Business?", "La app es para atender a mano desde el celular. La API permite automatizar, conectar con sistemas y que varias personas atiendan de forma ordenada."),
             ("¿Necesito tener mi negocio registrado?", "Meta pide verificar el negocio para algunas funciones. Te explicamos qué documentos necesitas según tu caso."),
             ("¿La API es gratis?", "Activarla no tiene costo de Meta, pero Meta cobra ciertos mensajes según su tarifa por país. Te lo mostramos con números claros."),
             ("¿El número sigue siendo mío?", "Sí. Todo queda a nombre de tu negocio; nosotros solo lo configuramos y lo conectamos.")],
        servicio="Activación de WhatsApp Business API",
    ),
    "s_clinicas": dict(
        ruta="sistema-para-clinicas/", vista="cobra", menu="Clínicas y consultorios",
        titulo="Sistema para clínicas y consultorios: citas y recordatorios por WhatsApp | Enlaza Studio",
        meta="Sistema para clínicas, consultorios y odontólogos en Panamá: agenda de citas, recordatorios por WhatsApp para que no falten, seguimiento de pacientes y cobros ordenados.",
        etq="Sector · Salud",
        h1="Sistema para clínicas y consultorios con recordatorios de citas por WhatsApp",
        lead="Tus pacientes escriben por WhatsApp para pedir cita. Ordenamos esas solicitudes, enviamos recordatorios automáticos para que no falten y te mostramos qué se cobró y qué está pendiente.",
        dolor_h2="¿Pacientes que no llegan a su cita?",
        dolor=["Los pacientes olvidan la cita y pierdes ese espacio en la agenda.",
               "La recepción pasa el día respondiendo precios y horarios por WhatsApp.",
               "No hay un registro claro de quién debe un saldo o una cuota."],
        incluye_h2="Qué incluye para tu clínica",
        incluye=[("Recordatorios de cita", "Un mensaje por WhatsApp el día antes y unas horas antes de la cita."),
                 ("Solicitudes ordenadas", "Cada paciente nuevo queda registrado con lo que necesita."),
                 ("Respuestas rápidas", "Horarios, ubicación y servicios respondidos al instante."),
                 ("Control de pagos", "Saldos, abonos y cuotas con recordatorios amables."),
                 ("Página web de la clínica", "Lista para Google y Google Maps, con botón para agendar por WhatsApp."),
                 ("Resumen diario", "Citas del día, pacientes nuevos y pagos pendientes en un mensaje.")],
        pasos_h2="Cómo lo implementamos en tu clínica",
        faq_h2="Preguntas frecuentes para clínicas y consultorios",
        faq=[("¿Sirve para odontólogos, fisioterapeutas y otros consultorios?", "Sí. Se adapta a cualquier consulta que agende citas y atienda por WhatsApp."),
             ("¿Los recordatorios salen de nuestro número?", "Sí, con la API oficial de WhatsApp Business a nombre de la clínica."),
             ("¿Se guarda información médica?", "No guardamos historias clínicas: solo datos de contacto, citas y pagos, en cuentas de la clínica."),
             ("¿Funciona con la agenda que ya usamos?", "Muchas veces sí, como Google Calendar. Lo revisamos en el diagnóstico.")],
        servicio="Sistema de citas y recordatorios para clínicas",
    ),
    "s_talleres": dict(
        ruta="sistema-para-talleres/", vista="vende", menu="Talleres mecánicos",
        titulo="Sistema para talleres mecánicos: cotizaciones y avisos por WhatsApp | Enlaza Studio",
        meta="Sistema para talleres mecánicos y de servicio en Panamá: cotizaciones ordenadas, avisos al cliente por WhatsApp cuando su carro está listo y cobros al día.",
        etq="Sector · Talleres",
        h1="Sistema para talleres: cotizaciones, avisos y cobros por WhatsApp",
        lead="Cada carro que entra queda registrado con su cotización y su estado. El cliente recibe avisos por WhatsApp y tú sabes qué trabajos están abiertos y qué falta por cobrar.",
        dolor_h2="¿El taller funciona a punta de chats y libretas?",
        dolor=["Las cotizaciones se pierden entre audios y fotos de WhatsApp.",
               "Los clientes llaman a cada rato para preguntar si su carro está listo.",
               "Se te olvida cobrar repuestos o saldos pendientes."],
        incluye_h2="Qué incluye para tu taller",
        incluye=[("Registro de trabajos", "Cliente, vehículo, cotización y estado en un solo lugar."),
                 ("Avisos por WhatsApp", "«Tu carro está listo» y avances sin que tengas que escribir uno por uno."),
                 ("Seguimiento de cotizaciones", "Recordatorio a quien no ha aprobado su cotización."),
                 ("Cobros y saldos", "Lo pendiente por cobrar, con recordatorios amables."),
                 ("Mantenimientos", "Aviso al cliente cuando le toca su próximo servicio."),
                 ("Página web del taller", "Para que te encuentren en Google y Maps cuando buscan un taller cerca.")],
        pasos_h2="Cómo lo implementamos en tu taller",
        faq_h2="Preguntas frecuentes para talleres",
        faq=[("¿Sirve para talleres de chapistería, motos o refrigeración?", "Sí. Se adapta a cualquier taller que cotice y entregue trabajos."),
             ("¿Mi equipo tiene que aprender un programa complicado?", "No. Lo diseñamos simple y les enseñamos a usarlo."),
             ("¿Puedo mandar la cotización por WhatsApp?", "Sí, y queda registrada para darle seguimiento."),
             ("¿Cuánto cuesta?", "Te damos un precio cerrado después del diagnóstico gratis.")],
        servicio="Sistema para talleres",
    ),
    "s_mudanzas": dict(
        ruta="sistema-para-mudanzas/", vista="atrae", menu="Mudanzas y transporte",
        titulo="Sistema y página web para empresas de mudanzas y transporte | Enlaza Studio",
        meta="Página web y sistema para empresas de mudanzas, acarreos y transporte en Panamá: cotizaciones por WhatsApp, seguimiento de clientes y cobros ordenados.",
        etq="Sector · Mudanzas y transporte",
        h1="Sistema para empresas de mudanzas, acarreos y transporte",
        lead="Tus clientes piden precio por WhatsApp a toda hora. Te ayudamos a que te encuentren en Google, a que cada cotización quede registrada y a que ninguna se quede sin seguimiento.",
        dolor_h2="¿Cotizas todo el día y cierras poco?",
        dolor=["Mandas precios por WhatsApp y el cliente no vuelve a responder.",
               "No sabes cuántas mudanzas cotizaste ni cuántas cerraste este mes.",
               "Cuando buscan mudanzas en Google, sale la competencia."],
        incluye_h2="Qué incluye para tu empresa de mudanzas",
        incluye=[("Página web lista para Google", "Con tus servicios, zonas y botón de cotizar por WhatsApp."),
                 ("Formulario de cotización", "Origen, destino, fecha y qué se muda: llega ordenado."),
                 ("Seguimiento automático", "Recordatorio al cliente que no respondió la cotización."),
                 ("Confirmaciones", "Aviso al cliente con la fecha y la hora del servicio."),
                 ("Cobros", "Adelantos y saldos registrados, con recordatorios."),
                 ("Reseñas", "Pedimos la reseña de Google después de cada trabajo.")],
        pasos_h2="Cómo lo implementamos en tu empresa",
        faq_h2="Preguntas frecuentes para mudanzas y transporte",
        faq=[("¿Ya trabajaron con empresas de mudanzas?", "Sí. Hicimos la página y el sistema de cotizaciones de Acarreos Makena, en Panamá."),
             ("¿Sirve para fletes, acarreos y transporte de carga?", "Sí. Las etapas y los datos se adaptan a tu tipo de servicio."),
             ("¿Puedo ver las cotizaciones desde el celular?", "Sí. Todo se consulta desde el teléfono."),
             ("¿Cuánto cuesta?", "Te damos un precio cerrado después del diagnóstico gratis.")],
        servicio="Sistema para empresas de mudanzas",
    ),
    "s_tiendas": dict(
        ruta="pedidos-por-whatsapp/", vista="cobra", menu="Tiendas y pedidos",
        titulo="Pedidos por WhatsApp para tiendas: catálogo, pedidos y cobros | Enlaza Studio",
        meta="Sistema de pedidos por WhatsApp para tiendas y negocios con catálogo en Panamá: pedidos ordenados, confirmaciones automáticas, cobros y clientes que vuelven a comprar.",
        etq="Sector · Tiendas y catálogos",
        h1="Pedidos por WhatsApp ordenados para tu tienda",
        lead="Si vendes por WhatsApp o Instagram, cada pedido queda registrado con lo que pidió el cliente, si ya pagó y cuándo se entrega, y tus clientes reciben confirmaciones y avisos automáticos.",
        dolor_h2="¿Los pedidos se pierden entre tantos chats?",
        dolor=["Tienes que revisar el chat para saber qué pidió cada cliente.",
               "Se te pasa confirmar pagos o entregas.",
               "Los clientes compran una vez y no vuelven."],
        incluye_h2="Qué incluye para tu tienda",
        incluye=[("Registro de pedidos", "Cliente, productos, monto y estado de cada pedido."),
                 ("Confirmaciones automáticas", "Pedido recibido, pago confirmado y entrega en camino."),
                 ("Cobros", "Quién pagó, quién no y recordatorios amables."),
                 ("Clientes que vuelven", "Mensajes a clientes que no compran hace tiempo."),
                 ("Catálogo en tu página", "Tus productos en una página rápida con botón de WhatsApp."),
                 ("Reporte de ventas", "Cuánto vendiste en el día y en el mes.")],
        pasos_h2="Cómo lo implementamos en tu tienda",
        faq_h2="Preguntas frecuentes para tiendas",
        faq=[("¿Sirve si vendo por Instagram?", "Sí. Los pedidos de Instagram y WhatsApp se pueden registrar en el mismo lugar."),
             ("¿Es una tienda en línea con pago con tarjeta?", "El enfoque es ordenar los pedidos que ya recibes. Los pagos en línea se evalúan según el proyecto."),
             ("¿Puedo aceptar Yappy o transferencia?", "Sí, el pedido indica cómo pagar y tú marcas cuando se recibe."),
             ("¿Cuánto cuesta?", "Te damos un precio cerrado después del diagnóstico gratis.")],
        servicio="Sistema de pedidos por WhatsApp",
    ),
    "s_tecnicos": dict(
        ruta="sistema-para-contratistas/", vista="controla", menu="Contratistas y servicios técnicos",
        titulo="Sistema para contratistas y servicios técnicos: cotizaciones y cobros | Enlaza Studio",
        meta="Sistema para contratistas, técnicos de aire acondicionado, electricistas y mantenimiento en Panamá: cotizaciones, visitas, avisos por WhatsApp y cobros ordenados.",
        etq="Sector · Construcción y mantenimiento",
        h1="Sistema para contratistas y servicios técnicos",
        lead="Cotizaciones, visitas técnicas y cobros en un solo lugar. Tus clientes reciben confirmaciones por WhatsApp y tú sabes qué trabajos están pendientes y cuánto te deben.",
        dolor_h2="¿Mucho trabajo y poco orden?",
        dolor=["Las cotizaciones quedan en el chat y nadie les da seguimiento.",
               "Se cruzan visitas o se olvida confirmar con el cliente.",
               "Cobras tarde porque no tienes claro quién debe qué."],
        incluye_h2="Qué incluye para tu negocio",
        incluye=[("Cotizaciones ordenadas", "Cada solicitud con su cotización y su estado."),
                 ("Visitas confirmadas", "Aviso por WhatsApp con fecha y hora de la visita."),
                 ("Seguimiento", "Recordatorio a quien no aprobó la cotización."),
                 ("Cobros por etapas", "Adelantos, avances y saldo final con recordatorios."),
                 ("Mantenimientos", "Aviso cuando le toca el próximo mantenimiento al cliente."),
                 ("Página web", "Para que te encuentren cuando buscan tu servicio en tu zona.")],
        pasos_h2="Cómo lo implementamos",
        faq_h2="Preguntas frecuentes para contratistas y técnicos",
        faq=[("¿Sirve para aire acondicionado, electricidad, plomería o remodelaciones?", "Sí. Se adapta a cualquier servicio que cotice y haga visitas."),
             ("¿Puedo usarlo desde el celular en la obra?", "Sí. Todo se consulta y se actualiza desde el teléfono."),
             ("¿Sirve si trabajo solo?", "Sí. Empiezas con lo básico y lo amplías si creces."),
             ("¿Cuánto cuesta?", "Te damos un precio cerrado después del diagnóstico gratis.")],
        servicio="Sistema para contratistas y servicios técnicos",
    ),
}
SECTORES = ["s_clinicas", "s_talleres", "s_mudanzas", "s_tiendas", "s_tecnicos"]
ORDEN = ["web", "crm", "cobros", "erp", "chatbot", "conectar", "wabapi", "api"]

PASOS = [("Diagnóstico gratis", "Vemos cómo te llegan los clientes hoy y qué te frena."),
         ("Propuesta clara", "Alcance, precio y tiempos por escrito antes de empezar."),
         ("Construcción por etapas", "Avances que pruebas en tu celular."),
         ("Acompañamiento", "Soporte y mejoras después de entregar.")]


def _head(P, d, ld):
    url = d + P["ruta"]
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{P["titulo"]}</title>
  <meta name="description" content="{P["meta"]}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#fbfbf8">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Enlaza Studio">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{P["titulo"]}">
  <meta property="og:description" content="{P["meta"]}">
  <meta property="og:locale" content="es_PA">
  <meta property="og:image" content="{d}img/compartir.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
  <link rel="manifest" href="../manifest.webmanifest">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{inicio.FUENTES}" rel="stylesheet">
  <link rel="stylesheet" href="../css/v3.css?v={inicio.V_CSS}">
</head>
'''


def _cabecera(wa):
    T = textos3.ES
    nav = "".join(f'<a href="../{h}">{t}</a>' for h, t in T["nav"])
    return f'''  <header class="cab" id="cab">
    <div class="cab__barra">
      <a class="marca" href="../" aria-label="Enlaza Studio, inicio">{inicio.MARCA}<span>Enlaza Studio</span></a>
      <nav class="cab__nav" id="menu" aria-label="Principal">
        {nav}
        <a class="btn btn--tinta btn--chico" href="{wa}" target="_blank" rel="noopener">{T["cta"]} {I["flecha"]}</a>
      </nav>
      <button class="cab__menu" id="hamburguesa" type="button" aria-label="{T["menu"]}" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
'''


def _pie(wa, actual):
    T = textos3.ES
    serv = "".join(f'<a href="../{PAGINAS[k]["ruta"]}"{" aria-current=\"page\"" if k == actual else ""}>{PAGINAS[k]["menu"]}</a>' for k in ORDEN)
    return f'''  <footer class="pie cierre">
    <div class="cont">
      <div class="pie__grid">
        <div class="pie__marca"><a class="marca" href="../">{inicio.MARCA}<span>Enlaza Studio</span></a><p>{T["eslogan"]}</p><p class="pie__desc">{T["pie"]["desc"]}</p></div>
        <nav aria-label="Servicios"><h2>Servicios</h2>{serv}</nav>
        <nav aria-label="Por tipo de negocio"><h2>Por tipo de negocio</h2>{"".join(f'<a href="../{PAGINAS[k]["ruta"]}">{PAGINAS[k]["menu"]}</a>' for k in SECTORES)}<a href="../privacidad/">Política de privacidad</a></nav>
        <div><h2>Contacto</h2><a class="pie__wa" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {inicio.TEL}</a><a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a><a href="../contacto/">Escríbenos por el formulario</a></div>
      </div>
      <p class="pie__gigante" aria-hidden="true">Enlaza Studio</p>
      <div class="pie__base"><span>© 2026 Enlaza Studio</span><span>Hecho en Panamá</span></div>
    </div>
  </footer>
'''


def _pagina(clave, cfg, wa_link):
    P = PAGINAS[clave]
    d = cfg["dominio"]
    url = d + P["ruta"]
    wa = wa_link(f"Hola Enlaza Studio, quiero información sobre {P['menu'].lower()}.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": P["servicio"], "serviceType": P["servicio"], "url": url, "description": P["meta"],
         "areaServed": {"@type": "Country", "name": "Panamá"},
         "provider": {"@type": "ProfessionalService", "@id": d + "#empresa", "name": "Enlaza Studio", "url": d, "telephone": "+" + cfg["whatsapp"]}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": d},
            {"@type": "ListItem", "position": 2, "name": P["menu"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faq"]]}]}

    dolor = "".join(f"<li>{I['check']}<span>{x}</span></li>" for x in P["dolor"])
    incluye = "".join(f'<article class="lp__item" data-revelar style="--rd:{j * .05:.2f}s"><h3>{t}</h3><p>{p}</p></article>' for j, (t, p) in enumerate(P["incluye"]))
    pasos = "".join(f'<li class="lp__paso"><span>0{j + 1}</span><h3>{t}</h3><p>{p}</p></li>' for j, (t, p) in enumerate(PASOS))
    faq = "".join(f'<details class="preg"><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in P["faq"])
    otros = "".join(f'<a class="lp__otro" href="../{PAGINAS[k]["ruta"]}"><b>{PAGINAS[k]["menu"]}</b><span>{PAGINAS[k]["h1"]}</span>{I["flecha"]}</a>'
                    for k in ORDEN if k != clave)
    vis = inicio._vis(P["vista"], textos3.ES)

    return (_head(P, d, ld) + '<body>\n  <a class="saltar" href="#contenido">Saltar al contenido</a>\n' + _cabecera(wa) + f'''
  <main id="contenido">
    <section class="lp-hero">
      <div class="cont lp-hero__grid">
        <div class="lp-hero__texto">
          <nav class="migas entra" aria-label="Ruta"><a href="../">Inicio</a><span aria-hidden="true">/</span><span aria-current="page">{P["menu"]}</span></nav>
          <p class="etq entra" style="--d:.04s">{P["etq"]}</p>
          <h1 class="entra" style="--d:.08s">{P["h1"]}</h1>
          <p class="lp-hero__lead entra" style="--d:.16s">{P["lead"]}</p>
          <div class="hero__botones lp-hero__botones entra" style="--d:.24s">
            <a class="btn btn--tinta btn--grande" href="{wa}" target="_blank" rel="noopener">{I["wa"]} Contáctanos</a>
            <a class="btn btn--claro btn--grande" href="#incluye">Qué incluye {I["flecha"]}</a>
          </div>
          <p class="hero__correo lp-hero__correo entra" style="--d:.28s">¿Prefieres correo? Escríbenos a <a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a></p>
        </div>
        <div class="lp-hero__vis activo entra" style="--d:.3s" aria-hidden="true">{vis}</div>
      </div>
    </section>

    <section class="sec sec--clara lp-dolor">
      <div class="cont lp-dolor__grid">
        <header class="encabezado" data-revelar><p class="etq">El problema</p><h2>{P["dolor_h2"]}</h2></header>
        <ul class="lp-dolor__lista" data-revelar>{dolor}</ul>
      </div>
    </section>

    <section class="sec lp-incluye" id="incluye">
      <div class="cont">
        <header class="encabezado" data-revelar><p class="etq">La solución</p><h2>{P["incluye_h2"]}</h2></header>
        <div class="lp__items">{incluye}</div>
      </div>
    </section>

    <section class="sec sec--oscura lp-pasos">
      <div class="cont">
        <header class="encabezado" data-revelar><p class="etq">Cómo trabajamos</p><h2>{P["pasos_h2"]}</h2></header>
        <ol class="lp__pasos" data-revelar>{pasos}</ol>
      </div>
    </section>

    <section class="sec sec--clara faq">
      <div class="cont faq__grid">
        <header class="encabezado" data-revelar><p class="etq">Preguntas frecuentes</p><h2>{P["faq_h2"]}</h2><p>Si tu duda no está aquí, escríbenos por WhatsApp o a <a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a>.</p></header>
        <div class="faq__lista" data-revelar>{faq}</div>
      </div>
    </section>

    <section class="sec sec--clara lp-otros">
      <div class="cont">
        <header class="encabezado" data-revelar><p class="etq">Más soluciones</p><h2>{"Servicios para tu negocio" if clave in SECTORES else "Otros servicios para tu negocio"}</h2></header>
        <div class="lp__otros" data-revelar>{otros}</div>
      </div>
    </section>

    <section class="final cierre">
      <canvas class="final__campo" id="campo-final" aria-hidden="true"></canvas>
      <div class="cont final__caja" data-revelar>
        <span class="final__marca">{inicio.MARCA}</span>
        <h2>Hablemos de tu negocio.</h2>
        <p>Cuéntanos cómo trabajas hoy y te decimos por dónde empezar, con precio claro.</p>
        <div class="final__botones"><a class="btn btn--verde btn--grande" href="{wa}" target="_blank" rel="noopener">{I["wa"]} Escríbenos por WhatsApp</a><a class="btn btn--claro btn--grande" href="mailto:hola@enlazastudio.com">✉ Escríbenos un correo</a></div>
      </div>
    </section>
  </main>

''' + _pie(wa, clave) + f'''  <script src="../js/v3.js?v={inicio.V_JS}" defer></script>
</body>
</html>
''')


def generar(raiz, cfg, wa_link):
    hechas = []
    for clave in ORDEN + SECTORES:
        carpeta = os.path.join(raiz, PAGINAS[clave]["ruta"])
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(_pagina(clave, cfg, wa_link))
        hechas.append(PAGINAS[clave]["ruta"])
    return hechas


# ---------------------------------------------------------------------------
# Privacidad (es/en) y 404 con el diseño 3.0 (antes usaban conektra.css)
# ---------------------------------------------------------------------------
def _head_doc(lang, pre, url, titulo, meta, noindex=False, alternos=(), ld=None):
    alt = "".join(f'\n  <link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternos)
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canon = f'\n  <link rel="canonical" href="{url}">' if url else ""
    ldjson = f'\n  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{titulo}</title>
  <meta name="description" content="{meta}">{canon}{alt}{robots}
  <meta name="theme-color" content="#fbfbf8">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="{pre}img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{inicio.FUENTES}" rel="stylesheet">
  <link rel="stylesheet" href="{pre}css/v3.css?v={inicio.V_CSS}">{ldjson}
</head>
'''


def _cab_doc(T, casa, wa):
    nav = "".join(f'<a href="{casa}{h}">{t}</a>' for h, t in T["nav"])
    etiqueta = "Principal" if T["lang"] == "es" else "Main"
    return f'''  <header class="cab" id="cab">
    <div class="cab__barra">
      <a class="marca" href="{casa}" aria-label="Enlaza Studio">{inicio.MARCA}<span>Enlaza Studio</span></a>
      <nav class="cab__nav" id="menu" aria-label="{etiqueta}">
        {nav}
        <a class="btn btn--tinta btn--chico" href="{wa}" target="_blank" rel="noopener">{T["cta"]} {I["flecha"]}</a>
      </nav>
      <button class="cab__menu" id="hamburguesa" type="button" aria-label="{T["menu"]}" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
'''


def _pie_doc(T, pre, casa, wa):
    es = T["lang"] == "es"
    if es:
        serv = "".join(f'<a href="{pre}{PAGINAS[k]["ruta"]}">{PAGINAS[k]["menu"]}</a>' for k in ORDEN)
    else:
        serv = "".join(f'<a href="{casa}#sol-{S["id"]}">{S["tag"]}</a>' for S in T["soluciones"])
    P = T["pie"]
    emp = "".join(f'<a href="{casa}{h}">{t}</a>' for h, t in T["nav"][1:])
    sect = "".join(f'<a href="{pre}{PAGINAS[k]["ruta"]}">{PAGINAS[k]["menu"]}</a>' for k in SECTORES)
    titulo_serv = "Servicios" if es else P["soluciones"]
    return f'''  <footer class="pie cierre">
    <div class="cont">
      <div class="pie__grid">
        <div class="pie__marca"><a class="marca" href="{casa}">{inicio.MARCA}<span>Enlaza Studio</span></a><p>{T["eslogan"]}</p><p class="pie__desc">{P["desc"]}</p></div>
        <nav aria-label="{titulo_serv}"><h2>{titulo_serv}</h2>{serv}</nav>
        <nav aria-label="Enlaza Studio"><h2>{"Por tipo de negocio" if es else "Enlaza Studio"}</h2>{sect if es else emp}</nav>
        <div><h2>{P["contacto"]}</h2><a class="pie__wa" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {inicio.TEL}</a><a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a></div>
      </div>
      <p class="pie__gigante" aria-hidden="true">Enlaza Studio</p>
      <div class="pie__base"><span>{P["derechos"]}</span><span>{P["hecho"]}</span></div>
    </div>
  </footer>
'''


def generar_extra(raiz, cfg, wa_link):
    import paginas
    d = cfg["dominio"]
    hechas = []
    for lang, T in (("es", textos3.ES), ("en", textos3.EN)):
        P = paginas.PRIVACIDAD[lang]
        ruta = paginas.RUTAS[lang]["privacidad"]
        pre = "../" * ruta.count("/")
        casa = pre + ("" if lang == "es" else "en/")
        wa = wa_link(T["wa_msg"])
        es = lang == "es"
        fecha = "Última actualización: 26 de noviembre de 2026" if es else "Last updated: November 26, 2026"
        correo = "Escríbenos por WhatsApp o a" if es else "Message us on WhatsApp or email"
        bloques = "".join(f'<section class="doc__bloque"><h2>{t}</h2><p>{x}</p></section>' for t, x in P["bloques"])
        alternos = (("es", d + paginas.RUTAS["es"]["privacidad"]), ("en", d + paginas.RUTAS["en"]["privacidad"]))
        html = (_head_doc(lang, pre, d + ruta, f'{P["titulo"]} | Enlaza Studio', P["meta"], alternos=alternos)
                + '<body>\n' + _cab_doc(T, casa, wa) + f'''
  <main id="contenido" class="doc">
    <div class="cont doc__cont">
      <nav class="migas" aria-label="{"Ruta" if es else "Breadcrumb"}"><a href="{casa}">{"Inicio" if es else "Home"}</a><span aria-hidden="true">/</span><span aria-current="page">{P["titulo"]}</span></nav>
      <p class="etq">Legal</p>
      <h1>{P["titulo"]}</h1>
      <p class="doc__fecha">{fecha}</p>
      {bloques}
      <section class="doc__bloque"><h2>{P["contacto"]}</h2><p>{correo} <a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a> · <a href="{wa}" target="_blank" rel="noopener">WhatsApp {inicio.TEL}</a></p></section>
    </div>
  </main>

''' + _pie_doc(T, pre, casa, wa) + f'''  <script src="{pre}js/v3.js?v={inicio.V_JS}" defer></script>
</body>
</html>
''')
        carpeta = os.path.join(raiz, ruta)
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        hechas.append(ruta)

    # 404: rutas absolutas porque GitHub Pages lo muestra en cualquier dirección
    T = textos3.ES
    wa = wa_link(T["wa_msg"])
    servicios = "".join(f'<a href="{d}{PAGINAS[k]["ruta"]}">{PAGINAS[k]["menu"]}</a>' for k in ORDEN)
    html = (_head_doc("es", d, "", "Página no encontrada | Enlaza Studio", "Esta página no existe o cambió de dirección.", noindex=True)
            + '<body>\n' + _cab_doc(T, d, wa) + f'''
  <main id="contenido" class="e404v">
    <canvas class="hero__campo" id="campo" aria-hidden="true"></canvas>
    <div class="cont e404v__caja">
      <span class="e404v__sim">{inicio.MARCA}</span>
      <p class="etq">Error 404</p>
      <h1>Este enlace <span class="degradado">se soltó.</span></h1>
      <p>La página que buscas no existe o cambió de dirección.<br><span lang="en">This page doesn't exist or has moved.</span></p>
      <div class="hero__botones">
        <a class="btn btn--tinta btn--grande" href="{d}">Ir al inicio {I["flecha"]}</a>
        <a class="btn btn--claro btn--grande" href="{d}en/" lang="en">Go to homepage {I["flecha"]}</a>
      </div>
      <p class="e404v__servicios">{servicios}</p>
    </div>
  </main>

''' + _pie_doc(T, d, d, wa) + f'''  <script src="{d}js/v3.js?v={inicio.V_JS}" defer></script>
</body>
</html>
''')
    with open(os.path.join(raiz, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return hechas + ["404.html"]



# ---------------------------------------------------------------------------
# Cómo trabajamos, Preguntas y Contacto en páginas propias (antes estaban en la portada)
# ---------------------------------------------------------------------------
SECCIONES = {
    "es": [("como-trabajamos/", "Cómo trabajamos | Enlaza Studio", "Cómo trabajamos en Enlaza Studio: diagnóstico, propuesta con precio claro, construcción por etapas y acompañamiento. Proyecto cerrado o plan mensual.", "proceso"),
           ("preguntas/", "Preguntas frecuentes | Enlaza Studio", "Preguntas frecuentes sobre páginas web, CRM, cobranza y automatización de WhatsApp para negocios en Panamá.", "preguntas"),
           ("contacto/", "Contacto | Enlaza Studio", "Escríbenos por el formulario, por WhatsApp o a hola@enlazastudio.com. Te respondemos y te proponemos por dónde empezar.", "contacto")],
    "en": [("en/how-we-work/", "How we work | Enlaza Studio", "How Enlaza Studio works: diagnosis, a clear proposal, building in stages and ongoing support. Fixed project or monthly plan.", "proceso"),
           ("en/faq/", "FAQ | Enlaza Studio", "Frequently asked questions about websites, CRM, payment reminders and WhatsApp automation for businesses in Panama.", "preguntas"),
           ("en/contact/", "Contact | Enlaza Studio", "Write to us through the form, on WhatsApp or at hola@enlazastudio.com. We'll reply and suggest where to start.", "contacto")],
}


def generar_secciones(raiz, cfg, wa_link):
    import paginas
    d = cfg["dominio"]
    hechas = []
    for lang, T in (("es", textos3.ES), ("en", textos3.EN)):
        otro = "en" if lang == "es" else "es"
        wa = wa_link(T["wa_msg"])
        for j, (ruta, titulo, meta, cual) in enumerate(SECCIONES[lang]):
            pre = "../" * ruta.count("/")
            casa = pre + ("" if lang == "es" else "en/")
            alternos = ((lang, d + ruta), (otro, d + SECCIONES[otro][j][0]))
            ld = None
            extra = ""
            if cual == "proceso":
                cuerpo = inicio._proceso(T)
            elif cual == "preguntas":
                cuerpo = inicio._preguntas(T)
                ld = {"@context": "https://schema.org", "@type": "FAQPage",
                      "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faqs"]]}
            else:
                privacidad = pre + paginas.RUTAS[lang]["privacidad"]
                cuerpo = inicio._contacto(T, wa, privacidad)
                F = T["form"]
                form_cfg = json.dumps({"crm": cfg["crm"], "wa": cfg["whatsapp"], "lang": lang, "enviando": F["enviando"], "enviar": F["enviar"], "error": F["error"]},
                                      ensure_ascii=False).replace("</", "<\\/")
                extra = f"  <script>window.CONEKTRA_FORM = {form_cfg};</script>\n"
            html = (_head_doc(lang, pre, d + ruta, titulo, meta, alternos=alternos, ld=ld)
                    + '<body>\n' + _cab_doc(T, casa, wa)
                    + f'  <main id="contenido" class="pagina-seccion">\n{cuerpo}  </main>\n\n'
                    + _pie_doc(T, pre, casa, wa) + extra
                    + f'  <script src="{pre}js/v3.js?v={inicio.V_JS}" defer></script>\n</body>\n</html>\n')
            carpeta = os.path.join(raiz, ruta)
            os.makedirs(carpeta, exist_ok=True)
            with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
            hechas.append(ruta)
    return hechas
