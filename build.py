"""Genera la página de Conektra en español (index.html) y en inglés (en/index.html).

Uso:  python build.py
Los datos de contacto se cambian en CONFIG. Los textos, en ES y EN.
"""
import json, os, urllib.parse
import servicios
import integraciones
import paginas

CONFIG = {
    "dominio": "https://ametlu2901-bot.github.io/conektra/",  # cambiar a https://conektra.dev/ cuando se compre el dominio
    "whatsapp": "50765523134",                  # solo números con código de país, p. ej. 50760000000
    "correo": "",                               # p. ej. hola@conektra.dev
    # URL /exec de la hoja «Conektra — CRM» (programa en crm/Codigo.gs)
    # testimonio real de Acarreos Makena: si "texto" está vacío se muestra un resumen, sin comillas ni persona
    "testimonio": dict(texto="", nombre="", cargo=""),
    "crm": "https://script.google.com/macros/s/AKfycbxvoagKEQKMfhn8mdVk7cknuZfPJyKL1HPd4mb6tjxPWa29TSFh78hAsZ2qJBwcZGWl/exec",
}

RAIZ = os.path.dirname(os.path.abspath(__file__))

# ---------- íconos (trazos simples, heredan el color) ----------
I = {
    "flecha": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.2-1.4A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.2-1.15l-.3-.18-3.1.82.83-3-.2-.31a8.2 8.2 0 1 1 6.97 3.82Zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.53.06a6.7 6.7 0 0 1-3.34-2.92c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43-.06-.12-.55-1.33-.76-1.82-.2-.48-.4-.41-.55-.42h-.47a.9.9 0 0 0-.66.31 2.77 2.77 0 0 0-.86 2.06 4.8 4.8 0 0 0 1 2.56 11 11 0 0 0 4.22 3.73c1.57.68 2.19.74 2.98.62.48-.07 1.46-.6 1.67-1.18.2-.58.2-1.08.14-1.18-.06-.1-.22-.17-.47-.29Z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18"/></svg>',
    "crm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0M16 6h5M16 10h5M18 14h3"/></svg>',
    "erp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4V5Z"/></svg>',
    "pago": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M7 15h4"/></svg>',
    "hoja": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M4 9h16M4 15h16M10 3v18"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4-4"/></svg>',
    "plano": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2Z"/><path d="M9 4v14M15 6v14"/></svg>',
    "codigo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/></svg>',
    "soporte": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 13v-1a8 8 0 0 1 16 0v1"/><rect x="3" y="13" width="4" height="6" rx="1.5"/><rect x="17" y="13" width="4" height="6" rx="1.5"/><path d="M19 19a4 4 0 0 1-4 3h-2"/></svg>',
    "nube": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9.5 4.3 4.3 0 0 0 7 18Z"/></svg>',
    "base": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/></svg>',
    "enlace": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
    "factura": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3Z"/><path d="M9 8h6M9 12h6"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.6v12.8a1 1 0 0 0 1.5.86l10.2-6.4a1 1 0 0 0 0-1.72L9.5 4.74A1 1 0 0 0 8 5.6Z"/></svg>',
    "estrella": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/></svg>',
    "escudo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m8.8 12.2 2.2 2.2 4.4-4.6"/></svg>',
    "rayo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"/></svg>',
}
LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#10241d"/><circle cx="10" cy="11" r="3.2" fill="#8fd9b0"/><circle cx="22" cy="21" r="3.2" fill="#2fbf71"/><path d="M10 14.5v2a4.5 4.5 0 0 0 4.5 4.5H18.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M22 17.5v-2A4.5 4.5 0 0 0 17.5 11H13.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".55"/></svg>'
NUCLEO = '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="10" cy="11" r="3.4" fill="#8fd9b0"/><circle cx="22" cy="21" r="3.4" fill="#2fbf71"/><path d="M10 14.5v2a4.5 4.5 0 0 0 4.5 4.5H18.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><path d="M22 17.5v-2A4.5 4.5 0 0 0 17.5 11H13.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".55"/></svg>'

