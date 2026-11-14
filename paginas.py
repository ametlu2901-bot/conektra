"""Páginas internas de Conektra: servicios, caso Acarreos Makena, privacidad y 404.

Se generan desde build.py. Cada página comparte cabecera y pie con la portada.
"""
import json, os, urllib.parse
import servicios

RUTAS = {
    "es": {"inicio": "", "web": "servicios/paginas-web/", "crm": "servicios/crm/", "api": "servicios/integraciones-api/",
           "erp": "servicios/erp-automatizacion/", "caso": "casos/acarreos-makena/", "privacidad": "privacidad/"},
    "en": {"inicio": "en/", "web": "en/services/websites/", "crm": "en/services/crm/", "api": "en/services/api-integrations/",
           "erp": "en/services/erp-automation/", "caso": "en/cases/acarreos-makena/", "privacidad": "en/privacy/"},
}
ORDEN_SERVICIOS = ["web", "crm", "api", "erp"]

UI = {
    "es": dict(nav=["Servicios", "Cómo funciona", "Casos", "Preguntas"], cta="Agenda una llamada", otra="EN", otra_nombre="English",
               incluye="Qué incluye", ideal="Ideal si…", como="Cómo lo hacemos", faq="Preguntas frecuentes", otros="Otros servicios",
               cta_h="¿Hablamos de tu proyecto?", cta_p="Cuéntanos qué sistemas usas hoy y te proponemos cómo conectarlos.", cta_form="Cuéntanos tu proyecto",
               wa_msg="Hola Conektra, quiero información sobre ", inicio="Inicio", servicios="Servicios", casos="Casos",
               pie_servicios="Servicios", pie_empresa="Conektra", pie_contacto="Contacto", privacidad="Privacidad",
               derechos="© 2026 Conektra. Integraciones API, CRM, ERP y páginas web.", hecho="Hecho en Panamá, para todo el mundo.",
               pasos=[("Diagnóstico", "Entendemos cómo trabajas hoy."), ("Propuesta", "Alcance, tiempos y precio claros."), ("Desarrollo", "Por etapas, con avances que pruebas."), ("Soporte", "Ajustes y mejoras después de entregar.")]),
    "en": dict(nav=["Services", "How it works", "Case study", "FAQ"], cta="Book a call", otra="ES", otra_nombre="Español",
               incluye="What's included", ideal="A good fit if…", como="How we do it", faq="FAQ", otros="Other services",
               cta_h="Shall we talk about your project?", cta_p="Tell us which systems you use today and we'll propose how to connect them.", cta_form="Tell us about your project",
               wa_msg="Hi Conektra, I'd like information about ", inicio="Home", servicios="Services", casos="Case studies",
               pie_servicios="Services", pie_empresa="Conektra", pie_contacto="Contact", privacidad="Privacy",
               derechos="© 2026 Conektra. API integrations, CRM, ERP and websites.", hecho="Made in Panama, for the world.",
               pasos=[("Discovery", "We learn how you work today."), ("Proposal", "Clear scope, timeline and price."), ("Build", "In stages, with progress you can test."), ("Support", "Tweaks and improvements after launch.")]),
}

