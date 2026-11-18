"""Páginas internas de Conektra: servicios, caso Acarreos Makena, privacidad, 404, sitemap y robots.

Se generan desde build.py y comparten el menú y el pie de marco.py.
"""
import os, urllib.parse
import servicios
import marco

RUTAS = {
    "es": {"inicio": "", "web": "servicios/paginas-web/", "crm": "servicios/crm/", "api": "servicios/integraciones-api/",
           "erp": "servicios/erp-automatizacion/", "caso": "casos/acarreos-makena/", "privacidad": "privacidad/"},
    "en": {"inicio": "en/", "web": "en/services/websites/", "crm": "en/services/crm/", "api": "en/services/api-integrations/",
           "erp": "en/services/erp-automation/", "caso": "en/cases/acarreos-makena/", "privacidad": "en/privacy/"},
}
ORDEN_SERVICIOS = ["web", "crm", "api", "erp"]
FECHA = "2026-11-17"

UI = {
    "es": dict(inicio="Inicio", servicios="Servicios", casos="Casos de éxito", resuelve="Lo que resuelve", incluye="Qué incluye",
               ideal="Es para ti si…", como="Cómo trabajamos", faq="Preguntas frecuentes", otros="Otros servicios",
               demo="Así se ve", cta_h="¿Hablamos de tu negocio?", cta_p="Cuéntanos cómo trabajas hoy y te proponemos por dónde empezar.",
               cta_form="Escríbenos por el formulario", wa_msg="Hola Conektra, quiero información sobre ", ver_incluye="Qué incluye",
               pasos=[("Diagnóstico", "Vemos cómo trabajas hoy."), ("Propuesta", "Alcance, precio y tiempos claros."),
                      ("Desarrollo", "Por etapas, con avances que pruebas."), ("Soporte", "Cambios y mejoras después de entregar.")]),
    "en": dict(inicio="Home", servicios="Services", casos="Success stories", resuelve="What it solves", incluye="What's included",
               ideal="It's for you if…", como="How we work", faq="FAQ", otros="Other services",
               demo="What it looks like", cta_h="Shall we talk about your business?", cta_p="Tell us how you work today and we'll propose where to start.",
               cta_form="Write to us through the form", wa_msg="Hi Conektra, I'd like information about ", ver_incluye="What's included",
               pasos=[("Discovery", "We look at how you work today."), ("Proposal", "Clear scope, price and timeline."),
                      ("Build", "In stages, with progress you can test."), ("Support", "Changes and improvements after launch.")]),
}