ES = dict(
    lang="es", ruta="", otra_ruta="en/", otra_etiqueta="EN", otra_nombre="English",
    titulo="Conektra | Páginas web para negocios de servicios en Panamá",
    descripcion="Páginas web para negocios de servicios en Panamá que cotizan por WhatsApp: aparece en Google, recibe cada solicitud de cotización en orden y muestra tus reseñas.",
    nav=["Servicios", "Cómo funciona", "Casos", "Preguntas"], cta="Escríbenos",
    wa_msg="Hola Conektra, tengo un negocio de servicios y quiero conseguir más clientes.",
    chip="Para negocios de servicios en Panamá",
    h1='<span class="titular__l1">Tus cotizaciones,</span> <em>en orden.</em> <span class="titular__l3">Tus clientes, desde Google.</span>',
    lead="Para negocios que viven de cotizar por WhatsApp: mudanzas, técnicos, instalaciones, limpieza y más. Te armamos una página que te trae clientes desde Google y guarda cada solicitud para que ninguna se quede sin respuesta.",
    ver_casos="Mira un caso real", ver_como="Mira cómo funciona",
    portada_alt="Dueño de una empresa de mudanzas revisando en su celular los mensajes de clientes junto a su camión",
    portada_pie="Menos chats perdidos. Más trabajos cerrados.",
    prueba='<b>Acarreos Makena:</b> página, Google y cotizaciones en orden',
    chip_cta="Hablemos", prueba_etiqueta="Caso de éxito · Mudanzas", prueba_texto="Página, Google y cotizaciones en orden",
    confianza=["Hecho para negocios de servicios", "Cotizaciones en Google Sheets", "Soporte después de entregar"],
    nodos=[("Google", "Te encuentran", "lupa"), ("Tu hoja", "Cotizaciones", "hoja"), ("Seguimiento", "Recordatorios", "rayo"), ("WhatsApp", "Mensajes", "chat"), ("Tu página", "Formulario", "web"), ("Reseñas", "Clientes felices", "check")],
    avisos=[("Nueva cotización", "Guardada en tu hoja"), ("Cliente desde Google", "Pidió precio por la página"), ("Seguimiento", "A Ana le falta respuesta"), ("Nueva reseña", "★★★★★ lista para aprobar")],
    franja_texto="Te ayudamos a",
    palabras=["aparecer en Google", "ordenar tus cotizaciones", "responder a tiempo", "mostrar tus reseñas", "cerrar más trabajos"],
    franja_cta="Cuéntanos de tu negocio",
    escena_chip="Automático", escena_paso="Paso",
    pie_servicios="Servicios", pie_empresa="Conektra", pie_contacto="Contacto", pie_hecho="Hecho en Panamá, para negocios de Panamá.",
    marquesina=["Mudanzas", "Aire acondicionado", "Cámaras de seguridad", "Limpieza", "Fumigación", "Talleres", "Plomería", "Electricidad"],
    dol_etiqueta="¿Te suena?", dol_h2="Lo que le pasa a todo negocio que vive de cotizar.",
    dol_p="Si tu negocio es de servicios, seguro te pasa al menos uno de estos.", dol_con="Con Conektra",
    dolores=[("«Te escribo luego»… y nunca respondiste", "Se te acumulan los chats y una cotización se queda sin respuesta. Ese cliente ya contrató a otro.", "Cada solicitud queda guardada con su estado. Sabes a quién te falta responder.", "chat"),
             ("Nadie te encuentra en Google", "Buscan «mudanzas en Panamá» o «técnico de aire acondicionado» y salen otros, aunque tú trabajes mejor.", "Páginas por servicio y por zona, pensadas para lo que tus clientes buscan.", "lupa"),
             ("Repites lo mismo en cada chat", "«¿Qué incluye?», «¿Van a mi zona?», «¿Cuánto cuesta?». Todos los días, a todos.", "Tu página responde por ti y el formulario pide los datos que necesitas para cotizar.", "web"),
             ("Tu buen trabajo no se ve", "Tus clientes quedan contentos, pero alguien que no te conoce no tiene cómo saberlo.", "Reseñas con estrellas en tu página. Tú decides cuáles se publican.", "check")],
    dol_minis=[("chat", "Hola, ¿me cotizan una mudanza para el sábado?", "Visto · hace 3 días"),
               ("google", "mudanzas en panamá", "Tu negocio no aparece"),
               ("chat", "¿Van a mi zona? ¿Cuánto cuesta?", "12 chats sin responder"),
               ("estrellas", "☆☆☆☆☆", "0 reseñas a la vista")],
    sectores_t="Hecho para negocios como",
    flujo_etiqueta="Cómo funciona", flujo_h2="De «¿me cotizas?» a <em>trabajo cerrado.</em>", flujo_insignia=("Más clientes,", "menos trabajo manual."), flujo_ventana="Conektra · Cotizaciones",
    flujo_p="Así se mueve un cliente cuando tu página, tu WhatsApp y tus cotizaciones trabajan juntos.",
    pasos=[("Te encuentra y te escribe", "Llega a tu página desde Google y pide cotización, o te escribe por WhatsApp."),
           ("Queda guardado", "La solicitud se guarda sola en tu hoja, con nombre, servicio y fecha."),
           ("Cotizas y das seguimiento", "Cada cotización avanza por etapas y sabes a quién te falta responder."),
           ("Cierras y te califica", "Haces el trabajo y el cliente deja su reseña en tu página.")],
    esc1=dict(cab="WhatsApp", est="En línea", b1="Hola, ¿me pueden cotizar una mudanza para el sábado?", b2="¡Claro! Ya registramos tu solicitud. Te enviamos la cotización en unos minutos."),
    esc2=dict(cab="Nueva solicitud", est="Hoja", filas=[("Nombre", "María Pérez"), ("Canal", "Formulario web"), ("Servicio", "Mudanza"), ("Etapa", "Nuevo")]),
    esc3=dict(cab="Cotización #1042", est="En revisión", filas=[("Servicio", "Mudanza residencial"), ("Fecha", "Sábado 9:00"), ("Seguimiento", "Recordatorio en 24 h")]),
    esc4=dict(cab="Trabajo #1042", est="Ganado", filas=[("Cliente", "María Pérez"), ("Servicio", "Mudanza residencial"), ("Reseña", "★★★★★")], total=("Total", "B/. 450")),
    serv_etiqueta="Servicios", serv_h2="Empieza con lo que necesitas hoy. Agrega más cuando crezcas.",
    servicios=[],
    caso_etiqueta="La experiencia de nuestros clientes", caso_h2="Acarreos Makena pasó del WhatsApp suelto a <em>cotizaciones en orden.</em>",
    caso_categoria="Mudanzas y servicios · Panamá", caso_estado="En línea", caso_tags_t="Qué incluyó el proyecto",
    caso_tags=["Página web", "SEO local", "Google Sheets", "Reseñas"],
    caso_chips=[("hoja", "Formulario → Google Sheets"), ("estrella", "Reseñas con aprobación"), ("lupa", "Páginas por servicio y zona")],
    caso_bloques=[("El problema", "Las solicitudes de cotización llegaban sueltas por WhatsApp, sin un lugar donde verlas todas."),
                  ("La solución", "Una página con sus servicios y sus zonas, un formulario conectado a Google Sheets y reseñas con estrellas."),
                  ("Lo que consiguió", "Cada solicitud queda registrada con su estado: nuevo, cotizado, ganado. Y el dueño decide qué reseñas se publican.")],
    caso_resumen="Le hicimos a Acarreos Makena una página con sus servicios y sus zonas, un formulario que guarda cada cotización en su hoja de Google Sheets y reseñas con estrellas que el dueño aprueba antes de publicarlas.",
    cifras=[("10", "páginas listas para Google"), ("5", "servicios con página propia"), ("3", "zonas con página propia"), ("24/7", "recibiendo cotizaciones")],
    caso_intro="Acarreos Makena es una empresa de mudanzas en Panamá, justo el tipo de negocio con el que trabajamos. Cada proyecto se diseña desde cero: tu página no se parecerá a esta, se parecerá a tu negocio.",
    medida_t="Hecho a tu medida", medida_p="Tu marca, tus colores, tus servicios y tus zonas. Diseñamos tu página según tu rubro y tu forma de trabajar, no con plantillas.",
    caso_nombre="Acarreos Makena", caso_sector="Mudanzas, acarreos y fletes en Panamá",
    logros=[("Página web con dominio propio", "Diseño a la medida, rápida en celular y con botón directo a WhatsApp."),
            ("SEO con páginas por servicio y por zona", "Páginas pensadas para cada búsqueda, sitemap y Search Console configurados."),
            ("Cotizaciones en Google Sheets", "Cada solicitud del formulario queda registrada con su estado: nuevo, cotizado, ganado."),
            ("Reseñas con aprobación", "Los clientes califican con estrellas y el dueño decide qué se publica.")],
    caso_cta="Ver la página en vivo",
    proc_etiqueta="Proceso", proc_h2="Así trabajamos contigo.",
    proceso=[("Diagnóstico", "Vemos cómo te llegan hoy los clientes y dónde se pierden cotizaciones."),
             ("Propuesta", "Te mostramos qué necesita tu página, con tiempos y precio claros."),
             ("Desarrollo", "Construimos por etapas y te mostramos avances para que pruebes desde temprano."),
             ("Soporte", "Te acompañamos después de entregar: cambios, mejoras y nuevas funciones.")],
    proc_recibes="Recibes", proc_entregables=["Mapa de cómo te llegan los clientes", "Plan con precio y tiempos", "Avances que puedes probar", "Soporte y mejoras"],
    tec_titulo="Trabajamos con",
    tecnologias=["WhatsApp", "Google Search Console", "Google Sheets", "Perfil de Empresa en Google", "SEO local", "Formularios de cotización", "Reseñas con estrellas", "Dominio propio", "APIs y webhooks", "Google Workspace"],
    faq_etiqueta="Preguntas frecuentes", faq_h2="Lo que más nos preguntan.",
    faqs=[("Ya tengo WhatsApp e Instagram, ¿para qué una página?", "Porque cuando alguien busca «mudanzas en Panamá» o «técnico de aire acondicionado» en Google, no ve tu Instagram: ve páginas web. Tu página te pone en esas búsquedas y manda a esa persona directo a tu WhatsApp."),
          ("¿Cuánto cuesta?", "Depende de cuántos servicios y zonas quieras mostrar y de qué funciones necesites. Te enviamos una propuesta con precio claro antes de empezar."),
          ("¿Tengo que saber de tecnología?", "No. Tus cotizaciones quedan en una hoja de Google Sheets que se usa como cualquier tabla, y te explicamos cómo funciona."),
          ("¿Cómo funcionan las reseñas?", "Tus clientes te califican con estrellas desde la página y tú decides cuáles se publican."),
          ("¿Qué pasa después de la entrega?", "Te acompañamos con soporte y mejoras. Si agregas un servicio o una zona nueva, lo sumamos a tu página."),
          ("¿Mis datos quedan seguros?", "Tus datos quedan en tus propias cuentas, como tu Google Sheets. Usamos accesos con permisos mínimos y te entregamos todo documentado.")],
    form=dict(etiqueta="Contacto", h2="Cuéntanos de tu negocio.", p="Respondemos en menos de un día hábil con los próximos pasos. Sin compromiso.",
              puntos=["Revisamos cómo te llegan hoy los clientes", "Propuesta con alcance y precio claros", "Te escribimos por el medio que prefieras"],
              nombre="Tu nombre", empresa="Negocio", contacto="Correo o WhatsApp", necesita="¿Qué necesitas?",
              opciones=["Página web", "Aparecer en Google", "Cotizaciones en orden", "Reseñas", "Otro"],
              presupuesto="Presupuesto aproximado", rangos=["Aún no lo sé", "Menos de $1,000", "$1,000 – $3,000", "$3,000 – $10,000", "Más de $10,000"],
              mensaje="Cuéntanos un poco", ph_mensaje="¿A qué se dedica tu negocio y cómo te llegan hoy las cotizaciones?",
              enviar="Enviar mensaje", enviando="Enviando…", error="Escribe tu nombre y un correo o WhatsApp para responderte.",
              ok_t="¡Recibimos tu mensaje!", ok_p="Te escribimos muy pronto. Si es urgente, sigue la conversación por WhatsApp.", ok_wa="Seguir por WhatsApp",
              privacidad="Usamos tus datos solo para responderte."),
    cierre_h2="Más trabajos, <em>cero cotizaciones perdidas.</em>",
    cierre_p="Escríbenos y cuéntanos a qué se dedica tu negocio. Te mostramos cómo conseguir más clientes desde Google y tener cada cotización en orden.",
    cierre_wa="Escríbenos por WhatsApp", cierre_correo="Enviar un correo",
    pie_derechos="© 2026 Conektra. Páginas web para negocios de servicios.",
)

