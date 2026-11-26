"""Portada 3.0 de Enlaza Studio: estructura HTML (español e inglés).

Estética: mezcla clara (portada, soluciones, preguntas, contacto) y oscura (red, proceso, cierre, pie).
Tipografía Geist. La escena 3D (img/escena-base.webp + escena-persona.webp) se conserva intacta en la sección «Para negocios reales».
Estilos en css/v3.css, interacciones en js/v3.js.
"""
import json
import math
import integraciones
import paginas
from iconos import I, LOGO

V_CSS = "8"
V_JS = "2"
FUENTES = "https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&display=swap"
TEL = "+507 6552-3134"
MARCA = LOGO.replace('aria-hidden="true"', 'aria-hidden="true" class="marca__simbolo"')


def _head(T, cfg, pre, ld):
    d = cfg["dominio"]
    url = d + T["ruta"]
    imagen = d + "img/" + ("compartir.jpg" if T["lang"] == "es" else "compartir-en.jpg")
    alt = "".join(f'\n  <link rel="alternate" hreflang="{h}" href="{u}">' for h, u in (("es", d), ("en", d + "en/"), ("x-default", d)))
    return f'''<!doctype html>
<html lang="{T["lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{T["titulo"]}</title>
  <meta name="description" content="{T["descripcion"]}">
  <link rel="canonical" href="{url}">{alt}
  <meta name="theme-color" content="#fbfbf8">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Enlaza Studio">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{T["titulo"]}">
  <meta property="og:description" content="{T["descripcion"]}">
  <meta property="og:locale" content="{"es_PA" if T["lang"] == "es" else "en_US"}">
  <meta property="og:image" content="{imagen}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{imagen}">
  <link rel="icon" href="{pre}img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{pre}img/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="{pre}img/apple-touch-icon.png">
  <link rel="manifest" href="{pre}manifest.webmanifest">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FUENTES}" rel="stylesheet">
  <link rel="stylesheet" href="{pre}css/v3.css?v={V_CSS}">
</head>
'''


def _cabecera(T, wa, otra):
    nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in T["nav"])
    return f'''  <header class="cab" id="cab">
    <div class="cab__barra">
      <a class="marca" href="./" aria-label="Enlaza Studio">{MARCA}<span>Enlaza Studio</span></a>
      <nav class="cab__nav" id="menu" aria-label="Principal">
        {nav}
        <a class="cab__idioma" href="{otra}" hreflang="{T["otra"].lower()}" title="{T["otra_nombre"]}">{T["otra"]}</a>
        <a class="btn btn--tinta btn--chico" href="{wa}" target="_blank" rel="noopener">{T["cta"]} {I["flecha"]}</a>
      </nav>
      <button class="cab__menu" id="hamburguesa" type="button" aria-label="{T["menu"]}" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
'''


