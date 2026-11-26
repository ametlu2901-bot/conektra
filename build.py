"""Genera la portada de Enlaza Studio en español (index.html) y en inglés (en/index.html), y las páginas internas.

Uso:  python build.py
Los datos de contacto se cambian en CONFIG; los textos de la portada, en textos.py;
el menú y el pie, en marco.py; los estilos, en css/conektra.css.
La escena 3D de la portada (img/escena-base.webp + img/escena-persona.webp) no se toca.
"""
import json, os, urllib.parse
import servicios
import paginas
import integraciones
import marco
import inicio
import textos3
from iconos import I, LOGO, NUCLEO
from textos import ES, EN

CONFIG = {
    "dominio": "https://enlazastudio.com/",  # dominio propio (Cloudflare, comprado 2026-11-26)
    "whatsapp": "50765523134",                  # solo números con código de país, p. ej. 50760000000
    "correo": "hola@enlazastudio.com",                               # p. ej. hola@enlazastudio.com
    # testimonio real de Acarreos Makena: si "texto" está vacío no se muestra ninguna cita
    "testimonio": dict(texto="", nombre="", cargo=""),
    # URL /exec de la hoja «Enlaza Studio — CRM» (programa en crm/Codigo.gs)
    "crm": "https://script.google.com/macros/s/AKfycbxvoagKEQKMfhn8mdVk7cknuZfPJyKL1HPd4mb6tjxPWa29TSFh78hAsZ2qJBwcZGWl/exec",
}

RAIZ = os.path.dirname(os.path.abspath(__file__))
PORTAL = os.path.join(os.path.dirname(RAIZ), "conektra-portal")  # el portal vive en su propio proyecto


def copiar_portal():
    """Copia la interfaz del portal (modo demostración) a app/ para publicarla en /app/."""
    import shutil
    if not os.path.isdir(PORTAL):
        return False
    destino = os.path.join(RAIZ, "app")
    shutil.rmtree(destino, ignore_errors=True)
    os.makedirs(destino)
    shutil.copy2(os.path.join(PORTAL, "index.html"), destino)
    for carpeta in ("css", "js", "img"):
        shutil.copytree(os.path.join(PORTAL, carpeta), os.path.join(destino, carpeta))
    return True


def wa_link(texto):
    return f'https://wa.me/{CONFIG["whatsapp"]}?text={urllib.parse.quote(texto)}'


# ---------- piezas de la portada ----------