SERVICIOS = {
    "es": {
        "web": dict(titulo="Páginas web y SEO", letra="A", familia="Presencia digital",
                    meta="Páginas web para pequeños negocios de Panamá: rápidas en el celular, con páginas por servicio y por zona para aparecer en Google, y formulario conectado a tu hoja.",
                    h1='Una página que <em>te trae clientes.</em>',
                    lead="Diseñamos tu página desde cero, con tu marca. Rápida en el celular, con una página para cada servicio y cada zona donde trabajas, y un botón directo a tu WhatsApp.",
                    problema=["Te buscan en Google y aparecen otros negocios.", "Tu Instagram no explica bien qué haces ni dónde trabajas.", "Respondes las mismas preguntas una y otra vez por chat."],
                    solucion="Tu página explica tus servicios, muestra tus zonas y recibe solicitudes de cotización a cualquier hora.",
                    incluye=[("Diseño a la medida", "Nada de plantillas: tu marca, tus colores y tu forma de hablarle a tus clientes."),
                             ("Rápida en el celular", "Hecha para cargar rápido en cualquier teléfono, donde está la mayoría de tus clientes."),
                             ("Páginas por servicio", "Una página para cada cosa que haces: mudanzas, acarreos, instalaciones…"),
                             ("Páginas por zona", "Para aparecer cuando buscan tu servicio en tu ciudad o tu barrio."),
                             ("Formulario de cotización", "Pide los datos que necesitas y llega a tu hoja de Google Sheets."),
                             ("Google listo", "Títulos, descripciones, sitemap y Search Console configurados.")],
                    ideal=["Tu negocio no tiene página o la que tiene no te trae clientes.", "Quieres aparecer en Google cuando buscan lo que haces.", "Recibes clientes por WhatsApp y quieres ordenarlos."],
                    faq=[("¿Cuánto tarda una página web?", "Depende de cuántas páginas y funciones lleve. Te damos el tiempo exacto en la propuesta, antes de empezar."),
                         ("¿Puedo pedir cambios después?", "Sí. Te explicamos cómo funciona y nos encargamos de los cambios cuando los necesites."),
                         ("¿Me garantizan el primer lugar en Google?", "Nadie puede garantizarlo con honestidad. Dejamos tu página técnicamente lista y con páginas pensadas para lo que buscan tus clientes.")]),
        "crm": dict(titulo="CRM a la medida", letra="B", familia="Gestión de clientes",
                    meta="CRM sencillo para pequeños negocios: cada solicitud entra sola, avanza por etapas y tienes recordatorios y reportes para no perder clientes.",
                    h1='Todos tus clientes, <em>en un solo lugar.</em>',
                    lead="Un CRM hecho con tus propias etapas: cada solicitud entra sola desde tu página o WhatsApp, sabes en qué va cada cliente y a quién te falta responder.",
                    problema=["Tus clientes están repartidos entre chats, libretas y hojas sueltas.", "Se te olvidan seguimientos y pierdes trabajos.", "No sabes cuántas cotizaciones cierras al mes."],
                    solucion="Cada solicitud queda guardada con su etapa, sus datos y un recordatorio, y ves cuánto entra y cuánto cierras.",
                    incluye=[("Etapas a tu manera", "Nuevo, contactado, cotizado, ganado… las etapas que de verdad usa tu negocio."),
                             ("Entrada automática", "Las solicitudes de tu página llegan solas, con todos sus datos."),
                             ("Recordatorios", "Seguimientos para que ningún cliente se quede sin respuesta."),
                             ("Reportes simples", "Cuántas solicitudes entran, cuántas cierras y cuánto vendes."),
                             ("Fácil de usar", "Podemos construirlo sobre Google Sheets, que tu equipo ya conoce."),
                             ("Crece contigo", "Agregamos campos, etapas y conexiones cuando lo necesites.")],
                    ideal=["Atiendes muchas cotizaciones por WhatsApp.", "Más de una persona responde a los clientes.", "Quieres saber cuánto vendes sin hacer cuentas a mano."],
                    faq=[("¿Necesito pagar una licencia de CRM?", "No necesariamente. Según tu caso podemos usar Google Sheets o conectar un CRM del mercado."),
                         ("¿Mi equipo podrá usarlo sin una capacitación larga?", "Esa es la idea: lo diseñamos con tus etapas y tus palabras, y te acompañamos al principio."),
                         ("¿Se conecta con mi página web?", "Sí. El formulario de tu página puede enviar cada solicitud directo al CRM.")]),
        "api": dict(titulo="Integraciones API", letra="C", familia="Automatización y conexiones",
                    meta="Conectamos tu página, WhatsApp, Google Sheets y otras herramientas para que la información llegue sola a donde tiene que llegar, sin copiar y pegar.",
                    h1='Tus herramientas, <em>hablando entre sí.</em>',
                    lead="Conectamos tu página, tu hoja, WhatsApp y otras herramientas para que la información llegue sola a donde tiene que llegar, sin copiar y pegar.",
                    problema=["Copias datos a mano de un lado a otro todos los días.", "Usas varias herramientas que no se comunican.", "Te enteras tarde de las solicitudes nuevas."],
                    solucion="Cada dato se escribe una sola vez y llega a donde se necesita: tu hoja, tu CRM o tu WhatsApp.",
                    incluye=[("Formularios conectados", "Cada solicitud de tu página llega a tu hoja o a tu CRM."),
                             ("Avisos automáticos", "Tu equipo se entera al momento de cada solicitud nueva."),
                             ("Conexiones por API", "Usamos las APIs y webhooks de las herramientas que ya usas."),
                             ("Sin doble digitación", "Los datos se escriben una vez y llegan a todos lados."),
                             ("Registros y alertas", "Si una conexión falla, queda registrada para corregirla."),
                             ("Documentación", "Te entregamos cómo funciona cada conexión.")],
                    ideal=["Pasas datos de un sistema a otro a mano.", "Quieres avisos automáticos de cada solicitud.", "Necesitas conectar una herramienta específica, como una pasarela de pago."],
                    faq=[("¿Pueden conectar cualquier herramienta?", "Casi cualquiera que tenga API o permita exportar e importar datos. Lo revisamos y lo probamos antes de comprometernos."),
                         ("¿Qué pasa si una conexión falla?", "Dejamos registros para detectarlo rápido y te damos soporte para corregirlo."),
                         ("¿Pueden conectar Yappy, Tilopay o PágueloFácil?", "Se evalúa según el proyecto: revisamos qué permite cada servicio y lo validamos contigo antes de prometerlo.")]),
        "erp": dict(titulo="ERP y automatizaciones", letra="C+", familia="Para cuando crezcas",
                    meta="Inventario, compras, facturación y procesos internos conectados para negocios que necesitan más control de su operación.",
                    h1='Más control <em>cuando tu negocio crece.</em>',
                    lead="Cuando ya tienes inventario, compras y facturas que controlar, conectamos esos procesos para que se actualicen solos y veas cómo va tu negocio sin esperar a fin de mes.",
                    problema=["Llevas el inventario o la facturación en hojas sueltas.", "Pierdes horas en tareas repetitivas cada semana.", "No sabes cómo va el mes hasta que haces cuentas."],
                    solucion="Ventas, inventario, compras y facturas conectados, con tableros simples para decidir con datos.",
                    incluye=[("Ventas e inventario", "Cada venta descuenta del inventario y te avisa antes de quedarte sin producto."),
                             ("Compras", "Órdenes de compra cuando el inventario baja de lo que tú definas."),
                             ("Facturación", "Facturas a partir de cada venta, sin volver a escribir los datos."),
                             ("Tareas automáticas", "Reportes y recordatorios que se hacen solos."),
                             ("Tableros", "Ventas, gastos e inventario en una sola pantalla."),
                             ("ERP del mercado o a la medida", "Conectamos el sistema que ya tienes o construimos lo que falta.")],
                    ideal=["Ya vendes productos o materiales además de servicios.", "Tu operación creció y las hojas sueltas ya no alcanzan.", "Quieres ver tus números sin esperar a fin de mes."],
                    faq=[("¿Tengo que cambiar mi sistema actual?", "No necesariamente. Muchas veces lo conectamos y automatizamos lo que ya tienes."),
                         ("¿Necesito esto desde el principio?", "Casi nunca. Es para cuando el negocio crece; muchos empiezan con su página y su CRM."),
                         ("¿Cómo empiezo?", "Con un diagnóstico de tus procesos. A partir de ahí te proponemos qué conectar primero.")]),
    },
    "en": {
        "web": dict(titulo="Websites and SEO", letra="A", familia="Online presence",
                    meta="Websites for small businesses in Panama: fast on mobile, with pages per service and area to show up on Google, and a form connected to your sheet.",
                    h1='A website that <em>brings you customers.</em>',
                    lead="We design your website from scratch, with your brand. Fast on mobile, with a page for every service and every area you cover, and a direct button to your WhatsApp.",
                    problema=["People search on Google and other businesses show up.", "Your Instagram doesn't clearly explain what you do or where.", "You answer the same questions over and over in chat."],
                    solucion="Your website explains your services, shows your areas and takes quote requests at any hour.",
                    incluye=[("Custom design", "No templates: your brand, your colors and your way of talking to customers."),
                             ("Fast on mobile", "Built to load quickly on any phone, where most of your customers are."),
                             ("Pages per service", "A page for each thing you do: moving, hauling, installations…"),
                             ("Pages per area", "To show up when people search for your service in your city or neighborhood."),
                             ("Quote form", "Asks for what you need and lands in your Google Sheets spreadsheet."),
                             ("Google ready", "Titles, descriptions, sitemap and Search Console set up.")],
                    ideal=["Your business has no website, or the one you have brings no customers.", "You want to show up on Google when people search for what you do.", "You get customers on WhatsApp and want to organize them."],
                    faq=[("How long does a website take?", "It depends on the number of pages and features. We give you the exact timeline in the proposal, before we start."),
                         ("Can I ask for changes later?", "Yes. We show you how it works and take care of changes whenever you need them."),
                         ("Do you guarantee first place on Google?", "No one can honestly guarantee that. We leave your website technically ready, with pages built for what your customers search for.")]),
        "crm": dict(titulo="Custom CRM", letra="B", familia="Customer management",
                    meta="A simple CRM for small businesses: every request comes in automatically, moves through stages, and you get reminders and reports so no customer slips away.",
                    h1='All your customers, <em>in one place.</em>',
                    lead="A CRM built with your own stages: every request comes in automatically from your website or WhatsApp, and you know where each customer stands and who's still waiting.",
                    problema=["Your customers are scattered across chats, notebooks and loose spreadsheets.", "Follow-ups slip and you lose jobs.", "You don't know how many quotes you close each month."],
                    solucion="Every request is saved with its stage, its details and a reminder, and you see what comes in and what you close.",
                    incluye=[("Stages your way", "New, contacted, quoted, won… the stages your business actually uses."),
                             ("Automatic intake", "Requests from your website arrive on their own, with all their details."),
                             ("Reminders", "Follow-ups so no customer is left without an answer."),
                             ("Simple reports", "How many requests come in, how many you close and how much you sell."),
                             ("Easy to use", "We can build it on Google Sheets, which your team already knows."),
                             ("Grows with you", "We add fields, stages and connections when you need them.")],
                    ideal=["You handle lots of quote requests on WhatsApp.", "More than one person answers customers.", "You want to know how much you sell without doing the math by hand."],
                    faq=[("Do I need to pay for a CRM license?", "Not necessarily. Depending on your case we can use Google Sheets or connect an off-the-shelf CRM."),
                         ("Can my team use it without long training?", "That's the idea: we design it with your stages and your words, and support you at the start."),
                         ("Does it connect to my website?", "Yes. Your website form can send every request straight to the CRM.")]),
        "api": dict(titulo="API integrations", letra="C", familia="Automation and connections",
                    meta="We connect your website, WhatsApp, Google Sheets and other tools so information gets where it needs to go on its own, with no copy and paste.",
                    h1='Your tools, <em>talking to each other.</em>',
                    lead="We connect your website, your sheet, WhatsApp and other tools so information gets where it needs to go on its own, with no copy and paste.",
                    problema=["You copy data by hand from one place to another every day.", "You use several tools that don't talk to each other.", "You find out about new requests too late."],
                    solucion="Every piece of data is typed once and reaches where it's needed: your sheet, your CRM or your WhatsApp.",
                    incluye=[("Connected forms", "Every request from your website lands in your sheet or CRM."),
                             ("Automatic alerts", "Your team hears about every new request right away."),
                             ("API connections", "We use the APIs and webhooks of the tools you already use."),
                             ("No double entry", "Data is typed once and reaches everywhere."),
                             ("Logs and alerts", "If a connection fails, it's logged so it can be fixed."),
                             ("Documentation", "We hand over how each connection works.")],
                    ideal=["You move data between systems by hand.", "You want automatic alerts for every request.", "You need to connect a specific tool, like a payment gateway."],
                    faq=[("Can you connect any tool?", "Almost any tool with an API or that allows data export and import. We review and test it before committing."),
                         ("What if a connection fails?", "We keep logs to catch it quickly and support you to fix it."),
                         ("Can you connect Yappy, Tilopay or PágueloFácil?", "It's evaluated per project: we check what each service allows and validate it with you before promising it.")]),
        "erp": dict(titulo="ERP and automation", letra="C+", familia="For when you grow",
                    meta="Connected inventory, purchasing, invoicing and internal processes for businesses that need more control over their operations.",
                    h1='More control <em>as your business grows.</em>',
                    lead="When you have inventory, purchases and invoices to keep track of, we connect those processes so they update themselves and you can see how the business is doing without waiting for month-end.",
                    problema=["You track inventory or invoicing in loose spreadsheets.", "You lose hours on repetitive tasks every week.", "You don't know how the month went until you do the math."],
                    solucion="Sales, inventory, purchasing and invoices connected, with simple dashboards to decide with data.",
                    incluye=[("Sales and inventory", "Every sale deducts stock and warns you before you run out."),
                             ("Purchasing", "Purchase orders when stock drops below what you define."),
                             ("Invoicing", "Invoices from each sale, without retyping data."),
                             ("Automated tasks", "Reports and reminders that run on their own."),
                             ("Dashboards", "Sales, expenses and inventory on a single screen."),
                             ("Off-the-shelf or custom ERP", "We connect the system you have or build what's missing.")],
                    ideal=["You sell products or materials in addition to services.", "Your operation grew and loose spreadsheets no longer cut it.", "You want to see your numbers without waiting for month-end."],
                    faq=[("Do I have to replace my current system?", "Not necessarily. We often connect and automate what you already have."),
                         ("Do I need this from day one?", "Rarely. It's for when the business grows; many start with their website and CRM."),
                         ("How do I start?", "With a review of your processes. From there we propose what to connect first.")]),
    },
}