EN = dict(
    lang="en", ruta="en/", otra_ruta="", otra_etiqueta="ES", otra_nombre="Español",
    titulo="Conektra | Websites for service businesses in Panama",
    descripcion="Websites for service businesses in Panama that quote on WhatsApp: show up on Google, get every quote request organized and show off your reviews.",
    nav=["Services", "How it works", "Case study", "FAQ"], cta="Message us",
    wa_msg="Hi Conektra, I run a service business and want more customers.",
    chip="For service businesses in Panama",
    h1='<span class="titular__l1">Your quotes,</span> <em>organized.</em> <span class="titular__l3">Your customers, from Google.</span>',
    lead="For businesses that live on quoting over WhatsApp: movers, technicians, installers, cleaners and more. We build you a website that brings customers from Google and saves every request so none goes unanswered.",
    ver_casos="See a real case", ver_como="See how it works",
    portada_alt="Owner of a moving company checking customer messages on the phone next to the truck",
    portada_pie="Fewer lost chats. More closed jobs.",
    prueba='<b>Acarreos Makena:</b> website, Google and organized quotes',
    chip_cta="Let's talk", prueba_etiqueta="Success story · Moving", prueba_texto="Website, Google and organized quotes",
    confianza=["Built for service businesses", "Quotes in Google Sheets", "Support after launch"],
    nodos=[("Google", "They find you", "lupa"), ("Quotes", "In your sheet", "hoja"), ("Follow-up", "Reminders", "rayo"), ("WhatsApp", "Messages", "chat"), ("Your website", "Form", "web"), ("Reviews", "Happy customers", "check")],
    avisos=[("New quote request", "Saved to your sheet"), ("Customer from Google", "Asked for a price on your site"), ("Follow-up", "Ana is waiting for a reply"), ("New review", "★★★★★ ready to approve")],
    franja_texto="We help you",
    palabras=["show up on Google", "organize your quotes", "reply on time", "show your reviews", "win more jobs"],
    franja_cta="Tell us about your business",
    escena_chip="Automatic", escena_paso="Step",
    pie_servicios="Services", pie_empresa="Conektra", pie_contacto="Contact", pie_hecho="Made in Panama, for Panama's businesses.",
    marquesina=["Movers", "Air conditioning", "Security cameras", "Cleaning", "Pest control", "Auto repair", "Plumbing", "Electricians"],
    dol_etiqueta="Sound familiar?", dol_h2="What happens to every business that lives on quotes.",
    dol_p="If you run a service business, at least one of these is probably happening to you.", dol_con="With Conektra",
    dolores=[("\"I'll get back to you\"… and you never did", "Chats pile up and a quote goes unanswered. That customer already hired someone else.", "Every request is saved with its status. You know exactly who's still waiting.", "chat"),
             ("Nobody finds you on Google", "People search \"movers in Panama\" or \"AC technician\" and others show up, even if your work is better.", "Pages for each service and area, built around what your customers search for.", "lupa"),
             ("You repeat yourself in every chat", "\"What's included?\", \"Do you cover my area?\", \"How much?\". Every day, to everyone.", "Your website answers for you, and the form asks for what you need to quote.", "web"),
             ("Your good work goes unseen", "Your customers are happy, but someone new has no way of knowing it.", "Star reviews on your website. You decide which ones get published.", "check")],
    dol_minis=[("chat", "Hi, can I get a quote for a move on Saturday?", "Seen · 3 days ago"),
               ("google", "movers in panama", "Your business isn't there"),
               ("chat", "Do you cover my area? How much?", "12 unanswered chats"),
               ("estrellas", "☆☆☆☆☆", "0 reviews in sight")],
    sectores_t="Built for businesses like",
    flujo_etiqueta="How it works", flujo_h2="From \"can I get a quote?\" to <em>a closed job.</em>", flujo_insignia=("More customers,", "less manual work."), flujo_ventana="Conektra · Quotes",
    flujo_p="This is how a customer moves when your website, your WhatsApp and your quotes work together.",
    pasos=[("They find you and reach out", "They land on your website from Google and request a quote, or message you on WhatsApp."),
           ("It gets saved", "The request is saved to your sheet automatically, with name, service and date."),
           ("You quote and follow up", "Every quote moves through stages and you know who's still waiting."),
           ("You close and they rate you", "You do the job and the customer leaves a review on your website.")],
    esc1=dict(cab="WhatsApp", est="Online", b1="Hi, can I get a quote for a move this Saturday?", b2="Of course! We've logged your request. Your quote is on its way in a few minutes."),
    esc2=dict(cab="New request", est="Sheet", filas=[("Name", "Maria Perez"), ("Channel", "Website form"), ("Service", "Moving"), ("Stage", "New")]),
    esc3=dict(cab="Quote #1042", est="In review", filas=[("Service", "Home move"), ("Date", "Saturday 9:00"), ("Follow-up", "Reminder in 24 h")]),
    esc4=dict(cab="Job #1042", est="Won", filas=[("Customer", "Maria Perez"), ("Service", "Home move"), ("Review", "★★★★★")], total=("Total", "$450")),
    serv_etiqueta="Services", serv_h2="Start with what you need today. Add more as you grow.",
    servicios=[],
    caso_etiqueta="What our clients experience", caso_h2="Acarreos Makena went from scattered WhatsApp chats to <em>organized quotes.</em>",
    caso_categoria="Moving and services · Panama", caso_estado="Live", caso_tags_t="What the project included",
    caso_tags=["Website", "Local SEO", "Google Sheets", "Reviews"],
    caso_chips=[("hoja", "Form → Google Sheets"), ("estrella", "Reviews with approval"), ("lupa", "Pages per service and area")],
    caso_bloques=[("The problem", "Quote requests arrived scattered across WhatsApp, with no single place to see them all."),
                  ("The solution", "A website with its services and areas, a form connected to Google Sheets and star reviews."),
                  ("What it achieved", "Every request is logged with its status: new, quoted, won. And the owner decides which reviews go live.")],
    caso_resumen="We built Acarreos Makena a website with its services and areas, a form that saves every quote request to its Google Sheets spreadsheet, and star reviews the owner approves before they go live.",
    cifras=[("10", "pages ready for Google"), ("5", "services with their own page"), ("3", "areas with their own page"), ("24/7", "receiving quote requests")],
    caso_intro="Acarreos Makena is a moving company in Panama, exactly the kind of business we work with. Every project is designed from scratch: your website won't look like this one, it will look like your business.",
    medida_t="Made to measure", medida_p="Your brand, your colors, your services and your areas. We design your website around your trade and the way you work, not templates.",
    caso_nombre="Acarreos Makena", caso_sector="Moving, hauling and freight in Panama",
    logros=[("Website on its own domain", "Custom design, fast on mobile, with a direct WhatsApp button."),
            ("SEO with service and location pages", "Pages built for each search, plus sitemap and Search Console set up."),
            ("Quotes in Google Sheets", "Every quote request from the form is logged with its status: new, quoted, won."),
            ("Reviews with approval", "Customers rate with stars and the owner decides what gets published.")],
    caso_cta="See the live website",
    proc_etiqueta="Process", proc_h2="How we work with you.",
    proceso=[("Discovery", "We look at how customers reach you today and where quotes get lost."),
             ("Proposal", "We show you what your website needs, with clear timeline and price."),
             ("Build", "We build in stages and show you progress so you can test early."),
             ("Support", "We stay with you after launch: changes, improvements and new features.")],
    proc_recibes="You get", proc_entregables=["A map of how customers reach you", "A plan with price and timeline", "Progress you can test", "Support and improvements"],
    tec_titulo="We work with",
    tecnologias=["WhatsApp", "Google Search Console", "Google Sheets", "Google Business Profile", "Local SEO", "Quote request forms", "Star reviews", "Your own domain", "APIs and webhooks", "Google Workspace"],
    faq_etiqueta="FAQ", faq_h2="What people ask us most.",
    faqs=[("I already have WhatsApp and Instagram. Why a website?", "Because when someone searches \"movers in Panama\" or \"AC technician\" on Google, they don't see your Instagram: they see websites. Your website puts you in those searches and sends that person straight to your WhatsApp."),
          ("How much does it cost?", "It depends on how many services and areas you want to show and which features you need. We send you a proposal with a clear price before we start."),
          ("Do I need to know about technology?", "No. Your quotes land in a Google Sheets spreadsheet you use like any table, and we show you how it works."),
          ("How do reviews work?", "Your customers rate you with stars from your website and you decide which ones get published."),
          ("What happens after delivery?", "We stay with you for support and improvements. If you add a new service or area, we add it to your website."),
          ("Is my data safe?", "Your data stays in your own accounts, like your Google Sheets. We use least-privilege access and hand everything over documented.")],
    form=dict(etiqueta="Contact", h2="Tell us about your business.", p="We reply within one business day with next steps. No commitment.",
              puntos=["We look at how customers reach you today", "A proposal with clear scope and price", "We reach out the way you prefer"],
              nombre="Your name", empresa="Business", contacto="Email or WhatsApp", necesita="What do you need?",
              opciones=["Website", "Show up on Google", "Organized quotes", "Reviews", "Other"],
              presupuesto="Approximate budget", rangos=["Not sure yet", "Under $1,000", "$1,000 – $3,000", "$3,000 – $10,000", "Over $10,000"],
              mensaje="Tell us a bit more", ph_mensaje="What does your business do and how do quote requests reach you today?",
              enviar="Send message", enviando="Sending…", error="Add your name and an email or WhatsApp so we can reply.",
              ok_t="We got your message!", ok_p="We'll get back to you very soon. If it's urgent, continue on WhatsApp.", ok_wa="Continue on WhatsApp",
              privacidad="We only use your details to reply to you."),
    cierre_h2="More jobs, <em>zero lost quotes.</em>",
    cierre_p="Message us and tell us what your business does. We'll show you how to get more customers from Google and keep every quote organized.",
    cierre_wa="Message us on WhatsApp", cierre_correo="Send an email",
    pie_derechos="© 2026 Conektra. Websites for service businesses.",
)