SERVICIOS = {
    "es": {
        "web": dict(titulo="Páginas web y SEO", meta="Páginas web a la medida de tu marca, rápidas en celular y listas para aparecer en Google, con formularios conectados a tu CRM.",
                    h1='Páginas web que <em>trabajan</em> por tu negocio.', lead="Diseñamos tu página desde cero, con tu marca y tu estilo. Rápida en celular, pensada para aparecer en Google y conectada a tu CRM y a WhatsApp.",
                    incluye=[("Diseño a la medida", "Nada de plantillas: tu marca, tus colores y tu forma de hablarle a tus clientes."),
                             ("Rápida en celular", "Optimizada para cargar rápido en cualquier teléfono, donde está la mayoría de tus clientes."),
                             ("SEO técnico", "Títulos, descripciones, datos estructurados, sitemap y Search Console configurados."),
                             ("Páginas por servicio y zona", "Una página para cada búsqueda importante de tus clientes."),
                             ("Formularios conectados", "Cada contacto llega a tu CRM o a tu hoja de cálculo, sin copiar y pegar."),
                             ("Dominio y publicación", "Te ayudamos con el dominio, la publicación y los cambios posteriores.")],
                    ideal=["Tu negocio no tiene página o la que tiene no te trae clientes.", "Quieres aparecer en Google cuando buscan lo que vendes.", "Recibes clientes por WhatsApp y quieres ordenarlos."],
                    faq=[("¿Cuánto tarda una página web?", "Depende de cuántas páginas y funciones lleve. Una página sencilla puede estar en pocas semanas; te damos el tiempo exacto en la propuesta."),
                         ("¿Puedo editarla yo después?", "Sí. Te explicamos cómo hacer cambios básicos, y también podemos encargarnos nosotros."),
                         ("¿Me garantizan el primer lugar en Google?", "Nadie puede garantizarlo con honestidad. Lo que sí hacemos es dejar tu página técnicamente lista y con contenido pensado para las búsquedas de tus clientes.")]),
        "crm": dict(titulo="CRM a la medida", meta="CRM a la medida para ordenar clientes, cotizaciones y seguimientos, conectado a tu página web y a WhatsApp.",
                    h1='Todos tus clientes, <em>en un solo lugar.</em>', lead="Un CRM hecho para tu forma de vender: cada contacto entra solo desde tu página o WhatsApp y avanza por etapas hasta cerrar.",
                    incluye=[("Etapas a tu manera", "Nuevo, contactado, cotizado, ganado… las etapas que de verdad usa tu negocio."),
                             ("Entrada automática", "Los contactos de tu página web y formularios llegan solos, con todos sus datos."),
                             ("Recordatorios", "Seguimientos programados para que ningún cliente se quede sin respuesta."),
                             ("Reportes al día", "Cuántos clientes entran, cuántos cierras y cuánto vendes, sin armar reportes a mano."),
                             ("Fácil de usar", "Podemos construirlo sobre herramientas que tu equipo ya conoce, como Google Sheets."),
                             ("Crece contigo", "Agregamos campos, etapas e integraciones cuando tu negocio lo necesite.")],
                    ideal=["Tus clientes están repartidos entre WhatsApp, libretas y hojas sueltas.", "Se te olvidan seguimientos y pierdes ventas.", "Quieres saber cuánto vendes sin hacer cuentas a mano."],
                    faq=[("¿Necesito pagar una licencia de CRM?", "No necesariamente. Según tu caso podemos usar herramientas que ya tienes o integrar un CRM del mercado."),
                         ("¿Mi equipo podrá usarlo sin capacitación larga?", "Esa es la idea: lo diseñamos con tus etapas y tus palabras, y te acompañamos al principio."),
                         ("¿Se conecta con mi página web?", "Sí, los formularios de tu página pueden enviar los datos directo al CRM.")]),
        "api": dict(titulo="Integraciones API", meta="Integraciones API para que tus sistemas hablen entre sí: página web, CRM, ERP, WhatsApp, pagos y facturación.",
                    h1='Tus sistemas, <em>hablando entre sí.</em>', lead="Conectamos tu página, tu CRM, tu ERP y servicios como WhatsApp, pagos y facturación, para que los datos viajen solos y sin errores.",
                    incluye=[("Conexiones a la medida", "Integramos los sistemas que ya usas mediante sus APIs y webhooks."),
                             ("Tiempo real", "Cuando algo pasa en un sistema, los demás se actualizan al momento."),
                             ("WhatsApp, pagos y facturación", "Mensajes automáticos, cobros y facturas conectados a tus ventas."),
                             ("Sin doble digitación", "Los datos se escriben una vez y llegan a donde tienen que llegar."),
                             ("Registros y alertas", "Si algo falla, queda registrado y te avisamos para corregirlo."),
                             ("Documentación", "Te entregamos cómo funciona cada conexión, para que no dependas de nadie.")],
                    ideal=["Tu equipo copia datos de un sistema a otro todos los días.", "Usas varias herramientas que no se comunican.", "Quieres automatizar avisos, cobros o facturas."],
                    faq=[("¿Pueden conectar cualquier sistema?", "Casi cualquiera que tenga API o permita exportar e importar datos. Lo revisamos en el diagnóstico."),
                         ("¿Qué pasa si una conexión falla?", "Dejamos registros y alertas para detectarlo rápido, y te damos soporte para corregirlo."),
                         ("¿Mis datos salen de mis sistemas?", "Los datos viajan entre tus propias cuentas, con accesos de permisos mínimos.")]),
        "erp": dict(titulo="ERP y automatizaciones", meta="ERP y automatizaciones: inventario, facturación y procesos internos que se actualizan solos, con tableros para decidir con datos.",
                    h1='Tu operación, <em>en automático.</em>', lead="Inventario, facturación y procesos internos conectados y automatizados, con tableros claros para tomar decisiones con datos.",
                    incluye=[("Inventario conectado", "Las ventas descuentan stock solas y te avisan antes de quedarte sin producto."),
                             ("Facturación", "Facturas que se generan a partir de cada venta, sin volver a escribir los datos."),
                             ("Tareas automáticas", "Reportes, recordatorios y órdenes que se ejecutan solos en el momento indicado."),
                             ("Tableros", "Ventas, gastos e inventario en tableros fáciles de leer."),
                             ("ERP del mercado o a la medida", "Integramos el ERP que ya tienes o construimos lo que te falta."),
                             ("Procesos documentados", "Dejamos cada flujo explicado para que tu equipo lo entienda.")],
                    ideal=["Llevas inventario o facturación en hojas sueltas.", "Pierdes horas en tareas repetitivas cada semana.", "Quieres ver cómo va tu negocio sin esperar a fin de mes."],
                    faq=[("¿Tengo que cambiar mi ERP actual?", "No necesariamente. Muchas veces lo conectamos y automatizamos lo que ya tienes."),
                         ("¿Qué tareas se pueden automatizar?", "Reportes, avisos, órdenes de compra, conciliaciones y casi cualquier tarea repetitiva con reglas claras."),
                         ("¿Cómo empiezo?", "Con un diagnóstico de tus procesos. A partir de ahí te proponemos qué automatizar primero.")]),
    },
    "en": {
        "web": dict(titulo="Websites and SEO", meta="Custom websites for your brand, fast on mobile and built to show up on Google, with forms connected to your CRM.",
                    h1='Websites that <em>work</em> for your business.', lead="We design your website from scratch around your brand. Fast on mobile, built to show up on Google and connected to your CRM and WhatsApp.",
                    incluye=[("Custom design", "No templates: your brand, your colors and your way of talking to customers."),
                             ("Fast on mobile", "Optimized to load quickly on any phone, where most of your customers are."),
                             ("Technical SEO", "Titles, descriptions, structured data, sitemap and Search Console set up."),
                             ("Service and location pages", "A page for each important search your customers make."),
                             ("Connected forms", "Every lead lands in your CRM or spreadsheet, no copy and paste."),
                             ("Domain and launch", "We help with the domain, publishing and later changes.")],
                    ideal=["Your business has no website, or the one you have brings no customers.", "You want to show up on Google when people search for what you sell.", "You get customers on WhatsApp and want to organize them."],
                    faq=[("How long does a website take?", "It depends on the number of pages and features. A simple site can be ready in a few weeks; we give you the exact timeline in the proposal."),
                         ("Can I edit it myself later?", "Yes. We show you how to make basic changes, and we can also handle them for you."),
                         ("Do you guarantee first place on Google?", "No one can honestly guarantee that. What we do is leave your site technically ready, with content built for your customers' searches.")]),
        "crm": dict(titulo="Custom CRM", meta="A custom CRM to organize customers, quotes and follow-ups, connected to your website and WhatsApp.",
                    h1='All your customers, <em>in one place.</em>', lead="A CRM built around the way you sell: every lead comes in automatically from your website or WhatsApp and moves through stages until it closes.",
                    incluye=[("Stages your way", "New, contacted, quoted, won… the stages your business actually uses."),
                             ("Automatic intake", "Leads from your website and forms arrive on their own, with all their details."),
                             ("Reminders", "Scheduled follow-ups so no customer is left without an answer."),
                             ("Up-to-date reports", "How many leads come in, how many you close and how much you sell, no manual reports."),
                             ("Easy to use", "We can build it on tools your team already knows, like Google Sheets."),
                             ("Grows with you", "We add fields, stages and integrations as your business needs them.")],
                    ideal=["Your customers are scattered across WhatsApp, notebooks and loose spreadsheets.", "Follow-ups slip and you lose sales.", "You want to know how much you sell without doing the math by hand."],
                    faq=[("Do I need to pay for a CRM license?", "Not necessarily. Depending on your case we can use tools you already have or integrate an off-the-shelf CRM."),
                         ("Can my team use it without long training?", "That's the idea: we design it with your stages and your words, and support you at the start."),
                         ("Does it connect to my website?", "Yes, your website forms can send data straight to the CRM.")]),
        "api": dict(titulo="API integrations", meta="API integrations so your systems talk to each other: website, CRM, ERP, WhatsApp, payments and invoicing.",
                    h1='Your systems, <em>talking to each other.</em>', lead="We connect your website, CRM, ERP and services like WhatsApp, payments and invoicing, so data flows on its own and without errors.",
                    incluye=[("Custom connections", "We integrate the systems you already use through their APIs and webhooks."),
                             ("Real time", "When something happens in one system, the others update instantly."),
                             ("WhatsApp, payments and invoicing", "Automatic messages, payments and invoices tied to your sales."),
                             ("No double entry", "Data is typed once and reaches everywhere it needs to go."),
                             ("Logs and alerts", "If something fails, it's logged and we let you know so it can be fixed."),
                             ("Documentation", "We hand over how each connection works, so you don't depend on anyone.")],
                    ideal=["Your team copies data from one system to another every day.", "You use several tools that don't talk to each other.", "You want to automate notifications, payments or invoices."],
                    faq=[("Can you connect any system?", "Almost any system with an API or that allows data export and import. We check it during discovery."),
                         ("What if a connection fails?", "We set up logs and alerts to catch it quickly, and support you to fix it."),
                         ("Does my data leave my systems?", "Data travels between your own accounts, with least-privilege access.")]),
        "erp": dict(titulo="ERP and automation", meta="ERP and automation: inventory, invoicing and internal processes that update themselves, with dashboards to decide with data.",
                    h1='Your operations, <em>on autopilot.</em>', lead="Connected, automated inventory, invoicing and internal processes, with clear dashboards to make decisions with data.",
                    incluye=[("Connected inventory", "Sales deduct stock automatically and warn you before you run out."),
                             ("Invoicing", "Invoices generated from each sale, without retyping data."),
                             ("Automated tasks", "Reports, reminders and orders that run on their own at the right time."),
                             ("Dashboards", "Sales, expenses and inventory in easy-to-read dashboards."),
                             ("Off-the-shelf or custom ERP", "We integrate the ERP you have or build what's missing."),
                             ("Documented processes", "Every flow explained so your team understands it.")],
                    ideal=["You track inventory or invoicing in loose spreadsheets.", "You lose hours on repetitive tasks every week.", "You want to see how your business is doing without waiting for month-end."],
                    faq=[("Do I have to replace my current ERP?", "Not necessarily. We often connect and automate what you already have."),
                         ("Which tasks can be automated?", "Reports, alerts, purchase orders, reconciliations and almost any repetitive, rule-based task."),
                         ("How do I start?", "With a review of your processes. From there we propose what to automate first.")]),
    },
}