def _panel(T):
    P = T["panel"]
    iconos_menu = ["base", "crm", "factura", "pago", "grafica", "rayo"]
    menu = "".join(f'<li{" class=\"activo\"" if j == 0 else ""}>{I[iconos_menu[j]]}<span>{m}</span>{"<b>3</b>" if j == 3 else ""}</li>' for j, m in enumerate(P["menu"]))
    kpis = "".join(f'<div class="kpi"><small>{t}</small><b>{v}</b><span>{s}</span></div>' for t, v, s in P["kpis"])
    filas = "".join(f'<li class="act" style="--i:{j}"><span class="act__ico act__ico--{ic}">{I[ic]}</span><span class="act__txt"><b>{t}</b><small>{s}</small></span><time>{h}</time></li>'
                    for j, (ic, t, s, h) in enumerate(P["actividad"]))
    tope = max(v for _, v in P["embudo"])
    barras = "".join(f'<li><span>{t}</span><i style="--v:{v / tope:.2f}"><b>{v}</b></i></li>' for t, v in P["embudo"])
    reporte = "".join(f"<li>{r}</li>" for r in P["reporte"])
    return f'''<div class="producto" aria-hidden="true">
          <div class="producto__rejilla"></div>
          <div class="app">
            <aside class="app__lado">
              <span class="app__marca">{MARCA}</span>
              <ul class="app__menu">{menu}</ul>
            </aside>
            <div class="app__main">
              <div class="app__top"><div><small>{P["saludo"]}</small><b>Enlaza Studio</b></div><span class="app__chip"><i></i>{P["fecha"]}</span><span class="app__buscar">{I["lupa"]}<i></i></span><span class="app__avatar">AM</span></div>
              <div class="app__kpis">{kpis}</div>
              <div class="app__cuerpo">
                <section class="app__caja app__actividad"><h4><span class="vivo"></span>{P["actividad_t"]}</h4><ul class="act__lista" id="actividad">{filas}</ul></section>
                <section class="app__caja app__embudo"><h4>{P["embudo_t"]}</h4><ul class="barras">{barras}</ul>
                  <svg class="linea-graf" viewBox="0 0 200 60" preserveAspectRatio="none"><defs><linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#36c98a" stop-opacity=".35"/><stop offset="1" stop-color="#36c98a" stop-opacity="0"/></linearGradient></defs>
                    <path d="M0 48 L25 44 L50 46 L75 34 L100 37 L125 26 L150 28 L175 15 L200 10 L200 60 L0 60Z" fill="url(#gArea)"/><path class="linea-graf__trazo" d="M0 48 L25 44 L50 46 L75 34 L100 37 L125 26 L150 28 L175 15 L200 10" fill="none" stroke="#1f9e66" stroke-width="2"/></svg>
                </section>
              </div>
            </div>
          </div>
          <div class="telefono">
            <div class="telefono__cab">{MARCA}<span><b>Enlaza Studio</b><small>{P["reporte_t"]}</small></span></div>
            <div class="telefono__chat"><div class="globo"><b>{P["reporte_t"]} ☀️</b><ul>{reporte}</ul><small>{P["reporte_hora"]} ✓✓</small></div></div>
          </div>
          <span class="producto__ejemplo">{P["ejemplo"]}</span>
        </div>'''


def _herramientas(T):
    usar = [x for x in integraciones.ITEMS if x[1] in ("op", "disp")]
    logos = "".join(f'<li title="{n}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{r}"/></svg><span>{n}</span></li>' for n, _, r, _c, _s in usar)
    return f'''<div class="herr" data-revelar><p>{T["herramientas_t"]}</p><ul>{logos}</ul></div>'''


def _vis(clave, T):
    V = T["vis"]
    if clave == "atrae":
        return f'''<div class="vis vis--atrae">
            <div class="nav-mini"><div class="nav-mini__barra"><i></i><i></i><i></i><span>{I["escudo"]}{V["web_url"]}</span></div>
              <div class="sitio"><div class="sitio__nav"><b>{MARCA}</b><i></i><i></i><i></i></div><h5>{V["web_h"]}</h5><p><i></i><i></i></p><span class="sitio__btn">{I["wa"]}{V["web_btn"]}</span><div class="sitio__fotos"><i></i><i></i><i></i></div></div></div>
            <div class="flot flot--google"><span class="flot__busca">{I["lupa"]}{V["google"]}</span><span class="res res--tu"><b>{V["google_tu"]}</b><small>★★★★★ · {I["wa"]}</small></span><span class="res"><i></i></span><span class="res"><i></i></span></div>
            <div class="flot flot--toast">{I["check"]}<span><b>{V["web_ok"]}</b><small>WhatsApp · {T["panel"]["fecha"]}</small></span></div>
          </div>'''
    if clave == "vende":
        cols = "".join(f'<div class="kan__col"><h6>{t}<b>{len(c)}</b></h6>' + "".join(f'<span class="kan__tarj"><i>{x[0]}</i>{x}</span>' for x in c) + "</div>" for t, c in V["crm_cols"])
        return f'''<div class="vis vis--vende"><div class="ventana-v"><div class="kan">{cols}</div></div>
            <div class="flot flot--rec">{I["reloj"]}<span><b>{V["crm_recordatorio"]}</b><small>{V["crm_rec_txt"]}</small></span></div></div>'''
    if clave == "cobra":
        filas = "".join(f'<li><span class="cob__nom"><i>{n[0]}</i>{n}</span><b>{m}</b><span class="pill pill--{e}">{s}</span></li>' for n, m, s, e in V["cobros"])
        return f'''<div class="vis vis--cobra"><div class="ventana-v"><div class="cob__cab"><small>{V["cobro_t"]}</small><b>{V["cobro_total"]}</b></div><ul class="cob">{filas}</ul></div>
            <div class="flot flot--wa"><span class="flot__wa">{I["wa"]}</span><p>{V["cobro_msg"]}</p></div></div>'''
    if clave == "controla":
        rep = "".join(f"<li>{r}</li>" for r in T["panel"]["reporte"])
        barras = "".join(f'<i style="--h:{h}"></i>' for h in (40, 55, 35, 70, 62, 85, 78))
        return f'''<div class="vis vis--controla"><div class="ventana-v graf"><small>{T["panel"]["embudo_t"]}</small><b>$12,480</b><div class="graf__barras">{barras}</div></div>
            <div class="telefono telefono--chico"><div class="telefono__cab">{MARCA}<span><b>Enlaza Studio</b><small>{V["rep_t"]}</small></span></div>
              <div class="telefono__chat"><div class="globo"><b>{V["rep_t"]} ☀️</b><ul>{rep}</ul><small>{T["panel"]["reporte_hora"]} ✓✓</small></div></div></div></div>'''
    nodos = "".join(f'<span class="nodo nodo--{j}">{x}</span>' for j, x in enumerate(V["conecta"]))
    return f'''<div class="vis vis--conecta">
            <svg class="vis__lineas" viewBox="0 0 400 300" preserveAspectRatio="none"><path d="M200 150 L70 60"/><path d="M200 150 L330 60"/><path d="M200 150 L60 170"/><path d="M200 150 L340 170"/><path d="M200 150 L200 260" class="dash"/></svg>
            <span class="nodo nodo--centro">{MARCA}{V["conecta_centro"]}</span>{nodos}<span class="nodo nodo--dev">{V["conecta_dev"]}</span></div>'''


