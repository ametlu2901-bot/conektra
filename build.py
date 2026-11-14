"""Genera la página de Integrafy en español (index.html) y en inglés (en/index.html).

Uso:  python build.py
Los datos de contacto se cambian en CONFIG. Los textos, en ES y EN.
"""
import json, os, urllib.parse
import servicios

CONFIG = {
    "dominio": "https://ametlu2901-bot.github.io/integrafy/",  # cambiar a https://integrafy.dev/ cuando se compre el dominio
    "whatsapp": "50765523134",                  # solo números con código de país, p. ej. 50760000000
    "correo": "",                               # p. ej. hola@integrafy.dev
}

RAIZ = os.path.dirname(os.path.abspath(__file__))

# ---------- íconos (trazos simples, heredan el color) ----------
I = {
    "flecha": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.2-1.4A9.9 9.9 0 1 0 12.04 2Zm4.5 11.96c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.53.06a6.7 6.7 0 0 1-3.34-2.92c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.66.31 2.77 2.77 0 0 0-.86 2.06 4.8 4.8 0 0 0 1 2.56 11 11 0 0 0 4.22 3.73c1.57.68 2.19.74 2.98.62.48-.07 1.46-.6 1.67-1.18.2-.58.2-1.08.14-1.18-.06-.1-.22-.17-.47-.29Z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18"/></svg>',
    "crm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0M16 6h5M16 10h5M18 14h3"/></svg>',
    "erp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4V5Z"/></svg>',
    "pago": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M7 15h4"/></svg>',
    "hoja": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M4 9h16M4 15h16M10 3v18"/></svg>',
    "rayo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg>',
}
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#0b1220"/><circle cx="10" cy="11" r="3.2" fill="#3b5bff"/><circle cx="22" cy="21" r="3.2" fill="#13c2a3"/><path d="M10 14.5v2a4.5 4.5 0 0 0 4.5 4.5H18.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M22 17.5v-2A4.5 4.5 0 0 0 17.5 11H13.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".55"/></svg>'
NUCLEO = '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="10" cy="11" r="3.4" fill="#3b5bff"/><circle cx="22" cy="21" r="3.4" fill="#13c2a3"/><path d="M10 14.5v2a4.5 4.5 0 0 0 4.5 4.5H18.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M22 17.5v-2A4.5 4.5 0 0 0 17.5 11H13.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".55"/></svg>'