CASO = {
    "es": dict(titulo="Caso: Acarreos Makena", meta="Cómo Acarreos Makena pasó de atender clientes por WhatsApp sueltos a tener página web, SEO, CRM y reseñas conectados.",
               etiqueta="Caso real", h1='Acarreos Makena: <em>del WhatsApp suelto</em> a un negocio conectado.', sector="Mudanzas, acarreos y fletes · Panamá",
               reto_t="El reto", reto=["Los clientes llegaban solo por WhatsApp y las cotizaciones quedaban repartidas entre chats.", "No había una página propia que apareciera en Google al buscar sus servicios.", "No había forma de mostrar opiniones de clientes ni de medir cuántas cotizaciones llegaban."],
               hicimos_t="Lo que hicimos",
               hicimos=[("Página web con dominio propio", "Diseño a la medida de la marca, rápida en celular, con botón directo a WhatsApp y formulario de cotización."),
                        ("SEO con páginas por servicio y por zona", "Páginas para mudanzas, acarreos, escombros, montaje de eventos y oficinas, y por zonas como San Miguelito, Panamá Oeste y Chiriquí. Sitemap y Search Console configurados."),
                        ("CRM en Google Sheets", "Cada cotización del formulario se guarda en una hoja con su estado: nuevo, contactado, cotizado, agendado, ganado o perdido. Con resumen automático."),
                        ("Reseñas con aprobación", "Los clientes califican con estrellas y dejan su comentario; el dueño decide cuáles se publican.")],
               entregado_t="Lo que quedó funcionando",
               entregado=["Página web publicada en acarreosmakena.com", "Más de 10 páginas pensadas para búsquedas en Google", "Formulario de cotización conectado al CRM y a WhatsApp", "Reseñas con estrellas y aprobación del dueño", "Sitemap enviado a Google Search Console"],
               herramientas_t="Herramientas", herramientas=["HTML, CSS y JavaScript", "GitHub Pages", "Google Sheets", "Google Apps Script", "Google Search Console", "WhatsApp"],
               ver="Ver la página en vivo", cta_h="¿Quieres algo así para tu negocio?", cta_p="Cada proyecto es distinto: lo diseñamos a la medida de tu marca y tu forma de trabajar."),
    "en": dict(titulo="Case study: Acarreos Makena", meta="How Acarreos Makena went from scattered WhatsApp chats to a connected website, SEO, CRM and reviews.",
               etiqueta="Case study", h1='Acarreos Makena: <em>from scattered WhatsApp chats</em> to a connected business.', sector="Moving, hauling and freight · Panama",
               reto_t="The challenge", reto=["Customers only came in through WhatsApp, and quotes were scattered across chats.", "There was no website showing up on Google when people searched for their services.", "There was no way to show customer reviews or measure how many quote requests came in."],
               hicimos_t="What we did",
               hicimos=[("Website on its own domain", "Custom design for the brand, fast on mobile, with a direct WhatsApp button and a quote form."),
                        ("SEO with service and location pages", "Pages for moving, hauling, debris removal, event and office setup, plus locations like San Miguelito, Panamá Oeste and Chiriquí. Sitemap and Search Console set up."),
                        ("CRM on Google Sheets", "Every quote request from the form is saved to a sheet with its status: new, contacted, quoted, scheduled, won or lost. With an automatic summary."),
                        ("Reviews with approval", "Customers rate with stars and leave a comment; the owner decides which ones get published.")],
               entregado_t="What's up and running",
               entregado=["Website live at acarreosmakena.com", "10+ pages built for Google searches", "Quote form connected to the CRM and WhatsApp", "Star reviews with owner approval", "Sitemap submitted to Google Search Console"],
               herramientas_t="Tools", herramientas=["HTML, CSS and JavaScript", "GitHub Pages", "Google Sheets", "Google Apps Script", "Google Search Console", "WhatsApp"],
               ver="See the live website", cta_h="Want something like this for your business?", cta_p="Every project is different: we design it around your brand and the way you work."),
}