def _soluciones(T, rel, wa):
    items, vistas = [], []
    for j, S in enumerate(T["soluciones"]):
        puntos = "".join(f"<li>{I['check']}{p}</li>" for p in S["puntos"])
        txt, clave = S["enlace"]
        href = rel(clave) if clave else wa
        extra = "" if clave else ' target="_blank" rel="noopener"'
        vis = _vis(S["id"], T)
        items.append(f'''<article class="sol__item{" activo" if j == 0 else ""}" data-sol="{j}" id="sol-{S["id"]}">
            <p class="sol__tag"><span>{S["n"]}</span>{S["tag"]}</p>
            <h3>{S["titulo"]}</h3>
            <p>{S["texto"]}</p>
            <ul>{puntos}</ul>
            <a class="enlace" href="{href}"{extra}>{txt} {I["flecha"]}</a>
            <div class="sol__vis-movil" aria-hidden="true">{vis}</div>
          </article>''')
        vistas.append(f'<div class="sol__vista{" activo" if j == 0 else ""}" data-vista="{j}">{vis}</div>')
    indice = "".join(f'<li><a href="#sol-{S["id"]}" data-ir="{j}"{" class=\"activo\"" if j == 0 else ""}>{S["tag"]}</a></li>' for j, S in enumerate(T["soluciones"]))
    return f'''    <section class="sec sec--clara soluciones" id="soluciones">
      <div class="cont">
        <header class="encabezado" data-revelar><p class="etq">{T["sol_etiqueta"]}</p><h2>{T["sol_h2"]}</h2><p>{T["sol_p"]}</p></header>
        <div class="sol">
          <div class="sol__lista">{"".join(items)}</div>
          <div class="sol__fijo" aria-hidden="true">
            <ul class="sol__indice">{indice}</ul>
            <div class="sol__escenario"><div class="sol__rejilla"></div>{"".join(vistas)}</div>
          </div>
        </div>
      </div>
    </section>
'''