# posiciones de los nodos alrededor del núcleo (porcentajes del diagrama)
POS = [(16, 18), (84, 22), (92, 58), (70, 90), (24, 86), (8, 52)]


def pagina(T):
    pre = "../" if T["ruta"] else ""
    url = CONFIG["dominio"] + T["ruta"]
    wa = f'https://wa.me/{CONFIG["whatsapp"]}?text={urllib.parse.quote(T["wa_msg"])}' if CONFIG["whatsapp"] else "#contacto"
    wa_attr = ' target="_blank" rel="noopener"' if CONFIG["whatsapp"] else ""
    correo = f'mailto:{CONFIG["correo"]}' if CONFIG["correo"] else ""

    # ritmo de cada línea: cuánto tarda un paquete en recorrerla y cuándo arranca
    CICLOS = [(2.6, 0.0), (3.1, 0.7), (2.8, 1.4), (3.4, 0.3), (2.9, 1.1), (3.2, 1.8)]
    PROFUNDIDAD = [1.0, 0.6, 1.3, 0.8, 1.2, 0.7]
    # los paquetes impares viajan del sistema hacia el núcleo; los pares, del núcleo hacia el sistema
    nodos = "\n".join(
        f'<div class="nodo" data-prof="{PROFUNDIDAD[i]}" style="left:{x}%;top:{y}%;--ciclo:{CICLOS[i][0]}s;'
        f'--llegada:{CICLOS[i][1]}s">'
        f'<i>{I[ico]}</i><span>{n}<small>{s}</small></span></div>'
        for i, ((n, s, ico), (x, y)) in enumerate(zip(T["nodos"], POS)))
    # curvas desde el núcleo (50,46) hacia cada nodo, en un lienzo de 100x92
    curva = lambda i, x, y: f'M50 46 Q {(50 + x) / 2 + (8 if i % 2 else -8)} {(46 + y * .92) / 2} {x} {y * .92}'
    rutas = "".join(f'<path class="ruta" id="ruta-{i}" d="{curva(i, x, y)}"/>' for i, (x, y) in enumerate(POS))
    flujos = "".join(f'<path class="flujo" d="{curva(i, x, y)}"/>' for i, (x, y) in enumerate(POS))
    paquetes = "".join(
        f'<g class="paquete"><circle r="2.4" fill="url(#g-halo)"/><circle r=".75" fill="#fff"/>'
        f'<animateMotion dur="{CICLOS[i][0]}s" begin="{CICLOS[i][1]}s" repeatCount="indefinite"'
        f'{"" if i % 2 == 0 else " keyPoints=\"1;0\" keyTimes=\"0;1\""}><mpath href="#ruta-{i}"/></animateMotion></g>'
        for i, _ in enumerate(POS))

    ICONOS_PAL = ["lupa", "hoja", "chat", "check", "rayo"]
    palabras = "".join(f'<span class="rotador__palabra">{p}</span>' for p in T["palabras"])
    iconos_franja = "".join(f'<span class="franja__ico" data-i="{j}" title="{p}">{I[ICONOS_PAL[j % len(ICONOS_PAL)]]}</span>' for j, p in enumerate(T["palabras"]))
    pasos = "\n".join(
        f'<li><button type="button" class="paso{" activo" if i == 0 else ""}" data-paso="{i}" aria-pressed="{str(i == 0).lower()}"><b>0{i + 1}</b><span class="paso__ico" aria-hidden="true">{I[("lupa", "hoja", "chat", "estrella")[i]]}</span><span><h3>{t}</h3><p>{d}</p></span><span class="paso__progreso" aria-hidden="true"><i></i></span></button></li>'
        for i, (t, d) in enumerate(T["pasos"]))

    def filas(lst): return "".join(f'<div class="fila"><span>{a}</span><b>{b}</b></div>' for a, b in lst)
    e1, e2, e3, e4 = T["esc1"], T["esc2"], T["esc3"], T["esc4"]
    escenas = f'''
<div class="cuadro activo" data-cuadro="0"><div class="tarjeta"><div class="tarjeta__cab"><b>{e1["cab"]}</b><span class="estado">{e1["est"]}</span></div><div class="burbuja">{e1["b1"]}</div><div class="burbuja burbuja--mia">{e1["b2"]}</div></div></div>
<div class="cuadro" data-cuadro="1"><div class="tarjeta"><div class="tarjeta__cab"><b>{e2["cab"]}</b><span class="estado estado--azul">{e2["est"]}</span></div>{filas(e2["filas"])}</div></div>
<div class="cuadro" data-cuadro="2"><div class="tarjeta"><div class="tarjeta__cab"><b>{e3["cab"]}</b><span class="estado estado--ambar">{e3["est"]}</span></div>{filas(e3["filas"])}</div></div>
<div class="cuadro" data-cuadro="3"><div class="tarjeta"><div class="tarjeta__cab"><b>{e4["cab"]}</b><span class="estado">{e4["est"]}</span></div>{filas(e4["filas"])}<div class="total"><span>{e4["total"][0]}</span><span>{e4["total"][1]}</span></div></div></div>'''

    enlaces = [paginas.RUTAS[T["lang"]][k].replace("en/", "", 1) if T["ruta"] else paginas.RUTAS[T["lang"]][k] for k in paginas.ORDEN_SERVICIOS]
    pestanas, paneles = servicios.seccion(T["lang"], I, enlaces=enlaces)

    logros = "\n".join(f'<li><i>{I["check"]}</i><span><b>{t}</b><span>{d}</span></span></li>' for t, d in T["logros"])
    ICONOS_PROC = ["lupa", "plano", "codigo", "soporte"]
    proceso = "\n".join(
        f'<li class="hito" data-revelar style="transition-delay:{i * .1}s"><span class="hito__punto"><b>0{i + 1}</b></span>'
        f'<div class="hito__tarjeta"><span class="hito__ico">{I[ICONOS_PROC[i]]}</span><h3>{t}</h3><p>{d}</p>'
        f'<span class="hito__recibes"><small>{T["proc_recibes"]}</small>{T["proc_entregables"][i]}</span></div></li>'
        for i, (t, d) in enumerate(T["proceso"]))
    ICONOS_TEC = ["enlace", "rayo", "chat", "nube", "hoja", "base", "pago", "erp", "crm", "lupa"]
    chips = [f'<span class="cinta__chip"><i>{I[ICONOS_TEC[j % len(ICONOS_TEC)]]}</i>{t}</span>' for j, t in enumerate(T["tecnologias"])]
    mitad = (len(chips) + 1) // 2
    fila1, fila2 = "".join(chips[:mitad]), "".join(chips[mitad:])
    # cada fila se repite para que el movimiento sea continuo
    tecnologias = (f'<div class="cinta"><div class="cinta__pista">{fila1}{fila1}</div></div>'
                   f'<div class="cinta cinta--reves"><div class="cinta__pista">{fila2}{fila2}</div></div>')
    # cada problema lleva una escena mini: un chat sin responder, una búsqueda en Google o unas estrellas vacías
    def mini(tipo, texto, meta):
        if tipo == "chat":
            return f'<div class="mini mini--chat"><span class="mini__burbuja">{texto}</span><small>{meta}</small></div>'
        if tipo == "google":
            return f'<div class="mini mini--google"><span class="mini__buscador">{I["lupa"]}{texto}</span><small>{meta}</small></div>'
        return f'<div class="mini mini--estrellas"><span class="mini__estrellas">{texto}</span><small>{meta}</small></div>'
    dolores = "\n".join(
        f'<li class="dolor" data-revelar style="transition-delay:{i * .08}s">{mini(*T["dol_minis"][i])}'
        f'<h3>{t}</h3><p>{p}</p><p class="dolor__solucion"><i>{I["check"]}</i><span><b>{T["dol_con"]}:</b> {s}</span></p></li>'
        for i, (t, p, s, _ico) in enumerate(T["dolores"]))
    sectores = "".join(f'<li>{x}</li>' for x in T["marquesina"])
    TS = CONFIG["testimonio"]
    if TS["texto"]:
        testimonio = (f'<blockquote class="cita"><p>{TS["texto"]}</p><footer><b>{TS["nombre"]}</b>'
                      f'<span>{TS["cargo"]}, Acarreos Makena</span></footer></blockquote>')
    else:
        testimonio = f'<p class="ficha-caso__resumen">{T["caso_resumen"]}</p>'
    cifras = "".join(f'<li style="--i:{j}"><span class="cifras-pro__idx">0{j + 1}</span><b>{n}</b><span class="cifras-pro__txt">{t}</span>'
                     f'{"<i class=\"cifras-pro__vivo\"></i>" if n == "24/7" else ""}</li>' for j, (n, t) in enumerate(T["cifras"]))
    bloques_caso = "".join(f'<li><span class="ficha-caso__marca">{et}</span><p>{tx}</p></li>' for et, tx in T["caso_bloques"])
    faqs = "\n".join(f'<details class="pregunta"><summary>{q}</summary><p>{a}</p></details>' for q, a in T["faqs"])
    avisos_json = json.dumps(T["avisos"], ensure_ascii=False).replace("</", "<\\/")
    F = T["form"]
    opciones = "".join(f'<label class="opcion"><input type="checkbox" name="necesita" value="{o}"><span>{o}</span></label>' for o in F["opciones"])
    rangos = "".join(f'<option>{r}</option>' for r in F["rangos"])
    puntos_form = "".join(f'<li>{I["check"]}{x}</li>' for x in F["puntos"])
    form_cfg = json.dumps({"crm": CONFIG["crm"], "wa": CONFIG["whatsapp"], "lang": T["lang"], "enviando": F["enviando"], "enviar": F["enviar"], "error": F["error"]}, ensure_ascii=False).replace("</", "<\\/")

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "#empresa", "name": "Conektra", "url": CONFIG["dominio"],
         "description": T["descripcion"], "areaServed": {"@type": "Country", "name": "Panamá"},
         "knowsAbout": ["Web development", "Local SEO", "Quote request forms", "Customer reviews", "CRM", "Google Sheets"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faqs"]]}]}

    marquesina = "".join(f'<span>{m}</span><i>✦</i>' for m in T["marquesina"])
    rel = lambda k: paginas.RUTAS[T["lang"]][k].replace("en/", "", 1) if T["ruta"] else paginas.RUTAS[T["lang"]][k]
    servicios_pie = "".join(f'<a href="{rel(k)}">{paginas.SERVICIOS[T["lang"]][k]["titulo"]}</a>' for k in paginas.ORDEN_SERVICIOS)
    enlace_caso = rel("caso")
    enlace_privacidad = rel("privacidad")
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
  <meta name="theme-color" content="#061b15">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Conektra">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{T["titulo"]}">
  <meta property="og:description" content="{T["descripcion"]}">
  <meta property="og:locale" content="{"es_PA" if T["lang"] == "es" else "en_US"}">
  <meta property="og:image" content="{CONFIG["dominio"]}img/{"compartir.jpg" if T["lang"] == "es" else "compartir-en.jpg"}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Conektra">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{CONFIG["dominio"]}img/{"compartir.jpg" if T["lang"] == "es" else "compartir-en.jpg"}">
  <link rel="icon" href="{pre}img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
  <link rel="manifest" href="{pre}manifest.webmanifest">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@300;400;500;600;700&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{pre}css/estilos.css?v=35">
</head>
<body>
  <div class="lectura" aria-hidden="true"><i id="lectura"></i></div>
  <header class="cabecera" id="cabecera">
    <div class="contenedor cabecera__barra">
      <a class="marca" href="{pre or './'}" aria-label="Conektra">{LOGO}Conektra</a>
      <nav class="menu" id="menu" aria-label="Principal">
        <a href="#servicios">{T["nav"][0]}</a>
        <a href="#como-funciona">{T["nav"][1]}</a>
        <a href="{enlace_caso}">{T["nav"][2]}</a>
        <a href="#preguntas">{T["nav"][3]}</a>
        <a class="idioma" href="{pre}{T["otra_ruta"] or './'}" hreflang="{"en" if T["lang"] == "es" else "es"}" lang="{"en" if T["lang"] == "es" else "es"}" title="{T["otra_nombre"]}">{T["otra_etiqueta"]}</a>
        <a class="boton boton--marca boton--wa" href="{wa}"{wa_attr}>{I["wa"]} {T["cta"]}</a>
      </nav>
      <button class="hamburguesa" id="hamburguesa" type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>

  <main>
    <section class="portada portada--nicho portada--premium">
      <div class="ambiente" aria-hidden="true">
        <span class="ambiente__forma ambiente__forma--1"></span><span class="ambiente__forma ambiente__forma--2"></span><span class="ambiente__forma ambiente__forma--3"></span>
        <svg class="ambiente__arcos" viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice"><circle cx="400" cy="400" r="210"/><circle cx="400" cy="400" r="300"/><circle cx="400" cy="400" r="390"/></svg>
        <span class="ambiente__grano"></span>
      </div>
      <div class="contenedor portada__grid">
        <div class="portada__texto">
          <p class="chip-nicho aparece" style="--a:.1s"><span class="chip__punto" aria-hidden="true"></span>{T["chip"]}</p>
          <h1 class="titulo-animado titular">{T["h1"]}</h1>
          <p class="portada__lead aparece" style="--a:.55s">{T["lead"]}</p>
          <div class="portada__botones aparece" style="--a:.7s">
            <a class="boton boton--menta" href="{wa}"{wa_attr}>{I["wa"]} {T["cta"]}</a>
            <a class="boton boton--linea" href="#como-funciona"><span class="boton__play">{I["play"]}</span>{T["ver_como"]} {I["flecha"]}</a>
          </div>
          <a class="prueba prueba--nicho aparece" style="--a:.9s" href="{enlace_caso}"><span class="prueba__foto"><img src="{pre}img/caso-acarreos-escritorio.webp" alt="" width="1440" height="900"></span><span class="prueba__txt"><small>{T["prueba_etiqueta"]}</small><b>Acarreos Makena</b><span>{T["prueba_texto"]}</span></span><span class="prueba__flecha">{I["flecha"]}</span></a>
        </div>
        <div class="escena-portada aparece" style="--a:.4s">
          <div class="escena-3d">
            <img class="escena-3d__base" src="{pre}img/escena-base.webp" alt="{T["portada_alt"]}" width="1536" height="1024" fetchpriority="high">
            <span class="escena-3d__sombra" aria-hidden="true"></span>
            <img class="escena-3d__persona" src="{pre}img/escena-persona.webp" alt="" width="357" height="900" aria-hidden="true">
            <span class="escena-3d__brillo" aria-hidden="true"></span>
            <span class="escena-3d__contador" aria-hidden="true">12</span>
            {"".join(f'<span class="escena-3d__burbuja escena-3d__burbuja--{n}" aria-hidden="true">{I["wa"]}<i></i><i></i></span>' for n in (1, 2, 3))}
          </div>
          <div class="escena-portada__aviso" id="aviso" aria-hidden="true"><span class="aviso__ico">{I["chat"]}</span><span><b id="aviso-titulo">{T["avisos"][0][0]}</b><small id="aviso-texto">{T["avisos"][0][1]}</small></span><i class="escena-portada__punto"></i></div>
          <p class="escena-portada__pie"><i></i>{T["portada_pie"]}</p>
        </div>
      </div>
    </section>

    <section class="franja">
      <div class="contenedor franja__caja">
        <p class="franja__frase" aria-label="{T["franja_texto"]} {", ".join(T["palabras"])}">
          <span aria-hidden="true">{T["franja_texto"]}</span>
          <span class="rotador" aria-hidden="true"><span class="rotador__pista" id="palabras">{palabras}</span></span>
        </p>
        <div class="franja__iconos" id="franja-iconos" aria-hidden="true">{iconos_franja}</div>
        <a class="boton boton--marca" href="#proyecto">{T["franja_cta"]} {I["flecha"]}</a>
      </div>
    </section>

    <section class="seccion" id="te-pasa">
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{T["dol_etiqueta"]}</p><h2>{T["dol_h2"]}</h2><p>{T["dol_p"]}</p></header>
        <ul class="dolores">{dolores}</ul>
        <div class="sectores" data-revelar><p>{T["sectores_t"]}</p><ul>{sectores}</ul></div>
      </div>
    </section>

    <section class="seccion" id="como-funciona" style="padding-top:0">
      <div class="oscura seccion flujo-premium">
        <div class="flujo-premium__ambiente" aria-hidden="true"><span class="fp-forma fp-forma--1"></span><span class="fp-forma fp-forma--2"></span><span class="fp-puntos"></span></div>
        <div class="contenedor">
          <header class="cabeza" data-revelar><p class="etiqueta">{T["flujo_etiqueta"]}</p><h2>{T["flujo_h2"]}</h2><p>{T["flujo_p"]}</p></header>
          <div class="flujo-grid">
            <div class="flujo-premium__izq">
              <ol class="pasos">{pasos}</ol>
              <p class="flujo-insignia"><span class="flujo-insignia__ico">{I["escudo"]}</span><span>{T["flujo_insignia"][0]} <b>{T["flujo_insignia"][1]}</b></span></p>
            </div>
            <div class="escena" aria-live="polite">
              <div class="escena__barra" aria-hidden="true"><i></i><i></i><i></i><span>{T["flujo_ventana"]}</span></div>
              <div class="escena__rejilla" aria-hidden="true"></div>
              <span class="escena__brillo" aria-hidden="true"></span>
              {escenas}
              <div class="escena__pie" aria-hidden="true"><span class="escena__chip">{I["rayo"]} {T["escena_chip"]}</span><span class="escena__contador"><b id="escena-n">1</b> / 4</span></div>
            </div>
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

    {integraciones.seccion(T["lang"], NUCLEO, wa, wa_attr, I)}

    <section class="seccion" style="padding-top:0">
      <div class="contenedor">
        <header class="cabeza cabeza--centro" data-revelar><p class="etiqueta">{T["proc_etiqueta"]}</p><h2>{T["proc_h2"]}</h2></header>
        <ol class="proceso" id="proceso"><span class="proceso__linea" aria-hidden="true"><i></i></span>{proceso}</ol>
      </div>
    </section>

    <section class="seccion" id="preguntas" style="padding-top:0">
      <div class="contenedor">
        <header class="cabeza cabeza--centro" data-revelar><p class="etiqueta">{T["faq_etiqueta"]}</p><h2>{T["faq_h2"]}</h2></header>
        <div class="preguntas">{faqs}</div>
      </div>
    </section>
    <section class="seccion proyecto" id="proyecto">
      <div class="contenedor proyecto__grid">
        <div class="proyecto__texto" data-revelar>
          <p class="etiqueta">{F["etiqueta"]}</p>
          <h2>{F["h2"]}</h2>
          <p>{F["p"]}</p>
          <ul class="proyecto__puntos">{puntos_form}</ul>
          <a class="proyecto__wa" href="{wa}"{wa_attr}>{I["wa"]} +507 6552-3134</a>
        </div>
        <div class="proyecto__caja" data-revelar>
          <form class="formulario" id="formulario" novalidate>
            <div class="campos">
              <label class="campo"><span>{F["nombre"]} *</span><input name="nombre" autocomplete="name" maxlength="80" required></label>
              <label class="campo"><span>{F["empresa"]}</span><input name="empresa" autocomplete="organization" maxlength="100"></label>
              <label class="campo campo--ancho"><span>{F["contacto"]} *</span><input name="contacto" autocomplete="email" maxlength="120" required></label>
              <fieldset class="campo campo--ancho"><legend>{F["necesita"]}</legend><div class="opciones">{opciones}</div></fieldset>
              <label class="campo campo--ancho"><span>{F["presupuesto"]}</span><select name="presupuesto">{rangos}</select></label>
              <label class="campo campo--ancho"><span>{F["mensaje"]}</span><textarea name="mensaje" rows="4" maxlength="1500" placeholder="{F["ph_mensaje"]}"></textarea></label>
              <label class="trampa" aria-hidden="true">Web <input name="web" tabindex="-1" autocomplete="off"></label>
            </div>
            <p class="formulario__error" id="form-error" role="alert"></p>
            <button class="boton boton--marca boton--ancho" type="submit">{F["enviar"]} {I["flecha"]}</button>
            <p class="formulario__nota">{F["privacidad"]}</p>
          </form>
          <div class="gracias" id="gracias" hidden>
            <span class="gracias__ico">{I["check"]}</span>
            <h3>{F["ok_t"]}</h3>
            <p>{F["ok_p"]}</p>
            <a class="boton boton--marca boton--wa" id="gracias-wa" href="{wa}"{wa_attr}>{I["wa"]} {F["ok_wa"]}</a>
          </div>
        </div>
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
            <a class="boton boton--blanco boton--wa" href="{wa}"{wa_attr}>{I["wa"]} {T["cierre_wa"]}</a>
            {boton_correo}
          </div>
        </div>
      </div>
    </div>
    <div class="marquesina" aria-hidden="true"><div class="marquesina__pista">{marquesina}{marquesina}</div></div>
    <div class="contenedor">
      <div class="pie__cols">
        <div class="pie__marca">
          <a class="marca" href="{pre or './'}">{LOGO}Conektra</a>
          <p>{T["descripcion"]}</p>
        </div>
        <nav aria-label="{T["pie_servicios"]}"><h4>{T["pie_servicios"]}</h4>{servicios_pie}</nav>
        <nav aria-label="{T["pie_empresa"]}"><h4>{T["pie_empresa"]}</h4><a href="#como-funciona">{T["nav"][1]}</a><a href="#preguntas">{T["nav"][3]}</a><a href="{enlace_caso}">{T["caso_etiqueta"]}</a><a href="{enlace_privacidad}">{"Privacidad" if T["lang"] == "es" else "Privacy"}</a></nav>
        <nav class="pie__contacto" aria-label="{T["pie_contacto"]}"><h4>{T["pie_contacto"]}</h4><a href="{wa}"{wa_attr}>WhatsApp +507 6552-3134</a><a href="#proyecto">{T["form"]["h2"]}</a><a href="{pre}{T["otra_ruta"] or './'}" hreflang="{"en" if T["lang"] == "es" else "es"}">{T["otra_nombre"]}</a></nav>
      </div>
      <div class="pie">
        <span>{T["pie_derechos"]}</span>
        <span>{T["pie_hecho"]}</span>
      </div>
    </div>
  </footer>

  <div class="barra-wa" id="barra-wa" aria-hidden="true">
    <span class="barra-wa__txt"><b>{"¿Quieres más clientes?" if T["lang"] == "es" else "Want more customers?"}</b>{"Respondemos por WhatsApp" if T["lang"] == "es" else "We reply on WhatsApp"}</span>
    <a class="boton boton--wa" href="{wa}"{wa_attr} tabindex="-1">{I["wa"]} WhatsApp</a>
  </div>
  <script>window.CONEKTRA_AVISOS = {avisos_json}; window.CONEKTRA_FORM = {form_cfg};</script>
  <script src="{pre}js/main.js?v=12" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(RAIZ, "en"), exist_ok=True)
    for T, destino in ((ES, "index.html"), (EN, "en/index.html")):
        with open(os.path.join(RAIZ, destino), "w", encoding="utf-8", newline="\n") as f:
            f.write(pagina(T))
        print("ok", destino)
    cfg = dict(CONFIG, v_css="35", v_js="12")
    hechas = paginas.generar(RAIZ, cfg, I, LOGO, {"es": ES["descripcion"], "en": EN["descripcion"]})
    print("ok", len(hechas), "páginas internas + 404, sitemap y robots")
    if not CONFIG["whatsapp"]:
        print("AVISO: falta el número de WhatsApp en CONFIG; los botones llevan a #contacto.")