PRIVACIDAD = {
    "es": dict(titulo="Política de privacidad", meta="Cómo Conektra usa los datos que nos envías por el formulario de contacto o por WhatsApp.", fecha="Última actualización: 14 de noviembre de 2026",
               bloques=[("Qué datos recogemos", "Solo los que tú nos envías por el formulario de contacto: nombre, empresa, correo o WhatsApp, qué necesitas, presupuesto aproximado y tu mensaje. Si nos escribes por WhatsApp, también tu número y lo que nos cuentes."),
                        ("Para qué los usamos", "Únicamente para responderte, preparar una propuesta y dar seguimiento a tu solicitud. No los vendemos ni los compartimos con terceros para publicidad."),
                        ("Dónde se guardan", "Los mensajes del formulario se guardan en una hoja de cálculo privada de Google a la que solo tiene acceso Conektra."),
                        ("Servicios de terceros", "La página se aloja en GitHub Pages y usa fuentes de Google Fonts; estos servicios pueden registrar datos técnicos de la visita, como la dirección IP, según sus propias políticas. No usamos cookies de publicidad ni herramientas de seguimiento."),
                        ("Tus derechos", "Puedes pedirnos en cualquier momento que te digamos qué datos tenemos tuyos, que los corrijamos o que los borremos. Escríbenos por WhatsApp y lo hacemos.")],
               contacto="Contacto"),
    "en": dict(titulo="Privacy policy", meta="How Conektra uses the information you send us through the contact form or WhatsApp.", fecha="Last updated: November 14, 2026",
               bloques=[("What we collect", "Only what you send us through the contact form: name, company, email or WhatsApp, what you need, approximate budget and your message. If you message us on WhatsApp, also your number and what you tell us."),
                        ("How we use it", "Only to reply to you, prepare a proposal and follow up on your request. We don't sell it or share it with third parties for advertising."),
                        ("Where it's stored", "Form messages are stored in a private Google spreadsheet that only Conektra can access."),
                        ("Third-party services", "The site is hosted on GitHub Pages and uses Google Fonts; these services may log technical visit data, such as your IP address, under their own policies. We don't use advertising cookies or tracking tools."),
                        ("Your rights", "You can ask us at any time what information we have about you, to correct it or to delete it. Message us on WhatsApp and we'll take care of it.")],
               contacto="Contact"),
}