def _red(T):
    lang = T["lang"]
    items = integraciones.ITEMS
    # 13 puestos repartidos en una elipse alrededor del centro (50 %, 50 %), empezando arriba:
    # operativas arriba, disponibles a los lados y las que requieren desarrollo abajo
    puestos = [(50 + 41 * math.cos(math.radians(-90 + k * 360 / 13)), 50 + 40 * math.sin(math.radians(-90 + k * 360 / 13))) for k in range(13)]
    orden = {"op": [12, 0, 1], "disp": [11, 2, 10, 3, 9], "dev": [8, 4, 7, 5, 6]}
    usados = {"op": 0, "disp": 0, "dev": 0}
    nodos, lineas, pulsos = [], [], []
    for n, est, ruta, color, sub in items:
        x, y = puestos[orden[est][usados[est]]]
        usados[est] += 1
        ico = (f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="{color}" d="{ruta}"/></svg>' if ruta
               else f'<span class="sigla" style="background:{color}">{integraciones.SIGLAS.get(n, n[:2])}</span>')
        nodos.append(f'<li class="herr-nodo herr-nodo--{est}" style="left:{x:.2f}%;top:{y:.2f}%"><span class="herr-nodo__ico">{ico}</span><b>{n}</b><small>{sub[0 if lang == "es" else 1]}</small></li>')
        # el lienzo SVG mide 160 × 100 (misma proporción que el mapa) para que los pulsos queden redondos
        lineas.append(f'<line x1="80" y1="50" x2="{x * 1.6:.2f}" y2="{y:.2f}" class="l l--{est}"/>')
        if est == "op":
            pulsos.append(f'<circle r="1" class="pulso"><animateMotion dur="{2.2 + len(pulsos) * .5}s" repeatCount="indefinite" path="M80 50 L{x * 1.6:.2f} {y:.2f}"/></circle>')
    leyenda = "".join(f'<li class="ley ley--{k}"><i></i>{v}</li>' for k, v in T["estados"].items())
    principios = "".join(f'<li class="princ" data-revelar><span>{I[ic]}</span><h3>{t}</h3><p>{p}</p></li>' for ic, t, p in T["principios"])
    pulsos = "".join(pulsos)
    return f'''    <section class="sec sec--oscura red" id="integraciones">
      <div class="red__brillo" aria-hidden="true"></div>
      <div class="cont">
        <header class="encabezado encabezado--centro" data-revelar><p class="etq">{T["red_etiqueta"]}</p><h2>{T["red_h2"]}</h2><p>{T["red_p"]}</p></header>
        <ul class="leyenda" data-revelar>{leyenda}</ul>
        <div class="mapa" data-revelar>
          <svg class="mapa__lineas" viewBox="0 0 160 100" preserveAspectRatio="none" aria-hidden="true">{"".join(lineas)}{pulsos}</svg>
          <div class="mapa__centro">{MARCA}<b>Enlaza Studio</b></div>
          <ul class="mapa__nodos">{"".join(nodos)}</ul>
        </div>
        <ul class="principios">{principios}</ul>
      </div>
    </section>
'''


def _proceso(T):
    pasos = "".join(f'<li class="paso" data-revelar style="--i:{j}"><span class="paso__n">0{j + 1}</span><h3>{t}</h3><p>{p}</p><p class="paso__recibe"><small>{T["proc_recibes"]}</small>{r}</p></li>'
                    for j, (t, p, r) in enumerate(T["proceso"]))
    modos = "".join(f'<article class="modo{" modo--destacado" if j == 1 else ""}" data-revelar><h3>{t}</h3><p>{p}</p><ul>' + "".join(f"<li>{I['check']}{x}</li>" for x in lst) + "</ul></article>"
                    for j, (t, p, lst) in enumerate(T["modos"]))
    return f'''    <section class="sec sec--oscura proceso" id="como-trabajamos">
      <div class="cont">
        <header class="encabezado encabezado--partido" data-revelar><div><p class="etq">{T["proc_etiqueta"]}</p><h2>{T["proc_h2"]}</h2></div><p>{T["proc_p"]}</p></header>
        <ol class="pasos" id="pasos"><span class="pasos__linea" aria-hidden="true"><i></i></span>{pasos}</ol>
        <div class="modos">{modos}</div>
      </div>
    </section>
'''