ES = dict(
    lang="es", ruta="", otra_ruta="en/", otra_etiqueta="EN", otra_nombre="English",
    titulo="Integrafy | Integraciones API, CRM, ERP y páginas web",
    descripcion="Conectamos tu página web, tu CRM, tu ERP, WhatsApp y tus pagos para que tu negocio trabaje en automático. Integraciones API, CRM a la medida, ERP y páginas web con SEO.",
    nav=["Servicios", "Cómo funciona", "Casos", "Preguntas"], cta="Agenda una llamada",
    wa_msg="Hola Integrafy, quiero conectar los sistemas de mi negocio.",
    chip="Integraciones · CRM · ERP · Web",
    h1='Tus sistemas, <em>conectados.</em> Tu negocio, en automático.',
    lead="Unimos tu página web, tu CRM, tu ERP, WhatsApp y tus pagos para que los datos viajen solos y tu equipo deje de copiar y pegar.",
    ver_casos="Mira un caso real",
    prueba='<b>Acarreos Makena:</b> web, SEO y CRM conectados',
    nodos=[("Web", "Formularios", "web"), ("CRM", "Clientes", "crm"), ("ERP", "Facturación", "erp"), ("WhatsApp", "Mensajes", "chat"), ("Pagos", "Cobros", "pago"), ("Sheets", "Reportes", "hoja")],
    avisos=[("Nuevo cliente", "Guardado en el CRM"), ("Factura creada", "Enviada al ERP"), ("Mensaje enviado", "Confirmación por WhatsApp"), ("Pago recibido", "Conciliado automáticamente")],
    franja_texto="Conectamos tu negocio con",
    palabras=["tu página web", "WhatsApp", "tu CRM", "tu ERP", "Google Sheets", "tus pagos", "tu facturación", "cualquier API"],
    franja_cta="Cuéntanos tu caso",
    flujo_etiqueta="Cómo funciona", flujo_h2="De un mensaje a una venta cerrada.",
    flujo_p="Así se mueve un cliente cuando tus sistemas hablan entre sí: sin hojas sueltas ni datos perdidos.",
    pasos=[("El cliente te escribe", "Desde tu página web o por WhatsApp, a cualquier hora."),
           ("Queda en tu CRM", "Sus datos se guardan solos y tu equipo recibe el aviso."),
           ("Cotizas y das seguimiento", "Cada oportunidad avanza por etapas hasta cerrar."),
           ("Se factura en tu ERP", "La venta pasa a facturación y contabilidad sin volver a escribirla.")],
    esc1=dict(cab="WhatsApp", est="En línea", b1="Hola, ¿me pueden cotizar una mudanza para el sábado?", b2="¡Claro! Ya registramos tu solicitud. Te enviamos la cotización en unos minutos."),
    esc2=dict(cab="Nuevo cliente", est="CRM", filas=[("Nombre", "María Pérez"), ("Canal", "Formulario web"), ("Servicio", "Mudanza"), ("Etapa", "Nuevo")]),
    esc3=dict(cab="Cotización #1042", est="Enviada", filas=[("Servicio", "Mudanza residencial"), ("Fecha", "Sábado 9:00"), ("Seguimiento", "Recordatorio en 24 h")]),
    esc4=dict(cab="Factura #A-2381", est="Pagada", filas=[("Cliente", "María Pérez"), ("Concepto", "Mudanza residencial"), ("Impuesto", "Calculado")], total=("Total", "Sincronizado")),
    serv_etiqueta="Servicios", serv_h2="Todo lo que tu negocio necesita para trabajar conectado.",
    servicios=[
        ("Páginas web y SEO", "Diseñadas a la medida de tu marca: rápidas, bonitas en celular y listas para aparecer en Google, con formularios que alimentan tu CRM."),
        ("CRM a la medida", "Tus clientes, cotizaciones y seguimientos en un solo lugar, con etapas, recordatorios y reportes."),
        ("Integraciones API", "Conectamos tus sistemas entre sí y con servicios externos: WhatsApp, pagos, facturación, Google y más."),
        ("ERP y automatizaciones", "Inventario, facturación y procesos internos que se actualizan solos, con tableros para decidir con datos."),
    ],
    mock_web=dict(url="tunegocio.com", h="Mudanzas en todo el país", serp_t="Tu negocio | Mudanzas y acarreos", serp_u="tunegocio.com › mudanzas", serp_d="Cotiza en minutos por WhatsApp. Camiones, personal y cobertura nacional."),
    mock_crm=dict(cols=[("Nuevos", [("María Pérez", "Mudanza · Web"), ("Carlos Ruiz", "Flete · WhatsApp")]), ("Cotizados", [("Ana Gómez", "Oficina · B/. 380"), ("Luis Díaz", "Escombros · B/. 120")]), ("Ganados", [("Rosa Vega", "Mudanza · B/. 450")])]),
    mock_api=dict(c="// webhook: formulario web → CRM → WhatsApp", log=[("POST /clientes", "200 · 84 ms"), ("Mensaje de confirmación enviado", "WhatsApp"), ("Fila agregada al reporte", "Sheets")]),
    mock_erp=dict(m=[("Ventas del mes", "B/. 12.4k"), ("Facturas", "86"), ("Inventario", "OK")]),
    caso_etiqueta="Caso real", caso_h2="Del WhatsApp suelto a un negocio conectado.",
    caso_intro="Un ejemplo de lo que hacemos. Cada proyecto se diseña desde cero: tu página no se parecerá a esta, se parecerá a tu negocio.",
    medida_t="Hecho a tu medida", medida_p="Tu marca, tus colores, tu estilo y las funciones que tu negocio necesita. Diseñamos tu página y tus integraciones según tu industria y tu forma de trabajar, no con plantillas.",
    caso_nombre="Acarreos Makena", caso_sector="Mudanzas, acarreos y fletes en Panamá",
    logros=[("Página web con dominio propio", "Diseño a la medida, rápida en celular y con botón directo a WhatsApp."),
            ("SEO con páginas por servicio y por zona", "Páginas pensadas para cada búsqueda, sitemap y Search Console configurados."),
            ("CRM en Google Sheets", "Cada cotización del formulario queda registrada con su estado: nuevo, cotizado, ganado."),
            ("Reseñas con aprobación", "Los clientes califican con estrellas y el dueño decide qué se publica.")],
    caso_cta="Ver la página en vivo",
    proc_etiqueta="Proceso", proc_h2="Así trabajamos contigo.",
    proceso=[("Diagnóstico", "Entendemos cómo funciona tu negocio hoy y dónde se pierde tiempo o información."),
             ("Propuesta", "Te mostramos qué conectar, cómo y en qué orden, con alcance, tiempos y precio claros."),
             ("Desarrollo", "Construimos por etapas y te mostramos avances para que pruebes desde temprano."),
             ("Soporte", "Te acompañamos después de entregar: ajustes, mejoras y nuevas integraciones.")],
    tec_titulo="Trabajamos con",
    tecnologias=["APIs REST", "Webhooks", "WhatsApp", "Google Workspace", "Google Sheets", "Bases de datos SQL", "Pasarelas de pago", "Facturación electrónica", "CRMs y ERPs del mercado", "SEO técnico"],
    faq_etiqueta="Preguntas frecuentes", faq_h2="Lo que más nos preguntan.",
    faqs=[("¿Cuánto cuesta un proyecto?", "Depende de qué sistemas hay que conectar y cuánto hay que construir. Cuéntanos tu caso y te enviamos una propuesta con alcance y precio claros antes de empezar."),
          ("¿Tengo que cambiar los sistemas que ya uso?", "No necesariamente. Muchas veces conectamos lo que ya tienes. Si algo no da para más, te lo decimos y te proponemos una alternativa."),
          ("¿Trabajan con negocios fuera de Panamá?", "Sí. Trabajamos de forma remota con negocios de Panamá y de otros países, en español o en inglés."),
          ("¿Qué pasa después de la entrega?", "Te acompañamos con soporte y mejoras. Tus sistemas crecen contigo, así que siempre podemos agregar nuevas integraciones."),
          ("¿Mis datos quedan seguros?", "Tus datos quedan en tus cuentas y sistemas. Usamos accesos con permisos mínimos y te entregamos todo documentado.")],
    cierre_h2="Tu negocio, <em>conectado.</em>",
    cierre_p="Escríbenos y cuéntanos qué sistemas usas hoy. Te decimos cómo hacer que trabajen juntos.",
    cierre_wa="Escríbenos por WhatsApp", cierre_correo="Enviar un correo",
    pie_derechos="© 2026 Integrafy. Integraciones API, CRM, ERP y páginas web.",
)