def prefijo(ruta):
    """Cuántos niveles subir desde una ruta como 'servicios/crm/' hasta la raíz."""
    return "../" * ruta.count("/")


def cabeza_html(T, ui, cfg, ruta, ruta_otra, titulo, meta, lang, extra_ld=None):
    pre = prefijo(ruta)
    url = cfg["dominio"] + ruta
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": titulo, "url": url, "description": meta, "isPartOf": {"@id": cfg["dominio"] + "#empresa"}}] + (extra_ld or [])}
    imagen = "compartir.jpg" if lang == "es" else "compartir-en.jpg"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{titulo} | Conektra</title>
  <meta name="description" content="{meta}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="{lang}" href="{url}">
  <link rel="alternate" hreflang="{"en" if lang == "es" else "es"}" href="{cfg["dominio"] + ruta_otra}">
  <meta name="theme-color" content="#f4f6fb" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0a0f1c" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Conektra">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{titulo} | Conektra">
  <meta property="og:description" content="{meta}">
  <meta property="og:image" content="{cfg["dominio"]}img/{imagen}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{pre}img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}css/estilos.css?v={cfg["v_css"]}">
</head>
<body class="interna">
'''


def cabecera_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr):
    pre = prefijo(ruta)
    inicio = pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")
    return f'''  <div class="lectura" aria-hidden="true"><i id="lectura"></i></div>
  <header class="cabecera" id="cabecera">
    <div class="contenedor cabecera__barra">
      <a class="marca" href="{inicio}" aria-label="Conektra">{LOGO}Conektra</a>
      <nav class="menu" id="menu" aria-label="Principal">
        <a href="{inicio}#servicios">{ui["nav"][0]}</a>
        <a href="{inicio}#como-funciona">{ui["nav"][1]}</a>
        <a href="{pre}{RUTAS[lang]["caso"]}">{ui["nav"][2]}</a>
        <a href="{inicio}#preguntas">{ui["nav"][3]}</a>
        <a class="idioma" href="{pre}{ruta_otra or './'}" hreflang="{"en" if lang == "es" else "es"}" lang="{"en" if lang == "es" else "es"}" title="{ui["otra_nombre"]}">{ui["otra"]}</a>
        <a class="boton boton--marca boton--wa" href="{wa}"{wa_attr}>{I["wa"]} {ui["cta"]}</a>
      </nav>
      <button class="hamburguesa" id="hamburguesa" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