def problemas(T):
    V = T["dol_vis"]
    # 1. ventana de chat con mensajes sin responder
    chat = "".join(f'<span class="vis-chat__burbuja" style="--i:{j}">{b}<small>{h} ✓✓</small></span>' for j, (b, h) in enumerate(V["chat"]))
    chat_html = (f'<div class="vis vis-chat" aria-hidden="true"><div class="vis-chat__cab"><span class="vis-chat__avatar">{I["wa"]}</span>'
                 f'<span><b>{V["cliente"]}</b><small>{V["enlinea"]}</small></span><span class="vis-chat__contador">{len(V["chat"])}</span></div>'
                 f'<div class="vis-chat__cuerpo">{chat}</div><p class="vis-chat__pie">{V["sinresp"]}</p></div>')
    # 2. resultados de búsqueda donde el negocio no está
    res = "".join(f'<span class="vis-google__res"><small>{u}</small><b>{t}</b><i></i></span>' for u, t in V["resultados"])
    google_html = (f'<div class="vis vis-google" aria-hidden="true"><span class="vis-google__barra"><b class="vis-google__g">G</b>{V["busca"]}{I["lupa"]}</span>'
                   f'{res}<span class="vis-google__hueco">{V["hueco"]}</span><small class="vis__alerta">{V["noesta"]}</small></div>')
    # 3. la misma pregunta y la misma respuesta, una y otra vez
    repetido = "".join(f'<span class="vis-rep__par" style="--i:{j}"><span class="vis-rep__in">{V["pregunta"]}</span><span class="vis-rep__out">{V["respuesta"]}</span></span>' for j in range(3))
    rep_html = f'<div class="vis vis-rep" aria-hidden="true">{repetido}<small class="vis-rep__sello">{I["chat"]} {V["veces"]}</small></div>'
    # 4. antes sin reseñas, después con una reseña aprobada por el dueño
    resenas_html = (f'<div class="vis vis-resenas" aria-hidden="true"><span class="vis-resenas__antes"><b>☆☆☆☆☆</b><small>{V["antes"]}</small></span>'
                    f'<span class="vis-resenas__flecha">{I["flecha"]}</span>'
                    f'<span class="vis-resenas__despues"><b>★★★★★</b><q>{V["resena"]}</q><small>{V["autor"]}</small><em>{I["check"]} {V["aprobada"]}</em></span></div>')
    visuales = [chat_html, google_html, rep_html, resenas_html]
    items = "".join(
        f'<article class="problema problema--{j + 1}" data-revelar style="transition-delay:{j * .08:.2f}s">{visuales[j]}'
        f'<div class="problema__cuerpo"><span class="problema__num">0{j + 1}</span><h3>{t}</h3><p>{p}</p>'
        f'<p class="problema__ayuda"><span>{I["check"]} {T["dol_con"]}</span>{s}</p></div></article>'
        for j, (t, p, s) in enumerate(T["dolores"]))
    sectores = "".join(f"<li>{x}</li>" for x in T["sectores"])
    return f'''    <section class="seccion problemas" id="problemas">
      <div class="contenedor">
        <header class="cabeza cabeza--partida" data-revelar>
          <div><p class="etiqueta">{T["dol_etiqueta"]}</p><h2>{T["dol_h2"]}</h2></div>
          <p>{T["dol_p"]}</p>
        </header>
        <div class="problemas__grid">{items}</div>
        <div class="sectores" data-revelar><p>{T["sectores_t"]}</p><ul>{sectores}</ul></div>
      </div>
    </section>
'''


def flujo(T):
    nodos = T["flujo_nodos"]
    activos = [(0, 1), (2,), (3,), (4,)]  # qué etapas del recorrido se encienden en cada paso

    def ruta(n):
        hechos = min(activos[n])
        return '<div class="ruta" aria-hidden="true">' + "".join(
            f'<span class="ruta__nodo{" ruta__nodo--activo" if k in activos[n] else (" ruta__nodo--hecho" if k < hechos else "")}">{x}</span>'
            for k, x in enumerate(nodos)) + "</div>"

    def filas(lst):
        return "".join(f'<div class="fila"><span>{a}</span><b>{b}</b></div>' for a, b in lst)

    e1, e2, e3, e4 = T["esc1"], T["esc2"], T["esc3"], T["esc4"]
    tarjetas = [
        f'<div class="tarjeta"><div class="tarjeta__cab"><b>{e1["cab"]}</b><span class="estado">{e1["est"]}</span></div><div class="burbuja">{e1["b1"]}</div><div class="burbuja burbuja--mia">{e1["b2"]}</div></div>',
        f'<div class="tarjeta"><div class="tarjeta__cab"><b>{e2["cab"]}</b><span class="estado estado--azul">{e2["est"]}</span></div>{filas(e2["filas"])}</div>',
        f'<div class="tarjeta"><div class="tarjeta__cab"><b>{e3["cab"]}</b><span class="estado estado--ambar">{e3["est"]}</span></div>{filas(e3["filas"])}</div>',
        f'<div class="tarjeta"><div class="tarjeta__cab"><b>{e4["cab"]}</b><span class="estado">{e4["est"]}</span></div>{filas(e4["filas"])}<div class="total"><span>{e4["total"][0]}</span><span>{e4["total"][1]}</span></div></div>',
    ]
    cuadros = "".join(f'<div class="cuadro{" activo" if n == 0 else ""}" data-cuadro="{n}">{ruta(n)}{t}</div>' for n, t in enumerate(tarjetas))
    iconos = ("lupa", "hoja", "chat", "estrella")
    pasos = "".join(
        f'<li><button type="button" class="paso{" activo" if i == 0 else ""}" data-paso="{i}" aria-pressed="{str(i == 0).lower()}">'
        f'<b>0{i + 1}</b><span class="paso__ico" aria-hidden="true">{I[iconos[i]]}</span><span><h3>{t}</h3><p>{d}</p></span>'
        f'<span class="paso__progreso" aria-hidden="true"><i></i></span></button></li>'
        for i, (t, d) in enumerate(T["pasos"]))
    return f'''    <section class="seccion flujo" id="como-funciona">
      <div class="flujo__ambiente" aria-hidden="true"><span></span><span></span><i></i></div>
      <div class="contenedor">
        <header class="cabeza" data-revelar><p class="etiqueta">{T["flujo_etiqueta"]}</p><h2>{T["flujo_h2"]}</h2><p>{T["flujo_p"]}</p></header>
        <div class="flujo__grid">
          <div>
            <ol class="pasos">{pasos}</ol>
            <p class="insignia"><span class="insignia__ico">{I["escudo"]}</span><span>{T["flujo_insignia"][0]} <b>{T["flujo_insignia"][1]}</b></span></p>
          </div>
          <div class="escena" aria-live="polite">
            <div class="escena__barra" aria-hidden="true"><i></i><i></i><i></i><span>{T["flujo_ventana"]}</span></div>
            <div class="escena__rejilla" aria-hidden="true"></div>
            <span class="escena__brillo" aria-hidden="true"></span>
            {cuadros}
            <div class="escena__pie" aria-hidden="true"><span class="escena__chip">{I["rayo"]} {T["escena_chip"]}</span><span class="escena__contador"><b id="escena-n">1</b> / 4</span></div>
          </div>
        </div>
      </div>
    </section>
'''


