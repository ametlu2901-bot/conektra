"""Partes comunes de todas las páginas: <head>, menú superior, pie y barra de WhatsApp del celular.

Las usan build.py (portada) y paginas.py (páginas internas), para que todo el sitio comparta el mismo marco.
"""
import json

V_CSS = "10"   # subir cuando cambie css/conektra.css
V_JS = "13"   # subir cuando cambie js/main.js
FUENTES = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800"
           "&family=Inter:wght@300;400;500;600;700&family=Instrument+Serif:ital@1&display=swap")

UI = {
    "es": dict(nav=["Servicios", "Cómo funciona", "Preguntas frecuentes"], cta="Hablemos", otra="EN", otra_nombre="English",
               menu="Menú", servicios_t="Servicios", nav_t="Navegación", contacto_t="Contacto", privacidad="Política de privacidad",
               form="Escríbenos por el formulario", derechos="© 2026 Enlaza Studio. Todos los derechos reservados.", hecho="Hecho en Panamá.",
               eslogan="Tu negocio, mejor conectado.",
               desc="Estudio tecnológico que ayuda a pequeños negocios a conseguir clientes, ordenar su trabajo y conectar sus herramientas.",
               barra_t="¿Hablamos de tu negocio?", barra_p="Te respondemos por WhatsApp"),
    "en": dict(nav=["Services", "How it works", "FAQ"], cta="Let's talk", otra="ES", otra_nombre="Español",
               menu="Menu", servicios_t="Services", nav_t="Navigation", contacto_t="Contact", privacidad="Privacy policy",
               form="Write to us through the form", derechos="© 2026 Enlaza Studio. All rights reserved.", hecho="Made in Panama.",
               eslogan="Your business, better connected.",
               desc="Tech studio that helps small businesses win customers, organize their work and connect their tools.",
               barra_t="Shall we talk about your business?", barra_p="We reply on WhatsApp"),
}
TEL = "+507 6552-3134"


def head(lang, pre, titulo, descripcion, url, alternos, imagen, ld, extra=""):
    """alternos: lista de (hreflang, url). imagen: URL absoluta de la imagen para compartir."""
    alt = "".join(f'\n  <link rel="alternate" hreflang="{h}" href="{u}">' for h, u in alternos)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{titulo}</title>
  <meta name="description" content="{descripcion}">
  <link rel="canonical" href="{url}">{alt}
  <meta name="theme-color" content="#08271e">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Enlaza Studio">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{titulo}">
  <meta property="og:description" content="{descripcion}">
  <meta property="og:locale" content="{"es_PA" if lang == "es" else "en_US"}">
  <meta property="og:image" content="{imagen}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Enlaza Studio">
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
  <link rel="stylesheet" href="{pre}css/conektra.css?v={V_CSS}">{extra}
</head>
'''


def cabecera(lang, inicio, otra_href, wa, wa_attr, I, LOGO, en_portada=False):
    """inicio: enlace a la portada del idioma ('./' en la propia portada). Los enlaces del menú van a sus secciones."""
    U = UI[lang]
    base = "" if en_portada else inicio
    destinos = [base + "#servicios", base + "#como-funciona", base + "#preguntas"]
    enlaces = "".join(f'<a href="{d}">{t}</a>' for d, t in zip(destinos, U["nav"]))
    return f'''  <div class="lectura" aria-hidden="true"><i id="lectura"></i></div>
  <header class="cabecera{" cabecera--portada" if en_portada else ""}" id="cabecera">
    <div class="contenedor cabecera__barra">
      <a class="marca" href="{inicio}" aria-label="Enlaza Studio">{LOGO}<span>Enlaza Studio</span></a>
      <nav class="menu" id="menu" aria-label="Principal">
        {enlaces}
        <a class="menu__idioma" href="{otra_href}" hreflang="{"en" if lang == "es" else "es"}" lang="{"en" if lang == "es" else "es"}" title="{U["otra_nombre"]}">{U["otra"]}</a>
        <a class="boton boton--menta boton--chico" href="{wa}"{wa_attr}>{I["wa"]} {U["cta"]}</a>
      </nav>
      <button class="hamburguesa" id="hamburguesa" type="button" aria-label="{U["menu"]}" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
'''


def pie(lang, pre, inicio, otra_href, wa, wa_attr, I, LOGO, servicios, privacidad_href, en_portada=False):
    """servicios: lista de (titulo, href)."""
    U = UI[lang]
    base = "" if en_portada else inicio
    serv = "".join(f'<a href="{h}">{t}</a>' for t, h in servicios)
    nav = "".join(f'<a href="{d}">{t}</a>' for d, t in zip([base + "#como-funciona", base + "#preguntas"], U["nav"][1:]))
    return f'''  <footer class="pie-sitio cierre">
    <div class="contenedor">
      <div class="pie-sitio__grid">
        <div class="pie-sitio__marca">
          <a class="marca" href="{inicio}">{LOGO}<span>Enlaza Studio</span></a>
          <p class="pie-sitio__eslogan">{U["eslogan"]}</p>
          <p>{U["desc"]}</p>
        </div>
        <nav aria-label="{U["servicios_t"]}"><h2>{U["servicios_t"]}</h2>{serv}</nav>
        <nav aria-label="{U["nav_t"]}"><h2>{U["nav_t"]}</h2>{nav}<a href="{privacidad_href}">{U["privacidad"]}</a></nav>
        <div class="pie-sitio__contacto"><h2>{U["contacto_t"]}</h2><a class="pie-sitio__wa" href="{wa}"{wa_attr}>{I["wa"]} WhatsApp {TEL}</a><a href="{base}#contacto">{U["form"]}</a>
          <a class="pie-sitio__idioma" href="{otra_href}" hreflang="{"en" if lang == "es" else "es"}">{U["otra_nombre"]} {I["flecha"]}</a></div>
      </div>
      <div class="pie-sitio__base"><span>{U["derechos"]}</span><span>{U["hecho"]}</span></div>
    </div>
  </footer>
  <div class="barra-wa" id="barra-wa" aria-hidden="true">
    <span class="barra-wa__txt"><b>{U["barra_t"]}</b>{U["barra_p"]}</span>
    <a class="boton boton--menta boton--chico" href="{wa}"{wa_attr} tabindex="-1">{I["wa"]} WhatsApp</a>
  </div>
'''