CASO = {
    "es": dict(titulo="Caso de éxito: Acarreos Makena", meta="Cómo Acarreos Makena pasó de atender clientes por WhatsApp sueltos a tener página web, páginas por servicio y zona, cotizaciones en Google Sheets y reseñas.",
               etiqueta="Caso de éxito", h1='Acarreos Makena: <em>del WhatsApp suelto</em> a un negocio conectado.', sector="Mudanzas, acarreos y fletes · Panamá",
               reto_t="El reto", reto=["Los clientes llegaban solo por WhatsApp y las cotizaciones quedaban repartidas entre chats.", "No había una página propia que apareciera en Google al buscar sus servicios.", "No había forma de mostrar opiniones de clientes ni de medir cuántas cotizaciones llegaban."],
               hicimos_t="Lo que hicimos",
               hicimos=[("Página web con dominio propio", "Diseño a la medida de la marca, rápida en celular, con botón directo a WhatsApp y formulario de cotización."),
                        ("Páginas por servicio y por zona", "Páginas para mudanzas, acarreos, escombros, montaje de eventos y oficinas, y por zonas como San Miguelito, Panamá Oeste y Chiriquí. Sitemap y Search Console configurados."),
                        ("Cotizaciones en Google Sheets", "Cada cotización del formulario se guarda en una hoja con su estado: nuevo, contactado, cotizado, agendado, ganado o perdido. Con resumen automático."),
                        ("Reseñas con aprobación", "Los clientes califican con estrellas y dejan su comentario; el dueño decide cuáles se publican.")],
               entregado_t="Lo que quedó funcionando",
               entregado=["Página web publicada en acarreosmakena.com", "10 páginas pensadas para búsquedas en Google", "Formulario de cotización conectado a Google Sheets y a WhatsApp", "Reseñas con estrellas y aprobación del dueño", "Sitemap enviado a Google Search Console"],
               herramientas_t="Herramientas", herramientas=["HTML, CSS y JavaScript", "GitHub Pages", "Google Sheets", "Google Apps Script", "Google Search Console", "WhatsApp"],
               ver="Ver la página en vivo", cta_h="¿Quieres algo así para tu negocio?", cta_p="Cada proyecto es distinto: lo diseñamos a la medida de tu marca y tu forma de trabajar."),
    "en": dict(titulo="Success story: Acarreos Makena", meta="How Acarreos Makena went from scattered WhatsApp chats to a website, pages per service and area, quotes in Google Sheets and reviews.",
               etiqueta="Success story", h1='Acarreos Makena: <em>from scattered WhatsApp chats</em> to a connected business.', sector="Moving, hauling and freight · Panama",
               reto_t="The challenge", reto=["Customers only came in through WhatsApp, and quotes were scattered across chats.", "There was no website showing up on Google when people searched for their services.", "There was no way to show customer reviews or measure how many quote requests came in."],
               hicimos_t="What we did",
               hicimos=[("Website on its own domain", "Custom design for the brand, fast on mobile, with a direct WhatsApp button and a quote form."),
                        ("Pages per service and area", "Pages for moving, hauling, debris removal, event and office setup, plus areas like San Miguelito, Panamá Oeste and Chiriquí. Sitemap and Search Console set up."),
                        ("Quotes in Google Sheets", "Every quote request from the form is saved to a sheet with its status: new, contacted, quoted, scheduled, won or lost. With an automatic summary."),
                        ("Reviews with approval", "Customers rate with stars and leave a comment; the owner decides which ones get published.")],
               entregado_t="What's up and running",
               entregado=["Website live at acarreosmakena.com", "10 pages built for Google searches", "Quote form connected to Google Sheets and WhatsApp", "Star reviews with owner approval", "Sitemap submitted to Google Search Console"],
               herramientas_t="Tools", herramientas=["HTML, CSS and JavaScript", "GitHub Pages", "Google Sheets", "Google Apps Script", "Google Search Console", "WhatsApp"],
               ver="See the live website", cta_h="Want something like this for your business?", cta_p="Every project is different: we design it around your brand and the way you work."),
}

