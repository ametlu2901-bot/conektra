"""Textos de la portada de Conektra en español (ES) y en inglés (EN).

Regla: no afirmar resultados, métricas ni integraciones que no estén comprobados.
"""

ES = dict(
    lang="es", ruta="", otra_ruta="en/", otra_etiqueta="EN", otra_nombre="English",
    titulo="Conektra | Tu negocio, mejor conectado · Páginas web, CRM y automatización en Panamá",
    descripcion="Estudio tecnológico para pequeños negocios de Panamá: páginas web con SEO local, un CRM para ordenar clientes y cotizaciones, e integraciones con WhatsApp y Google Sheets.",
    eslogan="Tu negocio, mejor conectado.",
    nav=["Servicios", "Cómo funciona", "Casos de éxito", "Preguntas frecuentes"], cta="Hablemos",
    wa_msg="Hola Conektra, quiero mejorar cómo funciona mi negocio.",

    # portada
    etiqueta="Tecnología para negocios que quieren crecer",
    h1='<span class="titular__l1">Tu negocio puede</span> <span class="titular__l2">funcionar</span> <em>mejor conectado.</em>',
    lead="Diseñamos páginas web, sistemas y automatizaciones que conectan tus clientes, ventas y operaciones para que trabajes de manera más organizada.",
    cta_principal="Hablemos de tu negocio", cta_secundario="Descubre lo que hacemos",
    linea=["Desarrollo web", "CRM", "Integraciones", "Automatización"],
    portada_alt="Dueño de una empresa de mudanzas revisando en su celular los mensajes de clientes junto a su camión",
    portada_pie="Menos chats perdidos. Más trabajos cerrados.",
    avisos=[("Nueva cotización", "Guardada en tu hoja"), ("Cliente desde Google", "Pidió precio por la página"), ("Seguimiento", "A Ana le falta respuesta"), ("Nueva reseña", "★★★★★ lista para aprobar")],

    # problemas
    dol_etiqueta="El día a día",
    dol_h2='Tu negocio no necesita más complicaciones. <em>Necesita trabajar mejor.</em>',
    dol_p="Estos problemas se repiten en casi todos los negocios de servicios. Y todos tienen solución.",
    dol_con="Cómo ayuda Conektra",
    dolores=[
        ("Cotizaciones que se quedan sin responder", "Se acumulan los chats y una solicitud queda en «te escribo luego». Ese cliente ya contrató a otro.",
         "Cada solicitud queda guardada con su estado y sabes a quién te falta responder."),
        ("Clientes que no te encuentran en Google", "Buscan «mudanzas en Panamá» o «técnico de aire acondicionado» y aparecen otros, aunque tú trabajes mejor.",
         "Páginas por servicio y por zona, pensadas para lo que tus clientes buscan."),
        ("Horas respondiendo lo mismo", "«¿Qué incluye?», «¿Van a mi zona?», «¿Cuánto cuesta?». Todos los días, a todos.",
         "Tu página responde por ti y el formulario pide los datos que necesitas para cotizar."),
        ("Buenos trabajos que nadie ve", "Tus clientes quedan contentos, pero alguien que no te conoce no tiene cómo saberlo.",
         "Reseñas con estrellas en tu página. Tú decides cuáles se publican."),
    ],
    dol_vis=dict(chat=[("Hola, ¿me cotizan una mudanza para el sábado?", "9:41"), ("¿Siguen disponibles?", "11:02"), ("Hola?? 🙏", "16:30")],
                 cliente="Cliente nuevo", enlinea="Escribió hace 3 días", sinresp="3 mensajes sin responder",
                 busca="mudanzas en panamá", resultados=[("otraempresa.com", "Mudanzas en Panamá | Otra empresa"), ("mudanzasya.com", "Mudanzas rápidas en todo Panamá")],
                 hueco="¿Y tu negocio?", noesta="No apareces en la búsqueda",
                 pregunta="¿Cuánto cuesta una mudanza?", respuesta="Hola 👋 Depende de la distancia y de cuántas cosas lleves…", veces="Copiado y pegado, otra vez",
                 antes="Sin reseñas a la vista", resena="«Llegaron puntuales y cuidaron todo.»", autor="Ana G. · ejemplo", aprobada="Aprobada por ti"),
    sectores_t="Para negocios como",
    sectores=["Mudanzas", "Aire acondicionado", "Instalaciones", "Limpieza", "Fumigación", "Electricistas", "Plomería", "Seguridad", "Talleres"],

    # cómo funciona
    flujo_etiqueta="Cómo funciona", flujo_h2='De un primer mensaje a <em>un cliente organizado.</em>',
    flujo_p="Conectamos tu página, tus solicitudes y tus herramientas para que cada oportunidad tenga seguimiento.",
    pasos=[("Te encuentra y te escribe", "Llega a tu página desde Google y pide cotización, o te escribe por WhatsApp."),
           ("Queda guardado", "La solicitud se guarda sola en tu hoja, con nombre, servicio y fecha."),
           ("Cotizas y das seguimiento", "Cada cotización avanza por etapas y sabes a quién te falta responder."),
           ("Cierras y te califica", "Haces el trabajo y el cliente deja su reseña en tu página.")],
    flujo_nodos=["Google", "Solicitud", "CRM", "Cotización", "Ganado"],
    flujo_ventana="Conektra · Flujo de clientes", flujo_insignia=("Más clientes,", "menos trabajo manual."),
    escena_chip="Automático",
    esc1=dict(cab="WhatsApp", est="Desde Google", b1="Hola, vi su página en Google. ¿Me cotizan una mudanza para el sábado?", b2="¡Claro! Ya registramos tu solicitud. Te enviamos la cotización en unos minutos."),
    esc2=dict(cab="Nueva solicitud", est="CRM", filas=[("Nombre", "María Pérez"), ("Canal", "Formulario web"), ("Servicio", "Mudanza"), ("Etapa", "Nuevo")]),
    esc3=dict(cab="Cotización #1042", est="En revisión", filas=[("Servicio", "Mudanza residencial"), ("Fecha", "Sábado 9:00"), ("Seguimiento", "Recordatorio en 24 h")]),
    esc4=dict(cab="Trabajo #1042", est="Ganado", filas=[("Cliente", "María Pérez"), ("Servicio", "Mudanza residencial"), ("Reseña", "★★★★★")], total=("Total", "B/. 450")),

    # servicios
    serv_etiqueta="Servicios", serv_h2='Todo lo que tu negocio necesita <em>para trabajar mejor.</em>',
    serv_p="Empieza con una solución y conecta más herramientas a medida que tu negocio crece.",
    escalera_t="Empieza con lo que necesitas hoy. Agrega más cuando crezcas.",
    soluciones=[
        dict(letra="A", clave="web", titulo="Presencia digital", ico="web",
             resuelve="La gente te busca en Google y no te encuentra, o llega a un perfil que no explica lo que haces.",
             explica="Te hacemos una página profesional, rápida en el celular, con una página para cada servicio y cada zona donde trabajas.",
             beneficios=["Diseño a la medida de tu negocio", "SEO local: páginas por servicio y por ubicación", "Formulario de contacto que llega a tu hoja", "Botón directo a WhatsApp"],
             enlace="Conoce Páginas web y SEO"),
        dict(letra="B", clave="crm", titulo="Gestión de clientes", ico="crm",
             resuelve="Tus clientes y cotizaciones están repartidos entre chats, libretas y hojas sueltas.",
             explica="Un CRM sencillo, con tus propias etapas, donde cada solicitud entra sola y sabes en qué va cada cliente.",
             beneficios=["Registro automático de solicitudes", "Seguimiento de cotizaciones por etapas", "Recordatorios para no olvidar a nadie", "Reportes de cuánto entra y cuánto cierras"],
             enlace="Conoce el CRM a la medida"),
        dict(letra="C", clave="api", titulo="Automatización y conexiones", ico="rayo",
             resuelve="Pasas datos a mano de un lado a otro, o tus herramientas no se hablan entre sí.",
             explica="Conectamos tu página, WhatsApp, Google Sheets y otras herramientas para que la información llegue sola a donde tiene que llegar.",
             beneficios=["Formularios conectados a tu hoja", "Avisos automáticos para tu equipo", "Integraciones con otras herramientas según tu proyecto", "Inventario y facturación cuando los necesites"],
             enlace="Conoce las integraciones"),
    ],
    serv_resuelve="Lo que resuelve", serv_incluye="Incluye",
    crecer=dict(etiqueta="Para cuando crezcas", titulo="ERP y automatizaciones avanzadas",
                texto="Inventario, compras, facturación y procesos internos conectados, para negocios que necesitan más control sobre su operación.",
                enlace="Conoce ERP y automatizaciones"),

    # casos de éxito
    caso_etiqueta="Casos de éxito", caso_h2='Soluciones reales <em>para negocios reales.</em>',
    caso_p="Así trabajamos con Acarreos Makena, una empresa de mudanzas en Panamá.",
    caso_nombre="Acarreos Makena", caso_categoria="Mudanzas y servicios · Panamá",
    caso_bloques=[
        ("El negocio", "Mudanzas, acarreos, retiro de escombros y montaje de eventos y oficinas en Panamá."),
        ("El problema", "Los clientes llegaban solo por WhatsApp, las cotizaciones quedaban repartidas entre chats y no tenían una página que apareciera en Google."),
        ("La solución", "Una página con dominio propio, páginas por servicio y por zona, un formulario de cotización conectado a Google Sheets y reseñas con aprobación del dueño."),
        ("La experiencia", "El cliente encuentra el servicio, ve las zonas donde trabajan y pide su cotización en un formulario corto o escribe directo por WhatsApp."),
    ],
    caso_sistemas_t="Sistemas conectados", caso_sistemas=[("web", "Página web"), ("hoja", "Google Sheets"), ("chat", "WhatsApp"), ("lupa", "Search Console"), ("estrella", "Reseñas")],
    caso_resultados_t="Resultados verificables",
    caso_resultados=["Página publicada en acarreosmakena.com", "Cotizaciones guardadas con su estado: nuevo, contactado, cotizado, agendado, ganado o perdido", "Reseñas con estrellas que el dueño aprueba", "Sitemap enviado a Google Search Console"],
    cifras=[("10", "páginas listas para Google"), ("5", "servicios con página propia"), ("3", "zonas con página propia"), ("24/7", "recibiendo cotizaciones")],
    caso_cta="Ver la página en vivo", caso_completo="Ver el caso completo",

    # proceso
    proc_etiqueta="Proceso", proc_h2='De la idea a <em>una solución que funciona.</em>',
    proc_p="Sin sorpresas: en cada etapa sabes qué estamos haciendo y qué recibes.",
    proc_hacemos="Qué hacemos", proc_recibes="Qué recibes",
    proceso=[("Diagnóstico", "Conversamos sobre cómo trabajas hoy: cómo te llegan los clientes, dónde se pierden cotizaciones y qué herramientas usas.", "Un mapa claro de cómo funciona tu negocio hoy"),
             ("Propuesta", "Te proponemos por dónde empezar, qué conectar y en qué orden, con precio y tiempos antes de comenzar.", "Una propuesta con alcance, precio y tiempos"),
             ("Desarrollo", "Construimos por etapas y te mostramos avances para que pruebes y opines desde temprano.", "Avances que puedes probar en tu celular"),
             ("Soporte", "Después de entregar seguimos contigo: cambios, mejoras y nuevas conexiones cuando las necesites.", "Acompañamiento y mejoras")],

    # preguntas
    faq_etiqueta="Preguntas frecuentes", faq_h2='Lo que más <em>nos preguntan.</em>',
    faq_p="Si tu duda no está aquí, escríbenos por WhatsApp y te respondemos.",
    faqs=[
        ("Servicios", [
            ("¿Qué hace Conektra exactamente?", "Hacemos páginas web, sistemas para ordenar clientes y cotizaciones (CRM) y conexiones entre tus herramientas. Puedes empezar con una sola cosa y sumar el resto después."),
            ("Ya tengo WhatsApp e Instagram, ¿para qué una página?", "Porque cuando alguien busca «mudanzas en Panamá» o «técnico de aire acondicionado» en Google, no ve tu Instagram: ve páginas web. Tu página te pone en esas búsquedas y manda a esa persona directo a tu WhatsApp.")]),
        ("Precios y contratación", [
            ("¿Cuánto cuesta?", "Depende de qué necesites: cuántos servicios y zonas mostrar, y qué funciones lleva. Te enviamos una propuesta con precio claro antes de empezar."),
            ("¿Tengo que contratar todo desde el principio?", "No. Empieza con lo que necesitas hoy, por ejemplo tu página, y agrega más cuando tu negocio lo pida.")]),
        ("Desarrollo", [
            ("¿Cuánto tarda?", "Depende de cuántas páginas y funciones lleve. Te damos el tiempo exacto en la propuesta, antes de empezar."),
            ("¿Tengo que saber de tecnología?", "No. Te explicamos todo con palabras simples, y tus cotizaciones quedan en una hoja de Google Sheets que se usa como cualquier tabla.")]),
        ("Google y SEO", [
            ("¿Me garantizan el primer lugar en Google?", "Nadie puede garantizarlo con honestidad. Lo que sí hacemos es dejar tu página técnicamente lista, con páginas pensadas para lo que buscan tus clientes."),
            ("¿Qué es el SEO local?", "Es preparar tu página para aparecer cuando alguien busca tu servicio en tu zona, por ejemplo «fumigación en San Miguelito».")]),
        ("CRM y automatizaciones", [
            ("¿Necesito pagar una licencia de CRM?", "No necesariamente. Según tu caso podemos usar herramientas que ya tienes, como Google Sheets, o conectar un CRM del mercado."),
            ("¿Cómo funcionan las reseñas?", "Tus clientes te califican con estrellas desde la página y tú decides cuáles se publican.")]),
        ("Integraciones", [
            ("¿Pueden conectar Yappy u otras pasarelas de pago?", "Se puede evaluar según el proyecto. Antes de prometerlo revisamos qué permite cada servicio y lo probamos contigo."),
            ("¿Tengo que cambiar las herramientas que ya uso?", "No necesariamente. Muchas veces conectamos lo que ya tienes. Si algo no da para más, te lo decimos y te proponemos una alternativa.")]),
        ("Soporte", [
            ("¿Qué pasa después de la entrega?", "Te acompañamos con soporte y mejoras. Si agregas un servicio, una zona o una herramienta nueva, lo sumamos.")]),
        ("Propiedad de los datos", [
            ("¿Mis datos quedan seguros?", "Tus datos quedan en tus propias cuentas, como tu Google Sheets. Usamos accesos con los permisos mínimos y te entregamos todo documentado.")]),
    ],

    # contacto
    form=dict(etiqueta="Contacto", h2='Cuéntanos qué quieres mejorar <em>en tu negocio.</em>',
              p="Cuéntanos cómo trabajas actualmente y qué te gustaría organizar. Revisaremos tu caso y te propondremos una solución.",
              puntos=["Revisamos tu caso sin compromiso", "Te proponemos una solución con precio claro", "Te escribimos por WhatsApp"],
              nombre="Tu nombre", empresa="Nombre del negocio", whatsapp="WhatsApp", correo="Correo", opcional="opcional",
              necesita="¿Qué necesitas solucionar?", opciones=["Presencia digital", "Gestión de clientes", "Automatización", "No estoy seguro"],
              mensaje="Cuéntanos brevemente", ph_mensaje="¿Cómo te llegan hoy los clientes y qué te gustaría organizar?",
              presupuesto="Presupuesto aproximado", rangos=["Prefiero no decirlo", "Menos de $1,000", "$1,000 – $3,000", "$3,000 – $10,000", "Más de $10,000"],
              enviar="Enviar mensaje", enviando="Enviando…", error="Escribe tu nombre y tu WhatsApp para poder responderte.",
              ok_t="¡Recibimos tu mensaje!", ok_p="Te escribimos muy pronto. Si es urgente, sigue la conversación por WhatsApp.", ok_wa="Seguir por WhatsApp",
              privacidad="Usamos tus datos solo para responderte.", privacidad_enlace="Política de privacidad", o_wa="¿Prefieres escribir directo?"),

    # cierre y pie
    cierre_h2='Tu negocio tiene mucho por crecer. <em>Conectemos lo que sigue.</em>',
    cierre_p="Cuéntanos qué necesitas y descubramos cómo podemos ayudarte.", cierre_wa="Hablemos por WhatsApp",
    pie_servicios="Servicios", pie_nav="Navegación", pie_contacto="Contacto", pie_privacidad="Política de privacidad",
    pie_form="Escríbenos por el formulario", pie_derechos="© 2026 Conektra. Todos los derechos reservados.", pie_hecho="Hecho en Panamá.",
    pie_desc="Estudio tecnológico que ayuda a pequeños negocios a conseguir clientes, ordenar su trabajo y conectar sus herramientas.",
    barra_t="¿Hablamos de tu negocio?", barra_p="Te respondemos por WhatsApp",
)