'''


def pie_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr, descripcion):
    pre = prefijo(ruta)
    inicio = pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")
    serv = "".join(f'<a href="{pre}{RUTAS[lang][k]}">{SERVICIOS[lang][k]["titulo"]}</a>' for k in ORDEN_SERVICIOS)
    return f'''  <footer class="cierre cierre--interna">
    <div class="contenedor">
      <div class="pie__cols">
        <div class="pie__marca"><a class="marca" href="{inicio}">{LOGO}Conektra</a><p>{descripcion}</p></div>
        <nav aria-label="{ui["pie_servicios"]}"><h4>{ui["pie_servicios"]}</h4>{serv}</nav>
        <nav aria-label="{ui["pie_empresa"]}"><h4>{ui["pie_empresa"]}</h4><a href="{inicio}#como-funciona">{ui["nav"][1]}</a><a href="{pre}{RUTAS[lang]["caso"]}">{ui["casos"]}</a><a href="{inicio}#preguntas">{ui["nav"][3]}</a><a href="{pre}{RUTAS[lang]["privacidad"]}">{ui["privacidad"]}</a></nav>
        <nav aria-label="{ui["pie_contacto"]}"><h4>{ui["pie_contacto"]}</h4><a href="{wa}"{wa_attr}>WhatsApp +507 6552-3134</a><a href="{inicio}#proyecto">{ui["cta_form"]}</a><a href="{pre}{ruta_otra or './'}">{ui["otra_nombre"]}</a></nav>
      </div>
      <div class="pie"><span>{ui["derechos"]}</span><span>{ui["hecho"]}</span></div>
    </div>
  </footer>
  <div class="barra-wa" id="barra-wa" aria-hidden="true">
    <span class="barra-wa__txt"><b>{"¿Tienes un proyecto?" if lang == "es" else "Have a project?"}</b>{"Respondemos por WhatsApp" if lang == "es" else "We reply on WhatsApp"}</span>
    <a class="boton boton--wa" href="{wa}"{wa_attr} tabindex="-1">{I["wa"]} WhatsApp</a>
  </div>
  <script src="{pre}js/main.js?v={cfg["v_js"]}" defer></script>
</body>
</html>
'''


def migas(ui, pre, lang, partes):
    inicio = pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")
    items = [f'<a href="{inicio}">{ui["inicio"]}</a>'] + [f'<a href="{h}">{t}</a>' if h else f'<span aria-current="page">{t}</span>' for t, h in partes]
    return '<nav class="migas" aria-label="Ruta">' + '<span class="migas__sep">/</span>'.join(items) + '</nav>'


def banda_cta(ui, I, pre, lang, wa, wa_attr, h=None, p=None):
    inicio = pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")
    return f'''    <section class="seccion" style="padding-top:0">
      <div class="contenedor"><div class="banda" data-revelar>
        <div><h2>{h or ui["cta_h"]}</h2><p>{p or ui["cta_p"]}</p></div>
        <div class="banda__botones"><a class="boton boton--blanco boton--wa" href="{wa}"{wa_attr}>{I["wa"]} WhatsApp</a><a class="boton boton--contorno" href="{inicio}#proyecto">{ui["cta_form"]} {I["flecha"]}</a></div>
      </div></div>
    </section>