PRIVACIDAD = {
    "es": dict(titulo="Política de privacidad", meta="Cómo Conektra usa los datos que nos envías por el formulario de contacto o por WhatsApp.", fecha="Última actualización: 17 de noviembre de 2026",
               bloques=[("Qué datos recogemos", "Solo los que tú nos envías por el formulario de contacto: tu nombre, el nombre de tu negocio, tu WhatsApp, tu correo si decides darlo, qué necesitas, tu presupuesto aproximado si lo indicas y tu mensaje. Si nos escribes por WhatsApp, también tu número y lo que nos cuentes."),
                        ("Para qué los usamos", "Únicamente para responderte, preparar una propuesta y dar seguimiento a tu solicitud. No los vendemos ni los compartimos con terceros para publicidad."),
                        ("Dónde se guardan", "Los mensajes del formulario se guardan en una hoja de cálculo privada de Google a la que solo tiene acceso Conektra."),
                        ("Servicios de terceros", "La página se aloja en GitHub Pages y usa fuentes de Google Fonts; estos servicios pueden registrar datos técnicos de la visita, como la dirección IP, según sus propias políticas. No usamos cookies de publicidad ni herramientas de seguimiento."),
                        ("Tus derechos", "Puedes pedirnos en cualquier momento que te digamos qué datos tenemos tuyos, que los corrijamos o que los borremos. Escríbenos por WhatsApp y lo hacemos.")],
               contacto="Contacto"),
    "en": dict(titulo="Privacy policy", meta="How Conektra uses the information you send us through the contact form or WhatsApp.", fecha="Last updated: November 17, 2026",
               bloques=[("What we collect", "Only what you send us through the contact form: your name, your business name, your WhatsApp, your email if you choose to share it, what you need, your approximate budget if you give one and your message. If you message us on WhatsApp, also your number and what you tell us."),
                        ("How we use it", "Only to reply to you, prepare a proposal and follow up on your request. We don't sell it or share it with third parties for advertising."),
                        ("Where it's stored", "Form messages are stored in a private Google spreadsheet that only Conektra can access."),
                        ("Third-party services", "The site is hosted on GitHub Pages and uses Google Fonts; these services may log technical visit data, such as your IP address, under their own policies. We don't use advertising cookies or tracking tools."),
                        ("Your rights", "You can ask us at any time what information we have about you, to correct it or to delete it. Message us on WhatsApp and we'll take care of it.")],
               contacto="Contact"),
}