EN = dict(
    lang="en", ruta="en/", otra_ruta="", otra_etiqueta="ES", otra_nombre="Español",
    titulo="Integrafy | API integrations, CRM, ERP and websites",
    descripcion="We connect your website, CRM, ERP, WhatsApp and payments so your business runs on autopilot. API integrations, custom CRM, ERP and SEO-ready websites.",
    nav=["Services", "How it works", "Case study", "FAQ"], cta="Book a call",
    wa_msg="Hi Integrafy, I want to connect my business systems.",
    chip="Integrations · CRM · ERP · Web",
    h1='Your systems, <em>connected.</em> Your business, on autopilot.',
    lead="We link your website, CRM, ERP, WhatsApp and payments so data flows on its own and your team stops copying and pasting.",
    ver_casos="See a real case",
    prueba='<b>Acarreos Makena:</b> website, SEO and CRM connected',
    nodos=[("Web", "Forms", "web"), ("CRM", "Customers", "crm"), ("ERP", "Invoicing", "erp"), ("WhatsApp", "Messages", "chat"), ("Payments", "Billing", "pago"), ("Sheets", "Reports", "hoja")],
    avisos=[("New customer", "Saved to the CRM"), ("Invoice created", "Sent to the ERP"), ("Message sent", "WhatsApp confirmation"), ("Payment received", "Reconciled automatically")],
    franja_texto="We connect your business with",
    palabras=["your website", "WhatsApp", "your CRM", "your ERP", "Google Sheets", "your payments", "your invoicing", "any API"],
    franja_cta="Tell us about your project",
    flujo_etiqueta="How it works", flujo_h2="From a message to a closed deal.",
    flujo_p="This is how a customer moves when your systems talk to each other: no loose spreadsheets, no lost data.",
    pasos=[("The customer reaches out", "From your website or on WhatsApp, at any time."),
           ("It lands in your CRM", "Their details are saved automatically and your team gets notified."),
           ("You quote and follow up", "Every opportunity moves through stages until it closes."),
           ("It's invoiced in your ERP", "The sale flows into invoicing and accounting without retyping it.")],
    esc1=dict(cab="WhatsApp", est="Online", b1="Hi, can I get a quote for a move this Saturday?", b2="Of course! We've logged your request. Your quote is on its way in a few minutes."),
    esc2=dict(cab="New customer", est="CRM", filas=[("Name", "Maria Perez"), ("Channel", "Website form"), ("Service", "Moving"), ("Stage", "New")]),
    esc3=dict(cab="Quote #1042", est="Sent", filas=[("Service", "Home move"), ("Date", "Saturday 9:00"), ("Follow-up", "Reminder in 24 h")]),
    esc4=dict(cab="Invoice #A-2381", est="Paid", filas=[("Customer", "Maria Perez"), ("Item", "Home move"), ("Tax", "Calculated")], total=("Total", "Synced")),
    serv_etiqueta="Services", serv_h2="Everything your business needs to run connected.",
    servicios=[
        ("Websites and SEO", "Custom-designed for your brand: fast, mobile-friendly and built to show up on Google, with forms that feed your CRM."),
        ("Custom CRM", "Your customers, quotes and follow-ups in one place, with stages, reminders and reports."),
        ("API integrations", "We connect your systems to each other and to external services: WhatsApp, payments, invoicing, Google and more."),
        ("ERP and automation", "Inventory, invoicing and internal processes that update themselves, with dashboards to decide with data."),
    ],
    mock_web=dict(url="yourbusiness.com", h="Moving services nationwide", serp_t="Your Business | Moving & hauling", serp_u="yourbusiness.com › moving", serp_d="Get a quote in minutes on WhatsApp. Trucks, crew and nationwide coverage."),
    mock_crm=dict(cols=[("New", [("Maria Perez", "Moving · Web"), ("Carlos Ruiz", "Freight · WhatsApp")]), ("Quoted", [("Ana Gomez", "Office · $380"), ("Luis Diaz", "Debris · $120")]), ("Won", [("Rosa Vega", "Moving · $450")])]),
    mock_api=dict(c="// webhook: website form → CRM → WhatsApp", log=[("POST /customers", "200 · 84 ms"), ("Confirmation message sent", "WhatsApp"), ("Row added to report", "Sheets")]),
    mock_erp=dict(m=[("Monthly sales", "$12.4k"), ("Invoices", "86"), ("Inventory", "OK")]),
    caso_etiqueta="Case study", caso_h2="From scattered WhatsApp chats to a connected business.",
    caso_intro="One example of what we do. Every project is designed from scratch: your website won't look like this one, it will look like your business.",
    medida_t="Made to measure", medida_p="Your brand, your colors, your style and the features your business needs. We design your website and integrations around your industry and the way you work, not templates.",
    caso_nombre="Acarreos Makena", caso_sector="Moving, hauling and freight in Panama",
    logros=[("Website on its own domain", "Custom design, fast on mobile, with a direct WhatsApp button."),
            ("SEO with service and location pages", "Pages built for each search, plus sitemap and Search Console set up."),
            ("CRM on Google Sheets", "Every quote request from the form is logged with its status: new, quoted, won."),
            ("Reviews with approval", "Customers rate with stars and the owner decides what gets published.")],
    caso_cta="See the live website",
    proc_etiqueta="Process", proc_h2="How we work with you.",
    proceso=[("Discovery", "We learn how your business runs today and where time or information gets lost."),
             ("Proposal", "We show you what to connect, how and in what order, with clear scope, timeline and price."),
             ("Build", "We build in stages and show you progress so you can test early."),
             ("Support", "We stay with you after launch: tweaks, improvements and new integrations.")],
    tec_titulo="We work with",
    tecnologias=["REST APIs", "Webhooks", "WhatsApp", "Google Workspace", "Google Sheets", "SQL databases", "Payment gateways", "E-invoicing", "Off-the-shelf CRMs and ERPs", "Technical SEO"],
    faq_etiqueta="FAQ", faq_h2="What people ask us most.",
    faqs=[("How much does a project cost?", "It depends on which systems need to be connected and how much needs to be built. Tell us about your case and we'll send a proposal with clear scope and price before we start."),
          ("Do I have to replace the systems I already use?", "Not necessarily. We often connect what you already have. If something can't keep up, we'll tell you and suggest an alternative."),
          ("Do you work with businesses outside Panama?", "Yes. We work remotely with businesses in Panama and abroad, in English or Spanish."),
          ("What happens after delivery?", "We stay with you for support and improvements. Your systems grow with you, so we can always add new integrations."),
          ("Is my data safe?", "Your data stays in your own accounts and systems. We use least-privilege access and hand everything over documented.")],
    cierre_h2="Your business, <em>connected.</em>",
    cierre_p="Message us and tell us which systems you use today. We'll show you how to make them work together.",
    cierre_wa="Message us on WhatsApp", cierre_correo="Send an email",
    pie_derechos="© 2026 Integrafy. API integrations, CRM, ERP and websites.",
)