EN = dict(
    lang="en", ruta="en/", otra_ruta="", otra_etiqueta="ES", otra_nombre="Español",
    titulo="Conektra | Your business, better connected · Websites, CRM and automation in Panama",
    descripcion="Tech studio for small businesses in Panama: websites with local SEO, a CRM to organize customers and quotes, and integrations with WhatsApp and Google Sheets.",
    eslogan="Your business, better connected.",
    nav=["Services", "How it works", "Success stories", "FAQ"], cta="Let's talk",
    wa_msg="Hi Conektra, I want to improve how my business runs.",

    etiqueta="Technology for businesses that want to grow",
    h1='<span class="titular__l1">Your business can</span> <span class="titular__l2">run</span> <em>better connected.</em>',
    lead="We design websites, systems and automations that connect your customers, sales and operations so you can work in a more organized way.",
    cta_principal="Let's talk about your business", cta_secundario="See what we do",
    linea=["Web development", "CRM", "Integrations", "Automation"],
    portada_alt="Owner of a moving company checking customer messages on the phone next to the truck",
    portada_pie="Fewer lost chats. More closed jobs.",
    avisos=[("New quote request", "Saved to your sheet"), ("Customer from Google", "Asked for a price on your site"), ("Follow-up", "Ana is waiting for a reply"), ("New review", "★★★★★ ready to approve")],

    dol_etiqueta="Day to day",
    dol_h2='Your business doesn\'t need more complications. <em>It needs to work better.</em>',
    dol_p="These problems show up in almost every service business. And every one of them has a fix.",
    dol_con="How Conektra helps",
    dolores=[
        ("Quote requests that go unanswered", "Chats pile up and a request stays at \"I'll get back to you\". That customer already hired someone else.",
         "Every request is saved with its status, so you know who's still waiting."),
        ("Customers who can't find you on Google", "People search \"movers in Panama\" or \"AC technician\" and others show up, even if your work is better.",
         "Pages for each service and area, built around what your customers search for."),
        ("Hours answering the same questions", "\"What's included?\", \"Do you cover my area?\", \"How much?\". Every day, to everyone.",
         "Your website answers for you, and the form asks for what you need to quote."),
        ("Great work nobody sees", "Your customers are happy, but someone new has no way of knowing it.",
         "Star reviews on your website. You decide which ones get published."),
    ],
    dol_vis=dict(chat=[("Hi, can I get a quote for a move on Saturday?", "9:41"), ("Are you still available?", "11:02"), ("Hello?? 🙏", "4:30")],
                 cliente="New customer", enlinea="Wrote 3 days ago", sinresp="3 unanswered messages",
                 busca="movers in panama", resultados=[("otherbusiness.com", "Movers in Panama | Other business"), ("fastmovers.com", "Fast moving across Panama")],
                 hueco="What about your business?", noesta="You don't show up in the search",
                 pregunta="How much does a move cost?", respuesta="Hi 👋 It depends on the distance and how much you're moving…", veces="Copied and pasted, again",
                 antes="No reviews in sight", resena="\"They arrived on time and took care of everything.\"", autor="Ana G. · example", aprobada="Approved by you"),
    sectores_t="For businesses like",
    sectores=["Movers", "Air conditioning", "Installers", "Cleaning", "Pest control", "Electricians", "Plumbing", "Security", "Auto repair"],

    flujo_etiqueta="How it works", flujo_h2='From a first message to <em>an organized customer.</em>',
    flujo_p="We connect your website, your requests and your tools so every opportunity gets followed up.",
    pasos=[("They find you and reach out", "They land on your website from Google and request a quote, or message you on WhatsApp."),
           ("It gets saved", "The request is saved to your sheet automatically, with name, service and date."),
           ("You quote and follow up", "Every quote moves through stages and you know who's still waiting."),
           ("You close and they rate you", "You do the job and the customer leaves a review on your website.")],
    flujo_nodos=["Google", "Request", "CRM", "Quote", "Won"],
    flujo_ventana="Conektra · Customer flow", flujo_insignia=("More customers,", "less manual work."),
    escena_chip="Automatic",
    esc1=dict(cab="WhatsApp", est="From Google", b1="Hi, I saw your website on Google. Can I get a quote for a move on Saturday?", b2="Of course! We've logged your request. Your quote is on its way in a few minutes."),
    esc2=dict(cab="New request", est="CRM", filas=[("Name", "Maria Perez"), ("Channel", "Website form"), ("Service", "Moving"), ("Stage", "New")]),
    esc3=dict(cab="Quote #1042", est="In review", filas=[("Service", "Home move"), ("Date", "Saturday 9:00"), ("Follow-up", "Reminder in 24 h")]),
    esc4=dict(cab="Job #1042", est="Won", filas=[("Customer", "Maria Perez"), ("Service", "Home move"), ("Review", "★★★★★")], total=("Total", "$450")),

    serv_etiqueta="Services", serv_h2='Everything your business needs <em>to work better.</em>',
    serv_p="Start with one solution and connect more tools as your business grows.",
    escalera_t="Start with what you need today. Add more as you grow.",
    soluciones=[
        dict(letra="A", clave="web", titulo="Online presence", ico="web",
             resuelve="People search for you on Google and can't find you, or land on a profile that doesn't explain what you do.",
             explica="We build you a professional website, fast on mobile, with a page for every service and every area you cover.",
             beneficios=["Designed around your business", "Local SEO: pages per service and location", "Contact form that lands in your sheet", "Direct WhatsApp button"],
             enlace="Explore Websites and SEO"),
        dict(letra="B", clave="crm", titulo="Customer management", ico="crm",
             resuelve="Your customers and quotes are scattered across chats, notebooks and loose spreadsheets.",
             explica="A simple CRM, with your own stages, where every request comes in automatically and you know where each customer stands.",
             beneficios=["Automatic request logging", "Quote follow-up by stage", "Reminders so nobody gets forgotten", "Reports on what comes in and what you close"],
             enlace="Explore the custom CRM"),
        dict(letra="C", clave="api", titulo="Automation and connections", ico="rayo",
             resuelve="You copy data by hand from one place to another, or your tools don't talk to each other.",
             explica="We connect your website, WhatsApp, Google Sheets and other tools so information gets where it needs to go on its own.",
             beneficios=["Forms connected to your sheet", "Automatic alerts for your team", "Integrations with other tools per project", "Inventory and invoicing when you need them"],
             enlace="Explore integrations"),
    ],
    serv_resuelve="What it solves", serv_incluye="Includes",
    crecer=dict(etiqueta="For when you grow", titulo="ERP and advanced automation",
                texto="Connected inventory, purchasing, invoicing and internal processes, for businesses that need more control over their operations.",
                enlace="Explore ERP and automation"),

    caso_etiqueta="Success stories", caso_h2='Real solutions <em>for real businesses.</em>',
    caso_p="This is how we worked with Acarreos Makena, a moving company in Panama.",
    caso_nombre="Acarreos Makena", caso_categoria="Moving and services · Panama",
    caso_bloques=[
        ("The business", "Moving, hauling, debris removal and event and office setup in Panama."),
        ("The problem", "Customers only came in through WhatsApp, quotes were scattered across chats and there was no website showing up on Google."),
        ("The solution", "A website on its own domain, pages per service and area, a quote form connected to Google Sheets and reviews approved by the owner."),
        ("The experience", "Customers find the service, see the areas covered and request a quote through a short form or message directly on WhatsApp."),
    ],
    caso_sistemas_t="Connected systems", caso_sistemas=[("web", "Website"), ("hoja", "Google Sheets"), ("chat", "WhatsApp"), ("lupa", "Search Console"), ("estrella", "Reviews")],
    caso_resultados_t="Verifiable results",
    caso_resultados=["Website live at acarreosmakena.com", "Quote requests saved with their status: new, contacted, quoted, scheduled, won or lost", "Star reviews approved by the owner", "Sitemap submitted to Google Search Console"],
    cifras=[("10", "pages ready for Google"), ("5", "services with their own page"), ("3", "areas with their own page"), ("24/7", "receiving quote requests")],
    caso_cta="See the live website", caso_completo="Read the full case",

    proc_etiqueta="Process", proc_h2='From idea to <em>a solution that works.</em>',
    proc_p="No surprises: at every stage you know what we're doing and what you get.",
    proc_hacemos="What we do", proc_recibes="What you get",
    proceso=[("Discovery", "We talk about how you work today: how customers reach you, where quotes get lost and which tools you use.", "A clear map of how your business runs today"),
             ("Proposal", "We propose where to start, what to connect and in what order, with price and timeline before we begin.", "A proposal with scope, price and timeline"),
             ("Build", "We build in stages and show you progress so you can test and give feedback early.", "Progress you can try on your phone"),
             ("Support", "After launch we stay with you: changes, improvements and new connections when you need them.", "Ongoing support and improvements")],

    faq_etiqueta="FAQ", faq_h2='What people <em>ask us most.</em>',
    faq_p="If your question isn't here, message us on WhatsApp and we'll answer.",
    faqs=[
        ("Services", [
            ("What exactly does Conektra do?", "We build websites, systems to organize customers and quotes (CRM) and connections between your tools. You can start with just one and add the rest later."),
            ("I already have WhatsApp and Instagram. Why a website?", "Because when someone searches \"movers in Panama\" or \"AC technician\" on Google, they don't see your Instagram: they see websites. Your website puts you in those searches and sends that person straight to your WhatsApp.")]),
        ("Pricing and hiring", [
            ("How much does it cost?", "It depends on what you need: how many services and areas to show and which features it includes. We send you a proposal with a clear price before we start."),
            ("Do I have to hire everything at once?", "No. Start with what you need today, like your website, and add more when your business calls for it.")]),
        ("Development", [
            ("How long does it take?", "It depends on the number of pages and features. We give you the exact timeline in the proposal, before we start."),
            ("Do I need to know about technology?", "No. We explain everything in plain words, and your quotes land in a Google Sheets spreadsheet you use like any table.")]),
        ("Google and SEO", [
            ("Do you guarantee first place on Google?", "No one can honestly guarantee that. What we do is leave your website technically ready, with pages built for what your customers search for."),
            ("What is local SEO?", "It's preparing your website to show up when someone searches for your service in your area, for example \"pest control in San Miguelito\".")]),
        ("CRM and automation", [
            ("Do I need to pay for a CRM license?", "Not necessarily. Depending on your case we can use tools you already have, like Google Sheets, or connect an off-the-shelf CRM."),
            ("How do reviews work?", "Your customers rate you with stars from your website and you decide which ones get published.")]),
        ("Integrations", [
            ("Can you connect Yappy or other payment gateways?", "It can be evaluated per project. Before promising it, we check what each service allows and test it with you."),
            ("Do I have to replace the tools I already use?", "Not necessarily. We often connect what you already have. If something can't keep up, we'll tell you and suggest an alternative.")]),
        ("Support", [
            ("What happens after delivery?", "We stay with you for support and improvements. If you add a service, an area or a new tool, we add it.")]),
        ("Data ownership", [
            ("Is my data safe?", "Your data stays in your own accounts, like your Google Sheets. We use least-privilege access and hand everything over documented.")]),
    ],

    form=dict(etiqueta="Contact", h2='Tell us what you want to improve <em>in your business.</em>',
              p="Tell us how you work today and what you'd like to organize. We'll review your case and propose a solution.",
              puntos=["We review your case, no commitment", "We propose a solution with a clear price", "We reply on WhatsApp"],
              nombre="Your name", empresa="Business name", whatsapp="WhatsApp", correo="Email", opcional="optional",
              necesita="What do you need to solve?", opciones=["Online presence", "Customer management", "Automation", "Not sure yet"],
              mensaje="Tell us briefly", ph_mensaje="How do customers reach you today and what would you like to organize?",
              presupuesto="Approximate budget", rangos=["I'd rather not say", "Under $1,000", "$1,000 – $3,000", "$3,000 – $10,000", "Over $10,000"],
              enviar="Send message", enviando="Sending…", error="Add your name and your WhatsApp so we can reply.",
              ok_t="We got your message!", ok_p="We'll get back to you very soon. If it's urgent, continue on WhatsApp.", ok_wa="Continue on WhatsApp",
              privacidad="We only use your details to reply to you.", privacidad_enlace="Privacy policy", o_wa="Prefer to message directly?"),

    cierre_h2='Your business has a lot of room to grow. <em>Let\'s connect what\'s next.</em>',
    cierre_p="Tell us what you need and let's find out how we can help.", cierre_wa="Let's talk on WhatsApp",
    pie_servicios="Services", pie_nav="Navigation", pie_contacto="Contact", pie_privacidad="Privacy policy",
    pie_form="Write to us through the form", pie_derechos="© 2026 Conektra. All rights reserved.", pie_hecho="Made in Panama.",
    pie_desc="Tech studio that helps small businesses win customers, organize their work and connect their tools.",
    barra_t="Shall we talk about your business?", barra_p="We reply on WhatsApp",
)