def servicios_html(T, rel):
    maquetas = servicios.seccion(T["lang"], I, solo_maquetas=True)
    idx = {"web": 0, "crm": 1, "api": 2}
    bloques = []
    for S in T["soluciones"]:
        beneficios = "".join(f"<li>{I['check']}{b}</li>" for b in S["beneficios"])
        bloques.append(f'''<article class="solucion solucion--{S["letra"].lower()}" data-revelar>
            <div class="solucion__texto">
              <p class="solucion__letra"><span>{S["letra"]}</span>{I[S["ico"]]}</p>
              <h3>{S["titulo"]}</h3>
              <div class="solucion__resuelve"><small>{T["serv_resuelve"]}</small><p>{S["resuelve"]}</p></div>
              <p class="solucion__explica">{S["explica"]}</p>
              <ul class="solucion__lista" aria-label="{T["serv_incluye"]}">{beneficios}</ul>
              <a class="enlace-flecha" href="{rel(S["clave"])}">{S["enlace"]} <span>{I["flecha"]}</span></a>
            </div>
            <div class="maqueta" aria-hidden="true"><div class="maqueta__rejilla"></div><div class="panel activo">{maquetas[idx[S["clave"]]]}</div></div>
          </article>''')
    C = T["crecer"]
    escalera = "".join(f'<li><b>{S["letra"]}</b>{S["titulo"]}</li>' for S in T["soluciones"])
    return f'''    <section class="seccion servicios-sec" id="servicios">
      <div class="contenedor">
        <header class="cabeza cabeza--partida" data-revelar>
          <div><p class="etiqueta">{T["serv_etiqueta"]}</p><h2>{T["serv_h2"]}</h2></div>
          <p>{T["serv_p"]}</p>
        </header>
        <div class="escalera" data-revelar><p>{T["escalera_t"]}</p><ol>{escalera}</ol></div>
        <div class="soluciones">
          {"".join(bloques)}
        </div>
        <aside class="crecer" data-revelar>
          <div><p class="etiqueta">{C["etiqueta"]}</p><h3>{C["titulo"]}</h3><p>{C["texto"]}</p>
            <a class="enlace-flecha enlace-flecha--claro" href="{rel("erp")}">{C["enlace"]} <span>{I["flecha"]}</span></a></div>
          <div class="maqueta maqueta--crecer" aria-hidden="true"><div class="panel activo">{maquetas[3]}</div></div>
        </aside>
      </div>
    </section>
'''