def _real(T, pre):
    burbujas = "".join(f'<span class="escena-3d__burbuja escena-3d__burbuja--{n}" aria-hidden="true">{I["wa"]}<i></i><i></i></span>' for n in (1, 2, 3))
    rutas_sector = {"Mudanzas y transporte": "sistema-para-mudanzas/", "Talleres y servicios técnicos": "sistema-para-talleres/",
                    "Clínicas y consultorios": "sistema-para-clinicas/", "Tiendas y catálogos": "pedidos-por-whatsapp/",
                    "Construcción y mantenimiento": "sistema-para-contratistas/"} if T["lang"] == "es" else {}
    sectores = "".join(f'<li><a href="{rutas_sector[s]}">{s}</a></li>' if s in rutas_sector else f"<li>{s}</li>" for s in T["sectores"])
    return f'''    <section class="sec sec--clara real" id="negocios">
      <div class="cont real__grid">
        <div class="escena-portada" data-revelar>
          <div class="escena-3d">
            <img class="escena-3d__base" src="{pre}img/escena-base.webp" alt="{T["portada_alt"]}" width="1536" height="1024" loading="lazy">
            <span class="escena-3d__sombra" aria-hidden="true"></span>
            <img class="escena-3d__persona" src="{pre}img/escena-persona.webp" alt="" width="357" height="900" aria-hidden="true" loading="lazy">
            <span class="escena-3d__brillo" aria-hidden="true"></span>
            <span class="escena-3d__contador" aria-hidden="true">12</span>
            {burbujas}
          </div>
          <div class="escena-portada__aviso" id="aviso" aria-hidden="true"><span class="aviso__ico">{I["chat"]}</span><span><b id="aviso-titulo">{T["avisos"][0][0]}</b><small id="aviso-texto">{T["avisos"][0][1]}</small></span><i class="escena-portada__punto"></i></div>
          <p class="escena-portada__pie"><i></i>{T["escena_pie"]}</p>
        </div>
        <div class="real__texto" data-revelar>
          <p class="etq">{T["real_etiqueta"]}</p>
          <h2>{T["real_h2"]}</h2>
          <p>{T["real_p"]}</p>
          <ul class="chips">{sectores}</ul>
          <p class="real__trabajo">{T["trabajo_reciente"]} <a href="https://acarreosmakena.com/" target="_blank" rel="noopener">Acarreos Makena <span aria-hidden="true">↗</span></a></p>
        </div>
      </div>
    </section>
'''


def _preguntas(T):
    lista = "".join(f'<details class="preg"><summary>{q}<i aria-hidden="true"></i></summary><p>{a}</p></details>' for q, a in T["faqs"])
    return f'''    <section class="sec sec--clara faq" id="preguntas">
      <div class="cont faq__grid">
        <header class="encabezado" data-revelar><p class="etq">{T["faq_etiqueta"]}</p><h2>{T["faq_h2"]}</h2><p>{T["faq_p"]}</p></header>
        <div class="faq__lista" data-revelar>{lista}</div>
      </div>
    </section>
'''