'''


def generar(raiz, cfg, I, LOGO, descripciones):
    escritas = []
    def escribir(ruta, html):
        destino = os.path.join(raiz, ruta, "index.html") if ruta.endswith("/") else os.path.join(raiz, ruta)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        escritas.append(ruta)

    for lang in ("es", "en"):
        otro = "en" if lang == "es" else "es"
        ui = UI[lang]
        maquetas = servicios.seccion(lang, I, solo_maquetas=True)
        for n, clave in enumerate(ORDEN_SERVICIOS):
            S = SERVICIOS[lang][clave]
            ruta, ruta_otra = RUTAS[lang][clave], RUTAS[otro][clave]
            pre = prefijo(ruta)
            wa = f'https://wa.me/{cfg["whatsapp"]}?text={urllib.parse.quote(ui["wa_msg"] + S["titulo"])}'
            wa_attr = ' target="_blank" rel="noopener"'
            incluye = "".join(f'<li class="beneficio" data-revelar style="transition-delay:{j * .05}s"><span class="beneficio__ico">{I["check"]}</span><h3>{t}</h3><p>{d}</p></li>' for j, (t, d) in enumerate(S["incluye"]))
            ideal = "".join(f'<li>{I["check"]}{x}</li>' for x in S["ideal"])
            pasos = "".join(f'<li><b>0{j + 1}</b><h3>{t}</h3><p>{d}</p></li>' for j, (t, d) in enumerate(ui["pasos"]))
            faqs = "".join(f'<details class="pregunta"><summary>{q}</summary><p>{a}</p></details>' for q, a in S["faq"])
            otros = "".join(f'<a class="otro" href="{pre}{RUTAS[lang][k]}"><span>{SERVICIOS[lang][k]["titulo"]}</span>{I["flecha"]}</a>' for k in ORDEN_SERVICIOS if k != clave)
            ld = [{"@type": "Service", "name": S["titulo"], "description": S["meta"], "provider": {"@id": cfg["dominio"] + "#empresa"}, "areaServed": "Worldwide"},
                  {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in S["faq"]]}]
            html = cabeza_html(None, ui, cfg, ruta, ruta_otra, S["titulo"], S["meta"], lang, ld) + cabecera_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr) + f'''
  <main>
    <section class="interna__hero">
      <div class="contenedor interna__grid">
        <div>
          {migas(ui, pre, lang, [(ui["servicios"], (pre + RUTAS[lang]["inicio"] if RUTAS[lang]["inicio"] else (pre or "./")) + "#servicios"), (S["titulo"], None)])}
          <h1>{S["h1"]}</h1>
          <p class="portada__lead">{S["lead"]}</p>
          <div class="portada__botones"><a class="boton boton--marca boton--wa" href="{wa}"{wa_attr}>{I["wa"]} {ui["cta"]}</a><a class="boton boton--claro" href="#incluye">{ui["incluye"]} {I["flecha"]}</a></div>
        </div>
        <div class="vitrina vitrina--interna"><div class="vitrina__rejilla" aria-hidden="true"></div><div class="panel activo">{maquetas[n]}</div></div>
      </div>
    </section>

    <section class="seccion" id="incluye">
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{S["titulo"]}</p><h2>{ui["incluye"]}</h2></header>
        <ul class="beneficios">{incluye}</ul>
      </div>
    </section>

    <section class="seccion" style="padding-top:0">
      <div class="contenedor ideal-grid">
        <div class="ideal" data-revelar><h2>{ui["ideal"]}</h2><ul>{ideal}</ul></div>
        <div class="mini-proceso" data-revelar><h2>{ui["como"]}</h2><ol>{pasos}</ol></div>
      </div>
    </section>

    <section class="seccion" style="padding-top:0">
      <div class="contenedor">
        <header class="cabeza cabeza--centro" data-revelar><p class="etiqueta">{ui["faq"]}</p><h2>{S["titulo"]}</h2></header>
        <div class="preguntas">{faqs}</div>
        <p class="etiqueta" style="text-align:center;margin-top:60px">{ui["otros"]}</p>
        <div class="otros">{otros}</div>
      </div>
    </section>
{banda_cta(ui, I, pre, lang, wa, wa_attr)}  </main>
''' + pie_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr, descripciones[lang])
            escribir(ruta, html)

        # ---------- caso ----------
        C = CASO[lang]
        ruta, ruta_otra = RUTAS[lang]["caso"], RUTAS[otro]["caso"]
        pre = prefijo(ruta)
        wa = f'https://wa.me/{cfg["whatsapp"]}?text={urllib.parse.quote(ui["wa_msg"] + "Acarreos Makena")}'
        wa_attr = ' target="_blank" rel="noopener"'
        reto = "".join(f'<li>{x}</li>' for x in C["reto"])
        hicimos = "".join(f'<li class="hecho" data-revelar><span class="hecho__n">0{j + 1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for j, (t, d) in enumerate(C["hicimos"]))
        entregado = "".join(f'<li>{I["check"]}{x}</li>' for x in C["entregado"])
        herramientas = "".join(f'<span class="cinta__chip"><i>{I["codigo"]}</i>{h}</span>' for h in C["herramientas"])
        html = cabeza_html(None, ui, cfg, ruta, ruta_otra, C["titulo"], C["meta"], lang) + cabecera_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr) + f'''
  <main>
    <section class="interna__hero">
      <div class="contenedor">
        {migas(ui, pre, lang, [(ui["casos"], None), ("Acarreos Makena", None)])}
        <p class="chip" style="margin-top:22px">{C["sector"]}</p>
        <h1 class="caso__h1">{C["h1"]}</h1>
        <div class="portada__botones"><a class="boton boton--marca" href="https://acarreosmakena.com/" target="_blank" rel="noopener">{C["ver"]} {I["flecha"]}</a></div>
        <div class="caso__fotos caso__fotos--grande" data-revelar>
          <div class="caso__escritorio"><div class="ventana__barra"><i></i><i></i><i></i><span>acarreosmakena.com</span></div><img src="{pre}img/caso-acarreos-escritorio.webp" alt="Página web de Acarreos Makena en computadora" width="1440" height="900"></div>
          <div class="caso__movil"><img src="{pre}img/caso-acarreos-movil.webp" alt="Página web de Acarreos Makena en celular" width="390" height="844" loading="lazy"></div>
        </div>
      </div>
    </section>

    <section class="seccion" style="padding-top:20px">
      <div class="contenedor caso-detalle">
        <div class="reto" data-revelar><p class="etiqueta">{C["reto_t"]}</p><ul>{reto}</ul></div>
        <div>
          <header class="cabeza" data-revelar><p class="etiqueta">{C["hicimos_t"]}</p></header>
          <ol class="hechos">{hicimos}</ol>
        </div>
      </div>
    </section>

    <section class="seccion" style="padding-top:0">
      <div class="contenedor ideal-grid">
        <div class="ideal" data-revelar><h2>{C["entregado_t"]}</h2><ul>{entregado}</ul></div>
        <div class="mini-proceso" data-revelar><h2>{C["herramientas_t"]}</h2><div class="herramientas">{herramientas}</div></div>
      </div>
    </section>
{banda_cta(ui, I, pre, lang, wa, wa_attr, C["cta_h"], C["cta_p"])}  </main>
''' + pie_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr, descripciones[lang])
        escribir(ruta, html)

        # ---------- privacidad ----------
        P = PRIVACIDAD[lang]
        ruta, ruta_otra = RUTAS[lang]["privacidad"], RUTAS[otro]["privacidad"]
        pre = prefijo(ruta)
        wa = f'https://wa.me/{cfg["whatsapp"]}'
        wa_attr = ' target="_blank" rel="noopener"'
        bloques = "".join(f'<section class="legal__bloque"><h2>{t}</h2><p>{d}</p></section>' for t, d in P["bloques"])
        html = cabeza_html(None, ui, cfg, ruta, ruta_otra, P["titulo"], P["meta"], lang) + cabecera_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr) + f'''
  <main>
    <section class="interna__hero interna__hero--corta">
      <div class="contenedor legal">
        {migas(ui, pre, lang, [(P["titulo"], None)])}
        <h1>{P["titulo"]}</h1>
        <p class="legal__fecha">{P["fecha"]}</p>
        {bloques}
        <section class="legal__bloque"><h2>{P["contacto"]}</h2><p><a href="{wa}"{wa_attr}>WhatsApp +507 6552-3134</a></p></section>
      </div>
    </section>
  </main>