def prefijo(ruta):
    """Cuántos niveles subir desde una ruta como 'servicios/crm/' hasta la raíz."""
    return "../" * ruta.count("/")


def demo_extra(clave, lang, I):
    """Demostración específica de cada servicio, además de su maqueta principal."""
    es = lang == "es"
    if clave == "web":
        res = [("tunegocio.com › mudanzas-en-panama", "Mudanzas en Panamá | Tu negocio" if es else "Movers in Panama | Your business", "Cotiza por WhatsApp. Camiones y personal propio." if es else "Get a quote on WhatsApp. Own trucks and crew.", True),
               ("tunegocio.com › mudanzas-san-miguelito", "Mudanzas en San Miguelito | Tu negocio" if es else "Movers in San Miguelito | Your business", "Servicio en San Miguelito y alrededores." if es else "Service in San Miguelito and nearby.", False)]
        filas = "".join(f'<div class="demo-serp__res{" demo-serp__res--tuyo" if t else ""}"><small>{u}</small><b>{h}</b><span>{d}</span></div>' for u, h, d, t in res)
        return f'<div class="demo demo-serp"><span class="demo-serp__barra">{I["lupa"]}{"mudanzas en panamá" if es else "movers in panama"}</span>{filas}</div>'
    if clave == "crm":
        etapas = [("Nuevo" if es else "New", 4), ("Contactado" if es else "Contacted", 3), ("Cotizado" if es else "Quoted", 3), ("Ganado" if es else "Won", 2)]
        barras = "".join(f'<li><span>{n}</span><i style="--v:{v * 22}%"></i><b>{v}</b></li>' for n, v in etapas)
        return f'<div class="demo demo-etapas"><p>{"Solicitudes por etapa · ejemplo" if es else "Requests by stage · example"}</p><ul>{barras}</ul></div>'
    if clave == "api":
        izq = ["Formulario web" if es else "Website form", "WhatsApp"]
        der = ["Google Sheets", "CRM", "Gmail"]
        nodo = lambda t: f'<span class="demo-red__nodo">{t}</span>'
        return (f'<div class="demo demo-red"><div class="demo-red__col">{"".join(nodo(t) for t in izq)}</div>'
                f'<div class="demo-red__centro"><i></i><b>Conektra</b><i></i></div><div class="demo-red__col">{"".join(nodo(t) for t in der)}</div></div>')
    filas = [("Cajas medianas" if es else "Medium boxes", "38", "OK"), ("Cinta de embalar" if es else "Packing tape", "6", "Comprar" if es else "Reorder"), ("Plástico burbuja" if es else "Bubble wrap", "12", "OK")]
    tabla = "".join(f'<div><span>{a}</span><b>{b}</b><em class="{"bajo" if c not in ("OK",) else ""}">{c}</em></div>' for a, b, c in filas)
    return f'<div class="demo demo-inventario"><p>{"Inventario y compras · ejemplo" if es else "Inventory and purchasing · example"}</p>{tabla}</div>'


