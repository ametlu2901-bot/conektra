"""Sección de servicios de Integrafy: pestañas con ícono, puntos y barra de progreso,
y una maqueta tipo aplicación por servicio, con tarjetas flotantes encima."""

TEXTOS = {
    "es": dict(
        incluye="Incluye",
        tabs=[
            ("Páginas web y SEO", "Diseñadas a la medida de tu marca, rápidas en celular y listas para aparecer en Google.", "web",
             ["Diseño a la medida de tu marca", "SEO técnico y páginas por servicio", "Formularios conectados a tu CRM"]),
            ("CRM a la medida", "Tus clientes, cotizaciones y seguimientos en un solo lugar.", "crm",
             ["Etapas de venta a tu manera", "Recordatorios y seguimientos", "Reportes de ventas al día"]),
            ("Integraciones API", "Tus sistemas hablan entre sí y con servicios externos.", "rayo",
             ["WhatsApp, pagos y facturación", "Sincronización en tiempo real", "Alertas si algo falla"]),
            ("ERP y automatizaciones", "Inventario, facturación y procesos que se actualizan solos.", "erp",
             ["Inventario y facturación conectados", "Tareas que se ejecutan solas", "Tableros para decidir con datos"]),
        ],
        web=dict(url="tunegocio.com", nav=["Inicio", "Servicios", "Contacto"], h="Mudanzas en todo el país", p="Cotiza en minutos y recibe tu precio por WhatsApp.",
                 cta="Cotizar ahora", f_titulo="Nuevo formulario", f_texto="Enviado al CRM",
                 serp_u="tunegocio.com › mudanzas", serp_t="Mudanzas en todo el país | Tu negocio", serp_d="Camiones, personal y cobertura nacional. Cotiza por WhatsApp.",
                 movil="Cotiza en minutos"),
        crm=dict(titulo="Oportunidades", buscar="Buscar cliente…", total="Total en proceso",
                 cols=[("Nuevos", [("MP", "María Pérez", "Mudanza", "B/. 450", "web"), ("CR", "Carlos Ruiz", "Flete", "B/. 180", "wa")]),
                       ("Cotizados", [("AG", "Ana Gómez", "Oficina", "B/. 380", "web"), ("LD", "Luis Díaz", "Escombros", "B/. 120", "wa")]),
                       ("Ganados", [("RV", "Rosa Vega", "Mudanza", "B/. 520", "web")])],
                 rec_t="Recordatorio", rec_p="Llamar a Ana Gómez · mañana 10:00"),
        api=dict(titulo="Flujo: formulario → CRM → WhatsApp", pasos=["Formulario", "API", "CRM", "WhatsApp"],
                 c="// nuevo cliente desde la página web", campos=[("nombre", "María Pérez"), ("servicio", "Mudanza"), ("canal", "web")],
                 log=[("POST /clientes", "200", "84 ms"), ("Mensaje de confirmación", "Enviado", "WhatsApp"), ("Fila agregada al reporte", "OK", "Sheets")],
                 ok_t="Sincronizado", ok_p="3 sistemas actualizados en 1,2 s"),
        erp=dict(menu=["Resumen", "Ventas", "Inventario", "Facturas"], titulo="Resumen del mes",
                 kpis=[("Ventas", "B/. 12.4k", "+12%"), ("Facturas", "86", "+8%"), ("Ticket promedio", "B/. 144", "+3%")],
                 grafico="Ventas por semana", tabla_t="Últimas facturas",
                 facturas=[("A-2381", "María Pérez", "B/. 450", "Pagada"), ("A-2380", "Grupo Delta", "B/. 1,280", "Pagada"), ("A-2379", "Luis Díaz", "B/. 120", "Pendiente")],
                 alerta_t="Stock bajo en 3 productos", alerta_p="Orden de compra creada sola"),
    ),
    "en": dict(
        incluye="Includes",
        tabs=[
            ("Websites and SEO", "Custom-designed for your brand, fast on mobile and built to show up on Google.", "web",
             ["Designed around your brand", "Technical SEO and service pages", "Forms connected to your CRM"]),
            ("Custom CRM", "Your customers, quotes and follow-ups in one place.", "crm",
             ["Sales stages your way", "Reminders and follow-ups", "Up-to-date sales reports"]),
            ("API integrations", "Your systems talk to each other and to external services.", "rayo",
             ["WhatsApp, payments and invoicing", "Real-time sync", "Alerts if something fails"]),
            ("ERP and automation", "Inventory, invoicing and processes that update themselves.", "erp",
             ["Connected inventory and invoicing", "Tasks that run on their own", "Dashboards to decide with data"]),
        ],
        web=dict(url="yourbusiness.com", nav=["Home", "Services", "Contact"], h="Moving services nationwide", p="Get a quote in minutes and your price on WhatsApp.",
                 cta="Get a quote", f_titulo="New form submission", f_texto="Sent to the CRM",
                 serp_u="yourbusiness.com › moving", serp_t="Moving services nationwide | Your Business", serp_d="Trucks, crew and nationwide coverage. Get a quote on WhatsApp.",
                 movil="Quote in minutes"),
        crm=dict(titulo="Opportunities", buscar="Search customer…", total="Total in pipeline",
                 cols=[("New", [("MP", "Maria Perez", "Moving", "$450", "web"), ("CR", "Carlos Ruiz", "Freight", "$180", "wa")]),
                       ("Quoted", [("AG", "Ana Gomez", "Office", "$380", "web"), ("LD", "Luis Diaz", "Debris", "$120", "wa")]),
                       ("Won", [("RV", "Rosa Vega", "Moving", "$520", "web")])],
                 rec_t="Reminder", rec_p="Call Ana Gomez · tomorrow 10:00"),
        api=dict(titulo="Flow: form → CRM → WhatsApp", pasos=["Form", "API", "CRM", "WhatsApp"],
                 c="// new customer from the website", campos=[("name", "Maria Perez"), ("service", "Moving"), ("channel", "web")],
                 log=[("POST /customers", "200", "84 ms"), ("Confirmation message", "Sent", "WhatsApp"), ("Row added to report", "OK", "Sheets")],
                 ok_t="Synced", ok_p="3 systems updated in 1.2 s"),
        erp=dict(menu=["Overview", "Sales", "Inventory", "Invoices"], titulo="This month",
                 kpis=[("Sales", "$12.4k", "+12%"), ("Invoices", "86", "+8%"), ("Average ticket", "$144", "+3%")],
                 grafico="Sales per week", tabla_t="Latest invoices",
                 facturas=[("A-2381", "Maria Perez", "$450", "Paid"), ("A-2380", "Delta Group", "$1,280", "Paid"), ("A-2379", "Luis Diaz", "$120", "Pending")],
                 alerta_t="Low stock on 3 products", alerta_p="Purchase order created automatically"),
    ),
}