def _contacto(T, wa, privacidad):
    F = T["form"]
    opciones = "".join(f'<label class="op"><input type="checkbox" name="necesita" value="{o}"><span>{o}</span></label>' for o in F["opciones"])
    rangos = "".join(f"<option>{r}</option>" for r in F["rangos"])
    puntos = "".join(f'<li>{I["check"]}{x}</li>' for x in F["puntos"])
    return f'''    <section class="sec sec--clara contacto" id="contacto">
      <div class="cont contacto__caja" data-revelar>
        <div class="contacto__texto">
          <p class="etq">{F["etiqueta"]}</p>
          <h2>{F["h2"]}</h2>
          <p>{F["p"]}</p>
          <ul class="contacto__puntos">{puntos}</ul>
          <p class="contacto__wa"><small>{F["o_wa"]}</small><a href="{wa}" target="_blank" rel="noopener">{I["wa"]} WhatsApp {TEL}</a><a href="mailto:hola@enlazastudio.com">✉ hola@enlazastudio.com</a></p>
        </div>
        <div class="contacto__form">
          <form class="form" id="formulario" novalidate>
            <div class="form__campos">
              <label class="campo"><span>{F["nombre"]} *</span><input name="nombre" autocomplete="name" maxlength="80" required></label>
              <label class="campo"><span>{F["empresa"]}</span><input name="empresa" autocomplete="organization" maxlength="100"></label>
              <label class="campo"><span>{F["whatsapp"]} *</span><input name="contacto" type="tel" inputmode="tel" autocomplete="tel" maxlength="40" placeholder="6000-0000" required></label>
              <label class="campo"><span>{F["correo"]} <em>({F["opcional"]})</em></span><input name="correo" type="email" autocomplete="email" maxlength="80"></label>
              <fieldset class="campo campo--ancho"><legend>{F["necesita"]}</legend><div class="ops">{opciones}</div></fieldset>
              <label class="campo campo--ancho"><span>{F["mensaje"]}</span><textarea name="mensaje" rows="3" maxlength="1500" placeholder="{F["ph_mensaje"]}"></textarea></label>
              <label class="campo campo--ancho"><span>{F["presupuesto"]} <em>({F["opcional"]})</em></span><select name="presupuesto">{rangos}</select></label>
              <label class="trampa" aria-hidden="true">Web <input name="web" tabindex="-1" autocomplete="off"></label>
            </div>
            <p class="form__error" id="form-error" role="alert"></p>
            <button class="btn btn--tinta btn--ancho" type="submit">{F["enviar"]} {I["flecha"]}</button>
            <p class="form__nota">{I["escudo"]} {F["privacidad"]} <a href="{privacidad}">{F["privacidad_enlace"]}</a></p>
          </form>
          <div class="gracias" id="gracias" hidden>
            <span class="gracias__ico">{I["check"]}</span>
            <h3>{F["ok_t"]}</h3>
            <p>{F["ok_p"]}</p>
            <a class="btn btn--verde" id="gracias-wa" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {F["ok_wa"]}</a>
          </div>
        </div>
      </div>
    </section>
'''


def _final_y_pie(T, wa, otra, rel):
    P = T["pie"]
    cobranza = "Cobranza automática" if T["lang"] == "es" else "Automatic collections"
    sol = "".join(f'<a href="{rel(S["enlace"][1]) if S["enlace"][1] and T["lang"] == "es" else "#sol-" + S["id"]}">{S["enlace"][0] if S["enlace"][1] else cobranza}</a>' for S in T["soluciones"])
    emp = "".join(f'<a href="#{i}">{t}</a>' for i, t in T["nav"][1:])
    return f'''    <section class="final cierre" id="final">
      <canvas class="final__campo" id="campo-final" aria-hidden="true"></canvas>
      <div class="cont final__caja" data-revelar>
        <span class="final__marca">{MARCA}</span>
        <h2>{T["cierre_h2"]}</h2>
        <p>{T["cierre_p"]}</p>
        <div class="final__botones"><a class="btn btn--verde btn--grande" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {T["cierre_cta"]}</a><a class="btn btn--claro btn--grande" href="mailto:hola@enlazastudio.com">✉ {T["correo_btn"]}</a></div>
      </div>
    </section>
  </main>

  <footer class="pie cierre">
    <div class="cont">
      <div class="pie__grid">
        <div class="pie__marca"><a class="marca" href="./">{MARCA}<span>Enlaza Studio</span></a><p>{T["eslogan"]}</p><p class="pie__desc">{P["desc"]}</p></div>
        <nav aria-label="{P["soluciones"]}"><h2>{P["soluciones"]}</h2>{sol}</nav>
        <nav aria-label="{P["empresa"]}"><h2>{P["empresa"]}</h2>{emp}<a href="{rel("privacidad")}">{P["privacidad"]}</a></nav>
        <div><h2>{P["contacto"]}</h2><a class="pie__wa" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {TEL}</a><a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a><a href="#contacto">{P["form"]}</a><a href="{otra}">{T["otra_nombre"]} {I["flecha"]}</a></div>
      </div>
      <p class="pie__gigante" aria-hidden="true">Enlaza Studio</p>
      <div class="pie__base"><span>{P["derechos"]}</span><span>{P["hecho"]}</span></div>
    </div>
  </footer>
  <div class="barra-wa" id="barra-wa" aria-hidden="true">
    <span><b>{T["barra_t"]}</b>{T["barra_p"]}</span>
    <a class="btn btn--verde btn--chico" href="{wa}" target="_blank" rel="noopener" tabindex="-1">{I["wa"]} WhatsApp</a>
  </div>
'''