def casos(T, pre, enlace_caso):
    TS = CONFIG["testimonio"]
    cita = (f'<blockquote class="cita"><p>{TS["texto"]}</p><footer><b>{TS["nombre"]}</b><span>{TS["cargo"]}, Acarreos Makena</span></footer></blockquote>'
            if TS["texto"] else "")
    bloques = "".join(f'<li><span>{t}</span><p>{d}</p></li>' for t, d in T["caso_bloques"])
    sistemas = "".join(f'<li><i>{I[ico]}</i>{t}</li>' for ico, t in T["caso_sistemas"])
    resultados = "".join(f'<li>{I["check"]}{r}</li>' for r in T["caso_resultados"])
    vivo = '<i class="cifras__vivo"></i>'
    cifras = "".join(f'<li style="--i:{j}"><b>{n}</b><span>{t}</span>{vivo if n == "24/7" else ""}</li>' for j, (n, t) in enumerate(T["cifras"]))
    es = T["lang"] == "es"
    return f'''    <section class="seccion casos" id="casos">
      <div class="casos__ambiente" aria-hidden="true"><span></span><span></span></div>
      <div class="contenedor">
        <header class="cabeza cabeza--partida" data-revelar>
          <div><p class="etiqueta">{T["caso_etiqueta"]}</p><h2>{T["caso_h2"]}</h2></div>
          <p>{T["caso_p"]}</p>
        </header>
        <div class="casos__grid">
          <figure class="vitrina-caso" data-revelar>
            <div class="vitrina-caso__escritorio"><div class="vitrina-caso__barra" aria-hidden="true"><i></i><i></i><i></i><span>acarreosmakena.com</span><em><b></b>{"En línea" if es else "Live"}</em></div>
              <img src="{pre}img/caso-acarreos-escritorio.webp" alt="{"Página web de Acarreos Makena en computadora" if es else "Acarreos Makena website on desktop"}" width="1440" height="900" loading="lazy"></div>
            <div class="vitrina-caso__movil"><img src="{pre}img/caso-acarreos-movil.webp" alt="{"Página web de Acarreos Makena en celular" if es else "Acarreos Makena website on mobile"}" width="390" height="844" loading="lazy"></div>
            <figcaption class="vitrina-caso__sello"><span class="vitrina-caso__mk">MK</span>Acarreos Makena <i>×</i> Enlaza Studio</figcaption>
          </figure>
          <div class="ficha" data-revelar>
            <p class="ficha__nombre"><b>{T["caso_nombre"]}</b><span>{T["caso_categoria"]}</span></p>
            {cita}
            <ol class="ficha__bloques">{bloques}</ol>
            <div class="ficha__sistemas"><small>{T["caso_sistemas_t"]}</small><ul>{sistemas}</ul></div>
            <div class="ficha__enlaces">
              <a class="boton boton--menta" href="{enlace_caso}">{T["caso_completo"]} {I["flecha"]}</a>
              <a class="enlace-flecha enlace-flecha--claro" href="https://acarreosmakena.com/" target="_blank" rel="noopener">{T["caso_cta"]} <span>{I["flecha"]}</span></a>
            </div>
          </div>
        </div>
        <div class="resultados" data-revelar>
          <div class="resultados__lista"><p class="etiqueta">{T["caso_resultados_t"]}</p><ul>{resultados}</ul></div>
          <ul class="cifras">{cifras}</ul>
        </div>
      </div>
    </section>
'''


def proceso_html(T):
    iconos = ["lupa", "plano", "codigo", "soporte"]
    hitos = "".join(
        f'<li class="hito" data-revelar style="transition-delay:{i * .1}s"><span class="hito__punto"><b>0{i + 1}</b></span>'
        f'<div class="hito__tarjeta"><span class="hito__ico">{I[iconos[i]]}</span><h3>{t}</h3>'
        f'<p><small>{T["proc_hacemos"]}</small>{hace}</p><p class="hito__recibes"><small>{T["proc_recibes"]}</small>{recibe}</p></div></li>'
        for i, (t, hace, recibe) in enumerate(T["proceso"]))
    return f'''    <section class="seccion proceso-sec" id="proceso-trabajo">
      <div class="contenedor">
        <header class="cabeza cabeza--partida" data-revelar>
          <div><p class="etiqueta">{T["proc_etiqueta"]}</p><h2>{T["proc_h2"]}</h2></div>
          <p>{T["proc_p"]}</p>
        </header>
        <ol class="proceso" id="proceso"><span class="proceso__linea" aria-hidden="true"><i></i></span>{hitos}</ol>
      </div>
    </section>
'''