def migas(ui, inicio, partes):
    items = [f'<a href="{inicio}">{ui["inicio"]}</a>'] + [f'<a href="{h}">{t}</a>' if h else f'<span aria-current="page">{t}</span>' for t, h in partes]
    return '<nav class="migas" aria-label="Ruta">' + '<span class="migas__sep">/</span>'.join(items) + '</nav>'


def banda_cta(ui, I, inicio, wa, wa_attr, h=None, p=None):
    return f'''    <section class="seccion seccion--sin-arriba">
      <div class="contenedor"><div class="banda" data-revelar>
        <div><h2>{h or ui["cta_h"]}</h2><p>{p or ui["cta_p"]}</p></div>
        <div class="banda__botones"><a class="boton boton--menta" href="{wa}"{wa_attr}>{I["wa"]} WhatsApp</a><a class="boton boton--linea" href="{inicio}#contacto">{ui["cta_form"]} <span class="boton__flecha">{I["flecha"]}</span></a></div>
      </div></div>
    </section>
'''


def generar(raiz, cfg, I, LOGO):
    escritas = []
    d = cfg["dominio"]

    def escribir(ruta, html):
        destino = os.path.join(raiz, ruta, "index.html")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        escritas.append(ruta)

    def marco_pagina(lang, ruta, ruta_otra, titulo, meta, ld, wa, cuerpo):
        pre = prefijo(ruta)
        inicio = pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")
        otra = pre + (ruta_otra or "./")
        wa_attr = ' target="_blank" rel="noopener"'
        alternos = [(lang, d + ruta), ("en" if lang == "es" else "es", d + ruta_otra)]
        imagen = d + "img/" + ("compartir.jpg" if lang == "es" else "compartir-en.jpg")
        ld_todo = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": titulo, "url": d + ruta, "description": meta, "inLanguage": lang,
                                                               "isPartOf": {"@id": d + "#empresa"}}] + ld}
        serv = [(SERVICIOS[lang][k]["titulo"], pre + RUTAS[lang][k]) for k in ORDEN_SERVICIOS]
        return (marco.head(lang, pre, f"{titulo} | Conektra", meta, d + ruta, alternos, imagen, ld_todo)
                + '<body class="interna">\n'
                + marco.cabecera(lang, inicio, otra, wa, wa_attr, I, LOGO)
                + cuerpo(pre, inicio, wa, wa_attr)
                + marco.pie(lang, pre, inicio, otra, wa, wa_attr, I, LOGO, serv, pre + RUTAS[lang]["privacidad"])
                + f'  <script src="{pre}js/main.js?v={marco.V_JS}" defer></script>\n</body>\n</html>\n')

    for lang in ("es", "en"):
        otro = "en" if lang == "es" else "es"
        ui = UI[lang]
        maquetas = servicios.seccion(lang, I, solo_maquetas=True)

        # ---------- servicios ----------
        for n, clave in enumerate(ORDEN_SERVICIOS):
            S = SERVICIOS[lang][clave]
            ruta, ruta_otra = RUTAS[lang][clave], RUTAS[otro][clave]
            wa = f'https://wa.me/{cfg["whatsapp"]}?text={urllib.parse.quote(ui["wa_msg"] + S["titulo"])}'
            ld = [{"@type": "Service", "name": S["titulo"], "description": S["meta"], "provider": {"@id": d + "#empresa"}, "areaServed": {"@type": "Country", "name": "Panamá"}},
                  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in S["faq"]]},
                  {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": ui["inicio"], "item": d + RUTAS[lang]["inicio"]},
                                                                  {"@type": "ListItem", "position": 2, "name": S["titulo"], "item": d + ruta}]}]

            def cuerpo(pre, inicio, wa, wa_attr, S=S, n=n, clave=clave):
                incluye = "".join(f'<li class="beneficio" data-revelar style="transition-delay:{j * .05:.2f}s"><span class="beneficio__ico">{I["check"]}</span><h3>{t}</h3><p>{x}</p></li>' for j, (t, x) in enumerate(S["incluye"]))
                ideal = "".join(f'<li>{I["check"]}{x}</li>' for x in S["ideal"])
                problema = "".join(f'<li><i>{I["mas"]}</i>{x}</li>' for x in S["problema"])
                pasos = "".join(f'<li><b>0{j + 1}</b><h3>{t}</h3><p>{x}</p></li>' for j, (t, x) in enumerate(ui["pasos"]))
                faqs = "".join(f'<details class="pregunta"><summary>{q}</summary><p>{a}</p></details>' for q, a in S["faq"])
                otros = "".join(f'<a class="otro" href="{pre}{RUTAS[lang][k]}"><small>{SERVICIOS[lang][k]["familia"]}</small><span>{SERVICIOS[lang][k]["titulo"]}</span>{I["flecha"]}</a>' for k in ORDEN_SERVICIOS if k != clave)
                return f'''
  <main>
    <section class="hero hero--interna">
      <div class="hero__ambiente" aria-hidden="true"><span></span><span></span><span></span><i></i></div>
      <div class="contenedor hero__grid hero__grid--interna">
        <div class="hero__texto">
          {migas(ui, inicio, [(ui["servicios"], inicio + "#servicios"), (S["titulo"], None)])}
          <p class="sello"><span class="sello__letra">{S["letra"]}</span>{S["familia"]}</p>
          <h1 class="titular titular--interna">{S["h1"]}</h1>
          <p class="hero__lead">{S["lead"]}</p>
          <div class="hero__botones"><a class="boton boton--menta" href="{wa}"{wa_attr}>{I["wa"]} {marco.UI[lang]["cta"]}</a><a class="boton boton--linea" href="#incluye">{ui["ver_incluye"]} <span class="boton__flecha">{I["flecha"]}</span></a></div>
        </div>
        <div class="maqueta maqueta--hero" aria-hidden="true"><div class="maqueta__rejilla"></div><div class="panel activo">{maquetas[n]}</div></div>
      </div>
    </section>

    <section class="seccion resuelve">
      <div class="contenedor resuelve__grid">
        <div data-revelar><p class="etiqueta">{ui["resuelve"]}</p><ul class="resuelve__lista">{problema}</ul></div>
        <div class="resuelve__solucion" data-revelar><p class="resuelve__frase">{S["solucion"]}</p>{demo_extra(clave, lang, I)}</div>
      </div>
    </section>

    <section class="seccion" id="incluye">
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{S["titulo"]}</p><h2>{ui["incluye"]}</h2></header>
        <ul class="beneficios">{incluye}</ul>
      </div>
    </section>

    <section class="seccion seccion--crema">
      <div class="contenedor ideal-grid">
        <div class="ideal" data-revelar><h2>{ui["ideal"]}</h2><ul>{ideal}</ul></div>
        <div class="mini-pasos" data-revelar><h2>{ui["como"]}</h2><ol>{pasos}</ol></div>
      </div>
    </section>

    <section class="seccion">
      <div class="contenedor faq-interna">
        <header class="cabeza" data-revelar><p class="etiqueta">{ui["faq"]}</p><h2>{S["titulo"]}</h2></header>
        <div class="faq__lista">{faqs}</div>
      </div>
      <div class="contenedor"><p class="etiqueta otros__t">{ui["otros"]}</p><div class="otros">{otros}</div></div>
    </section>
{banda_cta(ui, I, inicio, wa, wa_attr)}  </main>
'''
            escribir(ruta, marco_pagina(lang, ruta, ruta_otra, S["titulo"], S["meta"], ld, wa, cuerpo))

        # ---------- privacidad ----------
        P = PRIVACIDAD[lang]
        ruta, ruta_otra = RUTAS[lang]["privacidad"], RUTAS[otro]["privacidad"]
        wa = f'https://wa.me/{cfg["whatsapp"]}'

        def cuerpo_priv(pre, inicio, wa, wa_attr, P=P):
            bloques = "".join(f'<section class="legal__bloque"><h2>{t}</h2><p>{x}</p></section>' for t, x in P["bloques"])
            return f'''
  <main>
    <section class="seccion legal-sec">
      <div class="contenedor legal">
        {migas(ui, inicio, [(P["titulo"], None)])}
        <h1>{P["titulo"]}</h1>
        <p class="legal__fecha">{P["fecha"]}</p>
        {bloques}
        <section class="legal__bloque"><h2>{P["contacto"]}</h2><p><a href="{wa}"{wa_attr}>WhatsApp {marco.TEL}</a></p></section>
      </div>
    </section>
  </main>
'''
        escribir(ruta, marco_pagina(lang, ruta, ruta_otra, P["titulo"], P["meta"], [], wa, cuerpo_priv))

    # ---------- 404 (rutas absolutas: GitHub Pages lo muestra en cualquier dirección) ----------
    html404 = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Página no encontrada | Conektra</title>
  <meta name="robots" content="noindex">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#08271e">
  <link rel="icon" href="{d}img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{marco.FUENTES}" rel="stylesheet">
  <link rel="stylesheet" href="{d}css/conektra.css?v={marco.V_CSS}">
</head>
<body class="pagina-404">
  <main class="e404">
    <a class="marca" href="{d}">{LOGO}<span>Conektra</span></a>
    <div class="e404__cable" aria-hidden="true"><span></span><i></i><span></span></div>
    <p class="etiqueta">Error 404</p>
    <h1>Esta conexión <em>se perdió.</em></h1>
    <p>La página que buscas no existe o cambió de dirección.<br><span lang="en">This page doesn't exist or has moved.</span></p>
    <div class="hero__botones"><a class="boton boton--menta" href="{d}">Ir al inicio {I["flecha"]}</a><a class="boton boton--linea" href="{d}en/" lang="en">Go to homepage <span class="boton__flecha">{I["flecha"]}</span></a></div>
  </main>
</body>
</html>
'''
    with open(os.path.join(raiz, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html404)

    # ---------- sitemap y robots ----------
    urls = ["", "en/"] + escritas
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{d}{u}</loc><lastmod>{FECHA}</lastmod><priority>{'1.0' if u in ('', 'en/') else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n"
    with open(os.path.join(raiz, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap)
    with open(os.path.join(raiz, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {d}sitemap.xml\n")
    return escritas