''' + pie_html(ui, I, LOGO, cfg, ruta, ruta_otra, lang, wa, wa_attr, descripciones[lang])
        escribir(ruta, html)

    # ---------- 404 (rutas absolutas: GitHub Pages lo muestra en cualquier dirección) ----------
    d = cfg["dominio"]
    html404 = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Página no encontrada | Conektra</title>
  <meta name="robots" content="noindex">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{d}img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{d}css/estilos.css?v={cfg["v_css"]}">
</head>
<body class="pagina-404">
  <main class="e404">
    <a class="marca" href="{d}">{LOGO}Conektra</a>
    <div class="e404__cable" aria-hidden="true"><span></span><i></i><span></span></div>
    <p class="etiqueta">Error 404</p>
    <h1>Esta conexión <em>se perdió.</em></h1>
    <p>La página que buscas no existe o cambió de dirección.<br><span lang="en">This page doesn't exist or has moved.</span></p>
    <div class="portada__botones"><a class="boton boton--marca" href="{d}">Ir al inicio {I["flecha"]}</a><a class="boton boton--claro" href="{d}en/" lang="en">Go to homepage {I["flecha"]}</a></div>
  </main>
</body>
</html>
'''
    with open(os.path.join(raiz, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html404)

    # ---------- sitemap y robots ----------
    urls = ["", "en/"] + escritas
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{d}{u}</loc><lastmod>2026-11-14</lastmod><priority>{'1.0' if u in ('', 'en/') else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n"
    with open(os.path.join(raiz, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(sitemap)
    with open(os.path.join(raiz, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {d}sitemap.xml\n")
    return escritas