def preguntas(T):
    cats = "".join(f'<li><a href="#faq-{j + 1}">{c}</a></li>' for j, (c, _) in enumerate(T["faqs"]))
    grupos = "".join(
        f'<div class="faq__grupo" id="faq-{j + 1}"><h3>{c}</h3>' + "".join(
            f'<details class="pregunta"><summary>{q}</summary><p>{a}</p></details>' for q, a in lista) + "</div>"
        for j, (c, lista) in enumerate(T["faqs"]))
    return f'''    <section class="seccion faq" id="preguntas">
      <div class="contenedor faq__grid">
        <div class="faq__lado">
          <header class="cabeza" data-revelar><p class="etiqueta">{T["faq_etiqueta"]}</p><h2>{T["faq_h2"]}</h2><p>{T["faq_p"]}</p></header>
          <nav class="faq__cats" aria-label="{T["faq_etiqueta"]}"><ul>{cats}</ul></nav>
        </div>
        <div class="faq__lista">{grupos}</div>
      </div>
    </section>
'''


def contacto(T, wa, wa_attr, privacidad_href):
    F = T["form"]
    opciones = "".join(f'<label class="opcion"><input type="checkbox" name="necesita" value="{o}"><span>{o}</span></label>' for o in F["opciones"])
    rangos = "".join(f"<option>{r}</option>" for r in F["rangos"])
    puntos = "".join(f'<li>{I["check"]}{x}</li>' for x in F["puntos"])
    return f'''    <section class="seccion contacto" id="contacto">
      <span id="proyecto" aria-hidden="true"></span>
      <div class="contenedor contacto__caja">
        <div class="contacto__texto" data-revelar>
          <p class="etiqueta">{F["etiqueta"]}</p>
          <h2>{F["h2"]}</h2>
          <p>{F["p"]}</p>
          <ul class="contacto__puntos">{puntos}</ul>
          <p class="contacto__wa"><small>{F["o_wa"]}</small><a href="{wa}"{wa_attr}>{I["wa"]} WhatsApp {marco.TEL}</a></p>
        </div>
        <div class="contacto__form" data-revelar>
          <form class="formulario" id="formulario" novalidate>
            <div class="campos">
              <label class="campo"><span>{F["nombre"]} *</span><input name="nombre" autocomplete="name" maxlength="80" required></label>
              <label class="campo"><span>{F["empresa"]}</span><input name="empresa" autocomplete="organization" maxlength="100"></label>
              <label class="campo"><span>{F["whatsapp"]} *</span><input name="contacto" type="tel" inputmode="tel" autocomplete="tel" maxlength="40" placeholder="6000-0000" required></label>
              <label class="campo"><span>{F["correo"]} <em>({F["opcional"]})</em></span><input name="correo" type="email" autocomplete="email" maxlength="80"></label>
              <fieldset class="campo campo--ancho"><legend>{F["necesita"]}</legend><div class="opciones">{opciones}</div></fieldset>
              <label class="campo campo--ancho"><span>{F["mensaje"]}</span><textarea name="mensaje" rows="3" maxlength="1500" placeholder="{F["ph_mensaje"]}"></textarea></label>
              <label class="campo campo--ancho"><span>{F["presupuesto"]} <em>({F["opcional"]})</em></span><select name="presupuesto">{rangos}</select></label>
              <label class="trampa" aria-hidden="true">Web <input name="web" tabindex="-1" autocomplete="off"></label>
            </div>
            <p class="formulario__error" id="form-error" role="alert"></p>
            <button class="boton boton--oscuro boton--ancho" type="submit">{F["enviar"]} {I["flecha"]}</button>
            <p class="formulario__nota">{I["escudo"]} {F["privacidad"]} <a href="{privacidad_href}">{F["privacidad_enlace"]}</a></p>
          </form>
          <div class="gracias" id="gracias" hidden>
            <span class="gracias__ico">{I["check"]}</span>
            <h3>{F["ok_t"]}</h3>
            <p>{F["ok_p"]}</p>
            <a class="boton boton--menta" id="gracias-wa" href="{wa}"{wa_attr}>{I["wa"]} {F["ok_wa"]}</a>
          </div>
        </div>
      </div>
    </section>
'''