def pagina(T, cfg, wa_link):
    lang = T["lang"]
    pre = "../" if T["ruta"] else ""
    wa = wa_link(T["wa_msg"])
    rel = lambda k: paginas.RUTAS[lang][k].replace("en/", "", 1) if T["ruta"] else paginas.RUTAS[lang][k]
    otra = f'{pre}{T["otra_ruta"] or "./"}'
    d = cfg["dominio"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": d + "#empresa", "name": "Enlaza Studio", "alternateName": ["EnlazaStudio", "Enlaza"], "url": d, "slogan": T["eslogan"], "description": T["descripcion"],
         "areaServed": {"@type": "Country", "name": "Panamá"}, "telephone": "+" + cfg["whatsapp"], "email": "hola@enlazastudio.com", "image": d + "img/compartir.jpg", "logo": d + "img/icono-512.png",
         "knowsAbout": ["Diseño de páginas web", "SEO local", "CRM para WhatsApp", "Cobranza automática", "Automatización de WhatsApp Business", "WhatsApp Business API", "Integraciones", "Google Sheets"],
         "priceRange": "$$", "address": {"@type": "PostalAddress", "addressLocality": "Ciudad de Panamá", "addressCountry": "PA"}},
        {"@type": "WebSite", "name": "Enlaza Studio", "alternateName": ["EnlazaStudio", "Enlaza", "enlazastudio.com"], "url": d, "inLanguage": ["es", "en"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in T["faqs"]]}]}
    F = T["form"]
    form_cfg = json.dumps({"crm": cfg["crm"], "wa": cfg["whatsapp"], "lang": lang, "enviando": F["enviando"], "enviar": F["enviar"], "error": F["error"]},
                          ensure_ascii=False).replace("</", "<\\/")
    avisos = json.dumps(T["avisos"], ensure_ascii=False).replace("</", "<\\/")

    return (_head(T, cfg, pre, ld) + '<body>\n  <a class="saltar" href="#contenido">' + ("Saltar al contenido" if lang == "es" else "Skip to content") + "</a>\n"
            + _cabecera(T, wa, otra) + f'''
  <main id="contenido">
    <section class="hero">
      <canvas class="hero__campo" id="campo" aria-hidden="true"></canvas>
      <div class="cont hero__texto">
        <a class="anuncio entra" style="--d:0s" href="#sol-cobra"><span class="anuncio__tag">{T["anuncio_tag"]}</span>{T["anuncio"]} {I["flecha"]}</a>
        <h1 class="hero__h1 entra" style="--d:.04s">{T["h1_seo"]}</h1>
        <p class="hero__titular entra" style="--d:.08s">{T["h1_a"]}<br><span class="degradado">{T["h1_b"]}</span></p>
        <p class="hero__lead entra" style="--d:.18s">{T["lead"]}</p>
        <div class="hero__botones entra" style="--d:.28s">
          <a class="btn btn--tinta btn--grande" href="{wa}" target="_blank" rel="noopener">{I["wa"]} {T["cta1"]}</a>
          <a class="btn btn--claro btn--grande" href="#soluciones">{T["cta2"]} {I["flecha"]}</a>
        </div>
        <p class="hero__correo entra" style="--d:.32s">{T["correo_t"]} <a href="mailto:hola@enlazastudio.com">hola@enlazastudio.com</a></p>
        <p class="hero__nota entra" style="--d:.36s"><i></i>{T["nota_hero"]}</p>
      </div>
      <div class="cont-ancho hero__producto entra" style="--d:.45s">
        {_panel(T)}
      </div>
      <div class="cont">{_herramientas(T)}</div>
    </section>

{_soluciones(T, rel, wa)}
{_red(T)}
{_real(T, pre)}
{_proceso(T)}
{_preguntas(T)}
{_contacto(T, wa, rel("privacidad"))}
{_final_y_pie(T, wa, otra, rel)}  <script>window.CONEKTRA_AVISOS = {avisos}; window.CONEKTRA_FORM = {form_cfg};</script>
  <script src="{pre}js/v3.js?v={V_JS}" defer></script>
</body>
</html>
''')