# posiciones de los nodos alrededor del núcleo (porcentajes del diagrama)
POS = [(16, 18), (84, 22), (92, 58), (70, 90), (24, 86), (8, 52)]


def pagina(T):
    pre = "../" if T["ruta"] else ""
    url = CONFIG["dominio"] + T["ruta"]
    wa = f'https://wa.me/{CONFIG["whatsapp"]}?text={urllib.parse.quote(T["wa_msg"])}' if CONFIG["whatsapp"] else "#contacto"
    wa_attr = ' target="_blank" rel="noopener"' if CONFIG["whatsapp"] else ""
    correo = f'mailto:{CONFIG["correo"]}' if CONFIG["correo"] else ""

    nodos = "\n".join(
        f'<div class="nodo" style="left:{x}%;top:{y}%"><i>{I[ico]}</i><span>{n}<small>{s}</small></span></div>'
        for (n, s, ico), (x, y) in zip(T["nodos"], POS))
    # curvas desde el núcleo (50,50) hacia cada nodo, en un lienzo de 100x92
    rutas = "".join(f'<path class="ruta" d="M50 46 Q {(50 + x) / 2 + (8 if i % 2 else -8)} {(46 + y * .92) / 2} {x} {y * .92}"/>' for i, (x, y) in enumerate(POS))
    flujos = "".join(f'<path class="flujo" d="M50 46 Q {(50 + x) / 2 + (8 if i % 2 else -8)} {(46 + y * .92) / 2} {x} {y * .92}"/>' for i, (x, y) in enumerate(POS))

    palabras = "".join(f"<li>{p}</li>" for p in T["palabras"])
    pasos = "\n".join(
        f'<li><button type="button" class="paso{" activo" if i == 0 else ""}" data-paso="{i}" aria-pressed="{str(i == 0).lower()}"><b>0{i + 1}</b><span><h3>{t}</h3><p>{d}</p></span></button></li>'
        for i, (t, d) in enumerate(T["pasos"]))

    def filas(lst): return "".join(f'<div class="fila"><span>{a}</span><b>{b}</b></div>' for a, b in lst)
    e1, e2, e3, e4 = T["esc1"], T["esc2"], T["esc3"], T["esc4"]
    escenas = f'''
<div class="cuadro activo" data-cuadro="0"><div class="tarjeta"><div class="tarjeta__cab"><b>{e1["cab"]}</b><span class="estado">{e1["est"]}</span></div><div class="burbuja">{e1["b1"]}</div><div class="burbuja burbuja--mia">{e1["b2"]}</div></div></div>
<div class="cuadro" data-cuadro="1"><div class="tarjeta"><div class="tarjeta__cab"><b>{e2["cab"]}</b><span class="estado estado--azul">{e2["est"]}</span></div>{filas(e2["filas"])}</div></div>
<div class="cuadro" data-cuadro="2"><div class="tarjeta"><div class="tarjeta__cab"><b>{e3["cab"]}</b><span class="estado estado--ambar">{e3["est"]}</span></div>{filas(e3["filas"])}</div></div>
<div class="cuadro" data-cuadro="3"><div class="tarjeta"><div class="tarjeta__cab"><b>{e4["cab"]}</b><span class="estado">{e4["est"]}</span></div>{filas(e4["filas"])}<div class="total"><span>{e4["total"][0]}</span><span>{e4["total"][1]}</span></div></div></div>'''

    pestanas, paneles = servicios.seccion(T["lang"], I)

    logros = "\n".join(f'<li><i>{I["check"]}</i><span><b>{t}</b><span>{d}</span></span></li>' for t, d in T["logros"])
    proceso = "\n".join(f'<li data-revelar style="transition-delay:{i * .08}s"><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(T["proceso"]))
    tecnologias = "".join(f"<span>{t}</span>" for t in T["tecnologias"])
    faqs = "\n".join(f'<details class="pregunta"><summary>{q}</summary><p>{a}</p></details>' for q, a in T["faqs"])
    avisos_json = json.dumps(T["avisos"], ensure_ascii=False).replace("</", "<\\/")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "#empresa", "name": "Integrafy", "url": CONFIG["dominio"],
         "description": T["descripcion"], "areaServed": ["Panamá", "Latinoamérica", "Worldwide"],
         "knowsAbout": ["API integrations", "CRM", "ERP", "Web development", "SEO", "Automation"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faqs"]]}]}

    boton_correo = f'<a class="boton boton--contorno" href="{correo}">{T["cierre_correo"]}</a>' if correo else ""

    return f'''<!doctype html>
<html lang="{T["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{T["titulo"]}</title>
  <meta name="description" content="{T["descripcion"]}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="es" href="{CONFIG["dominio"]}">
  <link rel="alternate" hreflang="en" href="{CONFIG["dominio"]}en/">
  <link rel="alternate" hreflang="x-default" href="{CONFIG["dominio"]}">
  <meta name="theme-color" content="#0b1220">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Integrafy">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{T["titulo"]}">
  <meta property="og:description" content="{T["descripcion"]}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{pre}img/favicon.svg" type="image/svg+xml">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}css/estilos.css?v=5">
</head>
<body>
  <header class="cabecera">
    <div class="contenedor cabecera__barra">
      <a class="marca" href="{pre or './'}" aria-label="Integrafy">{LOGO}Integrafy</a>
      <nav class="menu" id="menu" aria-label="Principal">
        <a href="#servicios">{T["nav"][0]}</a>
        <a href="#como-funciona">{T["nav"][1]}</a>
        <a href="#caso">{T["nav"][2]}</a>
        <a href="#preguntas">{T["nav"][3]}</a>
        <a class="idioma" href="{pre}{T["otra_ruta"] or './'}" hreflang="{"en" if T["lang"] == "es" else "es"}" lang="{"en" if T["lang"] == "es" else "es"}" title="{T["otra_nombre"]}">{T["otra_etiqueta"]}</a>
        <a class="boton boton--marca" href="{wa}"{wa_attr}>{T["cta"]}</a>
      </nav>
      <button class="hamburguesa" id="hamburguesa" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>

  <main>
    <section class="portada">
      <div class="contenedor portada__grid">
        <div>
          <p class="chip">{T["chip"]}</p>
          <h1>{T["h1"]}</h1>
          <p class="portada__lead">{T["lead"]}</p>
          <div class="portada__botones">
            <a class="boton boton--marca" href="{wa}"{wa_attr}>{I["wa"]} {T["cta"]}</a>
            <a class="boton boton--claro" href="#caso">{T["ver_casos"]} {I["flecha"]}</a>
          </div>
          <a class="prueba" href="#caso"><img src="{pre}img/caso-acarreos-escritorio.webp" alt="" width="1440" height="900"><span>{T["prueba"]}</span></a>
        </div>
        <div class="diagrama" aria-hidden="true">
          <svg class="lineas" viewBox="0 0 100 92" preserveAspectRatio="none"><defs><linearGradient id="g-flujo" x1="0" x2="1"><stop offset="0" stop-color="#3b5bff"/><stop offset="1" stop-color="#13c2a3"/></linearGradient></defs>{rutas}{flujos}</svg>
          <div class="nucleo">{NUCLEO}</div>
          {nodos}
          <div class="aviso" id="aviso"><span class="aviso__ico">{I["rayo"]}</span><span><b id="aviso-titulo">{T["avisos"][0][0]}</b><span id="aviso-texto">{T["avisos"][0][1]}</span></span></div>
        </div>
      </div>
    </section>

    <section class="franja">
      <div class="contenedor franja__grid">
        <p class="franja__texto">{T["franja_texto"]}</p>
        <div class="palabras" aria-label="{T["franja_texto"]}"><ul class="palabras__pista" id="palabras">{palabras}</ul></div>
        <a class="boton boton--marca franja__accion" href="{wa}"{wa_attr}>{T["franja_cta"]}</a>
      </div>
    </section>

    <section class="seccion" id="como-funciona">
      <div class="oscura seccion">
        <div class="contenedor">
          <header class="cabeza" data-revelar><p class="etiqueta">{T["flujo_etiqueta"]}</p><h2>{T["flujo_h2"]}</h2><p>{T["flujo_p"]}</p></header>
          <div class="flujo-grid">
            <ol class="pasos">{pasos}</ol>
            <div class="escena" aria-live="polite">{escenas}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="seccion" id="servicios" style="padding-top:0">
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{T["serv_etiqueta"]}</p><h2>{T["serv_h2"]}</h2></header>
        <div class="servicios">
          <div class="pestanas" role="tablist" aria-label="{T["serv_etiqueta"]}">{pestanas}</div>
          <div class="vitrina"><div class="vitrina__rejilla" aria-hidden="true"></div>{paneles}</div>
        </div>
      </div>
    </section>

    <section class="seccion" id="caso" style="background:var(--blanco);border-block:1px solid var(--linea)">
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{T["caso_etiqueta"]}</p><h2>{T["caso_h2"]}</h2><p>{T["caso_intro"]}</p></header>
        <div class="caso">
          <div class="caso__fotos" data-revelar>
            <div class="caso__escritorio"><div class="ventana__barra"><i></i><i></i><i></i><span>acarreosmakena.com</span></div><img src="{pre}img/caso-acarreos-escritorio.webp" alt="Página web de Acarreos Makena en computadora" width="1440" height="900" loading="lazy"></div>
            <div class="caso__movil"><img src="{pre}img/caso-acarreos-movil.webp" alt="Página web de Acarreos Makena en celular" width="390" height="844" loading="lazy"></div>
          </div>
          <div data-revelar>
            <h3>{T["caso_nombre"]}</h3>
            <p class="caso__sector">{T["caso_sector"]}</p>
            <ul class="logros">{logros}</ul>
            <a class="boton boton--marca" href="https://acarreosmakena.com/" target="_blank" rel="noopener">{T["caso_cta"]} {I["flecha"]}</a>
            <div class="medida"><i>{I["rayo"]}</i><span><b>{T["medida_t"]}</b>{T["medida_p"]}</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="seccion">
      <div class="contenedor">
        <header class="cabeza cabeza--centro" data-revelar><p class="etiqueta">{T["proc_etiqueta"]}</p><h2>{T["proc_h2"]}</h2></header>
        <ol class="proceso">{proceso}</ol>
        <p class="etiqueta" style="text-align:center;margin-top:60px">{T["tec_titulo"]}</p>
        <div class="tecnologias">{tecnologias}</div>
      </div>
    </section>

    <section class="seccion" id="preguntas" style="padding-top:0">
      <div class="contenedor">
        <header class="cabeza cabeza--centro" data-revelar><p class="etiqueta">{T["faq_etiqueta"]}</p><h2>{T["faq_h2"]}</h2></header>
        <div class="preguntas">{faqs}</div>
      </div>
    </section>
  </main>

  <footer class="cierre" id="contacto">
    <div class="contenedor">
      <div class="cierre__grid">
        <h2>{T["cierre_h2"]}</h2>
        <div class="cierre__texto">
          <p>{T["cierre_p"]}</p>
          <div class="cierre__botones">
            <a class="boton boton--blanco" href="{wa}"{wa_attr}>{I["wa"]} {T["cierre_wa"]}</a>
            {boton_correo}
          </div>
        </div>
      </div>
      <div class="pie">
        <a class="marca" href="{pre or './'}">{LOGO}Integrafy</a>
        <nav><a href="#servicios">{T["nav"][0]}</a><a href="#como-funciona">{T["nav"][1]}</a><a href="#caso">{T["nav"][2]}</a><a href="{pre}{T["otra_ruta"] or './'}">{T["otra_nombre"]}</a></nav>
        <span>{T["pie_derechos"]}</span>
      </div>
    </div>
  </footer>

  <script>window.INTEGRAFY_AVISOS = {avisos_json};</script>
  <script src="{pre}js/main.js?v=2" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(RAIZ, "en"), exist_ok=True)
    for T, destino in ((ES, "index.html"), (EN, "en/index.html")):
        with open(os.path.join(RAIZ, destino), "w", encoding="utf-8", newline="\n") as f:
            f.write(pagina(T))
        print("ok", destino)
    if not CONFIG["whatsapp"]:
        print("AVISO: falta el número de WhatsApp en CONFIG; los botones llevan a #contacto.")