def pagina(T):
    lang = T["lang"]
    pre = "../" if T["ruta"] else ""
    url = CONFIG["dominio"] + T["ruta"]
    wa = wa_link(T["wa_msg"])
    wa_attr = ' target="_blank" rel="noopener"'
    rel = lambda k: paginas.RUTAS[lang][k].replace("en/", "", 1) if T["ruta"] else paginas.RUTAS[lang][k]
    inicio = "./"
    otra = f'{pre}{T["otra_ruta"] or "./"}'
    servicios_pie = [(paginas.SERVICIOS[lang][k]["titulo"], rel(k)) for k in paginas.ORDEN_SERVICIOS]

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": CONFIG["dominio"] + "#empresa", "name": "Enlaza Studio", "url": CONFIG["dominio"],
         "slogan": T["eslogan"], "description": T["descripcion"], "areaServed": {"@type": "Country", "name": "Panamá"},
         "telephone": "+" + CONFIG["whatsapp"], "image": CONFIG["dominio"] + "img/compartir.jpg",
         "knowsAbout": ["Web development", "Local SEO", "CRM", "API integrations", "Automation", "Google Sheets"]},
        {"@type": "WebSite", "name": "Enlaza Studio", "url": CONFIG["dominio"], "inLanguage": ["es", "en"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                            for _, lista in T["faqs"] for q, a in lista]}]}
    alternos = [("es", CONFIG["dominio"]), ("en", CONFIG["dominio"] + "en/"), ("x-default", CONFIG["dominio"])]
    imagen = CONFIG["dominio"] + "img/" + ("compartir.jpg" if lang == "es" else "compartir-en.jpg")
    precarga = f'\n  <link rel="preload" as="image" href="{pre}img/escena-base.webp" type="image/webp">'

    linea = "".join(f"<li>{x}</li>" for x in T["linea"])
    burbujas = "".join(f'<span class="escena-3d__burbuja escena-3d__burbuja--{n}" aria-hidden="true">{I["wa"]}<i></i><i></i></span>' for n in (1, 2, 3))
    F = T["form"]
    form_cfg = json.dumps({"crm": CONFIG["crm"], "wa": CONFIG["whatsapp"], "lang": lang, "enviando": F["enviando"], "enviar": F["enviar"], "error": F["error"]},
                          ensure_ascii=False).replace("</", "<\\/")
    avisos_json = json.dumps(T["avisos"], ensure_ascii=False).replace("</", "<\\/")

    return (marco.head(lang, pre, T["titulo"], T["descripcion"], url, alternos, imagen, ld, precarga)
            + '<body class="portada-pagina">\n'
            + marco.cabecera(lang, inicio, otra, wa, wa_attr, I, LOGO, en_portada=True)
            + f'''
  <main>
    <section class="hero" id="inicio">
      <div class="hero__ambiente" aria-hidden="true"><span></span><span></span><span></span>
        <svg viewBox="0 0 800 800" preserveAspectRatio="xMidYMid slice"><circle cx="400" cy="400" r="210"/><circle cx="400" cy="400" r="300"/><circle cx="400" cy="400" r="390"/></svg><i></i></div>
      <div class="contenedor hero__grid">
        <div class="hero__texto">
          <p class="sello aparece" style="--a:.1s"><span class="sello__punto" aria-hidden="true"></span>{T["etiqueta"]}</p>
          <h1 class="titulo-animado titular">{T["h1"]}</h1>
          <p class="hero__lead aparece" style="--a:.55s">{T["lead"]}</p>
          <div class="hero__botones aparece" style="--a:.7s">
            <a class="boton boton--menta" href="{wa}"{wa_attr}>{I["wa"]} {T["cta_principal"]}</a>
            <a class="boton boton--linea" href="#servicios">{T["cta_secundario"]} <span class="boton__flecha">{I["flecha"]}</span></a>
          </div>
          <ul class="hero__linea aparece" style="--a:.85s">{linea}</ul>
          <p class="hero__trabajo aparece" style="--a:1s">{T["trabajo_reciente"]} <a href="https://acarreosmakena.com/" target="_blank" rel="noopener">Acarreos Makena <span aria-hidden="true">↗</span></a></p>
        </div>
        <div class="escena-portada aparece" style="--a:.4s">
          <div class="escena-3d">
            <img class="escena-3d__base" src="{pre}img/escena-base.webp" alt="{T["portada_alt"]}" width="1536" height="1024" fetchpriority="high">
            <span class="escena-3d__sombra" aria-hidden="true"></span>
            <img class="escena-3d__persona" src="{pre}img/escena-persona.webp" alt="" width="357" height="900" aria-hidden="true">
            <span class="escena-3d__brillo" aria-hidden="true"></span>
            <span class="escena-3d__contador" aria-hidden="true">12</span>
            {burbujas}
          </div>
          <div class="escena-portada__aviso" id="aviso" aria-hidden="true"><span class="aviso__ico">{I["chat"]}</span><span><b id="aviso-titulo">{T["avisos"][0][0]}</b><small id="aviso-texto">{T["avisos"][0][1]}</small></span><i class="escena-portada__punto"></i></div>
          <p class="escena-portada__pie"><i></i>{T["portada_pie"]}</p>
        </div>
      </div>
    </section>

{problemas(T)}
    {integraciones.seccion(lang, NUCLEO, wa, wa_attr, I)}

{flujo(T)}
{servicios_html(T, rel)}

{proceso_html(T)}
{preguntas(T)}
{contacto(T, wa, wa_attr, rel("privacidad"))}
    <section class="final">
      <div class="final__ambiente" aria-hidden="true"><span></span><span></span></div>
      <div class="contenedor final__caja">
        <p class="sello"><span class="sello__punto" aria-hidden="true"></span>{T["eslogan"]}</p>
        <h2>{T["cierre_h2"]}</h2>
        <p>{T["cierre_p"]}</p>
        <a class="boton boton--menta boton--grande" href="{wa}"{wa_attr}>{I["wa"]} {T["cierre_wa"]}</a>
      </div>
    </section>
  </main>

'''
            + marco.pie(lang, pre, inicio, otra, wa, wa_attr, I, LOGO, servicios_pie, rel("privacidad"), en_portada=True)
            + f'''  <script>window.CONEKTRA_AVISOS = {avisos_json}; window.CONEKTRA_FORM = {form_cfg};</script>
  <script src="{pre}js/main.js?v={marco.V_JS}" defer></script>
</body>
</html>
''')


if __name__ == "__main__":
    os.makedirs(os.path.join(RAIZ, "en"), exist_ok=True)
    # portada 3.0 (inicio.py + textos3.py); pagina() queda como referencia de la versión 2.0
    for T, destino in ((textos3.ES, "index.html"), (textos3.EN, "en/index.html")):
        with open(os.path.join(RAIZ, destino), "w", encoding="utf-8", newline="\n") as f:
            f.write(inicio.pagina(T, CONFIG, wa_link))
        print("ok", destino)
    import landing
    lp = landing.generar(RAIZ, CONFIG, wa_link)
    print("ok", len(lp), "páginas de servicio (SEO):", ", ".join(lp))
    hechas = paginas.generar(RAIZ, CONFIG, I, LOGO, extra=lp)
    extra = landing.generar_extra(RAIZ, CONFIG, wa_link)
    print("ok diseño 3.0:", ", ".join(extra))
    print("ok", len(hechas), "páginas internas + 404, sitemap y robots")
    if copiar_portal():
        print("ok portal -> app/")