def ventana(titulo, cuerpo, clase=""):
    return (f'<div class="ventana {clase}"><div class="ventana__barra"><i></i><i></i><i></i><span>{titulo}</span></div>'
            f'<div class="ventana__cuerpo">{cuerpo}</div></div>')


def flotante(icono, titulo, texto, clase):
    return f'<div class="flotante {clase}"><span class="flotante__ico">{icono}</span><span><b>{titulo}</b><small>{texto}</small></span></div>'


def seccion(lang, I):
    X = TEXTOS[lang]
    # ---------- pestañas ----------
    pestanas = []
    for i, (t, d, ico, puntos) in enumerate(X["tabs"]):
        lis = "".join(f"<li>{I['check']}{p}</li>" for p in puntos)
        pestanas.append(
            f'<button type="button" class="pestana{" activa" if i == 0 else ""}" role="tab" id="tab-{i}" aria-controls="panel-{i}" '
            f'aria-selected="{str(i == 0).lower()}" data-tab="{i}">'
            f'<span class="pestana__ico">{I[ico]}</span>'
            f'<span class="pestana__txt"><h3>{t}</h3><p>{d}</p><ul class="pestana__lista" aria-label="{X["incluye"]}">{lis}</ul></span>'
            f'<span class="pestana__progreso" aria-hidden="true"><i></i></span></button>')

    # ---------- maqueta 1: página web ----------
    w = X["web"]
    nav = "".join(f"<span>{n}</span>" for n in w["nav"])
    web_cuerpo = (
        f'<div class="sitio"><div class="sitio__nav"><b class="sitio__logo"></b>{nav}<em>{w["cta"]}</em></div>'
        f'<div class="sitio__hero"><div><h4>{w["h"]}</h4><p>{w["p"]}</p><span class="sitio__cta">{I["wa"]} {w["cta"]}</span></div>'
        f'<div class="sitio__foto" aria-hidden="true"><i></i><i></i><i></i></div></div>'
        f'<div class="serp"><small>{w["serp_u"]}</small><b>{w["serp_t"]}</b><span class="serp__estrellas">★★★★★</span> {w["serp_d"]}</div></div>')
    movil = (f'<div class="telefono" aria-hidden="true"><div class="telefono__pantalla"><b class="sitio__logo"></b>'
             f'<h5>{w["h"]}</h5><span class="telefono__linea"></span><span class="telefono__linea corta"></span>'
             f'<span class="telefono__cta">{I["wa"]} {w["movil"]}</span></div></div>')
    panel_web = (ventana(w["url"], web_cuerpo, "ventana--sitio") + movil +
                 flotante(I["check"], w["f_titulo"], w["f_texto"], "flotante--arriba"))

    # ---------- maqueta 2: CRM ----------
    c = X["crm"]
    cols = []
    for col, leads in c["cols"]:
        tarjetas = "".join(
            f'<div class="lead"><div class="lead__cab"><span class="avatar">{ini}</span><b>{n}</b></div>'
            f'<div class="lead__pie"><span class="etiqueta-mini etiqueta-mini--{canal}">{"Web" if canal == "web" else "WhatsApp"}</span>'
            f'<span>{s}</span><strong>{monto}</strong></div></div>'
            for ini, n, s, monto, canal in leads)
        cols.append(f'<div class="kanban__col"><h5>{col}<span>{len(leads)}</span></h5>{tarjetas}</div>')
    crm_cuerpo = (f'<div class="app-cab"><b>{c["titulo"]}</b><span class="buscador">{c["buscar"]}</span></div>'
                  f'<div class="kanban">{"".join(cols)}</div>'
                  f'<div class="app-pie"><span>{c["total"]}</span><b>{"B/. 1,650" if lang == "es" else "$1,650"}</b></div>')
    panel_crm = ventana("CRM", crm_cuerpo) + flotante(I["crm"], c["rec_t"], c["rec_p"], "flotante--arriba")

    # ---------- maqueta 3: integraciones ----------
    a = X["api"]
    cadena = '<i class="cadena__linea"></i>'.join(f'<span class="cadena__nodo">{p}</span>' for p in a["pasos"])
    campos = ",\n".join(f'  <span class="n">"{k}"</span>: <span class="s">"{v}"</span>' for k, v in a["campos"])
    log = "".join(f'<div class="registro"><i></i><span class="registro__txt">{t}</span><span class="pill">{e}</span><span class="registro__meta">{m}</span></div>' for t, e, m in a["log"])
    api_cuerpo = (f'<div class="app-cab"><b>{a["titulo"]}</b><span class="vivo">● Live</span></div>'
                  f'<div class="cadena">{cadena}</div>'
                  f'<div class="codigo"><span class="c">{a["c"]}</span>\n<span class="k">POST</span> /webhook\n{{\n{campos}\n}}</div>'
                  f'<div class="registros">{log}</div>')
    panel_api = ventana("api.integrafy", api_cuerpo) + flotante(I["rayo"], a["ok_t"], a["ok_p"], "flotante--arriba")

    # ---------- maqueta 4: ERP ----------
    e = X["erp"]
    menu = "".join(f'<span class="{"activo" if j == 0 else ""}">{m}</span>' for j, m in enumerate(e["menu"]))
    kpis = "".join(f'<div class="kpi"><span>{n}</span><b>{v}</b><em>{d}</em></div>' for n, v, d in e["kpis"])
    filas = "".join(
        f'<div class="tabla__fila"><span>#{n}</span><span>{cli}</span><b>{monto}</b><span class="pill {"pill--ok" if j < 2 else "pill--pend"}">{est}</span></div>'
        for j, (n, cli, monto, est) in enumerate(e["facturas"][:2]))
    grafico = ('<svg class="grafico" viewBox="0 0 300 90" preserveAspectRatio="none" aria-hidden="true">'
               '<defs><linearGradient id="g-area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b5bff" stop-opacity=".28"/><stop offset="1" stop-color="#3b5bff" stop-opacity="0"/></linearGradient></defs>'
               '<path d="M0 70 C30 64 45 52 75 55 S120 40 150 42 S200 22 225 28 S270 12 300 8 V90 H0Z" fill="url(#g-area)"/>'
               '<path d="M0 70 C30 64 45 52 75 55 S120 40 150 42 S200 22 225 28 S270 12 300 8" fill="none" stroke="#3b5bff" stroke-width="2.5" vector-effect="non-scaling-stroke"/>'
               '<path d="M0 80 C40 76 70 70 100 72 S160 60 190 62 S250 48 300 44" fill="none" stroke="#13c2a3" stroke-width="2" stroke-dasharray="5 5" vector-effect="non-scaling-stroke"/></svg>')
    erp_cuerpo = (f'<div class="erp"><nav class="erp__menu"><b class="sitio__logo"></b>{menu}</nav><div class="erp__main">'
                  f'<div class="app-cab"><b>{e["titulo"]}</b><span class="buscador">2026</span></div>'
                  f'<div class="kpis">{kpis}</div>'
                  f'<div class="caja"><span class="caja__t">{e["grafico"]}</span>{grafico}</div>'
                  f'<div class="caja"><span class="caja__t">{e["tabla_t"]}</span><div class="tabla">{filas}</div></div></div></div>')
    panel_erp = ventana("ERP", erp_cuerpo, "ventana--erp") + flotante(I["erp"], e["alerta_t"], e["alerta_p"], "flotante--arriba flotante--ambar")

    paneles = "".join(
        f'<div class="panel{" activo" if i == 0 else ""}" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}>{p}</div>'
        for i, p in enumerate([panel_web, panel_crm, panel_api, panel_erp]))
    return "\n".join(pestanas), paneles
